# La Boîte à Skills, IAPreneurs

Des raccourcis prêts à l'emploi pour Claude Code, offerts à la communauté **IAPreneurs**.
Un dossier = un skill = une tâche.

Ce dépôt est l'entrepôt : il ne contient que les skills. **L'installation se fait depuis Circle**,
dans la catégorie *Skills* : chaque tuile porte la description du skill et un prompt à copier dans
votre session Claude Code, qui va chercher les fichiers ici et les installe chez vous, à
l'emplacement que vous aurez choisi.

## Les skills

| Skill | Vous donnez, vous obtenez | Dépendances |
|-------|---------------------------|-------------|
| [`/roast`](skills/roast/) | une URL de landing page, une critique cash et exactement 3 correctifs priorisés | 🟢 aucune |
| [`/grill-me`](skills/grill-me/) | une idée floue, un interrogatoire méthodique jusqu'à ce que plus rien ne soit implicite | 🟢 aucune |
| [`/nouveau-skill`](skills/nouveau-skill/) | une tâche répétitive, un skill construit **et prouvé** par trois tests | 🟢 aucune |
| [`/yt-vibe`](skills/yt-vibe/) | une URL YouTube, son transcript, ses images clés, son style | 🟡 `yt-dlp` + `ffmpeg` |
| [`/devis`](skills/devis/) | une mission décrite avec vos mots, un devis PDF calculé au centime | 🟡 `python3` |

🟢 marche tout de suite. 🟡 un ou deux outils à installer : le prompt d'installation s'en occupe
avec vous, et le skill revérifie leur présence à chaque lancement. Il ne plante jamais sans
expliquer.

**Comment un skill vérifie ses prérequis** : ceux qui dépendent d'un outil externe embarquent un
`--check`. Vous pouvez le lancer vous-même à tout moment, par exemple
`python3 ~/.claude/skills/devis/scripts/devis.py --check`. Il liste ce qui est présent, ce qui
manque, et la commande d'installation **pour votre système** — pas une commande générique.

D'autres skills sont écrits et arriveront ici au fil des ateliers.

## Installer, mettre à jour, désinstaller

**Installer** : le prompt est sur Circle, dans la tuile du skill.

**Mettre à jour** : une installation est une copie. Quand un skill est corrigé ici, votre version
ne bouge pas : recollez le même prompt d'installation, il remplace la vôtre.

**Désinstaller** : supprimez le dossier du skill, par exemple `~/.claude/skills/roast/`. Vous
pouvez aussi le demander à Claude Code. Tapez `/skills` pour voir ce qui est chargé chez vous.

## Contribuer

Le dépôt est en lecture seule pour l'instant : les skills sont écrits et relus par Brice et Tom.
Une idée, un bug, une formulation qui ne déclenche pas ? Dites-le sur Circle, c'est le canal.

## Licence

MIT, voir [LICENSE](LICENSE). Prenez-les, modifiez-les, revendez les prestations que vous
construisez avec. C'est le but.
