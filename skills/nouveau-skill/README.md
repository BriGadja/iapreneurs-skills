# `/nouveau-skill` — celui qui fabrique les autres

> La Boîte à Skills — IAPreneurs. Un dossier = un skill = une tâche.

**Vous donnez** : une tâche que vous refaites à la main, décrite avec vos mots.
**Vous obtenez** : un skill installé, **testé devant vous**, et que vous savez relire.

Il ne vous demande pas de savoir écrire un skill. Il vous interviewe une question à la fois,
regarde si l'équivalent existe déjà, construit le vôtre — et surtout **il le prouve** : trois
tests réels, dont un cas limite, avant de dire que c'est prêt. Il ne dit jamais « ça devrait
marcher ».

Il retient aussi votre métier et votre niveau, pour que chaque skill suivant soit écrit dans
votre vocabulaire.

---

## Installation

Ouvrez Claude Code (n'importe où) et collez ceci :

```
Installe le skill « nouveau-skill » de la Boîte à Skills IAPreneurs. Procède ainsi :

1. Lis https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json
   et trouve l'entrée « nouveau-skill ». Elle te donne la liste exacte des fichiers.

2. Pour CHAQUE fichier listé, lis-le à l'adresse
   https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<le chemin du fichier>
   puis écris-le dans mon dossier personnel Claude, en retirant le préfixe « skills/ » :
   « skills/nouveau-skill/SKILL.md » devient « ~/.claude/skills/nouveau-skill/SKILL.md » chez moi.
   Sous Windows, c'est C:\Users\<mon nom>\.claude\skills\nouveau-skill\.
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

**Aucun.** Ce skill ne demande aucune installation.

Si `skill-creator` (le skill officiel d'Anthropic) est présent sur votre machine, il s'en sert ;
sinon il construit lui-même, avec les mêmes exigences. La différence est invisible pour vous.

---

## Exemples de prompts

À copier-coller, en remplaçant par votre tâche à vous.

**Le cas de base**
```
/nouveau-skill
```
Il prend la main et vous interviewe. C'est la façon la plus simple de commencer.

**En décrivant directement la tâche** (le skill se déclenche tout seul) :
```
Chaque lundi je relis mes notes de la semaine et j'en fais un point d'avancement
pour mes clients. J'en ai marre de le refaire à la main.
```

**Un skill de prestation** :
```
/nouveau-skill
Je veux un skill qui prend le compte rendu d'un rendez-vous client et en sort
un mail de relance dans mon ton, avec les points bloquants remontés en premier.
```

**Un skill qui doit calculer juste** (le point important) :
```
/nouveau-skill
Je veux un skill de facturation. Attention : les totaux, la TVA et les arrondis
doivent être exacts au centime — je ne veux pas que l'IA fasse les calculs elle-même.
```

**Forker un gadget de la Boîte pour votre métier** :
```
/nouveau-skill
Je veux partir de /roast et en faire un « roast de propale » : je colle ma proposition
commerciale, il me dit franchement pourquoi le client ne signera pas.
```

**Un skill qui retient vos préférences** :
```
/nouveau-skill
Un skill de post LinkedIn dans MON style. Il doit retenir mes exemples de posts
pour ne plus me redemander mon ton à chaque fois.
```

**Quand une phrase ne déclenche pas votre skill** (le vrai réflexe à avoir) :
```
/nouveau-skill
Mon skill ne se lance pas quand je dis « prépare le point client ».
C'est sa description qu'il faut corriger, pas ma façon de parler.
```

---

## Ce qu'il faut savoir avant de croire le résultat

C'est le seul skill de la Boîte qui **refuse de se déclarer prêt sans preuve**. Il enchaîne
trois tests devant vous, et vous montre la sortie brute de chacun :

1. **le cas normal**, avec une vraie donnée de votre métier ;
2. **l'entrée invalide** — le skill doit échouer proprement et lister ce qui manque, pas cracher
   une trace technique ;
3. **le cas limite** : la valeur nulle, la liste vide, le mois de février, la collision. **C'est
   celui-là qui trouve les vrais bugs**, jamais le premier.

Puis il rejoue le cas normal pour vérifier que la sortie est identique. Si un test échoue, il
corrige et rejoue les trois.

Dernière étape, et c'est la plus importante : **il relit le skill avec vous, section par
section**, à votre niveau. Un skill qu'on ne sait pas relire est un outil qu'on subit.

Ce qu'il ne fait pas : il ne modifie pas un skill déjà installé, il n'en publie aucun, il ne va
pas chercher vos identifiants.

---

## Windows — si ça coince

Pour installer et utiliser ce skill, vous n'avez besoin **ni de Git, ni de Git Bash, ni de WSL** :
le prompt d'installation ne lance aucune commande, et le skill non plus.

Si Claude Code lui-même réclame Git Bash ou n'arrive à exécuter aucune commande, c'est un réglage
de Claude Code, pas de ce skill. Deux corrections, dans l'ordre :

1. **Installez Git for Windows** — https://git-scm.com/downloads/win, en laissant l'option
   « Add to PATH » cochée. Fermez le terminal, rouvrez-le, relancez `claude`.
2. **S'il est déjà installé mais que Claude Code ne le trouve pas**, donnez-lui le chemin.
   Ouvrez (ou créez) `C:\Users\VotreNom\.claude\settings.json` et mettez dedans :

   ```json
   { "env": { "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe" } }
   ```

   Les doubles antislashs sont obligatoires en JSON. Relancez Claude Code.

Référence officielle : https://code.claude.com/docs/en/setup

## Les fichiers de ce skill

```
skills/nouveau-skill/
└── SKILL.md
```

Au premier usage, le skill crée `~/.claude/mon-profil.json` : votre métier, vos outils, votre
niveau. C'est un fichier texte, vous pouvez l'ouvrir, le corriger, le supprimer. Dites-lui
« oublie mon profil » et il l'efface.

## Désinstaller

Supprimez le dossier `~/.claude/skills/nouveau-skill/` — c'est fini.

Sous Windows : `C:\Users\VotreNom\.claude\skills\nouveau-skill\`.

Et `~/.claude/mon-profil.json` si vous voulez effacer aussi ce qu'il a retenu de vous.
