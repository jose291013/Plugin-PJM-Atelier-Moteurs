# Atelier Moteurs PJM — application de cahier des charges

Une app (artifact) par client, créée par le skill `creer-atelier-pjm` ; privée, à partager en Éditeur depuis le menu Partager.

## Rôle
L'administrateur PJM crée une « fiche moteur » : type de produit (brochure, flyer, grand format, cartes),
questions du formulaire, machines/procédés par choix, papiers, finitions, délais, prix.
Statut « Prêt à construire » → Claude lit la fiche (ArtifactData, collection `briefs`) et construit le moteur dans PJM via Claude in Chrome.

## Base de données de l'app
- `briefs/<id>` : une fiche (name, productType, status, pjmCategory, description, quantityComponent, multiQty,
  priceMin/Max, components[], delays{}, margin{}, notes).
- `catalog/resources` : ressources de production PJM + procédés (lu par le skill `lire-catalogue-pjm`).
- `catalog/materials` : catégories de matériaux, noms détaillés jusqu'à 120 par catégorie.
- `catalog/categories` : catégories de moteurs de produit PJM `[{id, name}]` (≥ 1.6.3), lues par `lire-catalogue-pjm` ; elles remplissent la liste « Catégorie de moteur PJM » de la fiche (liste par défaut tant que le document n'existe pas).
  Écriture réservée aux éditeurs (règle `catalog write admin`). À rafraîchir quand PJM change.

## Structure PJM relevée (moteur « Brochure numerique »)
- Types de produit de l'Atelier (`productType`) : autre (fiche vide sans modèle, seulement Q1 ; type des fiches importées depuis 1.6.3), brochure, flyer, grandformat (bâches, adhésifs, textiles), panneau (panneaux rigides, prix à la plaque, Q1 versions × Q2 ex., Q3 × Q4 mm ; voir `panneau-rigide.md`), cartes. Imposition `plaque` = plaques rigides.
- Moteur : Nom, Catégorie (1-Calendriers, 2-Carterie, 3-Dépliant, 4-Enveloppes, 5-Flyers / poster, 6-Grand format,
  7-Livres et magazine, Textile), Description, Définition du calcul de quantité (Sélectionnez la quantité, quantités multiples),
  Prix min/max, Intégrations (groupe de prix, Tflow, QuickBooks).
- 4 types de composants (ajout : /ProductEngines/{Quantity|Option|Calculation|Material}/{engineId}) :
  - Quantity (Q1, Q2…) : Nom, Texte pour l'utilisateur.
  - Option : Nom, Texte, Masquer vue publique, Forcer une sélection ; liste d'options (Nom, Ajustement global %),
    chaque option a Matériaux, Production (de/jusqu'à quantité, Étape de production = ressource/procédé,
    calcul quantité processus, calcul poses, position rapport, instructions) et Attributs.
  - Material : Nom, Texte, Instruction, mode (matériaux spécifiques / toute la catégorie / même largeur-hauteur),
    calcul quantité matériel, calcul poses, calcul poids.
  - Calculation : comme une option unique toujours appliquée (Matériaux, Production, Attributs).
  - Tous : « Composants des suppressions » (masquer si composant X = valeur).
- Ex. production option « Quadri recto-verso » : Couleur recto - verso, quantité `floor(ceiling(((Q2-4)/Nup())*Q1))`,
  poses `CalcNup(Q3,Q4,450,320,6)`. Massicot : Guillotina de revistas, quantité `Q1`.

## Bases de calcul de la fiche → formules NCalc
- feuilles : Ceiling(exemplaires × unités / Nup()) selon imposition (à plat, brochure4 = blocs de 4 p., feuillets).
- exemplaires : Q1 · pages : Q1*Q2 · cahiers : Q1*Ceiling(Q2/4.0) · m² : Q1*Q2*Q3/10000 (cm) · ml : périmètre ou côté selon note · forfait : 1.
- custom : formule saisie ou note.
- Formats de feuille multiples → une ligne Matériel par format avec comparaison de surface (voir formules-brochure-pjm.md).

## Délais
Onglet « Délais & prix » : liste de délais avec marge (défaut J+5 0 %, J+3 15 %, J+1 25 %) → composant Option « Délais de production » dans PJM (Markup par choix). JSON : `leadTimes`.

## Langues (V1)
- Sélecteur FR / ES / EN en haut à droite. Ordre de priorité : choix personnel de l'utilisateur (mémorisé) > langue par défaut fixée par un admin (écran admin, doc `settings/app.defaultLang`, écriture réservée aux éditeurs) > langue du navigateur (ES/EN/FR, sinon EN).
- Toute l'interface suit le sélecteur. Les fiches sont créées dans la langue du sélecteur (`briefs.language`), y compris les textes des modèles et les délais (J+ en FR, D+ en ES/EN).
- Le moteur PJM est construit dans la langue de la fiche (`engine.language` du JSON). Si la langue du sélecteur diffère, un bandeau propose « Traduire la fiche » (Claude traduit noms, textes client, choix, délais, notes ; les noms PJM des machines, procédés et papiers ne sont pas traduits ; les conditions de masquage sont mises à jour).
- La langue de la fiche est aussi modifiable dans l'onglet Produit.

## Onglet « Règles & incompatibilités » (version du 16/10/2026)
1. Questions guidées : banque `questions/<id>` (écriture réservée aux éditeurs). Champs : text{fr,es,en}, effect{fr,es,en}, productTypes (["*"] = tous),
   answerType (yesno, number, size, materials, text), unit, showIf (mots séparés par « | » cherchés dans les noms de la fiche), order, active.
   14 questions de départ (copie dans pjm-ncalc/atelier/questions). Réponses dans `briefs.guided[qid]`, JSON `guidedAnswers`.
2. Règles en une phrase : `briefs.freeRules[]` {text, understood, effects, unclear, status}. Reformulation par Claude dans l'appli (capacité sample), validation par l'utilisateur.
   Bouton « Proposer comme question guidée » → `suggestions/<id>`, acceptées ou refusées par un admin.
3. Mode expert (replié) : grille des incompatibilités (hideWhen / restrictions).
- Écran admin « Questions guidées (admin) » visible pour les éditeurs de l'appli : édition des questions, des traductions et des propositions.

## V1 – mise à jour, import, tests (16/10/2026)
- Statuts ajoutés : « À mettre à jour dans PJM » (maj) et « À importer depuis PJM » (import).
- Onglet Produit → carte « Lien avec PJM » : moteur, dates, éléments reliés, boutons « Demander la mise à jour » et « Réimporter depuis PJM ».
- Nouvelle fiche → « Importer un moteur PJM existant » (adresse /ProductEngines/Edit/{id}).
- Écran admin → « Adresse du PJM du client » (`settings/app.pjmUrl`) ; avertissement si absente.
- Récapitulatif → « Cas de test » : quantités, choix, prix attendu, dernier résultat écrit par Claude.
- Correctif : les modèles Flyer et Cartes plantaient (mot « Papier » manquant dans les modèles traduits).

## Écrire une fiche depuis Claude (validé 20/10/2026)
- Toujours écrire `updatedBy: "claude"` et un `updatedAt` neuf : sinon un Atelier déjà ouvert (version ≤ 1.6.1) prend la mise à jour pour son propre écho, garde l'ancienne fiche et l'écrase à la prochaine modification.
- Après l'écriture, demander à l'utilisateur de recharger l'Atelier s'il était ouvert ; relire la fiche (version, `updatedAt`) avant toute nouvelle écriture.
- Questions guidées sur les finitions : demander ce qui est **impossible** (incompatibilités), jamais ce qui est possible.

## Fiche vide (création par import)
```json
{"name":"","productType":"autre","status":"import","pjmCategory":"","description":"","language":"fr","priceMin":"","priceMax":"","quantityComponent":"Q1","multiQty":false,"components":[],"delays":{"enabled":false,"name":"Délais de production","userText":"","choices":[],"notes":""},"restrictions":[],"rulesNotes":"","guided":{},"freeRules":[],"tests":[],"margin":{"pricingGroup":"","notes":""},"notes":"","pjm":{"engineId":"","url":""},"createdAt":"ISO","updatedAt":"ISO","schema":1}
```
Composants : quantity {id,type,code,name,userText,unit,min,max,def,hideWhen[]} ; option {id,type,name,userText,forceSelect,hidePublic,options:[{id,name,adjust,steps:[{id,resource,process,basis,formula,note}],materials:[]}],hideWhen[]} ; material {id,type,name,userText,hidePublic,mode,category,materials[],sheetFormats[{w,h}],bleed,sides,imposition,hideWhen[]} ; calculation {id,type,name,userText,steps[],hideWhen[]}. hideWhen = [{component: id local, value: nom du choix}].
