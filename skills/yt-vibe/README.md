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
Installe le skill « yt-vibe » de la Boîte à Skills IAPreneurs.

1. Lis l'index https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json et prends l'entrée « yt-vibe » : elle donne la liste
   exacte des fichiers de ce skill.

2. TÉLÉCHARGE chaque fichier de la liste. Ne le recopie pas de tête, ne le reformule pas.
   Utilise le shell dont tu disposes :

   - Bash (macOS, Linux, WSL, Git Bash) :
       mkdir -p ~/.claude/skills/yt-vibe
       curl -fsSL https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin du fichier> -o ~/.claude/skills/yt-vibe/<nom du fichier>

   - PowerShell (Windows sans Git for Windows) :
       New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills\yt-vibe"
       Invoke-WebRequest -Uri https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin> -OutFile "$env:USERPROFILE\.claude\skills\yt-vibe\<fichier>"

   Le préfixe « skills/ » du dépôt disparaît à l'arrivée :
   « skills/yt-vibe/SKILL.md » devient « ~/.claude/skills/yt-vibe/SKILL.md ».
   Certains skills ont des sous-dossiers (scripts/, references/) : recrée-les à l'identique.

3. PROUVE que ça a marché. Affiche la liste des fichiers écrits avec leur taille, et les trois
   premières lignes du SKILL.md : il doit commencer par --- et contenir « name: yt-vibe ».
   Un fichier vide, absent, ou qui commence par du HTML = l'installation a échoué. Dis-le.

4. INTERDIT : ne fabrique JAMAIS le contenu d'un skill. Si un téléchargement échoue, tu
   t'arrêtes et tu me le dis. Un skill réécrit de mémoire ressemble au vrai et ne fait pas
   la même chose — c'est le pire résultat possible, pire qu'une erreur.

5. Si l'entrée a des « prerequis » (outils externes), vérifie s'ils sont présents et dis-moi
   quoi installer pour MON système. N'installe rien sans mon accord.

6. Termine par la phrase à taper pour lancer le skill, et rappelle-moi de relancer Claude Code
   pour qu'il apparaisse.
```

Puis **relancez Claude Code** : les skills sont lus au démarrage.

Claude télécharge les fichiers avec le shell qu'il a sous la main — `curl` sous macOS, Linux,
WSL et Git Bash, `Invoke-WebRequest` sous PowerShell. **Chaque machine a l'un des deux** : vous
n'avez besoin ni de Git, ni de Git Bash, ni de WSL, et il n'y a rien à dézipper.

Pour mettre à jour plus tard, voir [INSTALLER.md](../../INSTALLER.md#le-prompt-de-mise-à-jour) —
une installation est une **copie**, elle ne se met pas à jour toute seule.

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
