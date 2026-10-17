---
name: construire-moteur-pjm
description: Builds a new pricing engine in PrintJobManager from a sheet of the Atelier Moteurs PJM marked "Prête à construire", through Claude in Chrome, then runs its test cases. Use when the user says "construis le moteur", "crée le moteur dans PJM", "la fiche est prête", "construye el motor en PJM", "build the engine in PJM", or when a sheet has status "pret".
---

# Build a PJM engine from an Atelier sheet

Load the `moteurs-pjm-expert` skill first (formulas, rules, `references/procedure-construction.md`, `references/scripts-pjm.md`). Answer in the user's language; build the engine in the sheet's language (`language`), never translate PJM names of resources, processes or materials.

## Usage
Before anything else, apply `moteurs-pjm-expert/references/consommation.md`: one task per conversation, estimate shown before starting, reminder at the end.

## Safety
- Never type PJM credentials: if the login page appears, ask the user to sign in and wait.
- Show the build plan and get a clear « oui » before the first write in PJM.
- Never delete anything in PJM. Changing a shared material record (e.g. dimensions / weight) needs the user's explicit approval for that change.

## 1. Read the sheet
- Atelier URL: ask, or Artifact `list`. ArtifactData `query` on `briefs` where `status = "pret"`; if several, ask which one. Read `settings/app.pjmUrl` (fall back to `pjm.instance`, else ask).
- Set the sheet's `status` to `construction` (ArtifactData `update`).

## 2. Plan (show it to the user)
Turn the sheet into a list of PJM objects:
- engine (name, category, description, min/max price, quantity component);
- quantities Q1…, with prompt, min, max, default;
- Options components with their choices (markup %), production lines (resource → process, quantity formula, poses formula) and material lines;
- Material and Calculation components;
- the lead-time Options component (`delays`), one choice per lead time with its markup;
- suppressions from `hideWhen`, `restrictions` (duplicate the target component: full / reduced version), validated `freeRules`, `guided` answers, plus the `select_one_id` rule for forced options;
- weight formulas for materials sold by m² (see expert skill);
- the report position (`Seq`) of every production line, from the shop flow (« Conventions » in `procedure-construction.md`), shown in the plan;
- the order of the questions in the form.
Do not set the integration price group (assigned by PJM from the customer company).
Write each formula from its `basis` (sheets, copies, pages, m², ml, flat, custom) with the expert skill; check parentheses, length ≤ 1400, spaces around `<`. Check that every resource, process and material exists in PJM (`catalog/*` of the Atelier, then the live combobox / `matIds`); report anything missing instead of guessing. If the user asks to create what is missing, add it to the plan and follow « Créer ressources, procédés et matériaux » in `procedure-construction.md`.
Before saving, check every formula against the pitfalls of `procedure-construction.md` « Pièges validés le 17/10/2026 » (scientific literals, poses division, ToQty, weight).

## 3. Build (after confirmation)
Follow the order of `procedure-construction.md` « Étapes et points d'entrée PJM »: create the engine, quantities, components (Forcer une sélection when `forceSelect`), choices (`addOpts`), production (`addProd`), materials (`addMat`), Calculation components, lead times, suppressions (`supp`), then set « Sélectionnez la quantité » (`QuantityDefinition`) and save, and finally order the questions with `orderComponents` (drag-and-drop equivalent) and re-read the order.
Every `addProd` gets its `Seq` from the report-position convention, never 1 by default.
After each component, re-read its grids and compare with the plan (process, formulas, `Seq`); fix silently-failed lines (manual-work processes) before moving on.

## 4. Record the link
ArtifactData `update` on the sheet:
- `pjm = {engineId, url: pjmUrl + "/ProductEngines/Edit/" + engineId, builtAt: ISO date, map}` where `map[componentLocalId] = {pjmId, options:{optionLocalId:{pjmId, productions:[ids], materials:[ids]}}, productions:[…], materials:[…], suppressions:[…]}` (local ids are the `id` fields of the sheet).

## 5. Test
Run every `tests[]` case with the PJM Test page; write `tests[i].last = {price, at, ok}` (`ok` = |price − expected| ≤ 1 % when `expected` is set). If the sheet has no test case, run one with the default quantities and the first choices, and add it as a case with `expected: null`.

## 6. Finish
Set `status` to `cree`. Report in a few lines: engine link, components created, test results (with the price group used by the Test page), anything left to do by hand (missing machines or papers, duplicated materials, rules PJM cannot express such as hiding a choice by quantity). Do not list the price group or the form order as to-do items.
