#!/usr/bin/env bash
# Bouwt de orphan branch `code` opnieuw op en pusht hem.
#
# Waarom die branch bestaat: `weekend-renders` sleept ~219 GB aan Git LFS-objecten mee (scenes,
# assets, renders) en is daardoor niet naar GitHub te pushen. De code en de handoffs zijn samen
# ~6 MB en juist moeilijk te reconstrueren, dus die gaan als losse orphan branch wél off-site.
#
# Werkt met een APARTE index (.git/code.index): HEAD, de branch waarop je staat en de werkboom
# blijven onaangeroerd. Dat is bewust - er draaien vaak renders uit deze werkboom.
#
#     bash scripts/push_code_branch.sh [--dry-run]
set -eu
cd "$(dirname "$0")/.."
DRY=${1:-}

LIJST=$(mktemp)
trap 'rm -f "$LIJST"' EXIT
# scripts/, docs/ en de losse .md-bestanden in de projectroot; geen beeld, geen bytecode
git ls-tree -r --name-only -z HEAD | tr '\0' '\n' \
  | grep -E '^(scripts/|docs/)|^[^/]+\.md$' \
  | grep -vE '\.(png|jpg|jpeg|pyc|blend|blend1|glb|hdr|exr)$' \
  | grep -v '^scripts/CODE_BRANCH\.md$' > "$LIJST"   # komt hieronder als CODE_BRANCH.md in de root
echo "code-branch: $(wc -l < "$LIJST") bestanden uit $(git rev-parse --short HEAD)"

if [ "$DRY" = "--dry-run" ]; then
  echo "(dry-run: niets gebouwd of gepusht)"; exit 0
fi

export GIT_INDEX_FILE="$(pwd)/.git/code.index"
rm -f "$GIT_INDEX_FILE"
git read-tree --empty
tr '\n' '\0' < "$LIJST" | git update-index --add -z --stdin

# CODE_BRANCH.md hoort bij de branch zelf, niet bij de werkboom
if [ -f scripts/CODE_BRANCH.md ]; then
  sha=$(git hash-object -w scripts/CODE_BRANCH.md)
  git update-index --add --cacheinfo 100644,"$sha",CODE_BRANCH.md
fi

tree=$(git write-tree)
commit=$(git commit-tree "$tree" -m "Code en documentatie zonder de LFS-objecten

Opnieuw opgebouwd uit $(git rev-parse --short HEAD) op $(date +%Y-%m-%d).
Orphan branch: geen gemeenschappelijke geschiedenis met de werkbranch, niet mergen.
Zie CODE_BRANCH.md en scripts/push_code_branch.sh.")
git branch -f code "$commit"
unset GIT_INDEX_FILE
rm -f "$(pwd)/.git/code.index"

git push -f origin code
echo "gepusht: code -> $commit"
