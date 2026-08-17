# `/yt-vibe` — l'ADN visuel et sonore d'une vidéo YouTube, en une commande

> La Boîte à Skills — IAPreneurs. Un dossier = un skill = une tâche.

**Vous donnez** : l'adresse d'une vidéo YouTube.
**Vous obtenez** : le transcript, une douzaine d'images clés (les moments où l'image change), et
une analyse de **l'ambiance, du style et du ton** — le visuel comme l'éditorial.

L'effet : Claude « regarde » vraiment la vidéo (il ouvre les images) et « l'écoute » (il lit le
transcript). Exactement ce qu'il faut pour s'inspirer d'un format, décortiquer un concurrent, ou
réutiliser un style. **Aucune clé API, aucun abonnement à un service tiers.**

---

## Installation

Ouvrez Claude Code (n'importe où) et collez ceci :

```
Installe le skill « yt-vibe » de la Boîte à Skills IAPreneurs. Procède ainsi :

1. Lis https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json
   et trouve l'entrée « yt-vibe ». Elle te donne la liste exacte des fichiers.

2. Pour CHAQUE fichier listé, lis-le à l'adresse
   https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<le chemin du fichier>
   puis écris-le dans mon dossier personnel Claude, en retirant le préfixe « skills/ » :
   « skills/yt-vibe/SKILL.md » devient « ~/.claude/skills/yt-vibe/SKILL.md » chez moi.
   Sous Windows, c'est C:\Users\<mon nom>\.claude\skills\yt-vibe\.
   Crée les sous-dossiers manquants. Écris les fichiers À L'IDENTIQUE.

3. Si l'entrée a des « prerequis », vérifie s'ils sont présents et dis-moi quoi installer
   s'il en manque, avec la commande pour MON système. N'installe rien sans me demander.

4. INTERDIT : si tu n'arrives pas à lire une de ces adresses, ARRÊTE-TOI et dis-le-moi.
   N'écris jamais un skill de mémoire ni « une version équivalente ».

5. Termine par la liste des fichiers écrits et la phrase à taper pour lancer le skill.
```

Puis **relancez Claude Code** : les skills sont lus au démarrage.

Aucun téléchargement, aucun terminal, aucune commande shell — donc identique sur macOS, Linux,
Windows et WSL. Pour mettre à jour plus tard, voir
[INSTALLER.md](../../INSTALLER.md#le-prompt-de-mise-à-jour).

## Prérequis

Ce skill a besoin de **deux outils gratuits**, et de rien d'autre :

| Outil | À quoi il sert |
|-------|----------------|
| `yt-dlp` | récupère la vidéo, les sous-titres et les informations depuis YouTube |
| `ffmpeg` | découpe la vidéo pour en extraire les images clés |

*(`python3` orchestre le tout, il est déjà présent sur quasiment toutes les machines.)*

`/setup` s'en occupe, y compris l'installation. Si vous préférez le faire à la main :

**Windows** — dans PowerShell ou le CMD :
```powershell
winget install --id yt-dlp.yt-dlp -e --accept-package-agreements --accept-source-agreements
winget install --id Gyan.FFmpeg  -e --accept-package-agreements --accept-source-agreements
```
🔴 **Puis fermez Claude Code et relancez-le.** `winget` ajoute les outils au `PATH` de Windows,
mais un programme déjà ouvert garde l'ancien : sans redémarrage, Claude Code continuera de dire
qu'ils sont absents alors qu'ils sont bel et bien installés. C'est le piège n°1 sous Windows.

Si `winget` est introuvable (Windows ancien), installez « App Installer » depuis le Microsoft
Store : https://apps.microsoft.com/detail/9nblggh4nns1

**macOS** :
```bash
brew install yt-dlp ffmpeg
```

**Linux / WSL** :
```bash
sudo apt install yt-dlp ffmpeg
```

⚠️ **Ça tourne sur VOTRE machine, pas sur un serveur.** Depuis votre box, votre wifi ou votre
4G, ça marche nativement. Depuis un serveur distant, YouTube peut bloquer avec un « confirmez que
vous n'êtes pas un robot » : ce skill n'est pas fait pour ça. Le détail et le contournement sont
dans `.claude/skills/yt-vibe/references/depannage.md`.

---

## Exemples de prompts

À copier-coller tels quels, en remplaçant l'adresse par la vôtre.

**Le cas de base**
```
/yt-vibe https://www.youtube.com/watch?v=XXXXXXXXXXX
```

**Sans même taper la commande** (le skill se déclenche tout seul) :
```
Analyse le style de cette vidéo : https://youtu.be/XXXXXXXXXXX
```

**Décortiquer un concurrent** :
```
/yt-vibe https://www.youtube.com/watch?v=XXXXXXXXXXX
C'est une chaîne concurrente de la mienne. Dis-moi ce qui fait tenir le spectateur :
l'accroche des 15 premières secondes, le rythme du montage, la structure du propos.
```

**S'inspirer d'un format pour sa propre vidéo** :
```
/yt-vibe https://youtu.be/XXXXXXXXXXX
J'aime ce format. Reprends sa structure et écris-moi le script de ma vidéo à moi,
sur le sujet : <votre sujet>.
```

**Plus ou moins d'images** (12 par défaut) :
```
/yt-vibe https://youtu.be/XXXXXXXXXXX
Prends-moi 25 images clés, je veux voir le montage en détail.
```

**Enchaîner après l'analyse** :
```
Refais-moi un moodboard à partir des images que tu as extraites.
```
```
Écris-moi 5 titres de vidéo dans le ton exact de cette chaîne.
```

**Si le téléchargement coince** (YouTube change souvent, l'outil doit suivre) :
```
Mets yt-dlp à jour et relance.
```

---

## Ce qu'il faut savoir avant de croire le résultat

Le skill **vérifie ses outils avant de démarrer** et affiche la commande d'installation exacte
s'il en manque un, au lieu de planter avec une erreur incompréhensible. C'est la différence entre
un gadget qui impressionne et un gadget qu'on désinstalle.

Il se protège aussi tout seul : au-delà d'une trentaine de minutes de vidéo, il s'arrête et vous
demande confirmation avant de télécharger plusieurs gigaoctets. Et il **supprime la vidéo** une
fois les images extraites — vous ne gardez que ce qui sert.

Si la vidéo n'a pas de sous-titres, il continue quand même : il vous le signale et travaille sur
les images et la description.

---

## Windows — si ça coince

Claude Code choisit son shell tout seul : **avec** Git for Windows il passe par Git Bash,
**sans** il passe par PowerShell. Les deux fonctionnent, vous n'avez normalement rien à faire.

Si Claude Code réclame Git Bash, ou n'arrive à lancer aucune commande, deux corrections dans
l'ordre :

1. **Installez Git for Windows** — https://git-scm.com/downloads/win, en laissant l'option
   « Add to PATH » cochée. Fermez le terminal, rouvrez-le, relancez `claude`.
2. **S'il est déjà installé mais que Claude Code ne le trouve pas**, donnez-lui le chemin.
   Ouvrez (ou créez) le fichier `C:\Users\VotreNom\.claude\settings.json` et mettez dedans :

   ```json
   { "env": { "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe" } }
   ```

   Les doubles antislashs sont obligatoires en JSON. Relancez Claude Code.

Référence officielle : https://code.claude.com/docs/en/setup

## Les fichiers de ce skill

```
skills/yt-vibe/
├── SKILL.md
├── scripts/yt_vibe.py          ← le programme qui fait le téléchargement
└── references/depannage.md     ← à lire si quelque chose coince
```

Les trois sont installés par le prompt : ils sont listés dans `skills.json`. Après un usage,
vous trouverez un dossier `yt-vibe-out/` (transcript, images, informations) — supprimable
quand vous voulez.

## Désinstaller

Supprimez le dossier `~/.claude/skills/yt-vibe/` — c'est fini.

Sous Windows : `C:\Users\VotreNom\.claude\skills\yt-vibe\`.

`yt-dlp` et `ffmpeg` restent installés sur votre machine — ils servent à plein d'autres choses.
