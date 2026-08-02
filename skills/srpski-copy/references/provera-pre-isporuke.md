# Provera pre isporuke

Obavezno, redom:

### 1. Mehanička pretraga
Nad **renderovanim DOM-om**, ne nad izvorom — mašinski jezik preživljava tamo gde tekst nema prevodni ključ ili je hardkodovan.

```bash
# HTML stranica
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --virtual-time-budget=9000 \
  --dump-dom "file:///putanja/index.html" > /tmp/dom.html

grep -c "—" /tmp/dom.html                 # crta u vidljivom tekstu
grep -n "€[0-9]" /tmp/dom.html            # notacija
grep -nE "[0-9]+\+" /tmp/dom.html         # sufiks + u prozi
grep -niE "napitak|užitak|besprekorno|širok asortiman" /tmp/dom.html

# jedan veznik nosi sve veze (v. 1.2) — prebroj po funkciji.
# grep -E nema lookbehind, a \b puca na dijakritici, pa ide python:
python3 -c 'import re,sys; s=open(sys.argv[1],encoding="utf-8").read(); \
print(len(re.findall(r"(?<![\wčćžšđČĆŽŠĐ])pa(?![\wčćžšđČĆŽŠĐ])", s)))' /tmp/dom.html

# crta nacrtana CSS-om: inline element između reči
grep -nE "height:\s*1px" styles.css | grep -v border
```

Posebno pretraži **vidljive tekstove bez `data-i18n` atributa** (ili bez prevodnog ključa u drugom sistemu) — tu se kriju zaostale engleske reči.

### 2. Brojanje mašinskih obrazaca
Prebroj mesta gde kratka rečenica (≤6 reči) stoji ispred duže u istom bloku. To je dvotakt (Z2). Cilj: nula u prozi.

Za to postoji skener — [../scripts/scan_copy.py](../scripts/scan_copy.py), relativno uz `SKILL.md` ovog skilla. Ulaz je običan tekst, **jedan copy-blok po redu**:

```bash
python3 "$SKILL_DIR/scripts/scan_copy.py" copy.txt
```

`$SKILL_DIR` je direktorijum u kome stoji `SKILL.md`. Skill se instalira na tri načina i putanja se razlikuje, pa ako ne znaš odakle je učitan, nađi skener umesto da pogađaš:

```bash
SCAN=$(find ~/.claude .claude -name scan_copy.py -path "*srpski-copy*" 2>/dev/null | head -1)
python3 "$SCAN" copy.txt
```

Pokriva sva tri slučaja: plugin (`~/.claude/plugins/…`), globalni skill (`~/.claude/skills/…`) i skill u projektu (`.claude/skills/…`).

Uz dvotakt prijavljuje i crte, metatekst, prazne prideve, prevedene glagole, korporativne imenice i **varijansu dužine rečenica** (ispod 8 znači da su dužine sumnjivo ujednačene, što je samo po sebi mašinski signal).

Skener ne utvrđuje autorstvo i **nije zamena za uredničku procenu** — daje mesta koja treba pogledati. Rečenice presečene na broju („Od 2026.") ili skraćenici („Infogram d.o.o.") sam preskače i prijavljuje zasebno.

### 3. Nezavisan svež pogled
Tekst pregleda prolaz koji **nije pisao tekst** — zaseban agent bez radne memorije pisca, sa ovim skillom kao kontrolnom listom. Ovaj korak je u praksi našao 29 nalaza u decku i 28 na sajtu, uključujući greške koje je pisac gledao i nije video.

### 4. Test čitanja naglas
Da li bi ovu rečenicu komercijalista izgovorio na sastanku, bez zastajkivanja? Da li bi je potrošač rekao prijatelju? Ako ne — piši ponovo.

### 5. Vizuelna verifikacija
Svaka izmena se potvrđuje renderom (screenshot stranice ili slajda). Tekst koji se prelama pogrešno nije isporučen tekst. Proveri više širina ekrana — pojedinačna stavka koja ostane sama u novom redu čita se kao kvar.

---
