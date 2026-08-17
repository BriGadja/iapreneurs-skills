# La Boîte à Skills — IAPreneurs

Des raccourcis prêts à l'emploi pour Claude Code. Un dossier = un skill = une tâche. Vous en
installez un en collant un prompt, et vous l'avez pour toujours dans tous vos projets.

**Aucun téléchargement, aucun zip, aucun terminal à préparer.** L'installation passe par un
prompt que Claude exécute lui-même : elle marche donc identiquement sur macOS, Linux, Windows
et WSL.

## Installer un skill

Ouvrez Claude Code et collez le prompt de **[INSTALLER.md](INSTALLER.md)**, en remplaçant le nom
du skill. C'est tout.

Le même fichier contient le **prompt de mise à jour** — pensez-y : une installation est une
copie, elle ne se met pas à jour toute seule quand on corrige un skill ici.

## Les skills

| Skill | Vous donnez → vous obtenez | Dépendances |
|-------|----------------------------|-------------|
| [`/roast`](skills/roast/) | une URL de landing page → une critique cash + exactement 3 correctifs priorisés | 🟢 aucune |
| [`/yt-vibe`](skills/yt-vibe/) | une URL YouTube → transcript, images clés, analyse du style | 🟡 `yt-dlp` + `ffmpeg` |
| [`/grill-me`](skills/grill-me/) | une idée floue → un interrogatoire méthodique jusqu'à ce que plus rien ne soit implicite | 🟢 aucune |
| [`/nouveau-skill`](skills/nouveau-skill/) | une tâche répétitive → un skill construit **et prouvé** par trois tests | 🟢 aucune |

🟢 zéro dépendance, ça marche tout de suite · 🟡 un ou deux outils à installer, le skill vous dit
lesquels et ne plante jamais sans le dire.

Chaque dossier a son propre `README.md` : à quoi ça sert, comment l'utiliser, des exemples de
prompts à copier-coller, et quoi faire quand ça coince.

## Comment c'est fait

`skills.json` est l'index : pour chaque skill, sa version, ses prérequis et **la liste de ses
fichiers**. Les prompts d'installation lisent ce fichier en premier, ils n'ont donc jamais de
liste en dur. Ajouter un fichier à un skill, c'est l'ajouter à l'index — les installations
suivantes le prennent, sans qu'aucun post publié ne soit à retoucher.

## Contribuer

Le dépôt est en lecture seule pour l'instant : les skills sont écrits et relus par Brice et Tom.
Une idée, un bug, une formulation qui ne déclenche pas ? Dites-le sur Circle, c'est le canal.

## Licence

MIT — voir [LICENSE](LICENSE). Prenez-les, modifiez-les, revendez les prestations que vous
construisez avec. C'est le but.
