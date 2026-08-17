# Installer un skill de la Boîte

> Ouvrez Claude Code (n'importe où, le dossier n'a pas d'importance) et collez le prompt
> ci-dessous **en remplaçant `NOM-DU-SKILL`** par celui que vous voulez :
> `roast`, `yt-vibe`, `grill-me` ou `nouveau-skill`.
>
> Rien à dézipper, aucun dossier à préparer. Le prompt fait télécharger les fichiers par Claude,
> avec le shell qu'il a sous la main : `curl` sous macOS, Linux, WSL et Git Bash ;
> `Invoke-WebRequest` sous PowerShell. **Chaque machine a l'un des deux** — vous n'avez donc
> besoin ni de Git, ni de Git Bash, ni de WSL.

---

## Le prompt d'installation

```
Installe le skill « NOM-DU-SKILL » de la Boîte à Skills IAPreneurs.

1. Lis l'index https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json et prends l'entrée « NOM-DU-SKILL » : elle donne la liste
   exacte des fichiers de ce skill.

2. TÉLÉCHARGE chaque fichier de la liste. Ne le recopie pas de tête, ne le reformule pas.
   Utilise le shell dont tu disposes :

   - Bash (macOS, Linux, WSL, Git Bash) :
       mkdir -p ~/.claude/skills/NOM-DU-SKILL
       curl -fsSL https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin du fichier> -o ~/.claude/skills/NOM-DU-SKILL/<nom du fichier>

   - PowerShell (Windows sans Git for Windows) :
       New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills\NOM-DU-SKILL"
       Invoke-WebRequest -Uri https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin> -OutFile "$env:USERPROFILE\.claude\skills\NOM-DU-SKILL\<fichier>"

   Le préfixe « skills/ » du dépôt disparaît à l'arrivée :
   « skills/NOM-DU-SKILL/SKILL.md » devient « ~/.claude/skills/NOM-DU-SKILL/SKILL.md ».
   Certains skills ont des sous-dossiers (scripts/, references/) : recrée-les à l'identique.

3. PROUVE que ça a marché. Affiche la liste des fichiers écrits avec leur taille, et les trois
   premières lignes du SKILL.md : il doit commencer par --- et contenir « name: NOM-DU-SKILL ».
   Un fichier vide, absent, ou qui commence par du HTML = l'installation a échoué. Dis-le.

4. INTERDIT : ne fabrique JAMAIS le contenu d'un skill. Si un téléchargement échoue, tu
   t'arrêtes et tu me le dis. Un skill réécrit de mémoire ressemble au vrai et ne fait pas
   la même chose — c'est le pire résultat possible, pire qu'une erreur.

5. Si l'entrée a des « prerequis » (outils externes), vérifie s'ils sont présents et dis-moi
   quoi installer pour MON système. N'installe rien sans mon accord.

6. Termine par la phrase à taper pour lancer le skill, et rappelle-moi de relancer Claude Code
   pour qu'il apparaisse.
```

---

## Le prompt de mise à jour

Une installation est une **copie**. Corriger un skill ici ne change rien chez vous tant que vous
ne le retéléchargez pas. Ce prompt le fait, pour un skill ou pour tous :

```
Mets à jour mes skills de la Boîte à Skills IAPreneurs.

1. Lis l'index https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json
2. Regarde lesquels de ces skills j'ai déjà dans ~/.claude/skills/
   (Windows : C:\Users\<mon nom>\.claude\skills\).
3. Pour chacun, retélécharge TOUS ses fichiers depuis https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin>
   avec curl (ou Invoke-WebRequest sous PowerShell) et remplace ma version.
   Ajoute aussi les fichiers qui sont nouveaux dans la liste.
4. Dis-moi, skill par skill, ce qui a changé : « identique », « mis à jour » ou
   « nouveau fichier ». Si rien n'a bougé, dis-le, ne fais pas semblant.
5. Même interdiction qu'à l'installation : un téléchargement qui échoue = tu t'arrêtes et tu
   me le dis. Tu ne réécris JAMAIS un skill de mémoire.
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

**Windows** — rien à installer pour que le prompt fonctionne. Sans Git for Windows, Claude Code
utilise PowerShell, et `Invoke-WebRequest` y est disponible d'origine
(https://code.claude.com/docs/en/setup). En revanche `/yt-vibe` a besoin de deux outils externes
**une fois installé** : voir son README.

**Le skill installé ne fait pas ce qu'annonce sa fiche** — vérifiez que le fichier a bien été
téléchargé et non reconstitué : `~/.claude/skills/<nom>/SKILL.md` doit commencer par `---` et
faire plusieurs kilooctets. Un fichier court et lisse est un fichier réécrit de mémoire :
supprimez-le et recommencez.
