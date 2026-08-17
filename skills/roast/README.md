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
Installe le skill « roast » de la Boîte à Skills IAPreneurs. Procède ainsi :

1. Lis https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json
   et trouve l'entrée « roast ». Elle te donne la liste exacte des fichiers.

2. Pour CHAQUE fichier listé, lis-le à l'adresse
   https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<le chemin du fichier>
   puis écris-le dans mon dossier personnel Claude, en retirant le préfixe « skills/ » :
   « skills/roast/SKILL.md » devient « ~/.claude/skills/roast/SKILL.md » chez moi.
   Sous Windows, c'est C:\Users\<mon nom>\.claude\skills\roast\.
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
