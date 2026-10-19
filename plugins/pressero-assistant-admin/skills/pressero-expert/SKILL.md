---
name: pressero-expert
description: Expertise on the Pressero (Aleyant) web-to-print admin and storefront, driven through Claude in Chrome. Use when the user asks how something works in Pressero, where a setting lives, or wants to change a Pressero site ("dans Pressero", "admin Pressero", "site B2B / B2C", "head bas", "fiche produit Pressero", "catégorie Pressero", "en Pressero", "Pressero admin"). Also loaded by every other skill of this plugin before it touches Pressero.
---

# Pressero admin – expert knowledge

Answer in the user's language (French, Spanish or English). Use plain words with the user; keep ids and selectors for yourself.

## Golden rules (always)
1. **Never type a password.** If a page shows a login (Pressero admin, PJM, storefront), ask the user to sign in in Claude's own tab, then continue. Never read, copy or display secrets (master site password, carrier credentials, payment keys, API tokens).
2. **Practice site first.** Test new procedures on the user's demo site (e.g. `equipe3`) before a customer site. Ask which site to work on if unclear.
3. **Back up before writing** anything that is not trivially reversible (head scripts: full copy in the admin's `localStorage`, see `scripts-head-pressero`).
4. **Show, then save.** Describe the exact change and get the user's go-ahead before clicking any Save button on a customer site. On the demo site, a general go-ahead for the test is enough.
5. **One change at a time**, then **verify**: reload the admin page (values kept) and check the storefront (rendering, price).
6. **Never click**: Supprimer / Delete (product, category, site), « Nettoyer l'acceptation », the domain HTTP/HTTPS padlock, the red cross / bin in the catalogue organiser, the « Supprimer les produits ne figurant pas dans le fichier Excel » checkbox — unless the user explicitly asks for that exact action.
7. **No file upload from Claude.** The Chrome file-upload tool refuses files Claude creates (tested in session, outputs, connected folder). Claude prepares files in the user's connected work folder (e.g. `Documentos\Pressero Claude`); the user drops them into Pressero.

## Admin map (version 2026.10, French UI)
- Admin: `https://admin.{region}.v6.pressero.com/` (e.g. `admin.ams.v6.pressero.com`). Site pages: `/site/{domain}/{Section}` (e.g. `/site/equipe3.ams.v6.pressero.com/Settings`).
- Site sections: Orders, PendingOrders, **Settings**, **Skins**, SkinCustomize, Widgets, Pages, Navigation, **Categories**, **Products**, **CatalogOperations** (catalogue organiser), Inventory, TagManagement, Filtering, Users, SiteGroups, AdminGroups, ProfileFields, Locations, Departments, Assets, AssetCategories, Promotions, CartLevelDiscount, opencarts, PONumbers, ApprovalPlans, Budgets, GiftCertificates, EmbeddedServices, Notifications, sent, SSO.
- Account-level (all sites): Préférences → Paramètres généraux `/settings`, **Moteur de calcul de prix** `/calculators`, Livraison (Méthodes `/shippingMethods`, transporteurs, caisses), **Calendriers d'entreprise** `/calendars` (jours ouvrés + vacances, date d'expédition), Modes de paiement `/paymentMethods`, eDocBuilder, Profils fiscaux, Formulaires `/forms`, Administrateurs, Flux de travail, Comptes FTP. Sites: « Créez un Site » `/Sites/NewSite`, « Dupliquer un site » `/Sites/DuplicateSite`.
- Storefront: `https://{domain}/product/{UrlName}`, `/category/{UrlName}`. The `<body>` carries `siteType_customer|retail`, `pageType_product|category|…`, `pageName_{url}`.

## B2B vs B2C
- **B2B (Customer site)**: custom HTML/JS only at site level (Settings → SEO/HTML → head bottom, loaded on **every** page) → scripts must guard themselves by path or `body.pageName_…`. Categories also have their own head HTML (SEO tab).
- **B2C (Retail)**: a head HTML field also exists per product.

## Working with the admin UI (techniques that work)
- Most forms are classic MVC pages with **one Save button for the whole page** (`input[type=submit]` value « Sauvegarder »). Success = message « Renseignements enregistrés avec succès. » or redirect to the list.
- Many fields are **Kendo UI** widgets: drive them with `kendo.jQuery('#id').data('kendoXxx')` → `.value(v)` then `.trigger('change')` (DropDownList, NumericTextBox, DateTimePicker, MultiSelect). Rich text = `kendoEditor`: `.value(html)`, `.update()`, `.trigger('change')`. Session grids (tags…): `grid.dataSource.add({...}); await ds.sync()` then page Save.
- The **catalogue organiser** is a Vue + Element UI app: use real clicks (`computer` tool) guided by screenshots.
- Pop-up windows (duplicate product, import/export, edit shipping method) are Kendo iframes whose URL can be opened directly (find it in the button's jQuery click handler: `content: '…'`).
- Plain `<input>`: set `.value` then dispatch `input` and `change`.
- JS tool output is capped (~800 characters) and blocked when it contains URLs with `?&=`: store big results in `window._x` and read slices; strip `?&=`.
- After a `navigate`, call `tabs_context_mcp` before running JS. From an edit page, the first `navigate` may be swallowed (leave-page warning): navigate again and check.
- Pressero storefront pages use two jQuery instances (`window.jQuery` ≠ `kendo.jQuery`): trigger engine events with `kendo.jQuery`.

## PJM link (summary)
- A product is priced by **couples (user group → pricing engine)**. For PJM: engine **APJM** (never APJM2), one couple « Tou le monde » → APJM by default, and the **MIS Product ID** = the PJM engine's **Id de l'intégration** for the chosen PJM price group (PJM → Paramètres → Moteurs de produit → engine → Intégrations). Details: `references/produits.md`. PJM formulas and engines: plugin `pjm-atelier-moteurs`.
- After each calculation Pressero calls `intCalcFinish(e, a)` with the engine's **attributes** (`a.Attributes`) and weight (`a.Weight`, comma string). Scripts must chain this function, never overwrite it. The attribute `SHIP_DAYS` sets the ship date with the company calendar. See skill `recap-attributs-pjm`.

## References (read the one you need)
- `references/head-scripts.md` – SEO/HTML fields, block convention, safe edit procedure.
- `references/produits.md` – product edit tabs, widgets, duplication, pricing couples (APJM), storefront price test, product page DOM for PJM engines.
- `references/import-excel.md` – product Excel import/export: columns, rules, pitfalls (5 groups max, image URL `?stamp=`).
- `references/categories.md` – categories and catalogue organiser.
- `references/parametres-site.md` – site Settings tabs (general, domains, shipping, payment, instructions, content, notifications, SEO, PDF2Press).
- `references/skins.md` – skin files, tags `###…###` / `@@@…@@@`, page types (skins are uploaded by FTP by the user).
- `references/api.md` – Pressero REST API: what it can and cannot do.
- `references/calendriers.md` – company calendars (working days, holidays, repeated vs dated), ship date with `SHIP_DAYS`.
