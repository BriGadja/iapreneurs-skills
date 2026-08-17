# `/grill-me` — l'interrogatoire qui fait sortir ce que vous n'aviez pas prévu

> La Boîte à Skills — IAPreneurs. Un dossier = un skill = une tâche.

**Vous donnez** : une idée, un plan, une offre, une décision — encore floue, ou trop belle pour
être vraie.
**Vous obtenez** : la même idée, mais dont chaque angle mort a été nommé, et que vous pouvez
défendre.

Au lieu de vous répondre « bonne idée ! », Claude vous **cuisine**. Il pose ses questions par
vagues, chaque réponse en débloque de nouvelles, et il ne s'arrête que quand il ne reste plus
rien d'implicite. Et surtout : **il ne construit rien tant que vous n'avez pas confirmé** que
vous êtes d'accord.

---

## Installation

Ouvrez Claude Code (n'importe où) et collez ceci :

```
Installe le skill « grill-me » de la Boîte à Skills IAPreneurs. Procède ainsi :

1. Lis https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/skills.json
   et trouve l'entrée « grill-me ». Elle te donne la liste exacte des fichiers.

2. Pour CHAQUE fichier listé, lis-le à l'adresse
   https://raw.githubusercontent.com/BriGadja/iapreneurs-skills/main/<le chemin du fichier>
   puis écris-le dans mon dossier personnel Claude, en retirant le préfixe « skills/ » :
   « skills/grill-me/SKILL.md » devient « ~/.claude/skills/grill-me/SKILL.md » chez moi.
   Sous Windows, c'est C:\Users\<mon nom>\.claude\skills\grill-me\.
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

**Aucun.** Ce skill ne demande aucune installation et ne produit aucun fichier : tout se passe
dans la conversation. Il marche dès le premier lancement.

---

## Exemples de prompts

À copier-coller, en remplaçant par votre sujet à vous.

**Le cas de base**
```
/grill-me
Je veux lancer une offre d'automatisation n8n à 1 500 € pour les cabinets comptables.
```

**Sans même taper la commande** (le skill se déclenche tout seul) :
```
Challenge-moi sur ce projet, qu'est-ce que j'ai oublié ?
<décrivez votre projet en quelques lignes>
```

**Avant d'écrire la moindre ligne de code** :
```
/grill-me
Je veux construire un outil qui transforme mes comptes rendus de rendez-vous en devis.
Avant qu'on code quoi que ce soit, cuisine-moi jusqu'à ce que le périmètre soit net.
```

**Sur une décision, pas un projet** :
```
/grill-me
J'hésite entre facturer à la journée et facturer au forfait sur mes missions IA.
Fais-moi trancher pour de bon.
```

**Sur un plan que quelqu'un vous a remis** :
```
/grill-me
Voilà le plan que m'a envoyé mon prestataire. Trouve ce qui n'est pas dit dedans :
<collez le plan>
```

**Sur un fichier de votre machine** :
```
/grill-me
Lis mon-plan.md dans ce dossier et grille-moi dessus.
```

**Pour clore** (quand vous n'avez plus rien à ajouter) :
```
C'est bon, on est d'accord. Fais-moi la synthèse de ce qu'on a tranché.
```

---

## Comment ça se passe, concrètement

Vous recevez des questions **numérotées, par vagues**, chacune accompagnée de la réponse que
Claude recommande :

```
❓ **Q1** — **Qui paie ?** : Le cabinet lui-même, ou son client final ?
➡️ Le cabinet — sinon vous vendez à quelqu'un que vous ne rencontrerez jamais.

❓ **Q2** — **Quel volume déclenche l'achat ?** : ...
➡️ ...
```

Vous répondez à la vague entière, il en recalcule une nouvelle à partir de vos réponses. Vous
pouvez répondre « je ne sais pas » — c'est justement une information.

Deux règles qu'il s'impose, et qui font la différence :

- **Les faits sont son travail, pas le vôtre.** S'il a besoin de savoir ce que contient un
  fichier ou ce qu'affiche une page, il va le chercher lui-même. Il ne vous demande que ce que
  vous seul pouvez trancher.
- **Il n'agit pas avant votre feu vert.** Ce skill sert à penser, pas à produire.

Comptez 3 à 6 vagues sur un vrai sujet. C'est plus long qu'une réponse instantanée — c'est le
principe.

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
skills/grill-me/
└── SKILL.md
```

## Désinstaller

Supprimez le dossier `~/.claude/skills/grill-me/` — c'est fini.

Sous Windows : `C:\Users\VotreNom\.claude\skills\grill-me\`.
