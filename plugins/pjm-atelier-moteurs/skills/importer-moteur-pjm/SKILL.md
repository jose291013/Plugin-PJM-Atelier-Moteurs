---
name: importer-moteur-pjm
description: Imports an existing PrintJobManager pricing engine into the Atelier Moteurs PJM as an editable sheet (questions, choices, machines, formulas, materials, suppressions, lead times), read-only on PJM. Use when the user says "importe le moteur", "reprends mon moteur existant", "importa el motor PJM", "import this PJM engine", pastes a /ProductEngines/Edit/ address, or when a sheet has status "import".
---

# Import an existing PJM engine into the Atelier

Load the `moteurs-pjm-expert` skill first. Answer in the user's language. This skill only reads PJM.

## Usage
Before anything else, apply `moteurs-pjm-expert/references/consommation.md`: one task per conversation, estimate shown before starting, reminder at the end.

## Steps
1. Get the engine: a sheet with `status = "import"` (its `pjm.engineId`, `pjm.url`), or an address `/ProductEngines/Edit/{id}` given by the user (then create the sheet: ArtifactData `set` on `briefs/{new id}` with the empty shape described in `atelier-donnees.md`, `status: "import"`).
2. Open the engine in Chrome (user signed in) and read it with « Reading an engine » of `scripts-pjm.md`: engine fields; quantities (code, name, prompt, min, max, default); Options (name, prompt, forced, hidden, choices with markup, production lines resource/process/formulas, material lines); Material components (materials, formulas); Calculation components; suppressions.
3. Fill the sheet:
   - `components[]` with local ids (8 random lowercase characters), `hideWhen` from suppressions (ignore `select_one_id` suppressions that duplicate the first-choice rule);
   - production steps: recognize standard formulas and set `basis` (copies, sheets, pages, m2, ml, flat); anything else → `basis: "custom"` with the original formula in `formula`;
   - an Options component whose choices only carry a markup and no lines (e.g. « Délais de production ») → `delays` (`enabled: true`, choices with label and markup);
   - `language` from the engine's texts; `productType` and `pjmCategory` from the category;
   - `pjm = {engineId, url, importedAt: ISO date, map}` with every PJM id read.
4. Write the sheet (ArtifactData `set` or `update`), then set `status` to `cree`.
5. Optionally run one test case with default values and store it in `tests[]` with its price as `expected`, so a later update can be checked against today's price.
6. Report what was imported and anything the Atelier cannot represent (listed in `notes`).
