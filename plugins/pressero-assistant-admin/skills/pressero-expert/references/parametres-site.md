# Pressero – Page « Paramètres » du site (référence)

- URL : https://admin.ams.v6.pressero.com/site/equipe3.ams.v6.pressero.com/Settings
- Site : Equipe 3 (equipe3.ams.v6.pressero.com) – relevé en lecture seule le 18/10/2026
- **Un seul bouton « Sauvegarder » pour toute la page** (barre du haut, hors onglets), à côté de « Créez un Site », « Dupliquer un site », « Supprimer le Site » (danger).
- Onglets (`.nav-tabs a`, href = id du panneau) : `general`, `domains`, `shipping`, `payment`, `instructions`, `content`, `notifications`, `seo`, `awe`.
- Les grilles Livraison et Paiement ne sont PAS enregistrées par « Sauvegarder » : chaque ligne s'édite dans une modale (`editShipping(...)` / `editPayment(...)`) qui a sa propre sauvegarde.
- Légende : ☑/☐ = case cochée/non cochée ; `Nc` = longueur de la valeur (contenu non recopié).

---

## 1. Général (`#general`)

Sections (h3) : L'image de marque · Site standard · Impôt · Consentement explicite · reCAPTCHA · Panier d'achat · Paiement · Formulaire pour la page de vérification · Approbation · Rapports de commande.
Aucun widget Kendo dans cet onglet : selects HTML natifs, cases natives.

| id | libellé | type | valeur actuelle |
|---|---|---|---|
| SiteName | Nom du site | text | « Equipe 3 » |
| StartUrl | URL de la page d'accueil | select (34) | Par défaut (options = pages produits `/product/...`) |
| Tagline | Slogan | text | vide |
| SiteStore_ContinueShoppingUrl | Continuez vos achats | select (34) | Par défaut |
| SiteStore_BackToCatalogUrl | Retour au catalogue | select (34) | Par défaut |
| logo | Logo (png, jpg, gif, bmp) | file | – |
| favicon | Logo favicon 16x16 | file | – |
| (Type de site) | Type de site | text (info, 39c) | renseigné |
| ImpersonateUserPassword | Mot de passe maître de site | text | **SENSIBLE** – vide ; ne jamais saisir |
| SiteStore_MisId | Intégration ID | text | renseigné (36c, GUID) – ne pas diffuser |
| SiteStore_LogoutUrl | Sortir/Fermer la session | text | vide |
| SiteStore_CXMLUrl | CXML auditeur Url | text | vide |
| SiteStore_ProductQuickViewText | Texte vue rapide du produit | text | vide |
| IsCartSavedForLaterEnabled | Sauvegardé pour plus tard | checkbox | ☑ |
| CartSavedForLaterDuration | Enregistrer des éléments pendant (jours) | number | 60 |
| OverrideCulture | Utiliser toujours la langue du site | checkbox | ☐ |
| Culture | Culture (langue) | select (73) | Français |
| UseUniversalLogin | Page de connexion universelle | checkbox | ☐ |
| UseiFrameFullScreen | eDocBuilder plein écran | checkbox | ☐ |
| siteStoreCustBrokerId | Intermédiaire | select (2) | vide |
| siteStoreCustSalesUserId | Responsable de ce site | select (22) | vide |
| AllowSelfSignup | Permettre l'auto-inscription | checkbox | ☑ |
| IsReqUserNameforSelfSignup | Exiger un nom d'utilisateur (auto-inscription) | checkbox | ☐ |
| SiteStore_SiteStoreCust_SelfSignup… | Groupe d'approbation pour l'auto-inscription | select (7) | vide |
| siteStoreCustBossGroupId | Responsable pour les utilisateurs | select (7) | vide |
| daysOption | Le mot de passe expire dans (jours) | select : Jamais/60/90/180 | Jamais |
| SiteStore_SiteStoreCust_DisableUse… | Mettre automatiquement les utilisateurs… (désactivation) | checkbox | ☐ |
| SiteStore_CaptureTaxId | Activer l'identification fiscale | checkbox | ☐ |
| SiteStore_TaxId / _TaxIdMask / _TaxIDName | Id taxe / masque / libellé demande | text ×3 | vides |
| SiteStore_SubscriberTaxProfileID | Profil fiscal | select (8 : Belgique 21 %, Europa, IVA 21 %, IVA Mexico, Tax Profile 20 %…) | Tax Profile 20 % |
| ExplicitConsentForPrivacy | Consentement explicite | checkbox | ☐ |
| PrivacyPolicyPageURL | URL politique de confidentialité | text | vide |
| PrivacyPolicySummaryStatement / PrivacyPolicyCustomPrompt / ConsentToContactCustomPrompt | Résumé / acceptation / consentement contact | textarea ×3 | vides |
| clearPrivacyPolicy | bouton « Nettoyer Acceptation… » | button | **action immédiate** (`ClearPrivacyPolicyAcceptance()`) – ne pas cliquer |
| ReCaptcha | Activer reCAPTCHA | checkbox | ☐ |
| ReCaptchaTermsOfUseUrl / ReCaptchaCookiePolicyUrl / ReCaptchaPrivacyPolicyUrl | URL CGU / cookies / confidentialité | text ×3 | vides |
| addressBookMode | Mode carnet d'adresses | select : Carnet d'adresses/Siège/succursale/Les deux | Les deux |
| SiteStore_SiteStoreCust_CaptureShi… | Afficher liste des adresses… | checkbox | ☑ |
| SiteStore_SelectShipAddress | L'utilisateur doit sélectionner une adresse | checkbox | ☐ |
| SiteStore_ShipToMultipleAddress | Envoi à plusieurs adresses | checkbox | ☐ |
| SiteStore_CaptureAttentionTo | « À l'attention de » | checkbox | ☑ |
| siteStoreCustPrimaryLocationId | Emplacement principal | select (17) | vide |
| siteStoreLocationId | Livraison depuis l'emplacement | select (3) | vide |
| SiteStore_ShoppingCartRedirectOption | Après ajout au panier, rediriger vers | select : Panier/Détails produit/Catégorie/Accueil/Catégorie racine | Panier d'achat |
| SiteStore_CaptureRequestedShipDate | Date de livraison souhaitée | select : Défaut/Obligatoire/Facultatif/Ne pas demander | Utilisation par défaut |
| SiteStore_CaptureBillingAddress | Saisir l'adresse de facturation | checkbox | ☑ |
| siteStoreCustBillToLocationId | Facturer à l'adresse | select (17) | vide |
| SiteStore_BudgetPrompt / SiteStore_IsEnableBudget | Étiquette budget / Activer budgets | text / checkbox | vide / ☐ |
| SiteStore_ProofType | Type de fichier eDocBuilder épreuve | select : PDF/PNG/JPG | PDF |
| SiteStore_PayBeforeApproval | Paiement avant approbation | checkbox | ☑ |
| SiteStore_AllowToUseGiftCertificat… / _GiftCertificateSectionPr… | Chèques cadeaux / texte section | checkbox / text | ☐ / vide |
| UseCartLevelDiscount | Remise au niveau du panier | checkbox | ☐ |
| SiteStore_CapturePurchaseOrder | Bon de commande | select : Obligatoire/Facultatif/Ne pas demander | Ne pas demander |
| SiteStore_ValidatePONumber / _ListPOCodeBasedOnBilling / _AllowCustomPONumber | Valider BC / BC selon facturation / BC personnalisé | checkbox ×3 | ☐ ☐ ☐ |
| SiteStore_PurchaseOrderPrompt / _TaxPrompt / _GiftCertificatePrompt | Libellés BC / TVA / chèque cadeau | text ×3 | vides |
| SiteStore_FinishPendingOnApprove | Finaliser commande en attente à l'approbation | checkbox | ☐ |
| SiteStore_AllowToUseGCWithNonInteg… | Chèques cadeaux avec paiements non intégrés | checkbox | ☐ |
| SiteStore_UseInventoryOnCheckout | Déduire le stock au checkout | checkbox | ☐ |
| CheckoutForms (+ listes bootstrap-duallistbox) | Formulaires page de vérification | dual listbox : 34 dispo / 0 sélectionné | aucun |
| SiteStore_SiteStoreCust_IsReturnFi… | Fichiers dans l'historique | checkbox | ☑ |
| SiteStore_SiteStoreCust_AllowOneCl… | Approbation en un clic | checkbox | ☑ |
| SiteStore_SiteStoreCust_AllowAppro… | Approbateur peut modifier | checkbox | ☑ |
| SiteStore_SiteStoreCust_ApproveIte… | Approuver l'élément à la personnalisation | checkbox | ☑ |
| siteStoreCustApprovalPlanId | Plan d'approbation par défaut | select (1) | Basic plan |
| SiteStore_SiteStoreCust_NeedConfir… | Confirmation à 2 niveaux | checkbox | ☐ |
| SiteStore_SiteStoreCust_AllowAppro… (2) | Commentaire de l'approbateur | checkbox | ☐ |
| HidePriceOnPickList | Masquer le prix sur le rapport de liste | checkbox | ☐ |

Remarques :
- Plusieurs id sont tronqués ici (…) : deux champs commencent par `SiteStore_SiteStoreCust_AllowAppro` → cibler par libellé ou id complet.
- CheckoutForms : dual listbox (boutons Move all / Move selected / Remove…) ; la valeur réelle est le `<select multiple id=CheckoutForms>`.

---

## 2. Domaines (`#domains`)

| id | libellé | type | valeur |
|---|---|---|---|
| NewDomain | Nouveau nom de domaine | text | vide |
| (sans id) | domaine listé | text readonly | equipe3.ams.v6.pressero.com |
| RedirectToPrimaryDomain | Redirection vers le domaine principal | checkbox | ☐ |

Liste : un seul domaine, **equipe3.ams.v6.pressero.com**, principal (étoile grisée = déjà principal), en HTTPS (cadenas vert).
Boutons : « Ajoutez un nouveau domaine » ; par domaine : étoile (définir principal), cadenas `.btnToggleSSLForDomain` (« Définir comme http ») → **action immédiate, ne pas cliquer** (repasserait le site en http).
Aide : KB a244 « domains tab in settings ».

---

## 3. Livraison (`#shipping`)

Intro : les options de livraison sont listées ; cliquer sur le nom (crayon) pour l'activer pour ce magasin, définir les groupes autorisés et l'ordre de tri.

Grille Kendo « Méthodes de livraison » (colonnes : Nom / Transporteur / Activé) – **56 méthodes**, pagination serveur 25 par page (select de page = DropDownList Kendo). Champs dataSource : SubscriberShippingMethodId, MethodName, Carrier, IsActive, MethodNameEncoded. Édition par modale `editShipping(nom, '/site/<site>/Settings/EditSiteShippingMethod/<id>…')`.

**Activées (3)** : Livraison SD (SendCloud) · Livraison2448HFrance (External) · UPS STANDARD (SendCloud).

Inactives (53) :
- NonIntZone (40) : Livraison standard par tranches de poids (0-5 … 400-500 kg), Livraison standard 48/72 H par tranches, Livraison express 24/48 H 35-50 et 400-500 kg, France Express 401-500 kg Zone 05 LM.
- SendCloud : +70 KG sencloud, Livraison grand format, Point se service, Test AMS Sendcloud.
- External : Livraison test external, SCHENKER, SOREP.
- None/none : Envío estandar 48/72 H, Livraison standard 48/72 Heures >, Retrait à l'imprimerie, Retrait en boutique 2, Seur 72 Horas, Test livraison gratuite sup à 100 €.

Section « Comptes de transporteurs » : identifiants par transporteur (`ShippingProvidersCredentials_<Transporteur>__<Champ>_`) pour : Australia Post (Domestic, International, V2/StarTrack), Canada Post, ChronoPost, Correios, Correios V2, Couriers Please, DHL, Direct Freight Express, Enviaya, External Shipping Service, Fastway, FedEx, FedEx V2, IFS SmartFreight, JNE Express, NZ Post (Domestic/International), OCA, Overseas, Purolator, Redyser, SendCloud, SpeeDee, StarTrack, UPS, UPS Freight (V1/V2), UPS V2, USPS V2/V3, ViettelPost.
- **SENSIBLE** : champs User Id / Username / Password / API Key / Access Key / Account Number. Seuls **SendCloud UserID et Password sont renseignés** (valeurs non lues). Ne jamais les afficher ni les modifier.

Testeur de livraison (ne modifie rien, mais ne sert qu'au test) : TestShippingWeight (Poids), TestShippingCountry (select 247, France), TestShippingStateProvince (DropDownList Kendo), TestShippingCity, TestShippingPostalCode, TestShippingDistrict + bouton « Tester maintenant ».
Aide : KB a246 « shipping setup for sites v6 ».

---

## 4. Paiements (`#payment`)

Intro : cocher pour rendre un mode disponible, possibilité de renommer. Avertissement : activer carte de crédit sans configurer PayPal dans Préférences > Paramètres > Paiement casse le checkout.

Grille Kendo (Nom / Type / Activé), 4 modes, édition par modale `editPayment(...)`. Champs dataSource : SubscriberPaymentMethodId, MethodName, ServiceName, ProviderCode, PaymentProcessingMethod, IsActive.

| Mode | Type | Activé |
|---|---|---|
| Ingenico test | Paypage | ☐ |
| Pago a 30 días | Misc | ☑ |
| pago al contado | Misc | ☑ |
| Patpal | PayPal | ☐ |

Aucun champ de saisie direct dans l'onglet (seulement le select de pagination). Les clés de passerelle (Ingenico, PayPal) sont au niveau Préférences/modale, pas ici – ne jamais les afficher.
Aide : KB a248 « setting the payment methods for sites ».

---

## 5. Instructions (`#instructions`)

Intro : personnalisation des textes d'aide affichés dans la boutique. 13 éditeurs **Kendo Editor** (textarea `SiteInstructions_<Nom>`), tous **vides** actuellement :

| id | libellé |
|---|---|
| SiteInstructions_AccessInstructions | Instructions pour la page d'accès |
| SiteInstructions_LoginInstructions | Aide page de connexion/création de compte |
| SiteInstructions_FTPInstructions | Aide comptes FTP |
| SiteInstructions_ProofInstructions | Prévisualisation d'un fichier téléchargé |
| SiteInstructions_CartPageInstructions | Panier d'achat |
| SiteInstructions_ShippingPageInstructions | Page frais d'expédition |
| SiteInstructions_CheckoutPageInstructions | Page de paiement (checkout) |
| SiteInstructions_CheckoutSuccessfulMessage | Après paiement effectué |
| SiteInstructions_PaymentPageInstructions | Page de paiement |
| SiteInstructions_eDocBuilderInstructions | Personnalisation eDocBuilder |
| SiteInstructions_CreateAccountInstructions | Création de compte |
| SiteInstructions_SaveforLaterCartInstructions | Sauvegardé pour plus tard |
| SiteInstructions_ReportPageInstructions | Rapport de site |

Piège : chaque éditeur a une barre d'outils avec des inputs sans id (SelectBox « format », 2 text 16c, ComboBox police/taille « inherit ») – ce ne sont pas des champs de données. Piloter via `kendo.jQuery('#SiteInstructions_X').data('kendoEditor').value(html)` (pas `textarea.value`).

---

## 6. Contenu (`#content`)

| id | libellé | widget | valeur |
|---|---|---|---|
| ContactBlock | Bloc de contact (adresse, téléphone…) | Kendo Editor | vide |
| FooterHtml | Contenu du pied de page | Kendo Editor | vide |

Même remarque Kendo Editor que ci-dessus.

---

## 7. Notifications (`#notifications`)

Intro : nom et e-mail d'expéditeur des notifications du site ; vides = repris des paramètres SMTP du souscripteur.

| id | libellé | type | valeur |
|---|---|---|---|
| SmptSenderName | Nom de l'expéditeur | text | vide |
| SmptSenderEmail | E-mail de l'expéditeur | text | vide |
| ReminderInfo_0__Enabled | Rappel commandes en attente d'approbation | checkbox | ☐ |
| ReminderInfo_1__Enabled | Rappel articles sauvegardés pour plus tard | checkbox | ☐ |
| ReminderInfo_2__Enabled | Rappel panier ouvert | checkbox | ☐ |
| ReminderInfo_3__Enabled | Rappel commandes en attente de paiement | checkbox | ☐ |

Attention à l'orthographe des id : `Smpt` (et non Smtp). Aide : KB a251.

---

## 8. SEO / HTML (`#seo`) – connu, non détaillé

ContentTopOfHeadSection (vide), AnalyticsHead (head bas, ~69 ko – **contenu non lu, ne jamais le lire ni l'afficher**), ContentTopOfBodySection (vide), ContentShareScript (vide). Textareas simples.

---

## 9. PDF2Press (`#awe`)

| id | libellé | type | valeur |
|---|---|---|---|
| ProofingStep | Autoriser l'épreuvage pendant le paiement | checkbox | ☑ |
| Pdf2PressRequireCheckoutApprove | Exiger l'approbation de l'épreuve au paiement | checkbox | ☑ |
| Pdf2PressAllowAproveAllProofListPa… | Autoriser « tout approuver » sur la liste des BAT | checkbox | ☑ |

Note : si Pressero perd la connexion avec PDF2Press, il bascule par défaut sur la vérification par e-mail.

---

## Points d'attention généraux

- Lecture JS : `.tab-pane` masqués restent lisibles ; cliquer l'onglet seulement pour l'affichage.
- Widgets Kendo : uniquement dans Instructions/Contenu (Editor), grilles Livraison/Paiement (Grid, pagination serveur : `grid.dataSource.query({page:1,pageSize:100})` pour tout lire, puis remettre 25) et testeur de livraison (DropDownList). Onglet Général = HTML natif (dispatcher `change` après modification).
- Boutons à action immédiate (hors Sauvegarder) : Nettoyer l'acceptation de la politique, cadenas SSL / étoile des domaines, Ajouter un domaine, modales des grilles, « Supprimer le Site ».
- Secrets : ImpersonateUserPassword, identifiants transporteurs (SendCloud renseigné), Intégration ID (GUID), AnalyticsHead → ne jamais afficher.

## Essais d'écriture et compléments (18/10/2026)
- **Bloc contact** (onglet Contenu, `ContactBlock`, kendoEditor) : HTML de test écrit via `kendo.jQuery('#ContactBlock').data('kendoEditor').value(html)` + `update()` + `trigger('change')`, puis **Sauvegarder** (unique `input[type=submit]` visible, valeur « Sauvegarder ») → message « Renseignements enregistrés avec succès. ». `AnalyticsHead` vérifié intact avant/après (69 563 caractères).
  Affichage vitrine : colonne du **pied de page** sur toutes les pages (`.row.footer-columns > .col-md-3 > .contactblcok.custom-html`, skin Responsive 6).
- **Méthode de livraison d'un site** : dans la grille `#shippingMethodGrid` (colonnes MethodName, Carrier, IsActive ; lecture seule `_SiteShippingMethods/{SiteId}`), l'icône de ligne appelle `editShipping('{nom}', '/site/{domaine}/Settings/EditSiteShippingMethod/{SubscriberShippingMethodId}')` (fenêtre). Cette page, ouvrable directement, ne contient que :
  `Order` (ordre de tri), `Enabled` (activer pour ce site), `AvailableToAllGroups`, boutons Sélectionner tout / aucun / Inverser, cases `AllowedGroups_{groupId}` (groupes autorisés), et son propre **Sauvegarder**.
  → Activer / désactiver une méthode, changer son ordre ou ses groupes = cette page. Les **tarifs et règles** d'une méthode se définissent au niveau du compte : Préférences → Livraison → Méthodes (`/shippingMethods`), à explorer.
  Exemple : « Livraison SD » (SendCloud) = `a80e0000-568f-0050-c5d0-08db56dd19c8`, activée, ordre 1, tous les groupes.
