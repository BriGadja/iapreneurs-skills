---
name: automatise
description: "Utilise CE skill DÈS QUE l'utilisateur veut qu'une tâche se fasse toute seule, à heure fixe ou à intervalle régulier : il dit « tous les matins », « chaque lundi », « automatise ça », « préviens-moi quand », « cron », « routine », « tâche planifiée », ou décrit un geste qu'il refait chaque semaine à la main, même sans demande explicite. Lancé sans argument, il lit le dossier et propose trois tâches tirées de son contenu. Il choisit où la faire tourner, fait un premier passage devant l'utilisateur, puis la programme et la note dans un carnet avec la façon de l'arrêter."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# /automatise : une tâche qui se fait sans vous

## Pour quoi faire

**Entrée** : une tâche que vous refaites à la main, ou rien du tout : le skill lit votre dossier
et vous en propose trois.
**Sortie** : la tâche programmée au bon endroit, un premier résultat sous vos yeux tout de suite,
et une ligne dans votre carnet `mes-taches.md` qui dit où elle tourne et comment l'arrêter.

Claude Code sait faire tourner une tâche sans vous de plusieurs façons : sur les serveurs
d'Anthropic, dans l'application Claude Desktop, sur un serveur à vous, ou sans Claude du tout. La
bonne dépend de la tâche bien plus que de votre machine, et la question que tout le monde oublie
est la première : **est-ce que cette tâche a besoin de réfléchir ?** Une vérification qui ne
réfléchit pas tourne en simple script, gratuitement, pour toujours.

## Aucune dépendance

Rien à installer pour lancer le skill. Il regarde ce qu'il y a sur votre machine et vous dit ce
qui manque pour la solution choisie, s'il manque quelque chose.

---

## Comment procéder

> *(Instructions pour toi, le skill. Ici « tu » = toi qui exécutes ; « vous » = la personne.)*
>
> 🔴 **Ce fichier dit ce que tu dois obtenir, pas comment t'y prendre.** Tu as sous les yeux la
> machine, le dossier et la version de Claude Code de cette personne ; ce fichier n'a rien de tout
> ça. Les façons de planifier une tâche changent vite : en cas de doute, lis la documentation
> officielle plutôt que ta mémoire. Le comparatif des trois modes de Claude Code est sur
> https://code.claude.com/docs/en/scheduled-tasks. À côté de ce fichier : le détail de chaque
> solution et ses pièges dans `references/voies.md`, et deux modèles à remplir dans `modeles/`
> (`consigne.md` pour la consigne de toute tâche, `lanceur.sh` pour un serveur Linux). Les lignes
> marquées 🔴 ne se négocient pas.

### Étape 0. Le carnet

Regarde si `${CLAUDE_SKILL_DIR}/mes-taches.md` existe.

- **Il existe** : résume en trois lignes au plus les tâches qu'il liste (nom, où elle tourne,
  quand). Pour chacune que tu peux vérifier depuis cette machine, regarde qu'elle existe encore
  là où le carnet le dit, et signale tout écart (« le carnet la donne active, je ne la trouve
  plus »). Puis demande : une nouvelle tâche, ou en modifier, mettre en pause ou arrêter une ?
  Pour arrêter, fais le geste écrit dans le carnet après accord, **vérifie que c'est arrêté**,
  puis mets le carnet à jour.
- **Il n'existe pas** : passe à l'étape 1.

### Étape 1. Trouver la tâche

**La personne a déjà décrit une tâche** (en argument ou plus haut dans la conversation) :
reformule-la en une phrase, fais-la confirmer, passe à l'étape 2.

**Sinon, lis le dossier avant de poser la moindre question** : `CLAUDE.md`, `README`, fichier de
suivi (`STATUS.md`, liste de tâches, backlog), arborescence, derniers commits s'il y a un dépôt
git, nature des fichiers. Puis propose **trois tâches tirées de CE dossier**, chacune en deux
lignes : ce qu'elle ferait et quand, ce que la personne recevrait, et **l'indice qui l'a
inspirée** (« vous avez un `STATUS.md` : chaque lundi à 8 h, le point de ce qui traîne »).
Quelques correspondances, à adapter, jamais à plaquer :

- un fichier de suivi → le point du lundi matin, ce qui est en retard en premier ;
- un site, une adresse en ligne → vérifier chaque matin qu'il répond, ne prévenir que s'il ne
  répond pas ;
- des devis ou des propositions → ceux restés sans réponse depuis sept jours, avec le brouillon
  de relance (que la personne envoie elle-même) ;
- des notes de réunion, de chantier, de visite → le récapitulatif de la semaine le vendredi ;
- des sources suivies, une veille → les nouveautés de ces sources une fois par semaine ;
- des exports, des tableaux qui grossissent → une copie datée chaque nuit.

🔴 **Ne propose rien qui ne s'appuie sur ce que tu as vu.** Un dossier vide ou sans indice se dit
tel quel : demande en une question ce que fait la personne et ce qu'elle refait chaque semaine à
la main, puis propose. Ne suppose aucun métier.

Une fois la tâche choisie, précise en une seule fois ce qui manque encore : **quand** (jour,
heure, fuseau) et **ce que « réussi » veut dire** pour elle.

### Étape 2. Choisir où elle tourne

Deux questions, dans cet ordre, puis une troisième si la tâche doit tourner sur l'ordinateur de la
personne. Pour les deux premières, réponds toi-même quand la tâche rend la réponse évidente, et
annonce ta réponse en une phrase pour qu'elle puisse la corriger.

**Question 1 : la tâche doit-elle réfléchir à chaque passage ?** (lire et résumer, trier,
rédiger, juger)

- **Non** (télécharger, copier, sauvegarder, compter, vérifier qu'une page répond) → **un script,
  sans Claude.** Tu l'écris une fois, le planificateur de la machine le lance. Il ne consomme rien
  du forfait Claude et ne dépend d'aucun service. Si la personne utilise déjà un outil
  d'automatisation (n8n, Make, Zapier), un scénario planifié dans cet outil est une option de
  même nature : propose-la.
  🔴 **C'est la réponse par défaut dès qu'elle est possible** : la plus fiable, et la seule
  gratuite.
- **Oui** → question 2.

**Question 2 : la tâche a-t-elle besoin de fichiers qui ne sont que sur cette machine ?**

- **Non** (elle lit le web, une boîte mail ou un outil par un connecteur, ou un dépôt GitHub) →
  **une routine cloud** : elle tourne sur les serveurs d'Anthropic, ordinateur éteint.
- **Oui**, sur **un ordinateur de bureau ou portable** → **une tâche planifiée de l'application
  Claude Desktop** : elle tourne si l'application est ouverte et l'ordinateur éveillé.
- **Oui**, sur **un serveur toujours allumé** → **le planificateur du serveur qui lance Claude
  Code sans fenêtre** (`claude -p`) : le plus robuste, et le plus de réglages.

**Question 3, dès que la solution retenue tourne sur l'ordinateur de la personne** (un script
lancé par son PC ou son Mac, une tâche Desktop) : **« Elle ne tournera pas quand votre ordinateur
est éteint ou en veille. Ça vous va ? »** Pose-la telle quelle et attends la réponse : c'est un
choix, pas une limite à signaler en passant.

- **Oui** → on garde.
- **Non** → propose ce qui tourne ordinateur éteint, et dis ce que chaque option coûte :
  - un outil d'automatisation qu'elle utilise déjà (n8n, Make, Zapier) ou un serveur toujours
    allumé, pour un script : rien de plus à payer ;
  - **une routine cloud**, si la tâche n'a pas besoin des fichiers de cette machine, même quand
    elle ne réfléchit pas : elle se crée depuis Claude Code avec `/schedule` quand la session est
    connectée avec un abonnement. En échange, chaque passage consomme son forfait, et il faut un
    dépôt GitHub ainsi que, pour joindre un site, l'ajouter aux domaines autorisés de la routine ;
  - si la tâche a besoin des fichiers de cette machine : seulement un serveur, ou des fichiers
    déplacés dans un dépôt GitHub que la routine clone.

Les conditions et les pièges de chaque solution sont dans `references/voies.md` : **lis la
section de la solution retenue avant d'aller plus loin**, et dis à la personne, en une ou deux
lignes, la limite qui la concerne (« elle ne tournera pas si votre ordinateur est en veille à
8 h », « il faut un dépôt GitHub »).

🔴 **Jamais `/loop` ni une tâche de session pour un besoin durable** : elles s'arrêtent avec la
session et expirent au bout de sept jours. Elles servent seulement à « surveille ça pendant que je
travaille ».

### Étape 3. Regarder la machine

Seulement ce dont la solution retenue a besoin, en constatant, jamais en devinant :

- **toujours** : le système (Windows, Mac, Linux) et les indices d'un serveur distant (connexion
  SSH, pas d'écran, Linux sans bureau). Fais confirmer en une phrase ;
- **script** : quel planificateur répond ici, quel langage est déjà installé. N'installe pas un
  langage pour l'occasion quand un autre est déjà là ;
- **routine cloud** : le dossier est-il relié à un dépôt GitHub ? La session est-elle connectée
  avec un compte claude.ai ? 🔴 Si une variable `ANTHROPIC_API_KEY` existe, dis-le (elle cache
  `/schedule`) **sans jamais afficher sa valeur** ;
- **tâche Desktop** : cette session tourne-t-elle dans l'application Desktop, et as-tu un outil
  pour créer une tâche planifiée ? Sinon, tu prépares tout et tu donnes les clics ;
- **serveur** : où est `claude` (son chemin absolu), avec quoi il est connecté
  (`claude auth status --text`), et comment cette connexion tiendra sans personne devant ?

Dis franchement ce que tu ne peux pas vérifier d'ici. **C'est toi qui raisonnes** : tu connais
cette machine et ce fichier ne la connaît pas. Propose le chemin qui lui convient, demande
confirmation, **n'installe et ne modifie rien sans accord**.

### Étape 4. Où arrive le résultat

🔴 **Une tâche dont personne ne voit le résultat ne sert à rien.** Demande où la personne veut le
voir, en ne proposant que ce qui marche avec la solution retenue : la notification de
l'application Desktop, un mail ou un message par un connecteur, un fichier daté dans le dossier
(seulement si elle l'ouvre vraiment). Pour une surveillance, le bon réglage est souvent **rien
quand tout va bien, un message quand ça casse**.

### Étape 5. Écrire la consigne de la tâche

La tâche tournera sans personne et sans cette conversation : sa consigne (ou son script) doit se
suffire à elle-même. Pars de `${CLAUDE_SKILL_DIR}/modeles/consigne.md` et remplis chaque section :
ce qu'elle lit, ce qu'elle produit, où elle le dépose, ce que « réussi » veut dire, et quoi faire
quand une source ne répond pas : **le dire dans le résultat, jamais inventer pour combler**. Pour
un script sans Claude, les mêmes questions valent, et la réponse est dans le code.

- 🔴 **La tâche prépare, la personne envoie.** Rien ne part vers un tiers (mail à un client,
  publication, paiement, suppression) sans que la personne l'ait relu. Si elle le demande quand
  même, dis le risque en une phrase et fais-le-lui confirmer.
- 🔴 **Le minimum d'accès** : seulement les connecteurs, dossiers et outils dont la tâche a besoin.
  Une tâche sans surveillance fait tout ce qu'on lui permet.
- 🔴 **Aucun secret dans la consigne** : ni mot de passe, ni clé. Ils vont dans les variables
  d'environnement ou le coffre de la plateforme, et la consigne les nomme sans les contenir.
- **Le coût** : chaque passage où Claude réfléchit consomme le forfait de la personne. Propose la
  fréquence la plus basse qui rend le service (toutes les heures, c'est vingt-quatre sessions par
  jour) et un modèle plus léger quand la tâche est simple.

Montre le tout en six lignes au plus (la consigne résumée, quand, où elle tourne, où arrive le
résultat, ce qu'elle a le droit de toucher, le coût), et attends son accord.

### Étape 6. Un premier passage, devant la personne

🔴 **Avant de programmer quoi que ce soit, lance la tâche une fois, maintenant, et lisez le
résultat ensemble.** Un statut « terminé » ne prouve rien : la documentation des routines le dit
elle-même, le vert signifie seulement que la session a démarré et s'est arrêtée. Ce qui prouve,
c'est le résultat arrivé là où la personne a dit qu'elle le verrait.

Corrige et relance jusqu'à ce que ce soit juste. Au bout de trois essais qui échouent, arrête-toi,
dis ce qui bloque, et propose une autre solution de l'étape 2.

### Étape 7. Programmer, vérifier, noter

1. **Programme la tâche**, après son accord.
2. **Vérifie qu'elle est programmée en la relisant là où elle vit** (la table du planificateur,
   la liste des routines, le détail de la tâche Desktop). 🔴 Pas de mémoire : tu ne l'annonces
   programmée que si tu l'as vue programmée. Donne à la personne ses **trois prochaines
   exécutions**, en heure locale : c'est là qu'on attrape un fuseau ou un jour de travers.
3. **Note-la dans le carnet** `${CLAUDE_SKILL_DIR}/mes-taches.md` (crée-le s'il n'existe pas,
   avec le titre `# Mes tâches automatiques`), un bloc par tâche :

```
## {nom court}
- **Ce qu'elle fait** : {une phrase}
- **Quand** : {jours et heure, avec le fuseau}
- **Où elle tourne** : {routine cloud / tâche Desktop / planificateur de {machine} / scénario {outil}}
- **Où arrive le résultat** : {…}
- **Ce qu'elle a le droit de toucher** : {dossiers, connecteurs, outils}
- **Comment l'arrêter** : {le geste exact : la commande, ou le chemin de clics}
- **Créée le** : {AAAA-MM-JJ}
- **À renouveler** : {seulement si quelque chose expire, ex. « jeton du serveur, expire le AAAA-MM-JJ »}
```

🔴 **La ligne « Comment l'arrêter » est obligatoire et exacte.** Une tâche qu'on ne sait plus
arrêter tourne pour rien, consomme pour rien, et finit par surprendre.

## Le ton, et ce qui est interdit

- **« Vous », toujours.** Court, direct. Chaque terme technique s'explique entre parenthèses la
  première fois : « cron (le planificateur intégré à Linux et au Mac) », « routine (une tâche que
  Claude exécute sur les serveurs d'Anthropic) ».
- 🔴 **Ne suppose aucun métier.** Les propositions viennent du dossier ou de ce que la personne a
  dit.
- 🔴 **Rien ne s'installe, ne se programme, ne s'arrête sans accord.**
- 🔴 **N'affiche jamais la valeur d'un secret**, même pour vérifier qu'il existe.

---

## Désinstaller, ou tout oublier

- **Arrêter une tâche** : relancez `/automatise`, ou faites le geste noté dans le carnet.
- **Désinstaller le skill** : supprimez son dossier. 🔴 **Les tâches programmées continuent de
  tourner** : elles vivent dans le planificateur, l'application ou votre compte, pas dans le
  skill. Arrêtez-les d'abord, le carnet dit comment.

## Handoff

Le skill laisse derrière lui une tâche programmée, un premier résultat déjà lu, et sa ligne dans
le carnet.

**Prochaine étape** : à l'heure prévue, regardez le résultat arriver là où vous l'avez demandé.
Relancez `/automatise` pour voir vos tâches, en ajouter une ou en arrêter une.
