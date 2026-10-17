---
name: mettre-a-jour-moteur-pjm
description: Updates an existing PrintJobManager engine after its Atelier sheet was changed (new options, choices, machines, papers, lead times, rules), applying only the differences through Claude in Chrome. Use when the user says "mets à jour le moteur", "ajoute une option au moteur existant", "actualiza el motor PJM", "update the PJM engine", or when a sheet has status "maj".
---

# Update an existing PJM engine from its sheet

Load the `moteurs-pjm-expert` skill first. Answer in the user's language. Same safety rules as `construire-moteur-pjm`: no credentials, confirmation before writing, **never delete in PJM without an explicit « oui » for each deletion** (and propose hiding with a suppression as an alternative).

## Usage
Before anything else, apply `moteurs-pjm-expert/references/consommation.md`: one task per conversation, estimate shown before starting, reminder at the end.

## Steps
1. Find the sheet (`briefs` with `status = "maj"`, or the one the user names). It must have `pjm.engineId`; if not, offer `importer-moteur-pjm` or `construire-moteur-pjm`.
2. Read the real engine in PJM (read-only, « Reading an engine » in `scripts-pjm.md`): components, choices, production and material lines with formulas, suppressions, lead times.
3. Compare the engine with `pjm.map` from the last build/import: anything changed directly in PJM since then is a manual edit. List these to the user and ask whether the sheet should take them over or the sheet wins.
4. Compare the sheet with the engine and produce the list of differences: additions, modifications (same Id, new values), deletions. Present it grouped by component and wait for confirmation.
5. Apply only the confirmed differences:
   - additions: `addOpts`, `addProd`, `addMat`, `supp`, new components;
   - modifications of a line (validated 17/10/2026): same endpoint with the existing line Id – material: `SaveComponentMaterial` with `Id = line Id`; production: `SaveComponentProduction` with `ComponentProductionId = line Id` (answers « correctement mise à jour », no duplicate). Resend every field of the line, not only the changed one;
   - new choices on a forced option: re-check the `select_one_id` suppressions.
6. Re-read the grids, update `pjm.map` and `pjm.builtAt` (ArtifactData `update`).
7. Run all test cases, write `tests[].last`, report differences against `expected` and against the previous `last`.
8. Set `status` to `cree` and summarize the changes made in PJM.
