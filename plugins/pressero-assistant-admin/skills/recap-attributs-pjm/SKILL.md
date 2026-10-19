---
name: recap-attributs-pjm
description: Shows results returned by a PrintJobManager engine (attributes) in the summary of a Pressero product page — total quantity, computed dimensions, warnings, weight, estimated delivery date — and syncs Pressero's ship date (SHIP_DAYS) with a cut-off hour. Use when the user says "affiche les attributs PJM dans le récapitulatif", "montre la date de livraison estimée", "heure limite de commande", "SHIP_DAYS", "muestra los atributos PJM en el resumen", "show PJM attributes in the Pressero summary".
---

# PJM attributes in the Pressero summary

Load `pressero-expert` first. Example validated on equipe3 `/product/etiquette` (19/10/2026): `assets/recap-attributs-exemple-etiquettes.html`. PJM side (creating attributes, limits, `SHIP_DAYS`, technical quantity S1): plugin `pjm-atelier-moteurs`, `moteurs-pjm-expert/references/attributs.md`. Calendar: `pressero-expert/references/calendriers.md`.

## How it works
- After each price calculation Pressero calls `intCalcFinish(e, a)`: `a.Attributes` = `[{Key, Value}]` (values may use a comma), `a.Weight` = PJM weight as a string with a comma (« 1,68646 »).
- The PJM configurator (`configurateur-produit-pjm`, v4) already sets `window.intCalcFinish = refresh`: **chain** the existing function (wrap it, call it, then render), never overwrite it; mark the wrapper (`__pzattr`) to avoid wrapping twice.
- Rows are added under the configurator's summary (`.sp-summary .sp-section__body`) with the summary's own classes; a MutationObserver re-inserts them when the configurator rebuilds `#calcParmInputs`. Without the configurator, a small fallback box is shown.
- A PJM attribute value is limited to 500 characters: send raw data from PJM (quantities, thicknesses, weights per choice) and compute the rest in the script (keep the formula identical to the Excel, test it on many cases in Python/Node).

## Delivery date with a cut-off hour
- Pressero computes the ship date from the `SHIP_DAYS` attribute with its **company calendar** (working days + holidays) but has **no cut-off hour**, and PJM has no clock.
- The engine has a hidden technical quantity **S1** (0–10, default 0) and `SHIP_DAYS = N+S1` on each lead-time choice. The script computes the estimated date (today not a working day → next working day; after `cutoffHour` → tomorrow; then + N working days excluding weekends, holidays, closures), then S1 = working days from today to that date − N + `shipDaysOffset`, writes it into the S1 field (`kendo.jQuery(input).val(v).trigger('change')` relaunches the price) and hides the field and its section. Re-check every minute (crossing the cut-off while the page is open).
- Holidays and closures must be the same in the script (`feriesFrance`, `fermetures`) and in the Pressero company calendar, otherwise the two dates differ. Check in the cart that Pressero's date equals the summary date; adjust `shipDaysOffset` only for a systematic gap.

## Steps
1. PJM: make sure the engine returns the needed attributes (test page). If not, add them with `pjm-atelier-moteurs` (ask before writing).
2. Read the product page: summary DOM, field labels (S1 label for `champJoursAjoutes`), lead-time select, attribute keys received (hook `intCalcFinish` temporarily and log `a.Attributes`).
3. Copy the example, edit `CONFIG` (paths, cutoffHour, fermetures, feriesFrance, shipDaysOffset, product constants) and the rows/calculations for the product. `node --check` the script.
4. Test by injecting it in Claude's tab (nothing saved): rows displayed, values right on 2–3 cases, price unchanged, S1 value and SHIP_DAYS consistent with the current time. Also test the cart edit page (`/product/{url}/{cart item id}`, « Éditer » button in the cart).
5. Install with `scripts-head-pressero` as a separate block placed **after** the configurator block (e.g. `AFFICHER LES ATTRIBUTS PJM DANS LE RECAPITULATIF {PRODUIT}`), backup first. Re-test on the storefront.
6. If needed, add holidays/closures to the company calendar (`references/calendriers.md`), with the user's go-ahead (the calendar is shared by many sites).
7. Tell the user where the settings are (CONFIG at the top of the block) and record the block in the project notes.
