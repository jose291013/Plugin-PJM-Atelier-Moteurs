# Procédure de construction d'un moteur PJM via Claude in Chrome (validée le 16/10/2026)

Procédure validée sur deux moteurs de test (brochure A4 numérique, bâche Frontlit).

## Langue du moteur
Construire le moteur dans la langue de la fiche (`engine.language`) : noms, textes client, choix et délais tels qu'ils sont dans la fiche. Ne jamais traduire les noms PJM (ressources, procédés, matériaux).

## Instance PJM du client
- L'adresse de base du PJM est dans l'Atelier : `settings/app.pjmUrl` (écran admin) et `pjm.instance` dans le JSON de la fiche. Toujours l'utiliser (ne jamais supposer une adresse).

## Cycle de vie d'une fiche (statuts)
brouillon → pret (Prête à construire) → construction → cree (Créé dans PJM) → maj (À mettre à jour) → … ; import (À importer depuis PJM).

## Correspondance fiche ↔ PJM (`briefs.pjm`)
- `pjm.engineId`, `pjm.url`, `pjm.builtAt`, `pjm.importedAt`, `pjm.map` :
  `map[componentLocalId] = {pjmId, options:{optionLocalId:{pjmId, productions:[pjmLineId…], materials:[pjmLineId…]}}, productions:[…], materials:[…], suppressions:[…]}`.
- À la construction et à l'import, remplir `map` avec les identifiants PJM de chaque composant, choix, ligne de production, ligne matériau et suppression.

## Mise à jour d'un moteur existant (statut « maj »)
1. Réimporter d'abord l'état réel du moteur PJM (lecture seule) pour repérer les modifications faites à la main ; les signaler à l'utilisateur.
2. Comparer la fiche au moteur : composants, choix, lignes (ressource/procédé/formules), suppressions, délais.
3. Présenter la liste des différences (ajouts, modifications, suppressions) et attendre la confirmation.
4. Appliquer uniquement les différences (ajout : endpoints habituels ; modification : même endpoint avec l'Id existant). Ne jamais supprimer sans confirmation explicite.
5. Relancer les cas de test, mettre à jour `pjm.map`, `tests[].last`, statut « cree ».

## Import d'un moteur existant (statut « import »)
- L'utilisateur colle l'adresse /ProductEngines/Edit/{id} dans l'Atelier (Nouvelle fiche → Importer).
- Lire le moteur : quantités (Name, Prompt, min, max, défaut), options (choix, Markup, lignes de production et matériaux avec formules), composants Matériel et Calcul, suppressions.
- Remplir la fiche (components, delays si un composant Option ne contient que des marges, hideWhen, pjm.map, pjm.importedAt) ; formules non standard → step.basis « custom » avec la formule d'origine. Statut « cree » à la fin.

## Cas de test (`briefs.tests`)
- {label, q:{Q1:…}, c:{componentLocalId: nom du choix, __delay: libellé}, expected, last:{price, at, ok}}.
- Après chaque construction ou mise à jour : les exécuter avec le bouton Test de PJM (« Calculer le plan de production »), écrire `last` (prix HT, date, ok = écart ≤ 1 % si expected renseigné) et signaler les écarts.

## Étapes et points d'entrée PJM
1. Moteur : /ProductEngines/Create → champs Name, catégorie (select), Description, Prix min/max → Sauvegarder. L'id se lit dans les liens /ProductEngines/Quantity/{engineId}.
2. Quantité : /ProductEngines/Quantity/{engineId} → select Name (Q1..Q5, R1.., P1.., S1..), Prompt, MinQty, MaxQty, DefaultQty, Decimals, ArbitraryQty (coché par défaut).
3. Option : /ProductEngines/Option/{engineId} → Name, Prompt → après sauvegarde, page ComponentEdit : case IsRequired (Forcer une sélection) puis Sauvegarder.
   - Ajout de choix : POST /productengines/saveoption (champs __RequestVerificationToken, Id=cid, ComponentId=cid, Sequence, SubscriberId, CreateDate, cid, OptionName, Markup). Le jeton se prend sur /productengines/addoption/{cid}.
   - Ids des choix : liens EditOption sur /ProductEngines/ComponentEdit/{cid}.
4. Production d'un choix ou d'un Calcul : POST /PECompWorkflows/SaveComponentProduction
   (ComponentProductionId=000…, ComponentId=cid=OptionId=<id du choix ou du composant Calcul>, FromQty, ToQty, WorkflowComponentId=<id du procédé>, WorkflowComponentId_input=<nom>, Seq, Instructions, QuantityCalculation, NumberUpExpression). Réponse {"ErrorCode":0}.
   - Les procédés (WorkflowComponent) : combobox #ddlworkflowComponents, items {Id, Name "Procédé (groupe)", Group = ressource}. L'Id = Id du procédé de la ressource.
5. Matériel : /ProductEngines/Material/{engineId} → Name, Prompt, MaterialListingType (0 = spécifiques), multiselect Kendo ddlMaterials (valeurs = ids des matériaux, retrouvés par le texte de l'option), CalculationFormula, NumberUpExpression, WeightCalculation.
6. Calcul : /ProductEngines/Calculation/{engineId} → Name, Prompt ; production comme au point 4 avec l'id du composant.
7. Suppressions (masquer X si composant Y = valeur) : POST /PECompSuppressions/Save?compId={X}&engineId={E}
   (Id=000…, EngineId, ComponentId=X, SubscriberId, SuppressedComponentId=Y (composant condition), Name=nom de Y, Value=<id du choix de Y>, ComponentName, SuppressedValueName, SuppressedComponentType=0, MaterialId=000…).
   - Valeurs possibles : POST /PECompSuppressions/GetOptionValues (cid=X, oid=Y) → « --Sélectionner-- » a la valeur `select_one_id`, puis les choix (StringId = id du choix).
8. Délais : composant Option « Délais de production » (non forcé, sans production), un choix par délai, marge dans Markup (Ajustement global du travail %). Ex. : J+5 0 %, J+3 15 %, J+1 25 %. Le 1er délai = défaut.
9. Moteur : « Sélectionnez la quantité » = Q1 puis Sauvegarder ; bouton Test → « Calculer le plan de production ».

## Lignes matériau dans une Option (validé sur la bâche, 16/10/2026)
- POST /PECompMaterials/SaveComponentMaterial : Id = 000… pour créer (ou l'Id de la ligne pour la modifier), ComponentId = cid = OptionId = id du choix,
  FromQty, ToQty, MaterialId (+ MaterialId_input = nom), ReportPosition, Instructions, QuantityCalculation, NumberUpExpression, WeightCalculation.
- Ids des matériaux : combobox MaterialId du formulaire matériau (champ Name). Lecture des lignes : grille /PECompMaterials/_Index (URL lue dans la grille).
- Le même matériau ne peut pas être ajouté deux fois au même choix (ErrorCode 437).
- Limite : 1400 caractères par formule (QuantityCalculation et NumberUpExpression).
- Astuce : `Nup()` dans la formule de quantité renvoie la formule de poses de la même ligne → on y met la consommation de la ligne, puis on la compare aux autres laizes.

## Choix automatique de la laize (bâche)
- Une ligne matériau par laize (100, 160, 200, 250, 320, 500 cm) dans chaque choix de bâche.
- Poses (NumberUpExpression) = consommation en cm² : `L*Min(if(MN <= L,Ceiling(Q1/floor(L/MN))*MX,9E8),if(MX <= L,Ceiling(Q1/floor(L/MX))*MN,9E8))` avec MN = (Min(Q2,Q3)+6), MX = (Max(Q2,Q3)+6).
- Quantité = `if(MN > L,0, if(C(autre) <= Nup(),0, … Nup()/10000.0))` : <= contre les laizes plus petites, < contre les plus grandes → une seule laize non nulle (m²).

## Poids des matériaux vendus au m² (16/10/2026)
- Quand on détourne le champ « poses » (Nup) pour un calcul (ex. consommation de laize), le poids calculé par PJM devient faux : il faut renseigner le champ « Calcul du poids » (WeightCalculation) de chaque ligne matériau.
- Formule : `(Q2*10)*(Q3*10)*Q1*Weight`
  - Q2, Q3 en cm → ×10 pour passer en mm (les dimensions des matériaux PJM sont en mm).
  - `Weight` = poids du matériau ramené au mm² = WeightPer / (Largeur × Hauteur du matériau).
- Prérequis sur la fiche matériau PJM : dimensions 1000 × 1000 mm (unité = 1 m²) et WeightPer = grammage en kg/m² (ex. 0,45 pour 450 g/m²). Sinon `Weight` est calculé sur la surface du rouleau et le poids est faux.
- Le poids est celui de la surface finie (Q2 × Q3), pas de la laize consommée.
- Contrôle : 1 bâche 200 × 100 cm en Frontlit 450 g → 0,90 kg ; en B1 510 g → 1,02 kg ; 5 × 300 × 600 cm en B1 → 45,9 kg.
- Fait sur le moteur test bâche : 12 matériaux Frontlit (PRINT PA 450 g et B1 510 g, 6 laizes) passés en 1000 × 1000 mm, WeightPer 0,45 / 0,51.
  Le choix de laize n'utilise pas les dimensions du matériau (laizes en dur dans les formules), il n'est donc pas affecté.
- Modifier une fiche matériau : passer par le formulaire /Materials/Edit/{id} (remplir puis Sauvegarder) ; un POST direct répond 500.

## Règles PJM importantes
- Une formule ne peut pas tester la réponse d'une option : on duplique les composants (ex. Impression intérieur / Impression intérieur + couv) et on les masque par suppression selon « Couverture différente ? ».
- Règle : une option à sélection forcée encore sur « --Sélectionner-- » doit se comporter comme si son 1er choix était choisi. Donc tout composant masqué quand le 1er choix est sélectionné reçoit aussi une suppression avec la valeur `select_one_id`. Ex. : Impression intérieur et Papier intérieur masqués si Couverture différente = Oui OU --Sélectionner--.

## Incompatibilités (onglet « Règles » de l'Atelier → JSON)
- Masquer une question entière quand X = valeur → suppression PJM (champ hideWhen des composants).
- Retirer seulement certains choix d'une option (`restrictions`) → PJM ne masque pas un choix isolé : dupliquer le composant cible (version complète / version réduite) et masquer l'une ou l'autre selon X.
- Une suppression peut dépendre d'un matériau (champ MaterialId) — à valider au premier cas réel.
- `businessRules` (texte libre) : règles liées aux quantités → formules ou limites min/max des Quantités.

## Pièges relevés
- Formules : toujours mettre des espaces autour de < et <= (« <Nup() » est rejeté par la protection anti-HTML du serveur : réponse HTML au lieu de JSON).
- Procédés des ressources « Travail manuel » (ex. Renfort, Oeuillets) : la liste #ddlworkflowComponents contient d'abord l'entrée de la ressource puis le procédé ; prendre le procédé (ex. « Oeuillets (oeuillets) »), sinon l'enregistrement répond OK mais rien n'est créé. Toujours relire la grille après ajout.
- La sortie de l'outil JavaScript est bloquée si elle contient « & » ou des motifs « x=y » : remplacer ces caractères avant de renvoyer du texte.
- Le nom affiché d'un matériau peut différer de son nom catalogue (ex. « Couché Brillant 135 Gr » s'affiche « Papier supérieur blanc 135 Gr »).
- L'ordre des composants dans le formulaire n'est pas l'ordre de création : le réordonner en fin de construction avec `UpdateCompSequence` (voir « Conventions »).
- Le formulaire Test de PJM affiche tous les composants (les suppressions ne s'y voient pas), mais le calcul les respecte.
- Session PJM expirée → l'utilisateur se reconnecte, Claude ne saisit jamais d'identifiants.

## Résultat du test bâche (Bâche Frontlit)
- 1 × 200 × 100 cm PRINT PA, Production, ourlet + œillets : laize 2,50 m, 2,65 m², 145,46 € HT (J+5) / 181,82 € (J+1, +25 %).
- 5 × 300 × 600 cm B1, Qualité, fourreaux : laize 3,20 m, 96,96 m², œillets masqués.
- Limite PJM : un choix (J+1) ne peut pas être masqué selon une quantité → libellé « J+1 (jusqu'à 50 ex.) ».

## Résultat du test brochure
100 ex. × 16 p. A4, Couché Mat 115, quadri RV, piqûre :
- couverture identique : 400 feuilles 450×320, 104,98 € HT ;
- couverture différente Brillant 250 g quadri recto + pelliculage mat : 300 feuilles intérieur + 100 couverture, 141,66 € HT.

## Conventions de construction (validées le 17/10/2026, moteur « Flyer formats fermé+ perso »)

### Position dans le rapport des étapes de production (champ `Seq`)
Le champ `Seq` d'une ligne de production = colonne « position s… » = ordre de l'étape dans le rapport / la fiche de travail. Ne jamais laisser 1 partout : suivre l'ordre réel de l'atelier, identique dans tous les choix du moteur.
| Position | Étapes |
|---|---|
| 1 | Pré-presse, vérification de fichiers, CTP / plaques |
| 2 | Impression (numérique, offset, grand format) |
| 3 | Pelliculage, lamination, vernis |
| 4 | Massicot, coupe, découpe |
| 5 | Rainage, perforation, coins arrondis |
| 6 | Pliage |
| 7 | Assemblage, piqûre, reliure, dos carré collé, wire-o |
| 8 | Finitions grand format (œillets, ourlets, fourreaux, soudure) |
| 9 | Conditionnement, emballage, expédition |
- N'utiliser que les numéros des familles présentes dans le moteur, dans cet ordre (ex. flyer : impression 1, pelliculage 2, massicot 3, rainage 4, pliage 5).
- Dans un même choix, deux étapes successives (ex. Rainage puis Pliage) gardent leur position de famille.
- Montrer les positions dans le plan de construction ; les vérifier à chaque mise à jour.
- Corriger une ligne existante : `SaveComponentProduction` avec `ComponentProductionId` = Id de la ligne et tous ses champs renvoyés (seul `Seq` change).

### Ordre des questions du formulaire
- Équivalent du glisser-déposer de PJM : POST JSON `/ProductEngines/UpdateCompSequence/` avec `{"newSettings":[id1, id2, …]}` (tous les composants, dans l'ordre voulu ; ids = id **bruts** des composants, SANS le préfixe `comp_` des éléments `.component-list` : avec `comp_` la réponse est aussi « Success » mais rien ne change, validé le 27/10/2026). Réponse `{"message":"Success"}` ; relire l'ordre ensuite.
- Faire cet appel à la fin de chaque construction (et après ajout de composants lors d'une mise à jour), puis relire l'ordre.
- Ordre logique : Quantité Q1 → Format → dimensions (Largeur, Hauteur) → Grammage / qualité → Papier → Impression → finitions (pelliculage, vernis) → pliage / façonnage → reliure → Délais de production. Les variantes dupliquées d'un même composant restent groupées.

### Groupe de prix pour l'intégration
- Ne pas le régler dans le moteur : PJM l'attribue automatiquement selon la société du devis. Ignorer `margin.pricingGroup` à la construction ; ne pas le signaler comme point à faire.
- Pour les tests, garder le groupe proposé par la page Test et l'indiquer avec les prix.

### CalcNup : fond perdu
- Le 5e paramètre de `CalcNup(docW, docH, sheetW, sheetH, bleed)` est le fond perdu TOTAL (deux côtés) : 3 mm par côté → 6. Ex. `CalcNup(105,148,450,320,6)` = 8 A6 sur 450 × 320.
- La fiche (`bleed`) est déjà ce total : la reporter telle quelle.

### Masquer selon le papier choisi (suppression par matériau) – validé
- Un composant Matériel peut servir de condition : `GetOptionValues` renvoie ses matériaux (StringId = Id du matériau).
- Enregistrer avec `SuppressedComponentId` = composant Matériel, `Value` = Id du matériau, `SuppressedValueName` = nom du matériau, `MaterialId` = 000….
- Ex. pelliculage masqué sur Couché 100 et 115 g : une suppression par matériau. Dans la fiche : `hideWhen` {component: id du composant matériel, value: nom du matériau}.

### Formats fermés + format personnalisé
- Option « Format » (A6, A5, A4…, Personnaliser) ; Largeur / Hauteur masquées sur les formats fermés et sur `select_one_id`.
- Tout ce qui dépend du format (papier, impression, pelliculage, coupe) est dupliqué par format, avec ses poses en dur (`CalcNup(148,210,450,320,6)`) ou `Max(CalcNup(Q3,Q4,450,320,6), 0.0001)` pour le format personnalisé (ou `floor(CalcNup(Q3,Q4,450,320,6))`) ; quantité des **matériaux** `Ceiling(Q1 / Nup())` (poses en formule → pas de division par PJM), quantité des **lignes de production** `Q1` (PJM divise lui-même par `Nup()` ; `Ceiling(Q1 / Nup())` y diviserait deux fois : 1 feuille facturée au lieu de 12, constaté le 27/10/2026). La coupe peut être portée par les choix de « Format ».

### Matériaux en double (même nom)
- `matIds` peut trouver deux matériaux actifs au même nom. Prendre celui déjà utilisé par un autre moteur (lire les `"value":[…]` du multiselect `ddlMaterials` des composants Matériel), sinon le plus ancien (`CreateDate`), et le signaler à l'utilisateur.

### Points techniques relevés
- Composants : `POST /ProductEngines/SaveComponent` avec les champs du formulaire `/ProductEngines/{Quantity|Option|Material}/{E}` (fetch, sans navigation). L'id du nouveau composant = lien `ComponentEdit` absent avant l'appel. Composant Matériel : un champ `ddlMaterials` répété par matériau, `MaterialListingType` 0, `CalculationFormula`, `NumberUpExpression`.
- « Forcer une sélection » : renvoyer le formulaire de `/ProductEngines/ComponentEdit/{cid}` avec `IsRequired=true`.
- `saveoption` répond en HTML (redirection) mais crée bien le choix : vérifier avec la grille `/PEOptions/_Index?cid=`.
- Moteur : « Sélectionnez la quantité » = champ `QuantityDefinition` (« Q1 ») du formulaire `/ProductEngines/Save`.
- Page Test : les questions masquées sont recalculées sur l'événement jQuery `change` de l'élément `#component-{id avec _}` ; avec Kendo, appeler `w.value(v); w.trigger('change'); jQuery(e).trigger('change')`, attendre ~0,7 s entre deux choix, sinon « Required: Papier ».

## Pièges validés le 17/10/2026 (moteur « Étiquettes en bobine »)
- **Decimal × Double** : `Ceiling()/floor()` renvoient des Double, `0.9` est un Decimal → expression en erreur sans message (production = 1 €, matériau absent). Tous les non-entiers en notation scientifique (`45E-1`, `198E-6`, `1E6`).
- **Production + poses** : quantité finale = Ceiling(formule / Nup()). Si les poses servent à autre chose (laize retenue…), écrire `(…)*Nup()` ; pour garder les centimes, procédé à 0,01 €/unité et formule × 100.
- **Matériau + poses en formule** : quantité non divisée ; poses en nombre fixe (`2`) : quantité divisée.
- **`Nup()` = 1 dans « Calcul du poids »** → recalculer la sélection dans la formule de poids (sinon division par 0 : « Value was either too large or too small for a Decimal »).
- **ToQty = 0 sur une ligne matériau d'un choix ⇒ ligne ignorée** : mettre 999999. Les lignes de quantité 0 n'apparaissent pas sur le devis.
- **Poids** : « Calcul du poids » ignoré si WeightPer du matériau = 0 ; PJM arrondit WeightPer et le coût matériau à 2 décimales → saisir le poids pour 1000 articles et le coût pour 100 000 articles.
- **Page Test en cache** : recharger la page d'édition du moteur avant de retester après une modification.
- Pas de Q6 : utiliser R1…R5, P1…P5, S1…S5.
- **CalcNup renvoie un Decimal** (validé 20/10/2026) : `Q1 / CalcNup(…)` et `Max(CalcNup(…),1E-4)` sont refusés (ErrorCode 448 « Operator '/' can't be applied to operands of types 'double' and 'decimal' ») ; écrire `floor(CalcNup(…))`. Le message d'erreur de `SaveComponentMaterial` cite la formule fautive : le lire.
- **Type de produit d'origine** : avant de construire, vérifier que les finitions de la fiche ont du sens pour le produit (ex. pas d'œillets / fourreaux sur un panneau rigide) et le signaler dans le plan.

## Matériau par laize au mètre linéaire (validé 17/10/2026)
- Un matériau par laize et par support : « {support} - laize {W} mm (ml) », dimensions W × 1000 mm, prix au ml = prix m² × W/1000.
- Dans chaque choix : une ligne par laize, poses = formule qui renvoie la laize retenue, quantité `if(Nup() = W, ml réels, 0)`, poids `if(<sélection> = W, …, 0)` (sélection recopiée, pas de Nup()).
- Marge variable (coefficient selon la surface) : ne pas la mettre dans la quantité matériau (l'atelier lirait des mètres faux) ; ajouter dans le même choix une ligne de production « Marge » (procédé à 0,01 €/unité, poses = formule de laize, quantité = (coef − 1) × coût matière × 100 × Nup()). Minimum de facturation : coef × Max(coût, minimum) − coût.
- Le devis n'affiche que la ligne de la laize retenue : l'atelier voit directement la bobine mère à sortir.
- Exemple complet : skill `reprendre-excel-pjm`, `references/exemple-etiquettes-bobine.md`.

## Créer ressources, procédés et matériaux (validé 17/10/2026)
- Seulement si l'utilisateur le demande ou le confirme ; détails des appels dans `scripts-pjm.md`.
- Ressource : `/Production/Save` (Name, DepartmentId, FacilityId, ProductionType 0 = Équipement, 1 = Travail manuel).
- Procédé : formulaire `/Processes/Create?pid={ressource}&ptype=Equipment` → POST de son action avec Name, UnitName et `WorkFlowComponentRange.RunTimeUnitRawCost` (prix par unité, virgule décimale) ; tarif modifiable ensuite par `/Processes/EditRange/{rangeId}?ptype=Equipment` → `/Processes/SaveRange`.
- Matériau : formulaire `/Materials/Create` → `/Materials/Save` avec CategoryID + ddlCategories = Id de catégorie, Width, Height, WeightPer / WeightTotal, `MaterialRange.FromQuantity/ToQuantity/ItemCount/CostforItemCount/CostAdjustment`. Prix unitaire = CostforItemCount / ItemCount × (1 + ajustement %).
- Modifier un matériau : renvoyer le formulaire `/Materials/Edit/{id}` vers `/Materials/Save` en remplaçant `ddlCategories` (« System.Guid[] ») par l'Id de catégorie et sans `ddlSubCategories` (sinon 500) ; tarif : `/Materials/SaveMaterialRange` (MaterialID, Id de la tranche, FromQuantity, ToQuantity, ItemCount, CostforItemCount, CostAdjustment).
