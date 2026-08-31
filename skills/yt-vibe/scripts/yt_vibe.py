#!/usr/bin/env python3
"""
yt_vibe.py — pipeline zéro-clé pour le skill /yt-vibe.

Télécharge le transcript (.vtt) + les métadonnées + extrait N frames clés d'une
vidéo YouTube, en utilisant UNIQUEMENT yt-dlp + ffmpeg. Aucune clé API, aucune
infra Sablia : ça tourne sur la machine d'un membre (IP résidentielle = pas de
bot-block YouTube).

Ce script vérifie lui-même ses prérequis (`--check`) : un seul code Python au lieu
d'un bloc shell par système, donc pas de piège Bash/PowerShell. Il dégrade proprement
(jamais de plantage cryptique) si une étape échoue : pas de sous-titres -> on continue
sur les frames + la description.

Usage :
    python3 yt_vibe.py --check              # vérifie les prérequis, ne télécharge rien
    python3 yt_vibe.py <URL> [--frames N] [--workdir DIR]
                        [--max-duration-min M] [--yes]

Sorties (dans --workdir, défaut ./yt-vibe-out/) :
    meta.json        métadonnées (titre, durée, description, tags, chaîne)
    transcript.vtt   sous-titres auto (fr prioritaire, sinon en), si dispo
    frames/*.jpg     N frames clés sous-échantillonnées
    MANIFEST.txt     récap de ce qui a été produit (Claude le lit ensuite)

Codes de sortie :
    0  succès (au moins les frames OU le transcript produits)
    2  vidéo trop longue et --yes absent (garde-fou durée — le SKILL.md demande confirmation)
    3  échec dur (URL invalide, yt-dlp absent, aucune sortie produite)
"""

import argparse
import datetime
import glob
import json
import os
import platform
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# Rapport d'environnement : ce script constate, il ne prescrit pas.
#
# Il ne connait ni la distribution, ni le gestionnaire de paquets, ni les droits
# admin, ni si la machine est un poste local ou un serveur. Ecrire ici des
# commandes d'installation en dur reviendrait a deviner -- et a se tromper pour
# tous ceux qui sortent du cas prevu. On rapporte donc des FAITS ; la session
# Claude de l'utilisateur, qui connait son contexte, decide de la suite.
# ---------------------------------------------------------------------------


def methode_installation(chemin):
    """Comment yt-dlp a-t-il ete installe ? C'est un FAIT, et il decide de la
    commande de mise a jour -- que la session Claude saura en deduire.

    Piege paye le 2026-08-31 : `yt-dlp -U` ne met a jour QUE le binaire autonome.
    Installe via pip/pipx/brew, il sort en erreur sans rien faire, et un skill qui
    avale cette erreur laisse l'utilisateur avec un yt-dlp perime sans le savoir.
    """
    if not chemin:
        return "inconnue"
    shebang = ""
    try:
        with open(chemin, "rb") as f:
            premiere = f.readline()
        if premiere.startswith(b"#!"):
            shebang = premiere.decode("utf-8", "replace").strip()
    except OSError:
        pass
    if "pipx" in shebang or "pipx" in chemin:
        return "pipx (script Python) — `yt-dlp -U` ne fonctionnera PAS dessus"
    if "python" in shebang:
        return "pip (script Python) — `yt-dlp -U` ne fonctionnera PAS dessus"
    return "binaire autonome ou gestionnaire de paquets systeme"


def indices_machine():
    """Indices sur le type de machine. On les EXPOSE, on ne conclut pas :
    c'est la session Claude qui sait ou tourne sa session."""
    indices = []
    if os.path.exists("/.dockerenv"):
        indices.append("conteneur Docker detecte (/.dockerenv)")
    if os.environ.get("WSL_DISTRO_NAME"):
        indices.append(f"WSL ({os.environ['WSL_DISTRO_NAME']})")
    if os.environ.get("SSH_CONNECTION"):
        indices.append("session SSH (machine probablement distante)")
    if platform.system() == "Linux" and not os.environ.get("DISPLAY") \
            and not os.environ.get("WAYLAND_DISPLAY"):
        indices.append("aucun affichage graphique (frequent sur un serveur)")
    return indices


def version_de(outil, args):
    """Renvoie la premiere ligne de `outil --version`, ou None si absent."""
    if not shutil.which(outil):
        return None
    _, out, err = run([outil] + args, timeout=20)
    return (out or err).strip().splitlines()[0] if (out or err).strip() else "?"


def check():
    """Rapporte l'etat de la machine. NE PRESCRIT RIEN : voir le commentaire ci-dessus."""
    print("/yt-vibe — etat de la machine\n")

    print("  Systeme")
    print(f"    plateforme     {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"    python3        {platform.python_version()}")
    for indice in indices_machine():
        print(f"    indice         {indice}")

    print("\n  Ce dont le skill a besoin")
    manquants = []

    chemin = shutil.which("yt-dlp")
    ytdlp = version_de("yt-dlp", ["--version"])
    print("    yt-dlp         INDISPENSABLE — telecharge la video et les sous-titres")
    if ytdlp:
        print(f"                   present : {ytdlp}  ->  {chemin}")
        print(f"                   installe via : {methode_installation(chemin)}")
        # yt-dlp se version par date (2026.08.19). Perime = il casse sur YouTube.
        try:
            pub = datetime.date(*[int(x) for x in ytdlp.split(".")[:3]])
            age = (datetime.date.today() - pub).days
            etat = "a jour" if age <= 60 else f"PERIME ({age} jours)"
            print(f"                   age : {age} jours — {etat}")
            if age > 60:
                print("                   yt-dlp casse des que YouTube change quelque chose ;")
                print("                   une version ancienne est la 1re cause d'echec.")
        except (ValueError, TypeError):
            pass
    else:
        manquants.append("yt-dlp")
        print("                   ABSENT")

    print("    ffmpeg         INDISPENSABLE — extrait les images de la video")
    if shutil.which("ffmpeg"):
        print(f"                   present  ->  {shutil.which('ffmpeg')}")
    else:
        manquants.append("ffmpeg")
        print("                   ABSENT")

    js = shutil.which("deno") or shutil.which("node")
    print("    moteur JS      OPTIONNEL — deno ou node ; yt-dlp previent que certains")
    print("                   formats video deviennent invisibles sans lui")
    print(f"                   {'present  ->  ' + js if js else 'absent (non bloquant aujourd hui)'}")

    print("\n  Verdict")
    if manquants:
        print(f"    MANQUE : {', '.join(manquants)}. Le skill ne peut pas tourner.")
        return 1
    print("    Les outils sont la.")
    print("    Reste une condition que ce script ne peut pas verifier : YouTube refuse")
    print("    les IP de datacenter (\"confirm you're not a bot\"). Depuis une connexion")
    print("    domestique ca passe ; depuis un serveur, souvent pas.")
    return 0


def run(cmd, **kw):
    """Lance une commande, renvoie (returncode, stdout, stderr). Ne lève jamais."""
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=kw.get("timeout", 1800)
        )
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", f"binaire introuvable : {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def even_subsample(items, max_n):
    """Renvoie au plus max_n éléments répartis uniformément dans la liste."""
    n = len(items)
    if n <= max_n:
        return list(items)
    step = n / float(max_n)
    return [items[int(i * step)] for i in range(max_n)]


def fetch_metadata(url, workdir):
    """yt-dlp --dump-json -> meta.json. Renvoie le dict (ou {} si échec)."""
    rc, out, err = run(["yt-dlp", "--dump-json", "--no-warnings", url])
    if rc == 127:
        print(f"❌ {err}", file=sys.stderr)
        sys.exit(3)
    if rc != 0 or not out.strip():
        print(f"⚠️  métadonnées indisponibles ({err.strip()[:200]})", file=sys.stderr)
        return {}
    try:
        meta = json.loads(out.splitlines()[0])
    except json.JSONDecodeError:
        return {}
    keep = {
        k: meta.get(k)
        for k in ("title", "duration", "uploader", "channel", "description",
                  "tags", "categories", "view_count", "upload_date", "webpage_url")
    }
    with open(os.path.join(workdir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(keep, f, ensure_ascii=False, indent=2)
    return keep


def fetch_transcript(url, workdir):
    """Sous-titres auto fr,en au format VTT. Renvoie le chemin .vtt ou None."""
    out_tmpl = os.path.join(workdir, "sub.%(ext)s")
    # Flags canoniques (pluriels) : --write-auto-subs / --sub-langs
    run([
        "yt-dlp", "--write-auto-subs", "--sub-langs", "fr,en",
        "--sub-format", "vtt", "--skip-download", "--no-warnings",
        "-o", out_tmpl, url,
    ])
    # fr prioritaire, sinon en, sinon n'importe quel .vtt produit
    for pat in ("sub.fr*.vtt", "sub.en*.vtt", "sub*.vtt"):
        hits = sorted(glob.glob(os.path.join(workdir, pat)))
        if hits:
            dst = os.path.join(workdir, "transcript.vtt")
            if hits[0] != dst:
                shutil.copyfile(hits[0], dst)
            return dst
    return None


def download_video(url, workdir):
    """best<=720p. Renvoie le chemin du fichier vidéo ou None."""
    out_tmpl = os.path.join(workdir, "video.%(ext)s")
    rc, _, err = run([
        "yt-dlp", "-f", "best[height<=720]/best",
        "--no-warnings", "-o", out_tmpl, url,
    ])
    hits = [p for p in glob.glob(os.path.join(workdir, "video.*"))
            if not p.endswith((".part", ".ytdl"))]
    if rc != 0 and not hits:
        print(f"⚠️  téléchargement vidéo échoué ({err.strip()[:200]})", file=sys.stderr)
        return None
    return hits[0] if hits else None


def extract_frames(video, workdir, target, duration):
    """Scene-detect puis fallback intervalle si <25% de la cible. Renvoie la liste finale de .jpg."""
    raw = os.path.join(workdir, "_frames_raw")
    os.makedirs(raw, exist_ok=True)
    for f in glob.glob(os.path.join(raw, "*.jpg")):
        os.remove(f)

    # 1) Détection de scène ( -fps_mode vfr : -vsync vfr déprécié ffmpeg 5.0+ )
    run([
        "ffmpeg", "-y", "-i", video,
        "-vf", "select='gt(scene,0.3)',scale=1280:-2",
        "-fps_mode", "vfr", "-frames:v", "80", "-q:v", "3",
        os.path.join(raw, "scene_%03d.jpg"),
    ])
    scene = sorted(glob.glob(os.path.join(raw, "scene_*.jpg")))

    # 2) Fallback intervalle si la détection a donné < 25% de la cible
    if len(scene) < max(1, target // 4) and duration and duration > 0:
        fps = max(target, 1) / float(duration)
        run([
            "ffmpeg", "-y", "-i", video,
            "-vf", f"fps={fps:.6f},scale=1280:-2",
            "-frames:v", str(target), "-q:v", "3",
            os.path.join(raw, "iv_%03d.jpg"),
        ])

    candidates = sorted(glob.glob(os.path.join(raw, "*.jpg")))
    chosen = even_subsample(candidates, target)

    frames_dir = os.path.join(workdir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    for f in glob.glob(os.path.join(frames_dir, "*.jpg")):
        os.remove(f)
    final = []
    for i, src in enumerate(chosen, 1):
        dst = os.path.join(frames_dir, f"frame_{i:03d}.jpg")
        shutil.copyfile(src, dst)
        final.append(dst)
    shutil.rmtree(raw, ignore_errors=True)
    return final


def main():
    # --check se traite avant argparse : il n'a pas besoin d'URL.
    if "--check" in sys.argv[1:]:
        sys.exit(check())

    ap = argparse.ArgumentParser(description="Pipeline zéro-clé /yt-vibe (yt-dlp + ffmpeg).")
    ap.add_argument("url", help="URL de la vidéo YouTube")
    ap.add_argument("--frames", type=int, default=12, help="nombre de frames clés (défaut 12)")
    ap.add_argument("--workdir", default="yt-vibe-out", help="dossier de sortie")
    ap.add_argument("--max-duration-min", type=int, default=30,
                    help="garde-fou : au-delà, demande --yes (défaut 30 min)")
    ap.add_argument("--yes", action="store_true",
                    help="confirme le téléchargement même pour une vidéo longue")
    args = ap.parse_args()

    os.makedirs(args.workdir, exist_ok=True)

    # 1) Métadonnées (+ garde-fou durée)
    meta = fetch_metadata(args.url, args.workdir)
    duration = meta.get("duration") or 0
    if duration and duration > args.max_duration_min * 60 and not args.yes:
        mins = round(duration / 60)
        print(f"⚠️  Vidéo longue : ~{mins} min. Le téléchargement peut peser plusieurs Go "
              f"et prendre du temps.\n   Relance avec --yes pour confirmer, ou choisis une "
              f"vidéo plus courte.", file=sys.stderr)
        sys.exit(2)

    # 2) Transcript (best-effort)
    transcript = fetch_transcript(args.url, args.workdir)

    # 3) Vidéo + frames (best-effort)
    frames = []
    video = download_video(args.url, args.workdir)
    if video:
        frames = extract_frames(video, args.workdir, args.frames, duration)
        try:
            os.remove(video)  # on garde les frames, pas la vidéo (lourde)
        except OSError:
            pass

    # 4) Manifest pour Claude
    has_caps = transcript is not None
    lines = [
        "# /yt-vibe — sortie du pipeline",
        f"URL        : {args.url}",
        f"Titre      : {meta.get('title', '(inconnu)')}",
        f"Chaîne     : {meta.get('uploader') or meta.get('channel') or '(inconnue)'}",
        f"Durée      : {round(duration/60, 1) if duration else '?'} min",
        f"Transcript : {'transcript.vtt' if has_caps else 'AUCUN sous-titre dispo'}",
        f"Frames     : {len(frames)} dans frames/",
        f"Métadonnées: meta.json",
        "",
    ]
    if not has_caps:
        lines.append("NOTE: pas de sous-titres -> analyse la vibe sur les frames + la description (meta.json).")
    with open(os.path.join(args.workdir, "MANIFEST.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))

    if not frames and not has_caps:
        print("\nRien n'a pu être récupéré : ni images, ni transcript.", file=sys.stderr)
        print("Les deux causes possibles, dans l'ordre :\n", file=sys.stderr)
        print("  1. Tu n'es pas sur une connexion domestique.", file=sys.stderr)
        print("     Si le message ci-dessus dit \"Sign in to confirm you're not a bot\",", file=sys.stderr)
        print("     c'est ça : YouTube bloque les IP de serveurs. Ce skill est fait pour", file=sys.stderr)
        print("     tourner sur TA machine (box, wifi, 4G), pas sur un VPS.\n", file=sys.stderr)
        print("  2. yt-dlp est périmé.", file=sys.stderr)
        print("     Il casse dès que YouTube change quelque chose, et une nouvelle", file=sys.stderr)
        print("     version corrige en général sous quelques jours.\n", file=sys.stderr)
        print("Lance `python3 scripts/yt_vibe.py --check` : il donne la version installée,",
              file=sys.stderr)
        print("son âge et la façon dont elle a été installée — de quoi trouver la bonne",
              file=sys.stderr)
        print("commande de mise à jour pour cette machine.", file=sys.stderr)
        sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
