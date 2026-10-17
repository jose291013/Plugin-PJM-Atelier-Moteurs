---
name: creer-atelier-pjm
description: Creates a new, empty "Atelier Moteurs PJM" app for a print shop (one per customer / PJM instance). Use when the user says "crée l'Atelier pour le client X", "installe l'Atelier Moteurs PJM", "nuevo Taller de motores PJM", "set up the PJM engine workshop", or when another skill of this plugin needs an Atelier and none exists yet.
---

# Create a customer's Atelier Moteurs PJM

Answer in the user's language. The Atelier is the web app where the print shop describes each pricing engine (questions, machines, papers, finishing, lead times, rules, test cases) before Claude builds it in PJM.

## Usage
Before anything else, apply `moteurs-pjm-expert/references/consommation.md`: one task per conversation, estimate shown before starting, reminder at the end.

## Ask first (one AskUserQuestion, skip what is already known)
1. Customer / print-shop name (used in the title: « Atelier Moteurs PJM – {name} »).
2. Base address of their PJM instance (e.g. `https://xxx.printjobmanager.com`). Normalize: add `https://`, remove the trailing `/`.
3. Default language of the Atelier: browser language (recommended), French, Spanish or English.

## Steps
1. Copy `${CLAUDE_PLUGIN_ROOT}/skills/creer-atelier-pjm/assets/atelier-moteurs-pjm.html` into the working directory as `atelier-moteurs-pjm-{customer-slug}.html`. Read the whole file before publishing it. Change only the `<title>` line to `<title>Atelier Moteurs PJM – {name}</title>`.
2. Publish it with the Artifact tool as a NEW artifact (no `url`), `icon: "form"`, a one-sentence description, and exactly these capabilities:
   `{"db": {"rules": [{"path": "catalog", "write": "admin"}, {"path": "questions", "write": "admin"}, {"path": "settings", "write": "admin"}]}, "user": {}, "sample": {}}`
   Load the `artifact-capabilities` skill first if the session requires it.
3. Seed the database with ArtifactData, in one `batch`:
   - `settings/app` = `{"defaultLang": null | "fr" | "es" | "en", "pjmUrl": "<address>", "customer": "<name>", "createdAt": "<ISO date>"}`
   - one `questions/{id}` document per file in `${CLAUDE_PLUGIN_ROOT}/skills/creer-atelier-pjm/assets/questions/` (use `file_path`, document id = the file's `id` field).
   Do not create any `briefs` document: the customer creates their own sheets.
4. Verify with one `list` of `questions` and one `get` of `settings/app`.
5. Offer to read the customer's PJM catalog right away (skill `lire-catalogue-pjm`): the machine and paper lists of the Atelier stay empty until then.
6. Tell the user, in one short paragraph:
   - the Atelier is private: share it from its Share menu;
   - people who fill in sheets must be **Editors** (outside the organization, invite them by email as Editor and do not enable a public link, otherwise they can only read);
   - the « Questions guidées (admin) » screen and the PJM address / default language settings are visible to Editors only.
7. Recommend a light Cowork project « PJM – {name} » (one conversation per task inside it, no documents in the project: the plugin already holds the PJM knowledge). Give the exact text to paste into the project instructions, in the user's language:
   ```
   Atelier Moteurs PJM : {artifact url}
   Adresse PJM : {pjmUrl}
   Langue : {fr|es|en}
   Une tâche PJM par conversation.
   ```

## Updating an existing Atelier to a newer plugin version
When the user asks to update an Atelier (« mets à jour l'Atelier »): read the current artifact (Artifact `read`), keep its `<title>`, replace the rest of the page with the new template, republish to the same `url` (omit `capabilities` unless they changed), then add new guided questions from `assets/questions/` that do not exist yet (never overwrite questions the customer edited: compare `updatedAt` / `source`).
