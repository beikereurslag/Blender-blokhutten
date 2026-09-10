# Branch `code` — alleen code en documentatie

Deze branch bestaat om één reden: de gewone werkbranch (`weekend-renders`) sleept **219 GB aan Git
LFS-objecten** mee (scenes, assets, renders) en is daardoor niet naar GitHub te pushen. De code en
de handoffs zijn klein en juist moeilijk te reconstrueren, dus die staan hier los en wél off-site.

Inhoud: `scripts/`, `docs/` en de handoff- en planbestanden uit de projectroot. Geen blends, geen
assets, geen renders, geen PNG's — dus geen LFS.

Het is een **orphan branch**: hij heeft geen geschiedenis gemeen met `weekend-renders` en is geen
afsplitsing daarvan. Niet mergen. Bijwerken gebeurt door de branch opnieuw op te bouwen uit de
werkbranch (aparte index, HEAD en werkboom blijven onaangeroerd).

De print-pijplijn (`C:\Users\beike\blokhut-print`) staat in zijn eigen repo:
https://github.com/beikereurslag/blokhut-print
