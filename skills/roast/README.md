# `/roast` — l'avis cash sur votre page (+ 3 correctifs qui comptent)

> La Boîte à Skills — IAPreneurs. Un dossier = un skill = une tâche.

**Vous donnez** : l'adresse d'une page (landing, site vitrine, page de vente).
**Vous obtenez** : une critique franche, sans langue de bois, puis **exactement 3 correctifs**
classés par impact — les trois choses à changer, dans l'ordre.

Pourquoi trois ? Parce qu'une liste de quinze améliorations ne se corrige jamais. La discipline
de prioriser, c'est toute la valeur du skill.

---

## Installation

Ouvrez Claude Code (n'importe où) et collez ceci :

```
Installe le skill « roast » de la Boîte à Skills IAPreneurs.

1. Lis l'index https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json et prends l'entrée « roast » : elle donne la liste
   exacte des fichiers de ce skill.

2. TÉLÉCHARGE chaque fichier de la liste. Ne le recopie pas de tête, ne le reformule pas.
   Utilise le shell dont tu disposes :

   - Bash (macOS, Linux, WSL, Git Bash) :
       mkdir -p ~/.claude/skills/roast
       curl -fsSL https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin du fichier> -o ~/.claude/skills/roast/<nom du fichier>

   - PowerShell (Windows sans Git for Windows) :
       New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills\roast"
       Invoke-WebRequest -Uri https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<chemin> -OutFile "$env:USERPROFILE\.claude\skills\roast\<fichier>"

   Le préfixe « skills/ » du dépôt disparaît à l'arrivée :
   « skills/roast/SKILL.md » devient « ~/.claude/skills/roast/SKILL.md ».
   Certains skills ont des sous-dossiers (scripts/, references/) : recrée-les à l'identique.

3. PROUVE que ça a marché. Affiche la liste des fichiers écrits avec leur taille, et les trois
   premières lignes du SKILL.md : il doit commencer par --- et contenir « name: roast ».
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

**Aucun.** Ce skill ne demande aucune installation : il lit la page avec un outil intégré à
Claude Code. Il marche dès le premier lancement.

*(La première fois, Claude peut vous demander l'autorisation d'aller lire une adresse web.
Acceptez : c'est exactement ce que le skill est censé faire.)*

---

## Exemples de prompts

À copier-coller tels quels, en remplaçant l'adresse par la vôtre.

**Le cas de base**
```
/roast https://mon-site.fr
```

**Sans même taper la commande** (le skill se déclenche tout seul) :
```
Donne-moi un avis cash sur https://mon-site.fr, qu'est-ce qui cloche ?
```

**La page d'un prospect** — le meilleur prétexte de premier contact qui existe :
```
/roast https://le-site-de-mon-prospect.fr
Je veux m'en servir comme accroche pour un premier message. Reste factuel, pas humiliant.
```

**Cibler un public précis** :
```
/roast https://mon-site.fr
Ma cible, ce sont des dirigeants de PME de 10 à 50 personnes qui n'y connaissent rien en IA.
Juge la page de leur point de vue à eux.
```

**Enchaîner après la critique** (une fois les 3 correctifs affichés) :
```
Réécris-moi le titre et le bouton principal avec le correctif n°1.
```
```
J'ai fait les changements, refais l'analyse sur la même adresse.
```

**Quand la page ne charge pas** (site en JavaScript lourd, accès bloqué) :
```
La page ne se charge pas pour toi. Voilà le texte, roaste-le :
<collez ici le contenu de votre page>
```

---

## Ce qu'il faut savoir avant de croire le résultat

Le skill lit le **texte et la structure** de la page. Il **ne la voit pas s'afficher**. Il a donc
l'interdiction formelle de vous parler de « ligne de flottaison », de contraste ou de vitesse de
chargement : ce sont des choses qui se voient, pas qui se lisent. Il annonce d'ailleurs en une
ligne, avant sa critique, ce qu'il a réellement lu.

Et si votre page est déjà bonne, il le dit : les 3 entrées deviennent des **renforcements** au
lieu de reproches. Un outil qui trouve toujours trois fautes n'analyse rien, il remplit un
gabarit.

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
skills/roast/
└── SKILL.md
```

## Désinstaller

Supprimez le dossier `~/.claude/skills/roast/` — c'est fini.

Sous Windows : `C:\Users\VotreNom\.claude\skills\roast\`.
