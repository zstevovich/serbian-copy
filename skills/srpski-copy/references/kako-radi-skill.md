# Kako radi skill — tok od poziva do isporuke

## Kome je namenjen ovaj fajl

Čoveku koji je instalirao plugin i hoće da vidi šta se zapravo dešava između poziva i gotovog teksta. **Ovo je jedini fajl u `references/` koji ne služi pisanju nego razumevanju toka** — model ga ne mora učitati da bi radio, i ne treba da ga učitava usred zadatka.

Primer u drugoj polovini fajla je stvarno izvršen, sa stvarnim izlazom alata, a ne rekonstruisan.

---

## Šta se učita pri pozivu

Kad se skill pozove — bilo izričito preko `/serbian-copy:srpski-copy`, bilo tako što ga Claude sam prepozna po `description` iz frontmattera — u kontekst ulazi **samo `SKILL.md`**.

Svih trideset fajlova u `references/` stoji neučitano. Skill ih povlači tek kad ga tok tamo pošalje, i po pravilu ih po zadatku bude dva do četiri. To je razlog zašto u `SKILL.md` ide samo ono što važi za **svaki** zadatak: svaka tvrdnja koja uđe u taj fajl troši kontekst na svakom pozivu.

## Sedam stanica

```
poziv → GLAS (uzori na početku SKILL.md) → KAPIJA (4 uslova) → radni tok
                                                      ↓
                                              postupci → rečnik
                                                      ↓
                              tri sloja pisanja (jezik → FMCG → registar)
                                                      ↓
                          zabrane → provera (skener, korpus, rubrika) → isporuka
```

Redosled nije kozmetički. Prvo što se učita su **stvarne domaće rečenice**, ne pravila — jer model koji prvo pročita pravilnik zaključi da je posao proveravanje. Korpusna provera je namerno **poslednja**: dok je stajala u kapiji, rečenica se sastavljala iz već odobrenog rečnika i tekst nije mogao da izađe iz proseka.

Kapija je jedina tvrda tačka. Sve ostalo se prilagođava zadatku; dok na sva četiri pitanja nema odgovora, tekst se smatra nezapočetim.

| Stanica | Šta se dešava | Šta se učitava |
|---|---|---|
| **Kapija** | radni tok, osovina, najviše dva postupka, **opklada** | — |
| **Radni tok** | procedura za vrstu zadatka | `web-copy-workflow.md`, `trade-deck-workflow.md`, `editorial-workflow.md`, `forma-poslovica.md`… |
| **Postupci** | najviše dva, birana po tome šta tekstu nedostaje | jedan do dva `autor-*.md` |
| **Rečnik** | potvrđene sprege reči po tome šta hoćeš da kažeš | `recnik-obrazaca.md`, `korpus.md` |
| **Tri sloja** | jezik → FMCG obrasci → registar | u `SKILL.md` |
| **Zabrane** | dvanaest pravila koja čuvaju pod | `zabrane.md`, `negative-patterns.md` |
| **Provera** | skener, kolokacije, rubrika, čitanje naglas | `provera-pre-isporuke.md`, `evaluation-rubric.md` |

---

## Primer: „napiši slogan za B2B kupce"

Brend je Brite (funkcionalno piće), format je naslovna strana decka koji ide trgovinskim lancima.

### 1. Kapija

| Pitanje | Odgovor |
|---|---|
| **Koji radni tok?** | Slogan → `forma-poslovica.md`. `SKILL.md` izričito šalje ovamo, **ne** na autorske profile. B2B kontekst → `trade-deck-workflow.md`, slajd 1. |
| **Koja osovina?** | *Trgovac poseže za ovim kada mu kategorija raste a polica stoji ista, jer želi rotaciju po metru police, ali ne želi da mu nov artikal stoji i pravi otpis.* |
| **Koja dva postupka?** | Binarna simetrija (poslovička forma, postupak 1) i konkretna imenica umesto pojma (postupak 8). |
| **Šta rizikuje?** | Kladi se da će kategorijski menadžer prepoznati problem otpisa, iako mu ne kažemo nijednu brojku o rotaciji — brief je nema. Rečnik za građu: `recnik-obrazaca.md`, grupe „Brend govori o sebi" i „Obrt X nije Y, X je Z". |

### 2. Registar gasi jedan postupak pre pisanja

Poslovička forma nudi **rimu** kao postupak 6. Tabela Sloja 3 u B2B koloni piše: dosetke i igre reči — zabranjeno, humor — ne. I sam profil nosi ogradu „NE KORISTITI U: B2B deck".

Rima ispada pre nego što je napisana. Ovo je radni primer redosleda slojeva: **registar nadjačava postupak**, a ne obrnuto.

### 3. Kandidati i presude

| Kandidat | Presuda |
|---|---|
| „Ko drži policu, drži i kategoriju." | **Pada.** Anti-obrazac 5 poslovičke forme: simetrija bez sadržaja — drugi deo ne dodaje ništa proverljivo. |
| „Premium piće koje se samo prodaje." | **Pada.** Doslovno na listi „ne govori se" u rečniku, i to zato što je nađeno na živom sajtu. Pred trgovcem je tvrdnja koju kupac obori u sebi. |
| „Brzo se okreće, lako se drži." | **Pada.** „Drži" je dvosmisleno — drži se na polici ili držite zalihu. Gramatika bez izuzetka, pravilo 4. |
| „Metar police se ne poklanja. Zarađuje se." | **Pada urednički.** Skener je propustio: druga rečenica ima dve reči, ispod praga `DUZA`. Slepa tačka zapisana u kodu, ne propust. |
| **„Ne tražimo policu, nego rotaciju."** | **Prolazi.** |

### 4. Zašto je pobednik prošao

Obrt „X nije Y, X je Z" radi samo kad je drugi član **konkretniji** od prvog: polica je mesto, rotacija je brojka. Da je bilo obrnuto — „ne tražimo policu, nego partnerstvo" — pao bi po istom pravilu koje obara „više od energetskog pića" (Z12).

Elipsa nosi drugi deo: glagol se ne ponavlja. Dve konkretne imenice, nula apstrakcija, nula superlativa, nula obraćanja na „ti" (B2B).

### 5. Izlaz i alati

```
Ne tražimo policu, nego rotaciju.
Kategorija raste [potreban podatak: rast kategorije] odsto godišnje, a polica se nije promenila.
Brite popunjava mesto koje kupac već traži, pa se metar police vraća kroz obrt, a ne kroz maržu na komad.
```

Skener: **0 mehaničkih nalaza.**

Ranija verzija drugog reda glasila je „Kategorija raste 14+ posto — polica se nije promenila" i pala je na dva mesta:

```
- em_dash: 1 (—)
- z5_notacije: 1 (14+)
```

Brojka je označena kao `[potreban podatak: …]`, ne izmišljena. Skill ne pokreće proveru činjenica sam, ali ni ne popunjava rupu iz briefa.

**Provera kolokacija nije prošla** — CLARIN.SI je u trenutku pisanja bio nedostupan (DNS se razrešava, port 443 odbija vezu). Alat je vratio treću presudu:

```
NEPROVERENO   -  traži ga kupac
To NIJE isto sto i nula pogodaka. Ne odbacuj izraz na osnovu ovoga.
```

Ta razlika je bila kvar u prvoj verziji alata i popravljena je u v1.5. Bez nje bi ispravan srpski bio odbačen zato što je akademski servis bio dole. Za „tražiti rotaciju" presuda je ostala urednička.

---

## Šta se iz primera vidi

Od šest kandidata pet je palo, i **nijedan nije pao na skeneru.** Pali su na rečniku, na anti-obrascu profila, na dvosmislenosti i na uredničkoj presudi. Skener je uhvatio samo crtu i „14+" — najlakše greške u celom skupu.

Zato zabrane nose 15 od 100 poena u `evaluation-rubric.md`. Nula na skeneru znači odsustvo grubih grešaka, ne dobar tekst.

## Gde tok najčešće pukne

1. **Preskočena kapija.** Znak: prva verzija izgleda gotovo, a ne umeš da kažeš odakle joj ritam. Tada je ritam engleski, i nijedna dalja provera to ne otkriva.
2. **Uzeta struktura iz profila, izmišljen rečnik.** Najteži kvar u poslu, jer je gramatički ispravan i nevidljiv skeneru. Profil daje potez, rečnik daje reči — nijedno ne zamenjuje drugo.
3. **Nula na skeneru shvaćena kao prolazna ocena.** Kvalitet meri rubrika, oblastima A, B i C, koje zajedno nose 55 poena.
