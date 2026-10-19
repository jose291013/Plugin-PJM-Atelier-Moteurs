# Calendriers d'entreprise (date d'expédition) — validé le 19/10/2026

Admin compte : Préférences → **Calendriers d'entreprise** (`/calendars`). Un calendrier est partagé par plusieurs sites (« Default Calendar » : 46 sites sur l'instance de démo) → **demander l'accord avant de le modifier**, une modification touche tous ces sites.

## Contenu
- Jours ouvrés (lun–ven par défaut).
- **Vacances** : une ligne par jour fermé, avec Nom, Jour, Mois et Année. **Année vide = répété chaque année** (fériés fixes : 1/1, 1/5, 8/5, 14/7, 15/8, 1/11, 11/11, 25/12). Année remplie = ce jour-là seulement (fêtes mobiles, fermetures).
- Pas d'heure limite de commande : à gérer par script (skill `recap-attributs-pjm`).

## Usage
- Pressero calcule la date d'expédition = date de commande + `SHIP_DAYS` jours ouvrés de ce calendrier (`SHIP_DAYS` = attribut renvoyé par le moteur PJM ou réglage du produit ; `SHIP_DAYS_OUT_STOCK` hors stock).
- Fêtes mobiles françaises (Lundi de Pâques, Ascension = Pâques + 39, Lundi de Pentecôte = Pâques + 50) : à saisir année par année. Saisies jusqu'en 2028 sur la démo ; 2029 : 2/4, 10/5, 21/5.

## Modifier par l'admin
- La liste des vacances s'édite dans des fenêtres modales (iframes Kendo). Modifier une ligne : `/Calendars/EditCalendarHoliday/{calendarId}?calendarHolidayId={id}&_modalLayout=True`.
- **Piège** : un jour enregistré avec l'année courante n'est plus répété. Rouvrir la ligne par l'URL ci-dessus, vider `Year` et enregistrer ; vérifier ensuite la colonne Année de la liste.
- Après ajout : contrôler le nombre de vacances affiché et la liste complète ; ne jamais supprimer une ligne sans demande explicite.
