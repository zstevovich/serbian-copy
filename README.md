# serbian-copy

**Claude Code skill za pisanje i lekturu srpskog marketinškog copy-ja** — sajt, deck, PR, social, opisi proizvoda, slogani.

> *A Claude Code skill for writing and editing Serbian-language marketing copy. The skill itself, and all of its documentation, is written in Serbian — that is the point of it. Everything below is in Serbian.*

---

## Problem koji rešava

Model koji piše srpski marketinški tekst „iz sebe" proizvodi **prevodilaštinu**: gramatički ispravan srpski koji je zapravo engleska rečenica sa srpskim rečima. Uzrok je uvek isti — kreće se od engleske slike pa se traži srpska reč za nju.

Ovaj skill okreće smer. Ne radi kao spisak zabrana nego kao **pozitivan uzor**: doslovna građa iz domaćeg copy-ja, pravila za građenje duge srpske rečenice, i tek na kraju zabrane koje čuvaju pod.

Zabrane su namerno poslednje i nose 15 od 100 poena u evaluacionoj rubrici. Tekst koji je prošao svih dvanaest zabrana i nula puta pogodio skener i dalje može biti prazan — što je i bio razlog da skill nastane.

## Instalacija

```
/plugin marketplace add zstevovich/claude-plugins
/plugin install serbian-copy@zstevovich
```

Posle toga je skill dostupan u svakom projektu kao `/serbian-copy:srpski-copy`, a Claude ga sam poziva kad prepozna zadatak pisanja ili lekture srpskog marketinškog teksta.

Nadogradnja ide preko `/plugin update serbian-copy@zstevovich`.

<details>
<summary>Ručna instalacija bez marketplace-a</summary>

```bash
git clone https://github.com/zstevovich/serbian-copy.git
cp -r serbian-copy/skills/srpski-copy ~/.claude/skills/     # globalno
# ili, samo za jedan projekat:
cp -r serbian-copy/skills/srpski-copy .claude/skills/
```

Ovako nema automatske nadogradnje — plugin put je preporučen.
</details>

## Šta pokriva

| Zadatak | Šta skill radi |
|---|---|
| Web sajt FMCG brenda | radni tok od briefa do strukture sajta, tri prolaza pisanja |
| B2B deck za trgovinske lance | narativ, dvanaest slajdova, pravila naslova, odnos teksta i dokaza |
| Ambalaža i deklaracija | odvaja obavezni tekst od slobodnog; obavezni se ne „popravlja" |
| Lektura i prerada | dijagnostika obrazaca, mapa očuvanja, kontrola gubitaka |
| Slogan i kratka forma | poslovička sintaksa — simetrija, elipsa, asindet, gradacija |
| Ocena teksta | rubrika od 100 poena sa listom automatskog odbijanja |

Uz to: trinaest stilističkih profila izvedenih iz srpske proze (Andrić, Kiš, Selimović, Crnjanski, Pekić, Ćopić, Nušić, Domanović, Radović, Kapor, Zmaj, Sremac, poslovička forma), od kojih se biraju najviše dva po tekstu — i to po **postupku koji tekstu nedostaje**, nikad po imenu pisca.

## Šta ne pokriva

- **Nije detektor AI teksta.** Ni skill ni skener ne utvrđuju autorstvo, nego prepoznaju obrasce koji proizvode neprirodan tekst.
- **Ne piše na engleskom** i ne prevodi. Engleski original sme biti izvor činjenica, nikad izvor jezika.
- **Ne dira obavezni tekst na deklaraciji** — tamo je zakon, ne copy.
- **Nije zamena za lektora.** Skener daje mesta koja treba pogledati; presuda je urednička.

## Skener

```bash
python3 skills/srpski-copy/scripts/scan_copy.py copy.txt
```

Ulaz je UTF-8 tekst ili Markdown, **jedan copy-blok po redu** — granice redova su značajne, jer susedni blokovi (naslov, dugme, oznaka) nisu tok rečenica.

Meri mašinski dvotakt (Z2), crte (Z1), engleske notacije (Z5), nizanje „bez" (Z9), nulu kao pridev (Z10), metatekst, prazne prideve, prevedene glagole, korporativne imenice i varijansu dužine rečenica.

Pragovi nisu procenjeni nego **izmereni na 83 doslovna citata iz domaćeg korpusa**, uz uslov da nijedna grana ne sme da opali na autentičnom srpskom: deklaracija („0 kcal", „99 mg", „250 ml"), skraćenice („B2B"), velike brojke („12.000") i jedno „bez" prolaze čiste. Obrazloženje svakog praga stoji u komentarima uz kod.

Zabrane Z3, Z4, Z6, Z7, Z8, Z11 i Z12 skener ne pokriva — prepoznaju se po značenju, ne po obliku.

Samo standardna biblioteka, Python 3.9+.

## Struktura

```
skills/srpski-copy/
├── SKILL.md              # doktrina: kapija, tri sloja, dvanaest zabrana
├── references/           # radni tokovi, korpus, zabrane, profili, rubrika, rečnik obrazaca (29 fajlova)
└── scripts/
    ├── scan_copy.py              # mašinski obrasci u tekstu
    ├── provera_kolokacije.py     # postoji li ova sprega reči u živom srpskom
    ├── napravi_indeks.py         # opciono: lokalni indeks za rad bez mreže
    └── tests/
```

`provera_kolokacije.py` pita **CLASSLA-web.sr** (2,34 milijarde reči, CC0) preko otvorenog API-ja na CLARIN.SI — bez naloga i bez ičega za instalaciju. Svaki tekst u tom korpusu nosi oznaku žanra, pa prekidač `--promocija` sužava pretragu na tekstove koji nešto nude.

Za rad bez mreže postoji `napravi_indeks.py`, ali **gotova tabela se ne isporučuje**: merenjem je utvrđeno da svaka verzija koja bi stala u paket odbacuje upravo retke izraze zbog kojih alat i postoji.

Skener hvata oblik. Ono što ne hvata — izmišljenu kolokaciju, iznuđenu rimu, apstrakciju umesto čoveka u rečenici — pokrivaju `provera_kolokacije.py` i koraci 2a–2c u `references/provera-pre-isporuke.md`.

`SKILL.md` se učitava uvek, `references/` po potrebi — zato u `SKILL.md` ide samo ono što važi za svaki zadatak.

## Građa i prava

Doktrina, primeri i kod su originalni i pod MIT licencom.

Skill sadrži i **kratke doslovne citate** sa sajtova 19 domaćih brendova (Jaffa, Plazma, Knjaz Miloš, Cedevita, Smoki, Štark, Grand kafa, Nectar i drugi), navedene uz izvor i korišćene za analizu jezičkog obrasca. Ti citati nisu vlasništvo autora ovog repozitorijuma i nisu obuhvaćeni MIT licencom — stoje po pravu citiranja, sa atribucijom.

Stilistički profili zaštićenih autora sadrže **samo izvedene postupke i originalne demonstracione primere**. Nijedan duži odlomak ni prepoznatljiva konstrukcija iz zaštićenog dela nije uključena, i to je tvrdo pravilo projekta, ne preporuka.

Akademski izvor za empirijske nalaze: Silva M. Kostić, „Strategije obraćanja u diskursu reklamnih poruka", doktorska disertacija, Filološki fakultet UB, 2023 (korpus 2.414 reklamnih poruka, 2016–2022).

## Razvoj

```bash
python3 skills/srpski-copy/scripts/tests/test_scan_copy.py
```

Svaka grana detekcije ima parnjak koji **ne sme** da se prijavi — test koji ne bi pao da je detekcija pokvarena ne dokazuje ništa. Pravila za izmenu skenera i doktrine stoje u [CLAUDE.md](CLAUDE.md).

## Status

**v1.7.** U upotrebi na stvarnim projektima.

Put do ovde:

- **v0.9** — spakovan kao plugin koji se instalira na bilo koji projekat;
- **v0.9.1** — skener proširen na Z5, Z9 i Z10, sa izmerenim pragovima;
- **v0.9.2** — `SKILL.md` rasterećen sa 36,5 na 31,5 KB, bez izgubljenog sadržaja;
- **v1.0** — svih trinaest profila prošlo primenu na četiri formata; pet izmenjeno na osnovu nalaza;
- **v1.1** — sekcija 1.0 „Gde čovek stoji u rečenici": enklitike, drugo lice, „onaj/ono", nadovezivanje umesto ugrađivanja;
- **v1.2** — korpus postaje četvrti uslov kapije. **Profil daje potez, rečnik daje reči**;
- **v1.3** — `recnik-obrazaca.md`: potvrđene sprege po tome šta hoćeš da kažeš, sa izvorom i sa listom onoga što se ne govori;
- **v1.4** — `provera_kolokacije.py`: postoji li ova sprega u živom srpskom (srWaC, 555 miliona reči);
- **v1.5** — mesto enklitike u grozdu; alat razlikuje „nema pogodaka" od „nisam mogao da proverim";
- **v1.6** — lokalni indeks za offline rad, uz merenje koje pokazuje zašto se gotova tabela ne isporučuje;
- **v1.7** — prelazak na **CLASSLA-web.sr** (2,34 milijarde reči, CC0) sa oznakom žanra po tekstu; prekidač `--promocija` sužava pretragu na tekstove koji nešto nude, čime korpus postaje i izvor fraza, ne samo proveravač.

Validacija profila (metod, merila fiksirana pre pisanja, svi testirani tekstovi i nalazi) stoji u `skills/srpski-copy/references/validacija-profila.md`.

### Šta ostaje otvoreno

- **Nezavisna provera validacije.** Isti prolaz je pisao i ocenjivao testove. Merila su fiksirana unapred i skener je nezavisna mera, ali nalazi nisu konačni dok ih ne pregleda neko ko nije pisao tekstove.
- **Jedan test-brief.** Svih trinaest profila mereno je na istoj temi. To je pošteno za poređenje, ali kažnjava profile kojima kategorija ne odgovara.
- **Rečnik obrazaca je tanak van pića i grickalica** — 83 citata iz 19 brendova. Raste upotrebom, i može se hraniti iz srWaC-a.
- **Stilometrija zaštićenih autora je trajno blokirana** — traži izdanja koja po pravilima projekta ne smeju u skill.

## Licenca

MIT — v. [LICENSE](LICENSE), uz ogradu iz odeljka „Građa i prava".
