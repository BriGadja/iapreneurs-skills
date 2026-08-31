#!/usr/bin/env python3
"""devis.py — genere un devis PDF (+ HTML) depuis un JSON, et verifie son travail.

Pourquoi un script et pas le LLM ? LE DETERMINISME : les totaux, la TVA et les
arrondis sont calcules ICI, en Python (Decimal, arrondi au centime ROUND_HALF_UP).
Le modele ne fait JAMAIS l'arithmetique d'un devis.

Pourquoi un devis et pas une facture ? La facturation electronique (reforme
2026-2027) impose d'emettre les factures B2B via une plateforme agreee. Le devis,
lui, reste libre : c'est le bon document a generer soi-meme.

Usage :
    python3 devis.py --check                  # verifie les prerequis, n'ecrit rien
    python3 devis.py devis-2026-001.json      # genere le devis
    python3 devis.py devis-2026-001.json --outdir dossier/

Entree (JSON) :
{
  "emetteur": {"nom": "...", "adresse": "...", "siret": "...",
               "email": "", "telephone": "", "tva_intra": "", "iban": "", "bic": "",
               "logo": ""},          # optionnel : chemin png/jpg/svg, embarque en base64
  "client":   {"nom": "...", "adresse": "", "siret": ""},
  "numero":   "2026-001",
  "date":     "2026-08-31",          # ISO ; affichee 31/08/2026
  "validite_jours": 30,              # optionnel, defaut 30 (fin de validite calculee)
  "tva_taux": 20,                    # 0 => mention art. 293 B du CGI
  "lignes":   [{"description": "...", "quantite": 1, "prix_unitaire": 450.0}],
  "conditions": "",                  # optionnel : acompte, delais, modalites...
  "notes":    "",                    # optionnel
  "couleur":  "#6855F8",             # optionnel, accent du document
  "pied_de_page": ""                 # optionnel : assurance, qualifications, mentions
}

Apparence : seuls `logo`, `couleur` et `pied_de_page` sont a regler. Le reste du
gabarit ne se modifie pas a la main -- un devis se juge sur sa lisibilite, pas sur
sa decoration, et toucher au gabarit c'est risquer la mise en page a l'impression.

Sortie : devis-{numero}.pdf + devis-{numero}.html
Exit : 0 si OK, 1 si le JSON est invalide (toutes les erreurs listees d'un coup).
"""

import base64
import json
import platform
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CENT = Decimal("0.01")

# ---------------------------------------------------------------------------
# Moteur PDF : n'importe quel navigateur Chromium fait l'affaire, en headless.
# Edge est preinstalle sur TOUT Windows 10/11 -> la plupart des gens n'ont
# rien a installer. On cherche dans le PATH puis aux emplacements connus.
# ---------------------------------------------------------------------------
PDF_ENGINES = [
    ("msedge", "Microsoft Edge"),
    ("google-chrome", "Google Chrome"),
    ("google-chrome-stable", "Google Chrome"),
    ("chromium", "Chromium"),
    ("chromium-browser", "Chromium"),
    ("brave-browser", "Brave"),
    ("chrome", "Google Chrome"),
]

PDF_PATHS = [
    # Windows — Edge est la par defaut sur toutes les machines recentes
    (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "Microsoft Edge"),
    (r"C:\Program Files\Microsoft\Edge\Application\msedge.exe", "Microsoft Edge"),
    (r"C:\Program Files\Google\Chrome\Application\chrome.exe", "Google Chrome"),
    (r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "Google Chrome"),
    # macOS
    ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "Google Chrome"),
    ("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge", "Microsoft Edge"),
    ("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser", "Brave"),
    ("/Applications/Chromium.app/Contents/MacOS/Chromium", "Chromium"),
]


def find_pdf_engine():
    """Renvoie (chemin, nom lisible) du premier navigateur trouve, ou (None, None)."""
    for binaire, nom in PDF_ENGINES:
        exe = shutil.which(binaire)
        if exe:
            return exe, nom
    for chemin, nom in PDF_PATHS:
        if Path(chemin).exists():
            return chemin, nom
    return None, None


def check() -> int:
    """Rapporte l'etat de la machine. NE PRESCRIT RIEN.

    Ce script ne connait pas la machine de l'utilisateur : distribution, gestionnaire
    de paquets, droits admin, VPS ou poste local, tout cela varie. Ecrire ici une
    commande d'installation en dur reviendrait a deviner. On rapporte donc des FAITS,
    et c'est la session Claude de l'utilisateur -- qui, elle, connait son contexte --
    qui decide quoi installer et comment.
    """
    print("/devis — etat de la machine\n")

    print("  Systeme")
    print(f"    plateforme     {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"    python3        {platform.python_version()}  ->  {sys.executable}")

    print("\n  Ce dont le skill a besoin")
    print("    python3        INDISPENSABLE — il calcule les totaux du devis")
    print("                   present (c'est lui qui execute ce message)")

    exe, nom = find_pdf_engine()
    print("    navigateur     OPTIONNEL — il transforme le devis en PDF")
    if exe:
        print(f"                   present : {nom}  ->  {exe}")
    else:
        print("                   absent : aucun navigateur Chromium trouve")
        print("                   (cherche dans le PATH et aux emplacements usuels)")
        print("                   Sans lui, le devis sort en HTML et s'imprime en PDF")
        print("                   par Ctrl+P. Le rendu est identique.")

    print("\n  Verdict")
    if exe:
        print("    Tout est la. Le devis sortira directement en PDF.")
    else:
        print("    Rien ne bloque : /devis fonctionne, sortie HTML.")
        print("    Un navigateur Chromium ajouterait le PDF automatique.")
    return 0


# ---------------------------------------------------------------------------
# Mise en forme
# ---------------------------------------------------------------------------
def num(value: Decimal) -> str:
    """Decimal -> texte francais sans zeros inutiles NI notation scientifique.
    Le separateur decimal est la VIRGULE : le devis part chez un client francais,
    un taux affiche "5.5 %" fait amateur.
    (Piege : Decimal('20').normalize() s'affiche '2E+1', d'ou le format 'f'.)"""
    txt = format(value, "f")
    if "." in txt:
        txt = txt.rstrip("0").rstrip(".")
    return txt.replace(".", ",")


def eur(value: Decimal) -> str:
    """1234.5 -> '1 234,50 €' (format francais, espace insecable)."""
    txt = f"{value:,.2f}".replace(",", " ").replace(".", ",")
    return f"{txt} €"


def fr_date(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%d/%m/%Y")


def load(path: Path):
    """Charge et valide le JSON. Retourne (data, erreurs) ; erreurs = liste FR."""
    errors = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"fichier introuvable : {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"JSON invalide ({exc.lineno}:{exc.colno}) : {exc.msg}"]

    emetteur = data.get("emetteur") or {}
    client = data.get("client") or {}
    for champ in ("nom", "adresse", "siret"):
        if not str(emetteur.get(champ, "")).strip():
            errors.append(f"emetteur.{champ} manquant (obligatoire sur un devis)")
    if not str(client.get("nom", "")).strip():
        errors.append("client.nom manquant")
    if not str(data.get("numero", "")).strip():
        errors.append("numero manquant (ex. \"2026-001\")")

    if data.get("date"):
        try:
            date.fromisoformat(str(data["date"]))
        except ValueError:
            errors.append(f"date invalide : \"{data['date']}\" (attendu AAAA-MM-JJ)")
    else:
        errors.append("date manquante (AAAA-MM-JJ)")

    try:
        vj = int(data.get("validite_jours", 30))
        if vj <= 0:
            errors.append(f"validite_jours doit etre positif : {vj}")
    except Exception:
        errors.append(f"validite_jours invalide : \"{data.get('validite_jours')}\"")

    lignes = data.get("lignes") or []
    if not lignes:
        errors.append("lignes vide : il faut au moins une prestation")
    for i, ligne in enumerate(lignes, 1):
        if not str(ligne.get("description", "")).strip():
            errors.append(f"lignes[{i}].description manquante")
        for champ in ("quantite", "prix_unitaire"):
            try:
                Decimal(str(ligne.get(champ)))
            except Exception:
                errors.append(f"lignes[{i}].{champ} invalide : \"{ligne.get(champ)}\"")

    try:
        taux = Decimal(str(data.get("tva_taux", 0)))
        if taux < 0 or taux > 100:
            errors.append(f"tva_taux hors bornes : {taux}")
    except Exception:
        errors.append(f"tva_taux invalide : \"{data.get('tva_taux')}\"")

    return data, errors


def compute(data):
    """Tous les calculs d'argent vivent ici, et nulle part ailleurs."""
    lignes = []
    total_ht = Decimal("0")
    for ligne in data["lignes"]:
        qte = Decimal(str(ligne["quantite"]))
        pu = Decimal(str(ligne["prix_unitaire"]))
        montant = (qte * pu).quantize(CENT, rounding=ROUND_HALF_UP)
        total_ht += montant
        lignes.append({"description": ligne["description"], "quantite": qte,
                       "prix_unitaire": pu, "montant": montant})
    taux = Decimal(str(data.get("tva_taux", 0)))
    tva = (total_ht * taux / 100).quantize(CENT, rounding=ROUND_HALF_UP)
    return lignes, total_ht, taux, tva, total_ht + tva


def logo_data_uri(chemin, base: Path):
    """Embarque le logo dans le HTML en base64.

    Pourquoi embarquer plutot que pointer le fichier : le navigateur headless
    imprime depuis un contexte ou un chemin relatif ne veut plus rien dire, et un
    devis envoye par mail doit rester complet une fois le HTML detache du disque.
    Jamais bloquant : logo introuvable ou illisible -> devis sans logo.
    """
    if not chemin:
        return None
    p = Path(chemin).expanduser()
    if not p.is_absolute():
        p = (base / p).resolve()
    if not p.is_file():
        return None
    mimes = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}
    mime = mimes.get(p.suffix.lower())
    if not mime:
        return None
    try:
        donnees = p.read_bytes()
    except OSError:
        return None
    if len(donnees) > 2_000_000:      # un logo de 2 Mo est une photo, pas un logo
        return None
    return f"data:{mime};base64,{base64.b64encode(donnees).decode('ascii')}"


def render(data, lignes, total_ht, taux, tva, ttc, base: Path = Path(".")) -> str:
    emetteur, client = data["emetteur"], data["client"]
    couleur = data.get("couleur", "#6855F8")
    logo = logo_data_uri(emetteur.get("logo"), base)
    logo_html = (f'<img class="logo" src="{logo}" alt="">' if logo else "")
    pied = data.get("pied_de_page") or emetteur.get("pied_de_page") or ""
    fin_validite = (
        date.fromisoformat(data["date"])
        + timedelta(days=int(data.get("validite_jours", 30)))
    ).isoformat()

    def bloc(entite):
        extra = [entite.get(k, "") for k in ("email", "telephone")]
        parts = [entite["nom"], entite.get("adresse", "")]
        if entite.get("siret"):
            parts.append(f"SIRET {entite['siret']}")
        if entite.get("tva_intra"):
            parts.append(f"TVA intracom. {entite['tva_intra']}")
        parts += [x for x in extra if x]
        return "<br>".join(p.replace("\n", "<br>") for p in parts if p)

    rows = "".join(
        f"<tr><td>{l['description']}</td>"
        f"<td class='num'>{num(l['quantite'])}</td>"
        f"<td class='num'>{eur(l['prix_unitaire'])}</td>"
        f"<td class='num'>{eur(l['montant'])}</td></tr>"
        for l in lignes
    )
    if taux == 0:
        tva_rows = ("<tr><td colspan='3' class='mention'>TVA non applicable, "
                    "art. 293 B du CGI</td><td class='num'></td></tr>")
    else:
        tva_rows = (f"<tr><td colspan='3'>TVA ({num(taux)} %)</td>"
                    f"<td class='num'>{eur(tva)}</td></tr>")

    conditions = ""
    if data.get("conditions"):
        conditions = f"<p><strong>Conditions :</strong> {data['conditions']}</p>"
    if emetteur.get("iban"):
        bic = f" · BIC {emetteur['bic']}" if emetteur.get("bic") else ""
        conditions += (f"<p><strong>Reglement par virement :</strong> "
                       f"IBAN {emetteur['iban']}{bic}</p>")
    notes = f"<p>{data['notes']}</p>" if data.get("notes") else ""

    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>Devis {data['numero']}</title>
<style>
  @page {{ size: A4; margin: 18mm; }}
  body {{ font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
         color: #1a1a1a; max-width: 720px; margin: 2rem auto; padding: 0 1rem;
         font-size: 14px; line-height: 1.5; }}
  header {{ display: flex; justify-content: space-between; align-items: flex-start;
            border-bottom: 3px solid {couleur}; padding-bottom: 1rem; }}
  h1 {{ color: {couleur}; font-size: 1.6rem; margin: 0; }}
  .logo {{ max-height: 56px; max-width: 220px; display: block; margin-bottom: .5rem; }}
  .meta {{ text-align: right; }}
  .parties {{ display: flex; justify-content: space-between; gap: 2rem; margin: 1.5rem 0; }}
  .parties h2 {{ font-size: .8rem; text-transform: uppercase; letter-spacing: .05em;
                 color: {couleur}; margin: 0 0 .3rem; }}
  table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
  th {{ background: {couleur}; color: #fff; text-align: left; padding: .5rem .6rem; }}
  td {{ border-bottom: 1px solid #e5e5e5; padding: .5rem .6rem; vertical-align: top; }}
  .num {{ text-align: right; white-space: nowrap; }}
  .totaux td {{ border: none; }}
  .ttc td {{ font-weight: 700; font-size: 1.05rem; border-top: 2px solid {couleur}; }}
  .mention {{ font-style: italic; color: #555; }}
  .accord {{ display: flex; gap: 2rem; margin-top: 2rem; }}
  .accord > div {{ flex: 1; border: 1px solid #d5d5d5; border-radius: 6px;
                   padding: .8rem; min-height: 110px; font-size: .85rem; color: #444; }}
  footer {{ margin-top: 2rem; font-size: .75rem; color: #666;
            border-top: 1px solid #e5e5e5; padding-top: .8rem; }}

  /* Impression. CE BLOC DOIT RESTER EN DERNIER : une media query n'ajoute aucune
     specificite, donc place plus haut il serait annule par les regles ci-dessus.
     Sans lui, le body garde margin:2rem + max-width:720px (~190 mm) alors que la
     zone utile d'une A4 a 18 mm de marge n'en fait que 174 : le devis debordait
     sur une 2e page. Trouve sur un devis reel de 7 lignes, le 2026-08-31. */
  @media print {{
    body {{ margin: 0; max-width: none; padding: 0; font-size: 13px; }}
    .logo {{ max-height: 46px; }}
    header {{ padding-bottom: .7rem; }}
    .parties {{ margin: 1rem 0; }}
    table {{ margin: .7rem 0; }}
    th, td {{ padding: .35rem .5rem; }}
    .accord {{ margin-top: 1.2rem; }}
    .accord > div {{ min-height: 90px; }}
    footer {{ margin-top: 1.2rem; padding-top: .6rem; }}
    tr, .accord {{ break-inside: avoid; }}
  }}
</style></head><body>
<header>
  <div>{logo_html}<h1>DEVIS</h1><div>N° {data['numero']}</div></div>
  <div class="meta">Date d'émission : <strong>{fr_date(data['date'])}</strong><br>
       Valable jusqu'au : <strong>{fr_date(fin_validite)}</strong></div>
</header>
<div class="parties">
  <div><h2>Émetteur</h2>{bloc(emetteur)}</div>
  <div><h2>Adressé à</h2>{bloc(client)}</div>
</div>
<table>
  <thead><tr><th>Prestation</th><th class="num">Qté</th>
             <th class="num">PU HT</th><th class="num">Montant HT</th></tr></thead>
  <tbody>{rows}</tbody>
  <tbody class="totaux">
    <tr><td colspan="3">Total HT</td><td class="num">{eur(total_ht)}</td></tr>
    {tva_rows}
    <tr class="ttc"><td colspan="3">Total TTC</td><td class="num">{eur(ttc)}</td></tr>
  </tbody>
</table>
{conditions}{notes}
<div class="accord">
  <div><strong>Bon pour accord</strong><br>
       Date, signature et mention « Bon pour accord » :</div>
  <div><strong>Cachet / nom du signataire</strong></div>
</div>
<footer>
  Devis gratuit, valable jusqu'au {fr_date(fin_validite)}. L'acceptation du devis
  (mention « Bon pour accord », date et signature) vaut commande aux conditions ci-dessus.
  {pied}
</footer>
</body></html>
"""


def make_pdf(html_path: Path):
    """HTML -> PDF via un navigateur headless.

    Renvoie (chemin, nom du moteur, erreur). `erreur` est None en cas de succes ;
    sinon elle DIT ce qui s'est passe. Distinguer "aucun navigateur" de "le
    navigateur a echoue" n'est pas cosmetique : la premiere version renvoyait
    (None, None) dans les deux cas, et le message annoncait un navigateur absent
    alors qu'Edge etait bien la et refusait d'ecrire. Un message d'erreur qui
    designe la mauvaise cause coute plus cher que pas de message du tout.
    """
    exe, nom = find_pdf_engine()
    if not exe:
        return None, None, "aucun navigateur trouve"

    # resolve() est OBLIGATOIRE : le navigateur headless resout un chemin relatif
    # depuis SON repertoire de travail, pas le notre. Un chemin relatif marche par
    # accident quand les deux coincident, et echoue en "Acces refuse" sinon.
    pdf_path = html_path.with_suffix(".pdf").resolve()
    cmd = [exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()]
    try:
        subprocess.run(cmd, capture_output=True, timeout=90, check=True)
    except subprocess.TimeoutExpired:
        return None, nom, f"{nom} n'a pas repondu en 90 s"
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or b"").decode("utf-8", "replace").strip().splitlines()
        raison = detail[-1][:160] if detail else f"code de sortie {exc.returncode}"
        return None, nom, f"{nom} a echoue : {raison}"
    except OSError as exc:
        return None, nom, f"{nom} n'a pas pu etre lance : {exc}"
    if not pdf_path.exists():
        return None, nom, f"{nom} s'est termine sans ecrire le fichier"
    return pdf_path, nom, None


def verify_pdf(pdf_path: Path):
    """Le script relit son propre PDF. Renvoie (ok: bool, message).

    On ne se contente PAS de "le fichier existe" : un PDF tronque ou vide existe
    aussi. On verifie la signature, la taille, et le nombre de pages.
    """
    if not pdf_path.exists():
        return False, "le fichier PDF n'a pas ete cree"
    blob = pdf_path.read_bytes()
    taille = len(blob)
    if not blob.startswith(b"%PDF-"):
        return False, f"ce n'est pas un PDF valide (signature absente, {taille} octets)"
    if taille < 1000:
        return False, f"PDF anormalement petit ({taille} octets), probablement tronque"
    pages = len(re.findall(rb"/Type\s*/Page[^s]", blob))
    if pages == 0:
        trouve = re.search(rb"/Count\s+(\d+)", blob)
        pages = int(trouve.group(1)) if trouve else 0
    if pages == 0:
        return False, "PDF sans page lisible"
    ko = round(taille / 1024)
    # Seuil a 1 et non a 2 : un devis courant tient sur une page, et la 2e page
    # est justement le symptome du debordement de mise en page corrige plus haut.
    # Un seuil a 2 laissait passer le defaut en silence (constate le 2026-08-31).
    if pages > 1:
        return True, (f"{pages} pages, {ko} Ko — ATTENTION, un devis de cette taille "
                      f"tient normalement sur 1 page : regarde s'il ne deborde pas")
    return True, f"{pages} page, {ko} Ko"


def main() -> int:
    argv = sys.argv[1:]
    if "--check" in argv:
        return check()

    args = [a for a in argv if not a.startswith("--")]
    outdir = Path(".")
    if "--outdir" in argv:
        idx = argv.index("--outdir")
        outdir = Path(argv[idx + 1])
        args = [a for a in args if a != argv[idx + 1]]
    if len(args) != 1:
        print(__doc__)
        return 1

    data, errors = load(Path(args[0]))
    if errors or data is None:
        print("Devis NON genere. Corrige d'abord ceci, puis relance :")
        for err in errors:
            print(f"   - {err}")
        print("\n(Le script refuse de generer plutot que d'inventer une valeur.)")
        return 1

    lignes, total_ht, taux, tva, ttc = compute(data)
    slug = str(data["numero"]).replace("/", "-").replace(" ", "-")
    outdir.mkdir(parents=True, exist_ok=True)
    html_path = outdir / f"devis-{slug}.html"
    html_path.write_text(
        render(data, lignes, total_ht, taux, tva, ttc, base=Path(args[0]).resolve().parent),
        encoding="utf-8")

    print(f"Total HT  : {eur(total_ht)}")
    if taux == 0:
        print("TVA       : non applicable, art. 293 B du CGI")
    else:
        print(f"TVA ({num(taux)} %) : {eur(tva)}")
    print(f"Total TTC : {eur(ttc)}")
    print("(calcules par ce script, en Decimal, au centime — pas par le modele)\n")

    pdf_path, moteur, erreur = make_pdf(html_path)
    if pdf_path:
        ok, detail = verify_pdf(pdf_path)
        if ok:
            print(f"PDF  : {pdf_path}   [verifie : {detail}, via {moteur}]")
            print(f"HTML : {html_path}")
        else:
            print(f"PDF  : PROBLEME — {detail}")
            print(f"HTML : {html_path}  <- utilise celui-ci, Ctrl+P -> Enregistrer en PDF")
            return 1
    else:
        print(f"HTML : {html_path}")
        print(f"PDF  : non genere — {erreur}.")
        print("       Ouvre le HTML et fais Ctrl+P -> \"Enregistrer en PDF\" "
              "(rendu identique).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
