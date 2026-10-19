---
name: creer-produit-pressero
description: Creates a Pressero product by duplicating a model product, renames it, attaches or replaces its PrintJobManager pricing couple (APJM + integration Id), edits its tabs (descriptions, groups, tags…) and tests the price on the storefront. Use when the user says "crée le produit … dans Pressero", "duplique le produit …", "rattache le moteur PJM au produit", "change le groupe de tarif du produit", "crea el producto en Pressero", "duplicate this Pressero product", "link the PJM engine to the product".
---

# Create / update a product (admin UI)

Load `pressero-expert` first. Selectors and details: `pressero-expert/references/produits.md`.

## Inputs to settle
Site; model product (default: an existing product on the same PJM engine, otherwise ask); new name and URL (check unique); PJM engine and PJM price group → integration Id; visibility groups; descriptions/tags if any; target site if different (duplication can copy to another site).

## A. Duplicate (new product)
1. Open `https://{admin}/site/{domain}/Products/Duplicate`.
2. `#ProductId` DropDownList → model (match `UrlName`); `#TargetSiteId` → target site; check the new URL is not in the dataSource; fill `#NewProductUrl`, `#NewProductName` (+input/change); click « Dupliquer ».
3. Check « Duplication realisée avec succès », then find the new product in the list (`/Products`, row with the new URL) and get its ProductId from the edit link.

## B. Pricing couple (when the engine or price group differs from the model)
1. Get the integration Id: PJM → Paramètres → Moteurs de produit → engine → Intégrations → price group → « Id de l'intégration » (read-only; ask the user to sign in to PJM in Claude's tab, or to paste the Id).
2. Edit the product → Tarification → remove the current couple (`.btn-remove-calculator`) → group « Tou le monde » → APJM → MIS Product ID = integration Id → green button → couple listed, no error.
3. Never pick APJM2.

## C. Other tabs (only what the user asked)
Long description via `kendo.jQuery('#pressero-editor').data('kendoEditor')`, short description, groups (`SiteGroups_*` checkboxes), tags (grid dataSource add + sync), Générale fields (Kendo widgets via their API). Images: tell the user to upload them in the Illustration tab (Claude cannot upload files).

## D. Save and verify
1. Click the single visible « Sauvegarder » → back to the product list = success.
2. Re-open the product: name, URL, couple, groups, edited fields.
3. Storefront `/product/{url}`: pick the first choice of every option (one at a time, re-query, ~3 s, 2–3 passes) and read `#pricingEngine_lblFinalPrice`; compare with the model or the expected price (a new price group should change the price accordingly).
4. If the product needs the segmented-buttons configurator, offer `configurateur-produit-pjm` (add its path to the existing block's CONFIG.paths or create a block).
5. Report in plain words; note new ProductIds in the user's project notes.

## Never
Delete a product, uncheck groups not mentioned by the user, or change the model product.
