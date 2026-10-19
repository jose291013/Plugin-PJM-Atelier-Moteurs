---
name: configurateur-produit-pjm
description: Builds the "segmented buttons + side-by-side quantities + sticky price bar" configurator script for a Pressero product priced by a PrintJobManager (APJM) engine, adapts it to the product's real parameters, and installs it as a named block in the site's head bottom. Use when the user says "boutons segmentés pour ce produit", "fais le configurateur du produit …", "transforme les listes déroulantes en boutons", "botones segmentados Pressero", "segmented buttons for this Pressero product".
---

# PJM product configurator script

Load `pressero-expert` first. Template: `assets/configurateur-pjm-template.html` (v4, validated on equipe3 `/product/etiquette`, 18/10/2026). Product DOM facts: `pressero-expert/references/produits.md` (section "Product page DOM with a PJM engine").

## 1. Read the real product page (read-only)
Open `https://{domain}/product/{url}` (sign-in by the user if needed). With JS, list each `#calcParmInputs li`: label, field type (input / select), `name` (`Options[n].Value`), number of real options (excluding `select_one_id` / « --Sélectionner-- »), option texts. Note lists with a single real choice, date-like options, arrow options (↑ ↓ ← →), the price label, two jQuery instances, presence of the Pressero Script Server (`pressero.js`, `.pss-segmented-buttons`).

## 2. Adapt the template (copy it, edit only CONFIG and comments)
- `paths`: `['/product/{url}']` (lower case, no trailing slash); the template also matches the cart edit page `/product/{url}/{id}` — test it too (add to cart, click « Éditer »). Several products → several paths, or one block per product family.
- `sections`: titles in the user's language; `match` by normalised label fragments (lower case, no accents/spaces) — robust to engine re-ordering — or by option number. `cols: 2` for side-by-side numeric fields (quantities, width/height…). Last section = catch-all.
- `unitRules` (e.g. « (mm) » → mm), `deliveryMatch` (label of the lead-time list), `optionImages` keyed by option TEXT (PJM values are GUIDs), `i18n`.
- `takeoverPss`: true only if the Pressero Script Server segmented buttons / fixed price bar are active on the site (then also tell the user the clean fix is to disable those PSS features).
- Keep the CSS rule `body.pageName_{url} .k-loading-mask` scoped to the product(s).
- Update the header comment (site, product, date, engine parameter numbering).
Check JS syntax (`node --check` on the extracted script) and CSS brace balance.

## 3. Test before installing
Inject the CSS and JS into the product page in Claude's tab (temporary, nothing saved). Check: number of groups and sections, no native select left visible, single-choice lists auto-selected and shown in the summary, then click one option per group and verify the price is computed and equals the native price label. Report results.

## 4. Install
Use `scripts-head-pressero`: block name e.g. `BOUTONS SEGMENTÉS ET PLUS POUR {PRODUIT}` (ask the user's preferred name). If a block for the same product exists, replace it instead of adding a second one. After saving, reload the storefront page and re-run the checks of step 3 on the real installation.

Note: the template sets `window.intCalcFinish = refresh`. Other blocks that need the calculation result (skill `recap-attributs-pjm`) must be placed after it and chain that function.

## 5. Deliver
Also give the adapted file to the user (write it to the connected work folder if there is one) and record in the user's project notes: product, path, block name, sections mapping.
