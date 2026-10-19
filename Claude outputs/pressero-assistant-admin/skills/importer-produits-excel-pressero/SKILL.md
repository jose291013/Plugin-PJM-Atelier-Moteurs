---
name: importer-produits-excel-pressero
description: Prepares a Pressero product import Excel file (bulk update or creation of products, PJM pricing couples, descriptions, groups, image URL) from a fresh export, has the user import it, then checks every imported product. Use when the user says "mets à jour ces produits par Excel", "crée ces produits par import", "prépare le fichier d'import Pressero", "importa productos en Pressero", "bulk update Pressero products", or uploads a Pressero product export (.xlsx with columns Product Id, Url Name, Pricing Engine price 1…).
---

# Bulk products by Excel

Load `pressero-expert` first. Format and pitfalls: `pressero-expert/references/import-excel.md`. Helper: `scripts/prepare_import.py`.

## Steps
1. **Fresh export**: ask the user for a recent export of the site (Products → Import/Export → « Exporter maintenant ») attached to the chat or saved in the connected work folder. Never build a file from an old export.
2. **Plan**: list the rows to update (by Product Id) and to create (empty Product Id), and the columns to change. Keep only those rows; never change other columns.
3. **Checks before writing**:
   - products with more than 5 checked groups in the admin (open the product → Groupes) → exclude, or plan to re-check groups after import;
   - more than 5 pricing couples or suggested products → exclude;
   - `Primary Image URL`: remove `?stamp=…`; must be a public URL;
   - creation: empty Product Id and the 4 date columns, unique Url Name; PJM couple = `Tou le monde` / `APJM` / integration Id.
4. **Build** the file with `scripts/prepare_import.py` (or openpyxl, keeping the header row and sheet as exported). Save it in the connected work folder (e.g. `Documentos\Pressero Claude`) and attach it to the chat; summarise rows and changes in plain words.
5. **Import by the user**: ask them to open Products → Import/Export, leave « Supprimer les produits ne figurant pas dans le fichier Excel » UNCHECKED, drop the file, click « Importer maintenant », and paste or screenshot the import report.
6. **Read the report**: Added / Updated / Failed + errors. Fix failing rows (typical: image URL) and produce a corrected file if needed.
7. **Verify**: product count in the list; each imported product (name, URL, pricing couple, groups, descriptions); storefront price test for PJM products; re-check groups of products that had 6+ groups.
8. Report and record new ProductIds in the user's project notes.
