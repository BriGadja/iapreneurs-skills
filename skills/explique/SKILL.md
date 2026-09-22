---
name: explique
description: "Utilise CE skill DÈS QUE l'utilisateur veut comprendre un concept : il dit « explique », « vulgarise », « c'est quoi », « comment marche », « je comprends rien à… », ou cite un sigle / une techno / un buzzword qu'il ne maîtrise pas, même sans demande explicite. Transforme n'importe quel concept (technique, IA, business) en une page d'explication limpide, publiée en artifact (une page web privée, avec un lien à partager), avec analogie du quotidien et exemple concret, dans le ton IAPreneurs."
allowed-tools: Read, Write, WebFetch, Artifact
---

# /explique : n'importe quel concept, vulgarisé façon IAPreneurs, sur une page qu'on partage

## Pour quoi faire

**Entrée** : un concept. Un mot, un sigle, une techno, un buzzword (« webhook », « RAG », « MCP », « API REST », « token »…).
**Sortie** : **une page**, publiée en artifact, que **n'importe qui comprend en 30 secondes** : une phrase qui dit l'essentiel, une analogie du quotidien, le concept démonté, un exemple qu'on peut vivre, et ce que ça change pour vous. Dans le ton chaleureux et direct d'IAPreneurs.

L'effet magique : vous collez un mot que vous ne comprenez pas, vous ressortez avec une page claire, et un lien. Vous la relisez sur votre téléphone, vous l'envoyez à un client, à un associé, à la personne qui vous a posé la question.

## Aucune dépendance

Ce skill ne dépend **d'aucun binaire externe**, il marche immédiatement. Pour les concepts stables, il répond sans toucher au web. Le seul outil optionnel est `WebFetch`, utilisé uniquement si le concept est trop récent ou trop pointu pour être expliqué de mémoire (voir Étape 2).

La page est publiée avec l'outil **Artifact** de Claude Code : une page web hébergée sur claude.ai, **privée** tant que vous ne la partagez pas, avec un lien que vous choisissez ou non de diffuser. Il faut une session connectée à un compte claude.ai (Pro, Max, Team ou Entreprise). Si l'outil n'est pas disponible dans votre session, le skill vous le dit et écrit la page dans un fichier HTML à ouvrir dans votre navigateur (voir Étape 5).

## Comment procéder

> *(Instructions pour toi, le skill : le membre ne lit pas cette section. Ici « tu » = toi
> qui exécutes ; « vous » = le membre à qui s'adresse l'explication finale.)*

### Étape 1. Cerner le concept

Identifie **ce qu'on te demande d'expliquer** et à quel niveau. Un mot isolé (« webhook ») ?
Une comparaison (« la différence entre API et webhook ») ? Pose UNE question de cadrage seulement
si c'est vraiment ambigu (ex. « token » = jeton d'auth ou token LLM ?). Sinon, enchaîne.

### Étape 2. (optionnel) Vérifier si c'est récent ou pointu

Si le concept est très récent (un produit sorti il y a quelques mois), un sigle de niche, ou que
tu n'es pas sûr à 100 %, fais **un** `WebFetch` rapide pour te caler. **Sinon, ne fais aucun appel** :
l'explication d'un concept stable (« webhook », « base de données ») n'a pas besoin du web.
Ne jamais inventer : si tu ne sais pas et que le web ne répond pas, dis-le franchement.

### Étape 3. Rédiger selon le gabarit (à respecter au mot)

Écris d'abord le texte, dans **cet ordre exact**. C'est ce gabarit qui fait le style IAPreneurs,
et c'est lui qui devient la structure de la page :

1. **TL;DR en une phrase** : commence par « **En une phrase :** … ». Le lecteur pressé s'arrête là et a compris l'essentiel.
2. **L'analogie du quotidien**, « **Imaginez que** … » : une scène concrète tirée de la vraie vie
   (une sonnette, un serveur au restaurant, un facteur, un carnet d'adresses…). C'est le cœur de l'effet wow.
3. **Le concept démonté** : relie l'analogie au vrai truc, en vulgarisant **chaque terme technique
   entre parenthèses** : « le webhook (la sonnette) prévient ton appli (la maison) dès qu'un événement arrive (quelqu'un sonne) ».
4. **Un exemple concret « pour de vrai »**, un cas que le membre peut vivre dans son activité, quelle
   qu'elle soit : son propre agenda en ligne qui prévient son outil d'automatisation, son site qui
   envoie un mail, sa caisse qui met le stock à jour… Evergreen, pas de persona fictif suivi, et
   ne présume pas le métier de la personne qui lit : si la conversation dit ce qu'elle fait,
   prends un exemple chez elle ; sinon, un exemple que tout commerce ou toute activité peut vivre.
5. **Pourquoi ça compte pour vous** : une ou deux phrases « C'est-à-dire que… » qui font mesurer
   l'impact réel (« c'est-à-dire que vous n'avez plus besoin de vérifier à la main, ça vous prévient tout seul »).
6. **Une interjection rhétorique** pour clore avec connivence, et **varie** d'une fois sur l'autre :
   « Pas si sorcier, non ? », « Ça fait rêver non ? », « Et voilà », « Vous voyez l'idée ? », « Oui, juste ça. ».
   Ne ressors pas toujours la même.

### Étape 4. Relire le ton

Avant de mettre en page, vérifie :
- **« vous » informel**, chaleureux, jamais condescendant.
- Chaque jargon a sa **parenthèse de vulgarisation**.
- L'analogie est **concrète** (un objet/une scène du quotidien), pas une métaphore abstraite.
- Zéro persona fictif suivi (pas de « Marc le plombier »).
- Pas de pavé : aère, utilise des → bullets si ça aide, mais toujours **encadrés par ta voix**
  (une phrase d'intro avant, un commentaire après, jamais une liste nue). Réserve les bullets aux
  concepts qui ont des **parties énumérables** (« un webhook a 3 morceaux : → l'URL, → l'événement,
  → les données ») ; pour un concept simple, la prose suffit (comme l'exemple ci-dessous).

### Étape 5. Mettre en page et publier en artifact

🔴 **Le livrable est la page, pas un message dans la conversation.** Tu ne recopies pas
l'explication dans le terminal : tu la publies, et tu donnes le lien.

Construis **une seule page HTML autoportante** (styles et scripts inclus dans le fichier, rien à
charger d'ailleurs, pas de bibliothèque externe : l'explication n'en a pas besoin) et publie-la
avec l'outil **Artifact** de Claude Code. Le contrat de la page :

- **Le titre de la page, c'est le concept**, en deux à quatre mots (« Le webhook », « API et
  webhook », « Le RAG »). Pas de « Explication de… », pas de nom de skill.
- **La phrase « En une phrase » ouvre la page, en gros**, c'est la seule chose qu'un lecteur
  pressé lira. Puis les cinq autres blocs du gabarit, dans l'ordre, chacun avec son propre
  titre court (« Imaginez que… », « Ce qui se passe vraiment », « Pour de vrai », « Ce que ça
  change pour vous »), et la ligne de clôture seule, en bas.
- **Le texte reste exactement celui de l'Étape 3.** La mise en page sert le texte, elle ne le
  réécrit pas et n'y ajoute pas de sections.
- **Un seul visuel, et seulement s'il aide** : quand l'analogie se dessine (une sonnette et une
  maison, un serveur entre la salle et la cuisine), un schéma simple en SVG dans la page, légendé
  avec les mots de l'analogie ET les vrais termes en dessous, pour que le lecteur fasse le lien
  d'un coup d'œil. Un concept qui ne se dessine pas n'a pas de schéma : pas d'illustration
  décorative.
- **Lisible sur un téléphone** : c'est là que le lien sera ouvert la plupart du temps. Une seule
  colonne, texte large, marges, pas de défilement horizontal. Sobre et clair, en mode clair et en
  mode sombre : c'est une page de lecture, pas une plaquette.
- **Aucune mention de la Boîte à Skills, d'IAPreneurs ni de Claude** sur la page : elle
  appartient à la personne qui l'a demandée, qui l'enverra peut-être à un client.

Quand la page est publiée, ton message dans la conversation tient en trois lignes : le lien, la
phrase « En une phrase », et un rappel que la page est **privée** tant qu'elle n'est pas partagée
depuis son en-tête (bouton Partager). Rien d'autre : l'explication est sur la page.

**Si l'outil Artifact n'est pas disponible** dans la session (pas d'outil du nom d'Artifact, ou
une publication refusée), ne fais pas semblant et ne publie pas ailleurs : écris la même page dans
un fichier `explique-<concept>.html` dans le dossier courant, donne son chemin, et dis en une
phrase pourquoi il n'y a pas de lien (les artifacts demandent une session connectée à un compte
claude.ai Pro, Max, Team ou Entreprise ; une clé d'API ne suffit pas). Le membre ouvre le fichier
dans son navigateur et la page est la même.

## Exemple de sortie (référence de ton, c'est le texte de la page)

> **Le webhook**
>
> **En une phrase :** un webhook, c'est une sonnette que votre application installe chez un autre service pour être prévenue à la seconde où quelque chose se passe.
>
> **Imaginez que** vous attendez un colis. Sans webhook, vous descendez vérifier la boîte aux lettres toutes les 10 minutes (épuisant, et vous ratez le facteur). Avec un webhook, vous posez une sonnette : le facteur sonne, vous descendez **pile au bon moment**.
>
> **Ce qui se passe vraiment :** le webhook (la sonnette) est une adresse web que vous donnez à un service (votre agenda en ligne, votre outil de paiement…). Dès qu'un événement arrive (un rendez-vous pris, un paiement reçu), ce service « sonne » en envoyant les informations à cette adresse (votre application, ou votre scénario d'automatisation).
>
> **Pour de vrai :** votre agenda en ligne envoie un webhook à votre outil d'automatisation dès qu'un client réserve un créneau. C'est-à-dire que le client est ajouté à votre fichier et reçoit un mail de confirmation **tout seul**, sans que vous touchiez à rien.
>
> Pas si sorcier, non ?

Et dans la conversation, une fois la page publiée :

> Votre page est là : https://claude.ai/code/artifact/…
> **En une phrase :** un webhook, c'est une sonnette que votre application installe chez un autre service pour être prévenue à la seconde où quelque chose se passe.
> Elle est privée. Pour l'envoyer à quelqu'un, ouvrez-la et utilisez Partager, en haut de la page.

## Handoff

Le skill produit une page par concept. Pour aller plus loin, propose au besoin : une version plus
courte, une version « pour un enfant de 10 ans », ou un deuxième concept sur la même page pour
les comparer. Une retouche se fait sur la même page : le lien ne change pas, tout le monde voit
la nouvelle version.

**Prochaine étape** : relance `/explique {autre concept}` pour le mot suivant, ou demande
« ajoute {concept} sur la même page » si vous voulez les comparer.
