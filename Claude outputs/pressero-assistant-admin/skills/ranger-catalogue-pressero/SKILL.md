---
name: ranger-catalogue-pressero
description: Creates or edits Pressero categories (name, URL, parent, descriptions, SEO, category head HTML, visibility groups) and attaches products to categories in the catalogue organiser, then checks the storefront category page. Use when the user says "crée la catégorie …", "range ces produits dans la catégorie …", "organise le catalogue", "ajoute le produit à la catégorie", "crea la categoría en Pressero", "add these products to a Pressero category".
---

# Categories and catalogue organisation

Load `pressero-expert` first. Details: `pressero-expert/references/categories.md`.

## A. Create / edit a category
1. Open `/site/{domain}/Categories?ignoreSavedState=True`; check the URL is unused (and find the parent's URL).
2. Create: `/site/{domain}/Categories/Create` (edit: `/Categories/Edit/{id}`).
3. Fill `CategoryName`, `UrlName`, `parentCategoryId` (option whose text = parent URL, `root` for top level), short description, long description (kendoEditor), SEO fields / `HeadHtml` if asked, visibility groups (all checked unless told otherwise). Category image: the user uploads it.
4. Click « Sauvegarder » → back to the list; check the new row (name, URL, parent) and note its id.

## B. Attach products (catalogue organiser)
1. Open `/site/{domain}/CatalogOperations?ignoreSavedState=True`; take a screenshot to locate elements.
2. Tick the products in the left list (use its search box for long lists).
3. Click the target category in the tree → the bottom button reads « Add To {category} » → click it → toast « N produits Catégorie ajoutée … ».
4. Click « Sauvegarder toutes les modifications » → toast « Les produits et les catégories ont été sauvegardés avec succès ».
5. Do not use the red × / bin (removal) unless explicitly asked; to reorder, drag the ☰ handles only on request.

## C. Verify
Open `https://{domain}/category/{url}`: products listed, long description shown; top-level categories appear in the automatic menu. Report in plain words.
