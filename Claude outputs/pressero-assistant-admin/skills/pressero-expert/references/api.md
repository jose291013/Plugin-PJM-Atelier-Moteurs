# Pressero REST API (V6) – capabilities

Docs: `https://admin.{region}.v6.pressero.com/docs/api/` (apiDoc, 44 groups). Not used by V1 of this plugin (no API account yet); kept for later versions.

- Auth: `POST /api/V2/Authentication` with UserName, Password, SubscriberId, ConsumerID → token; then header `Authorization: token <token>`. Credentials are entered by the user, never by Claude.
- Products: full CRUD `/api/site/{domain}/products` (create, get, get by MIS ID, list, search, search by tags, update, delete). ProductData: ProductInfo (same fields as the admin), ImageUrl (ONE image, downloaded from a URL), Seo, KitComponents, SuggestedProducts, Markups, Categories (Guid[]), AllowedGroups (Guid[]), Attributes, **ProductGroupCalculators** `[{GroupId, CalculatorId, ProductInfo:[{Key:"productID", Value:"<PJM integration Id>"}]}]`, Tags (TagId or TagName + TagValue).
- Calculators: CRUD `/api/Calculators`, methods only Calculator, PriceBreaks, Spreadsheet, Uom (no PJM) → APJM couples reference the existing APJM calculator.
- Categories, Content Pages (ContentHtml, HeadHtml), Site Assets, Site Groups, Site Navigation, Attributes, Tags, Workflows, Users, Orders (38 endpoints), WebHooks…
- Not available: create a site, skins / CSS / layouts, site head scripts → admin UI (and FTP for skins).
