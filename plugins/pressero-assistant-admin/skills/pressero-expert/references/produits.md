# Products (admin)

List `/site/{domain}/Products` · create `/Products/Create` · edit `/Products/Edit/{ProductId}` · duplicate `/Products/Duplicate` · import/export `/Products/ProductImportExport`.
All tabs live in ONE page/form: one « Sauvegarder » at the bottom (success → back to the list). Buttons: Sauvegarder, Annuler, Supprimer (never).

## Tabs (anchors) and key fields
- **Générale `#generalPage`**: ProductName, UrlName (storefront `/product/{UrlName}`), ProductStartDate / ProductExpirationDate (kendoDateTimePicker), IsUseOpenFrame / IsOpenFrameForCustomizationOnly / OpenframeUrl, IsFeatured, EnableQuickView, PrintersPartNum, PublicPartNum, KitOption (select), TeaserPrice, DisplayProductImage, ShowShippingEstimator, IsPrintEstimate + PrintEstimatePromoText, RelatedSuggestedProducts (kendoMultiSelect), AcceptanceControl (Aucun/case/texte) + AcceptanceText, AllowNameEditInCart, stockId (kendoDropDownList), IsBackOrderingAllowed, IsHideOnOutOfStock, DaysToShipInStock / DaysToShipOutStock (kendoNumericTextBox), MustShipSeparately, shipFromLocationId, IsDigitalOnly, ShowFilePreview, OverrideTax (numeric) / OverrideTaxOnShipping / TaxId, workflowId (kendoDropDownList, e.g. « apjm »), MisId (product « Intégration ID », not the pricing MIS Product ID), ProductLocationNotes, vendorId / VendorGetsNonMarkupPrice / VendorInstructions, Folding / Finishing / Binding / Packaging, eDocBuilder fields (CustomizableTemplate…).
- **Description `#descriptionPage`**: long description `#pressero-editor` (kendoEditor, name LongDescription); `#ShortDescription` textarea.
- **Tarification `#pricingPage`** (container `#pricingPageId`): pricing couples (below), Q1–Q5 Min/Max/DecPlaces/CalculatorAllowArbQty, MinPrice, CalcShowPricePerPiece, MarkupQtyParam, markups (NewMarkup_*), vendor comparison.
- **Illustration `#artworkPage`**: « Télécharger » button (`#btnProductImageUpload`, file picker). Several images only here (Excel / API load ONE image) → the user uploads.
- **Formulaires `#formsPage`**: `formId` (kendoDropDownList). A file-upload form is incompatible with a product page (it is attached but not displayed).
- **Groupes d'utilisateurs `#groupsPage`**: checkboxes `SiteGroups_{groupId}_` (who sees the product).
- **Attributs**: NewAttribute_AttributeId (kendo) + value + « Ajoutez à la liste ».
- **Montage (kits) `#kittingPage`**, **Package `#packagePage`**, **Téléchargements `#uploadsPage`** (FileUploadRequired, UploadDimentions_*, UploadFields_{n}_*), **Tags `#tagsPage`** (Kendo grid TagName/TagValue: `ds.add({TagName, TagValue}); await ds.sync();` then page Save; never use the grid's delete button — it opens a confirm dialog).

## Pricing couples (APJM / PJM)
1. Tab Tarification (`document.querySelector('.nav-tabs a[href="#pricingPage"]').click()`).
2. Existing couples: `#PricingPairingList .product-group-calculator` (`data-group`, `data-calculator`, label `.paring-item-main` « Groupe: Moteur »). The integration Id of an existing couple is NOT in the DOM (server side) → verify by price.
3. Remove a couple: `.btn-remove-calculator` (no confirm dialog; `$.post` + list refresh).
4. Add: `select#PricingPairing_GroupId` = « Tou le monde » (+change) → DropDownList `#PricingPairing_CalculatorId`:
   ```js
   const dd = kendo.jQuery('#PricingPairing_CalculatorId').data('kendoDropDownList');
   const item = dd.dataSource.data().find(i => i.CalculatorName === 'APJM');
   dd.value(item.CalculatorId); dd.trigger('select', {dataItem: item}); dd.trigger('change');
   ```
   wait ~2.5 s → `#PricingPairingProductInfo` gets `[name="PricingPairing.ProductInfo[0].Key"]` = `productID` and `[name="PricingPairing.ProductInfo[0].Value"]` = **MIS Product ID** → set the PJM integration Id (+input/change).
5. Green button « Sauvegarder le moteur de prix pour ce groupe d'utilisateurs » → couple appears; `#PricingPairingError` must be empty.
6. Page **Sauvegarder** (nothing is stored before).
APJM CalculatorId on the Aleyant AMS account: `480a0000-568f-0050-f674-08d940905eba` (look it up by name on other accounts). Ignore APJM2.

## Integration Id (PJM side)
PJM → Paramètres → Moteurs de produit → edit engine → panel « Intégrations » → choose « Groupe de prix pour l'intégration » → read-only « Id de l'intégration ». One Id per engine × price group. If Claude's PJM tab is not signed in, ask the user to sign in in that tab, or to paste the Id. Default couple uses the group the user names (e.g. « Sur barème + 0 % »).

## Duplication (`/Products/Duplicate`)
`#ProductId` (kendoDropDownList; dataSource ProductId, ProductName, UrlName, SiteDomain…), `select#TargetSiteId` (target site; preselected = current site; any site of the account), `#NewProductUrl`, `#NewProductName`, submit « Dupliquer ». Check the URL is unused first. Success message « Duplication realisée avec succès ». The copy keeps pricing couples (incl. integration Id), groups, options, tags… The head-bottom configurator script only applies to paths listed in its CONFIG.paths.

## Storefront price test
On `/product/{url}`: choose options one by one with `kendo.jQuery(select).val(v).trigger('change')`, re-querying the select each time (`#calcParmInputs` is replaced after every choice), ~3 s between choices, 2–3 passes. Price: `#pricingEngine_lblFinalPrice` (`#.##` until every required choice is made). Compare with the expected price.

## Product page DOM with a PJM engine (for scripts)
- Every parameter is named `Options[n].Value`, n = position in the PJM engine; `Options[0]` = hidden technical `<li style="display:none">`.
- Quantities: `input.PriceCalc_CalcParmInput` (+`PriceCalc_CalcParmInputN`); choices: `select.PriceCalc_CalcParmSelect`.
- `<li>` class = `form-group PriceCalc_CalcParm {GUID}` → group by label text or option number, not by class.
- Option values are GUIDs; first entry `--Sélectionner--` value `select_one_id` (except lead-time lists).
- `#calcParmInputs` (inside stable `#pricingEngineArea`) is replaced on each choice (`/product/{x}/options/` then `/product/{x}/pricing`). Price `#pricingEngine_lblFinalPrice`, `#calcResults`, `.calculatorTotalArea`, add to cart `#btnAddToCartButton`.
(Pressero calculators instead use Q1, Q2… and `input.pricingGridQuantity`.)
