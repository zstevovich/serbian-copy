#!/usr/bin/env python3
"""Heuristic scanner for Serbian marketing copy.

It flags mechanical patterns for editorial review. It does not determine AI authorship.

Ulaz: UTF-8 tekst ili Markdown, jedan copy-blok po redu.
Granice redova su značajne — dvotakt se traži SAMO unutar istog bloka, jer
susedni blokovi (naslov, dugme, oznaka) nisu tok rečenica.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERNS = {
    "em_dash": re.compile(r"—"),
    "meta_text": re.compile(
        r"\b(važno je (?:napomenuti|istaći)|ključ je u tome|vredi napomenuti|sve u svemu|zaključno|na kraju dana)\b",
        re.I,
    ),
    # „premium" namerno NIJE ovde: SKILL.md ga u testu za anglicizme drži u koloni
    # „ostaje" jer „premium segment" trgovci stvarno govore.
    "empty_adjectives": re.compile(
        r"\b(inovativan|inovativna|moderan|moderna|jedinstven|jedinstvena|vrhunski|savršena|savršeno|autentičan|besprekorno)\b",
        re.I,
    ),
    # „više od" je kliše samo ispred kategorije („više od pekare"), ne ispred količine
    # („više od 10 miliona limenki", „više od trista objekata") — otud negativni lookahead
    # i na cifru i na broj napisan rečima.
    "template_turn": re.compile(
        r"(?:\bnije samo\b|\bnije pitanje da li\b|\bs jedne strane\b|\bs druge strane\b"
        r"|\bviše od\b(?!\s+(?:\d|jedn|dv|tri|četiri|pet|šest|sedam|osam|devet|deset|"
        r"jedanaest|dvanaest|dvadeset|trideset|četrdeset|pedeset|šezdeset|sedamdeset|"
        r"osamdeset|devedeset|sto|dvesta|trista|hiljad|milion|milijard|pola|polovin)))",
        re.I,
    ),
    "translated_verbs": re.compile(
        r"\b(otključaj|otključava|osnaži|osnažuje|redefiniše|transformiše|podigni iskustvo)\b", re.I
    ),
    "corporate_nouns": re.compile(
        r"\b(unapređenje|optimizacija|implementacija|pozicioniranje|osnaživanje|transformacija)\b", re.I
    ),
}

# Prag za Z2. Kratka rečenica ispred duže je dvotakt; obe granice su na 6 reči
# jer je to mera kojom SKILL.md meri isti obrazac u sekciji „Provera pre isporuke".
#
# Prag je izmeren, ne procenjen. Na 83 doslovna domaća citata iz korpus.md i na
# šest kanonskih Z2 primera iz SKILL.md:
#   DUZA=6  -> hvata 5 od 6 primera, 7 uzbuna na korpusu
#   DUZA=8  -> hvata 4 od 6 primera, 6 uzbuna
#   DUZA=10 -> hvata 2 od 6 primera, 4 uzbune
# Ranija vrednost 10 propuštala je i tri primera koja SKILL.md sam vodi kao Z2.
#
# Poznata slepa tačka: kratka rečenica koja prepričava prethodnu, a i sama je
# kratka („Kofeina koliko i u šoljici kafe. Razlika je u L-teaninu.") ne može se
# uhvatiti dužinom. Nju traži urednik, ne skener.
KRATKA = 6
DUZA = 6

# Rečenica presečena na broju („Od 2026.") ili skraćenici („Infogram d.o.o.")
# nije kratka rečenica nego pola duže; takav pogodak je lažan.
FALSE_BREAK = re.compile(
    r"(?:\d+|\b(?:d\.o\.o|a\.d|o\.d|dr|mr|prof|inž|itd|npr|god|str|tj|tzv|čl|br|hilj|mil)\.?)\.$",
    re.I,
)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def blocks(text: str) -> list[str]:
    return [b.strip() for b in text.splitlines() if b.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="UTF-8 text or Markdown file")
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8")

    print("Stilisticki skener (ne utvrdjuje AI autorstvo)\n")
    total = 0
    for name, pattern in PATTERNS.items():
        matches = list(pattern.finditer(text))
        if matches:
            total += len(matches)
            examples = ", ".join(sorted({m.group(0) for m in matches}, key=str.lower)[:6])
            print(f"- {name}: {len(matches)} ({examples})")

    all_sentences: list[str] = []
    short_then_long: list[tuple[str, str]] = []
    skipped_false = 0
    for block in blocks(text):
        ss = sentences(block)
        all_sentences.extend(ss)
        for a, b in zip(ss, ss[1:]):
            if len(a.split()) <= KRATKA and len(b.split()) >= DUZA:
                if FALSE_BREAK.search(a):
                    skipped_false += 1
                else:
                    short_then_long.append((a, b))

    if short_then_long:
        total += len(short_then_long)
        print(f"- moguci_masinski_dvotakt: {len(short_then_long)}")
        for a, b in short_then_long[:5]:
            print(f"  * {a} | {b}")
    if skipped_false:
        print(f"- preskoceno kao lazan prelom (broj ili skracenica): {skipped_false}")

    lengths = [len(s.split()) for s in all_sentences]
    if len(lengths) >= 5:
        avg = sum(lengths) / len(lengths)
        variance = sum((x - avg) ** 2 for x in lengths) / len(lengths)
        print(f"- recenice: {len(lengths)}, prosek_reci: {avg:.1f}, varijansa: {variance:.1f}")
        if variance < 8:
            print("  * upozorenje: duzine recenica su veoma ujednacene")

    print(f"\nUkupno mehanickih nalaza: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
