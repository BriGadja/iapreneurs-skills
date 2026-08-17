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

Une question à la fois, en sautant celles auxquelles son profil ou sa demande répond déjà :
1. **La tâche** : qu'est-ce qui entre, qu'est-ce qui doit sortir ? Exige un exemple CONCRET,
   une vraie entrée et la sortie rêvée. Sans exemple, tu construis à l'aveugle.
2. **Les déclencheurs** : les 3 à 5 phrases qu'il dirait naturellement pour lancer ça.
3. **La fréquence** : chaque jour, chaque semaine, avant chaque rendez-vous ?
4. **Ce qui doit être EXACT** : calculs, montants, comptages, dates, formats de fichier ?
5. **Les dépendances acceptées** : outils déjà installés, binaires à installer, ou zéro ?
6. **Ce que le skill doit retenir de lui** d'une fois sur l'autre.
7. **Le livrable** : une réponse dans la conversation, un fichier, les deux ?

Si ses réponses décrivent deux tâches distinctes, dis-le et propose de découper. Un skill fait
une chose.

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

Compile A, B et C en un brief complet. `skill-creator` installé, invoque-le avec ce brief ;
sinon construis toi-même à partir du même brief. Dans les deux cas, le résultat doit obtenir :

- **Une seule tâche.**
- **Un déclenchement qui ne demande aucun effort** : ce qui annonce quand l'utiliser doit
  contenir SES formulations de l'étape B, être impératif, et couvrir le cas où il n'emploie
  pas le mot évident.
- **L'exactitude hors du modèle** : tout ce qui relève de l'étape B.4 passe par du code que le
  skill appelle, et le skill s'interdit noir sur blanc de refaire ce calcul lui-même. Choisis
  le langage adapté à sa machine, ne le lui demande pas.
- **Un échec propre** : ce code refuse de produire quoi que ce soit tant qu'une donnée
  obligatoire manque, et liste TOUT ce qui cloche d'un coup, dans sa langue.
- **Aucune dépendance surprise** : si le skill a besoin d'un outil externe, il vérifie sa
  présence avant de s'en servir et dit comment l'installer.
- **Une mémoire lisible** : ce qu'il retient (étape B.6) tient dans un seul fichier que le
  membre peut ouvrir, corriger et supprimer. Minimum au premier usage, une question à la fois.
- **Un réglage de modèle si la version le permet** : tâche courte et répétitive, réglage
  économe ; analyse exigeante, réglage plus fort ; sinon laisse hériter de la session.
- **Une sortie qui dit la suite** : le skill se termine en indiquant ce qu'on peut faire après.

### Étape E. Prouve-le, ne l'annonce pas

Un skill n'est pas prêt parce qu'il est écrit. Lance **trois** tests réels et montre la sortie
brute de chacun. Jamais « ça devrait marcher ».

1. **Le cas normal** : une vraie donnée de son métier, du début à la fin.
2. **L'entrée invalide** : incomplète ou mal formée. Le skill doit échouer proprement et lister
   ce qui manque, pas afficher une trace technique.
3. **Le cas limite** : la valeur nulle, la quantité décimale, la liste vide, le mois de février,
   la collision. **C'est ce test qui trouve les vrais bugs, pas le premier.**

Puis **prouve le déterminisme** : rejoue le cas normal et vérifie que la sortie est
rigoureusement identique. Si elle diffère, soit tu supprimes la source de variation, soit tu
rends la sortie rejouable en affichant les valeurs à réinjecter pour reproduire à l'identique.

Un test échoue, tu corriges et tu **rejoues les trois**.

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
