#!/usr/bin/env python3
"""Testovi za scan_copy.py.

Pokretanje:  python3 scripts/tests/test_scan_copy.py

Svaka grana skenera se proverava zasebno. Test koji ne bi pao da je detekcija
pokvarena ne dokazuje ništa, pa svaki slučaj ima i parnjak koji NE sme da se
prijavi.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent

spec = importlib.util.spec_from_file_location("scan_copy", SCRIPTS_DIR / "scan_copy.py")
scan_copy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan_copy)

pali: list[str] = []


def proveri(naziv: str, uslov: bool, detalj: str = "") -> None:
    if uslov:
        print(f"  OK   {naziv}")
    else:
        pali.append(naziv)
        print(f"  PAO  {naziv}" + (f" — {detalj}" if detalj else ""))


def dvotakt(text: str) -> list[tuple[str, str]]:
    """Ista logika kao u main(): kratka pa duža, unutar istog bloka."""
    nadjeno = []
    for block in scan_copy.blocks(text):
        ss = scan_copy.sentences(block)
        for a, b in zip(ss, ss[1:]):
            if len(a.split()) <= scan_copy.KRATKA and len(b.split()) >= scan_copy.DUZA:
                if not scan_copy.FALSE_BREAK.search(a):
                    nadjeno.append((a, b))
    return nadjeno


def pogodaka(naziv: str, text: str) -> int:
    return len(scan_copy.PATTERNS[naziv].findall(text))


print("\n== Z2 — dvotakt ==")

# Tri primera koje SKILL.md sam vodi kao Z2. Ako skener ne vidi sopstvene
# primere, ne vidi ništa.
KANONSKI = TESTS_DIR / "dvotakt_mora_pasti.txt"
nadjeni = dvotakt(KANONSKI.read_text(encoding="utf-8"))
proveri(
    "hvata najmanje 5 od 6 kanonskih dvotakta",
    len(nadjeni) >= 5,
    f"nađeno {len(nadjeni)}",
)

# Poznata slepa tačka, dokumentovana u scan_copy.py: druga rečenica je kratka
# („Razlika je u L-teaninu.") pa je dužinska heuristika ne dohvata.
proveri(
    "slepa tačka je i dalje slepa (kratko pa kratko se ne prijavljuje)",
    not any("Razlika je" in b for _, b in nadjeni),
)

# Parnjak: duga pa kratka je ispravan poredak po 1.3 i ne sme da se prijavi.
proveri(
    "duga pa kratka ne pada",
    dvotakt("Kofein budi, a L-teanin smiruje, pa ostane fokus bez nervoze. Toliko.") == [],
)

# Susedni blokovi (naslov pa pasus) nisu tok rečenica.
proveri(
    "granica bloka razdvaja naslov od pasusa",
    dvotakt("Kofein te budi.\nL-teanin tu budnost umiri i izravna.") == [],
)

# Rečenica presečena na skraćenici ili broju nije kratka rečenica.
proveri(
    "lažan prelom na skraćenici se preskače",
    dvotakt("Uvozi ga Infogram d.o.o. Limenka od 330 ml stiže u četiri ukusa danas.") == [],
)

print("\n== Z1 — crta ==")
proveri("hvata crtu", pogodaka("em_dash", "Radni dan — najveća prilika.") == 1)
proveri("ne hvata crticu ni minus", pogodaka("em_dash", "L-teanin, 2025-2026, co-working") == 0)

print('\n== „više od" — kliše naspram količine ==')
proveri("hvata kliše ispred kategorije", pogodaka("template_turn", "Više od energetskog pića.") == 1)
proveri("propušta cifru", pogodaka("template_turn", "više od 10 miliona limenki") == 0)
proveri("propušta broj rečima", pogodaka("template_turn", "više od trista objekata") == 0)
proveri('hvata „nije samo"', pogodaka("template_turn", "Brite nije samo brend.") == 1)

print("\n== prazni pridevi ==")
proveri("hvata prazan pridev", pogodaka("empty_adjectives", "Inovativan i vrhunski proizvod.") == 2)
proveri(
    '„premium" ostaje dozvoljen (v. test za anglicizme u SKILL.md)',
    pogodaka("empty_adjectives", "premium segment") == 0,
)

print("\n== prevedeni glagoli i korporativne imenice ==")
proveri("hvata prevedeni glagol", pogodaka("translated_verbs", "Otključaj svoj potencijal.") == 1)
proveri("hvata nominalizaciju", pogodaka("corporate_nouns", "optimizacija i implementacija") == 2)
proveri("ne hvata običan glagol", pogodaka("translated_verbs", "Probaj i saznaj više.") == 0)

print("\n== rečenice i varijansa ==")
proveri(
    "deli rečenice po tački, upitniku i uzviku",
    len(scan_copy.sentences("Jedan. Dva? Tri! Četiri")) == 4,
)

print()
if pali:
    print(f"PALO: {len(pali)}")
    for naziv in pali:
        print(f"  - {naziv}")
    sys.exit(1)
print("Svi testovi prošli.")
sys.exit(0)
