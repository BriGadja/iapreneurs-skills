---
name: close
description: "Le dernier geste d'une session Claude Code : à taper quand ce que vous aviez demandé est fait. Il relit la conversation, range ce qui mérite d'être gardé (mémoire, CLAUDE.md, fichier de suivi), committe le travail de la session s'il y a un dépôt git, et rend un récapitulatif court. Au premier lancement, il fait l'état de ce que Claude sait déjà de votre projet, vous interviewe sur votre façon de travailler, puis se réécrit à votre mesure et efface son interview. À lancer avec /close, sans argument, à la fin de chaque session."
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Bash(git *)
---

# /close : le dernier geste d'une session

## Pour quoi faire

**Entrée** : rien. Vous tapez `/close` quand ce que vous aviez demandé est fait.
**Sortie** : ce que la session a appris est rangé à sa place, le travail est committé s'il y a un
dépôt git, et un récapitulatif d'une dizaine de lignes vous dit ce qui a été fait, rangé, et ce
qui reste.

Claude fait exactement ce que vous lui demandez, et seulement ça. Retenir ce qu'il vient
d'apprendre, noter ce qui reste à faire, garder une trace de ce qui a changé : tout ça ne se fait
que si on le demande. `/close` le demande pour vous, à chaque fois, dans le même ordre : le vôtre.

C'est le pendant de `/prime` : `/prime` ouvre la session en chargeant ce qui a été rangé,
`/close` la ferme en rangeant ce qui a été appris. Il marche aussi très bien seul.

Au **premier** lancement, il ne ferme rien tout de suite : il regarde ce que Claude sait déjà de
votre projet, vous interviewe sur votre façon de travailler, puis **réécrit ce fichier à votre
mesure et en efface l'interview**. Ensuite, `/close` fait votre fermeture, pas la nôtre.

## Aucune dépendance

Rien à installer, aucune clé, aucun compte. Il se sert de `git` s'il y en a un, et s'en passe
sinon.

---

## Comment procéder

> *(Instructions pour toi, le skill. Ici « tu » = toi qui exécutes ; « vous » = la personne.)*
>
> 🔴 **Ce fichier dit ce que tu dois obtenir, pas comment t'y prendre.** Tu as sous les yeux la
> conversation, le dossier, la machine et la version de Claude Code de cette personne ; ce
> fichier n'a rien de tout ça. Traduis chaque exigence dans les conventions de la version
> installée ici, et va lire la documentation officielle en cas de doute
> (https://code.claude.com/docs/en/memory pour les instructions et la mémoire). Les lignes
> marquées 🔴 ne se négocient pas.

<!-- PREMIER LANCEMENT : DÉBUT. Tout ce qui se trouve entre ce repère et le repère FIN est
supprimé de ce fichier à la fin du premier lancement (étape B). -->

## Premier lancement

Cette section n'existe que jusqu'au premier lancement. **Si tu la lis, c'est le premier
lancement** : fais d'abord les deux vérifications de l'Étape 1 plus bas, puis les étapes A et B
ci-dessous, puis enchaîne sur la fermeture (Étape 2).

### A. L'état de la couche IA de ce projet

Avant toute question, regarde ce qui, aujourd'hui, permet à une nouvelle session de savoir chez
qui elle travaille. **Ne devine pas : ouvre.** Ce que tu dois pouvoir dire à la fin :

- **Les instructions** : quels fichiers d'instructions se chargent pour ce projet (le
  `CLAUDE.md` du projet, celui de l'utilisateur, des règles), et leur longueur. Au-delà d'environ
  200 lignes, la doc officielle dit que ça consomme du contexte et que l'adhésion baisse.
- **La mémoire** : la mémoire automatique de Claude Code est-elle active, et que contient-elle
  sur ce projet ?
- **Le suivi** : un fichier qui porte le reste à faire (`STATUS.md` si `/prime` est passé, une
  liste de tâches, rien).
- **L'historique** : un dépôt git ? Ses derniers messages de commit disent-ils *pourquoi*, ou
  seulement *quoi* ? Y a-t-il des modifications jamais committées ?
- **Les conversations** : Claude Code les garde sur la machine, puis les efface au bout d'une
  durée réglable (vérifie la valeur par défaut dans la doc officielle de cette version).
- **La sécurité** : des fichiers sensibles traînent-ils dans le dossier (mots de passe, clés,
  exports de clients) ? Sont-ils exclus de git, et protégés par une règle de refus de lecture ?
  🔴 Regarde leurs **noms**, n'ouvre jamais leur contenu.

Rends-le en une dizaine de lignes, sous la forme « ce qui existe / ce qui manque », puis au plus
**trois** suggestions tirées de CE projet, chacune avec sa raison. Jamais une liste de bonnes
pratiques génériques ; rien de solide, rien à proposer. Termine par « je me trompe quelque
part ? » et **attends la réponse**.

🔴 **Interdit : inventer.** Un dossier vide se décrit comme vide. Un état plausible mais faux est
pire qu'un état vide : il a l'air juste.

### B. L'interview, puis votre /close sur mesure

Pose ces questions **une à la fois**, jamais en formulaire, et saute celles auxquelles l'étape A,
le `CLAUDE.md` ou la conversation répondent déjà (annonce ce que tu sais et fais-le confirmer).
Propose des réponses possibles à chaque fois : c'est plus rapide qu'une page blanche.

1. **Son usage** : Claude Code sert-il à un projet précis (un site, une application, un
   document) ou à toute son activité ? La réponse change ce qui mérite d'être retenu.
2. **Ce qui mérite d'être gardé** d'une session à l'autre : des décisions, ses préférences, des
   faits sur ses clients ou ses dossiers, les erreurs corrigées, les chiffres de référence… Les
   corrections qu'elle te fait en cours de route sont souvent les plus précieuses.
3. **Le reste à faire** : dans quel fichier ? `STATUS.md` si `/prime` est installé, un autre
   fichier, ou nulle part.
4. **Git** (seulement s'il y a un dépôt) : committer sans demander, montrer puis committer après
   accord, ou ne jamais toucher à git. Et pousser vers le dépôt distant : oui ou non.
5. **La trace des conversations** : rien de plus, allonger la durée de conservation de Claude
   Code, ou tenir un journal (quelques lignes par session dans un fichier).
6. **Ses tâches à elle** : « à la fin de chaque session, je voudrais aussi que… ». Donne des
   exemples de métiers éloignés (mettre à jour la fiche du client concerné, préparer le mail de
   suivi, noter le temps passé, vérifier qu'un document de référence est toujours juste).
   « Rien » est une bonne réponse, et la section se remplira à l'usage.
7. **Son autonomie** : « faites, puis dites-moi » ou « proposez, et j'accepte ».

Puis écris sa méthode :

1. **Montre-lui la section « Votre méthode de fermeture » telle que tu vas l'écrire** : ses
   réponses, dans ses mots, en étapes numérotées et dans l'ordre où elles doivent se faire.
   Attends son accord.
2. **Réécris ton propre fichier**, `${CLAUDE_SKILL_DIR}/SKILL.md` :
   - remplis la section « Votre méthode de fermeture », à la place de la ligne
     `(vide pour l'instant)` ;
   - supprime tout ce qui se trouve entre le repère `PREMIER LANCEMENT : DÉBUT` et le repère
     `PREMIER LANCEMENT : FIN`, repères compris ;
   - ne touche à rien d'autre, en-tête compris.
   🔴 Vérifie ensuite, en relisant le fichier écrit : il commence par `---`, contient
   `name: close`, ne contient plus le mot `PREMIER LANCEMENT`, et sa section « Votre méthode de
   fermeture » ne contient plus la ligne `(vide pour l'instant)`. Si une vérification échoue, dis-le et ne prétends pas que c'est
   fait. Donne-lui le chemin exact du fichier.
3. **Propose (sans l'imposer) une ligne** pour le `CLAUDE.md` du projet, ou pour son `CLAUDE.md`
   personnel si elle a installé `/close` pour tous ses projets : « Quand ce que je t'ai demandé est
   terminé, propose-moi `/close` en une ligne. » Explique pourquoi : `/close` ne se lance jamais
   tout seul, exprès, parce qu'il peut committer ; cette ligne est ce qui fera que Claude le propose.
4. **Enchaîne tout de suite sur une vraie fermeture** (Étape 2), sur la conversation en cours :
   elle vient de tout paramétrer, elle doit voir ce que ça donne.

<!-- PREMIER LANCEMENT : FIN -->

### Étape 1. Savoir où on en est

1. **Projet du kit ?** Si le dossier contient un `PRD.md` à la racine **et** un `docs/plans/` ou
   `docs/specs/`, il a été monté avec le kit Claude Code des IAPreneurs, qui a **son propre
   `/close`** : il clôture une phase, met le PRD à jour et fait son propre tri de mémoire. Il est
   masqué parce qu'un skill installé pour tous les projets passe avant un skill de projet.
   Dis-le en une fois : pour lui rendre la main sur ce projet, il suffit d'installer celui-ci
   projet par projet plutôt que pour tous. Propose de continuer quand même pour cette fois, et
   ne repose pas la question dans la même session.
2. **La demande est-elle finie ?** Si la conversation montre un travail à moitié fait (une
   erreur non résolue, une modification commencée, une question restée sans réponse), dis-le en
   une phrase et demande : fermer quand même en le notant « en cours », ou finir d'abord.

### Étape 2. La fermeture

Fais-la dans l'ordre de **sa méthode** (section plus bas). Ce qui suit est ce que chaque
fermeture doit obtenir, quelle que soit la méthode.

**1. Relis toute la conversation**, pas seulement la fin : ce qui a été demandé, ce qui a été fait
(les fichiers touchés), ce qui a été décidé, ce qui a été appris, les corrections qu'elle t'a
faites, ce qui reste.

**2. Range chaque chose à sa place**, une seule destination par chose :

| Ce que la session a appris | Où ça va |
|---|---|
| Un fait sur la personne, un client, un dossier | la mémoire |
| Une règle qui change la façon de travailler sur ce projet | le `CLAUDE.md` (proposé) |
| Une tâche qui reste à faire | le fichier de suivi |
| La raison d'une modification | le message de commit |
| Une procédure refaite pour la troisième fois | une suggestion de skill |
| Une erreur qui ne doit jamais se reproduire | une suggestion de règle de permission |

« Rien à ranger » est un résultat valable : dis-le, ne remplis pas pour remplir.

- 🔴 **Avant d'écrire, vérifie que ce n'est pas déjà écrit.** Mets à jour plutôt que de dupliquer.
- 🔴 **Le `CLAUDE.md` se propose, il ne s'impose pas** : montre la modification en une à trois
  lignes et attends l'accord, même en mode « faites ». N'y mets jamais ce que Claude fait déjà
  bien tout seul (« sois rigoureux », « vérifie ton travail ») : ces lignes prennent de la place
  et diluent le reste. S'il approche des 200 lignes, propose en même temps quoi fusionner ou
  retirer.
- **La mémoire** : la mémoire automatique de Claude Code si elle est active, sinon l'endroit
  choisi dans sa méthode.
- **Le suivi** : 🔴 **additif**. Ce qui a été tapé à la main reste mot pour mot ; ce qui est fini
  passe dans « fait ».

**3. Git**, s'il y a un dépôt et selon sa méthode :

- 🔴 **Seulement les fichiers que CETTE session a modifiés**, listés avant le commit. Des
  modifications plus anciennes traînent ? Laisse-les et signale-les en une ligne.
- 🔴 **Jamais un fichier qui ressemble à un secret** (mots de passe, clés, `.env`, exports de
  clients). S'il en apparaît un, arrête-toi, dis-le, et propose de l'exclure de git et de le
  protéger par une règle de refus de lecture.
- Un message qui dit **quoi et pourquoi**.
- 🔴 **Jamais de push** si sa méthode ne le dit pas.

**4. Ses tâches à elle**, celles de sa méthode, dans son ordre. Si l'une est devenue impossible
(un fichier disparu), dis-le en une ligne plutôt que de la sauter en silence.

**5. Si ce projet n'a encore ni fichier d'instructions ni suivi** (un `/close` installé pour tous
les projets arrive un jour dans un dossier neuf), dis-le en une ligne et propose de les créer.

**6. Le récapitulatif**, dans cet esprit, une douzaine de lignes au plus :

```
## Session fermée

**Demandé** : {en une phrase}
**Fait** : {ce qui a vraiment été fait}
**Rangé** : {chaque chose, avec le chemin exact du fichier où elle est allée}
**Proposé, en attente de votre accord** : {ou rien}
**Commit** : {identifiant et message, ou « rien à committer », ou « non, comme convenu »}
**Reste à faire** : {chaque tâche avec d'où elle vient}
**À la prochaine session** : {une phrase}
```

🔴 **N'annonce rien que tu n'as pas écrit.** Chaque ligne « Rangé » renvoie à un fichier que tu
as vraiment modifié. Une trace annoncée et absente est pire qu'une trace manquante : on s'y fie.

**7. Au plus une suggestion** pour la suite, et seulement si elle est solide : une procédure
refaite pour la troisième fois qui mériterait un skill, une erreur qui mériterait une règle de
refus. Rien de solide, rien.

## Votre méthode de fermeture

_Écrite avec vous au premier lancement. Tout ce qui est écrit ici, `/close` le fait à chaque
fois, dans cet ordre. Vous pouvez la modifier à la main quand vous voulez : c'est du français
dans un fichier texte._

(vide pour l'instant)

## Le ton, et ce qui est interdit

- **« Vous », toujours.** Court, direct, jamais professoral.
- 🔴 **Ne range que ce qui a été dit ou fait dans la conversation.** Une décision que personne n'a
  prise ne s'écrit nulle part.
- 🔴 **N'ouvre jamais un fichier sensible pour « vérifier »** ce qu'il contient : son nom suffit.
- 🔴 **En mode « proposez », rien ne s'écrit sans accord.** En mode « faites », tout s'écrit sauf
  le `CLAUDE.md`, qui se propose toujours.

---

## Reconfigurer, ou tout oublier

- **Changer votre méthode** : ouvrez ce fichier et modifiez la section « Votre méthode de
  fermeture ». Ou dites à Claude « ajoute à ma méthode de fermeture : … ».
- **Refaire l'interview** : réinstallez le skill avec le prompt de la tuile Circle, il revient
  dans son état d'origine.
- **Tout oublier** : supprimez le dossier du skill. Ce qu'il a rangé (mémoire, `CLAUDE.md`,
  fichier de suivi, commits) vous appartient et reste en place.

## Handoff

Le skill laisse derrière lui une session rangée et un récapitulatif.

**Prochaine étape** : fermez la conversation. La prochaine commence par `/prime`, si vous l'avez,
et repart de ce qui vient d'être rangé.
