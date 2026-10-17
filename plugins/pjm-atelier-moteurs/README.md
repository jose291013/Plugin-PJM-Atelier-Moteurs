# PJM – Atelier Moteurs (Aleyant)

**FR** – Décrivez vos moteurs de prix PrintJobManager dans une application simple (l'« Atelier »), puis laissez Claude les construire, les mettre à jour ou les importer dans votre PJM via Claude in Chrome.
**ES** – Describa sus motores de precios PrintJobManager en una aplicación sencilla (el «Taller») y deje que Claude los construya, actualice o importe en su PJM con Claude in Chrome.
**EN** – Describe your PrintJobManager pricing engines in a simple app (the "Atelier"), then let Claude build, update or import them in your PJM through Claude in Chrome.

## Prerequisites / Requisitos / Prerequisites
- Claude Cowork (desktop app) with this plugin installed.
- Claude in Chrome extension, connected; a PJM administrator account, signed in by the user in Chrome (Claude never types passwords).
- The address of the PJM instance (e.g. `https://xxx.printjobmanager.com`).

## Skills
| Skill | What it does | Say for example |
|---|---|---|
| creer-atelier-pjm | Creates the customer's Atelier (app + guided questions + settings) | « Crée l'Atelier pour l'imprimerie Dupont » |
| lire-catalogue-pjm | Loads machines, processes and materials from PJM into the Atelier | « Relis le catalogue PJM » |
| construire-moteur-pjm | Builds a new engine from a sheet « Prête à construire », runs tests | « Construis le moteur de la fiche Brochure A4 » |
| mettre-a-jour-moteur-pjm | Applies the changes of a sheet to its existing engine | « Mets à jour le moteur Bâche » |
| importer-moteur-pjm | Turns an existing PJM engine into an Atelier sheet | « Importe le moteur …/ProductEngines/Edit/… » |
| reprendre-excel-pjm | Rebuilds an Excel / Pressero price calculator in PJM (creates missing machines and papers), tests against the Excel | « Reproduis ce moteur Excel dans PJM » |
| moteurs-pjm-expert | NCalc / PJM formula expertise, used by all the others | « Corrige cette formule PJM » |

## Getting started
1. « Crée l'Atelier Moteurs PJM pour {client} » → answer name, PJM address, language.
2. « Relis le catalogue PJM » (sign in to PJM in Chrome first).
3. Share the Atelier with the people who fill in sheets **as Editors** (outside your organization: invite by email as Editor, no public link).
4. Fill in a sheet, set it to « Prête à construire », then ask Claude to build it.

## Consommation / Consumo / Usage
- Conseillé : un projet Cowork « PJM – {imprimerie} » sans documents, avec dans ses instructions l'adresse de l'Atelier, l'adresse PJM et la langue (Claude donne le texte à coller).
- Repère mesuré : création de l'Atelier + lecture du catalogue ≈ 5 % d'un forfait (17/10/2026).
- Une tâche par conversation : la consommation de la conversation = celle de la tâche. Une conversation por tarea. One task per conversation.
- Claude annonce avant chaque tâche son niveau estimé (léger / moyen / lourd).
- À la fin, demandez « où sont passés mes tokens ? » (ES : « ¿en qué se gastaron mis tokens? », EN : « explain my usage ») pour voir le détail.
- Avec un abonnement Claude, on ne paie pas au token : la tâche consomme une part du forfait, visible dans les paramètres du compte (Team / Enterprise : tableaux de consommation pour les administrateurs).

## Safety
Claude asks before the first write in PJM, never deletes in PJM without explicit confirmation, never enters credentials, and asks before changing a shared material record.

## Version
1.4.0 – 17/10/2026 : nouveau skill reprendre-excel-pjm (Excel / Pressero → PJM, simulateur NCalc), pièges PJM validés (Decimal × Double, division par les poses, ToQty matériau, poids), création de ressources / procédés / matériaux, matériaux par laize au mètre linéaire.
1.3.0 – 17/10/2026 : position des étapes dans le rapport selon le flux de l'atelier, ordre des questions du formulaire automatique, groupe de prix laissé à PJM, fond perdu total dans CalcNup, masquage selon le papier choisi, formats fermés + personnalisé.
1.2.0 – 17/10/2026 : projet client conseillé, premier repère de consommation mesuré.
1.1.0 – 17/10/2026 : consommation (une tâche par conversation, estimation avant la tâche).
1.0.0 – 17/10/2026. Validated on two test engines (digital A4 brochure, Frontlit banner with automatic roll width and weight).
