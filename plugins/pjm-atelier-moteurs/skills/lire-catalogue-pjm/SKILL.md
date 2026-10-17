---
name: lire-catalogue-pjm
description: Reads a print shop's PrintJobManager catalog (production resources with their processes, material categories and materials) through Claude in Chrome and loads it into their Atelier Moteurs PJM. Use when the user says "relis le catalogue PJM", "mets à jour les machines / papiers de l'Atelier", "lee el catálogo de PJM", "refresh the PJM catalog", after creating an Atelier, or when a sheet references a machine or paper the Atelier does not know.
---

# Read the PJM catalog into the Atelier

Answer in the user's language. This skill is read-only on PJM.

## Usage
Before anything else, apply `moteurs-pjm-expert/references/consommation.md`: one task per conversation, estimate shown before starting, reminder at the end.

## Prerequisites
- The Atelier URL (ask, or find it with Artifact `list`). Read `settings/app` with ArtifactData to get `pjmUrl`; if empty, ask for it and save it (`settings/app.pjmUrl`).
- Claude in Chrome connected. Load the claude-in-chrome skill and its tools in one ToolSearch call. The user must already be signed in to PJM in Chrome: never type credentials. If the page shows the login form, ask the user to sign in and wait.

## Steps
1. Open `{pjmUrl}/Production` in a new tab and wait until the grid is loaded.
2. Run the « resources » script from `references/scripts.md` with the JavaScript tool. It sets the grid page size to 500, fetches every resource's processes and writes a JSON document into a `<pre>` on the page.
3. Read that JSON with `get_page_text` (the JavaScript tool's output is truncated and is blocked when it contains `&` or `x=y` patterns; `get_page_text` is not). Save it to a local file `catalog_resources.json` without changing it.
4. Open `{pjmUrl}/Materials`, run the « materials » script, read the JSON with `get_page_text`, save it as `catalog_materials.json`.
5. Write both to the Atelier with one ArtifactData `batch`: `catalog/resources` and `catalog/materials` (`set` with `file_path`; pass `if_version` when the documents already exist – read them first).
6. Reload the PJM tab (the scripts replaced the page content) or close it.
7. Report: number of resources, processes, material categories and materials, and any change since the previous catalog (new or removed machines / processes) when one existed.

## Expected document shapes (the Atelier depends on them)
- `catalog/resources`: `{"resources":[{"name","dept","kind":"Équipement"|"Travail manuel","processes":[names]}], "source": pjmUrl, "readAt": "YYYY-MM-DD"}`
- `catalog/materials`: `{"categories":[{"category","count","items":[names]}], "total": n, "source": pjmUrl, "readAt": "YYYY-MM-DD"}` – items are listed for categories up to 120 materials; larger categories keep `items: []` and only `count`.
