# Tvrde zabrane — puna razrada

Indeks svih dvanaest zabrana, sa pravilom u jednoj liniji, stoji u `SKILL.md`. Ovde je razrada: tabele, granični slučajevi i obrazloženja.

**Dva mesta gde ovaj fajl nije poslednja reč:**

- **Opseg primene** — na šta zabrane važe a na šta ne (uputstva, FAQ, mikrocopy, deklaracija) stoji u `SKILL.md`, uz indeks. Pročitaj to pre nego što bilo šta ispraviš.
- **Izuzeci** — [negative-patterns.md](negative-patterns.md) nosi slučajeve u kojima obrazac prolazi. Ko primeni samo ovaj fajl, radi po strožem pravilniku nego što skill traži.

**Z2 (mašinski dvotakt) nije ovde** — stoji u celini u `SKILL.md`, jer je od svih dvanaest najteži za presudu i najčešće se koristi.

---

## Z1. Crta (—) koja lomi rečenicu

Najjači pojedinačni signal mašinskog teksta. Rečenica se gradi rečima — kopulom, veznikom, dvotačkom.

| Bilo | Ispravljeno |
|---|---|
| „Radni dan — najveća prilika." | „Radni dan **je** najveća prilika." |
| „ne poseže za limenkom — poseže za kafom" | „ne poseže za limenkom, **nego** za kafom" |
| „radnom danu — poslu, učenju…" | „radnom danu**:** poslu, učenju…" |

**Ne beži od crte tamo gde ima smisla. Meri se upotreba, ne znak.** Crta pada kad **zamenjuje reč koju je pisac trebalo da izabere** — kopulu, veznik, dvotačku — ili kad postane podrazumevani ritam dokumenta. Crta ostaje kad radi posao koji nijedna reč ne radi.

| Crta ostaje | Crta pada |
|---|---|
| opseg (2025–2026, 08:00–16:00) | umesto kopule: „Radni dan — najveća prilika." |
| paginacija i dizajn-element („02 — 13") | umesto veznika: „probali — i poručili ponovo" |
| dijalog u prozi („— A kafa?") | pred poentom, kao najava obrta |
| pravi umetak koji zapeta ne razdvaja jasno | kao razdelnik oznaka, gde ide „·" |
| oznaka vremena ili odeljka („08:00 — jutro") | dva umetka u istoj rečenici |

**Isti obrazac nacrtan CSS-om je isti nalaz.** Crta izvedena kao `<span>` sa `height:1px` čita se identično, a grep nad tekstom je ne vidi. Mehanička pretraga zato ide i kroz CSS — slučaj sa sajta: [primeri.md](primeri.md), „Studija slučaja: crta nacrtana CSS-om".

Za engleski: crta je tamo prirodna figura, ali je istovremeno najprepoznatljiviji AI potpis u tom jeziku. Ista tabela važi — proverava se upotreba, ne broj.

---

## Z3. Zbijeni genitiv po engleskom kalupu

| Bilo | Ispravljeno |
|---|---|
| „kofein jedne kafe" | „kofein **kao u** jednoj kafi" |
| „prilika kategorije" | „prilika **u kategoriji**" |
| „tržište SAD" | „**američko** tržište" |
| „najveća grupa **Baltika**" *(čita se kao firma!)* | „najveća grupa **na Baltiku**" |

---

## Z4. Goli broj bez imenske fraze

„330 ml" → „**limenka od** 330 ml" · „20 minuta: uzorci" → „**Sastanak od** 20 minuta: uzorci"

---

## Z5. Engleske notacije u prozi

„€2M" → „**2 miliona evra**" · „14+ tržišta" → „**više od 14** tržišta" · „~21 kcal" → „**oko** 21 kcal" · „10M+" → „10 miliona" ili „10+ miliona"

Izuzetak: velika izložena brojka kao dizajn-element („2.000+", „300+") — ali prateća proza ide punom frazom. Skener ne razlikuje slajd od proze i prijaviće oba; proveri gde broj stoji.

---

## Z6. Atributivni engleski red reči (imenica kao pridev)

„Brite tim" → „**tim kompanije Brite**" · „Marketing stručnjak" → „**stručnjak za marketing**" · „energy brend" → „**brend energetskih pića**" · „nootropik napitak" → „**prirodni nootropik**"

---

## Z7. Kalkovi izraza i predloga

| Bilo | Ispravljeno |
|---|---|
| „kameno mleveni list" (stone-ground) | red se briše — v. Z8 |
| „ulazak **kroz** REWE" | „ulazak **preko** REWE" |
| „Voće i **bobice**" (berries) | „Voće i **šumski plodovi**" |
| „**delikatesi**" (delis, kao format radnje) | „**prodavnice zdrave hrane** / **specijalizovane radnje**" *(kod nas je delikates pult sa suhomesnatim)* |
| „šta stavljamo na sto" | „šta je na nama" |
| „Energija bez **ljuljaške**" (crash) | „Energija bez **nervoze**" *(ne infantilno, ne medicinski)* |

---

## Z8. Proizvodni detalji i prevedene oznake kvaliteta

Engleski marketing voli teksturu proizvodnje (*stone-ground, shade-grown, small-batch, cold-pressed*) i prevodi je automatski. U srpskom ne prodaje ništa. Red o sastojku kaže **šta sastojak jeste** ili **šta daje**, ne kako je napravljen. Isto za prevedene oznake kvaliteta (*ceremonial grade* → ne „ceremonijalni kvalitet", nego „Japanski čaj u prahu").

---

## Z9. Nizanje „bez, bez, bez"

Engleska wellness formula. Jedno „bez" radi; **već dva u istom pasusu su ritam iz drugog jezika.** „Bez sintetike. Bez preteranih doza." → „Nema sintetike ni preteranih doza, samo biljni ekstrakti odmereni tako da drže ceo radni dan."

Ime pravila kaže tri, ali mera je dva — i to izmereno: na 83 doslovna citata iz [korpus.md](korpus.md) postoji **jedan jedini blok sa „bez" uopšte**, i to sa jednim pojavljivanjem. Dva „bez" u istom pasusu nema uzora u domaćem korpusu.

Nabrajanje je izuzetak: dve susedne stavke sa „bez" su oznake, ne proza. Skener zato broji po bloku, pa nabrajanje prolazi ako je svaka stavka u svom redu.

---

## Z10. Nula kao pridev

„Nula obaveza" (zero obligation) → „**Bez ikakve obaveze**" · „0 kompromisa" → „**bez kompromisa**"

Jedinice iz deklaracije nisu kalk: „0 kcal" i „0 g šećera" su podatak i skener ih izuzima.

---

## Z11. Kolokvijalna slika tela za apstraktan benefit

Benefit se kaže standardnim glagolima: **raste, traje, drži, ostaje**. „budnost koja se **popne**" → „budnost koja **traje**".

---

## Z12. Domaći klišei koje struka vodi kao promašaj

- **„Više od [kategorije]"** — kalk od *more than a X*; ne kaže šta je to više.
- **„Tradicija, cena, kvalitet"** — potrošač ne ume da proceni kvalitet; ovo ne ubeđuje nikoga.
- **„Zabava"** kao vrednost — svakome je nešto drugo zabavno.
- **CSR imperativ „Pokreni X"** — bez intonacije zvuči kao naređenje bogate korporacije.
- **Rima radi rime.**
