---
name: devis
description: "Utilise CE skill DÈS QUE l'utilisateur veut chiffrer une prestation : il dit « fais-moi un devis », « devis pour {client} », « chiffre-moi cette mission », « prépare la proposition de prix », liste des prestations avec des montants, ou doit envoyer un prix à un prospect, même sans demande explicite. Au premier lancement il pose quelques questions pour apprendre l'entreprise et les tarifs de l'utilisateur, puis génère un devis PDF dont TOUS les calculs sont faits par scripts/devis.py : le modèle ne fait jamais l'arithmétique d'un devis."
allowed-tools: Bash(python3 *), Read, Write
---

# /devis : une mission décrite → un devis PDF, calculé au centime

**Entrée** : ce qu'il y a à chiffrer, dit avec les mots de l'utilisateur (« 3 jours
d'automatisation à 450 € et une demi-journée de formation, pour ACME, acompte 30 % »).
**Sortie** : un devis PDF avec numéro, validité, TVA, conditions et bloc « Bon pour accord ».

Deux choses le distinguent : **les totaux sont calculés par un script Python**, jamais par le
modèle — et **il apprend l'entreprise de l'utilisateur une fois pour toutes**, au premier
lancement.

> Pourquoi un devis et pas une facture ? La réforme de la facturation électronique (réception
> obligatoire en septembre 2026, émission en septembre 2027) impose une plateforme agréée pour
> les factures B2B. Le devis, lui, reste libre : c'est LE document à générer soi-même.

## Étape 1. Vérifier les prérequis

```bash
python3 scripts/devis.py --check
```

Il vérifie python3 et cherche un navigateur pour fabriquer le PDF (Edge est présent sur tous les
Windows récents, donc en général il n'y a rien à installer). L'absence de navigateur **n'est pas
bloquante** : le devis sort en HTML et l'utilisateur fait Ctrl+P → « Enregistrer en PDF ».

## Étape 2. La fiche entreprise — l'onboarding, une seule fois

Lis `mon-entreprise.json` **dans le dossier de ce skill**.

**S'il n'existe pas**, c'est le premier lancement : annonce qu'on va le configurer en quelques
questions, une fois pour toutes, puis pose-les **une par une** (pas un formulaire d'un bloc) :

1. Le nom ou la raison sociale, tel qu'il doit apparaître sur le devis.
2. L'adresse.
3. Le SIRET.
4. L'email (et le téléphone, s'il veut le faire figurer).
5. La TVA : **franchise en base** (le cas de la plupart des micro-entrepreneurs — le devis
   portera « TVA non applicable, art. 293 B du CGI ») ou **assujetti** (en général 20 %) ?
6. **Ses prestations habituelles et leurs prix**, avec ses mots, en vrac. C'est la question qui
   fait gagner le plus de temps ensuite.
7. L'IBAN et le BIC, s'il veut que le devis affiche les modalités de règlement (facultatif).

**Ne JAMAIS inventer un SIRET, un IBAN ou un taux de TVA.** Si l'information manque, demande-la.

**Si l'utilisateur ne sait pas quoi facturer** — c'est fréquent, et c'est le moment d'aider —
propose ces ordres de grandeur du marché français 2026, en disant que ce sont des repères à
ajuster, pas des tarifs :

| Prestation | Repère | D'où il sort |
|---|---|---|
| Journée d'automatisation | 650 € | TJM médian « Automatisation IA », 660 €/j |
| Journée d'audit / conseil IA | 750 € | TJM médian « Consultant IA » |
| Forfait d'installation (audit + 1ʳᵉ automatisation + connecteurs) | 2 500 € | build freelance : 1 500 à 4 500 € |
| Formation, demi-journée | 450 € | — |
| Maintenance mensuelle, périmètre borné | 600 €/mois | retainer solo/TPE : 400 à 800 €/mois |

Et dis-lui la chose que personne ne lui dira : **le risque n'est pas de vendre trop cher, c'est
de sous-tarifer la maintenance.** Si le forfait mensuel inclut un point hebdomadaire, descendre
sous 1 000 €/mois fait travailler à perte. Borner le périmètre (« 4 interventions incluses »)
est ce qui évite le travail qui gonfle sans que le prix bouge.

Écris ensuite `mon-entreprise.json` :

```json
{
  "nom": "", "adresse": "", "siret": "", "email": "",
  "telephone": "", "tva_intra": "", "iban": "", "bic": "",
  "tva_taux_defaut": 0,
  "prestations_frequentes": [{"description": "", "prix_unitaire": 0}]
}
```

**S'il existe déjà**, ne repose aucune de ces questions : va directement à l'étape 3. Quand une
prestation nouvelle revient une deuxième fois, propose **une fois** de l'ajouter à la liste.
L'utilisateur peut ouvrir ce fichier et le corriger à la main ; s'il demande « oublie mes
infos », supprime-le et dis-le.

## Étape 3. Les informations du devis

Demande ce qui manque, propose des valeurs sensées :

- **Client** : nom, adresse, SIRET si c'est un professionnel.
- **Lignes** : description, quantité, prix unitaire HT — pioche dans `prestations_frequentes`
  dès que ça colle (« ta demi-journée de formation habituelle à 450 € ? »).
- **Numéro** : `AAAA-NNN`, en incrémentant le plus grand `devis-*.json` du dossier courant.
- **Validité** : 30 jours par défaut. **Conditions** : acompte, délais (facultatif).

Écris `devis-{numero}.json` dans le dossier courant, en recopiant `emetteur` depuis
`mon-entreprise.json` et `tva_taux` depuis `tva_taux_defaut`. Le format exact est documenté en
tête de `scripts/devis.py`.

## Étape 4. Générer — le script calcule, pas toi

```bash
python3 scripts/devis.py devis-{numero}.json
```

**Tu ne calcules JAMAIS un total, une TVA ou un arrondi**, ni dans la conversation, ni en
retouchant le HTML. Un montant à corriger = corriger le JSON et relancer. Si le script sort en
erreur, il liste les champs à corriger : corrige-les et relance. **Recopie ses montants tels
qu'il les affiche.**

## Étape 5. Relire le PDF avant de le livrer

Le script vérifie déjà son PDF (signature, taille, nombre de pages) et le dit dans sa sortie.
Fais la vérification qu'il ne peut pas faire : **ouvre le PDF avec l'outil Read et regarde-le.**

Contrôle en le regardant : les deux blocs émetteur / client sont remplis, aucune ligne n'est
tronquée, les totaux affichés sont bien ceux du script, la mention de TVA correspond au régime,
le bloc « Bon pour accord » est présent, et le devis tient sur une page. Si quelque chose cloche,
corrige le JSON et relance — jamais le HTML à la main.

Annonce alors : le fichier produit, le Total HT et TTC **tels que le script les a affichés**, la
date de fin de validité. C'est le bon moment pour proposer d'enrichir la fiche entreprise.

## Handoff

Produit `devis-{numero}.json` (la source), `devis-{numero}.pdf` et `devis-{numero}.html`.
Les devis passés sont des fichiers JSON : ils se recyclent.

**Prochaine étape** : relance `/devis` pour le suivant, la numérotation s'incrémente seule.
Devis accepté ? La facture part dans un outil de facturation agréé, pas dans un fichier maison.
