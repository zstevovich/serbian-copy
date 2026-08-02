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
├── references/           # radni tokovi, korpus, zabrane, profili, rubrika (27 fajlova)
└── scripts/
    ├── scan_copy.py
    └── tests/test_scan_copy.py
```

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

**v0.9.2.** Doktrina i skener su u upotrebi na stvarnim projektima.

Urađeno posle prve objave:

- **v0.9.1** — skener proširen na Z5, Z9 i Z10, sa pragovima izmerenim na korpusu i negativnim parnjakom uz svaku granu;
- **v0.9.2** — `SKILL.md` rasterećen sa 36,5 na 31,4 KB (−14%): studije slučaja su otišle u `primeri.md`, a razrada dvanaest zabrana u `references/zabrane.md`, uz indeks koji svako pravilo drži u jednoj liniji. Nijedan sadržaj nije izgubljen.

Do v1.0 ostaje **validacija trinaest stilističkih profila** na četiri formata (hero, brand-story, B2B uvod, naslov). Profili su za sada „radna verzija 1.0" — izvedeni iz stilističkih studija, ali još neizmereni na korpusu.

## Licenca

MIT — v. [LICENSE](LICENSE), uz ogradu iz odeljka „Građa i prava".
