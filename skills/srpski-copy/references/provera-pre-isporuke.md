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

Uz dvotakt prijavljuje i crte (Z1), engleske notacije (Z5), nizanje „bez" (Z9), nulu kao pridev (Z10), metatekst, prazne prideve, prevedene glagole, korporativne imenice i **varijansu dužine rečenica** (ispod 8 znači da su dužine sumnjivo ujednačene, što je samo po sebi mašinski signal).

Tri stvari koje skener po prirodi prijavljuje a nisu uvek greška:

- **Z5 kod izložene brojke.** „2.000+" kao dizajn-element je dozvoljen izuzetak, ali skener ne razlikuje slajd od proze. Proveri gde broj stoji.
- **Z9 u nabrajanju.** Dve stavke sa „bez" su oznake, ne wellness formula. Skener već broji po bloku, pa nabrajanje prolazi ako je svaka stavka u svom redu.
- **Z10 u deklaraciji.** „0 kcal" i „0 g šećera" su izuzeti, ali svaka nova jedinica koja se pojavi u tekstu može da promakne kao kalk.

Zabrane Z3, Z4, Z6, Z7, Z8, Z11 i Z12 skener ne pokriva — prepoznaju se po značenju, pa ostaju na koraku 3 i 4.

Skener ne utvrđuje autorstvo i **nije zamena za uredničku procenu** — daje mesta koja treba pogledati. Rečenice presečene na broju („Od 2026.") ili skraćenici („Infogram d.o.o.") sam preskače i prijavljuje zasebno.

### 2a. Provera skidanjem rime — obavezno za svaku rimovanu i poslovičku liniju

**Skener ovo ne vidi i ne može da vidi.** U validaciji profila namerno su napisani rimovano telo teksta sa iznuđenom besmislenom reči i poslovica sa ubačenim imenom brenda; oba su prošla skener sa **nula nalaza**. Skener meri oblik, a ove greške su u značenju.

Postupak: **prepiši istu misao prozom, bez rime i bez simetrije.**

- ako je nešto izgubljeno — sažetost, poenta, spoj dve reči koji nosi sud — rima je radila i ostaje;
- ako je proza ista — rima je bila ukras i izbacuje se (Z12, „rima radi rime").

Isto važi za poslovičku formu: ako se drugi član može izbaciti bez gubitka, simetrija je lažna. I za oba: ako rečenica oblikom liči na narodnu mudrost a iznosi reklamnu želju, to je parazitiranje na formi, ne postupak.

### 2b. Podvuci subjekte — skener ni ovo ne vidi

Prođi kroz renderovani tekst i podvuci subjekat svake rečenice. **Ako je više od polovine apstraktna imenica** (energija, fokus, budnost, kvalitet, iskustvo, rešenje), tekst je pisan iz engleskog i zvučaće izveštačeno bez obzira na to što je skener čist.

Isto proveri i enklitike: **te, ti, ga, mu, vam**. Tekst na srpskom koji se obraća čoveku a nema nijednu od njih skoro sigurno ima apstrakciju kao vršioca radnje. V. `SKILL.md`, sekcija 1.0.

### 2c. Proveri sprege reči na živom korpusu

Za svaku spregu koju si sam sklopio, a nemaš je u [recnik-obrazaca.md](recnik-obrazaca.md):

```bash
python3 "$SKILL_DIR/scripts/provera_kolokacije.py" "sporna fraza" "još jedna"
```

Pita srWaC (555 miliona reči) i vraća broj pojavljivanja sa stvarnim rečenicama. Nula je jak signal da je sprega izmišljena — na kalibraciji su sve potvrđene imale bar 23 pojavljivanja, a sve izmišljene tačno nulu. **Nula ipak nije dokaz**: probaj drugi red reči i drugi glagolski oblik pre nego što odbaciš izraz.

### 3. Nezavisan svež pogled
Tekst pregleda prolaz koji **nije pisao tekst** — zaseban agent bez radne memorije pisca, sa ovim skillom kao kontrolnom listom. Ovaj korak je u praksi našao 29 nalaza u decku i 28 na sajtu, uključujući greške koje je pisac gledao i nije video.

### 4. Test čitanja naglas
Da li bi ovu rečenicu komercijalista izgovorio na sastanku, bez zastajkivanja? Da li bi je potrošač rekao prijatelju? Ako ne — piši ponovo.

### 5. Vizuelna verifikacija
Svaka izmena se potvrđuje renderom (screenshot stranice ili slajda). Tekst koji se prelama pogrešno nije isporučen tekst. Proveri više širina ekrana — pojedinačna stavka koja ostane sama u novom redu čita se kao kvar.

---
