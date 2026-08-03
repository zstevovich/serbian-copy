#!/usr/bin/env python3
"""Provera da li sprega reci postoji u zivom srpskom jeziku.

Pita CLASSLA-web.sr (2,34 milijarde reci, CC0, CLARIN.SI) preko NoSketch
Engine API-ja i vraca broj pojavljivanja plus stvarne recenice iz korpusa.
Bez naloga, bez kljuca, bez ijedne zavisnosti van standardne biblioteke.

Cemu sluzi: izmisljena kolokacija je gramaticki ispravna i scan_copy.py je ne
vidi. Recenica 'drzi te ravno umesto na skokove' prosla je sve zabrane i skener,
a takva sprega u srpskom ne postoji. Ovaj skript je jedina mehanicka odbrana.

Ulaz je obicna fraza. Skript sam gradi vise oblika upita i uzima najbolji.

    python3 provera_kolokacije.py "drzi budnim" "budnost se razvlaci"
    python3 provera_kolokacije.py --lema "doci sebi"
    python3 provera_kolokacije.py --promocija "ukus koji se pamti"

MREZA: skript zavisi od spoljnog servisa i zato NIJE deo CI testova.
Testira se samo gradnja upita, koja je cista funkcija.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://www.clarin.si/noske/run.cgi/first"
KORPUS = "classlaweb_sr"

# KORPUS: CLASSLA-web.sr 1.0 - 2,34 milijarde reci, 5,26 miliona tekstova, CC0.
# Zamenio je srWaC (555 miliona) iz dva razloga: cetiri puta je veci, i svaki
# tekst nosi oznaku zanra, pa se pretraga moze suziti na promotivne tekstove.
# Zanr dodeljuje X-GENRE klasifikator, dakle automatski i sa greskom - koristan
# je kao filter, ne kao istina o tekstu.
#
# Pragovi su premereni na novom korpusu:
#   potvrdjene   drzati budan 727 | povecavati budnost 130
#                podizati nivo 3761 | ostajati isti 7180
#   izmisljene   budnost razvlaciti 0 | energija bez pad 0
#                kofein skinuti ostrica 0 | fokus popeti 0
#
# Najniza potvrdjena 130, sve izmisljene tacna nula. Razdvajanje je cistije
# nego na srWaC-u, pa prag ostaje na jednom pogotku.
PRAG_POTVRDE = 1

# Lokalni indeks trazi SVOJ prag, visi od servisovog. Servis poredi susedne
# reci; indeks gleda i parove sa dva tokena izmedju, pa hvata i slucajne
# susrete. Izmereno na indeksu od 86,8 miliona sprega:
#   stvarne:    oko sklapati 25 | trebati odmor 129 | drzati budan 154
#               pasti mrak 537  | boleti glava 1030 | doci sebe 5685
#   izmisljene: budnost razvlaciti 0 | fokus popeti 0 | kafa tresti 1
#               energija skakati 3
# Najniza stvarna je 25, najvisa izmisljena 3. Prag 10 razdvaja bez preklapanja.
PRAG_LOKALNI = 10

# STA BROJKA NE RADI: ne bira izmedju dva postojeca izraza.
# 'oci se sklapaju' = 9, 'oci se zatvaraju' = 2. Na 555 miliona reci to je sum,
# a ne razlog da se jedan izraz zameni drugim. Alat odgovara na pitanje DA LI
# sprega postoji, ne koja je bolja. Izbor izmedju postojecih je urednicki.
#
# STA BROJKA POGOTOVO NE RADI: ne kaze REGISTAR.
# srWaC je veb-korpus i mesa registre. 'drhtavica' ima 353 pogotka, a svi
# primeri su medicinski (groznica, jeza, bol) — u prodajnom tekstu zvuci kao
# sirup protiv temperature. 'oci se sklapaju' postoji, ali pripada prozi, ne
# govoru kupca. Zato skript UVEK vraca primere: broj kaze da izraz postoji,
# a tek recenice kazu ko ga i gde izgovara. Ko gleda samo broj, pogresice.

# ZAMKA 1 — lematizacija zamenica i pomocnih reci.
# 'sebi' se u srWaC-u lematizuje kao 'sebe', pa [lemma="sebi"] daje NULU
# iako [lemma="doci"][word="sebi"] daje 606. Naivno lematizovanje svake reci
# proizvodi lazne negative, sto je gore od nikakve provere: pisac odbaci
# ispravan srpski. Zato se uvek probaju i oblici reci, ne samo leme.
#
# ZAMKA 2 — nedovrseno brojanje.
# Prvi odgovor na hladan upit ume da ima finished=0 i delimican concsize
# (izmereno: 99 umesto 606). Zato se upit ponavlja dok finished ne bude 1.

ZAGLAVLJE = {"User-Agent": "srpski-copy-skill/1.0 (provera kolokacije)"}

# Lokalni indeks, ako postoji, radi trenutno i bez mreze. Pravi ga
# napravi_indeks.py iz preuzetog srWaC-a; ne isporucuje se jer je gigabajtski.
def upitaj_lokalno(indeks: Path, fraza: str) -> tuple[int, list[str]]:
    """Trazi par lema u lokalnom indeksu. Vraca (pogodaka, primeri).

    Indeks nosi parove lema, pa se ovde poredi po lemama koje korisnik navede.
    Primera nema — indeks cuva brojeve, ne recenice; za primere ide servis.
    """
    reci = fraza.lower().split()
    if len(reci) < 2:
        return 0, []
    ukupno = 0
    trazeni = {f"{reci[i]} {reci[j]}" for i in range(len(reci)) for j in range(i + 1, len(reci))}
    with indeks.open(encoding="utf-8") as f:
        for red in f:
            delovi = red.split(None, 1)
            if len(delovi) == 2 and delovi[1].rstrip("\n") in trazeni:
                ukupno += int(delovi[0])
    return ukupno, []


def napravi_cql(fraza: str, kao_leme: bool = False, razmak: int = 0) -> str:
    """Gradi CQL iz obicne fraze.

    razmak = koliko tokena sme da stoji izmedju reci (slobodan red reci,
    enklitike i predlozi se cesto ubace izmedju glagola i imenice).
    """
    atribut = "lemma" if kao_leme else "word"
    reci = [r for r in fraza.split() if r]
    if not reci:
        raise ValueError("prazna fraza")
    spoj = f'[]{{0,{razmak}}}' if razmak else ""
    return spoj.join(f'[{atribut}="{r}"]' for r in reci)


def upitaj(cql: str, primeri: int = 2, pokusaja: int = 4) -> tuple[int, list[str]]:
    """Vraca (broj_pogodaka, primeri). Nula znaci stvarno nula, ne gresku."""
    par = urllib.parse.urlencode({
        "corpname": KORPUS, "queryselector": "cqlrow", "cql": cql,
        "format": "json", "pagesize": str(max(primeri, 1)), "viewmode": "kwic",
    })
    zahtev = urllib.request.Request(f"{BASE}?{par}", headers=ZAGLAVLJE)
    for pokusaj in range(pokusaja):
        with urllib.request.urlopen(zahtev, timeout=60) as odgovor:
            podaci = json.load(odgovor)
        if podaci.get("error") == "Empty result":
            return 0, []
        if "concsize" not in podaci:
            raise RuntimeError(f"neocekivan odgovor: {sorted(podaci)[:6]}")
        if podaci.get("finished") or pokusaj == pokusaja - 1:
            return int(podaci["concsize"]), izvuci_primere(podaci, primeri)
        time.sleep(1.5)  # brojanje jos traje, v. ZAMKA 2
    return 0, []


def izvuci_primere(podaci: dict, koliko: int) -> list[str]:
    redovi = []
    for linija in podaci.get("Lines", [])[:koliko]:
        def spoji(kljuc):
            return "".join(x.get("str", "") for x in linija.get(kljuc, []))
        levo, sredina, desno = spoji("Left"), spoji("Kwic"), spoji("Right")
        redovi.append(f"...{levo.strip()[-50:]} [{sredina.strip()}] {desno.strip()[:50]}...")
    return redovi


ZANR_PROMOCIJA = " within <text genre=" + chr(34) + "Promotion" + chr(34) + " />"


def proveri(fraza: str, kao_leme: bool = False, samo_promocija: bool = False) -> dict:
    """Probava vise oblika upita i vraca najbolji pogodak."""
    varijante = [
        ("tacan niz", napravi_cql(fraza, kao_leme=False)),
        ("sa razmakom", napravi_cql(fraza, kao_leme=False, razmak=3)),
    ]
    if kao_leme:
        varijante += [
            ("leme", napravi_cql(fraza, kao_leme=True)),
            ("leme sa razmakom", napravi_cql(fraza, kao_leme=True, razmak=3)),
        ]
    if samo_promocija:
        varijante = [(n, c + ZANR_PROMOCIJA) for n, c in varijante]
    najbolji = {"fraza": fraza, "pogodaka": 0, "varijanta": None,
                "primeri": [], "odgovorio": False}
    for naziv, cql in varijante:
        try:
            broj, primeri = upitaj(cql)
        except (urllib.error.URLError, RuntimeError, TimeoutError, OSError) as greska:
            print(f"    upozorenje: {naziv} nije prosao ({type(greska).__name__})", file=sys.stderr)
            continue
        najbolji["odgovorio"] = True
        if broj > najbolji["pogodaka"]:
            najbolji.update(pogodaka=broj, varijanta=naziv, primeri=primeri)
        time.sleep(0.8)  # ne opterecuj javni akademski servis
    return najbolji


def presudi(nalaz: dict) -> str:
    """POTVRDJENO / NEMA / NEPROVERENO.

    Treci ishod postoji zbog kvara koji je alat imao u prvoj verziji: kada
    servis ne odgovori, svi upiti padnu i rezultat je nula pogodaka — sto se
    ispisivalo isto kao stvarna nula. Pisac bi tada odbacio ISPRAVAN srpski
    zato sto je akademski servis bio nedostupan. Nedostupnost i nepostojanje
    nisu ista stvar i ne smeju da izgledaju isto.
    """
    if not nalaz["odgovorio"]:
        return "NEPROVERENO"
    return "POTVRDJENO" if nalaz["pogodaka"] >= PRAG_POTVRDE else "NEMA"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("fraze", nargs="+", help="fraze za proveru")
    p.add_argument("--lema", action="store_true",
                   help="probaj i lematizovane oblike (fraze navedi u osnovnom obliku)")
    p.add_argument("--promocija", action="store_true",
                   help="trazi samo u promotivnim tekstovima (zanr Promotion)")
    p.add_argument("--indeks", type=Path, default=None,
                   help="lokalni indeks kolokacija (v. napravi_indeks.py); "
                        "bez mreze i trenutno, ali bez primera")
    args = p.parse_args()

    # Lokalni indeks se NE bira sam, iako postoji. Servis daje strogo vise:
    # i broj i prave recenice, a registar se cita iz recenica. Brzina lokalnog
    # indeksa ne vredi gubitka primera, pa se trazi izricito.
    if args.indeks:
        print(f"lokalni indeks: {args.indeks}  (prag {PRAG_LOKALNI})\n")
        for fraza in args.fraze:
            broj, _ = upitaj_lokalno(args.indeks, fraza)
            if broj >= PRAG_LOKALNI:
                ishod = "POTVRDJENO"
            elif broj > 0:
                ishod = "SLUCAJNO"
            else:
                ishod = "NEMA"
            print(f"  {ishod:<11} {broj:>6}  {fraza}")
        print("\nSLUCAJNO znaci par postoji, ali premalo puta da bi bio izraz.")
        print("Indeks nema recenice, samo brojeve — za primere i registar")
        print("pokreni bez --indeks, pa ide servis.")
        return 0

    opseg = "samo promotivni tekstovi" if args.promocija else "ceo korpus"
    print(f"CLASSLA-web.sr preko CLARIN.SI ({opseg})\n")
    sumnjive = 0
    nedostupno = 0
    for fraza in args.fraze:
        nalaz = proveri(fraza, kao_leme=args.lema, samo_promocija=args.promocija)
        ishod = presudi(nalaz)
        if ishod == "NEPROVERENO":
            nedostupno += 1
            print(f"  NEPROVERENO      -  {fraza}")
            continue
        if ishod == "POTVRDJENO":
            print(f"  POTVRDJENO  {nalaz['pogodaka']:>6}  {fraza}   ({nalaz['varijanta']})")
            for red in nalaz["primeri"]:
                print(f"                        {red}")
        else:
            sumnjive += 1
            print(f"  NEMA        {nalaz['pogodaka']:>6}  {fraza}")
    if nedostupno:
        print(f"\n{nedostupno} fraza NIJE provereno — servis nije odgovorio.")
        print("To NIJE isto sto i nula pogodaka. Ne odbacuj izraz na osnovu ovoga;")
        print("probaj kasnije ili presudi urednicki.")
    if sumnjive:
        print(f"\n{sumnjive} fraza bez ijednog pogotka.")
        print("Nula je jak signal da je sprega izmisljena, ali NIJE dokaz:")
        print("proveri i drugi red reci i drugi glagolski oblik pre nego sto odbacis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
