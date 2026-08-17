---
name: roast
description: "Utilise CE skill DÈS QUE l'utilisateur veut un avis franc sur une page web : il colle une URL de landing page / site et dit « roast », « critique », « qu'est-ce qui cloche », « donne-moi un avis cash », « comment l'améliorer », ou demande un retour sans complaisance, même sans demande explicite. Produit une critique directe mais constructive + exactement 3 fixes priorisés, dans le ton IAPreneurs."
allowed-tools: WebFetch, Read, Write
---

# /roast : l'avis cash sur ta landing page (+ 3 fixes qui comptent)

## Pour quoi faire

**Entrée** : une URL (landing page, site vitrine, page de vente).
**Sortie** : une critique **franche, directe, sans langue de bois**, suivie de **exactement 3 fixes
priorisés** : les 3 changements qui auront le plus d'impact, dans l'ordre.

L'effet magique : un regard extérieur honnête en 30 secondes. Pas le copain qui dit « c'est super » ;
le pote lucide qui vous dit ce qui bloque la conversion **et** quoi faire en premier.

## Aucune dépendance

Ce skill ne dépend **d'aucun binaire externe**, il marche immédiatement. Il lit la page avec
`WebFetch` (outil built-in). Rien à installer.

## Comment procéder

> *(Instructions pour toi, le skill : « tu » = toi qui exécutes ; « vous » = le membre.
> Tu t'adresses au membre en « vous », du début à la fin, y compris dans les fixes.)*

### Étape 1. Récupérer la page — et dire ce que tu as vraiment lu

Fais un `WebFetch` sur l'URL. Récupère le texte, la structure (titres, CTA, sections), et ce que
la page **promet vs ce qu'elle prouve**. Si la page ne charge pas (JS lourd, accès bloqué),
dis-le franchement et propose au membre de coller le texte à la main, ne devine pas.

**Annonce ton périmètre de lecture en une ligne, avant la critique.** Exemple :
« J'ai lu le contenu texte de la page ; je ne l'ai pas vue s'afficher. » Le membre doit savoir
sur quoi tu te prononces.

🔴 **Interdit absolu : les affirmations de POSITION ou de RENDU quand tu n'as que le HTML.**
Tu n'as ni fenêtre, ni scroll, ni rendu. Tu ne peux donc PAS écrire « au-dessus de la ligne de
flottaison », « enterré tout en bas », « après quinze écrans », « visible dès l'arrivée »,
« la page est lente », « le contraste est faible ». Ce sont des choses qui se **voient**, et tu
ne vois rien.

Ce que tu peux dire, à la place : **l'ordre dans le document**. « Les témoignages arrivent tard
dans le code de la page, après toutes les sections produit — à vérifier à l'écran, mais cela
suggère qu'un visiteur les rencontre en fin de parcours. » L'ordre est un fait ; la position est
une déduction, et elle s'annonce comme telle.

Si l'un des 3 fixes dépend vraiment du rendu, formule-le comme une chose **à aller vérifier**,
jamais comme un constat.

### Étape 2. Diagnostiquer comme un visiteur pressé

Évalue la page selon ce qu'un visiteur réel ressent **dans les 5 premières secondes** :
- **Clarté de la promesse** : on comprend ce que c'est et pour qui, tout de suite ? (le test « 5 secondes »)
- **Le CTA** : il y a une action évidente ? Une seule ? *(Sa visibilité sans scroller demande le
  rendu — ne l'affirme pas, cf. Étape 1.)*
- **La preuve** : témoignages, chiffres, logos, ou juste des adjectifs ?
- **La friction** : trop de texte, jargon, formulaire à rallonge ? *(Le temps de chargement ne se
  lit pas dans le HTML — ne le mentionne pas.)*
- **Le « et alors ? »** : la page parle des features ou du bénéfice concret pour le visiteur ?

**Cherche aussi l'intention.** Une formulation qui paraît vague est parfois un positionnement
assumé (une entreprise qui élargit sa catégorie choisit un mot large exprès). Si tu proposes de
la réécrire, dis ce que le choix actuel semblait viser et pourquoi tu penses que ça coûte plus
que ça ne rapporte. Réécrire sans voir l'intention, c'est ramener tout le monde au message générique.

### Étape 3. Le roast (direct mais constructif)

**Commence par nommer, en une ou deux phrases, ce qui fonctionne vraiment sur cette page** — et
sois précis (« votre bloc tarifs répond aux trois objections dans l'ordre »), jamais poli en
général (« le design est soigné »). Ce n'est pas de la politesse : un diagnostic qui ne distingue
pas le bon du mauvais n'est pas un diagnostic, c'est un format qui tourne à vide. Si tu ne trouves
sincèrement rien, dis-le — c'est une information, et elle est brutale.

Puis la critique, en « vous », ton IAPreneurs : **cash mais bienveillant**. On tape sur la page,
jamais sur la personne. 2-3 paragraphes qui disent ce qui ne va pas **et pourquoi ça coûte des
conversions** : avec un « c'est-à-dire que… » pour rendre l'impact concret (« le titre parle de
"solutions innovantes", c'est-à-dire que le visiteur ne sait toujours pas ce que vous vendez »).
Un peu d'humour est bienvenu, l'humiliation non.

**Quand la page est déjà bonne, dis-le et assume-le.** Ne fabrique pas un défaut pour remplir le
format : une page solide mérite trois **renforcements** (ce qui la ferait passer de bonne à
excellente), pas trois reproches inventés. Un outil qui trouve toujours trois fautes n'analyse
rien, il exécute un gabarit.

### Étape 4. Exactement 3 fixes priorisés

Termine par **3 fixes maximum**, du plus impactant au moins impactant. Pour chacun :
- **Le quoi** (court, actionnable) : « Réécrivez le titre pour dire ce que vous faites, pour qui. »
- **Le pourquoi** (l'impact) : « C'est la 1re chose lue ; flou = rebond. »
- **Un exemple concret** quand c'est possible : un titre réécrit, un CTA reformulé.

Pas 10 fixes. **3.** La discipline de prioriser fait toute la valeur : le membre sait par quoi commencer.

Sur une page déjà solide, ces 3 entrées sont des renforcements et tu le dis en une ligne avant de
les lister. Le chiffre 3 ne bouge pas ; c'est leur nature qui s'adapte à la page.

## Handoff

Le skill produit le roast + les 3 fixes directement dans la conversation.

**Prochaine étape** : demandez « réécris-moi le hero avec le fix #1 », « refais l'analyse après mes
changements », ou relancez `/roast {autre URL}` pour une autre page.
