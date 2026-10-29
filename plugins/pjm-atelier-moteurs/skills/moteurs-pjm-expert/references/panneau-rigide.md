# Panneaux rigides (productType `panneau`) – validé le 20/10/2026

Moteur de référence : « Panneau PVC » (Imprimerie Démo, ams.printjobmanager.com), modèle de formulaire repris d'un e-store PJM du marché (Forex).

## Formulaire type
| Ordre | Composant | PJM |
|---|---|---|
| 1 | Q1 Nombre de versions (1–50) | Quantity |
| 2 | Q2 Quantité d'exemplaires par version (1–9999) | Quantity |
| 3 | Q3 Petite dimension (mm) | Quantity |
| 4 | Q4 Grande dimension (mm) | Quantity |
| 5 | Épaisseur / matière | Options (forcée), un choix par matière + épaisseur |
| 6 | Impression quadri : Recto / Recto/Verso | Options (forcée) |
| 7 | Découpe : au format (droite) / à la forme | Options (forcée) |
| 8 | Coins arrondis (rayon) : Non, 5…30 mm | Options |
| 9 | Perforation : Non / 4 coins / 2 coins supérieurs | Options |
| 10 | Vérification du fichier : gratuite / mise aux normes / + BAT | Options (forcée) |
| 11 | Emballage | Calculation |
| 12 | Délais de production | Options |
- « Sélectionnez la quantité » (`QuantityDefinition`) = `Q1*Q2` (nombre total de panneaux) ; à vérifier à la première construction, sinon `Q1`.
- Ne jamais proposer œillets, ourlets ou fourreaux : ce sont des finitions de bâche (type `grandformat`).
- Dimensions en mm (dimensions des matériaux PJM en mm aussi) : pas de conversion.

## Composant « Épaisseur » de la fiche → Options PJM
Dans la fiche, c'est un composant `material` avec `imposition: "plaque"` (mode `category` ou `specific`). À la construction :
1. Lire les plaques de la catégorie dans PJM (`/Materials/_Index`, puis `/Materials/Edit/{id}` : Width, Height, WeightPer ; tarif `/Materials/_ListMaterialRanges`). Les plaques sont vendues **à la plaque** (ItemCount 1).
2. Regrouper par matière + épaisseur (ex. « PVC Forex NOIR / 5 / 3050 x 2050 / ft usine » → « Forex 5 mm ») ; montrer le regroupement dans le plan.
3. Créer un composant **Options** forcé avec un choix par groupe, et dans chaque choix **une ligne matériau par format de plaque** (ToQty 999999).
4. Vérifier le prix au m² des formats d'un même groupe : s'il est identique, « moins de surface consommée » = « moins cher » (cas validé). S'il diffère, comparer le coût (surface × prix) au lieu de la surface et le signaler.

## Formules de la plaque la plus économique
Notations : bleed = fond perdu total de la fiche (6 = 3 mm par côté), W × H = format de la plaque en mm.
- Plaques nécessaires `S(W,H)` :
  `Ceiling(Q1*Q2 / Max(Max(floor(CalcNup(Q3,Q4,W,H,bleed)),floor(CalcNup(Q4,Q3,W,H,bleed))),1E-4))`
  - `floor()` autour de `CalcNup` est **obligatoire** : CalcNup renvoie un Decimal et `Q / CalcNup(...)` échoue (« Operator '/' can't be applied to operands of types 'double' and 'decimal' », ErrorCode 448).
  - Les deux sens (Q3×Q4 et Q4×Q3) sont testés.
  - Panneau qui ne tient sur aucune plaque → 1E-4 → quantité énorme : limiter Q3 / Q4 sous la plus grande plaque.
- Surface consommée `A(W,H)` = `S(W,H)*{W*H}` (entier en mm²).
- Ligne de la plaque i : poses (NumberUpExpression) = `A(Wi,Hi)` ; quantité = imbrication `if(A(Wj,Hj) <= Nup(),0, … S(Wi,Hi))` sur toutes les autres plaques j, `<=` pour les plaques plus petites, `<` pour les plus grandes (égalité → plus petite plaque). Une seule ligne non nulle.
- Ordonner les formats par surface croissante avant de générer. Longueur ≈ 770 caractères pour 6 formats (< 1400).
- Poids : laisser « Calcul du poids » vide, PJM prend qty × WeightPer de la plaque (poids des plaques consommées, pas du panneau fini).
- Générer et simuler avec `reprendre-excel-pjm/scripts/ncalc_sim.py` (CalcNup simulé : `floor(W/(w+b))*floor(H/(h+b))`).

## Production
| Étape | Seq | Formule (mm) |
|---|---|---|
| Vérification / mise aux normes (par version) | 1 | `Q1` |
| Impression recto (m²) | 2 | `Q1*Q2*Q3*Q4/1E6` |
| Impression recto/verso (m²) | 2 | `Q1*Q2*Q3*Q4*2/1E6` |
| Découpe droite ou à la forme (ml, périmètre) | 3 | `Q1*Q2*(Q3+Q4)*2/1E3` |
| Coins arrondis (par panneau) | 4 | `Q1*Q2` |
| Perforation 2 ou 4 trous (par panneau) | 4 | `Q1*Q2` |
| Emballage (forfait) | 5 | `1` |
Positions = familles de « Conventions » (pré-presse, impression, découpe, perforation / coins, conditionnement) renumérotées 1…n. Sans choix de vérification payant, décaler. Les lignes de production sont arrondies à l'unité supérieure (1 m² / 1 ml minimum) : le signaler.

## Points relevés à la mise à jour (20/10/2026)
- Quantités multiples : `PEComponentGuidforMultipleQuantity` = Q2 (exemplaires), pas Q1 (versions).
- Procédés « Travail manuel » : la ressource et le procédé peuvent porter le même nom (« Coins arrondis » deux fois) ; prendre la 2e entrée (le procédé) et relire la grille.
- Lire l'unité du procédé dans son nom (« … avec BAT (Heure(s)) ») : une formule « par version » donne alors des heures ; le signaler.
- Le Test PJM affiche « Quantité : Q1*Q2 » quand `QuantityDefinition` = `Q1*Q2` : la formule est acceptée.

## Résultats de test v2 (Q1 versions × Q2 ex., mm ; groupe « Sur barême + 0 % »)
- 1 × 1 ex. 1000 × 1000 mm, Forex 5 mm, recto, découpe droite, J+5 → 1 plaque 1010 × 1010, 104,38 € HT (identique à la v1).
- 2 versions × 5 ex. 400 × 600 mm, Forex 8 mm, recto/verso, à la forme, coins 10 mm, 4 trous, mise aux normes + BAT, J+3 → 1 plaque 3050 × 1020 (10 panneaux), 463,20 € HT.

## Résultats de test (Panneau PVC v1, dimensions en cm et une seule quantité ; groupe « Sur barême + 0 % »)
- 1 × 100 × 100 cm, Forex 5 mm, recto, découpe droite, J+5 → 1 plaque 1010 × 1010, 104,38 € HT.
- 10 × 60 × 40 cm, Forex 8 mm, J+1 → 1 plaque 3050 × 1020 (10 poses), 462,88 € HT.
