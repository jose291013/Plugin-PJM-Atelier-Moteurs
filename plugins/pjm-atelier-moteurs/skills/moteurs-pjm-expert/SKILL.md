---
name: moteurs-pjm-expert
description: Expertise on PrintJobManager (PJM) pricing engines and their NCalc formulas. Use when the user asks to write, check or fix a PJM formula (CalcNup, Nup, floor, Ceiling, poses, feuilles, laize), explains how a PJM engine is structured (Quantity, Options, Material, Calculation components, suppressions, markups), or asks "comment calculer… dans PJM", "fórmula PJM", "PJM formula". Also loaded by the other skills of this plugin before they touch PJM.
---

# PJM pricing engines – expert knowledge

Answer in the user's language (French, Spanish or English).

## Core facts
- PJM formulas use NCalc. Functions: Abs, Ceiling, floor, Min, Max (2 arguments), Round, Pow, Sqrt, Truncate, if(cond, a, b), in(x, a, b…). No variables: repeat sub-expressions. Operators `= == != <> < <= > >= and or not`, `+ - * / %`. Use `4.0` / `1.0 *` to force decimals.
- PJM helpers: `CalcNup(docW, docH, sheetW, sheetH, bleed)` = poses per side; `bleed` is the TOTAL bleed of both sides (3 mm per side → 6); `Nup()` = the result of the same line's « Calcul du nombre de pose » field.
- Quantities: Q1 = copies by convention, then Q2, Q3, Q4… (pages, width, height). Dimensions are entered in the units the engine asks (mm or cm); PJM material dimensions are in mm.
- Engine components: Quantity, Options (choices with « Ajustement global du travail % », Materials lines, Production lines, Attributes), Material (customer picks a material, one formula), Calculation (always applied). « Composants des suppressions » hide a component when another option has a given value (including `--Sélectionner--` = `select_one_id`).
- A formula cannot read an option's answer: duplicate components and hide them with suppressions (e.g. inside printing with and without a separate cover).
- A choice cannot be hidden according to a quantity. Each formula is limited to 1400 characters.
- Quantity names: Q1–Q5, R1–R5, P1–P5, S1–S5 (no Q6). Quantities are integers.
- How PJM uses the poses field (validated 17/10/2026): production line → final quantity = Ceiling(formula / Nup()) (multiply by `Nup()` when the field holds something else; count in cents with a 0,01 € process to avoid rounding to the unit); material line with a formula in poses → quantity not divided; material line with a plain number (e.g. `2`) → divided. In « Calcul du poids », `Nup()` is 1: never use it there.
- Material lines of a choice need ToQty > 0 (999999), otherwise they are ignored; a line whose quantity is 0 does not appear. The weight formula is ignored when the material's WeightPer is 0 (PJM rounds it to 2 decimals: enter it for 1000 items).

## Proven formulas
- Brochure, 4-page blocks, sheets: `Ceiling(Q1 * Ceiling(Q2 / 4.0) / floor(Nup() / 2))`; with a separate 4-page cover: inside `Ceiling(Q1 * Ceiling((Q2 - 4) / 4.0) / floor(Nup() / 2))`, cover `Ceiling(Q1 / floor(Nup() / 2))`.
- Double-sided leaves (perfect bound): `Ceiling(Q1 * Ceiling((Q2 - 4) / 2.0) / Nup())`.
- Cheapest sheet format / roll width: one Material line per format, each returns 0 unless it consumes the least paper; ties go to the smallest format (`<=` against smaller formats, `<` against larger ones). Put the line's own consumption in the poses field and compare with `Nup()` to stay under 1400 characters. Details and full formulas: `references/procedure-construction.md`.
- Banner grommets every 50 cm + 4 corners: `Q1 * (Ceiling((Q2 + Q3) * 2 / 50.0) + 4)`; hem (m): `Q1 * (Q2 + Q3) * 2 / 100.0`; print area (m²): `Q1 * Q2 * Q3 / 10000.0`.
- Weight when the poses field is used for another calculation: fill « Calcul du poids » with `(Q2*10)*(Q3*10)*Q1*Weight` (cm → mm), with the material declared as 1000 × 1000 mm and WeightPer = kg/m².
- Lead times: one Options component « Délais de production », one choice per lead time with its markup %.
- Automatic roll width / format with one material per width (ticket shows the roll to use): poses = selection formula returning the width (220/180/140/100), each line `if(Nup() = 220, …, 0)`; full example in `reprendre-excel-pjm/references/exemple-etiquettes-bobine.md`.
- Forced option still on `--Sélectionner--` must behave like its first choice: add a `select_one_id` suppression wherever the first choice has one.

## Build conventions (details: « Conventions » in `references/procedure-construction.md`)
- Report position (`Seq`) of production lines follows the shop flow: prepress → printing → lamination/varnish → cutting → creasing → folding → binding → large-format finishing → packing. Never leave every line at 1.
- Form order is set at the end of the build with `UpdateCompSequence` (same as PJM drag and drop): quantity, format, dimensions, grammage, paper, printing, finishing, folding, binding, lead times.
- Do not set the integration price group: PJM assigns it from the customer company.
- A component can be hidden by the paper chosen (suppression on a Material component, Value = material Id).

## Rules when writing formulas
- Always put spaces around `<` and `<=` (the PJM server rejects `<Nup()` as HTML).
- Never mix a decimal literal with Ceiling/floor/Sqrt results: `Ceiling(…)*0.9` fails silently (Decimal × Double: production = 1, material missing). Write non-integers in scientific notation: `9E-1`, `45E-1`, `1E6`, `198E-6`.
- Check a non-trivial formula with `reprendre-excel-pjm/scripts/ncalc_sim.py` (Python evaluator + static checks) on many cases.
- Guard divisions: `Max(CalcNup(...), 0.0001)` when a format may not fit.
- Check parenthesis balance and length (≤ 1400) before giving or saving a formula; simulate a few cases when the logic is not trivial.

## References
- `references/procedure-construction.md`: full build procedure, PJM endpoints, pitfalls, test results.
- `references/atelier-donnees.md`: data model of the Atelier app (briefs, catalog, questions, settings).
- `references/ncalc.md`: NCalc syntax summary.
- `references/consommation.md`: usage rules (one task per conversation, estimate before starting, measured values).
- `references/scripts-pjm.md`: verified JavaScript helpers (choices, production and material lines, suppressions, reading an engine, tests, creating resources / processes / materials).
- Skill `reprendre-excel-pjm`: rebuild an Excel / Pressero calculator in PJM.
