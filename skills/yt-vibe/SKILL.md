---
name: yt-vibe
description: "Utilise CE skill DÈS QUE l'utilisateur donne une URL YouTube et veut en saisir l'ambiance, le style, le ton ou le contenu visuel : il dit « analyse cette vidéo », « c'est quoi le style de », « récupère le transcript + des screenshots », « inspire-toi de cette vidéo », ou colle un lien youtube.com / youtu.be, même sans demande explicite. Produit transcript + frames clés + analyse vibe/style, sans aucune clé API."
allowed-tools: Bash(yt-dlp *), Bash(ffmpeg *), Bash(python3 *), Read, Write
requires:
  bins: [yt-dlp, ffmpeg]
---

# yt-vibe : l'ADN visuel et sonore d'une vidéo YouTube, en une commande

## Pour quoi faire

**Entrée** : une URL YouTube.
**Sortie** : le transcript de la vidéo + N screenshots clés (les moments où l'image change) +
une analyse de **l'ambiance, du style et du ton** (visuel ET éditorial).

L'effet magique : Claude « regarde » vraiment la vidéo (il lit les frames) et « l'écoute »
(il lit le transcript), puis t'en restitue le vibe, exactement ce qu'il faut pour t'inspirer
d'un format, décortiquer un concurrent, ou réutiliser un style.

C'est le gadget le plus impressionnant de la Boîte… et c'est aussi **la leçon** : un bon skill
qui dépend d'outils externes **vérifie ses prérequis et ne plante jamais**. Regarde l'Étape 0.

## Prérequis

Ce skill a besoin de **2 binaires** (🟡), c'est tout, **aucune clé API** :
- **`yt-dlp`** : télécharge vidéo, sous-titres et métadonnées depuis YouTube.
- **`ffmpeg`** : extrait les frames clés de la vidéo.
- (`python3` est quasi toujours déjà là, il orchestre le pipeline.)

> ⚠️ **Tourne sur TA machine, pas sur un serveur.** Depuis une IP **résidentielle** (ta box,
> ton wifi, ta 4G), yt-dlp marche nativement. Sur un VPS / serveur distant (IP datacenter),
> YouTube peut bloquer (« confirm you're not a bot »), ce skill n'est pas fait pour ça.
> Détail + contournement cookies : `references/depannage.md`.

## Comment procéder

> *(Instructions pour toi, le skill : « tu » = toi qui exécutes ; « vous » = le membre.)*

### Étape 0. Check des binaires (le garde-fou anti-SAV)

Lance ce check **avant tout**. S'il manque un binaire, il affiche la commande d'install exacte
et **STOP proprement**, jamais de plantage cryptique.

🔴 **Deux shells possibles.** Sur macOS, Linux, WSL et Windows-avec-Git-for-Windows, Claude Code
te donne un outil **Bash**. Sur Windows **sans** Git for Windows, il te donne un outil
**PowerShell** — et `command -v` n'y existe pas. Regarde l'outil dont tu disposes et lance le
bloc correspondant, jamais l'autre.

**Colonne Bash** :

```bash
MISSING=
for bin in yt-dlp ffmpeg python3; do
  command -v "$bin" >/dev/null 2>&1 || {
    echo "MANQUANT : $bin";
    MISSING=1;
  }
done
if [ -n "$MISSING" ]; then
  case "$(uname -s)" in
    Darwin)               echo "-> brew install yt-dlp ffmpeg" ;;
    MINGW*|MSYS*|CYGWIN*) echo "-> winget install --id yt-dlp.yt-dlp -e ; winget install --id Gyan.FFmpeg -e" ;;
    *)                    echo "-> sudo apt install yt-dlp ffmpeg" ;;
  esac
  echo "Installe puis relance /yt-vibe. Sous Windows, relance AUSSI Claude Code (le PATH d'un processus deja lance ne bouge pas)."
else
  # Anti version-rot : yt-dlp casse souvent suite aux changements YouTube.
  # Un skill copie n'a pas d'autre vecteur de MAJ, on le met a jour a chaque run.
  yt-dlp -U >/dev/null 2>&1 || true
  echo "Prerequis OK."
fi
```

**Colonne PowerShell** :

```powershell
$manque = @()
foreach ($bin in @("yt-dlp","ffmpeg","python")) {
  if (-not (Get-Command $bin -ErrorAction SilentlyContinue)) { $manque += $bin }
}
if ($manque.Count -gt 0) {
  Write-Output "MANQUANT : $($manque -join ' ')"
  Write-Output "-> winget install --id yt-dlp.yt-dlp -e --accept-package-agreements --accept-source-agreements"
  Write-Output "-> winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements"
  Write-Output "Puis QUITTE ET RELANCE Claude Code : le PATH d'un processus deja lance ne bouge pas."
} else {
  yt-dlp -U 2>&1 | Out-Null
  Write-Output "Prerequis OK."
}
```

Tant qu'il manque un binaire, **tu t'arrêtes là** et tu affiches la commande. Tu ne lances pas
le pipeline « pour voir ».

> **Windows, accents** : si `yt_vibe.py` s'arrête sur une `UnicodeEncodeError` en affichant du
> texte accentué depuis PowerShell 5.1, relance-le en préfixant `PYTHONIOENCODING=utf-8`
> (ou mets Claude Code à jour : le défaut est corrigé côté Claude Code depuis la v2.1.214).

### Étape 1. Lancer le pipeline zéro-clé

Tout le téléchargement + l'extraction des frames est dans le helper autonome
`scripts/yt_vibe.py` (livré avec le skill). Lance-le avec l'URL :

```bash
python3 scripts/yt_vibe.py "<URL_YOUTUBE>" --frames 12 --workdir yt-vibe-out
```

Ce qu'il fait, dans l'ordre (avec dégradation propre à chaque étape) :
- **Métadonnées** (`yt-dlp --dump-json`) → `meta.json` (titre, durée, description, tags, chaîne).
  Il lit aussi la **durée** : au-delà de ~30 min il s'arrête et te demande de confirmer avec
  `--yes` (garde-fou : éviter de télécharger plusieurs Go sans prévenir).
- **Transcript** (`yt-dlp --write-auto-subs --sub-langs fr,en --skip-download`) → `transcript.vtt`
  (fr en priorité). **Pas de sous-titres ?** Il continue sans planter et te le signale.
- **Vidéo** (`yt-dlp -f "best[height<=720]/best"`) puis **frames clés** (`ffmpeg` détection de
  scène, fallback intervalle si trop peu de scènes) → `frames/frame_NNN.jpg`. La vidéo lourde
  est supprimée après extraction, on ne garde que les frames.

Résultat : un dossier `yt-vibe-out/` avec `meta.json`, `transcript.vtt`, `frames/`, et un
`MANIFEST.txt` qui récapitule ce qui a été produit. **Lis le `MANIFEST.txt` en premier.**

### Étape 2. Analyser la vibe

Maintenant, Claude fait le travail intelligent (built-in, aucune clé) :
1. **Regarde les frames** : ouvre `frames/*.jpg` (vision), couleurs dominantes, mise en scène,
   rythme de montage, décor, présence à l'écran, typographie des incrustations.
2. **Lis le transcript** (`transcript.vtt`) : ton, vocabulaire, structure narrative, accroches.
   Corrige mentalement les coquilles de transcription auto (ex. « and date » → « n8n »).
   Si pas de transcript, appuie-toi sur la description (`meta.json`) + les frames.
3. **Restitue le vibe** au membre, en « vous », style IAPreneurs :
   - **L'ambiance en une phrase** (ex. « tuto carré, fond clair, débit posé, zéro fioriture »).
   - **Le style visuel** : palette, montage, plans, incrustations.
   - **Le style éditorial** : ton, structure, type d'accroche, manière d'expliquer.
   - **Ce que tu peux en réutiliser** : 2-3 points concrets si le membre veut s'en inspirer.

> Power-up **optionnel** : si (et seulement si) tu as déjà une clé **Supadata**, tu peux
> récupérer un transcript premium, **jamais requis**, le skill marche à 100 % sans aucune clé.
> Voir `references/depannage.md`.

## Handoff

Le skill produit le dossier `yt-vibe-out/` + une analyse de vibe directement dans la conversation.

**Prochaine étape** : demande « refais-moi le moodboard à partir des frames », « écris un script
dans ce style », ou relance `/yt-vibe {autre URL}`. Si un téléchargement coince : `yt-dlp -U`
puis relance (voir `references/depannage.md`).
