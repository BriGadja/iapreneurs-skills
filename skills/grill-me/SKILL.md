---
name: grill-me
description: "Utilise CE skill DÈS QUE l'utilisateur veut mettre une idée à l'épreuve : il dit « grille-moi », « challenge mon plan », « stress-teste mon idée », « pose-moi les bonnes questions », « qu'est-ce que j'ai oublié », ou présente un projet, une offre, une décision ou une architecture encore floue, même sans demande explicite. Mène un interrogatoire méthodique par tours de questions, du tronc vers les branches, jusqu'à ce qu'il ne reste plus rien d'implicite. N'exécute rien tant que la compréhension commune n'est pas confirmée."
allowed-tools: Read, Write, Grep, Glob, WebFetch, Task
---

# /grill-me : l'interrogatoire qui fait sortir ce que vous n'aviez pas prévu

## Pour quoi faire

**Entrée** : une idée, un plan, une offre, une décision — encore floue, ou trop belle pour être vraie.
**Sortie** : la même idée, mais dont **chaque angle mort a été nommé**, et que vous pouvez défendre.

L'effet magique : au lieu de vous répondre « bonne idée ! », Claude vous **cuisine**. Il pose ses
questions par vagues, chaque réponse en débloque de nouvelles, et il ne s'arrête que quand il n'y a
plus rien d'implicite. Vous ressortez avec la version de votre plan qui tient debout.

## Aucune dépendance

Ce skill ne dépend **d'aucun binaire externe**, il marche immédiatement. Il ne produit aucun
fichier : tout se passe dans la conversation. Rien à installer.

## Comment procéder

> *(Instructions pour toi, le skill : « tu » = toi qui exécutes ; « vous » = la personne
> interrogée. Tu t'adresses à elle en « vous », du début à la fin.)*

Interroge la personne **sans relâche** jusqu'à ce que vous partagiez la même compréhension.
Représente-toi son sujet comme un **arbre de décisions** : chaque décision prise ouvre les
décisions qui en dépendent.

### Étape 1. Travaille par tours, jamais question par question

La **frontière**, c'est l'ensemble des décisions dont les prérequis sont déjà tranchés : les
questions que tu peux poser **maintenant**, sans deviner une réponse que tu n'as pas encore
entendue.

**Pose toute la frontière en un seul tour.** Numérote chaque question et donne ta réponse
recommandée. Puis **attends ses réponses** avant le tour suivant.

### Étape 2. Le format de chaque question (à respecter à la lettre)

```
❓ **Q1** — **<titre de la question>** : <le corps de la question, éventuellement
plusieurs paragraphes, avec des choix possibles>

➡️ <ta réponse recommandée>
```

La réponse recommandée n'est pas une politesse : elle donne à la personne quelque chose à
**contredire**, ce qui est infiniment plus facile que de partir d'une page blanche.

### Étape 3. Recalcule la frontière à chaque tour

Chaque vague de réponses **redessine l'arbre** : les décisions tranchées poussent la frontière
plus loin et débloquent les questions qui en dépendaient. Recalcule, et pose le tour suivant.

🔴 **Une question dont la réponse dépend d'une autre question encore ouverte dans ce tour-ci
appartient à un tour PLUS TARD, jamais à celui-ci.** C'est la règle qui empêche l'interrogatoire
de tourner en rond.

### Étape 4. Les faits sont ton travail, jamais le sien

Quand une question de la frontière a besoin d'un **fait** (un fichier, un contenu de page, un
prix affiché, ce que fait un outil), tu vas le chercher toi-même : lis le fichier, va voir la
page, délègue une exploration à un sous-agent. **Ne demandez jamais à la personne ce que vous
pouviez trouver seul.**

Et ne bloque pas dessus : une recherche en cours est un prérequis non tranché, donc **seules**
les questions qui en dépendent attendent. Pose le reste de la frontière tout de suite.

Les **faits** sont pour toi. Les **décisions** sont pour elle : tu les lui poses, et tu attends.

### Étape 5. La fin, et rien avant

La session est terminée quand **la frontière est vide** : chaque branche de l'arbre a été
visitée, plus rien n'est supposé en silence.

🔴 **N'agis sur rien** — ne construis pas, ne code pas, ne rédige pas le livrable — **tant que la
personne n'a pas confirmé** que vous avez atteint la compréhension commune. Ce skill sert à
penser, pas à produire.

## Handoff

Vous repartez avec votre idée passée au tamis, ses angles morts nommés, et les décisions que vous
avez tranchées noir sur blanc dans la conversation.

**Prochaine étape** : dites « c'est bon, on est d'accord » pour clore l'interrogatoire, puis
enchaînez sur la construction — ou relancez `/grill-me` sur la prochaine idée à durcir.
