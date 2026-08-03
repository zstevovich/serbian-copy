# Mapa izvora za stilistički korpus

## Namena

Ovaj fajl vodi istraživanje izvora. Ne predstavlja dozvolu da se sadržaj automatski preuzima ili ugrađuje u Skill. Pre svakog preuzimanja proveri autorska prava, uslove korišćenja i status konkretnog dela.

## Korpusi za proveru prirodne upotrebe jezika

### srWaC — ReLDI

Veliki srpski web-korpus sa oko 555 miliona tokena, morfosintaksičkim oznakama i lemama. Koristi ga za:

- proveru da li konstrukcija prirodno postoji u savremenom jeziku;
- kolokacije;
- dominantne padežne i glagolske obrasce;
- poređenje književne konstrukcije sa savremenom upotrebom.

Ne koristi ga kao čist književni korpus: web sadržaj meša registre i kvalitet.

**Ne koristi ga ni kao izvor marketinškog jezika.** Izmereno: u korpusu dominiraju vesti, politika, tehnika i književnost, a trgovačkog sadržaja praktično nema. Automatsko vađenje kolokacija po pojmu vraća „električnu energiju" i „radnu snagu", ne jezik police. Pun nalaz u [recnik-obrazaca.md](recnik-obrazaca.md). Korpus je **proveravač, ne izvor**.

**Uvezan je u rad.** `scripts/provera_kolokacije.py` pita srWaC preko NoSketch Engine API-ja na CLARIN.SI i vraća broj pojavljivanja sa primerima. Koristi se kad [recnik-obrazaca.md](recnik-obrazaca.md) ne pokriva traženu spregu reči. Dve izmerene zamke stoje u komentarima skripta: „sebi" se lematizuje kao „sebe" (pa naivan upit po lemama daje lažne negative), a prvi odgovor na hladan upit ume da bude nedovršen i vrati delimičan broj.

### CLASSLA-web i drugi javni korpusi

Koristi žanrovske oznake kada su dostupne da odvojiš publicistiku, promociju, diskusiju i druge registre. Korpus je koristan za poređenje, ne za izvođenje individualnog autorskog profila.

### Korpusi srpskog jezika Matematičkog fakulteta

Istraži dostupne kolekcije beletristike i druge registre. Pre automatizovanog preuzimanja proveri pristup, licencu i mogućnost izvoza rezultata.

## Digitalne biblioteke

### Projekat Rastko

Neprofitna elektronska biblioteka srpske kulture, naročito korisna za dela u javnom vlasništvu, istorijske tekstove, kritiku i bibliografski kontekst.

Koristi za:

- javnodomenske autore i dela;
- književnu kritiku i eseje o autorima;
- istorijski i jezički kontekst;
- proveru pouzdanog izdanja kada je jasno navedeno.

Ne pretpostavljaj da je svako delo na sajtu automatski slobodno za ponovno pakovanje.

### Digitalne kolekcije Narodne biblioteke Srbije i univerzitetskih biblioteka

Koristi kataloge i digitalizovane zbirke za pronalaženje izdanja, kritike i bibliografije. Zaštićeno delo može biti dostupno za čitanje, ali ne i za ugrađivanje u Skill.

## Akademski izvori

Traži radove iz:

- stilistike;
- sintakse srpskog jezika;
- naratologije;
- korpusne lingvistike;
- stilometrije;
- književne kritike pojedinačnih autora.

Prednost imaju doktorske disertacije, radovi u naučnim časopisima, univerzitetska izdanja i radovi sa jasno opisanom metodologijom.

## Plan pribavljanja građe po autorima

Za svakog autora prikupi tri vrste izvora:

1. **Primarni uzorak:** legalno dostupan tekst ili tekst koji korisnik poseduje i dostavi za analizu.
2. **Sekundarna literatura:** najmanje dva stručna rada o stilu, sintaksi ili poetici autora.
3. **Kontrolni korpus:** savremeni srpski korpus kojim se proverava da li je postupak i dalje prirodan ili je istorijski obeležen.

## Evidencija izvora

Za svaki izvor zapiši:

```text
Autor / institucija:
Naslov:
Vrsta izvora:
Godina:
URL ili bibliografski podatak:
Status prava / licenca:
Dostupni obim:
Za šta se koristi:
Šta se ne sme preuzeti:
Datum provere:
```

## Faze rada

### Faza 1 — javni domen i metodologija

Počni autorima i delima za koje je status prava čist, kao i stručnom literaturom. Cilj je proveriti analitički okvir i format nalaza.

### Faza 2 — zaštićeni autori bez pakovanja tekstova

Za Andrića, Selimovića, Crnjanskog, Pekića, Ćopića, Radovića, Kapora i Kiša koristi legalno pribavljene primerke ili korisnikove datoteke za internu analizu. U Skill ulaze samo izvedeni stilistički obrasci, statistika i originalni primeri.

### Faza 3 — validacija na copy zadacima

Svaki profil testiraj na najmanje:

- jednom hero bloku;
- jednoj brand-story sekciji;
- jednom B2B uvodu;
- jednom kratkom naslovu.

Tek postupci koji poboljšavaju prirodnost bez gubitka jasnoće ulaze u stabilni deo Skill-a.

## Izvori za završene autorske profile

- **Ivo Andrić:** radovi o umetničkom postupku pripovedaka, perspektivi naratora, gnomskom i anegdotskom stilu i jakim pozicijama teksta.
- **Meša Selimović:** lingvostilističke analize elipse, parcelacije, jedinica bez predikata i narativnog diskursa u „Tvrđavi“ i „Dervišu i smrti“.
- **Miloš Crnjanski:** disertacija o sintaksičko-stilističkim strukturama, radovi o sumatraizmu, ponavljanju, imenovanju i poetskoj sintaksi proze.
- **Borislav Pekić:** studije o analitičkoj ironiji, metafikcionalnom pripovedanju, polisemiji, mitu i postupku pronađenog rukopisa.
- **Branko Ćopić:** lingvostilistička analiza „Magarećih godina“ i studije o humoru, ekspresivnoj leksici, aoristu, poređenju i hiperboli.
- **Branislav Nušić:** radovi o stilogenoj funkciji imena, nadimaka i leksičkih odnosa u komičnom efektu.
- **Radoje Domanović:** studije o alegorijsko-satiričnom postupku, paraboličnosti, karnevalizaciji i epizodičnosti.
- **Momo Kapor:** studija idiostila kolumni u „Vodiču kroz srpski mentalitet“, sa fokusom na govorne žanrove, kolokvijalnost i odnos lokalnog i globalnog.

Zaštićene književne tekstove ne pakovati u Skill. Koristiti ih samo iz legalno pribavljenih izdanja za internu proveru i stilometriju.
