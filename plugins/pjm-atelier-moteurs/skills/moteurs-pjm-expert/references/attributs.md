# Attributs PJM → Pressero (validé le 19/10/2026, moteur « Étiquettes en bobine »)

Les attributs d'un moteur PJM sont des paires clé / valeur renvoyées avec le prix. Pressero les reçoit à chaque calcul : ils servent à afficher des résultats dans la page produit (récapitulatif) et à piloter certaines fonctions de Pressero (date d'expédition).

## Où les mettre
- Sur un **composant** (ex. Calcul « Impression et bobinage ») : renvoyés à chaque calcul.
- Sur un **choix** d'une Option (ex. Mandrin 40 mm, Délai 3 jours) : renvoyés seulement quand ce choix est sélectionné. C'est la façon de « lire une option » côté Pressero.
- La **valeur est une formule NCalc** (Q1…, S1…, constantes) : `Q1*Q2`, `Q4+Q5`, `Q2*(Q4+Q5)*(Q3+5)*16E-9`, ou un nombre fixe `76`.

## Limites validées
- **Valeur ≤ 500 caractères** (sinon ErrorCode 437). Une formule longue (sélection de laize de 792 car.) ne tient pas : renvoyer les données de base (quantités, épaisseurs, grammages) et faire le calcul dans le script Pressero.
- **Deux attributs d'un même choix ne peuvent pas avoir la même valeur** (ErrorCode 433) : écrire l'expression autrement (`5+S1` et `S1+5`).
- Mêmes règles NCalc que les lignes : pas de littéral décimal (`16E-9`, pas `0.000000016`).
- PJM ne connaît ni la date ni l'heure : une donnée dynamique doit venir de la page (voir « Quantité technique » plus bas).

## Créer et rattacher (endpoints)
1. **Clé globale** (une fois par instance) : PJM → Paramètres → Attributs (`/Attributes`, grille). POST `/Attributes/Save` avec `Id` = `00000000-0000-0000-0000-000000000000`, `AttributeKey`, `AttributeType` 0, `StandardKeyType` 0, `IsDeleted` false, **`CreateDate` au format `jj/mm/aaaa hh:mm:ss`** (sans elle, la création échoue). Préfixer les clés par produit (`ETQ_…`) ; les clés réservées Pressero (`SHIP_DAYS`, `SHIP_DAYS_OUT_STOCK`) s'écrivent telles quelles.
2. **Rattachement** : ouvrir le formulaire `/ProductEngines/ComponentAttribute/{id du composant ou du choix}`, puis POST `/PECompAttributes/SaveAttributeModel` avec les champs du formulaire : `ComponentAttrributeId` (sic, 3 r ; 000… pour un nouveau), `ComponentId`, `OptionId`, `cid`, `SubscriberId`, `AttributeId` (Id de la clé globale), `Value`.
3. **Lecture / contrôle** : `/PECompAttributes/_Index?cid={id}`. Recharger la page d'édition du moteur puis tester.

## Ce que Pressero en fait
- Le résultat du calcul est passé à `intCalcFinish(e, a)` sur la page produit : `a.Attributes` = `[{Key, Value}]`, `a.Weight` = poids PJM en chaîne à virgule (« 1,68646 »). Script de récapitulatif : plugin `pressero-assistant-admin`, skill `recap-attributs-pjm`.
- **`SHIP_DAYS`** (et `SHIP_DAYS_OUT_STOCK`) : nombre de jours ouvrés que Pressero ajoute pour la date d'expédition, avec le **calendrier d'entreprise** Pressero (jours ouvrés + vacances, sans heure limite). Mettre un `SHIP_DAYS` par choix de délai.

## Quantité technique pour une donnée dynamique (heure limite)
PJM ne voit pas l'heure : créer une quantité **S1** « Jours ajoutés (heure limite) - champ technique » (min 0, max 10, défaut 0). Le script de la page produit calcule les jours à ajouter (après l'heure limite, jour non ouvré…) et écrit S1, ce qui relance le calcul ; les attributs utilisent S1 : `SHIP_DAYS = 5+S1`. Le script masque le champ. S1 ne doit jamais entrer dans le prix.
