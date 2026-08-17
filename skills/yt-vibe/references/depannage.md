# /yt-vibe — dépannage & power-ups (lecture à la demande)

> Le SKILL.md reste court. Tout le détail « si ça coince » est ici.

## 1. « Sign in to confirm you're not a bot » (bot-block YouTube)

**Ce que c'est** : YouTube bloque parfois les téléchargements depuis des **IP de datacenter**
(serveurs, VPS, certains réseaux d'entreprise). Le message ressemble à
« Sign in to confirm you're not a bot ».

**Bonne nouvelle pour toi** : depuis la machine d'un membre (IP **résidentielle** :
ta box, ton wifi maison, ta 4G), yt-dlp marche **nativement**, sans blocage. Ce skill
est conçu pour TA machine — pas pour un serveur. Si tu vois ce message, c'est presque
toujours que tu l'exécutes sur un VPS / un serveur distant.

**Si tu es vraiment bloqué** (cas rare, réseau d'entreprise filtrant) :
- Exporte tes cookies YouTube depuis ton navigateur (extension « Get cookies.txt »)
  dans un fichier `cookies.txt`, puis ajoute `--cookies cookies.txt` aux commandes yt-dlp.
- Ne committe JAMAIS ce fichier (il contient ta session). Il est déjà gitignoré.

## 2. yt-dlp casse après une mise à jour YouTube (« version rot »)

yt-dlp est un outil qui court après les changements de YouTube : il casse régulièrement,
et une nouvelle version corrige en général sous quelques jours. Comme tu as copié ce skill
(il n'a pas de vecteur de mise à jour automatique), le réflexe quand un téléchargement
échoue bizarrement :

```bash
yt-dlp -U      # met yt-dlp à jour vers la dernière version
```

L'Étape 0 du skill le lance déjà pour toi. Si ça coince encore, refais `yt-dlp -U`
manuellement — 9 fois sur 10 ça repart.

## 3. Pas de sous-titres sur la vidéo

Certaines vidéos n'ont aucune piste de sous-titres auto. Le pipeline **ne plante pas** :
il continue sur les **frames + la description** (dans `meta.json`) et te le signale dans
le `MANIFEST.txt` (« AUCUN sous-titre dispo »). L'analyse de vibe reste possible — juste
sans le texte parlé.

## 4. Power-up optionnel : Supadata (transcript premium)

Si — et seulement si — tu as déjà une clé **Supadata**, tu peux récupérer un transcript
plus propre (ponctuation, segmentation) via leur API. **Ce n'est jamais requis** : le skill
marche à 100 % sans aucune clé, avec les sous-titres auto de yt-dlp. N'ajoute Supadata que
si tu en as déjà l'usage par ailleurs — un gadget communautaire ne doit dépendre d'aucune infra.

## 5. Nettoyer le jargon du transcript (optionnel)

Les sous-titres auto de YouTube transcrivent souvent mal les termes techniques (« and date »
pour « n8n », « cloud code » pour « Claude Code »…). Au moment d'analyser, corrige
mentalement les coquilles évidentes selon le contexte. Inutile de maintenir une liste figée :
laisse Claude reconstituer le terme correct d'après le sujet de la vidéo.

## 6. Vidéo très longue

Au-delà de ~30 min, le téléchargement peut peser plusieurs Go. Le helper s'arrête et te
demande de confirmer avec `--yes` (ou de choisir une vidéo plus courte). C'est volontaire :
on évite de remplir ton disque sans prévenir.
