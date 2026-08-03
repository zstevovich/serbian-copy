# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Šta je ovaj repozitorijum

Ovo nije aplikacija nego **paket jednog Claude Code skilla** — `srpski-copy` (ime iz frontmattera; direktorijum se zove `serbian-copy`). Sadržaj je doktrina za pisanje srpskog marketinškog copy-ja; jedini izvršni kod je heuristički skener od ~130 linija i njegovi testovi.

Zbog toga se rad ovde deli na dve vrste izmena, sa različitim merilom kvaliteta:

- **izmena doktrine** (`SKILL.md`, `references/*.md`) — meri se time da li nova tvrdnja ima potporu u korpusu ili u stvarnoj ispravci, i da li se sudara sa nekim drugim fajlom;
- **izmena skenera** (`scripts/`) — meri se testom koji pada pre izmene i prolazi posle.

Nema build-a, nema paket-menadžera, nema git repozitorijuma. Python 3.9+, samo standardna biblioteka.

## Komande

```bash
# testovi skenera — jedini automatski gate u projektu; isto vrti i CI
python3 skills/srpski-copy/scripts/tests/test_scan_copy.py

# skener nad copy-jem (ulaz: UTF-8 tekst, JEDAN COPY-BLOK PO REDU)
python3 skills/srpski-copy/scripts/scan_copy.py copy.txt

# postoji li sprega reči u živom srpskom (srWaC, 555M reči — traži mrežu)
python3 skills/srpski-copy/scripts/provera_kolokacije.py "drži budnim"
python3 skills/srpski-copy/scripts/tests/test_provera_kolokacije.py
```

`provera_kolokacije.py` zavisi od spoljnog akademskog servisa (CLARIN.SI). U CI-ju se testira **samo gradnja CQL upita**, koja je čista funkcija — pad servisa ne sme da obori build.

Granice redova u ulazu skenera su značajne: dvotakt se traži samo unutar istog reda, jer susedni blokovi (naslov, dugme, oznaka) nisu tok rečenica. Fajl sa prelomom po rečenicama daće lažnu nulu.

Testovi nemaju runner ni izbor pojedinačnog testa — to je jedan skript sa ručnom `proveri()` funkcijom koja izlazi sa kodom 1 ako bilo šta padne. Pojedinačni slučaj se izoluje komentarisanjem ostalih poziva, ne flagom.

Pun postupak provere isporučenog teksta (headless Chrome nad renderovanim DOM-om, grep obrasci, brojanje veznika) stoji u `references/provera-pre-isporuke.md` sa gotovim komandama.

## Arhitektura

### Oblik repozitorijuma

Repo je Claude Code **plugin** koji isporučuje jedan skill:

```
.claude-plugin/plugin.json     # ime plugina: serbian-copy
skills/srpski-copy/            # ime skilla: srpski-copy
├── SKILL.md
├── references/
└── scripts/
```

Plugin i skill se namerno zovu različito: repo je engleski radi pretraživosti na GitHubu, skill zadržava srpsko ime, pa je poziv `/serbian-copy:srpski-copy`. Preimenovanje bilo kog od ta dva lomi i `marketplace.json` u katalog-repou i sve interne putanje — nije kozmetička izmena.

Distribucija ide preko kataloga `zstevovich/claude-plugins` (marketplace ime `zstevovich`), koji je zaseban repo i sadrži samo spisak. Verzija se drži na dva mesta i mora biti ista: `.claude-plugin/plugin.json` ovde i stavka u `marketplace.json` tamo.

### Progresivno otkrivanje

`SKILL.md` (~440 linija, 31,5 KB) je jedini fajl koji se uvek učitava; `references/*.md` (29 fajlova, ~3.400 linija) učitavaju se na zahtev preko linkova iz sekcije „Izbor radnog toka". Svaka tvrdnja koja uđe u `SKILL.md` troši kontekst na svakom pozivu skilla — zato tamo idu samo pravila koja važe za svaki zadatak, a specijalizovano ide u `references/`.

### Tri sloja i redosled prioriteta

`SKILL.md` je namerno složen tako da **zabrane budu poslednje**, a ne prve. Redosled nije kozmetički:

1. **Kapija + radni tok** — bez imenovanog radnog toka, osovine i najviše dva stilistička postupka, tekst se smatra nezapočetim;
2. **SLOJ 1** — srpski jezik (građa duge rečenice, ritam, veznici, obraćanje);
3. **SLOJ 2** — FMCG obrasci mereni na 19 brendova i akademskom korpusu od 2.414 poruka;
4. **SLOJ 3** — registar (B2C / B2B / PR), tabela dozvola;
5. **TVRDE ZABRANE Z1–Z12** — pomoćno sredstvo, nose 15 od 100 poena u rubrici.

Kad predlažeš izmenu, drži ovaj redosled. Dodavanje trinaeste zabrane je najlakši potez i najmanje vredan; ono što nedostaje je po pravilu pozitivan uzor.

### Pravila razrešenja sukoba (već zapisana u fajlovima)

- **Izmereno pobeđuje izvedeno:** autorski profili su „radna verzija 1.0"; kad se sukobe sa Slojem 2, prednost ima Sloj 2.
- **`references/ambalaza-deklaracija.md` nadjačava ceo skill** za obavezni tekst na etiketi — tamo se copy ne popravlja.
- **`references/negative-patterns.md` nosi izuzetke od zabrana.** Model koji učita samo `SKILL.md` radi po strožem pravilniku nego što skill traži; izmena zabrane u jednom fajlu bez drugog stvara upravo taj kvar.
- Zabrane ne važe za uputstva, FAQ odgovore, mikrocopy i obavezni tekst na ambalaži.

### Autorski profili — režim prava

Trinaest profila (`references/autor-*.md` + `references/forma-poslovica.md`), svaki po istom kalupu: status profila → prenosivi postupci → gde se NE koristi → anti-obrasci → primena u webu i u decku → originalni demonstracioni primeri → kontrolna pitanja.

Tri profila su u javnom domenu (poslovička forma, Zmaj, Sremac) i smeju sadržati autentičan tekst za kalibraciju. Za osam zaštićenih autora (`references/stilisticki-izvori.md`, Faza 2: Andrić, Selimović, Crnjanski, Pekić, Ćopić, Radović, Kapor, Kiš) u skill ulaze **samo izvedeni postupci i originalni primeri** — nikad duži odlomci ni prepoznatljive konstrukcije. Ovo je tvrdo pravilo (`references/stilisticki-korpus.md`, „Tvrda pravila"), ne preporuka.

Formulacija „piši kao X" zabranjena je u svakom profilu: ime vodi u pastiš, postupak u sintaksu. Najviše dva profila po tekstu, i ne kao par oni koji dele mehanizam (Andrić+Kiš, Ćopić+Kapor).

### Skener kao treći sloj odbrane, ne kao merilo

`scripts/scan_copy.py` pokriva Z1, Z2, Z5, Z9 i Z10, plus metatekst, prazne prideve, prevedene glagole, korporativne imenice i varijansu dužine rečenica. Z3, Z4, Z6, Z7, Z8, Z11 i Z12 su van domašaja regexa — prepoznaju se po značenju. Ne pokušavaj da ih dodaš bez merenja; jedina prihvatljiva detekcija je ona koja na 83 citata iz `korpus.md` daje nulu. Nula nalaza **nije prolazna ocena** — kvalitet meri `references/evaluation-rubric.md` (100 poena, oblasti A–F, plus lista automatskog odbijanja).

Skener po dizajnu ne razlikuje dvotakt od paralelizma i obrta, pa prijavljuje sva tri; presuda je uvek urednička. Ne „popravljaj" to tako što ćeš praviti pametniju heuristiku bez merenja na korpusu.

## Invarijante pri izmeni skenera

Ovo su mesta gde je izmena koja izgleda bezopasno već jednom bila pogrešna; komentari u kodu nose obrazloženje i ne brišu se uz izmenu koda.

1. **Pragovi su izmereni, ne procenjeni**, i svaki nosi svoje merenje u komentaru iznad sebe. `KRATKA` i `DUZA` (oba 6) mereni su na 83 citata iz `korpus.md` i 6 kanonskih Z2 primera, sa tabelom za vrednosti 6/8/10. `BEZ_PRAG` (2) meren je na istih 83 citata: prag 2 hvata oba kanonska primera uz nula uzbuna, prag 3 hvata samo jedan. Menjaj ih samo sa novim merenjem i ažuriranim komentarom.
2. **Svaka grana detekcije mora imati parnjak koji NE sme da se prijavi.** Test koji ne bi pao da je detekcija pokvarena ne dokazuje ništa — to je eksplicitna doktrina fajla `test_scan_copy.py`.
3. **Poznata slepa tačka je testirana kao slepa.** „Kofeina koliko i u šoljici kafe. Razlika je u L-teaninu." se ne hvata dužinskom heuristikom, i postoji test koji tvrdi da se i dalje ne hvata. Ako je jednog dana uhvatiš, taj test pada namerno — obriši ga svesno, ne mimo.
4. **`SKILL.md` i regexi moraju ostati saglasni.** „premium" namerno nije u `empty_adjectives` jer ga test za anglicizme u `SKILL.md` drži u koloni „ostaje". „više od" ima negativni lookahead i na cifru i na broj napisan rečima, jer je kliše samo ispred kategorije („više od pekare"), ne ispred količine („više od trista objekata"). Izmena reči u `SKILL.md` bez izmene regexa (i obrnuto) je tiho razilaženje.
5. **`FALSE_BREAK`** hvata rečenice presečene na broju ili skraćenici („Od 2026.", „Infogram d.o.o.") — one nisu kratke rečenice nego pola duže.
6. **Ispis skenera je namerno bez dijakritike** (`Stilisticki skener`, `moguci_masinski_dvotakt`), dok je sav dokumentacioni tekst pun srpski sa dijakritikom. Ne „popravljaj" jedno u drugo.

## Konvencije pisanja u ovom repozitorijumu

- **Sve je na srpskom, sa punom dijakritikom.** Izuzetak je ispis skenera (v. gore) i docstring prve linije u `scan_copy.py`.
- **Svako pravilo nosi razlog ili izvor.** Obrasci u `SKILL.md` označeni su brendom („— Jaffa", „— Knjaz Miloš") ili akademskim nalazom; parovi „bilo → ispravljeno" su plaćeni stvarnom ispravkom, ne hipotetički. Nov primer bez izvora slabi ceo fajl.
- **Ispravke se zapisuju kao klasa, ne kao anegdota.** Kad se nađe obrazac (npr. „pa" koje nosi posledicu na devet mesta jednog sajta), u fajl ide pravilo, tabela sredstava za smenjivanje i mera provere — ne samo popravljena rečenica.
- **Linkovi između fajlova su radni mehanizam**, ne dekor: `SKILL.md` rutira na `references/` i model stvarno učitava te fajlove. Preimenovanje fajla lomi rutiranje.

## Dve kopije istog skilla na disku

Pre pakovanja u plugin, skill je ručno kopiran u `~/.claude/skills/srpski-copy/` i **ta kopija je i dalje tamo**. Ona je zatečeno stanje, ne deo ovog repoa, i po instalaciji plugina postaje duplikat koji zaklanja plugin — dva skilla istog imena, od kojih jedan ne prati git.

Kad se izmena „ne uhvati", prvo proveri koju od dve verzije je Claude Code zapravo učitao:

```bash
find ~/.claude -name SKILL.md -path "*srpski-copy*" -exec ls -la {} \;
```

Ne briši ručnu kopiju bez izričite saglasnosti vlasnika projekta. Ako smeta, predloži uklanjanje i sačekaj odgovor.

## Šta ostaje do v1.0

Redosled je namerno ovakav — prvo alat i saglasnost fajlova, pa tek onda najveći posao:

1. ~~Skener na Z5, Z9 i Z10~~ — urađeno u v0.9.1, sa izmerenim pragovima i negativnim parnjakom uz svaku granu.
2. **Rasterećenje `SKILL.md`** — deo doslovne građe iz Sloja 2 pripada u `references/korpus.md`; fajl se učitava na svaki poziv skilla.
3. **Faza 3 validacije profila** (`references/stilisticki-izvori.md`) — trinaest profila × četiri formata. Najveći preostali posao i jedino što stvarno razdvaja v0.9 od v1.0.

## Verzija se drži na dva mesta

`.claude-plugin/plugin.json` ovde i stavka u `marketplace.json` katalog-repoa `zstevovich/claude-plugins`. **Ako se raziđu, korisnik instalira jedno a dobije drugo.** Svaka izmena skilla koja ide u objavu podiže obe, i push ide u oba repoa.
