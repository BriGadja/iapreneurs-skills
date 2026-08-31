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

## Étape 1. Regarder la machine

Toujours en premier, à chaque lancement :

```bash
python3 scripts/yt_vibe.py --check
```

Il **rapporte des faits** — plateforme, outils présents ou absents, versions, chemins, méthode
d'installation de yt-dlp, indices de machine distante. Il ne prescrit rien, et c'est voulu :
il ne connaît ni la distribution, ni le gestionnaire de paquets, ni les droits de l'utilisateur.

**C'est toi qui raisonnes**, parce que tu connais cet environnement et pas lui. À partir de son
rapport et de ce que tu sais déjà de cette machine (le `CLAUDE.md` du projet, l'historique de la
session, ce que l'utilisateur t'a dit) :

- **Un outil indispensable manque** → propose la voie d'installation qui convient *à cette
  machine-là* : le gestionnaire de paquets réellement utilisé, avec ou sans `sudo`, en tenant
  compte du fait que c'est un poste local, un WSL, un conteneur ou un serveur distant.
  Demande confirmation. **N'installe rien sans accord**, et arrête-toi là : ne lance jamais le
  pipeline « pour voir ».
- **yt-dlp est signalé périmé** → la bonne commande de mise à jour dépend de la ligne
  « installé via » du rapport. `yt-dlp -U` ne met à jour **que** le binaire autonome : sur une
  installation pip ou pipx, il sort en erreur sans rien faire.
- **Le rapport signale une machine distante** (SSH, conteneur, pas d'affichage) → préviens
  l'utilisateur avant de lancer : YouTube refuse les IP de datacenter. Ce n'est pas une panne du
  skill, et ça ne se contourne pas proprement.
- **Après une installation sous Windows** → il faut fermer et relancer Claude Code, un programme
  déjà ouvert garde l'ancien PATH.

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

## Livrer, court

L'analyse EST le livrable : ce qui compte, c'est la vibe restituée, pas le récit de la mécanique.
Termine sur le dossier produit et une suite possible, et arrête-toi.

🔴 **Pas de « notes techniques » en fin de réponse.** Pas de compte rendu des tentatives, pas de
détail sur le client YouTube employé, pas de rappel des limites quand tout s'est bien passé. Le
script gère ses replis tout seul et le signale déjà dans sa sortie si besoin. Une clôture chargée
donne l'impression que ça a été laborieux alors que le résultat est bon.

Deux exceptions, et une seule phrase chacune : **rien n'a pu être récupéré** (dis la cause et la
suite), ou **le résultat est partiel** — pas de sous-titres, peu d'images — auquel cas dis sur
quoi ton analyse s'appuie vraiment.

## Ce qu'il faut savoir, sans le réciter

**Ça tourne sur SA machine.** Depuis une box, un wifi ou une 4G, ça marche. Depuis un serveur
distant, YouTube répond « confirm you're not a bot » et rien ne sort. À dire seulement si la
question se pose, ou si ça échoue.

**Les refus de YouTube sont gérés.** yt-dlp se fait passer pour une application YouTube, et
YouTube en refuse régulièrement une : le téléchargement tombe en 403 pendant que les sous-titres
passent. Le script essaie plusieurs clients l'un après l'autre et te dit lequel a fonctionné.
**N'ajoute pas d'options `--extractor-args` toi-même**, c'est déjà fait.

**yt-dlp se périme.** Quand un téléchargement échoue sans raison, c'est souvent ça. `--check`
donne l'âge de la version et la façon dont elle a été installée — de quoi trouver la bonne
commande pour cette machine.

## Handoff

Produit `yt-vibe-out/` (transcript, images, `meta.json`, `MANIFEST.txt`) + l'analyse dans la
conversation.

**Prochaine étape** : « refais-moi un moodboard à partir des images », « écris-moi un script dans
ce style », ou `/yt-vibe` sur une autre URL.
