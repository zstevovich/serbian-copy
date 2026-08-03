#!/usr/bin/env python3
"""Pravi lokalni indeks kolokacija iz srWaC korpusa. Pokrece se JEDNOM.

Zasto lokalno a ne isporuceno: izmereno je da tabela ne moze u paket.
Puna tabela je oko 2,4 GB, filtrirana po vokabularu od 2.500 lema oko 300 MB,
a prag ucestalosti odbacuje dugi rep u kome zive izrazi koji nam trebaju
('drzi budnim' ima 33 pojavljivanja u celom korpusu, 'oci se sklapaju' devet).
Zato se indeks gradi kod korisnika, a u paket ide samo ovaj skript.

Korpus: srWaC 1.1, CC BY-SA 4.0, http://hdl.handle.net/11356/1063
Preuzimanje je otvoreno, bez naloga; sest fajlova, oko 3,6 GB.

    python3 napravi_indeks.py ~/Projects/Other/skills/korpus/srwac

Rezultat je sortirana tabela pored korpusa. Traje desetak minuta po delu i
zauzima nekoliko gigabajta — sve van git repoa.

VAZNO: ulaze SVE reci, ne samo punoznacne. Prva verzija je zadrzavala samo
imenice, glagole, prideve i priloge, pa je bila slepa za zamenice — a cela
sekcija 1.0 u SKILL.md je o enklitikama (te, ti, ga, mu, se). Provera koja
ne vidi 'doci sebi' ne sluzi nicemu.
"""
from __future__ import annotations

import argparse
import gzip
import subprocess
import sys
from pathlib import Path

# Koliko tokena sme izmedju dve reci u paru. Dva pokriva slucaj kada se izmedju
# glagola i imenice ubaci enklitika ili predlog: 'drzi te budnim', 'doci k sebi'.
MAX_RAZMAK = 2


def emituj_parove(putanje: list[Path], izlaz) -> int:
    recenica = 0
    for putanja in putanje:
        with gzip.open(putanja, "rt", encoding="utf-8", errors="replace") as ulaz:
            tokeni: list[str] = []
            for red in ulaz:
                if red.startswith("</s>"):
                    for i in range(len(tokeni)):
                        for razmak in range(1, MAX_RAZMAK + 1):
                            j = i + razmak
                            if j < len(tokeni):
                                izlaz.write(f"{tokeni[i]} {tokeni[j]}\n")
                    recenica += 1
                    if recenica % 1_000_000 == 0:
                        print(f"  ...{recenica // 1000}k recenica", file=sys.stderr)
                    tokeni = []
                elif red.startswith("<"):
                    continue
                else:
                    delovi = red.rstrip("\n").split("\t")
                    if len(delovi) >= 3:
                        lema = delovi[2].lower()
                        if lema.isalpha():
                            tokeni.append(lema)
        print(f"  gotov {putanja.name}", file=sys.stderr)
    return recenica


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("korpus", type=Path, help="direktorijum sa srWaC1.1.*.xml.gz")
    p.add_argument("--izlaz", type=Path, default=None,
                   help="putanja indeksa (podrazumevano: kolokacije.tsv pored korpusa)")
    args = p.parse_args()

    delovi = sorted(args.korpus.glob("srWaC1.1.*.xml.gz"))
    if not delovi:
        print(f"nema srWaC fajlova u {args.korpus}", file=sys.stderr)
        return 1
    indeks = args.izlaz or args.korpus / "kolokacije.tsv"
    privremeno = args.korpus / "_sort_tmp"
    privremeno.mkdir(exist_ok=True)

    print(f"delova: {len(delovi)}  ->  {indeks}", file=sys.stderr)

    # Brojanje ide preko sortiranja na disku. Recnik sa desetinama miliona
    # kljuceva ne staje u memoriju, a spoljasnje sortiranje staje uvek.
    cev = subprocess.Popen(
        f'LC_ALL=C sort -S 2G -T "{privremeno}" | LC_ALL=C uniq -c '
        f'| LC_ALL=C sort -rn -S 1G -T "{privremeno}" > "{indeks}"',
        shell=True, stdin=subprocess.PIPE, text=True,
    )
    try:
        recenica = emituj_parove(delovi, cev.stdin)
    finally:
        cev.stdin.close()
        cev.wait()

    velicina = indeks.stat().st_size / 1_048_576
    print(f"\nindeks gotov: {velicina:.0f} MB, iz {recenica} recenica", file=sys.stderr)
    print(f"pretraga: python3 provera_kolokacije.py --indeks {indeks} \"drzi budnim\"",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
