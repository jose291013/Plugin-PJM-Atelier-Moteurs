# Exemple validé : « Étiquettes en bobine » (Excel Pressero → PJM, 17/10/2026)

Moteur de démonstration : prix identiques à l'Excel à 0,01 € près sur 4 cas, poids identique.

## Excel d'origine (logique reproduite à l'identique)
- Entrées : Q1 nombre de bobines, Q2 étiquettes par bobine, Q3 laize étiquette (mm), Q4 hauteur (mm), Q5 espace (mm), R1 diamètre maxi (info).
- S = Q2·(Q4+5)·(Q3+5)/1e6 (surface d'UNE bobine) → coefficient 4,5 / 4 / 3,5 / 2,5 / 2 (paliers 2,1 / 5,1 / 20,1 / 100,1).
- Impression = (S·Q1·1,5 + 20 calage) × coef. Frais de 1er tirage 80 € (hors coef). Délai : 0 / +25 % / +40 % (markup PJM).
- Une seule laize de bobine mère par commande parmi 220 / 180 / 140 / 100 mm, toutes les bobines client côte à côte :
  poses = Min(Q1, floor(W/(Q3+20))) (100 mm : Q1 si Q1 ≤ floor(80/(Q3+5)), sinon floor(100/(Q3+20))),
  mises en route MR = Ceiling(Q1/poses), ml = MR·Q2·(Q4+Q5)/1000,
  coût de sélection = MR·(Q2·(Q4+Q5)·0,9·W/1e6 + 5) (prix papier, même en polypro) ; la moins chère, égalité → la plus large.
- Support = ml × prix/ml × coef ; changement de bobine 5 € × MR × coef ; pelliculage = Max(ml × prix/ml, 5 €) × coef sur la même laize.
- Poids = ml × laize × kg/m² (support) + Q2·(Q4+Q5)·(Q3+5)/1e6 × kg/m² (film, bizarrerie de l'Excel : une seule bobine).

## Structure PJM
- Ressource « Presse étiquettes » : Impression étiquettes (1 €/u), Frais de 1er tirage (1 €/u), Changement de bobine (0,01 €/u = centimes).
- Calcul « Impression et bobinage » : Impression étiquettes (position 2, poses vide) ; Changement de bobine (position 2, poses = formule de laize, quantité × 100 × Nup() car PJM divise par les poses et arrondit à l'unité).
- Option Type de tirage → 1er tirage : Frais de 1er tirage, quantité `80`, position 1.
- Options Support (Papier / Polypro) et Pelliculage (Aucun / Brillant / Mat) : 4 lignes matériau par choix, une par laize, matériaux « Étiquette papier adhésif - laize 220 mm (ml) » (220 × 1000 mm, prix au ml), ToQty 999999.
- Options informatives sans ligne : Mandrin, Pose, Orientation, Impression.

## Formules (copiées du moteur validé)
Coefficient (repris dans plusieurs formules) :
```
if((Q2*(Q4+5)*(Q3+5)/1E6) < 21E-1, 45E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 51E-1, 4, if((Q2*(Q4+5)*(Q3+5)/1E6) < 201E-1, 35E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 1001E-1, 25E-1, 2))))
```
Poses de toutes les lignes laize et de « Changement de bobine » = laize retenue (renvoie 220/180/140/100) :
```
if(Ceiling(Q1/Max(Min(Q1, floor(220/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*198E-6+5) <= Min(Min(Ceiling(Q1/Max(Min(Q1, floor(180/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*162E-6+5),Ceiling(Q1/Max(Min(Q1, floor(140/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*126E-6+5)),Ceiling(Q1/Max(if(Q1 <= floor(80/(Q3+5E0)), Q1, floor(100/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*9E-5+5)), 220, if(Ceiling(Q1/Max(Min(Q1, floor(180/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*162E-6+5) <= Min(Ceiling(Q1/Max(Min(Q1, floor(140/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*126E-6+5),Ceiling(Q1/Max(if(Q1 <= floor(80/(Q3+5E0)), Q1, floor(100/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*9E-5+5)), 180, if(Ceiling(Q1/Max(Min(Q1, floor(140/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*126E-6+5) <= Ceiling(Q1/Max(if(Q1 <= floor(80/(Q3+5E0)), Q1, floor(100/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*9E-5+5), 140, 100)))
```
Impression étiquettes (quantité, en €) :
```
if((Q2*(Q4+5)*(Q3+5)/1E6) < 21E-1, 45E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 51E-1, 4, if((Q2*(Q4+5)*(Q3+5)/1E6) < 201E-1, 35E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 1001E-1, 25E-1, 2))))*((Q2*(Q4+5)*(Q3+5)/1E6)*Q1*15E-1+20)
```
Changement de bobine (quantité, en centimes ; poses = formule de laize) :
```
(if((Q2*(Q4+5)*(Q3+5)/1E6) < 21E-1, 45E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 51E-1, 4, if((Q2*(Q4+5)*(Q3+5)/1E6) < 201E-1, 35E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 1001E-1, 25E-1, 2))))*5*Ceiling(Q1/if(Nup() = 100, if(Q1 <= floor(80/(Q3+5E0)), Q1, floor(100/(Q3+2E1))), Min(Q1, floor(Nup()/(Q3+2E1))))))*100*Nup()
```
Ligne papier laize 220 mm — quantité (ml × coef) :
```
if(Nup() = 220, if((Q2*(Q4+5)*(Q3+5)/1E6) < 21E-1, 45E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 51E-1, 4, if((Q2*(Q4+5)*(Q3+5)/1E6) < 201E-1, 35E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 1001E-1, 25E-1, 2))))*Ceiling(Q1/Max(Min(Q1, floor(220/(Q3+2E1))), 1E-9))*Q2*(Q4+Q5)/1E3, 0)
```
Ligne papier laize 220 mm — calcul du poids (recalcule la laize : Nup() vaut 1 dans le poids) :
```
if(if(Ceiling(Q1/Max(Min(Q1, floor(220/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*198E-6+5) <= Min(Min(Ceiling(Q1/Max(Min(Q1, floor(180/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*162E-6+5),Ceiling(Q1/Max(Min(Q1, floor(140/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*126E-6+5)),Ceiling(Q1/Max(if(Q1 <= floor(80/(Q3+5E0)), Q1, floor(100/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*9E-5+5)), 220, if(Ceiling(Q1/Max(Min(Q1, floor(180/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*162E-6+5) <= Min(Ceiling(Q1/Max(Min(Q1, floor(140/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*126E-6+5),Ceiling(Q1/Max(if(Q1 <= floor(80/(Q3+5E0)), Q1, floor(100/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*9E-5+5)), 180, if(Ceiling(Q1/Max(Min(Q1, floor(140/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*126E-6+5) <= Ceiling(Q1/Max(if(Q1 <= floor(80/(Q3+5E0)), Q1, floor(100/(Q3+2E1))), 1E-9))*(Q2*(Q4+Q5)*9E-5+5), 140, 100))) = 220, Ceiling(Q1/Max(Min(Q1, floor(220/(Q3+2E1))), 1E-9))*Q2*(Q4+Q5)*220*315E-9, 0)
```
Ligne pelliculage brillant laize 220 mm — quantité (minimum 5 € : 5 / prix du ml) :
```
if(Nup() = 220, if((Q2*(Q4+5)*(Q3+5)/1E6) < 21E-1, 45E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 51E-1, 4, if((Q2*(Q4+5)*(Q3+5)/1E6) < 201E-1, 35E-1, if((Q2*(Q4+5)*(Q3+5)/1E6) < 1001E-1, 25E-1, 2))))*Max(Ceiling(Q1/Max(Min(Q1, floor(220/(Q3+2E1))), 1E-9))*Q2*(Q4+Q5)/1E3, 5/136840E-6), 0)
```
Autres lignes : remplacer 220 par la laize, le prix au ml (`5/136840E-6` → prix brillant 0,13684 €/ml en 220) et le poids (315E-9 papier, 145E-9 polypro, 16E-9 brillant, 27E-9 mat, en kg par mm²).

## Tests (groupe « Sur barême + 0 % »)
| Cas | Excel | PJM | Matériau | Poids |
|---|---|---|---|---|
| 2 × 1000, 15×150, esp. 3, papier, 1er tirage, 5 j | 272,28 | 272,28 | papier 100 mm | 4,82 |
| 5 × 500, 40×60, esp. 2, polypro + brillant, 3 j | 527,05 | 527,06 | 180 mm | 1,64 |
| 1 × 2000, 100×50, esp. 3, papier + mat, réimpression, express | 324,04 | 324,03 | 140 mm | 4,98 |
| 10 × 3000, 60×80, esp. 3, polypro + mat, 1er tirage, 5 j | 3 628,58 | 3 628,59 | 180 mm | 32,93 |

## Limites
- Non reproductible : date estimée de livraison, blocage « 50 à N étiquettes par bobine » selon le diamètre, arrondi Excel au 0,1 € supérieur.
- La quantité matériau affichée = ml × coefficient (marge intégrée dans les formules) ; l'instruction de la ligne le précise.
