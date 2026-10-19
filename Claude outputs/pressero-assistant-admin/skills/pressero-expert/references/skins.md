# Référence condensée : skins Pressero (Aleyant)

Source : « Aleyant Skinning Technical Guide », https://presserolibrary.chi.v7.pressero.com//files/skins/docs/ (pages overview, tools, files, pagetypes, checkout, productfilter, tags), lue le 17/10/2026.
Les éléments marqués **[hors doc]** ne figurent PAS dans la doc officielle ; ils viennent de l'analyse du skin local `nietoResponsive6` (doc projet `claude/skin-pressero-structure.md`).

Abréviations des fichiers de mise en page utilisées plus bas :
L = layout.txt · C = categorylayout.txt · PD = productdetail.txt · CP = contentpagelayout.txt · OS = ordersummarylayout.txt · E = edoclayout.txt · QV = productquickviewlayout.txt (ProductQuickViewLayout.txt)
Types de site : I = Informational, R = Retail (B2C), C = Customer (B2B).

---

## 1. Vue d'ensemble

- **Skin** : design propre à un site, une boutique ou un portail client. C'est un dossier sur le serveur Aleyant contenant des fichiers (certains obligatoires) qui décrivent la mise en page (.txt/.inc), le style (.css) et le comportement (requirements.xml, JS). Pressero reconnaît et lit automatiquement les fichiers déposés dans le dossier du skin.
- **Skinning tags** : chaînes placées dans les fichiers de mise en page et remplacées par du HTML à l'analyse.
  - Syntaxe : `###NOM###` ou `###NOM, param1, param2###` (paramètres séparés par des **virgules**).
  - Version JSON (moderne, à privilégier) : `###NOM_JSON, {cle: 'valeur', ...}###`.
  - **Sous-tags** (dans un paramètre d'un tag) : `@@@NOM@@@` ou `@@@NOM:arg1:arg2@@@` (paramètres séparés par des **deux-points**).
  - CSS : `@ShadeN@` = couleur N de la palette de requirements.xml.
- **Connaissances requises** : XHTML, CSS, XML, standards web.
- **Outils** : éditeur de texte, client **FTP**, navigateur. Recommandés par la doc : Coda / Transmit (Mac), Sublime Text / SmartFTP (Windows), Chrome. Tester sur tous les navigateurs majeurs.
- **Encodage** : requirements.xml se corrompt facilement : l'enregistrer en ASCII ou au plus **UTF-8** (jamais UTF-16). Après envoi, vérifier qu'il se télécharge : `http://orderingplatform.com/files/skins/{skinid}/requirements.xml`.

## 2. Fichiers d'un skin

**Emplacement / téléversement** : les fichiers sont envoyés **par FTP** dans le dossier du skin sur le serveur. Avec plusieurs skins, chaque skin est un dossier au nom hexadécimal (GUID, ex. `3A8D5BC2-2954-4140-AC12-...`) ; avec un seul skin, on peut ne pas voir ces dossiers. URL publique du dossier : `.../files/Skins/{SKINGUID}/` (cf. `###SKINPATH###`, `###SITEINFO, skin-id###`). Les images d'admin ajoutées via la page Skins vont dans un autre répertoire (`skin-images-directory`).

Règle : HTML en .txt et .inc, style dans au moins un layout.css. On peut créer autant de .inc et .css que voulu, mais **les noms de .txt sont limités à la liste ci-dessous**.

| Fichier | Obligatoire ? | Rôle | Remarques |
|---|---|---|---|
| `layout.txt` | **Oui** | Gabarit maître de toutes les pages (head, en-tête, pied, includes). | Doit contenir `###CONTENTAREA###` (une seule fois). Seul fichier où marchent `###INCLUDE###`/`###HEADINCLUDE###`. |
| `layout.css` | **Oui** (la page Files dit « Required » ; la section Layout.css dit « optional » : traiter comme obligatoire) | Style de tout le site. | Peut utiliser `@ShadeN@`. Éviter le style inline et le CSS dans le head de layout.txt. Ne jamais cibler d'id commençant par `ctl00` (ids ASPX qui changent). |
| `requirements.xml` | **Oui** | Manifeste du skin : notes, palette, images, flux RSS/Twitter, CSS/JS par défaut ou bibliothèques, emplacements de widgets, options du skin, isResponsive, useCheckoutCSS. | Encodage UTF-8 max. Détail ci-dessous. |
| `categorylayout.txt` | Non | Mise en page des pages catégorie (`/category`, `/category/x`) : description, sous-catégories, produits. | Requiert `###CATEGORYITEMLAYOUT###`, `###PRODUCTITEMLAYOUT###`, `###PRODUCTS###`, `###SUBCATEGORIES###` (à placer en haut pour les *LAYOUT). |
| `productdetail.txt` | Non | Fiche produit (`/product/nom`). C'est là que s'affiche le moteur de prix (`###PRICING###`). | Tags obligatoires : ADDTOCARTBUTTON, PRICING, CUSTOMFIELDS, FULLPRODUCTDESCRIPTION, SHORTPRODUCTDESCRIPTION, ORDERNOTESBOX, RENAMEITEM, DOWNLOADASSET. **[hors doc]** le skin local contient aussi `v6/productdetail.txt`, version utilisée en V6. |
| `ProductQuickViewLayout.txt` (productquickviewlayout.txt) | Non | Fenêtre modale « aperçu rapide » d'un produit (`?mode=quickview`, en iframe). | Sous-ensemble des tags de PD. **[hors doc]** existe aussi sous `v6/`. |
| `contentpagelayout.txt` | Non | Pages de contenu (`/page/nom`). | `###CONTENT###` ; si formulaire : `###FORM###` + `###CAPTCHA###` (après FORM) + `###SUBMIT###`. |
| `edoclayout.txt` | Non | Page de personnalisation eDocBuilder (`/customize`). | Tags obligatoires : APPROVEBUTTON, APPROVECHECKBOX, CANCELBUTTON, PAGESELECTOR, PREVIEWIMAGES, SAVEFORLATERBUTTON, UPDATEBUTTON, UPDATEREQUIRED. |
| `ordersummarylayout.txt` | Non | Récapitulatif de commande (`/summary/numero`). | Tags obligatoires : ITEMS, NOTES, ORDERDATE, ORDERFORM, PROMODISCOUNT. |
| `print.css` | Non | Style à l'impression. | |
| `*.inc` | Non | Fragments HTML insérés par `###INCLUDE, f.inc, pages###` (dans le body) ou `###HEADINCLUDE, f.inc, pages###` (dans le head). | La plupart des tags ne fonctionnent PAS dans un .inc (voir colonne « inc » au §6) ; exceptions : SKINPATH, SITEPATH, TEXT, SITEINFO, USERINFO, LINK, IMAGE, LOCATION_JSON, NAVIGATION_JSON, SITELOGO*, SUBSCRIBERLOGO*, FEATUREDPRODUCT_JSON, RSS_JSON, TWITTER_JSON, PRODUCTFILTER_JSON. |
| `images/` (dossier) | Non (mais requis si `<imageEntry>`) | Images par défaut et bibliothèque d'images proposées dans l'admin. | Chaque image `X.png` doit avoir un aperçu `X.png_preview.png` (largeur max 300 px) et respecter la taille de l'imageEntry. |
| Autres .css / .js | Non | CSS/JS supplémentaires. | Chargés via `<cssLibraryURLs>`/`<jsLibraryURLs>` ou référencés dans un .inc avec `###SKINPATH###`. |
| `layout.uncompressed.css`, `src/…` | **[hors doc]** | Non mentionnés par la doc officielle. Dans le skin local : versions source (non minifiées) du CSS. | Seul `layout.css` est lu par Pressero (nom imposé). Toute modification d'une source doit être reportée/recompilée dans `layout.css`, sinon elle n'a aucun effet. |
| `v6/…` | **[hors doc]** | Non mentionné par la doc officielle. Dans le skin local : `v6/productdetail.txt`, `v6/productquickview…` utilisés par l'interface produit V6. | Modifier la version `v6/` (et la racine par cohérence). |

### requirements.xml : balises (namespace `xmlns="http://w2p.aleyant.com/"`, racine `<skinRequirements>`)

| Balise | Requis ? | Multiple ? | Rôle |
|---|---|---|---|
| `<designerNotes>` | Oui | Non | Notes pour l'utilisateur. |
| `<rssFeed>` | Oui | Non | URL du flux RSS affiché. |
| `<twitterFeed>` | Oui | Non | Compte Twitter affiché. |
| `<palette>` | Oui | Non | Contient les `<paletteEntry>`. |
| `<paletteEntry>` (`<description>`, `<defaultRGB>#111111</defaultRGB>`) | Oui | Oui | Couleur modifiable dans l'admin ; la N-ième entrée = `@ShadeN@` dans layout.css. **L'ordre compte.** |
| `<useDefaultCSS>` | Oui | Non | true/false : CSS par défaut Aleyant. |
| `<useDefaultJS>` | Oui | Non | true/false : JS par défaut Aleyant. |
| `<cssLibraryURLs><string>…` | Non | Non | Avec useDefaultCSS=false : feuilles ajoutées dans le head, dans l'ordre. |
| `<jsLibraryURLs><string>…` | Non | Non | Avec useDefaultJS=false : scripts ajoutés en bas de page, dans l'ordre. |
| `<telerikSkin>` | Oui (obsolète, non utilisé) | Non | Laisser `Default`. |
| `<images>` / `<imageEntry>` (`description`, `width`, `height` (0 = libre), `defaultImageName`, `imageLibrary/string`) | Oui / Oui (multiple) | | Choix d'images dans l'admin ; la N-ième = `###IMAGE_JSON, {image_number: N}###`. |
| `<imageLibrary>` (niveau racine) | Non | Non | Images proposées au widget bannière. |
| `<locations>` / `<locationEntry>` (`name`, `nameResourceKey`) | Non | Oui | Expose un emplacement de widget (ex. Home Page Banner) ; à coupler avec `###LOCATION_JSON###`. |
| `<isResponsive>` | Non | Non | true ajoute la classe `isResponsive` au body. |
| `<options>` / `<optionEntry id="…">` | Non | Non | « Additional Skin Options » dans l'admin. `id` : lettres seulement. Enfants requis : `description`, `type` (checkbox/number/string), `label`, `defaultValue`, `usage` (`class` = classe sur body ; `css` = règle `.skinsetting-{id}{valeur}` dans le head ; `json` = propriété JS dans un script du head) ; `trueValue`/`falseValue` pour checkbox. |
| `<useCheckoutCSS>` | Non (défaut true) | Non | false = Pressero n'injecte plus checkout.css (voir §4). |

## 3. Types de pages et classes CSS (bref)

- Chaque page a un type, visible dans l'URL et sur le `<body>` (classes `xxxPage`, ainsi que `pageType_xxx` et `pageName_xxx` utilisées par les skins, ex. `.pageName_shipping`, `pageType_category`).
- Principales URL : `/login`, `/category`, `/product/nom`, `/cart`, `/checkoutNew`, `/settings`, `/orders`, `/summary/n`, `/page/nom`, `/search/search?text=`, `/customize`, `/savedforlater`, `/sitemap`, `/inventory`, `/preview`, `/webforms/printestimate.aspx?prdurl=` (iframe), `/product/nom?mode=quickview` (iframe).
- Classes body : `.categoryPage .productPage .loginPage .lostPasswordPage .createAccountPage .cartPage .checkoutPage .guestCheckoutPage .savedForLaterPage .ordersPage .orderSummaryPage .contentPage .searchPage .previewPage .printEstimatePage .quickViewProductPage .quickViewCartPage .settingsPage .addressFormPage .inventoryPage .proof*Page .reportsPage .errorPage …`
- Toutes les pages (y compris iframes devis/aperçu rapide) doivent être stylées dans layout.css.

## 4. Nouveau checkout

- Pages modifiées (nouvelle structure HTML) : **cart, checkout, payment**. Pages nouvelles : **access, shipping, pending orders list, pending order details**.
- Pressero injecte par défaut un **checkout.css** global pour que les skins personnalisés ne cassent pas.
- `<useCheckoutCSS>false</useCheckoutCSS>` dans requirements.xml : désactive l'injection ; le skin doit alors styler lui-même toutes ces pages.
- Améliorations conseillées : masquer la barre latérale sur les nouvelles pages (ex. `.pageName_shipping #main-sidebar{display:none}` et contenu pleine largeur) ; passer **Font Awesome en 4.7** (icônes des boutons dupliquer/enregistrer/supprimer/modifier du panier).

## 5. Filtre de produits

- Tag : `###PRODUCTFILTER_JSON, {container_class, container_id, prefix, suffix}###` dans **categorylayout.txt**. Il ne produit qu'un `div` vide avec `data-category-id` et des textes localisés (`data-show-more-text`, `data-show-less-text`, `data-search-text`, `data-apply-text`, `data-selected-text`, `data-clear-all-text`). **Il faut du JS** pour l'afficher.
- Les skins Aleyant appellent le plugin jQuery : `if ($("body").hasClass("pageType_category")) $(".product-filter").productFilter({onNoData, onLoadFailed})` (en cas d'absence de données/échec, cacher le panneau `.sidebar-panel`).
- Données : `GET /getCategoryFilters?categoryId=…` -> `{items:[{filterName, values:[{label, productCount}]}], success}`.
- Application : paramètre d'URL `filters` = JSON encodé `{"NomFiltre":["label1","label2"]}` ; le numéro de page `/category/x/N` est retiré lors de l'application.
- Options du plugin : `showMoreThreshold` (6), `searchThreshold` (6), `showMoreText`, `showLessText`, `searchPlaceholderText`, `applyButtonText`, `selectedText`, `clearAllText`, `enableClearAll` (true), `defaultFilterState` ('collapsed'|'expanded'), `breakpoints` ({992:'expanded'}), `onNoData`, `onLoadFailed`. Priorité : options > data-attributes > défauts. Méthode `$.fn.productFilter.destroy`.
- Classes générées (à styler) : `.product-filter-item`, `.product-filter-item__header`, `.product-filter-item__content`, `.filter-toggle-icon` (fa-plus/fa-minus), `.filter-search-input`, `.filter-checkboxes`, `.filter-label-text`, `.filter-product-count`, `.filter-show-more`, `.filter-show-count`, `.btn-apply-filter`, `.filter-clear-container`, `.selected-count`, `.btn-clear-filter`.

## 6. Skinning tags

Colonnes : **Où** = fichiers autorisés ; **M** = utilisable plusieurs fois ; **Inc** = utilisable dans un .inc ; **Sites**. REQ = obligatoire dans son fichier. DEPR = obsolète (remplacé par la version JSON ou supprimé) : ne pas l'ajouter dans un nouveau code, mais ne pas le supprimer d'un skin existant sans le remplacer.
Paramètres « prefix, suffix » = HTML ajouté avant/après la sortie (le tag ne produit rien si vide).

### 6.1 Structure globale et utilitaires (layout.txt et partout)

| Tag | Où | M/Inc | Paramètres clés | Rôle |
|---|---|---|---|---|
| `###CONTENTAREA###` REQ | L | N/N | aucun | Zone de contenu principal de toutes les pages. |
| `###INCLUDE, file, page###` | L | O/N | `file`* (.inc), `page`* : noms de pages séparés par `\|`, joker `*`, regex, `_all_`, `_startPage_`, `page` (pages de contenu), `product` | Insère un .inc à cet endroit. |
| `###HEADINCLUDE, file, page###` | L | O/N | idem | Insère un .inc dans le `<head>`. |
| `###LOCATION_JSON, {name, display}###` | tous | O/O | `name`*, `display`* (comme `page` : `_all_`, `_startPage_`, nom) | Emplacement de widget (ex. bannière) ; doit correspondre à un `<locationEntry>`. |
| `###ANALYTICS###` | L | N/N | aucun | Code analytics de l'admin (Site > Settings > SEO/HTML). |
| `###CONTENTSHARELINKS, prefix, suffix###` | L | N/N | | Script de partage (admin SEO/HTML). |
| `###SKINPATH###` | L | O/O | aucun | Chemin du dossier du skin (pour CSS/JS/images du skin). |
| `###SITEPATH###` | L | O/O | aucun | Chemin du dossier images du subscriber. |
| `###SITEINFO, clé###` | tous | O/O | clés : site-name, site-tagline, home-url, continue-shopping-url, catalog-url, skin-directory, skin-images-directory, skin-images, site-logo, site-type, site-host, site-origin, query-string, site-timezone, site-culture, subscriber-culture, subscriber-id, skin-id | Infos du site en texte brut. |
| `###USERINFO, clé###` | tous | O/O | fullname, firstname, lastname, login, email, fax, phone, title, lastlogin, lastorder, locaddress1-3, locbusiness, loccity, loccountry, locemail, locpostal, locstateprovince, locfax | Infos de l'utilisateur connecté. |
| `###TEXT, clé###` (sous-tag `@@@TEXT:clé@@@`) | tous | O/O | address, addtocart, cart, cartItems, categories, checkout, contactinfo, createaccount, details, display, featured, featuredProducts, history, items, login, logout, menu, myaccount, news, of, open, orderHistory, price, products, qty, quantity, recenthistory, resources, rss, saved, searchsite, seemore, settings, shop, shoppingCart, showing, sortby, totalitems, twitter, view, viewCart, viewDetails, viewItems, viewShoppingCart, visitor, welcome, welcomevisitor (+ select, partnumber… vus dans les exemples) | Texte localisé. |
| `###LINK, pagetype, pathOnly###` | tous | O/O | `pagetype`* : home, login, address, orderhistory, cart, settings, rss ; 2e param = `pathOnly` (chemin seul) ou texte du lien | Lien/chemin vers une page système. |
| `###IMAGE_JSON, {…}###` (aussi `###IMAGE, {…}###`) | tous | O/O | `image_number` (N-ième imageEntry), `return_type` (path/name/tag), `tag_alt`, `tag_title`, `tag_class`, prefix, suffix | Image choisie dans l'admin Skins. |
| `###IMAGE, n, pathOnly, width, height, defaultImage, cssClass, altText###` DEPR | tous | O/O | | Ancienne version. |
| `###SITELOGO_JSON, {…}###` | tous | O/O | `size` (small, smallsquare, medium, mediumsquare, large, xlarge), `alt`, `title`, `class`, `id`, `url_only`, prefix, suffix | Logo du site/boutique. |
| `###SITELOGO, size, alt/title, prefix, suffix###` DEPR | L | O/O | | |
| `###SUBSCRIBERLOGO_JSON, {…}###` | tous | O/O | mêmes clés que SITELOGO_JSON | Logo de l'imprimeur (sites B2B). |
| `###SUBSCRIBERLOGO, size, prefix, suffix###` DEPR | L | O/O | | |
| `###TAGLINE, prefix, suffix###` | L | N/N | | Slogan (Settings > General Info). |

### 6.2 Navigation, recherche, compte (layout.txt)

| Tag | Où | M/Inc | Paramètres clés | Rôle |
|---|---|---|---|---|
| `###NAVIGATION_JSON, {…}###` | L | O/O | `menu_number`* (1-4), container_class, container_id, active_class, dropdown_class, dropdown_container_class, dropdown_anchor_class, dropdown_anchor_before/after, page_type_class, page_name_class, prefix, suffix | Menu n°1-4 défini dans l'admin. |
| `###NAVIGATION, n, orientation, prefix, suffix###` DEPR | L | O/N | | |
| `###SITESEARCH_JSON, {…}###` | L (non précisé par la doc) | N/N | placeholder, button_text, input_class, button_class, input_first, input_prefix/suffix, button_prefix/suffix, panel_class, prefix, suffix | Champ de recherche. |
| `###SITESEARCH, input text, button text###` DEPR | L | N/N | | |
| `###SITEMAPNAV, pagetype, prefix, suffix###` | L | O/N | pagetype : contentpage, productpage, categorypage | Liste de toutes les pages d'un type. |
| `###RECENTHISTORY_JSON, {…}###` | L | N/N | maxitems, maxhours, prefix, suffix | Historique de navigation. |
| `###RECENTHISTORY, maxItems, prefix, suffix, maxHours###` DEPR | L | N/N | | |
| `###CREATEACCOUNTLINK, prefix, suffix, cssClass, linkText###` | L | O/N | linkText remplace le texte localisé | Lien « Créer un compte ». |
| `###FOOTERMODULE_JSON, {prefix, suffix}###` | L | N/N | prefix, suffix | Contenu du pied de page de l'admin. |
| `###FOOTERMODULE, prefix, suffix###` DEPR | L | N/N | | |
| `###CONTACTBLOCK_JSON, {…}###` | C (selon doc) | N/N | heading, heading_text, layout (`@@@CBHEADING@@@`, `@@@CBCONTENT@@@`), prefix, suffix | Bloc contact de l'admin. |
| `###CONTACTBLOCK, prefix, suffix###` DEPR | L | O/N | | |
| `###RSS_JSON, {…}###` | L | N/O | maxitems, feedmaxlength, feedTitlePrefix/Suffix, feedDescriptionPrefix/Suffix, prefix, suffix | Flux RSS (URL dans requirements.xml). |
| `###RSS, url, max, prefix, suffix, heading, length###` DEPR | L | N/N | | |
| `###TWITTER_JSON, {…}###` | L | O/O | userName, maxitems, datePrefix/Suffix, messagePrefix/Suffix, prefix, suffix | Fil Twitter. |
| `###TWITTER, userName, maxTweets, prefix, suffix, heading###` DEPR | L | N/N | | |

### 6.3 Panier (layout.txt)

| Tag | Où | M/Inc | Paramètres clés | Rôle |
|---|---|---|---|---|
| `###CARTCOUNT_JSON, {prefix, suffix}###` | L | O/N | | Nombre d'articles du panier. |
| `###CARTCOUNT###` DEPR | L | O/N | | |
| `###CARTCOST_JSON, {…}###` | L | O/N | showOnEmpty, emptyText, prefix, suffix | Montant du panier. |
| `###CARTCOST, prefix, suffix###` DEPR | L | O/N | | |
| `###CARTITEMS_JSON, {…}###` | L | N/N | maxItems, showFooterLayout, showCountLayout, showLatestAdded, itemLayout (`@@@IMAGEURL:taille@@@ @@@NAME@@@ @@@URL@@@ @@@COST@@@`), countLayout (`@@@TEXT@@@ @@@SHOWCOUNT@@@ @@@CARTCOUNT@@@`), footerLayout (`@@@TEXT@@@ @@@CARTCOST@@@`) | Mini-panier. |
| `###SAVEDFORLATERCARTCOUNT###` | L | N/N | | Nombre d'articles « enregistrés pour plus tard ». |

### 6.4 Page catégorie (categorylayout.txt)

| Tag | Où | M/Inc | Paramètres clés | Rôle |
|---|---|---|---|---|
| `###CATEGORYITEMLAYOUT, layout###` REQ | C | N/N | sous-tags `@@@CATEGORYIMAGE:taille:taillerel@@@`, `@@@CATEGORYNAME@@@` (avec lien), `@@@CATEGORYSHORTDESCRIPTION@@@`, `@@@CATPATH@@@`, `@@@CATNAME@@@`, `@@@CATIMAGEPATH:taille@@@`, `@@@SKINPATH@@@`, `@@@TEXT:clé@@@` | Gabarit d'une vignette catégorie (en haut du fichier). |
| `###PRODUCTITEMLAYOUT, layout###` REQ | C | N/N | `@@@PRODUCTIMAGE:taille:taillerel@@@`, `@@@PRODUCTNAME@@@`, `@@@PRODUCTSHORTDESCRIPTION@@@`, `@@@PRODUCTATTRIBUTE:nom@@@`, `@@@QUICKVIEW@@@`, `@@@TEASERPRICE:prefix:suffix:texte@@@`, `@@@TEXT:clé@@@` (+ PRODNAME, PRODUCTPATH… vus dans les skins) | Gabarit d'une vignette produit. |
| `###PRODUCTS, prefix, suffix###` REQ | C | N/N | prefix, suffix, altinner (div/li), altclass | Liste des produits de la catégorie. |
| `###SUBCATEGORIES, prefix, suffix###` REQ | C | N/N | | Liste des sous-catégories. |
| `###CATEGORYNAME_JSON, {prefix, suffix}###` | C | N/N | | Nom de la catégorie. |
| `###CATEGORYNAME###` DEPR | C | N/N | | |
| `###CATEGORYDESCRIPTION_JSON, {prefix, suffix}###` | C | N/N | | Description longue. |
| `###CATEGORYDESCRIPTION###` DEPR | C | N/N | | |
| `###CATEGORYSHORTDESCRIPTION_JSON, {prefix, suffix}###` | C | N/N | | Description courte. |
| `###CATEGORYPRODUCTCOUNT, prefix, suffix###` | C | O/N | | Nombre de produits. |
| `###PRODUCTPAGER_JSON, {…}###` | C | O/N | products_per_page, prev_indicator, next_indicator, list_class, show_prev_and_next, active_class, prev_class, next_class, prefix, suffix | Pagination. |
| `###PRODUCTPAGERLAYOUT, n###` | C | N/N | nombre de produits par page | À placer au-dessus de PRODUCTPAGER. |
| `###PRODUCTPAGER###` DEPR | C | N/N | | |
| `###PRODUCTSORT_JSON, {…}###` | C | N/N | label_text, show_label, select_class, prefix, suffix | Liste de tri. |
| `###PRODUCTSORT, prefix, suffix, labelText###` DEPR | C | N/N | | |
| `###PRODUCTFILTER_JSON, {…}###` | C | O/O | container_class, container_id, prefix, suffix | Filtre de produits (voir §5). |
| `###FEATUREDPRODUCT_JSON, {…}###` | C | O/O | heading, heading_text, count, layout* (`@@@NAME@@@ @@@IMAGEURL:taille@@@ @@@URL@@@ @@@TEXT@@@`), prefix, suffix | Produits mis en avant. |
| `###FEATUREDPRODUCT, layout###` DEPR | L | O/N | `@@@IMAGE:taille:rel@@@`, `@@@NAME@@@` | |
| `###BREADCRUMBS_JSON, {…}###` | C, PD | N/N | active_class, list_class, prefix, suffix | Fil d'Ariane. |
| `###BREADCRUMBS###` DEPR | C, PD | N/N | | |

### 6.5 Fiche produit et aperçu rapide (productdetail.txt, productquickviewlayout.txt)

| Tag | Où | M/Inc | Paramètres clés | Rôle |
|---|---|---|---|---|
| `###PRICING###` REQ | PD, QV | N/N | aucun | Moteur de prix (calculateur/grille + totaux). |
| `###ADDTOCARTBUTTON, add text, customize text###` REQ | PD, QV | N/N | texte produit normal, texte produit eDoc | Bouton Ajouter au panier / Personnaliser. |
| `###CUSTOMFIELDS, heading###` REQ | PD | N/N | heading (vide = localisé, `none` = sans titre) | Formulaires personnalisés du produit. |
| `###FULLPRODUCTDESCRIPTION###` REQ | PD | N/N | prefix, suffix | Description complète (HTML). |
| `###SHORTPRODUCTDESCRIPTION###` REQ | PD, QV | N/N | prefix, suffix | Description courte. |
| `###ORDERNOTESBOX, heading###` REQ | PD, QV | N/N | heading | Zone de notes de commande. |
| `###RENAMEITEM, heading###` REQ | PD | N/N | heading | Champ pour nommer l'article. |
| `###DOWNLOADASSET, prefix, suffix, showheading, headingtext, showdescription, showthumbnail###` REQ | PD | O/N | | Liens de téléchargement des ressources. |
| `###PRODUCTNAME###` | PD, QV | N/N | | Nom du produit. |
| `###FILEUPLOAD_JSON, {…}###` | PD, QV | N/N | requredClass (sic), inputClass, inputLayout (`@@@FILEINPUT@@@ @@@FILEINPUTLABEL@@@ @@@FILEINPUTCOUNT@@@`), prefix, suffix | Champs d'envoi de fichiers. |
| `###FILEUPLOAD###` DEPR (marqué REQ) | PD, QV | N/N | | Ancienne version : garder l'un des deux. |
| `###PARTNUMBER_JSON, {…}###` | PD, QV | N/N | partNumberLayout (`@@@PARTNUMBER@@@`, `@@@TEXT:partnumber@@@`), prefix, suffix | Référence produit. |
| `###PARTNUMBER, prefix, suffix###` DEPR | PD, QV | N/N | | |
| `###PRODIMAGENEW, imagesize, relimagesize, prefix, suffix, cssclass, alt, title, showanchor, anchorclass, anchorimagesize###` | PD, QV | O/N | tailles : small, smallsquare, medium, mediumsquare, large, xlarge | Image produit avec options. |
| `###PRODUCTIMAGE, size, pathonly, relsize###` DEPR | PD, QV | N/N | | |
| `###PRODUCTMULTIPLEIMAGES_JSON, {…}###` | PD, QV | O/N | layout (`@@@PRIMARYIMAGELAYOUT@@@`, `@@@ITEMLAYOUT@@@`), primaryImageLayout, itemLayout (`@@@IMAGEURL:taille@@@`, `@@@IMAGESIZE:taille:width\|height@@@`, `@@@TEXT@@@`, `@@@SKINPATH@@@` ; tailles + `original`) | Galerie (si plusieurs images uniquement). |
| `###PRODUCTSINGLEIMAGE_JSON, {layout}###` | PD, QV | O/N | layout avec `@@@IMAGEURL:taille@@@` | Image unique (si une seule image). Prévoir les deux tags. |
| `###INSTRUCTIONS###` | PD, E, QV | N/N | | Instructions système. |
| `###ACCEPTANCE###` | PD, QV | N/N | | Case/champ « J'accepte » si configuré. |
| `###INVENTORY, prefix, suffix###` | PD, QV | N/N | | Stock (B2B uniquement). |
| `###SHIPTOADDRESS, heading###` | PD, QV | N/N | heading (`none` possible) | Choix de l'adresse de livraison. |
| `###SHIPCALC, heading###` | PD | N/N | | Estimateur de frais de port. |
| `###CATALOGBUTTON###` | PD, QV | O/N | | Bouton retour au catalogue. |
| `###SHOPCARTBUTTON###` | PD, QV | N/N | | Bouton vers le panier. |
| `###SUGGESTEDPRODUCTS_JSON, {…}###` | PD | N/N | listPrefix, listSuffix, maxItems, showHeading, itemLayout (`@@@TEXT@@@ @@@IMAGEURL@@@ @@@NAME@@@ @@@URL@@@ @@@TEASER@@@ @@@SHORT@@@`), headingLayout (`@@@HEADING@@@`), prefix, suffix | Produits suggérés. |
| `###SUGGESTIVESELLING, prefix, suffix, maxItems, heading###` DEPR | PD | N/N | | |
| `###NEWKITSET, HTML layout###` | PD | N/N | `@@@KITSETNUMBER@@@ @@@KITSETNAME@@@ @@@INVENTORYAMOUNT@@@ @@@DESCRIPTION@@@ @@@INSTRUCTIONS@@@ @@@ITEMS@@@ @@@IMAGE@@@` | Gabarit d'un kit. |
| `###KITSET, layout###` DEPR | PD | N/N | `@@@DESCRIPTION@@@ @@@INSTRUCTIONS@@@ @@@ITEMS@@@` | |
| `###KITSETITEM, layout###` DEPR | PD | N/N | `@@@DESCRIPTION@@@ @@@NAME@@@ @@@IMAGE:t:rel@@@ @@@INSTRUCTIONS@@@ @@@PRICECALC@@@ @@@UPLOAD@@@` | Article de kit (contient le moteur de prix `@@@PRICECALC@@@`). |
| `###KITITEMS, heading###` DEPR | PD | N/N | | |

### 6.6 Page de contenu (contentpagelayout.txt)

| Tag | Où | M/Inc | Paramètres | Rôle |
|---|---|---|---|---|
| `###CONTENT###` REQ | CP | N/N | | Contenu de la page. |
| `###PAGENAME###` | CP | O/N | | Nom de la page. |
| `###FORM###` REQ | CP | N/N | | Formulaire de la page (avec CAPTCHA et SUBMIT). |
| `###CAPTCHA, prefix, suffix###` REQ | CP | N/N | | Captcha (sites I et B2C), à placer après FORM. |
| `###SUBMIT###` | CP | N/N | | Bouton d'envoi du formulaire. |

### 6.7 eDocBuilder (edoclayout.txt)

| Tag | Rôle |
|---|---|
| `###APPROVEBUTTON###` REQ | Valide le modèle et ajoute au panier. |
| `###APPROVECHECKBOX###` REQ | Case « J'approuve ce document ». |
| `###CANCELBUTTON###` REQ | Annule la personnalisation. |
| `###SAVEFORLATERBUTTON###` REQ | Enregistre pour plus tard. |
| `###UPDATEBUTTON###` REQ (multiple autorisé) | Met à jour l'aperçu. |
| `###UPDATEREQUIRED###` REQ | Message « mise à jour nécessaire ». |
| `###PAGESELECTOR###` REQ | Sélecteur de pages du modèle. |
| `###PREVIEWIMAGES###` REQ | Zone d'aperçu. |
| `###CHOICES###` | Tous les champs de saisie. |
| `###SIZESELECTOR###` | Taille d'aperçu. |
| `###DATAMAP###` | Correspondance des champs (données variables). |
| `###RESPONSESET###` | Jeux de réponses. |
| `###INSTRUCTIONS###` | Instructions. |
| `###COPYRIGHT###` DEPR | Ne fait rien : à retirer. |

### 6.8 Récapitulatif de commande (ordersummarylayout.txt)

| Tag | Paramètres | Rôle |
|---|---|---|
| `###ITEMS, html layout###` REQ | sous-tags : `@@@PRODUCTNAME:p:s@@@`, `@@@QUANTITY:p:s@@@`, `@@@PRICE@@@`, `@@@APPROVALINFO:p:s@@@`, `@@@IMAGE:taille:rel@@@`, `@@@PARTNUMBER@@@`, `@@@ITEMNAME:p:s@@@`, `@@@ITEMNUMBER:p:s@@@`, `@@@ITEMDESCRIPTION@@@`, `@@@ITEMDETAILS@@@` (choix du moteur de prix), `@@@BARCODE@@@`, `@@@REQUESTEDDELIVERY:p:s@@@`, `@@@STATUS@@@`, `@@@STATUSDATE@@@`, `@@@STATUSHISTORY@@@`, `@@@ACCEPTANCE:p:s@@@`, `@@@FORMINFO:p:s@@@`, `@@@FILES:p:s@@@`, `@@@EDOCPROOF:p:s@@@`, `@@@SHIPMENTS:p:s@@@`, `@@@SHIPTO:p:s@@@`, `@@@ADDITIONALINSTRUCTIONS@@@` | Lignes de la commande. |
| `###NOTES, prefix, suffix###` REQ | | Notes de commande. |
| `###ORDERDATE, prefix, suffix###` REQ | | Date. |
| `###ORDERFORM###` REQ | | Formulaire de checkout éventuel. |
| `###PROMODISCOUNT###` REQ | | Remise promo. |
| `###ORDERNUMBER, prefix, suffix###` | | Numéro de commande. |
| `###ORDEREDBY, prefix, suffix###` | | Commanditaire. |
| `###BILLTO, prefix, suffix###` | | Adresse de facturation. |
| `###PONUMBER, prefix, suffix###` | | N° de bon de commande. |
| `###PAYMENTS, prefix, suffix###` | | Paiements (2023). |
| `###PAGETITLE###` | | Nom de la commande. |
| `###SHIPPING, prefix, suffix###` | | Frais de port. |
| `###SUBTOTAL###`, `###TAX1###`, `###TAX2###`, `###TAX3###`, `###VAT###`, `###TOTAL###` | | Montants. |
| `###REORDERLINK, prefix, suffix, displayText###` | | Lien Recommander. |
| `###PRINTLINK###` | | Lien d'impression (nécessite le JS par défaut). |
| `###EXPANDLINK###` DEPR | | À ne plus utiliser. |

## 7. Règles et pièges pour modifier un skin sans le casser

1. **Syntaxe des tags** : `###…###` avec virgules ; sous-tags `@@@…@@@` avec deux-points. Ne jamais casser un délimiteur, ni mélanger virgule/deux-points. Attention : une virgule dans un paramètre positionnel (prefix/suffix) est interprétée comme séparateur ; préférer les versions `_JSON` où le HTML est entre quotes.
2. **Quotes dans les _JSON** : la valeur est entre `'…'` ou `"…"` ; utiliser l'autre type de guillemet pour les attributs HTML internes (ex. `prefix: '<div class="x">'`).
3. **Tags obligatoires** (REQ) : ne jamais les supprimer de leur fichier (CONTENTAREA dans layout.txt ; PRICING, ADDTOCARTBUTTON, CUSTOMFIELDS… dans productdetail ; CATEGORYITEMLAYOUT, PRODUCTITEMLAYOUT, PRODUCTS, SUBCATEGORIES dans categorylayout ; etc.).
4. **Bon fichier** : un tag ne fonctionne que dans les fichiers listés (colonne « Où ») ; la plupart des tags ne marchent pas dans les .inc ; INCLUDE/HEADINCLUDE uniquement dans layout.txt.
5. **Unicité** : la plupart des tags sont « une seule fois » par fichier (M = N).
6. **Noms de .txt imposés** : ne pas inventer de nouveaux .txt ; utiliser des .inc pour factoriser.
7. **requirements.xml** : UTF-8 sans UTF-16, XML valide, namespace conservé. Ne pas réordonner les `<paletteEntry>` (décale tous les `@ShadeN@`) ni les `<imageEntry>` (décale les `image_number`). Après envoi, vérifier qu'il s'ouvre dans le navigateur.
8. **CSS** : pas d'id `ctl00…` ; préférer `@ShadeN@` aux couleurs codées en dur ; styler toutes les pages (iframes devis et aperçu rapide inclus) ; utiliser les classes body (`pageType_…`, `pageName_…`, `xxxPage`) pour cibler une page.
9. **Checkout** : si `useCheckoutCSS=false`, styler cart, checkout, payment, access, shipping, pending orders ; sinon, simplement vérifier le rendu, masquer la barre latérale, Font Awesome 4.7.
10. **Filtre produits** : PRODUCTFILTER_JSON n'affiche rien sans le plugin JS `productFilter`.
11. **JS/CSS par défaut** : `useDefaultJS=false` supprime le JS Aleyant (PRINTLINK, EXPANDLINK… en dépendent) : il faut alors fournir les bibliothèques via `<jsLibraryURLs>`.
12. **Tags obsolètes** : en conserver le fonctionnement ; s'il faut en modifier un, le remplacer par l'équivalent `_JSON`.
13. **[hors doc] Variantes** : si le skin contient `v6/productdetail.txt` (ou `v6/` pour l'aperçu rapide), c'est cette version qui sert à la fiche produit V6 : la modifier aussi. Si le skin contient des sources CSS (`layout.uncompressed.css`, `src/…`), seul `layout.css` est lu par Pressero : toute modification doit finir dans `layout.css`.
14. **Méthode** : travailler sur une copie locale, sauvegarder chaque fichier avant modification, téléverser par FTP sur un site de test, vérifier dans le navigateur (plusieurs navigateurs, mobile si isResponsive).
