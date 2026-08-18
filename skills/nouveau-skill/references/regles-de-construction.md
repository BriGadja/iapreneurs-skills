# Les règles de construction d'un skill

> Lis ce fichier avant d'écrire le skill (étape D). Il condense les règles du `skill-creator`
> officiel d'Anthropic (https://github.com/anthropics/skills, dossier `skills/skill-creator/`) et
> la documentation Claude Code (https://code.claude.com/docs/en/skills). Quand un doute persiste
> sur un format ou un champ, va lire ces deux sources : elles bougent, pas ce fichier.

## 1. La divulgation progressive, le principe qui structure tout le reste

Un skill se charge en trois niveaux, et chacun coûte du contexte à quelqu'un :

1. **Le nom et la description** sont TOUJOURS en mémoire, pour tous les skills installés, à chaque
   conversation. C'est le niveau le plus cher : quelques dizaines de mots, pas plus.
2. **Le corps du `SKILL.md`** n'est lu que lorsque le skill se déclenche. Vise moins de 500 lignes.
3. **Les fichiers annexes** ne sont lus que si le corps dit d'aller les lire. Illimités, et un
   script peut même s'exécuter sans être lu.

La conséquence pratique : tout ce qui n'est utile que dans un cas particulier descend d'un niveau.
Un skill qui gère trois situations différentes garde le tronc commun dans le `SKILL.md` et met une
fiche par situation dans `references/`, avec un mot sur quand aller la lire.

```
mon-skill/
├── SKILL.md          obligatoire : frontmatter + instructions
├── scripts/          du code exécutable, pour ce qui doit être exact ou répétitif
├── references/       des fiches lues à la demande
└── assets/           des fichiers qui servent à produire la sortie (gabarits, polices, icônes)
```

Si un fichier de `references/` dépasse 300 lignes, mets un sommaire en tête.

## 2. La description est le mécanisme de déclenchement, pas un résumé

C'est le seul élément sur lequel Claude décide d'ouvrir le skill ou non. Tout le « quand s'en
servir » va là, jamais dans le corps du fichier, que personne ne lira si le skill ne se déclenche
pas.

**Le vrai problème est le sous-déclenchement.** Claude a tendance à ne PAS ouvrir un skill qui
aurait pourtant servi. Une description tiède se paie donc par un skill installé qui ne part jamais,
et un membre qui croit qu'il ne marche pas. Écris-la insistante, à la troisième personne, en
nommant les situations et les formulations réelles :

- Tiède, et donc inutile : « Aide à construire un tableau de bord. »
- Utile : « Utilise CE skill DÈS QUE l'utilisateur parle de tableau de bord, de visualisation de
  données, de métriques internes, ou veut afficher des chiffres d'entreprise, même s'il n'emploie
  jamais le mot "dashboard". »

Deux choses à savoir sur le déclenchement, qui évitent de faux diagnostics :

- Claude ne consulte un skill que pour une tâche qu'il ne traite pas trivialement lui-même. Une
  demande en une étape (« lis ce fichier ») ne déclenchera aucun skill, quelle que soit la
  description. Ce n'est pas un défaut.
- Chaque entrée du catalogue est plafonnée à 1 536 caractères, description comprise. Mets le cas
  d'usage principal en premier : c'est la fin qui est coupée.

## 3. Écris le pourquoi, pas des interdictions en majuscules

Le modèle qui lira ce skill est bon et a de la théorie de l'esprit. Il fait mieux avec une raison
qu'avec un ordre.

Si tu te surprends à écrire TOUJOURS, JAMAIS ou MUST en capitales, c'est un signal : reformule en
expliquant ce qui casse si on ne le fait pas. Une règle comprise survit aux cas que tu n'avais pas
prévus ; une règle assénée s'applique de travers dès le premier cas de bord.

Deux exceptions où l'interdiction sèche est justifiée : la sécurité, et les échecs silencieux (les
cas où se tromper ne se voit pas). Là, dis-le franchement, et dis quand même pourquoi.

Le reste du style : forme impérative pour les instructions, et un gabarit littéral quand la sortie
doit avoir une forme précise. Un exemple d'entrée suivi de la sortie attendue vaut mieux qu'un
paragraphe de description.

## 4. Ne construis pas pour les trois exemples que tu as sous la main

Un skill sera utilisé des centaines de fois, sur des cas que ni toi ni le membre n'avez vus. Vous
allez pourtant itérer sur deux ou trois exemples, parce que c'est rapide. Le piège est de coudre le
skill à ces exemples : il marchera sur eux, et sur rien d'autre.

Quand un problème résiste, ne le corrige pas en ajoutant une contrainte de plus au cas particulier.
Prends du recul, change de formulation, propose une autre façon de travailler. C'est peu coûteux à
essayer.

Corollaire : garde le skill maigre. Ce qui ne porte pas son poids se retire. Un skill long fait
perdre du temps au modèle avant même qu'il commence.

## 5. Le travail qui se répète devient un script

Si, en testant, tu vois le modèle réécrire trois fois la même fonction ou refaire la même séquence
en plusieurs étapes, c'est le signe qu'il manque un script. Écris-le une fois, mets-le dans
`scripts/`, et dis au skill de l'appeler. Chaque usage futur en profite.

C'est la même logique que l'exactitude : ce qui doit être juste (un calcul, un total, une date, un
comptage) sort du modèle et passe par du code. Le skill s'interdit alors noir sur blanc de refaire
ce calcul lui-même.

## 6. Le skill ne doit pas surprendre

Ce qu'il fait doit correspondre à ce qu'il annonce. Pas de code malveillant, pas d'accès à des
données que sa description ne laisse pas prévoir, pas d'envoi vers l'extérieur non annoncé. Un
membre installe un skill sur la foi de trois lignes : ces trois lignes l'engagent.

## 7. Ce qui rend un skill vraiment utilisable

- **Une seule tâche.** Deux tâches, deux skills.
- **Aucune dépendance surprise** : si le skill a besoin d'un outil externe, il vérifie sa présence
  avant de s'en servir, dit comment l'installer, et s'arrête proprement. Jamais une erreur
  technique incompréhensible.
- **Un échec qui informe** : quand une donnée obligatoire manque, le skill refuse de produire et
  liste tout ce qui cloche d'un coup, dans la langue du membre.
- **Une mémoire lisible** : ce que le skill retient d'une fois sur l'autre tient dans un fichier
  que le membre peut ouvrir, corriger et supprimer.
- **Une sortie qui dit la suite** : le skill se termine en indiquant ce qu'on peut faire après.
