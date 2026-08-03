#!/usr/bin/env python3
"""Testovi za provera_kolokacije.py.

Pokretanje:  python3 scripts/tests/test_provera_kolokacije.py

MREZA SE NE DIRA. Testira se samo gradnja CQL upita, koja je cista funkcija.
Poziv ka srWaC-u zavisi od spoljnog akademskog servisa i nema mesta u CI-ju:
pad servisa ne sme da obori build.

Kao i u test_scan_copy.py, svaki slucaj ima parnjak koji NE sme da prodje.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent

spec = importlib.util.spec_from_file_location("pk", SCRIPTS_DIR / "provera_kolokacije.py")
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)

pali: list[str] = []


def proveri(naziv: str, uslov: bool, detalj: str = "") -> None:
    if uslov:
        print(f"  OK   {naziv}")
    else:
        pali.append(naziv)
        print(f"  PAO  {naziv}" + (f" — {detalj}" if detalj else ""))


print("\n== gradnja CQL-a ==")

proveri(
    "dve reci kao oblici",
    pk.napravi_cql("drži budnim") == '[word="drži"][word="budnim"]',
    pk.napravi_cql("drži budnim"),
)
proveri(
    "dve reci kao leme",
    pk.napravi_cql("držati budan", kao_leme=True) == '[lemma="držati"][lemma="budan"]',
    pk.napravi_cql("držati budan", kao_leme=True),
)
# Parnjak: bez kao_leme ne sme da se pojavi atribut lemma.
proveri(
    "oblici ne proizvode lemma atribut",
    "lemma" not in pk.napravi_cql("drži budnim"),
)
proveri(
    "razmak ubacuje prazne tokene",
    pk.napravi_cql("drži budnim", razmak=3) == '[word="drži"][]{0,3}[word="budnim"]',
    pk.napravi_cql("drži budnim", razmak=3),
)
# Parnjak: bez razmaka nema praznog tokena.
proveri("bez razmaka nema []{}", "[]{" not in pk.napravi_cql("drži budnim"))

proveri(
    "jedna rec je validan upit",
    pk.napravi_cql("budnost") == '[word="budnost"]',
)
proveri(
    "visak razmaka se ignorise",
    pk.napravi_cql("  drži   budnim  ") == '[word="drži"][word="budnim"]',
)

greska = False
try:
    pk.napravi_cql("   ")
except ValueError:
    greska = True
proveri("prazna fraza puca umesto da vrati prazan upit", greska)

print("\n== presuda: nedostupno nije isto sto i nepostojece ==")
# Kvar iz prve verzije: kad servis ne odgovori, svi upiti padnu i rezultat je
# nula — sto se ispisivalo isto kao stvarna nula. Pisac bi odbacio ispravan
# srpski zato sto je servis bio dole.
proveri(
    "servis nije odgovorio -> NEPROVERENO",
    pk.presudi({"odgovorio": False, "pogodaka": 0}) == "NEPROVERENO",
)
# Parnjak: servis JESTE odgovorio i vratio nulu -> to je stvarna nula.
proveri(
    "servis odgovorio sa nulom -> NEMA",
    pk.presudi({"odgovorio": True, "pogodaka": 0}) == "NEMA",
)
proveri(
    "servis odgovorio sa pogotkom -> POTVRDJENO",
    pk.presudi({"odgovorio": True, "pogodaka": 33}) == "POTVRDJENO",
)
# Parnjak koji cuva smisao praga: jedan pogodak je vec potvrda.
proveri(
    "jedan pogodak je dovoljan",
    pk.presudi({"odgovorio": True, "pogodaka": 1}) == "POTVRDJENO",
)

print("\n== prag ==")
# Merenje u zaglavlju skripta: sve izmisljene sprege dale su tacnu nulu,
# sve potvrdjene bar 23. Prag zato razdvaja nulu od svega ostalog.
proveri("prag je postavljen na jedan pogodak", pk.PRAG_POTVRDE == 1)

print()
if pali:
    print(f"PALO: {len(pali)}")
    for naziv in pali:
        print(f"  - {naziv}")
    sys.exit(1)
print("Svi testovi prošli.")
sys.exit(0)
