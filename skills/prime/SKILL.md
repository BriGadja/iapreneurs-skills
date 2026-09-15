---
name: prime
description: "Utilise CE skill DÈS QUE l'utilisateur ouvre une session sur un projet : il tape « /prime », dit « on en était où », « fais le point », « par quoi je commence », « rappelle-moi ce projet », ou il arrive sur un dossier que vous n'avez encore jamais regardé ensemble, même sans demande explicite. Il se lance SANS aucun argument. Au premier passage il audite le dossier et installe avec l'utilisateur son socle de démarrage (un CLAUDE.md qui dit ce qu'est le projet, un STATUS.md qui porte le reste à faire) ; tous les matins suivants il rend le point en trente secondes et propose par quoi commencer."
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Bash(git *)
---

# /prime : ce qu'on tape le matin, avant tout le reste

## Pour quoi faire

**Entrée** : rien. Pas d'argument, jamais. Vous tapez `/prime` en arrivant.
**Sortie** : le point sur votre projet en trente secondes, et une proposition de par quoi commencer.

Au **premier** passage, il fait autre chose : il regarde votre dossier, vous dit ce qu'il a compris,
et vous propose le socle qui manque pour que les matins suivants marchent tout seuls. Sur un
dossier vide, ce socle il le crée avec vous. Sur un projet qui existe déjà, il vous dit ce qui est
là, ce qui manque, et ce qu'il vaut la peine d'y brancher.

Après ça, la règle est simple : **vous tapez `/prime` chaque matin, et ça marche.**

## Aucune dépendance

Ce skill ne dépend d'aucun outil à installer, il marche immédiatement. Il lit des fichiers avec les
outils intégrés de Claude Code, et se sert de `git` s'il y en a un. Rien à télécharger, aucune clé,
aucun compte.

---

## Comment procéder

> *(Instructions pour toi, le skill. Ici « tu » = toi qui exécutes ; « vous » = la personne, à qui
> tu t'adresses du début à la fin.)*
>
> 🔴 **Ce fichier dit ce que tu dois obtenir, pas comment t'y prendre.** Tu as ce dossier sous les
> yeux, son `CLAUDE.md`, l'historique de la conversation et la machine de cette personne. Ce
> fichier n'a rien de tout ça. Là où il décrit un résultat, c'est à toi de choisir les moyens :
> quels fichiers ouvrir, dans quel ordre, quoi proposer. Les seules lignes qui ne se négocient pas
> sont celles marquées 🔴.

### Étape 1. Savoir où on met les pieds

Trois choses à établir avant d'agir, dans l'ordre.

**1. Est-ce un projet du kit ?** Si le dossier contient un `PRD.md` à la racine **et** un
`docs/plans/` ou `docs/specs/`, il a été monté avec le kit Claude Code des IAPreneurs. Ce kit a
**son propre `/prime`**, meilleur que celui-ci sur ces projets-là : il connaît les phases, les
SPECs, les décisions. S'il est masqué, c'est parce qu'un skill installé pour tous les projets passe
avant un skill installé dans un projet. Dis-le en une fois, proprement :

> « Ce projet vient du kit IAPreneurs, qui a son propre `/prime` : il connaît vos phases, vos SPECs
> et vos décisions, et il est meilleur que moi ici. Il est masqué parce que je suis installé pour
> tous vos projets. Pour lui rendre la main : supprimez `~/.claude/skills/prime/` et réinstallez-moi
> projet par projet. Je continue quand même pour cette fois ? »

Ne repose jamais la question deux fois dans la même session.

**2. Le socle est-il là ?** Un `CLAUDE.md` à la racine (ou dans `.claude/`) **et** un `STATUS.md`.

- **Les deux existent** → c'est un matin ordinaire, va à l'**Étape 4**.
- **Il en manque un ou les deux** → premier passage, enchaîne sur l'Étape 2.

**3. Cas particuliers.** Si la personne a dit « reconfigure », « refais le tour », traite-le comme
un premier passage, mais relis d'abord ce qui existe et pars de là. Si elle a donné un argument
malgré tout (un nom de dossier, un sujet), prends-le comme une indication de cadrage et continue :
le skill n'en exige aucun.

### Étape 2. (premier passage) L'audit

Tu vas dire à quelqu'un ce qu'est son propre projet. **Ne le devine pas : regarde.** Choisis
toi-même quoi ouvrir ; ce qui compte est ce que tu dois pouvoir dire à la fin :

- **Ce que c'est**, en une phrase, et pour qui.
- **Comment c'est fait** : la technique s'il y en a (les dépendances d'un `package.json` ou d'un
  `requirements.txt` en disent plus long que le README), la forme sinon (des documents, des notes,
  des exports).
- **Où ça en est** : la dernière activité, ce qui semble en cours, ce qui a été commencé et
  abandonné.
- **Ce qui manque pour bien comprendre**, dit franchement.

Un `CLAUDE.md`, un `README.md`, la forme du dossier sur deux niveaux, les fichiers de dépendances,
les `TODO`/`FIXME`, les fichiers modifiés récemment, et `git log` s'il y a un dépôt : voilà des
pistes, pas une liste à cocher. Un dossier sans git n'est pas un problème, beaucoup de très bons
projets n'en ont pas : passe sans commenter.

🔴 **Interdit : inventer le projet.** Si le dossier est vide, ou ne contient que quelques documents
sans contexte, dis-le tel quel (« je vois trois fichiers Word et rien qui explique le projet ») et
demande de te le raconter en deux phrases. Un audit qui décrit un projet plausible mais faux est
pire qu'un audit vide : il a l'air juste.

🔴 **Interdit : présumer le métier.** Cette personne vend peut-être des poêles à bois, tient un
cabinet, fait du conseil. Tu décris ce que tu vois, tu ne remplis pas les trous avec le vocabulaire
d'un secteur.

### Étape 3. (premier passage) Montrer, faire corriger, puis poser le socle

**D'abord montre ce que tu as compris**, en une dizaine de lignes, et termine par « je me trompe
quelque part ? ». **Attends la réponse.** Ce n'est pas une politesse : c'est le moment où un mot
corrige ce que tu aurais mis dix minutes à déduire.

**Ensuite, propose le socle.** Deux fichiers, pas trois, et ce sont les fichiers de Claude Code,
pas une invention de ce skill :

| Fichier | Ce qu'il porte | Qui l'écrit |
|---|---|---|
| `CLAUDE.md` | ce qu'est le projet, et ce qu'il faut relire ou surveiller au démarrage | vous deux, une fois |
| `STATUS.md` | ce qui est en cours et ce qui reste à faire | lui, à chaque passage |

**Sur un dossier vide ou presque**, sois franchement proactif : c'est là que le skill rend le plus
de service. Propose de créer les deux, explique en une phrase à quoi chacun sert, et écris-les dès
qu'on te dit oui. Ne fais pas un interrogatoire pour les remplir : deux ou trois lignes honnêtes
valent mieux qu'un formulaire, et le reste se remplira tout seul à l'usage.

**Sur un projet qui existe déjà**, ne réécris rien par-dessus. Dis ce qui est là, ce qui manque, et
propose l'ajout minimal. Si un `CLAUDE.md` existe, **ajoute** le bloc de démarrage à la fin sans
toucher au reste. Si un `STATUS.md` existe déjà avec un autre format, garde son format.

Le bloc à ajouter au `CLAUDE.md`, court, adapté à ce projet-ci :

```markdown
## Au démarrage

`/prime` se lance au début de chaque session. Il lit `STATUS.md`, qui porte le reste à faire.

**À relire à chaque fois** : {les fichiers qui évitent de repartir à côté, avec la raison de
chacun en quelques mots. Rien si la question ne se pose pas.}

**À surveiller** : {un ou deux sujets sur lesquels regarder ce qui est sorti de neuf. Deux
maximum : au-delà, le point devient une revue de presse et personne ne le lit. Rien si la
question ne se pose pas.}
```

Et le `STATUS.md`, qui n'a pas besoin d'être plus compliqué que ça :

```markdown
# STATUS

_Tenu à jour par `/prime`. Vous pouvez l'éditer à la main quand vous voulez._

## En cours
- {ce qui est commencé}

## À faire
- {la suite, du plus utile au moins utile}

## Fait
- {une ligne par chose finie, la plus récente en haut}
```

🔴 **N'écris aucun fichier sans accord explicite**, et dis à chaque fois le chemin exact de ce que
tu viens d'écrire. Ce sont ses fichiers, pas les tiens.

**Enfin, propose ce qui vaut la peine d'être branché.** Au maximum trois choses, tirées de ce que
tu as vu dans CE projet, chacune avec la raison : un `.gitignore` qui manque alors qu'un fichier de
mots de passe traîne, un dépôt git absent sur un travail qui mériterait un historique, une veille
utile sur l'outil dont tout dépend. **Jamais une liste de bonnes pratiques génériques.** Si tu n'as
rien de solide à proposer, ne propose rien.

Puis enchaîne directement sur un vrai point (Étape 4) : elle vient de paramétrer, elle doit voir
tout de suite ce que ça donne.

### Étape 4. (tous les matins) Le point

C'est ce qui sera vu tous les jours. **Il se lit en trente secondes.**

Ce que tu dois avoir regardé avant d'écrire une ligne :

1. `CLAUDE.md` et `STATUS.md`.
2. Ce que le bloc « Au démarrage » demande de relire. Pour de vrai. Si un fichier a disparu,
   signale-le en une ligne et propose de le retirer.
3. Ce qui a bougé depuis la dernière fois : les commits récents s'il y a un git, les fichiers
   modifiés récemment sinon.
4. Les sujets « à surveiller », une recherche par sujet, pas plus. Ne garde que ce qui est neuf
   **et** utile à ce projet. Rien d'intéressant ? dis « rien de neuf sur {sujet} » et passe.
   🔴 **Chaque trouvaille vient avec son URL complète et cliquable** : une information sans sa
   source n'est pas vérifiable.

Puis rends le point, dans cet esprit :

```
## {Nom du projet}

**Le projet** : {une phrase}
**Depuis la dernière fois** : {ce qui a bougé, ou « rien depuis le {date} »}
**Du neuf sur ce que vous surveillez** : {une ou deux lignes avec les URL, ou rien}

**Ce qui reste à faire**
1. {tâche} : {d'où elle vient}
2. ...

**Par quoi je commencerais** : {une seule proposition, la plus utile, en une phrase}
```

🔴 **Chaque tâche dit d'où elle vient.** « Reprendre la page tarifs : vous l'aviez notée le 3
septembre », « Finir l'export : il y a un TODO ligne 44 de `export.py` ». Une tâche sans origine
est une tâche que tu as inventée, et personne n'a moyen de s'en rendre compte. Rien trouvé ? la
liste est vide et tu le dis : c'est une information, pas un échec.

**Termine en mettant `STATUS.md` à jour.** Ajoute ce que tu as trouvé, remonte dans « Fait » ce qui
est visiblement terminé. 🔴 **Additif** : ce qui a été tapé à la main reste tel quel, mot pour mot.

### Étape 5. Le ton, et ce qui est interdit

- **« Vous », toujours.** Chaleureux, direct, jamais professoral.
- **Court.** Le point qu'on ne lit pas ne sert à rien. Au-delà d'une vingtaine de lignes, coupe.
- 🔴 **Ne prétends jamais avoir lu un fichier que tu n'as pas ouvert**, ni avoir cherché sur le web
  si tu ne l'as pas fait. Dis « je n'ai pas pu lire X ».
- 🔴 **Ne romance pas l'avancement.** « Le projet avance bien » ne veut rien dire. « Trois commits
  la semaine dernière, rien depuis jeudi » veut dire quelque chose.
- **Si le projet a beaucoup changé** depuis l'écriture du `CLAUDE.md` (des dossiers entiers
  apparus, une technique remplacée), dis-le en une ligne et propose de refaire le tour.

---

## Reconfigurer, ou tout oublier

- **Changer quelque chose** : ouvrez `CLAUDE.md` ou `STATUS.md`, ce sont des fichiers texte
  normaux. Ou dites « refais le tour » et le skill reprend depuis l'audit.
- **Tout oublier** : supprimez le bloc « Au démarrage » de votre `CLAUDE.md`, et `STATUS.md` si
  vous n'en voulez plus. Ce skill n'écrit nulle part ailleurs.
- **Un socle par projet** : les deux fichiers vivent dans le projet, pas dans le skill. Rien ne
  déborde d'un dossier sur l'autre, et si le projet est sur git, le socle suit le dépôt et sert à
  toute l'équipe.

## Handoff

Le skill laisse derrière lui un `STATUS.md` à jour et une proposition de prochaine action.

**Prochaine étape** : attaquez la tâche proposée, ou dites « non, plutôt {autre chose} ». Le point
n'est pas un ordre de mission.
