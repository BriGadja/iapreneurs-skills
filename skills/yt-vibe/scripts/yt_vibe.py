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
# Doctor : ce que le skill verifie AVANT de toucher a YouTube.
# Tout est ici, en Python, donc identique sur Windows, macOS et Linux.
# ---------------------------------------------------------------------------
INSTALL = {
    "Windows": {
        "yt-dlp": "winget install --id yt-dlp.yt-dlp -e",
        "ffmpeg": "winget install --id Gyan.FFmpeg -e",
        "deno": "winget install --id DenoLand.Deno -e",
    },
    "Darwin": {
        "yt-dlp": "brew install yt-dlp",
        "ffmpeg": "brew install ffmpeg",
        "deno": "brew install deno",
    },
    "Linux": {
        "yt-dlp": "sudo apt install yt-dlp     (ou : pipx install yt-dlp)",
        "ffmpeg": "sudo apt install ffmpeg",
        "deno": "curl -fsSL https://deno.land/install.sh | sh",
    },
}


def install_cmd(outil):
    return INSTALL.get(platform.system(), INSTALL["Linux"])[outil]


def update_cmd():
    """La bonne commande de mise a jour DEPEND de la facon dont yt-dlp a ete installe.

    Piege paye le 2026-08-31 : `yt-dlp -U` ne met a jour QUE le binaire autonome.
    Installe via pip/pipx/brew, il sort en erreur sans rien faire -- et un skill qui
    avale cette erreur laisse l'utilisateur avec un yt-dlp perime sans le savoir.
    """
    chemin = shutil.which("yt-dlp") or ""
    # Un yt-dlp installe par pip/pipx est un script Python : sa premiere ligne est
    # un shebang qui pointe vers l'interpreteur, et dit donc QUI l'a installe.
    shebang = ""
    try:
        with open(chemin, "rb") as f:
            premiere = f.readline()
        if premiere.startswith(b"#!"):
            shebang = premiere.decode("utf-8", "replace")
    except OSError:
        pass
    if "pipx" in shebang or "pipx" in chemin:
        return "pipx upgrade yt-dlp"
    if "python" in shebang:
        return "python3 -m pip install -U yt-dlp"
    if platform.system() == "Windows":
        return "winget upgrade yt-dlp.yt-dlp"
    if platform.system() == "Darwin":
        return "brew upgrade yt-dlp"
    return "yt-dlp -U     (si installe via pip/pipx : python3 -m pip install -U yt-dlp)"


def version_de(outil, args):
    """Renvoie la premiere ligne de `outil --version`, ou None si absent."""
    if not shutil.which(outil):
        return None
    _, out, err = run([outil] + args, timeout=20)
    return (out or err).strip().splitlines()[0] if (out or err).strip() else "?"


def check():
    """Dit ce qui est present, ce qui manque, et la commande exacte pour reparer."""
    print("Verification des prerequis de /yt-vibe\n")
    manquants = []

    ytdlp = version_de("yt-dlp", ["--version"])
    if ytdlp:
        print(f"  [OK] yt-dlp           {ytdlp}")
        # yt-dlp se version par date (2026.08.19). Perime = il casse sur YouTube.
        try:
            pub = datetime.date(*[int(x) for x in ytdlp.split(".")[:3]])
            age = (datetime.date.today() - pub).days
            if age > 60:
                print(f"       ATTENTION : cette version a {age} jours. yt-dlp casse des que")
                print("       YouTube change quelque chose ; s'il refuse de telecharger,")
                print(f"       mets-le a jour : {update_cmd()}")
        except (ValueError, TypeError):
            pass
    else:
        manquants.append("yt-dlp")
        print("  [!!] yt-dlp           MANQUANT  (il telecharge la video et les sous-titres)")
        print(f"       -> {install_cmd('yt-dlp')}")

    if shutil.which("ffmpeg"):
        print("  [OK] ffmpeg           present")
    else:
        manquants.append("ffmpeg")
        print("  [!!] ffmpeg           MANQUANT  (il extrait les images de la video)")
        print(f"       -> {install_cmd('ffmpeg')}")

    if shutil.which("deno") or shutil.which("node"):
        print("  [OK] moteur JS        present")
    else:
        print("  [--] moteur JS        absent (facultatif aujourd'hui)")
        print("       yt-dlp s'en passe encore, mais il previent que certains formats")
        print("       video deviennent invisibles sans lui. A installer seulement si un")
        print(f"       telechargement echoue sans raison claire : {install_cmd('deno')}")

    print()
    if manquants:
        print(f"MANQUE : {', '.join(manquants)}. Installe ce qui est indique ci-dessus.")
        if platform.system() == "Windows":
            print("Puis FERME ET RELANCE Claude Code : un programme deja ouvert garde")
            print("l'ancien PATH et ne verra pas les nouveaux outils.")
        return 1

    print("Tout est bon. Tu peux lancer /yt-vibe sur une URL YouTube.")
    print("Rappel : ca marche depuis TA machine (box, wifi, 4G). Depuis un serveur")
    print("distant, YouTube repond \"confirm you're not a bot\" et rien ne sort.")
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
        print(f"     version corrige en général sous quelques jours :\n       {update_cmd()}\n",
              file=sys.stderr)
        print("Relance `python3 scripts/yt_vibe.py --check` pour voir où tu en es.",
              file=sys.stderr)
        sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
