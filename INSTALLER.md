# Installer un skill de la Boîte

> Ouvrez Claude Code (n'importe où, le dossier n'a pas d'importance) et collez le prompt
> ci-dessous **en remplaçant `NOM-DU-SKILL`** par celui que vous voulez :
> `roast`, `yt-vibe`, `grill-me` ou `nouveau-skill`.
>
> Rien à télécharger, rien à dézipper, aucun terminal à préparer. Ça marche sur macOS, Linux,
> Windows et WSL — le prompt n'utilise aucune commande shell.

---

## Le prompt d'installation

```
Installe le skill « NOM-DU-SKILL » de la Boîte à Skills IAPreneurs. Procède ainsi :

1. Lis https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json
   et trouve l'entrée « NOM-DU-SKILL ». Elle te donne la liste exacte des fichiers.

2. Pour CHAQUE fichier listé, lis-le à l'adresse
   https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<le chemin du fichier>
   puis écris-le dans mon dossier personnel Claude, en retirant le préfixe « skills/ » :
   le fichier « skills/NOM-DU-SKILL/SKILL.md » du dépôt devient
   « ~/.claude/skills/NOM-DU-SKILL/SKILL.md » chez moi.
   Sous Windows, c'est C:\Users\<mon nom>\.claude\skills\NOM-DU-SKILL\.
   Crée les sous-dossiers manquants. Écris les fichiers À L'IDENTIQUE, sans rien reformuler,
   sans rien raccourcir, sans ajouter de commentaire.

3. Si l'entrée a des « prerequis » (des outils externes), vérifie s'ils sont présents sur ma
   machine et dis-moi exactement quoi installer s'il en manque, avec la commande pour MON
   système. N'installe rien sans me demander.

4. INTERDIT : si tu n'arrives pas à lire une de ces adresses, ARRÊTE-TOI et dis-le-moi
   franchement. N'écris jamais un skill de mémoire, ni « une version équivalente », ni un
   fichier reconstitué de tête. Je dois recevoir le fichier du dépôt ou rien du tout.

5. Termine par : la liste des fichiers que tu as réellement écrits (avec leur chemin complet),
   et la phrase exacte à taper pour lancer le skill. Précise-moi qu'il faut relancer Claude
   Code pour que la commande apparaisse.
```

---

## Le prompt de mise à jour

Une installation est une **copie**. Corriger un skill ici ne change rien chez vous tant que vous
ne le retéléchargez pas. Ce prompt le fait, pour un skill ou pour tous :

```
Mets à jour mes skills de la Boîte à Skills IAPreneurs.

1. Lis https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json
2. Regarde lesquels de ces skills j'ai déjà dans ~/.claude/skills/
   (sous Windows : C:\Users\<mon nom>\.claude\skills\).
3. Pour chacun d'eux, retélécharge tous ses fichiers depuis
   https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin>
   et remplace ma version. Ajoute aussi les fichiers qui sont nouveaux dans la liste.
4. Dis-moi, skill par skill, ce qui a changé : « identique », « mis à jour », ou
   « nouveau fichier ». Si rien n'a bougé, dis-le, ne fais pas semblant.
5. Même interdiction que pour l'installation : une adresse illisible = tu t'arrêtes et tu me
   le dis. Tu ne réécris JAMAIS un skill de mémoire.
```

---

## Si ça ne marche pas

**« Je n'arrive pas à lire cette adresse »** — Claude Code doit pouvoir aller sur le web. La
première fois, il demande l'autorisation pour le domaine `raw.githubusercontent.com` : acceptez.
Si vous êtes derrière le réseau d'une entreprise, il est possible que GitHub soit filtré.

**Il a écrit un skill sans télécharger quoi que ce soit** — c'est exactement ce que le point 4
interdit. Supprimez le dossier créé et recommencez en collant le prompt en entier : c'est le
point 4 qui l'empêche d'improviser, ne le retirez pas.

**La commande n'apparaît pas après l'installation** — relancez Claude Code. Les skills sont lus
au démarrage.

**Windows** — vous n'avez besoin ni de Git, ni de Git Bash, ni de WSL pour installer : ce prompt
n'utilise que la lecture web et l'écriture de fichiers. En revanche `yt-vibe` a besoin de deux
outils externes une fois installé, voir son README.
