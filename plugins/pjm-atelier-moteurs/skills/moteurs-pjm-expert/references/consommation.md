# Usage (token consumption) – rules for every action skill

## 1. One task per conversation
Each action (créer l'Atelier, lire le catalogue, construire, importer, mettre à jour) should run in its own Cowork conversation, so that the usage of the conversation equals the usage of the task.
- At the start of an action skill: if the current conversation already contains another PJM task (build, import, update, catalog read), suggest in one sentence to start a new conversation for this task (« pour suivre la consommation tâche par tâche »). Continue if the user prefers.
- At the end: remind in one line that typing « où sont passés mes tokens ? » / « explain my usage » shows the usage of this conversation.

## 2. Estimate before starting
Before the first PJM call, show one short line with the level and what drives it, then continue (no confirmation needed unless the level is « lourd »: then ask « On y va ? »).

| Task | Level | What makes it grow |
|---|---|---|
| Créer l'Atelier | léger | – |
| Lire le catalogue PJM | moyen | number of resources and materials |
| Construire un moteur | moyen → lourd | number of components and choices, long formulas, test cases |
| Importer un moteur | moyen → lourd | number of components, material lines, formulas > 400 characters |
| Mettre à jour un moteur | léger → moyen | number of differences (a full re-read of the engine is always done) |
| Corriger / écrire une formule | léger | – |

Size the level from what is known before starting: number of components / choices in the sheet, or the component list of the PJM engine page (read it first, it is cheap). Rough thresholds: up to 8 components = léger/moyen, 9–20 = moyen, more than 20 or many laize/format lines = lourd.
Measured reference values (share of a Claude plan, one conversation per task; quote them as « environ », never as a promise):
| Task | Measured | Context |
|---|---|---|
| Créer l'Atelier + lire le catalogue (same conversation) | ≈ 5 % | 17/10/2026, 2 resources, 1 192 materials; 46 % of it = fixed instructions |
Other tasks: not measured yet – give the level only.
- If the project instructions hold the Atelier address and PJM address, use them instead of asking or listing artifacts.

## 3. Keep it lean
- Read PJM through grid JSON (scripts-pjm.md), never screenshots, except for UI-only widgets.
- Keep long material formulas in PJM (« [PJM] ») when importing.
- Build JSON in the page and read it once with get_page_text instead of many small reads.
