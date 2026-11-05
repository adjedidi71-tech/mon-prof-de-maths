"""MathiCap Collège — cours et QCM originaux du chapitre 1 (5e).

Référence pédagogique : photos du manuel, chapitre Opérations, 18 pages.
Programme complémentaire : mathématiques de 5e, BO du 5 mars 2026.
Ce module n'effectue aucune écriture Supabase : validation pédagogique avant
connexion des scores au compte élève.
"""
from __future__ import annotations
import random
from uuid import uuid4
import streamlit as st

LESSONS = [{'id': 'decimaux', 'titre': 'Calculer avec des nombres décimaux', 'couleur': '#2D7BE8', 'icone': '🔢', 'temps': '7 min', 'objectif': 'Additionner, soustraire et multiplier des décimaux en gardant la bonne position de la virgule.', 'situation': 'Dans un jeu, tu gagnes 12,40 points puis 3,75 points bonus. Ton score augmente de 16,15 points.', 'comprendre': 'Un nombre décimal comporte une partie entière et une partie décimale. Pour additionner ou soustraire, les unités doivent se trouver sous les unités et les dixièmes sous les dixièmes.', 'methode': ['Addition et soustraction : écris les nombres en alignant les virgules.', 'Ajoute des zéros si besoin : 8,5 = 8,50.', 'Effectue le calcul colonne par colonne, puis replace la virgule au même endroit.', 'Multiplication : calcule d’abord sans les virgules, puis compte les chiffres décimaux des deux facteurs.'], 'exemples': [('Addition', '12{,}40+3{,}75=16{,}15', 'Les virgules sont alignées : 40 centièmes + 75 centièmes, avec retenue.'), ('Soustraction', '20{,}00-7{,}86=12{,}14', 'On peut ajouter des zéros à 20 pour écrire les centièmes.'), ('Multiplication', '2{,}4\\times1{,}5=3{,}60=3{,}6', '24 × 15 = 360 et les facteurs comportent deux chiffres décimaux au total.')], 'retenir': '\\boxed{\\text{Aligner les virgules pour }+,-\\quad;\\quad\\text{compter les décimales pour }\\times}', 'erreur': 'Ne place pas la virgule au hasard dans un produit. Vérifie avec un ordre de grandeur : 2,4 × 1,5 est proche de 2,5 × 1,5.', 'micro': ('Calcule 5,6 + 2,75.', '8,35', '5,6 = 5,60 ; donc 5,60 + 2,75 = 8,35.')}, {'id': 'euclidienne', 'titre': 'Division euclidienne, multiples et diviseurs', 'couleur': '#159B70', 'icone': '🧩', 'temps': '8 min', 'objectif': 'Trouver quotient et reste, puis reconnaître les multiples, diviseurs et critères de divisibilité.', 'situation': 'Tu veux ranger 77 cartes dans des pochettes de 9 cartes. Tu remplis 8 pochettes et il reste 5 cartes.', 'comprendre': 'La division euclidienne partage un nombre entier en groupes complets. Le quotient est le nombre de groupes, le reste est ce qui ne forme pas un groupe supplémentaire.', 'methode': ['Cherche le plus grand multiple du diviseur qui ne dépasse pas le dividende.', 'Écris le quotient, puis calcule le reste.', 'Vérifie l’égalité : dividende = diviseur × quotient + reste.', 'Vérifie toujours que 0 ≤ reste < diviseur.', 'Si le reste est zéro, le diviseur divise exactement le dividende.'], 'exemples': [('Quotient et reste', '77=9\\times8+5', 'Quotient 8, reste 5. Écriture : 77 ÷ 9 → quotient 8, reste 5.'), ('Multiple / diviseur', '42=6\\times7', '42 est un multiple de 6 et de 7 ; 6 et 7 sont des diviseurs de 42.'), ('Critère de 3 et de 9', '2+4+3=9', '243 est divisible par 3 et par 9, car la somme de ses chiffres vaut 9.')], 'retenir': '\\boxed{a=b\\times q+r\\quad\\text{avec}\\quad 0\\le r<b}', 'erreur': 'Écrire 77 ÷ 9 = 8 + 5 est faux. Il faut préciser « quotient 8, reste 5 » ou écrire 77 = 9 × 8 + 5.', 'micro': ('Quel est le reste de 53 ÷ 6 ?', '5', '6 × 8 = 48 ; 53 = 6 × 8 + 5.')}, {'id': 'division_decimale', 'titre': 'Diviser par un nombre décimal', 'couleur': '#E39A24', 'icone': '📏', 'temps': '7 min', 'objectif': 'Transformer une division par un nombre décimal en division par un entier.', 'situation': 'Tu as 8,4 litres de jus et des bouteilles de 0,7 litre. Tu peux remplir 12 bouteilles.', 'comprendre': 'Pour rendre le diviseur entier, on multiplie le dividende ET le diviseur par la même puissance de 10. Le quotient ne change pas.', 'methode': ['Repère combien de chiffres se trouvent après la virgule du diviseur.', 'Multiplie les deux nombres par 10, 100, etc. : la virgule se déplace autant de rangs dans les deux.', 'Effectue la division obtenue par un entier.', 'Contrôle : quotient × diviseur doit retrouver le dividende.'], 'exemples': [('Un chiffre décimal', '8{,}4\\div0{,}7=84\\div7=12', 'On multiplie les deux nombres par 10.'), ('Deux chiffres décimaux', '9{,}1\\div2{,}8=91\\div28=3{,}25', 'Le diviseur 2,8 a un chiffre décimal ; on multiplie donc les deux par 10.'), ('Autre exemple', '1{,}26\\div0{,}3=12{,}6\\div3=4{,}2', 'Vérification : 0,3 × 4,2 = 1,26.')], 'retenir': '\\boxed{a\\div b=(10a)\\div(10b)\\quad(b\\neq0)}', 'erreur': 'Ne déplace jamais la virgule du diviseur sans déplacer aussi celle du dividende.', 'micro': ('Calcule 6,3 ÷ 0,9.', '7', '6,3 ÷ 0,9 = 63 ÷ 9 = 7.')}, {'id': 'priorites', 'titre': 'Respecter les priorités opératoires', 'couleur': '#865BCA', 'icone': '🧠', 'temps': '7 min', 'objectif': 'Calculer une expression avec parenthèses, multiplications, divisions, additions et soustractions.', 'situation': 'Tu achètes 3 cahiers à 4 € et un stylo à 2 €. Le total est 3 × 4 + 2, soit 14 €, pas 18 €.', 'comprendre': 'Quand plusieurs opérations apparaissent, on suit des règles communes pour que chacun trouve le même résultat.', 'methode': ['Calcule d’abord les parenthèses, de l’intérieur vers l’extérieur.', 'Effectue les multiplications et divisions avant les additions et soustractions.', 'Entre opérations de même priorité, calcule de gauche à droite.', 'Réécris les étapes pour limiter les erreurs.'], 'exemples': [('Sans parenthèses', '18-3\\times4=18-12=6', 'La multiplication est prioritaire.'), ('Avec parenthèses', '(18-3)\\times4=15\\times4=60', 'Les parenthèses changent le résultat.'), ('Même priorité', '24\\div3\\times2=8\\times2=16', 'Division et multiplication se calculent ici de gauche à droite.')], 'retenir': '\\boxed{\\text{Parenthèses}\\;\\to\\;\\times,\\div\\;\\to\\;+,-}', 'erreur': 'Les multiplications ne sont pas toujours à faire avant les divisions : elles ont le même rang.', 'micro': ('Calcule 4 + 3 × 5.', '19', '3 × 5 = 15, puis 4 + 15 = 19.')}, {'id': 'distributivite', 'titre': 'Découvrir la distributivité simple', 'couleur': '#D96A8B', 'icone': '✨', 'temps': '8 min', 'objectif': 'Développer ou factoriser une expression avec une seule parenthèse, puis calculer astucieusement.', 'situation': 'Un rectangle mesure 3 cm de haut et (4 + 2) cm de long. Son aire totale est égale à la somme des aires de deux petits rectangles.', 'comprendre': 'La distributivité permet de multiplier chaque terme d’une somme ou d’une différence par un même nombre. Elle fonctionne aussi en sens inverse : on met le facteur commun en évidence.', 'methode': ['Repère le nombre devant la parenthèse.', 'Multiplie ce nombre par CHACUN des termes à l’intérieur.', 'Conserve le signe + ou − entre les deux produits.', 'Pour factoriser, retrouve le facteur commun aux deux termes.'], 'exemples': [('Développer une somme', '3\\times(4+2)=3\\times4+3\\times2=18', 'Deux petits rectangles : aires 12 cm² et 6 cm².'), ('Développer une différence', '5\\times(12-2)=5\\times12-5\\times2=50', 'Il faut multiplier les deux termes.'), ('Calculer astucieusement', '7\\times19=7\\times(20-1)=140-7=133', 'On choisit une décomposition facile à calculer.')], 'retenir': '\\boxed{k(a+b)=ka+kb\\quad;\\quad k(a-b)=ka-kb}', 'erreur': 'Attention : 3 × (4 + 2) ≠ 3 × 4 + 2. Il faut aussi multiplier le 2.', 'micro': ('Développe puis calcule 4 × (6 + 3).', '36', '4 × 6 + 4 × 3 = 24 + 12 = 36.')}]
QUESTION_BANK = {'decimaux': [{'id': 'd01', 'question': '12,4 + 3,75 = ?', 'options': ['15,79', '16,15', '15,115', '16,79'], 'answer': 1, 'explain': '12,40 + 3,75 = 16,15.', 'level': 1}, {'id': 'd02', 'question': '8,5 − 2,75 = ?', 'options': ['6,25', '5,75', '5,85', '6,75'], 'answer': 1, 'explain': '8,50 − 2,75 = 5,75.', 'level': 1}, {'id': 'd03', 'question': '2,4 × 1,5 = ?', 'options': ['3,6', '36', '2,9', '0,36'], 'answer': 0, 'explain': '24 × 15 = 360 ; avec deux chiffres décimaux, 3,60.', 'level': 1}, {'id': 'd04', 'question': '0,7 × 0,6 = ?', 'options': ['4,2', '0,42', '0,042', '1,3'], 'answer': 1, 'explain': '7 × 6 = 42 et deux chiffres décimaux : 0,42.', 'level': 1}, {'id': 'd05', 'question': '18,2 + 0,08 = ?', 'options': ['18,10', '18,28', '18,208', '18,82'], 'answer': 1, 'explain': '18,20 + 0,08 = 18,28.', 'level': 1}, {'id': 'd06', 'question': '15 − 4,65 = ?', 'options': ['11,65', '10,45', '10,35', '11,35'], 'answer': 2, 'explain': '15,00 − 4,65 = 10,35.', 'level': 1}, {'id': 'd07', 'question': '3,25 × 2 = ?', 'options': ['6,5', '6,05', '3,50', '65'], 'answer': 0, 'explain': 'Deux fois 3,25 donne 6,50.', 'level': 1}, {'id': 'd08', 'question': '0,4 + 0,06 = ?', 'options': ['0,10', '0,46', '0,406', '4,6'], 'answer': 1, 'explain': '0,40 + 0,06 = 0,46.', 'level': 1}, {'id': 'd09', 'question': '5,6 × 0,1 = ?', 'options': ['56', '5,06', '0,56', '0,056'], 'answer': 2, 'explain': 'Multiplier par 0,1 revient à diviser par 10.', 'level': 1}, {'id': 'd10', 'question': 'Un livre coûte 7,80 € et un stylo 1,35 €. Total ?', 'options': ['8,15 €', '8,95 €', '9,15 €', '9,25 €'], 'answer': 2, 'explain': '7,80 + 1,35 = 9,15 €.', 'level': 1}, {'id': 'd11', 'question': '12,04 − 1,9 = ?', 'options': ['11,14', '10,14', '10,24', '11,04'], 'answer': 1, 'explain': '12,04 − 1,90 = 10,14.', 'level': 1}, {'id': 'd12', 'question': '1,2 × 0,5 = ?', 'options': ['6', '0,6', '0,06', '1,7'], 'answer': 1, 'explain': '12 × 5 = 60 ; deux chiffres décimaux donnent 0,60.', 'level': 1}], 'euclidienne': [{'id': 'e01', 'question': '77 partagé en groupes de 9 : quotient et reste ?', 'options': ['8 et 5', '9 et 4', '7 et 8', '8 et 7'], 'answer': 0, 'explain': '77 = 9 × 8 + 5 et 5 est inférieur à 9.', 'level': 1}, {'id': 'e02', 'question': '53 ÷ 6 : quel reste ?', 'options': ['3', '4', '5', '6'], 'answer': 2, 'explain': '53 = 6 × 8 + 5.', 'level': 1}, {'id': 'e03', 'question': 'Dans une division euclidienne par 7, quel reste est impossible ?', 'options': ['0', '3', '6', '7'], 'answer': 3, 'explain': 'Le reste doit être strictement inférieur au diviseur, ici 7.', 'level': 1}, {'id': 'e04', 'question': 'Quel nombre est divisible par 9 ?', 'options': ['235', '243', '245', '248'], 'answer': 1, 'explain': '2 + 4 + 3 = 9, multiple de 9.', 'level': 1}, {'id': 'e05', 'question': 'Quel nombre est divisible par 3 mais PAS par 9 ?', 'options': ['135', '123', '117', '171'], 'answer': 1, 'explain': '1 + 2 + 3 = 6, divisible par 3 mais pas par 9.', 'level': 1}, {'id': 'e06', 'question': 'Lequel est un diviseur de 42 ?', 'options': ['5', '6', '8', '10'], 'answer': 1, 'explain': '42 = 6 × 7.', 'level': 1}, {'id': 'e07', 'question': 'Le nombre 48 est un multiple de…', 'options': ['5', '6', '7', '9'], 'answer': 1, 'explain': '48 = 6 × 8.', 'level': 1}, {'id': 'e08', 'question': '65 = 8 × 8 + 1. Quel est le quotient de 65 ÷ 8 ?', 'options': ['1', '7', '8', '9'], 'answer': 2, 'explain': '65 ÷ 8 : quotient 8, reste 1.', 'level': 1}, {'id': 'e09', 'question': 'Une division euclidienne est exacte quand…', 'options': ['le reste vaut 0', 'le quotient vaut 0', 'le diviseur vaut 1', 'le reste dépasse le diviseur'], 'answer': 0, 'explain': 'Une division exacte laisse un reste nul.', 'level': 1}, {'id': 'e10', 'question': 'Combien de sachets COMPLETS de 6 billes avec 38 billes ?', 'options': ['5', '6', '7', '8'], 'answer': 1, 'explain': '38 = 6 × 6 + 2 : 6 sachets complets.', 'level': 1}, {'id': 'e11', 'question': 'Quel est le reste de 100 ÷ 9 ?', 'options': ['0', '1', '2', '9'], 'answer': 1, 'explain': '100 = 9 × 11 + 1.', 'level': 1}, {'id': 'e12', 'question': 'Quel critère montre que 378 est divisible par 9 ?', 'options': ['Son dernier chiffre est pair', '3 + 7 + 8 = 18', 'Il finit par 8', 'Il est supérieur à 100'], 'answer': 1, 'explain': '3 + 7 + 8 = 18, multiple de 9.', 'level': 1}], 'division_decimale': [{'id': 'v01', 'question': '8,4 ÷ 0,7 = ?', 'options': ['1,2', '12', '0,12', '120'], 'answer': 1, 'explain': '8,4 ÷ 0,7 = 84 ÷ 7 = 12.', 'level': 1}, {'id': 'v02', 'question': '6,3 ÷ 0,9 = ?', 'options': ['0,7', '7', '70', '5,4'], 'answer': 1, 'explain': '63 ÷ 9 = 7.', 'level': 1}, {'id': 'v03', 'question': '1,26 ÷ 0,3 = ?', 'options': ['0,42', '42', '4,2', '3,6'], 'answer': 2, 'explain': '12,6 ÷ 3 = 4,2.', 'level': 1}, {'id': 'v04', 'question': '9,1 ÷ 2,8 = ?', 'options': ['32,5', '3,25', '2,8', '0,325'], 'answer': 1, 'explain': '91 ÷ 28 = 3,25.', 'level': 1}, {'id': 'v05', 'question': 'Pour transformer 5,6 ÷ 0,4, on écrit…', 'options': ['56 ÷ 4', '5,6 ÷ 4', '56 ÷ 0,4', '0,56 ÷ 4'], 'answer': 0, 'explain': 'Multiplier le dividende ET le diviseur par 10.', 'level': 1}, {'id': 'v06', 'question': '4,5 ÷ 0,5 = ?', 'options': ['0,9', '9', '90', '4'], 'answer': 1, 'explain': '45 ÷ 5 = 9.', 'level': 1}, {'id': 'v07', 'question': '1,2 ÷ 0,03 = ?', 'options': ['0,4', '4', '40', '400'], 'answer': 2, 'explain': 'Multiplier les deux nombres par 100 : 120 ÷ 3 = 40.', 'level': 1}, {'id': 'v08', 'question': 'Quelle égalité est vraie ?', 'options': ['2,4 ÷ 0,6 = 24 ÷ 6', '2,4 ÷ 0,6 = 2,4 ÷ 6', '2,4 ÷ 0,6 = 24 ÷ 0,6', '2,4 ÷ 0,6 = 0,24 ÷ 6'], 'answer': 0, 'explain': 'On déplace les deux virgules de la même façon.', 'level': 1}, {'id': 'v09', 'question': '3,6 ÷ 1,2 = ?', 'options': ['0,3', '3', '30', '4,8'], 'answer': 1, 'explain': '36 ÷ 12 = 3.', 'level': 1}, {'id': 'v10', 'question': '0,84 ÷ 0,07 = ?', 'options': ['1,2', '0,12', '12', '120'], 'answer': 2, 'explain': '84 ÷ 7 = 12.', 'level': 1}, {'id': 'v11', 'question': 'Pour vérifier 2,5 ÷ 0,5 = 5, on calcule…', 'options': ['5 + 0,5', '5 × 0,5', '2,5 × 0,5', '5 − 0,5'], 'answer': 1, 'explain': '5 × 0,5 = 2,5.', 'level': 1}, {'id': 'v12', 'question': 'Un ruban de 3,6 m est découpé en morceaux de 0,9 m. Nombre de morceaux ?', 'options': ['3', '4', '5', '9'], 'answer': 1, 'explain': '3,6 ÷ 0,9 = 36 ÷ 9 = 4.', 'level': 1}], 'priorites': [{'id': 'p01', 'question': '18 − 3 × 4 = ?', 'options': ['60', '6', '15', '24'], 'answer': 1, 'explain': '3 × 4 = 12, puis 18 − 12 = 6.', 'level': 1}, {'id': 'p02', 'question': '(18 − 3) × 4 = ?', 'options': ['6', '15', '60', '72'], 'answer': 2, 'explain': 'Parenthèses : 18 − 3 = 15, puis × 4.', 'level': 1}, {'id': 'p03', 'question': '4 + 3 × 5 = ?', 'options': ['35', '19', '23', '20'], 'answer': 1, 'explain': '3 × 5 = 15, puis 4 + 15 = 19.', 'level': 1}, {'id': 'p04', 'question': '24 ÷ 3 × 2 = ?', 'options': ['4', '16', '12', '2'], 'answer': 1, 'explain': 'Division et multiplication ont même priorité : de gauche à droite.', 'level': 1}, {'id': 'p05', 'question': '20 − (6 + 4) = ?', 'options': ['10', '18', '22', '30'], 'answer': 0, 'explain': '6 + 4 = 10, puis 20 − 10 = 10.', 'level': 1}, {'id': 'p06', 'question': '7 + 12 ÷ 3 = ?', 'options': ['19', '11', '6', '7'], 'answer': 1, 'explain': '12 ÷ 3 = 4, puis 7 + 4 = 11.', 'level': 1}, {'id': 'p07', 'question': '5 × (3 + 2) = ?', 'options': ['17', '25', '20', '15'], 'answer': 1, 'explain': 'La parenthèse vaut 5, donc 5 × 5 = 25.', 'level': 1}, {'id': 'p08', 'question': '30 ÷ 5 + 2 × 4 = ?', 'options': ['32', '14', '8', '24'], 'answer': 1, 'explain': '6 + 8 = 14.', 'level': 1}, {'id': 'p09', 'question': '9 − 8 ÷ 2 + 1 = ?', 'options': ['2', '6', '7', '1'], 'answer': 1, 'explain': '9 − 4 + 1 = 6.', 'level': 1}, {'id': 'p10', 'question': 'Quelle expression vaut 21 ?', 'options': ['3 × (5 + 2)', '3 × 5 + 2', '(3 + 5) × 2', '3 + 5 × 2'], 'answer': 0, 'explain': '3 × 7 = 21.', 'level': 1}, {'id': 'p11', 'question': '(12 + 8) ÷ 4 = ?', 'options': ['6', '5', '8', '20'], 'answer': 1, 'explain': '20 ÷ 4 = 5.', 'level': 1}, {'id': 'p12', 'question': '36 ÷ (3 × 4) = ?', 'options': ['48', '12', '3', '9'], 'answer': 2, 'explain': '3 × 4 = 12, puis 36 ÷ 12 = 3.', 'level': 1}], 'distributivite': [{'id': 't01', 'question': '3 × (4 + 2) = ?', 'options': ['3 × 4 + 2', '3 × 4 + 3 × 2', '3 + 4 × 2', '3 × 6 + 2'], 'answer': 1, 'explain': 'Distribuer 3 sur les deux termes : 12 + 6 = 18.', 'level': 1}, {'id': 't02', 'question': '5 × (12 − 2) = ?', 'options': ['5 × 12 − 5 × 2', '5 × 12 − 2', '5 × 10 − 2', '12 × 2 − 5'], 'answer': 0, 'explain': '5 × 12 − 5 × 2 = 60 − 10 = 50.', 'level': 1}, {'id': 't03', 'question': '4 × (6 + 3) = ?', 'options': ['30', '36', '24', '45'], 'answer': 1, 'explain': '4 × 6 + 4 × 3 = 24 + 12 = 36.', 'level': 1}, {'id': 't04', 'question': '7 × 19 = ?', 'options': ['7 × (20 − 1)', '7 × (20 + 1)', '7 + 20 − 1', '20 × (7 + 1)'], 'answer': 0, 'explain': '19 = 20 − 1, donc 140 − 7 = 133.', 'level': 1}, {'id': 't05', 'question': 'Quelle expression est égale à 2 × 5 + 2 × 3 ?', 'options': ['2 × (5 × 3)', '2 × (5 + 3)', '(2 + 5) × 3', '2 + 5 + 3'], 'answer': 1, 'explain': '2 est un facteur commun : 2 × (5 + 3).', 'level': 1}, {'id': 't06', 'question': '6 × (10 + 4) = ?', 'options': ['64', '84', '68', '140'], 'answer': 1, 'explain': '60 + 24 = 84.', 'level': 1}, {'id': 't07', 'question': '8 × 99 = ?', 'options': ['8 × (100 + 1)', '8 × (100 − 1)', '8 × 9 × 9', '800 + 8'], 'answer': 1, 'explain': '800 − 8 = 792.', 'level': 1}, {'id': 't08', 'question': '3 × (7 − 2) = ?', 'options': ['3 × 7 − 2', '3 × 7 − 3 × 2', '3 × 7 + 3 × 2', '3 × (7 + 2)'], 'answer': 1, 'explain': '21 − 6 = 15.', 'level': 1}, {'id': 't09', 'question': '2,5 × (8 + 2) = ?', 'options': ['20', '25', '10', '250'], 'answer': 1, 'explain': '2,5 × 8 + 2,5 × 2 = 20 + 5 = 25.', 'level': 1}, {'id': 't10', 'question': 'Quel est le facteur commun dans 9 × 4 + 9 × 6 ?', 'options': ['4', '6', '9', '10'], 'answer': 2, 'explain': 'Les deux termes contiennent le facteur 9.', 'level': 1}, {'id': 't11', 'question': '15 × 12 − 15 × 2 = ?', 'options': ['15 × 10', '15 × 14', '13 × 10', '15 × 12 × 2'], 'answer': 0, 'explain': '15 × (12 − 2) = 15 × 10 = 150.', 'level': 1}, {'id': 't12', 'question': 'Le développement correct de 2 × (a + b) est…', 'options': ['2a + b', '2a + 2b', 'a + 2b', '2ab'], 'answer': 1, 'explain': 'On multiplie a ET b par 2.', 'level': 1}]}
COURSE_IDS = [lesson['id'] for lesson in LESSONS]
COURSE_BY_ID = {lesson['id']: lesson for lesson in LESSONS}
COURSE_LABELS = {lesson['id']: lesson['titre'] for lesson in LESSONS}
ALL_KEY = 'melange'


def _style():
    st.html("""<style>
    .mc-lecon-entete {border-radius:22px;padding:23px 22px 17px;
        background:linear-gradient(115deg,#e9f4ff,#f6f1ff 68%,#fff4e5);
        border:1px solid #d9e7fa;max-width:900px;margin:6px 0 18px;}
    .mc-lecon-entete {position:relative;overflow:hidden;isolation:isolate;--mc-accent:#2778e2}
    .mc-lecon-entete::before {content:"π   ×   +   ÷";position:absolute;right:14px;top:12px;
        font-size:clamp(1.3rem,3.3vw,2.5rem);font-weight:850;letter-spacing:.16em;
        color:var(--mc-accent);opacity:.19;pointer-events:none;z-index:0;
        animation:mc-decoration 5s ease-in-out infinite}
    .mc-lecon-entete .mc-lecon-pastille {display:inline-block;color:var(--mc-accent);
        background:#fff;border-radius:999px;padding:5px 12px;font-weight:800;
        font-size:.8rem;margin-bottom:11px;box-shadow:0 3px 14px #bfd6ec55}
    .mc-lecon-entete h2 {color:#163a70;font-size:clamp(1.3rem,3.7vw,2rem);margin:4px 0 10px;line-height:1.2;max-width:680px}
    .mc-lecon-entete p, .mc-lecon-entete h2, .mc-lecon-pastille, .mc-mission {position:relative;z-index:1;}
    .mc-lecon-entete p {max-width:680px}
    .mc-lecon-entete .mc-mission {margin-top:12px;color:#47617f;font-size:.86rem}
    .st-key-mc_methode, .st-key-mc_exemples, .st-key-mc_micro_activite {max-width:900px;
        background:linear-gradient(120deg,#f3f8ff,#fffdf9);border-radius:20px;
        padding:15px 18px;margin:10px 0 14px;box-shadow:0 5px 20px rgba(40,74,125,.055)}
    .st-key-mc_methode {border-left:5px solid #68a7f7}
    .st-key-mc_exemples {border-left:5px solid #c8a4ec}
    .st-key-mc_micro_activite {border-left:5px solid #42b998}
    .mc-equation-demo {display:flex;gap:10px;align-items:center;max-width:850px;
        margin:10px 0 18px;flex-wrap:wrap}
    .mc-equation-demo .mc-equation-part {padding:10px 16px;border-radius:14px;
        background:#e8f2ff;color:#1b4b8c;font-size:clamp(.9rem,2.1vw,1.2rem);
        font-weight:750;box-shadow:0 3px 12px #bcd6ef44}
    .mc-equation-demo .mc-equation-part:nth-child(3) {background:#fff0d9;color:#9f5800}
    .mc-equation-demo .mc-arrow {font-size:1.7rem;color:#8881c5;font-weight:850}
    @media (prefers-reduced-motion:no-preference) {
      .mc-equation-demo .mc-arrow {animation:mc-arrow-move 2.8s ease-in-out infinite}
      @keyframes mc-arrow-move {0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}
    }
    @media (prefers-reduced-motion: reduce) { .mc-equation-demo .mc-arrow {animation:none!important} }
    .mc-quiz-box {position:relative;overflow:hidden;border-left:6px solid #4678ea}
    .mc-quiz-box::after {content:"?";position:absolute;right:14px;top:2px;color:#9db4ed;
        opacity:.25;font-size:clamp(3rem,8vw,6rem);font-weight:900;pointer-events:none}
    .mc-quiz-box h2 {position:relative;z-index:1;max-width:690px}
    @keyframes mc-decoration {0%,100%{transform:translateY(0)}50%{transform:translateY(5px)}}
    .mc-lecon-entete p {color:#3b557a;margin:0;line-height:1.55}
    .mc-lesson-block {max-width:900px;margin:12px 0;padding:16px 19px;
        background:var(--secondary-background-color,#f6f8fc);border-radius:16px;}
    .mc-lesson-block h3 {font-size:1.08rem;margin:0 0 10px;color:var(--text-color);}
    .mc-lesson-list {line-height:1.85;padding-left:20px;margin:4px 0;}
    .mc-kicker {font-weight:750;color:#205cbb;font-size:.82rem;letter-spacing:.025em}
    .mc-quiz-box {max-width:850px;border-radius:20px;padding:16px 19px;
         background:linear-gradient(115deg,#eff7ff,#f8f3ff);margin:13px 0;}
    .mc-quiz-box h2 {font-size:1.32rem;color:#173969;line-height:1.35;}
    @media (prefers-reduced-motion: reduce) { .mc-lecon-entete::before {animation:none !important} }
    @media (prefers-reduced-motion: no-preference) {
      .mc-lecon-entete {animation:mc-lesson-show .32s ease-out both}
      @keyframes mc-lesson-show {from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
    }
    @media(max-width:640px) {
       .mc-lecon-entete,.mc-lesson-block,.mc-quiz-box {padding:15px 13px;border-radius:15px}
       .mc-lecon-entete {margin-top:0}
    }
    </style>""")


def _notion_selector(widget_key, allow_all=False):
    keys = ([ALL_KEY] if allow_all else [])+COURSE_IDS
    def fmt(k):
        return 'Tout le chapitre — 10 questions mélangées' if k==ALL_KEY else COURSE_LABELS[k]
    old = st.session_state.get(widget_key)
    if old not in keys:
        st.session_state[widget_key] = COURSE_IDS[0]
    return st.selectbox('Choisir une notion',keys,format_func=fmt,key=widget_key,width='stretch')


# Illustrations conceptuelles : originales, légères, sans fichiers externes.
FIGURES = {
    'decimaux': ('12,40 + 3,75', '16,15'),
    'euclidienne': ('77 cartes ÷ 9', '8 groupes + 5 cartes'),
    'division_decimale': ('8,4 ÷ 0,7', '84 ÷ 7 = 12'),
    'priorites': ('Parenthèses', '× ÷ puis + −'),
    'distributivite': ('3 × (4 + 2)', '3 × 4 + 3 × 2'),
}


def _illustrer_notion(notion):
    gauche, droite = FIGURES[notion]
    st.html(
        '<div class="mc-equation-demo" role="img" aria-label="Étape de calcul : '
        + gauche + ' donne ' + droite + '">'
        + '<span class="mc-equation-part">' + gauche + '</span>'
        + '<span class="mc-arrow" aria-hidden="true">→</span>'
        + '<span class="mc-equation-part">' + droite + '</span></div>'
    )


def afficher_cours(aller_vers=None):
    _style()
    st.subheader('Cours & points à retenir')
    st.caption('5e · Chapitre 1 — Opérations · 5 leçons progressives')
    notion = _notion_selector('mathicap_cours_notion')
    l=COURSE_BY_ID[notion]
    position = COURSE_IDS.index(notion) + 1
    st.html(
        f'<div class="mc-lecon-entete" style="--mc-accent:{l["couleur"]}">'
        f'<div class="mc-lecon-pastille">{l["icone"]} MISSION {position} / 5 · {l["temps"]}</div>'
        f'<h2>{l["titre"]}</h2><p>{l["objectif"]}</p>'
        f'<div class="mc-mission">🔍 Découvrir · Comprendre · Tester</div></div>'
    )
    st.markdown('#### 🎯 Je découvre')
    st.info(l['situation'],width=850)
    _illustrer_notion(notion)
    st.markdown('#### 💡 Je comprends')
    st.markdown(l['comprendre'])
    with st.container(key='mc_methode'):
        st.markdown('#### 🧭 La méthode, pas à pas')
        for i,step in enumerate(l['methode'],start=1):
            st.markdown(f'**{i}.** {step}')
    with st.container(key='mc_exemples'):
        st.markdown('#### 🔎 Exemples guidés')
        for titre,formule,explication in l['exemples']:
            with st.expander('▸ '+titre,expanded=False):
                st.latex(formule)
                st.caption(explication)
    st.markdown('#### 📌 À retenir')
    st.latex(l['retenir'])
    st.markdown('#### ⚠️ Erreur à éviter')
    st.warning(l['erreur'],width=850)
    if notion=='distributivite':
        st.markdown('#### 🎨 Laboratoire interactif : dessine la distributivité')
        st.caption('Déplace les curseurs : les deux aires et l’égalité se mettent à jour.')
        col_a,col_b,col_c=st.columns(3, gap='small')
        with col_a:
            k=st.slider('Hauteur',min_value=2,max_value=6,value=3,key='mc_distrib_hauteur')
        with col_b:
            a=st.slider('Largeur bleue',min_value=2,max_value=8,value=4,key='mc_distrib_a')
        with col_c:
            b=st.slider('Largeur jaune',min_value=1,max_value=6,value=2,key='mc_distrib_b')
        st.html(f'''<div style="max-width:560px;display:flex;gap:3px;align-items:stretch;
        height:115px;color:#14355f;font-size:clamp(.85rem,2.5vw,1.13rem);font-weight:750;text-align:center">
         <div style="flex:{a};background:#bee3ff;display:flex;align-items:center;
           justify-content:center;border:2px solid #2c7ed5;border-radius:8px 0 0 8px">{k} × {a} = {k*a}</div>
         <div style="flex:{b};background:#ffe6ad;display:flex;align-items:center;
           justify-content:center;border:2px solid #e7a333;border-radius:0 8px 8px 0">{k} × {b} = {k*b}</div></div>''')
        st.latex(f'{k}\\times({a}+{b})={k}\\times{a}+{k}\\times{b}={k*(a+b)}')
        st.caption('La grande aire et les deux petites aires ont exactement la même valeur.')
    st.markdown('#### ✍️ À toi de jouer')
    prompt,rep,explication=l['micro']
    with st.container(key='mc_micro_activite'):
        with st.form('mathicap_micro_'+notion):
            st.write(prompt)
            entree=st.text_input('Ta réponse',key='mc_micro_rep_'+notion,width=280)
            go=st.form_submit_button('Vérifier ma réponse')
        if go:
            norm=lambda s:s.strip().replace(' ','').replace(',','.')
            if norm(entree)==norm(rep):
                st.success('Bravo ! '+explication,width=850)
            else:
                st.info('Essaie encore. Indice : '+explication,width=850)
    st.divider()
    if st.button('✅ Passer au QCM de cette notion',key='mc_cours_vers_qcm'):
        st.session_state['mathicap_qcm_notion']=notion
        st.session_state.pop('mathicap_qcm_partie',None)
        if aller_vers: aller_vers('QCM')
        st.rerun()


def _tirer_questions(notion):
    hasard=random.SystemRandom()
    if notion==ALL_KEY:
        questions=[]
        for identifiant in COURSE_IDS:
            questions += hasard.sample(QUESTION_BANK[identifiant],2)
        hasard.shuffle(questions)
    else:
        questions = hasard.sample(QUESTION_BANK[notion],10)
    # Une seule bonne réponse ; l’ordre des choix change à chaque nouveau QCM.
    resultat=[]
    for question in questions:
        ordre=list(range(len(question['options'])))
        hasard.shuffle(ordre)
        copie=dict(question)
        copie['options']=[question['options'][j] for j in ordre]
        copie['answer']=ordre.index(question['answer'])
        resultat.append(copie)
    return resultat

def _demarrer(notion):
    st.session_state['mathicap_qcm_partie']={
       'id':uuid4().hex[:10],'notion':notion,'questions':_tirer_questions(notion),
       'index':0,'reponses':{},'validee':False,
    }


def afficher_qcm(aller_vers=None):
    _style()
    st.subheader('QCM rapides')
    st.caption('5e · Chapitre 1 — Opérations · 10 questions par QCM')
    select = _notion_selector('mathicap_qcm_notion',allow_all=True)
    partie=st.session_state.get('mathicap_qcm_partie')
    if partie and partie['notion']!=select:
        st.info('Une partie est en cours dans une autre notion. Démarre un nouveau QCM pour changer.',width=850)
    c1,c2=st.columns([1,3],gap='small')
    with c1:
        if st.button('🎯 Démarrer un QCM',key='mc_qcm_demarrer',width='stretch'):
            _demarrer(select);st.rerun()
    if not partie:
        st.info('Choisis une notion, puis démarre un QCM de 10 questions. Tu obtiendras une explication après chaque réponse.',width=850)
        if st.button('📖 Revoir le cours',key='mc_qcm_vers_cours'):
            if select in COURSE_IDS: st.session_state['mathicap_cours_notion']=select
            if aller_vers: aller_vers('Cours')
            st.rerun()
        return
    i=partie['index'];questions=partie['questions'];ident=partie['id']
    if i>=len(questions):
        bonnes=sum(1 for q in questions if partie['reponses'].get(q['id'])==q['answer'])
        score=int(100*bonnes/len(questions))
        st.markdown('### 🏅 Mission terminée !')
        st.metric('Ton score',f'{bonnes} / 10')
        st.progress(score/100,text=f'{score} % de bonnes réponses')
        if bonnes>=8: st.success('Très bien ! Tu maîtrises l’essentiel de ces questions.',width=850)
        elif bonnes>=5: st.info('Bon début ! Revois les erreurs puis retente ta chance.',width=850)
        else: st.info('Continue à t’entraîner : relis le cours et réessaie.',width=850)
        with st.expander('🔎 Revoir mes 10 réponses',expanded=False):
            for idx,q in enumerate(questions,1):
                bonne=q['options'][q['answer']]
                rep=partie['reponses'].get(q['id'])
                donne=q['options'][rep] if rep is not None else 'Non renseignée'
                st.markdown(f'**{idx}. {q["question"]}**')
                st.write(f'Ta réponse : {donne} · Bonne réponse : {bonne}')
                st.caption(q['explain'])
                st.divider()
        st.caption('Ce premier modèle n’enregistre pas encore les scores dans Supabase. Les séries d’exercices existantes ne sont pas modifiées.')
        if st.button('↻ Nouveau QCM',key='mc_qcm_recommencer'):
            _demarrer(select); st.rerun()
        return
    q=questions[i]
    st.progress(i/10,text=f'Question {i+1} sur 10')
    st.html('<div class="mc-quiz-box"><div class="mc-kicker">QUESTION '+str(i+1)+'/10</div><h2>'+str(q['question'])+'</h2></div>')
    champ='mc_qcm_radio_'+ident+'_'+str(i)
    reponse=st.radio('Choisis une seule réponse',q['options'],index=None,key=champ,disabled=partie['validee'])
    if not partie['validee']:
        if st.button('Vérifier ma réponse',key='mc_qcm_valider',disabled=reponse is None):
            partie['reponses'][q['id']]=q['options'].index(reponse)
            partie['validee']=True
            st.rerun()
    else:
        correcte=partie['reponses'][q['id']]==q['answer']
        if correcte: st.success('Bonne réponse !',width=850)
        else: st.error('Réponse incorrecte. La bonne réponse est : '+q['options'][q['answer']],width=850)
        st.markdown('**Explication :** '+q['explain'])
        if st.button('Question suivante →' if i<9 else 'Voir mon résultat →',key='mc_qcm_suivante'):
            partie['index']+=1
            partie['validee']=False
            st.rerun()
