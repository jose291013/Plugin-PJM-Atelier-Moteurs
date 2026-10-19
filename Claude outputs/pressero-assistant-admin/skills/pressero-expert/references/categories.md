# Categories and catalogue organiser

## Categories
- List `/site/{domain}/Categories?ignoreSavedState=True` (Nom, URL, Catégorie parentale). Root = `--RootCategory--` (URL `root`, never modify). Create `/Categories/Create` (button « Ajouter nouveau » `#addNewBtn`), edit `/Categories/Edit/{CategoryId}`. No Excel import/export.
- Form POST `/Categories/Save`; buttons Sauvegarder (→ list), Annuler, Supprimer (never).
- Tabs: Informations générales `#infoPage` (`CategoryName`, `parentCategoryId` = native select showing the **URL** of categories, e.g. `root`, `Rollup`; `UrlName`) · Description longue `#longDescriptionPage` (`#pressero-editor` kendoEditor, shown at the top of the category page) · Description courte `#shortDescriptionPage` (`#ShortDescription`, shown in the category tile on the parent page) · SEO `#seoPage` (SeoInfo_Title, _Author, _ContentLanguage, _Robots, _Copyright, _RevisitAfter, _Description, _Keywords, **`HeadHtml`** = head HTML of this category only) · Illustration `#artworkPage` (`input[type=file]#logo` → user uploads) · Groupes `#siteGroupsPage` (`SiteGroups_{groupId}` checkboxes).
- Fill plain fields with `.value` + `input`/`change`; select parent by matching option text to the parent's URL.
- Storefront `/category/{UrlName}`; new top-level categories appear in the automatic category menu.

## Catalogue organiser `/site/{domain}/CatalogOperations?ignoreSavedState=True`
Vue + Element UI app → real clicks with screenshots (take one first; coordinates change with the window).
- Left « Produits »: search, filter, each product shows how many categories it belongs to (green ≥ 1, red 0) and a checkbox. Bottom bar: « N Sélectionné » + action button.
- Right « Categories »: tree with product counts, search, expand buttons (levels 2/3/4). Clicking a category selects it and opens its product panel below (drag handle ☰ to reorder, red × to remove, red bin to remove all — don't use without explicit request).
- **Attach products**: tick products on the left → click the target category → the bottom button becomes « Add To {category} » → click → toast « N produits Catégorie ajoutée "…" » → click **« Sauvegarder toutes les modifications »** (bottom right) → toast « Les produits et les catégories ont été sauvegardés avec succès ». Nothing is saved before this last click.
- Without a selected category the bottom arrow does nothing. A product may belong to several categories.
- Verify on `/category/{url}` (products listed).
