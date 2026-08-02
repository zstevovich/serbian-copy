# Primeri — bilo → ispravljeno (nastavak)

Prva dva primera stoje u `SKILL.md`. Ovde su ostali. Svaki par dolazi iz stvarne ispravke; nijedan nije izmišljen.

**3. Kalk formata prodavnice**
- ❌ „Lanci, delikatesi, koncept prodavnice."
- ✅ „Trgovinski lanci, prodavnice zdrave hrane, specijalizovane radnje."
- *Zašto:* „delikatesi" je kod nas pult sa suhomesnatim; „koncept prodavnice" se čita kao genitiv.

**4. Netačna tvrdnja pred trgovcem**
- ❌ „Najjači konkurent nije na vašoj polici." *(a kafa jeste na njihovoj polici)*
- ✅ „Najveći konkurent energetskih pića stoji na drugoj polici."
- *Zašto:* kupac obori tvrdnju u sebi pre nego što pročita sledeći red.

**5. Marketinško preterivanje pred B2B publikom**
- ❌ „Lanci su probali, pa poručili ponovo."
- ✅ „Rezultati u evropskim lancima."
- *Zašto:* brojke ispod već ubeđuju; naslov ne drži govor.

**6. Apsolutna tvrdnja koja nije tačna**
- ❌ „Brite ne preuzima promet sa energetske police."
- ✅ „Da, Brite će konkurisati i drugim energetskim pićima. Ali novi promet stiže **i od** kupca koji danas bira kafu."
- *Zašto:* koncesija pa tačna tvrdnja. Ono „i od" spušta garanciju na mogućnost — i to je razlika između istine i prodaje magle.

**7. Birokratska prazna fraza**
- ❌ „Regionalna logistika je proverena u praksi."
- ✅ *(izbačeno — ili konkretno, ili ništa)*

**8. Kafanski žargon**
- ❌ „Snabdevanje već radi kao podmazano."
- ✅ „Dostava u roku od 48 h za Beograd i Novi Sad."

**9. Korporativna fraza**
- ❌ „Misija se od tada nije promenila:"
- ✅ „Ideja je i danas ista:"

**10. Prevod glagola**
- ❌ „Prisutan na najzahtevnijim tržištima." (*present in the market*)
- ✅ „Već na policama najzahtevnijih tržišta."
- *Zašto:* piće se prodaje ili stoji na polici; ono ne biva prisutno.

**11. Dvosmislen pridev**
- ❌ „Četiri SKU-a sa jedinstvenim dizajnom limenke." (*unique* → čita se i kao „ujednačen")
- ✅ „Četiri SKU-a, ista limenka u četiri boje."

**12. Personifikovan objekat**
- ❌ „Šta dobija vaša polica" · „Polica koja privlači pogled"
- ✅ „Šta dobijate vi" · „Limenka se na polici primeti iz prve"

---

## Studija slučaja: jedan veznik nosi sve veze

Pravilo je u `SKILL.md`, sekcija 1.2 — ako se isti veznik u istoj funkciji pojavi više od dva-tri puta u dokumentu, deo mesta se prepisuje drugim sredstvom. Ovde je izvedba.

Mereno na jednom FMCG sajtu: **„pa" je nosilo posledicu na devet mesta** — upravo zato što je prvo u tabeli veznika. Alat protiv jednog obrasca proizveo je drugi. Stvarne zamene:

| Bilo | Ispravljeno |
|---|---|
| „…koja uz njega obično ide, **pa** pažnja ostaje ravnomerna satima." | „…koja uz njega obično ide, **tako da** pažnja ostaje ravnomerna satima." |
| „Kofein iz četiri biljna izvora, **pa** energija raste postepeno…" | „Kofein iz četiri biljna izvora**:** energija raste postepeno…" |
| „…otpušta polako, **pa** budnost traje duže." | „…otpušta polako, **zbog čega** budnost traje duže." |
| „…oko šest sati, **pa** dan delimo na dva trenutka…" | „…oko šest sati, **zato** dan delimo na dva trenutka…" |
| „Uz ovo ga preskočiš, **pa** fokus ostane do kraja radnog dana." | „Uz ovo ga preskočiš **i** fokus ostane do kraja radnog dana." |
| „Poslednju popiješ do četiri, **pa** do spavanja…" | „**Ako** poslednju popiješ do četiri, do spavanja…" |

Šest zamena, šest različitih sredstava — nijedno se ne ponavlja. To je i poenta: zamena koja svih devet mesta prepiše istim novim veznikom samo pomera tik.

---

## Studija slučaja: crta nacrtana CSS-om

Pravilo je u `SKILL.md`, Z1. Na jednom sajtu je u hero-liniji stajalo „Bistra glava · mirna energija ——— Pineapple Mango", a to nije bio znak nego `<span class="divider">` sa `width:24px;height:1px;background:currentColor`.

U tekstu nije bilo nijedne crte, a čitalo se identično. Zamenjeno je tačkom koja već stoji u istoj liniji.

**Posledica za proveru:** mehanička pretraga ide i kroz CSS (`height:1px` na inline elementu između reči), ne samo kroz tekst. Grep nad izvorom teksta bi ovde vratio nulu i propustio nalaz.

---
