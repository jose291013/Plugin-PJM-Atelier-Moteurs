# Site head scripts (Settings → SEO / HTML)

Page: `/site/{domain}/Settings`, tab anchor `#seo`. Four plain `<textarea>` (no code editor):

| Label (FR) | id |
|---|---|
| Contenu HTML pour le haut de la page `<head>` | `ContentTopOfHeadSection` |
| **Contenu HTML pour le bas de la section `<head>`** ("head bas") | **`AnalyticsHead`** |
| Contenu HTML pour le haut du `<body>` | `ContentTopOfBodySection` |
| Partager la zone de script | `ContentShareScript` |

The whole Settings page is ONE form with ONE « Sauvegarder » button (`input[type=submit]`): saving re-posts every tab. Never touch other tabs while editing scripts. Grids inside Settings (shipping, payment) are not saved by this button.

## Block convention (user's rule)
Every function is wrapped:
```
<!-- START NOM DE LA FONCTION -->
…style / script…
<!-- END NOM DE LA FONCTION -->
```
Real-life deviations seen on equipe3 (tolerate, report, don't silently fix):
- END shorter than START (`START CHECKOUT : libellé Attention…` / `END CHECKOUT`; `START CREER LIEN FACTURE Order History - stable` / `END CREER LIEN FACTURE`) → match a block by the beginning of its name.
- A closing marker written `START` instead of `END` (fixed on equipe3 on 18/10/2026 at the user's request).
Detection regexes: `/<!--\s*START\s+([^>]*?)\s*-->/g`, `/<!--\s*END\s+([^>]*?)\s*-->/g`.

## Safe edit procedure (validated 18/10/2026)
1. Open `/site/{domain}/Settings`, wait ~3 s, read `document.getElementById('AnalyticsHead').value` (length, markers, positions). Do not print the content (it is long and output is capped).
2. **Backup** in the admin's localStorage: key `claude_backup_AnalyticsHead_{site}_{ISO date with - instead of : .}`; check the stored length equals the field length. Tell the user the key.
3. Locate the block by name; compute start/end positions; abort if anything is ambiguous (two blocks with the same name, missing END).
4. Build the new value = prefix + new block + suffix; check `prefix` and `suffix` are byte-identical to the original; count START/END.
5. Set `ta.value = nv`, dispatch `input`, `change`, `keyup` (+ `jQuery(ta).trigger('change')`).
6. Check the textarea is inside the form of the single visible « Sauvegarder » button, then click it (via `setTimeout(() => b.click(), 50)`).
7. Wait, then check the message « Renseignements enregistrés avec succès. », re-read the field (length, markers).
8. Storefront: open a page concerned, check the new code is in the HTML and works (console without errors, expected DOM).

## Restore
Copy the localStorage backup value back into `#AnalyticsHead`, dispatch events, Save. Ask the user before restoring.

## Writing scripts for the head bottom
- B2B: the code runs on every page → guard by path (`location.pathname`) or `document.body.classList.contains('pageName_xxx')`; scope CSS to classes the script creates or to `body.pageName_xxx`.
- Use `kendo.jQuery` to talk to Pressero widgets (pricing engine listens to jQuery events of that instance). Don't load another jQuery.
- Keep each function in its own START/END block, named in the user's language, upper case like the existing ones.
