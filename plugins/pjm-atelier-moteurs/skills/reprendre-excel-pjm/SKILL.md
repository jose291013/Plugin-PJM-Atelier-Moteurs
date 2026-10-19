---
name: reprendre-excel-pjm
description: Rebuilds an Excel pricing calculator (for example a Pressero Excel engine) as a PrintJobManager engine, faithfully, creating missing production resources and materials, then tests it against the Excel. Use when the user uploads an .xls/.xlsx price calculator and says "reproduis ce moteur dans PJM", "reprends mon Excel Pressero", "pasa este Excel a PJM", "rebuild this Excel engine in PJM".
---

# Rebuild an Excel price calculator in PJM

Load the `moteurs-pjm-expert` skill first (formulas, rules, `references/procedure-construction.md`, `references/scripts-pjm.md`). Answer in the user's language; build the engine in the language of the Excel.
Worked example with every formula: `references/exemple-etiquettes-bobine.md` (Pressero labels on rolls, 17/10/2026).

## Usage
Apply `moteurs-pjm-expert/references/consommation.md`. This task is **lourd** (analysis + build + debugging): say so, one task per conversation.

## Safety
Same as `construire-moteur-pjm`: never type PJM credentials, show the plan and get a clear « oui » before the first write in PJM, never delete anything in PJM (repurpose a line by saving it with its Id instead), ask before changing a shared material record.

## 1. Read the Excel (cloud workspace)
- Copy the upload into its own folder; convert `.xls` with `soffice --headless --convert-to xlsx`.
- Dump every sheet with openpyxl twice (formulas, and `data_only=True` values). Ask the user, if not given, where the form (inputs), the dropdown lists, the price and the weight cells are.
- Follow the chain from the price cell back to the inputs. Note lookup tables (VLOOKUP exact = choices / attributes; VLOOKUP approximate = tiers → nested `if`), fixed costs, minimums, rounding, time/date-based cells (not reproducible in PJM), validation messages (only static min/max in PJM), and every result the Excel shows the customer besides the price (total quantity, roll diameter, warnings, delivery date).

## 2. Replicate and verify before touching PJM
- Write the model in Python (`model(inputs) → price, weight, intermediate choices`).
- Check it against LibreOffice: write new inputs with openpyxl, recalc with `soffice --convert-to xlsx`, read the price cells; 5–7 varied cases must match exactly.
- List the quirks of the Excel (e.g. tier on one roll instead of the total, selection on the wrong price, fixed constant) and ask with AskUserQuestion: reproduce identically (recommended, prices equal to the old site) or correct.
- Ask how to handle a margin that varies with quantity/surface: in the formulas (lines compute the selling price; processes at 1 €/unit; recommended when PJM markups cannot express the tiers) or PJM markups.

## 3. Design the PJM engine
- Inputs → Q1…Q5, then R1…R5 (there is no Q6); dropdowns that change the price → forced Options; informative dropdowns → Options without lines; lead-time multipliers → « Délai » Option with markups.
- A formula cannot read an option: put each option-dependent cost in a line of that choice; costs depending only on quantities → a Calculation component.
- Automatic choice among formats / roll widths: the selection goes in the poses field (returns the chosen width), each line tests `if(Nup() = W, …, 0)`; one material per width so the ticket shows what to use (see the example).
- Keep material quantities real (m², ml, sheets): the workshop reads them. A margin that varies with the quantity goes in a separate « Marge » production line (0,01 € process, cents) in the same choice, never in the material quantity.
- Write every NCalc formula from the Python model, then evaluate the formulas themselves with `scripts/ncalc_sim.py` on ≥ 3 000 random cases against the model (0 differences, length ≤ 1400, spaces around `<`, no decimal literal: `45E-1`, not `4.5`).

## 3b. Results shown to the customer (attributes)
The Excel often displays more than the price. Return the raw data as PJM attributes (`moteurs-pjm-expert/references/attributs.md`: quantities, thicknesses, weights per choice, `SHIP_DAYS` per lead time) and let a Pressero page script compute and display the rest (plugin `pressero-assistant-admin`, skill `recap-attributs-pjm`). Delivery date with a cut-off hour: technical quantity S1 written by the page script, `SHIP_DAYS = N+S1`, French holidays in the Pressero company calendar.

## 4. Catalogue
- Read resources (`/Production/_Index`), their processes (`/Processes/Steps/{id}`) and materials (`/Materials/_Index`). Missing machine → create a resource + processes; missing paper → create materials (procedures in `scripts-pjm.md` « Créer ressources, procédés et matériaux »), only if the user asked for it or confirms.
- Materials sold by m² or linear metre: dimensions W × 1000 mm; enter cost for 100 000 items and weight for 1000 items (PJM rounds both to 2 decimals).

## 5. Plan → confirmation → build
Show the plan (catalogue creations, components, choices, lines with positions, tests with expected prices), wait for « oui », then build with the steps of `procedure-construction.md`. Re-read every grid after writing.

## 6. Test
- Reload the engine edit page before testing (the Test page caches the engine), pick the « + 0 % » price group if one exists.
- Run the Excel cases; expected = Excel price before its own display rounding. Tolerance 0,01 € (cent rounding).
- If a line is missing or equals 1, look first at the pitfalls of `procedure-construction.md` « Pièges validés le 17/10/2026 ».

## 7. Finish
Report: engine link, objects created in the catalogue, attributes and what the Pressero script must compute, test table (expected / PJM / chosen material / weight), what PJM cannot reproduce (dates, dynamic validations, display rounding), materials left unused. Save a note of the engine in the Cowork project if one is attached. Optionally offer to import the engine into the Atelier (`importer-moteur-pjm`).
