---
name: devis
description: "Utilise CE skill DÈS QUE l'utilisateur veut chiffrer une prestation : il dit « fais-moi un devis », « devis pour {client} », « chiffre-moi cette mission », « prépare la proposition de prix », liste des prestations avec des montants, ou doit envoyer un prix à un prospect, même sans demande explicite. Au premier lancement il pose quelques questions pour apprendre l'entreprise et les tarifs de l'utilisateur, puis génère un devis PDF dont TOUS les calculs sont faits par scripts/devis.py : le modèle ne fait jamais l'arithmétique d'un devis."
allowed-tools: Bash(python3 *), Read, Write
---

# /devis : une mission décrite → un devis PDF, calculé au centime

**Entrée** : ce qu'il y a à chiffrer, dit avec les mots de l'utilisateur — « un poêle Godin
posé, avec le tubage et la mise en service, pour les Martin » aussi bien que « 3 jours
d'intervention à 450 € et une demi-journée de formation, pour ACME, acompte 30 % ».
**Sortie** : un devis PDF avec numéro, validité, TVA, conditions et bloc « Bon pour accord ».

Deux choses le distinguent : **les totaux sont calculés par un script Python**, jamais par le
modèle — et **il apprend l'entreprise de l'utilisateur une fois pour toutes**, au premier
lancement.

> Pourquoi un devis et pas une facture ? La réforme de la facturation électronique (réception
> obligatoire en septembre 2026, émission en septembre 2027) impose une plateforme agréée pour
> les factures B2B. Le devis, lui, reste libre : c'est LE document à générer soi-même.

## Étape 1. Regarder la machine

```bash
python3 scripts/devis.py --check
```

Il **rapporte des faits** — plateforme, python3, présence d'un navigateur pour fabriquer le PDF.
Il ne prescrit aucune commande d'installation, et c'est voulu : il ne connaît pas cette machine.

**C'est toi qui raisonnes.** L'absence de navigateur n'est jamais bloquante : le devis sort en
HTML et s'imprime en PDF par Ctrl+P, rendu identique. Si l'utilisateur veut le PDF automatique,
propose la voie d'installation adaptée à *sa* machine, d'après le rapport et ce que tu sais déjà
de son environnement — et n'installe rien sans son accord.

## Étape 2. Comprendre son activité — une seule fois

Lis `mon-entreprise.json` **dans le dossier de ce skill**. **S'il existe**, ne repose aucune
question : va à l'étape 3.

**S'il n'existe pas**, c'est le premier lancement. Avant tout, une règle :

> 🔴 **Ne présume JAMAIS ce que cette personne vend.** Ce skill sert un artisan qui installe des
> poêles à bois aussi bien qu'un consultant qui facture des journées. Un plombier, un
> photographe, un traiteur, un formateur, une agence : ils n'ont ni les mêmes lignes, ni les
> mêmes unités, ni les mêmes taux de TVA. Un devis pré-rempli avec le vocabulaire d'un autre
> métier est pire qu'un devis vide.

**Commence donc par savoir à qui tu parles.** Sers-toi d'abord de ce que tu as déjà : le
`CLAUDE.md` du projet, l'historique de la conversation, ce que l'utilisateur t'a dit ailleurs.
Si tu sais déjà quel est son métier, **ne le lui redemande pas** — annonce ce que tu as compris
et fais-le confirmer en une phrase. Sinon, demande-le simplement : « qu'est-ce que vous vendez,
et sous quelle forme ? »

Puis pose le reste **une question à la fois**, en adaptant le vocabulaire à ce qu'il t'a répondu :

1. Le nom ou la raison sociale, tel qu'il doit figurer sur le devis.
2. L'adresse.
3. Le SIRET.
4. L'email, et le téléphone s'il veut le faire figurer.
5. **La TVA.** Demande son cas, ne le devine pas : franchise en base (le devis portera « TVA non
   applicable, art. 293 B du CGI »), ou assujetti — et à quel taux. Les taux réduits existent et
   dépendent de l'activité : un même artisan peut relever de 20 %, 10 % ou 5,5 % selon la nature
   des travaux. S'il hésite, dis-lui de vérifier auprès de son comptable plutôt que de trancher
   à sa place.
6. **Ce qu'il vend habituellement, et à quel prix.** C'est la question qui fait gagner le plus de
   temps ensuite. Laisse-le répondre avec ses mots et ses unités — une journée, une pièce, un
   forfait, un mètre carré, une heure. Reformule ses lignes telles qu'elles apparaîtront.
7. L'IBAN et le BIC, s'il veut afficher les modalités de règlement (facultatif).

**S'il ne sait pas quoi facturer**, aide-le à raisonner sur *son* métier : ce qu'il a facturé la
dernière fois, ce que ça lui coûte, ce que pratiquent ses concurrents directs. **Ne sors pas un
tarif d'un secteur que tu n'as pas confirmé.** Si tu connais réellement des repères pour son
métier, donne-les en disant d'où ils viennent ; sinon, dis franchement que tu n'en as pas et
aide-le à partir de ses propres chiffres.

**N'invente JAMAIS un SIRET, un IBAN ou un taux de TVA.** Ces trois-là se demandent, toujours.

Écris ensuite `mon-entreprise.json` — les descriptions et les prix sont ceux de l'utilisateur,
pas des exemples :

```json
{
  "nom": "", "adresse": "", "siret": "", "email": "",
  "telephone": "", "tva_intra": "", "iban": "", "bic": "",
  "tva_taux_defaut": 0,
  "prestations_frequentes": [{"description": "", "prix_unitaire": 0}]
}
```

Ensuite, quand une ligne nouvelle revient une deuxième fois, propose **une fois** de l'ajouter à
`prestations_frequentes`. L'utilisateur peut ouvrir ce fichier et le corriger à la main ; s'il
demande « oublie mes infos », supprime-le et dis-le.

## Étape 3. Les informations du devis

Demande ce qui manque, propose des valeurs sensées :

- **Client** : nom, adresse, SIRET si c'est un professionnel (un particulier n'en a pas).
- **Lignes** : description, quantité, prix unitaire HT — pioche dans `prestations_frequentes`
  dès qu'une ligne y ressemble, en la citant telle qu'il l'a formulée (« ta pose de tubage
  habituelle à 340 € ? »). La quantité porte l'unité de son métier : des jours, des pièces, des
  mètres, des heures. Mets l'unité dans la description si ce n'est pas évident.
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
