---
name: yt-vibe
description: "Utilise CE skill DÈS QUE l'utilisateur donne une URL YouTube et veut en saisir l'ambiance, le style, le ton ou le contenu visuel : il dit « analyse cette vidéo », « c'est quoi le style de », « récupère le transcript + des screenshots », « inspire-toi de cette vidéo », ou colle un lien youtube.com / youtu.be, même sans demande explicite. Produit transcript + frames clés + analyse vibe/style, sans aucune clé API."
allowed-tools: Bash(python3 *), Bash(yt-dlp *), Bash(ffmpeg *), Read, Write
---

# yt-vibe : l'ADN visuel et sonore d'une vidéo YouTube

**Entrée** : une URL YouTube. **Sortie** : le transcript + des captures aux moments clés +
une analyse de l'ambiance, du style et du ton.

Claude « regarde » vraiment la vidéo (il lit les images) et « l'écoute » (il lit le transcript).
De quoi décortiquer un concurrent, s'inspirer d'un format, réutiliser un style. **Zéro clé API.**

## Étape 1. Vérifier les prérequis

Toujours en premier, à chaque lancement :

```bash
python3 scripts/yt_vibe.py --check
```

Il dit ce qui est présent, ce qui manque, et **la commande exacte pour le système de
l'utilisateur**. S'il sort en erreur, montre sa sortie telle quelle, propose d'installer ce qui
manque, et **arrête-toi là**. Ne lance jamais le pipeline « pour voir ».

Sous Windows, après une installation, il faut fermer et relancer Claude Code : un programme déjà
ouvert garde l'ancien PATH.

## Étape 2. Lancer le pipeline

```bash
python3 scripts/yt_vibe.py "<URL_YOUTUBE>" --frames 12 --workdir yt-vibe-out
```

Il récupère les métadonnées, le transcript (fr puis en) et la vidéo, en extrait les images aux
changements de scène, puis supprime la vidéo (lourde) et ne garde que les images. Chaque étape
dégrade proprement : pas de sous-titres n'empêche pas les images.

Au-delà de ~30 min de vidéo il s'arrête et demande `--yes` : ne le passe pas sans l'accord de
l'utilisateur, le téléchargement peut peser plusieurs Go.

**Lis `yt-vibe-out/MANIFEST.txt` en premier** : il récapitule ce qui a réellement été produit.
Si le script échoue, il explique lui-même les deux causes possibles et la commande pour chacune —
transmets sa sortie plutôt que de la reformuler.

## Étape 3. Analyser la vibe

Regarde les images (`frames/*.jpg`) et lis le transcript (`transcript.vtt`), puis restitue en
« vous », style IAPreneurs :

- **L'ambiance en une phrase** (« tuto carré, fond clair, débit posé, zéro fioriture »).
- **Le style visuel** : palette, montage, plans, incrustations, présence à l'écran.
- **Le style éditorial** : ton, structure, type d'accroche, manière d'expliquer.
- **Ce qui est réutilisable** : 2-3 points concrets.

Les sous-titres automatiques écorchent les termes techniques (« and date » pour « n8n », « cloud
code » pour « Claude Code ») : rétablis-les d'après le sujet. Sans transcript, appuie-toi sur les
images et la description dans `meta.json`.

## Ce qu'il faut dire à l'utilisateur, une fois

**Ça tourne sur SA machine.** Depuis une box, un wifi ou une 4G, ça marche. Depuis un serveur
distant, YouTube répond « confirm you're not a bot » et rien ne sort.

**yt-dlp se périme.** Il parle à YouTube, qui change ses protections : quand un téléchargement
échoue sans raison, c'est presque toujours ça. `--check` affiche l'âge de la version installée et
la bonne commande de mise à jour — qui **dépend de la façon dont yt-dlp a été installé**
(`yt-dlp -U` ne met à jour que le binaire autonome, et échoue silencieusement sur une install
pip, pipx ou brew).

## Handoff

Produit `yt-vibe-out/` (transcript, images, `meta.json`, `MANIFEST.txt`) + l'analyse dans la
conversation.

**Prochaine étape** : « refais-moi un moodboard à partir des images », « écris-moi un script dans
ce style », ou `/yt-vibe` sur une autre URL.
