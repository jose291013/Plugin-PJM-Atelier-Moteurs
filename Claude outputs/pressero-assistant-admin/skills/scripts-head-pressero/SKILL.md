---
name: scripts-head-pressero
description: Lists, adds, replaces, fixes or removes ONE named script block in the head bottom ("head bas", Settings → SEO / HTML) of a Pressero site, with backup and storefront check. Use when the user says "ajoute ce script dans le head", "mets à jour le bloc … du head bas", "liste les scripts du site", "corrige les balises START/END", "añade el script al head de Pressero", "update the head script block in Pressero".
---

# Head-bottom script blocks

Load `pressero-expert` first and follow its golden rules. Full procedure and selectors: `pressero-expert/references/head-scripts.md`.

## Inputs to settle
- Site (domain, e.g. `equipe3.ams.v6.pressero.com`) and admin host. Ask if unclear.
- Action: list · add · replace · fix markers · remove. Block name (upper case, user's language).
- For add/replace: the code (from the user, from `configurateur-produit-pjm`, or written by Claude). B2B: make sure the code guards itself by page.

## Steps
1. Open `https://{admin}/site/{domain}/Settings`; if a login page appears, ask the user to sign in in Claude's tab.
2. Read `#AnalyticsHead` (never print it whole). List blocks: name, start/end positions, size, anomalies (missing END, END written START, duplicate names, text outside blocks). For "list", report and stop.
3. Back up the full value to `localStorage` (`claude_backup_AnalyticsHead_{site}_{date}`); verify length.
4. Prepare the new value:
   - add → append `\n\n<!-- START {NAME} -->\n{code}\n<!-- END {NAME} -->` at the end (or where the user says);
   - replace → swap only the text between the block's START and END markers (markers kept);
   - fix markers → change only the faulty marker;
   - remove → only on explicit request; remove START…END inclusive.
   Verify prefix/suffix unchanged and START/END counts.
5. Tell the user in plain words what will change (block name, size before/after); on a customer site wait for the go-ahead.
6. Write the value, dispatch events, click the single visible « Sauvegarder », check « Renseignements enregistrés avec succès. », re-read the field.
7. Storefront check on a relevant page: marker present in the page HTML, expected behaviour (e.g. `window.SegmentedPricing` defined, buttons rendered), no console error.
8. Report: what changed, backup key, verification result.

## Never
- Edit another tab of Settings in the same save, reformat other blocks, or "clean up" other people's code without being asked.
- Load a second jQuery in a block.
- Overwrite a global hook another block uses (e.g. `window.intCalcFinish`): wrap and chain it.
