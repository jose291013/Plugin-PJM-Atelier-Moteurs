# Pressero – Assistant Admin (v0.2.0)

Plugin Cowork qui pilote l'admin **Pressero** (Aleyant) via Claude in Chrome. Répond en français, espagnol ou anglais.

## Compétences
| Compétence | Rôle |
|---|---|
| `pressero-expert` | Connaissance de l'admin et de la vitrine, règles de sécurité, techniques (widgets Kendo, fenêtres, organiseur Vue), lien PJM. Chargée par toutes les autres. |
| `scripts-head-pressero` | Lister / ajouter / remplacer / corriger un bloc `<!-- START … -->…<!-- END … -->` du head bas, avec sauvegarde dans le navigateur et vérification vitrine. |
| `configurateur-produit-pjm` | Script « boutons segmentés + quantités côte à côte + barre de prix » pour un produit tarifé par un moteur PJM (APJM), adapté au produit, testé puis installé comme bloc. |
| `creer-produit-pressero` | Dupliquer un produit modèle, le renommer, rattacher APJM + Id d'intégration PJM, modifier les onglets, tester le prix. |
| `importer-produits-excel-pressero` | Préparer un fichier d'import produits (mise à jour / création en masse) depuis un export récent ; l'utilisateur l'importe ; Claude vérifie. Script `prepare_import.py`. |
| `recap-attributs-pjm` | Affiche dans le récapitulatif de la page produit les résultats renvoyés par le moteur PJM (attributs : quantité totale, dimensions calculées, alertes, poids, date estimée) et aligne la date d'expédition Pressero (`SHIP_DAYS`) avec une heure limite. |
| `ranger-catalogue-pressero` | Créer / modifier des catégories et y ranger les produits (organisation du catalogue). |

## Prérequis
- Claude in Chrome connecté ; l'utilisateur se connecte lui-même à l'admin Pressero (et à PJM si besoin) dans l'onglet de Claude.
- Un dossier de travail connecté (ex. `Documentos\Pressero Claude`) pour les fichiers d'import et de scripts.
- Plugin complémentaire : `pjm-atelier-moteurs` (moteurs et formules PJM).

## Limites connues (V1)
- Claude ne peut pas déposer de fichier dans le navigateur : images de la galerie produit, image de catégorie, fichier d'import Excel et fichiers de skin (FTP) sont déposés par l'utilisateur.
- Non couverts en V1 : préférences du compte (tarifs de livraison, paiements, taxes, workflows ; seuls les calendriers d'entreprise sont documentés), apparence/skin (hors référence), création de site complet, API.

## Versions
- 0.2.0 – 19/10/2026 : skill `recap-attributs-pjm` (attributs PJM dans le récapitulatif via `intCalcFinish` chaîné, date estimée, heure limite par quantité technique S1 et `SHIP_DAYS`), référence calendriers d'entreprise (jours fériés répétés / datés, piège de l'année).
- 0.1.0 – 18/10/2026.

## Sécurité
Jamais de saisie de mot de passe, jamais d'affichage de secrets, sauvegarde avant écriture, validation de l'utilisateur avant d'enregistrer sur un site client, une modification à la fois, aucune suppression sans demande explicite.
