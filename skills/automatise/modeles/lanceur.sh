#!/usr/bin/env bash
# Lanceur d'une tâche /automatise sur un serveur Linux : Claude Code sans fenêtre (claude -p).
#
# Une tâche = un dossier qui contient ce lanceur, sa consigne (consigne.md), son journal
# (journal.log) et ses résultats (resultats/). Supprimer le dossier supprime la tâche, une fois
# la ligne de crontab retirée.
#
# La crontab n'appelle QUE ce fichier, avec un marqueur qui permet de retrouver la ligne :
#   7 7 * * * /chemin/absolu/vers/ce/dossier/lanceur.sh # automatise:{nom-court}
#
# Tout ce qui casse sous cron casse ici, de façon lisible : le PATH réduit, le dossier courant,
# la connexion au compte, une permission que personne n'est là pour accorder, deux passages qui
# se chevauchent, un passage qui ne s'arrête pas.

set -u
umask 077   # journal, résultats et verrou lisibles par le seul propriétaire : ils peuvent contenir
            # des données clients, et un serveur peut avoir d'autres comptes.

# ── À REMPLIR ───────────────────────────────────────────────────────────────────────────────
NOM="{nom-court}"                          # le même que dans le carnet et dans le marqueur cron
TRAVAIL="{/chemin/absolu/du/dossier/de/travail}"   # là où Claude lit et écrit
CLAUDE="{/chemin/absolu/vers/claude}"      # la sortie de : command -v claude
# Lire le dossier de travail ne demande aucune autorisation. N'ajoute que ce dont la tâche a
# besoin, au plus près : "WebFetch(domain:example.com)" pour lire un site,
# "Edit(rapports/**)" pour écrire dans rapports/ du dossier de travail.
# 🔴 Jamais "Bash", "Bash(curl *)" ni "Read" sans chemin : une tâche qui lit le web peut être
# manipulée par ce qu'elle lit, et une règle Bash ne bride pas les arguments (doc permissions).
OUTILS=""
# Retirés à Claude pendant le passage. Bash est retiré par défaut : même sans autorisation,
# certaines commandes (cat, echo…) passent sans demander, et elles verraient le jeton.
INTERDITS="Bash,Read(~/.config/automatise/**),Read(~/.claude/**)"
MODELE=""                                  # vide = le modèle par défaut ; ex. "sonnet" ou "haiku"
ECHANGES_MAX=30                            # nombre maximal d'allers-retours par passage
DUREE_MAX="30m"                            # au-delà, le passage est arrêté (code 124)
JETON="$HOME/.config/automatise/jeton"     # optionnel : le jeton de « claude setup-token »,
                                           # seul dans ce fichier, droits 600
# Prévenir la personne : une commande qui reçoit le message sur son entrée standard, choisie avec
# elle à l'étape 4. Vide = seulement le fichier ECHEC.txt dans ce dossier.
# Exemple (ntfy) : PREVENIR="curl -s -H 'Title: automatise' -d @- https://ntfy.sh/{sujet-long-et-imprevisible}"
# Attention : un sujet ntfy.sh est public pour qui connaît son nom. Par un tel service, laisse
# PREVENIR_SI_SUCCES à "non" dès que le résultat touche des clients ou de l'argent.
PREVENIR=""
PREVENIR_SI_SUCCES="non"                   # "oui" = envoyer aussi le résultat quand tout va bien
# ────────────────────────────────────────────────────────────────────────────────────────────

ICI="$(cd "$(dirname "$0")" && pwd)"
JOURNAL="$ICI/journal.log"
mkdir -p "$ICI/resultats"
PATH="$(dirname "$CLAUDE"):/usr/local/bin:/usr/bin:/bin"
export PATH

journal() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$JOURNAL"; }

prevenir() {  # $1 = titre ; le corps arrive sur l'entrée standard
  local corps; corps="$(cat)"
  if [ -n "$PREVENIR" ]; then
    printf '%s\n\n%s\n' "$1" "$corps" | sh -c "$PREVENIR" >/dev/null 2>&1 \
      || journal "la commande PREVENIR a échoué"
  fi
  return 0
}

echec() {  # $1 = raison
  journal "ÉCHEC : $1"
  { printf 'Tâche « %s » en échec le %s\n%s\n\nDernières lignes du journal :\n' \
      "$NOM" "$(date '+%Y-%m-%d %H:%M')" "$1"; tail -n 15 "$JOURNAL"; } > "$ICI/ECHEC.txt"
  prevenir "Tâche « $NOM » : échec" < "$ICI/ECHEC.txt"
  exit 1
}

# Deux passages ne tournent jamais en même temps (flock existe sur Linux, pas sur Mac).
if command -v flock >/dev/null 2>&1; then
  exec 9>"$ICI/.verrou"
  flock -n 9 || { journal "passage sauté : le précédent tourne encore"; exit 0; }
fi

journal "début"
[ -x "$CLAUDE" ] || echec "claude introuvable à $CLAUDE (refaire : command -v claude)"
[ -d "$TRAVAIL" ] || echec "dossier de travail introuvable : $TRAVAIL"
[ -r "$ICI/consigne.md" ] || echec "consigne introuvable : $ICI/consigne.md"

# Une clé d'API présente serait utilisée à la place de l'abonnement, et facturée à l'usage.
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN

if [ -r "$JETON" ]; then
  [ "$(stat -c %a "$JETON" 2>/dev/null)" = "600" ] || journal "attention : $JETON devrait être en droits 600"
  CLAUDE_CODE_OAUTH_TOKEN="$(tr -d '[:space:]' < "$JETON")"
  export CLAUDE_CODE_OAUTH_TOKEN
else
  journal "pas de jeton : la connexion enregistrée par /login sur ce serveur sera utilisée"
fi

ARGS=(-p "$(cat "$ICI/consigne.md")" --permission-mode dontAsk --max-turns "$ECHANGES_MAX")
[ -n "$OUTILS" ] && ARGS+=(--allowedTools "$OUTILS")
[ -n "$INTERDITS" ] && ARGS+=(--disallowedTools "$INTERDITS")
[ -n "$MODELE" ] && ARGS+=(--model "$MODELE")

DUREE=()
command -v timeout >/dev/null 2>&1 && DUREE=(timeout "$DUREE_MAX")

SORTIE="$ICI/resultats/$(date '+%Y-%m-%d_%H%M').md"
cd "$TRAVAIL" || echec "impossible d'entrer dans $TRAVAIL"
${DUREE[@]+"${DUREE[@]}"} "$CLAUDE" "${ARGS[@]}" < /dev/null > "$SORTIE" 2>> "$JOURNAL"
CODE=$?

case "$CODE" in
  0)   journal "fin : réussi -> $SORTIE"
       rm -f "$ICI/ECHEC.txt"
       [ "$PREVENIR_SI_SUCCES" = "oui" ] && prevenir "Tâche « $NOM »" < "$SORTIE" ;;
  124) echec "arrêtée au bout de $DUREE_MAX (DUREE_MAX)" ;;
  *)   echec "claude a terminé avec le code $CODE ; sa réponse : $(head -c 400 "$SORTIE")" ;;
esac

# Ménage : les résultats de plus de 30 jours, dans le dossier de CETTE tâche seulement.
find "$ICI/resultats" -type f -name '*.md' -mtime +30 -delete 2>/dev/null
exit 0
