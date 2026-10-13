# Les solutions, une par une : ce qu'il faut, ce qui casse

> À lire à l'étape 2 du skill, **seulement la section de la solution retenue**. Chaque section dit
> quand la choisir, ce qu'il faut, comment la programmer, comment l'arrêter, et les pièges qui
> font qu'une tâche « programmée » ne tourne jamais.
>
> 🔴 Tout ce qui suit a été vérifié dans la documentation officielle le 2026-10-13. Les outils de
> planification de Claude Code changent vite : si un détail ne correspond pas à ce que tu vois sur
> cette machine, **crois la machine et la documentation du jour**, pas ce fichier.
> Comparatif officiel : https://code.claude.com/docs/en/scheduled-tasks

---

## A. Un script, sans Claude

**Quand** : la tâche ne réfléchit pas. Télécharger, copier, sauvegarder, compter, vérifier qu'une
page répond, renommer des fichiers.

**Pourquoi c'est la meilleure option quand elle est possible** : aucun forfait consommé, aucune
connexion à un compte qui peut expirer, aucun service tiers. Un script qui marchait hier marche
demain.

**Le planificateur, selon la machine** :

| Machine | Planificateur | Programmer | Arrêter |
|---|---|---|---|
| Linux, serveur | cron (`crontab -e`) ou un minuteur systemd | une ligne dans la crontab | supprimer la ligne |
| Mac | launchd (un fichier `.plist` dans `~/Library/LaunchAgents/`) ; cron existe aussi | `launchctl` charge le fichier | `launchctl` le décharge, puis supprimer le fichier |
| Windows | le Planificateur de tâches (`schtasks` ou `Register-ScheduledTask` en PowerShell) | une tâche nommée | la supprimer par son nom |

**Les pièges** :
- 🔴 **Le planificateur ne voit pas ce que voit votre terminal.** Sous cron, le `PATH` est réduit
  au strict minimum (`/usr/bin:/bin` sur la plupart des Linux, vérifiable avec `man 5 crontab`),
  le dossier courant est le dossier personnel, et vos alias et variables de `.bashrc` n'existent
  pas. Un programme installé dans `~/.local/bin`, par nvm ou par Homebrew est **introuvable** :
  écris des chemins absolus partout, ou fixe le `PATH` dans le script lui-même.
- 🔴 **Sous cron, le caractère `%` coupe la ligne** (tout ce qui suit part sur l'entrée standard).
  `date +%F` dans une ligne de crontab casse sans message. Mets la commande dans un script, ou
  échappe `\%`.
- **Garde une trace** : redirige la sortie et les erreurs vers un fichier journal
  (`>> journal.log 2>&1`). Sans ça, un échec ne laisse aucune trace.
- **Le fuseau** : cron utilise l'heure de la machine. Un serveur est souvent réglé en UTC, donc
  « 8 h » dans la crontab peut vouloir dire 9 h ou 10 h à Paris. Vérifie avec `date` et
  `timedatectl`, et dis l'heure réelle à la personne.
- **Mac** : préfère launchd à cron. Apple le dit (« `cron` is not a recommended solution. It has
  been deprecated in favor of `launchd` ») et la différence compte : une exécution cron tombée
  pendant la veille est perdue, une exécution launchd (`StartCalendarInterval`) part au réveil.
  Ni l'un ni l'autre ne rattrape un Mac **éteint**. Source :
  https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/ScheduledJobs.html
- **Linux qui n'est pas un serveur** (un portable) : un minuteur systemd avec `Persistent=true`
  rattrape au démarrage une exécution manquée ; cron ne le fait pas.
- **Retrouver la ligne plus tard** : termine chaque ligne de crontab par un marqueur,
  `# automatise:{nom-court}`. C'est ce que le carnet cite dans « Comment l'arrêter ».
- **Windows et ordinateur éteint** : une tâche du Planificateur ne tourne que si la machine est
  allumée ; l'option « exécuter dès que possible si une exécution a été manquée » rattrape au
  démarrage. Si la tâche doit tourner sans session ouverte, il faut l'option « exécuter même si
  l'utilisateur n'est pas connecté », qui demande le mot de passe Windows : c'est la personne qui
  le tape dans la fenêtre du système, **jamais dans la conversation**.

---

## B. Une routine cloud

**Quand** : la tâche réfléchit, et n'a pas besoin des fichiers de cette machine. Elle lit le web,
une boîte mail ou un outil par un connecteur, ou un dépôt GitHub. Aussi pour une tâche qui ne
réfléchit pas (vérifier qu'un site répond) quand elle doit tourner ordinateur éteint et que la
personne n'a ni serveur ni outil d'automatisation : elle paie alors en forfait ce qu'un script
ferait gratuitement, dis-le.

**Ce que c'est** : une session Claude Code complète qui démarre sur les serveurs d'Anthropic à
l'heure dite, ordinateur éteint. Doc : https://code.claude.com/docs/en/routines

**Ce qu'il faut** :
- un abonnement Pro, Max, Team ou Enterprise, et une session connectée **avec ce compte claude.ai**.
  `/schedule` est caché si la session est connectée par une clé d'API (variable
  `ANTHROPIC_API_KEY`) ;
- **un dépôt GitHub** : la documentation définit une routine comme « un prompt, un ou plusieurs
  dépôts, et des connecteurs », et le dépôt est cloné à chaque passage. Si la personne n'a ni
  GitHub ni dépôt, dis-le avant de commencer : c'est un coût d'entrée réel, et la tâche Desktop
  (section C) peut suffire ;
- pour lire une boîte mail, un agenda, un Drive : le connecteur correspondant, ajouté sur
  https://claude.ai/customize/connectors. Un serveur MCP ajouté seulement dans le terminal
  (`claude mcp add`) n'existe pas pour une routine.

**Programmer** : `/schedule` dans Claude Code (la conversation pose les questions et enregistre),
ou le formulaire de https://claude.ai/code/routines. Le formulaire propose des fréquences toutes
faites (toutes les heures, chaque jour, en semaine, chaque semaine) ; pour une autre fréquence,
`/schedule update` accepte une expression cron. **Au moins une heure entre deux passages.**
Choisis une heure qui ne tombe pas pile (8 h 07 plutôt que 8 h) : la doc prévient qu'une routine
calée sur l'heure pile peut démarrer avec plusieurs minutes de retard.

**Premier passage** : bouton « Run now » sur la page de la routine, ou `/schedule run`.

**Arrêter** : l'interrupteur en haut de la page de la routine (pause), ou « Delete » dans son menu.
`/schedule list` les montre toutes.

**Les pièges** :
- 🔴 **Tous les connecteurs du compte sont inclus par défaut**, et la routine s'en sert en
  écriture sans rien demander. Retire tous ceux dont la tâche n'a pas besoin.
- 🔴 **Un statut vert ne veut pas dire que la tâche a réussi**, seulement que la session a démarré
  et s'est terminée (dit tel quel dans la doc). Il faut ouvrir le passage et lire.
- Le réseau est filtré : par défaut, une routine n'atteint qu'une liste de domaines courants. Un
  site hors liste répond 403 ; il faut l'autoriser dans l'environnement de la routine.
- Ce que fait la routine se fait **au nom de la personne** : un commit porte son compte GitHub, un
  mail part de sa boîte.
- Chaque passage consomme son forfait comme une session normale.
- Si la connexion GitHub expire, la routine saute ses passages, puis s'éteint au bout de 72 h.

---

## C. Une tâche planifiée de l'application Claude Desktop

**Quand** : la tâche réfléchit, a besoin des fichiers de l'ordinateur, et l'ordinateur est un
poste de travail (pas un serveur).

**Ce que c'est** : l'application Desktop ouvre une nouvelle session à l'heure dite, dans le dossier
choisi, avec les fichiers et outils de la machine. Doc :
https://code.claude.com/docs/en/desktop-scheduled-tasks

**Ce qu'il faut** : l'application Claude Desktop, **ouverte**, sur un ordinateur **allumé et
éveillé** à l'heure dite.

**Programmer** : dans l'onglet Code de l'application, « Routines », nouvelle routine, en
choisissant **« Local »** (« Cloud » crée une routine de la section B). On y renseigne un nom, la
consigne, la fréquence, le dossier de travail et le mode de permission. Si cette session tourne
dans l'application Desktop, on peut aussi le demander en langage courant (« programme chaque lundi
à 8 h… »). Si tu n'as pas d'outil pour créer cette tâche (c'est le cas dans un terminal),
prépare la consigne mot pour mot et donne les clics.

**Premier passage** : « Run now » sur la page de la tâche. 🔴 **Pendant ce premier passage,
accepte « toujours autoriser » pour chaque outil demandé** : sinon chaque passage suivant
s'arrêtera sur une demande de permission que personne ne verra.

**Arrêter** : la tâche passe de « Active » à « Paused » sur sa page ; « Delete » la supprime (cocher
la suppression des fichiers sur disque pour effacer aussi sa consigne). La consigne vit dans
`~/.claude/scheduled-tasks/<nom>/SKILL.md`, modifiable à la main.

**Les pièges** :
- 🔴 **Ordinateur en veille à l'heure dite = passage sauté.** Au réveil, un seul rattrapage pour
  le passage manqué le plus récent. Une tâche de 9 h peut donc tourner à 23 h : la consigne doit
  s'en protéger (« ne traite que les éléments du jour ; s'il est après 17 h, fais seulement le
  résumé de ce qui a été manqué »). L'option « Keep computer awake » des réglages évite la veille
  automatique, pas celle du capot fermé.
- Par défaut, la tâche travaille sur l'état réel du dossier, modifications en cours comprises.
- Un outil marqué comme exigeant une validation humaine bloquera chaque passage.

---

## D. Le planificateur d'un serveur qui lance Claude Code sans fenêtre

**Quand** : la tâche réfléchit, a besoin des fichiers d'une machine, et cette machine est un
serveur toujours allumé (VPS).

**Ce que c'est** : cron (ou un minuteur systemd) lance `claude -p "consigne"`, Claude Code sans
interface : il fait la tâche, écrit son résultat, s'arrête. Doc :
https://code.claude.com/docs/en/headless

**Ce qu'il faut** :
- `claude` installé sur le serveur, et son **chemin absolu** (`command -v claude`) : il est souvent
  dans `~/.local/bin`, que cron ne connaît pas ;
- **une connexion au compte qui tient sans personne** : `claude setup-token` génère un jeton valable
  un an, à mettre dans la variable `CLAUDE_CODE_OAUTH_TOKEN`. Il utilise l'abonnement, fait des
  requêtes au modèle, **mais n'accède pas aux connecteurs claude.ai** (les serveurs MCP configurés
  sur la machine marchent). 🔴 C'est la personne qui lance la commande et place le jeton (dans un
  fichier lisible par elle seule, chargé par le lanceur) : il ne passe jamais par la conversation ;
- 🔴 **pas de variable `ANTHROPIC_API_KEY` dans l'environnement de la tâche**, sauf si c'est voulu :
  en mode `-p`, une clé présente est toujours utilisée, et la tâche est alors facturée à l'usage
  sur l'API au lieu de l'abonnement ;
- **les permissions décidées à l'avance** : personne ne sera là pour cliquer. Fixe toujours le mode
  (`--permission-mode dontAsk` : tout ce qui demanderait une permission est refusé ; sans mode
  explicite, la doc prévient que le mode de départ peut être `auto`). Lire le dossier de travail
  ne demande rien ; n'autorise en plus que le nécessaire, au plus près :
  `WebFetch(domain:example.com)` pour lire un site, `Edit(rapports/**)` pour écrire dans un
  sous-dossier (une règle `Write(…)` avec un chemin n'est jamais consultée : c'est `Edit` qui
  compte). 🔴 **Retire Bash** (`--disallowedTools "Bash"`) sauf besoin réel : une règle comme
  `Bash(curl *)` ne bride pas les arguments (« Bash permission patterns that try to constrain
  command arguments are fragile », doc https://code.claude.com/docs/en/permissions), et des
  commandes comme `cat` ou `echo` passent sans autorisation dans tous les modes, assez pour
  afficher le jeton si une page lue par la tâche l'y pousse. Interdis aussi la lecture du jeton
  et de `~/.claude/` (`Read(~/.config/automatise/**)`, `Read(~/.claude/**)`). Le lanceur le fait
  par défaut. 🔴 N'utilise jamais un mode qui saute toutes les permissions pour une tâche sans
  surveillance.
- **la connexion vérifiée** : `claude auth status --text` dit avec quoi Claude est connecté sur
  cette machine.

**Programmer** : une tâche = un dossier (par exemple `~/automatise/{nom-court}/`) qui contient
le lanceur, sa consigne, son journal et ses résultats. Pars des deux modèles rangés dans le
dossier `modeles/` du skill :
- `modeles/lanceur.sh` : le lanceur à remplir (chemin absolu de `claude`, dossier de travail,
  outils autorisés et interdits, modèle, nombre maximal d'échanges, durée maximale, jeton, façon
  de prévenir). Dossier de la tâche en droits 700 (`chmod 700`) : le lanceur peut contenir le
  sujet ntfy, et ses résultats des données clients.
  Il pose un verrou contre deux passages simultanés, retire toute clé d'API de l'environnement,
  écrit un journal, range chaque résultat daté, et prévient la personne en cas d'échec (et en cas
  de succès si elle le veut). Testé le 2026-10-13 dans les conditions de cron : réussite,
  `claude` introuvable, durée dépassée ;
- `modeles/consigne.md` : la consigne, à remplir à l'étape 5.

La crontab n'appelle que le lanceur, avec son marqueur :
`7 7 * * * /chemin/absolu/lanceur.sh # automatise:{nom-court}`.

**Prévenir la personne depuis un serveur** est la partie la plus délicate : le jeton d'abonnement
n'ouvre pas les connecteurs claude.ai (pas de mail par Gmail). Une solution
simple : une notification sur le téléphone par ntfy (une application de notifications : on
s'abonne à un « sujet » dans l'application, et un `curl` vers `https://ntfy.sh/{sujet}` y envoie un
message ; doc https://docs.ntfy.sh/publish/). 🔴 La doc le dit : « topic names are public ».
Choisis un sujet long et imprévisible, et **n'y envoie que l'état et l'endroit où lire le
résultat**, jamais son contenu quand il touche des clients ou de l'argent. Si la personne a déjà un
bot Telegram, un relais mail ou un outil d'automatisation, utilise le sien.

**Premier passage** : lance le lanceur à la main, depuis un shell, puis **une seconde fois dans
les conditions de cron** (`env -i HOME="$HOME" /bin/sh -c '/chemin/lanceur.sh'`) : c'est là que les
problèmes de `PATH` et de jeton apparaissent, pas dans le terminal.

**Arrêter** : supprimer la ligne de la crontab (`crontab -e`), puis le dossier de la tâche. Le
jeton, lui, reste valable jusqu'à son expiration : s'il ne sert plus à aucune tâche, supprime le
fichier qui le contient.

**Les pièges** : tous ceux du script (section A : `PATH`, `%`, journal, fuseau), plus :
- 🔴 **Le jeton expire au bout d'un an** et la tâche échoue alors à chaque passage. Note la date
  d'expiration dans le carnet.
- Sans `--bare`, `claude -p` charge le `CLAUDE.md`, les hooks et le `.mcp.json` du dossier, sans
  demander de confiance. Lance la tâche dans un dossier dont tu connais le contenu. (`--bare` ne lit
  pas le jeton d'abonnement : ne l'utilise pas avec `CLAUDE_CODE_OAUTH_TOKEN`.)
- Le code de sortie est non nul quand le passage échoue : c'est ce qui permet au lanceur de
  prévenir la personne.
- Chaque passage consomme le forfait de l'abonnement, comme une session normale.

---

## Ce qui ne convient jamais à une tâche durable

`/loop` et les tâches planifiées à l'intérieur d'une session ne tournent que tant que la session
est ouverte, et **expirent au bout de sept jours**. Elles servent à surveiller quelque chose pendant
qu'on travaille, pas à automatiser.
