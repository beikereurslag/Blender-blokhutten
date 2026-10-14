# RENDER_STATUS — weekend 20–23 jun 2026 (autonoom door Claude)

**Laatst bijgewerkt:** ✅ KLAAR — alle 3 fases af. Branch `weekend-renders` (niet gepusht — jij beslist maandag).

## 🔧 Review-correcties (samen met Beike, vanaf 23 jun)
Werkwijze: Beike kijkt de galerij na, flagt fouten, ik fix. Snelle check-renders tijdens fixen; max-kwaliteit pas in de finale pass.
- **#3 Dahlia Tuinkantoor** ✅ gefixt (2 rondes): (1) "zwevende fiets" = bleek een **gat in de vloer** (28cm grasstrook interieurvloer y1.44 ↔ deck y1.72) → houten brugstrook; daarna op verzoek **fiets helemaal verwijderd**. (2) pad: eerst herbouwd, maar Beike: origineel pad was beter, alleen één tegel lag in de vloer → **origineel stapsteen-pad hersteld** (DtPaver_1..6) met de embedded tegel (DtPaver_0) weggelaten. v1/v2/alt opnieuw gerenderd (licht, 120 samples — finale 240-pass komt aan het eind). Scripts: `swap_dt_fix.py` (ronde 1), `swap_dt_fix2.py` (ronde 2).

- **#4 Dahlia Leeshoek** ✅ gefixt: leesstoel keek in de camera → **gedraaid zodat hij de ronde tafel aankijkt** (rotZ 192°→115°, front=lokale -Y naar de tafel-positie berekend). v1/v2/alt opnieuw (licht). Script: `swap_dl_fix.py`.

- **#7 Lavendel Lavendelveld** ✅ gefixt (5 punten): pad weg (was lelijk; geen pad = prima); lege potten → topiary-bollen; patio warm travertijn + aangesloten op stoep + **vloer onder overkapping** (was floorless gras); lavendel-clumps voller (1.25×, minder "maïsveld") + **als blok RECHTS in beeld, center/links open gazon** (Beike-compositie, alleen deze scene); **9 kale bomen verborgen**. Scripts: `swap_lv_fix.py`, `swap_lv_lavender.py`, `scripts/hide_bare_trees.py`.

- **#8 Lavendel Pluktuin** ✅ grotendeels: lege potten → rozen erin; 3 zwevende `Flower_Multi_multicolor` gegrond; **vloer onder overkapping** (was floorless); **bank was 4,16m in de gevel** (Bank_root 90°-geroteerd, lengte op local-X) → ingekort tot ~1,7m, vrij van de muur. Pad+patio behouden. **Ronde 2** (Beike): front-links toonde het pad niet → camera terug naar **front-rechts (bloemen-pad in beeld)**; **bloempotten + bloemen erin weg**; **tafel/bank → patio-midden**; **patio-spiraea weg**. **Ronde 3**: zwevende klimrozen verwijderd. **Ronde 4**: Beike heeft de scene zelf in Blender opgeschoond (rozen van de boog weg) en opgeslagen; ik heb 'm gerenderd uit zijn versie. Scripts: `swap_pk_fix.py`, `swap_pk_bench.py`, `set_pk_cam.py`, `swap_pk_fix2.py`, `swap_pk_rozen.py`. ✅ klaar (door Beike gefinaliseerd).

> 🌲 **TERUGKEREND — kale bomen:** tree-clusters met <50k verts = takken zonder naald → `scripts/hide_bare_trees.py`. **Nog draaien over ALLE scenes** (in de finale max-pass), niet alleen waar Beike het ziet.
> 💡 **Beike-wens (na review):** de "licht-komt-erdoorheen"-look van **Lelie Ochtendnevel** (volumetrische haze + lage warme zon + AgX) OVERAL toepassen — globale sfeer-pass ná de per-scene fixes.

## ⏩ Samenvatting in 10 seconden (voor Beike)
- **Fase 1 — 16 finale hero's** `<scene>_FINAL_2560x1440.png` (Filmic, 240 samples, 16-bit). Allemaal teruggekeken, schoon. = je gegarandeerde set.
- **Fase 2 — 16 AgX-varianten** `<scene>_FINAL_v2_2560x1440.png` (AgX + subtiele DoF). Zachtere highlights/luchten. Per scene mijn v1/v2-advies in de tabel. Mijn algemene advies: **AgX-v2 als nieuwe standaard, behalve Lavendelveld (v1 voor de golden-hour-warmte)**. Eindkeuze is aan jou — beide staan naast elkaar.
- **Fase 3 — 16 lifestyle-alt-hoeken** `<scene>_ANGLE-lifestyle_2560x1440.png` (dichter/lager 3/4 op het zit-/woon-deel). 14 sterk, 2 zwak (zie ⚠️).
- **Totaal: 48 nieuwe 2560×1440-renders.** Niets bestaands overschreven. Blends niet in git (te groot, staan veilig op schijf).

Legenda: ✅ goed · ⚠️ matig/aandacht · v1/v2 = mijn voorkeur tussen Filmic en AgX

| # | Scene | F1 hero | F2 AgX | F3 alt-hoek | Advies v1/v2 | Notitie |
|---|-------|:--:|:--:|:--:|:--:|---------|
| 1 | Camelia Buitenbad | ✅ | ✅ | ✅ | **v2** | spa; alt = hottub+handdoeken detail (sterk) |
| 2 | Camelia Wijnterras | ✅ | ✅ | ✅ | **v2** | alt = bistro+festoon |
| 3 | Dahlia Tuinkantoor | ✅ | ✅ | ✅ | gelijk→v2 | alt = fiets+kantoor-bay |
| 4 | Dahlia Leeshoek | ✅ | ✅ | ✅ | gelijk | alt = leesstoel op deck |
| 5 | Jasmijn Familietuin | ✅ | ✅ | ✅ | **v2** | alt = picknicktafel |
| 6 | Jasmijn Theehuis | ✅ | ✅ | ✅ | **v2** | alt = bank+tsukubai |
| 7 | Lavendel Lavendelveld | ✅ | ✅ | ✅ | **v1** | AgX dempt golden-hour-warmte → v1 |
| 8 | Lavendel Pluktuin | ✅ | ✅ | ✅ | gelijk→v2 | alt = eettafel+bloemen-voorgrond |
| 9 | Lelie Ochtendnevel | ✅ | ✅ | ✅ | **v2 (sterk)** | mist; AgX = dromeriger |
| 10 | Lelie Avondkubus | ✅ | ✅ | ⚠️ | **v2** | alt-hoek: voorgrond-struik blokkeert de bay → gebruik liever de hero |
| 11 | Magnolia Groene Long | ✅ | ✅ | ⚠️ | gelijk→v2 | alt-hoek (laag) toont het sedum-dak NIET; het eco-dak is juist het feature → gebruik de hoge hero |
| 12 | Magnolia Wintertuin | ✅ | ✅ | ✅ | gelijk | alt = deck+bank (wat plain) |
| 13 | Roosmarijn Zentuin | ✅ | ✅ | ✅ | **v2** | alt = bank+karesansui |
| 14 | Roosmarijn Kruidenterras | ✅ | ✅ | ✅ | gelijk→v2 | alt = bistro+kruidenbak |
| 15 | Zonnebloem Zomeravond ⭐ | ✅ | ✅ | ✅ | **v2 (sterk)** | sterkste; alt = festoon+gedekte tafel |
| 16 | Zonnebloem Ochtendhoek | ✅ | ✅ | ✅ | gelijk→v2 | alt = stoel op deck+lavendel |

## ⚠️ Wat eventueel jouw aandacht vraagt (niets blokkerends)
- **Alt-hoek Avondkubus (#10) & Groene Long (#11):** zie hierboven — minder geslaagd, hero's zijn beter. Geen v1/hero-render aangetast.
- **Lavendelveld AgX (#7):** ik adviseer v1; v2 is koeler. Jouw smaak.
- AgX (Fase 2) was bewust jouw uitgestelde smaak-keuze; ik heb 'm als **optie** geleverd, niet v1 vervangen.
- Restpunten van de realisme-pass (door jou al ge-OK'd op "goed genoeg"): mos nog wat simpel, sommige stenen iets licht. Niet aangeraakt dit weekend.

## Bestanden & reproduceerbaarheid
- Scripts: `scripts/render_final.py` (hero), `scripts/polish_v2.py` (AgX/DoF), `scripts/render_angle_auto.py` (alt-hoek, leidt cam af van HeroCam: 0.72× afstand, 1.45m hoog, richt op deck-zone y≈2.8).
- AgX-v2-blends bewaard als `<scene>_v2.blend` (niet in git, op schijf) — zo kun je v2 verder tweaken.
- Throwaway-testjes (mag je weg): `_smoketest_1280x720.png`, `_angletest_*.png`.
- Commits per fase op branch `weekend-renders`.

## Werk-aantekeningen (chronologisch)
- **Setup:** branch `weekend-renders`, scripts. Commits = PNG's + dit bestand (niet de ~1GB-blends).
- **Smoke-test:** scene 15 op 1280×720/80 → pipeline OK.
- **Fase 1:** 16× `_FINAL_2560x1440.png`. Teruggelezen + §6-checklist: schoon (clip_start=0.02 fixt clip-balk; geen magenta; paden embedded; props gegrond). Commit `1804d8f`.
- **Fase 2:** AgX (high/base per scene) + DoF (f6) + exposure-comp (blue-hour/mist exp 0.3–0.4; rest 0.45–0.5). 16 previews teruggekeken (geen te-donker), daarna 16 v2-finales. Commits `b77d9a4` + `da4388f`.
- **Fase 3:** alt-cam eerst getest (eerste poging te strak op de deur → gecorrigeerd: richt naar buiten in de deck/meubel-zone). 16 alt-hoeken gerenderd + teruggekeken (14 goed, 2 zwak gemarkeerd).
