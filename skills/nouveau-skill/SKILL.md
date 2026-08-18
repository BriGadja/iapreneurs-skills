---
name: nouveau-skill
description: "Utilise CE skill DÈS QUE l'utilisateur veut fabriquer un skill Claude Code : il dit « je veux créer un skill », « fais-moi un skill qui… », « j'aimerais automatiser cette tâche que je répète », « transforme ça en commande », ou décrit une tâche qu'il refait chaque semaine à la main, même sans prononcer le mot skill. Interviewe-le une question à la fois, regarde ce qui existe déjà, construit le skill (via skill-creator s'il est installé, seul sinon), puis le PROUVE par trois tests réels avant de le déclarer prêt. Retient son métier et son niveau pour adapter chaque skill suivant."
when_to_use: >-
  Une tâche répétitive que l'utilisateur décrit avec ses mots et voudrait déclencher d'une
  phrase. Aussi : créer une commande, fabriquer un outil sur mesure, industrialiser un
  processus manuel, forker un skill existant pour son métier. Ne pas utiliser pour exécuter
  une tâche ponctuelle, ni pour modifier un skill déjà installé.
allowed-tools: Read, Write, WebFetch, Bash, AskUserQuestion
---

# /nouveau-skill : votre skill, construit et prouvé

## Pour quoi faire

**Entrée** : une tâche que vous refaites à la main, décrite avec vos mots.
**Sortie** : un skill installé, testé devant vous, et que vous savez relire.

Ce skill ne vous demande pas de savoir écrire un skill. Il vous interviewe, il construit, et
surtout **il prouve que ça marche** avant de vous dire que c'est prêt.

**Aucune dépendance à installer.** Si `skill-creator` (le skill officiel Anthropic) est présent,
il s'en sert ; sinon il construit lui-même, avec les mêmes exigences. La différence est
invisible pour vous.

## Comment procéder

> *(Instructions pour toi, le skill. « Tu » = toi qui exécutes. « Vous » = le membre.)*
>
> **Cadre général** : ce qui suit décrit ce que le résultat doit OBTENIR, jamais la façon de
> l'écrire. Traduis chaque exigence dans les conventions en vigueur de la version de Claude
> Code installée ici, et va lire la documentation officielle si tu as un doute sur un format
> ou sur les champs de frontmatter disponibles. Ne recopie aucun gabarit de mémoire.

### Étape 0. Repère si skill-creator est là (jamais bloquant)

```bash
command -v claude >/dev/null 2>&1 || true   # informatif, n'arrête jamais le skill
[ -d "$HOME/.claude/skills/skill-creator" ] \
  && echo "ℹ️  skill-creator détecté : il sera utilisé à l'étape D." \
  || echo "ℹ️  skill-creator absent : construction directe, mêmes exigences."
exit 0
```

Quel que soit le résultat, tu continues. Cette étape ne sert qu'à savoir quel chemin prendre
à l'étape D, jamais à refuser de travailler.

### Étape A. Apprends qui est le membre (une seule fois)

Lis `~/.claude/mon-profil.json`. S'il n'existe pas, crée-le en posant ces questions **une à la
fois**, jamais en formulaire :
- son métier et à qui il vend ;
- les outils de son quotidien ;
- son niveau technique (débutant, à l'aise, développeur) ;
- sa langue de travail et le ton qu'il préfère.

Ce profil sert à ADAPTER chaque skill : exemples tirés de son métier, vocabulaire de ses
clients, niveau d'explication ajusté. Tiens-le à jour au fil des créations. S'il demande
« oublie mon profil », supprime le fichier et dis-le.

### Étape B. Interviewe-le sur CE skill

**Commence par ce que tu sais déjà.** Si la conversation en cours contient le travail qu'il veut
transformer en skill (« fais-en un skill », « je refais ça tout le temps »), c'est ta meilleure
source : relis-la et extrais-en les outils employés, l'ordre des étapes, les formats d'entrée et
de sortie observés, et surtout **les corrections qu'il t'a faites en route**, qui disent ce qui
compte pour lui. Restitue-lui ce que tu en as tiré et fais-le confirmer. Ne repose jamais une
question dont la réponse est déjà sous tes yeux : c'est le meilleur moyen de perdre sa confiance
avant d'avoir commencé.

Complète ensuite, **une question à la fois**, jamais en formulaire, en sautant celles auxquelles
son profil ou sa demande répond déjà :

1. **La tâche** : qu'est-ce qui entre, qu'est-ce qui doit sortir ? Exige un exemple CONCRET, une
   vraie entrée et la sortie rêvée. Sans exemple, tu construis à l'aveugle.
2. **Le déclenchement** : les 3 à 5 phrases qu'il dirait naturellement pour lancer ça. Prends ses
   mots à lui, pas les tiens : c'est ce qui décidera si le skill part ou reste muet.
3. **La forme de la sortie** : à quoi ressemble le résultat quand il est parfait ? Une réponse
   dans la conversation, un fichier, les deux ? Une structure imposée, ou libre ?
4. **Ce qui doit être EXACT** : calculs, montants, comptages, dates, formats de fichier ?
5. **Ce qui casse en vrai** : demande-lui les cas tordus qu'il a déjà rencontrés, les entrées
   incomplètes, les exceptions de son métier. Ce sont eux qui décideront de la qualité du skill,
   pas le cas nominal.
6. **La fréquence** : chaque jour, chaque semaine, avant chaque rendez-vous ?
7. **Les dépendances acceptées** : outils déjà installés, binaires à installer, ou zéro ?
8. **Ce que le skill doit retenir de lui** d'une fois sur l'autre.

**Ne t'arrête pas à ses réponses littérales : cherche la raison derrière la demande.** Quelqu'un
qui demande « un skill qui met en forme mes comptes rendus » veut peut-être surtout ne plus les
oublier. Reformule ce que tu as compris de son besoin réel, en une phrase, et fais-le valider
avant d'écrire quoi que ce soit. Un skill construit sur la demande de surface fait ce qu'on a
dit, et pas ce qu'on voulait.

Deux verdicts à poser à la fin de l'interview, à voix haute :

- **Est-ce une tâche ou deux ?** Si ses réponses en décrivent deux, dis-le et propose de découper.
  Un skill fait une chose.
- **Sa sortie est-elle vérifiable objectivement** (un fichier, des chiffres, une transformation)
  **ou subjective** (un ton, un style, une critique) ? Le premier cas se teste par des assertions,
  le second se juge à l'œil. Ça décide de la forme des tests de l'étape E, dis-lui laquelle tu
  prévois.

### Étape C. Regarde ce qui existe avant d'inventer

Cherche un skill proche : le repo officiel `anthropics/skills` d'abord, puis les annuaires
communautaires.

**Règle anti-faux-vide, sans exception** : une recherche qui ne rend rien n'est PAS une preuve
qu'il n'existe rien. Avant de conclure « on part de zéro », tu dois avoir tenté au moins DEUX
formulations, dont une à deux mots-clés maximum, et être allé voir la page de catégorie
pertinente et non la seule page d'accueil. Dis explicitement ce que tu as essayé.

Restitue en trois lignes : ce que tu as trouvé, ce qui est réutilisable, ou pourquoi on part de
zéro. Juge un skill sur son contenu, jamais sur ses étoiles. Relis intégralement tout skill
téléchargé avant de l'installer.

### Étape D. Construis

**Avant d'écrire une ligne, lis `references/regles-de-construction.md`.** Ce fichier condense les
règles du `skill-creator` officiel d'Anthropic et de la documentation Claude Code : divulgation
progressive, anatomie du dossier, description qui déclenche vraiment, écriture du pourquoi plutôt
que d'interdictions, refus de surajuster aux exemples de test. Un skill construit sans ces règles
fonctionne le jour où on l'écrit et déçoit ensuite.

Compile A, B et C en un brief complet. `skill-creator` installé, invoque-le avec ce brief ; sinon
construis toi-même à partir du même brief. **Dans les deux cas, la barre est la même**, et c'est à
toi de la tenir : le résultat doit obtenir

- **Une seule tâche**, et la structure du dossier qui va avec (`scripts/`, `references/`,
  `assets/` seulement si le skill en a l'usage).
- **Une description qui déclenche** : elle porte tout le « quand s'en servir », contient SES
  formulations de l'étape B, et couvre le cas où il n'emploie pas le mot évident. Le vrai risque
  est qu'elle soit trop tiède, pas trop insistante.
- **Un corps court**, sous 500 lignes, avec ce qui ne sert qu'à un cas particulier déporté dans
  `references/` et un mot sur quand aller le lire.
- **L'exactitude hors du modèle** : tout ce qui relève de l'étape B.4 passe par du code que le
  skill appelle, et le skill s'interdit noir sur blanc de refaire ce calcul lui-même. Choisis le
  langage adapté à sa machine, ne le lui demande pas.
- **Un échec propre** : ce code refuse de produire quoi que ce soit tant qu'une donnée obligatoire
  manque, et liste TOUT ce qui cloche d'un coup, dans sa langue.
- **Aucune dépendance surprise** : si le skill a besoin d'un outil externe, il vérifie sa présence
  avant de s'en servir et dit comment l'installer.
- **Une mémoire lisible** : ce qu'il retient (étape B.8) tient dans un seul fichier que le membre
  peut ouvrir, corriger et supprimer. Minimum au premier usage, une question à la fois.
- **Un réglage de modèle si la version le permet** : tâche courte et répétitive, réglage économe ;
  analyse exigeante, réglage plus fort ; sinon laisse hériter de la session.
- **Une sortie qui dit la suite** : le skill se termine en indiquant ce qu'on peut faire après.

Écris un premier jet, puis relis-le à froid comme si tu ne l'avais pas écrit, et coupe ce qui ne
porte pas son poids. C'est la relecture qui fait la différence, pas le premier jet.

### Étape E. Prouve-le, ne l'annonce pas

Un skill n'est pas prêt parce qu'il est écrit. Deux choses se prouvent, et elles sont
indépendantes : **qu'il parte quand il faut**, et **qu'il fasse ce qu'il doit**. Un skill parfait
qui ne se déclenche jamais est un skill mort ; un skill qui part toujours et se trompe est pire.

**E1. Le déclenchement.** Reprends les phrases de l'étape B.2, celles que le membre dirait
vraiment, et montre-lui ce que tu comptes essayer avant de le faire : « voilà les trois phrases sur
lesquelles je vais tester, elles vous ressemblent ? » Puis vérifie pour chacune que le skill part.
S'il reste muet sur une formulation naturelle, ce n'est pas la faute du membre : c'est la
description qu'il faut élargir, pas sa façon de parler. Deux nuances à connaître avant de conclure
à une panne : Claude ne consulte pas de skill pour une demande qu'il traite trivialement lui-même,
et il a une tendance générale à sous-déclencher, donc une description tiède est le premier suspect.

**E2. L'exécution.** Lance **trois** tests réels et montre la sortie brute de chacun. Jamais « ça
devrait marcher ».

1. **Le cas normal** : une vraie donnée de son métier, du début à la fin.
2. **L'entrée invalide** : incomplète ou mal formée. Le skill doit échouer proprement et lister
   ce qui manque, pas afficher une trace technique.
3. **Le cas limite** : la valeur nulle, la quantité décimale, la liste vide, le mois de février,
   la collision. **C'est ce test qui trouve les vrais bugs, pas le premier.**

Puis **prouve le déterminisme** : rejoue le cas normal et vérifie que la sortie est
rigoureusement identique. Si elle diffère, soit tu supprimes la source de variation, soit tu
rends la sortie rejouable en affichant les valeurs à réinjecter pour reproduire à l'identique.

Un test échoue, tu corriges et tu **rejoues les trois**.

Quand tu corriges, corrige la cause, pas l'exemple. Ajouter une règle qui traite le cas précis qui
vient d'échouer donne un skill qui passe tes trois tests et rate le quatrième, que le membre
rencontrera seul, sans toi. Et si les trois tests t'ont vu réécrire trois fois le même bout de
code, c'est qu'il manque un script dans `scripts/` : écris-le une fois, le skill l'appellera.

### Étape F. Installe et explique

Dis où placer le dossier, quelle phrase taper pour déclencher la première fois, et **relis le
skill avec lui, section par section**, à son niveau (profil, étape A). Il doit repartir capable
de le modifier seul. C'est le seul critère qui compte : un skill qu'on ne sait pas relire est
un outil qu'on subit.

## Ce que ce skill ne fait pas

Il ne modifie pas un skill déjà installé, il n'en publie aucun, et il ne va pas chercher vos
identifiants. Il construit, il teste, il explique.

## Handoff

Vous repartez avec le dossier du skill, son profil dans `~/.claude/mon-profil.json`, et la
sortie des trois tests sous les yeux.

**Prochaine étape** : utilisez votre skill sur un vrai cas dès aujourd'hui. Si une phrase ne
le déclenche pas, relancez `/nouveau-skill` et dites-la : c'est la description qu'il faut
corriger, pas votre façon de parler.
