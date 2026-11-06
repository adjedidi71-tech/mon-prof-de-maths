"""MathiCap Collège — cours et QCM originaux du chapitre 1 (5e).

Référence pédagogique : photos du manuel, chapitre Opérations, 18 pages.
Programme complémentaire : mathématiques de 5e, BO du 5 mars 2026.
Les scores des QCM terminés sont enregistrés séparément dans Supabase,
après vérification de la session de l'élève.
"""
from __future__ import annotations
import random
from html import escape
from uuid import uuid4
import streamlit as st

LESSONS = [{'id': 'decimaux', 'titre': 'Calculer avec des nombres décimaux', 'couleur': '#2D7BE8', 'icone': '🔢', 'temps': '7 min', 'objectif': 'Additionner, soustraire et multiplier des décimaux en gardant la bonne position de la virgule.', 'situation': 'Dans un jeu, tu gagnes 12,40 points puis 3,75 points bonus. Ton score augmente de 16,15 points.', 'comprendre': 'Un nombre décimal comporte une partie entière et une partie décimale. Pour additionner ou soustraire, les unités doivent se trouver sous les unités et les dixièmes sous les dixièmes.', 'methode': ['Addition et soustraction : écris les nombres en alignant les virgules.', 'Ajoute des zéros si besoin : 8,5 = 8,50.', 'Effectue le calcul colonne par colonne, puis replace la virgule au même endroit.', 'Multiplication : calcule d’abord sans les virgules, puis compte les chiffres décimaux des deux facteurs.'], 'exemples': [('Addition', '12{,}40+3{,}75=16{,}15', 'Les virgules sont alignées : 40 centièmes + 75 centièmes, avec retenue.'), ('Soustraction', '20{,}00-7{,}86=12{,}14', 'On peut ajouter des zéros à 20 pour écrire les centièmes.'), ('Multiplication', '2{,}4\\times1{,}5=3{,}60=3{,}6', '24 × 15 = 360 et les facteurs comportent deux chiffres décimaux au total.')], 'retenir': '\\boxed{\\text{Aligner les virgules pour }+,-\\quad;\\quad\\text{compter les décimales pour }\\times}', 'erreur': 'Ne place pas la virgule au hasard dans un produit. Vérifie avec un ordre de grandeur : 2,4 × 1,5 est proche de 2,5 × 1,5.', 'micro': ('Calcule 5,6 + 2,75.', '8,35', '5,6 = 5,60 ; donc 5,60 + 2,75 = 8,35.')}, {'id': 'euclidienne', 'titre': 'Division euclidienne, multiples et diviseurs', 'couleur': '#159B70', 'icone': '🧩', 'temps': '8 min', 'objectif': 'Trouver quotient et reste, puis reconnaître les multiples, diviseurs et critères de divisibilité.', 'situation': 'Tu veux ranger 77 cartes dans des pochettes de 9 cartes. Tu remplis 8 pochettes et il reste 5 cartes.', 'comprendre': 'La division euclidienne partage un nombre entier en groupes complets. Le quotient est le nombre de groupes, le reste est ce qui ne forme pas un groupe supplémentaire.', 'methode': ['Cherche le plus grand multiple du diviseur qui ne dépasse pas le dividende.', 'Écris le quotient, puis calcule le reste.', 'Vérifie l’égalité : dividende = diviseur × quotient + reste.', 'Vérifie toujours que 0 ≤ reste < diviseur.', 'Si le reste est zéro, le diviseur divise exactement le dividende.'], 'exemples': [('Quotient et reste', '77=9\\times8+5', 'Quotient 8, reste 5. Écriture : 77 ÷ 9 → quotient 8, reste 5.'), ('Multiple / diviseur', '42=6\\times7', '42 est un multiple de 6 et de 7 ; 6 et 7 sont des diviseurs de 42.'), ('Critère de 3 et de 9', '2+4+3=9', '243 est divisible par 3 et par 9, car la somme de ses chiffres vaut 9.')], 'retenir': '\\boxed{a=b\\times q+r\\quad\\text{avec}\\quad 0\\le r<b}', 'erreur': 'Écrire 77 ÷ 9 = 8 + 5 est faux. Il faut préciser « quotient 8, reste 5 » ou écrire 77 = 9 × 8 + 5.', 'micro': ('Quel est le reste de 53 ÷ 6 ?', '5', '6 × 8 = 48 ; 53 = 6 × 8 + 5.')}, {'id': 'division_decimale', 'titre': 'Diviser par un nombre décimal', 'couleur': '#E39A24', 'icone': '📏', 'temps': '7 min', 'objectif': 'Transformer une division par un nombre décimal en division par un entier.', 'situation': 'Tu as 8,4 litres de jus et des bouteilles de 0,7 litre. Tu peux remplir 12 bouteilles.', 'comprendre': 'Pour rendre le diviseur entier, on multiplie le dividende ET le diviseur par la même puissance de 10. Le quotient ne change pas.', 'methode': ['Repère combien de chiffres se trouvent après la virgule du diviseur.', 'Multiplie les deux nombres par 10, 100, etc. : la virgule se déplace autant de rangs dans les deux.', 'Effectue la division obtenue par un entier.', 'Contrôle : quotient × diviseur doit retrouver le dividende.'], 'exemples': [('Un chiffre décimal', '8{,}4\\div0{,}7=84\\div7=12', 'On multiplie les deux nombres par 10.'), ('Deux chiffres décimaux', '9{,}1\\div2{,}8=91\\div28=3{,}25', 'Le diviseur 2,8 a un chiffre décimal ; on multiplie donc les deux par 10.'), ('Autre exemple', '1{,}26\\div0{,}3=12{,}6\\div3=4{,}2', 'Vérification : 0,3 × 4,2 = 1,26.')], 'retenir': '\\boxed{a\\div b=(10a)\\div(10b)\\quad(b\\neq0)}', 'erreur': 'Ne déplace jamais la virgule du diviseur sans déplacer aussi celle du dividende.', 'micro': ('Calcule 6,3 ÷ 0,9.', '7', '6,3 ÷ 0,9 = 63 ÷ 9 = 7.')}, {'id': 'priorites', 'titre': 'Respecter les priorités opératoires', 'couleur': '#865BCA', 'icone': '🧠', 'temps': '7 min', 'objectif': 'Calculer une expression avec parenthèses, multiplications, divisions, additions et soustractions.', 'situation': 'Tu achètes 3 cahiers à 4 € et un stylo à 2 €. Le total est 3 × 4 + 2, soit 14 €, pas 18 €.', 'comprendre': 'Quand plusieurs opérations apparaissent, on suit des règles communes pour que chacun trouve le même résultat.', 'methode': ['Calcule d’abord les parenthèses, de l’intérieur vers l’extérieur.', 'Effectue les multiplications et divisions avant les additions et soustractions.', 'Entre opérations de même priorité, calcule de gauche à droite.', 'Réécris les étapes pour limiter les erreurs.'], 'exemples': [('Sans parenthèses', '18-3\\times4=18-12=6', 'La multiplication est prioritaire.'), ('Avec parenthèses', '(18-3)\\times4=15\\times4=60', 'Les parenthèses changent le résultat.'), ('Même priorité', '24\\div3\\times2=8\\times2=16', 'Division et multiplication se calculent ici de gauche à droite.')], 'retenir': '\\boxed{\\text{Parenthèses}\\;\\to\\;\\times,\\div\\;\\to\\;+,-}', 'erreur': 'Les multiplications ne sont pas toujours à faire avant les divisions : elles ont le même rang.', 'micro': ('Calcule 4 + 3 × 5.', '19', '3 × 5 = 15, puis 4 + 15 = 19.')}, {'id': 'distributivite', 'titre': 'Découvrir la distributivité simple', 'couleur': '#D96A8B', 'icone': '✨', 'temps': '8 min', 'objectif': 'Développer ou factoriser une expression avec une seule parenthèse, puis calculer astucieusement.', 'situation': 'Un rectangle mesure 3 cm de haut et (4 + 2) cm de long. Son aire totale est égale à la somme des aires de deux petits rectangles.', 'comprendre': 'La distributivité permet de multiplier chaque terme d’une somme ou d’une différence par un même nombre. Elle fonctionne aussi en sens inverse : on met le facteur commun en évidence.', 'methode': ['Repère le nombre devant la parenthèse.', 'Multiplie ce nombre par CHACUN des termes à l’intérieur.', 'Conserve le signe + ou − entre les deux produits.', 'Pour factoriser, retrouve le facteur commun aux deux termes.'], 'exemples': [('Développer une somme', '3\\times(4+2)=3\\times4+3\\times2=18', 'Deux petits rectangles : aires 12 cm² et 6 cm².'), ('Développer une différence', '5\\times(12-2)=5\\times12-5\\times2=50', 'Il faut multiplier les deux termes.'), ('Calculer astucieusement', '7\\times19=7\\times(20-1)=140-7=133', 'On choisit une décomposition facile à calculer.')], 'retenir': '\\boxed{k(a+b)=ka+kb\\quad;\\quad k(a-b)=ka-kb}', 'erreur': 'Attention : 3 × (4 + 2) ≠ 3 × 4 + 2. Il faut aussi multiplier le 2.', 'micro': ('Développe puis calcule 4 × (6 + 3).', '36', '4 × 6 + 4 × 3 = 24 + 12 = 36.')}]
# Phrases choisies pour le niveau 5e : aucun symbole d'inégalité nécessaire.
NOTES_SIMPLES = {
    'decimaux': (
        "Addition et soustraction : place les virgules l’une sous l’autre, "
        "puis calcule colonne par colonne. Exemple : 5,6 + 2,75 = 5,60 + 2,75 = 8,35.\n"
        "Multiplication : il ne faut PAS aligner les virgules. "
        "Calcule d’abord comme s’il n’y avait pas de virgule : 24 × 15 = 360. "
        "Dans 2,4 × 1,5, les deux nombres ont au total deux chiffres après leur virgule : "
        "on compte donc deux chiffres en partant de la droite de 360, ce qui donne 3,60, soit 3,6."
    ),
    'euclidienne': (
        "Dividende = diviseur × quotient + reste. "
        "Le reste doit être plus petit que le diviseur. "
        "Exemple : 77 = 9 × 8 + 5. On peut former 8 groupes de 9 et il reste 5."
    ),
    'division_decimale': (
        "Quand le diviseur a une virgule, transforme-le en nombre entier. "
        "S’il a un chiffre après la virgule, multiplie LES DEUX nombres par 10. "
        "Exemple : 8,4 ÷ 0,7 devient 84 ÷ 7 = 12 : le résultat ne change pas.\n"
        "S’il a deux chiffres après la virgule, multiplie les deux nombres par 100. "
        "Exemple : 6 ÷ 0,25 devient 600 ÷ 25 = 24. "
        "Attention : on ne peut jamais diviser par zéro."
    ),
    'priorites': (
        "D’abord les parenthèses. Puis les multiplications et les divisions, "
        "qui ont la même priorité : on les effectue de gauche à droite. "
        "Enfin les additions et les soustractions, elles aussi de gauche à droite."
    ),
    'distributivite': (
        "On multiplie le nombre placé devant la parenthèse par CHACUN des nombres "
        "à l’intérieur. Exemple : 3 × (4 + 2) = 3 × 4 + 3 × 2 = 18."
    ),
}

ERREURS_ILLUSTREES = {
    'decimaux': (
        "Pour 0,4 × 0,5, calcule 4 × 5 = 20. Il y a deux chiffres "
        "après la virgule au total : le résultat est 0,20 = 0,2, et non 20."
    ),
    'euclidienne': (
        "53 ÷ 6 donne un quotient de 8 et un reste de 5, car 53 = 6 × 8 + 5. "
        "On n’écrit pas « 53 ÷ 6 = 8 + 5 »."
    ),
    'division_decimale': (
        "Pour 1,2 ÷ 0,3, il faut multiplier les deux nombres par 10 : "
        "12 ÷ 3 = 4. Multiplier seulement 0,3 par 10 donnerait un résultat faux."
    ),
    'priorites': (
        "24 ÷ 3 × 2 se calcule de gauche à droite : "
        "24 ÷ 3 = 8, puis 8 × 2 = 16. "
        "Si on fait 3 × 2 en premier, on trouve 4 : c’est faux."
    ),
    'distributivite': (
        "2 × (5 + 3) = 2 × 5 + 2 × 3 = 16. "
        "Écrire 2 × 5 + 3 = 13 oublie de multiplier le 3."
    ),
}

# Le cours garde des écritures accessibles avant d'introduire les lettres.
for _lesson in LESSONS:
    if _lesson['id'] == 'euclidienne':
        _lesson['methode'] = [
            "Repère le dividende (nombre à partager) et le diviseur (taille de chaque groupe).",
            "Cherche combien de groupes complets tu peux former : c'est le quotient.",
            "Calcule ce qui reste après les groupes complets : c'est le reste.",
            "Vérifie avec la multiplication et l'addition.",
            "Le reste doit toujours être plus petit que le diviseur.",
        ]
    elif _lesson['id'] == 'division_decimale':
        _lesson['retenir'] = r"8{,}4\div0{,}7 = 84\div7 = 12"

QUESTION_BANK = {'decimaux': [{'id': 'd01', 'question': '12,4 + 3,75 = ?', 'options': ['15,79', '16,15', '15,115', '16,79'], 'answer': 1, 'explain': '12,40 + 3,75 = 16,15.', 'level': 1}, {'id': 'd02', 'question': '8,5 − 2,75 = ?', 'options': ['6,25', '5,75', '5,85', '6,75'], 'answer': 1, 'explain': '8,50 − 2,75 = 5,75.', 'level': 1}, {'id': 'd03', 'question': '2,4 × 1,5 = ?', 'options': ['3,6', '36', '2,9', '0,36'], 'answer': 0, 'explain': '24 × 15 = 360 ; avec deux chiffres décimaux, 3,60.', 'level': 1}, {'id': 'd04', 'question': '0,7 × 0,6 = ?', 'options': ['4,2', '0,42', '0,042', '1,3'], 'answer': 1, 'explain': '7 × 6 = 42 et deux chiffres décimaux : 0,42.', 'level': 1}, {'id': 'd05', 'question': '18,2 + 0,08 = ?', 'options': ['18,10', '18,28', '18,208', '18,82'], 'answer': 1, 'explain': '18,20 + 0,08 = 18,28.', 'level': 1}, {'id': 'd06', 'question': '15 − 4,65 = ?', 'options': ['11,65', '10,45', '10,35', '11,35'], 'answer': 2, 'explain': '15,00 − 4,65 = 10,35.', 'level': 1}, {'id': 'd07', 'question': '3,25 × 2 = ?', 'options': ['6,5', '6,05', '3,50', '65'], 'answer': 0, 'explain': 'Deux fois 3,25 donne 6,50.', 'level': 1}, {'id': 'd08', 'question': '0,4 + 0,06 = ?', 'options': ['0,10', '0,46', '0,406', '4,6'], 'answer': 1, 'explain': '0,40 + 0,06 = 0,46.', 'level': 1}, {'id': 'd09', 'question': '5,6 × 0,1 = ?', 'options': ['56', '5,06', '0,56', '0,056'], 'answer': 2, 'explain': 'Multiplier par 0,1 revient à diviser par 10.', 'level': 1}, {'id': 'd10', 'question': 'Un livre coûte 7,80 € et un stylo 1,35 €. Total ?', 'options': ['8,15 €', '8,95 €', '9,15 €', '9,25 €'], 'answer': 2, 'explain': '7,80 + 1,35 = 9,15 €.', 'level': 1}, {'id': 'd11', 'question': '12,04 − 1,9 = ?', 'options': ['11,14', '10,14', '10,24', '11,04'], 'answer': 1, 'explain': '12,04 − 1,90 = 10,14.', 'level': 1}, {'id': 'd12', 'question': '1,2 × 0,5 = ?', 'options': ['6', '0,6', '0,06', '1,7'], 'answer': 1, 'explain': '12 × 5 = 60 ; deux chiffres décimaux donnent 0,60.', 'level': 1}], 'euclidienne': [{'id': 'e01', 'question': '77 partagé en groupes de 9 : quotient et reste ?', 'options': ['8 et 5', '9 et 4', '7 et 8', '8 et 7'], 'answer': 0, 'explain': '77 = 9 × 8 + 5 et 5 est inférieur à 9.', 'level': 1}, {'id': 'e02', 'question': '53 ÷ 6 : quel reste ?', 'options': ['3', '4', '5', '6'], 'answer': 2, 'explain': '53 = 6 × 8 + 5.', 'level': 1}, {'id': 'e03', 'question': 'Dans une division euclidienne par 7, quel reste est impossible ?', 'options': ['0', '3', '6', '7'], 'answer': 3, 'explain': 'Le reste doit être strictement inférieur au diviseur, ici 7.', 'level': 1}, {'id': 'e04', 'question': 'Quel nombre est divisible par 9 ?', 'options': ['235', '243', '245', '248'], 'answer': 1, 'explain': '2 + 4 + 3 = 9, multiple de 9.', 'level': 1}, {'id': 'e05', 'question': 'Quel nombre est divisible par 3 mais PAS par 9 ?', 'options': ['135', '123', '117', '171'], 'answer': 1, 'explain': '1 + 2 + 3 = 6, divisible par 3 mais pas par 9.', 'level': 1}, {'id': 'e06', 'question': 'Lequel est un diviseur de 42 ?', 'options': ['5', '6', '8', '10'], 'answer': 1, 'explain': '42 = 6 × 7.', 'level': 1}, {'id': 'e07', 'question': 'Le nombre 48 est un multiple de…', 'options': ['5', '6', '7', '9'], 'answer': 1, 'explain': '48 = 6 × 8.', 'level': 1}, {'id': 'e08', 'question': '65 = 8 × 8 + 1. Quel est le quotient de 65 ÷ 8 ?', 'options': ['1', '7', '8', '9'], 'answer': 2, 'explain': '65 ÷ 8 : quotient 8, reste 1.', 'level': 1}, {'id': 'e09', 'question': 'Une division euclidienne est exacte quand…', 'options': ['le reste vaut 0', 'le quotient vaut 0', 'le diviseur vaut 1', 'le reste dépasse le diviseur'], 'answer': 0, 'explain': 'Une division exacte laisse un reste nul.', 'level': 1}, {'id': 'e10', 'question': 'Combien de sachets COMPLETS de 6 billes avec 38 billes ?', 'options': ['5', '6', '7', '8'], 'answer': 1, 'explain': '38 = 6 × 6 + 2 : 6 sachets complets.', 'level': 1}, {'id': 'e11', 'question': 'Quel est le reste de 100 ÷ 9 ?', 'options': ['0', '1', '2', '9'], 'answer': 1, 'explain': '100 = 9 × 11 + 1.', 'level': 1}, {'id': 'e12', 'question': 'Quel critère montre que 378 est divisible par 9 ?', 'options': ['Son dernier chiffre est pair', '3 + 7 + 8 = 18', 'Il finit par 8', 'Il est supérieur à 100'], 'answer': 1, 'explain': '3 + 7 + 8 = 18, multiple de 9.', 'level': 1}], 'division_decimale': [{'id': 'v01', 'question': '8,4 ÷ 0,7 = ?', 'options': ['1,2', '12', '0,12', '120'], 'answer': 1, 'explain': '8,4 ÷ 0,7 = 84 ÷ 7 = 12.', 'level': 1}, {'id': 'v02', 'question': '6,3 ÷ 0,9 = ?', 'options': ['0,7', '7', '70', '5,4'], 'answer': 1, 'explain': '63 ÷ 9 = 7.', 'level': 1}, {'id': 'v03', 'question': '1,26 ÷ 0,3 = ?', 'options': ['0,42', '42', '4,2', '3,6'], 'answer': 2, 'explain': '12,6 ÷ 3 = 4,2.', 'level': 1}, {'id': 'v04', 'question': '9,1 ÷ 2,8 = ?', 'options': ['32,5', '3,25', '2,8', '0,325'], 'answer': 1, 'explain': '91 ÷ 28 = 3,25.', 'level': 1}, {'id': 'v05', 'question': 'Pour transformer 5,6 ÷ 0,4, on écrit…', 'options': ['56 ÷ 4', '5,6 ÷ 4', '56 ÷ 0,4', '0,56 ÷ 4'], 'answer': 0, 'explain': 'Multiplier le dividende ET le diviseur par 10.', 'level': 1}, {'id': 'v06', 'question': '4,5 ÷ 0,5 = ?', 'options': ['0,9', '9', '90', '4'], 'answer': 1, 'explain': '45 ÷ 5 = 9.', 'level': 1}, {'id': 'v07', 'question': '1,2 ÷ 0,03 = ?', 'options': ['0,4', '4', '40', '400'], 'answer': 2, 'explain': 'Multiplier les deux nombres par 100 : 120 ÷ 3 = 40.', 'level': 1}, {'id': 'v08', 'question': 'Quelle égalité est vraie ?', 'options': ['2,4 ÷ 0,6 = 24 ÷ 6', '2,4 ÷ 0,6 = 2,4 ÷ 6', '2,4 ÷ 0,6 = 24 ÷ 0,6', '2,4 ÷ 0,6 = 0,24 ÷ 6'], 'answer': 0, 'explain': 'On déplace les deux virgules de la même façon.', 'level': 1}, {'id': 'v09', 'question': '3,6 ÷ 1,2 = ?', 'options': ['0,3', '3', '30', '4,8'], 'answer': 1, 'explain': '36 ÷ 12 = 3.', 'level': 1}, {'id': 'v10', 'question': '0,84 ÷ 0,07 = ?', 'options': ['1,2', '0,12', '12', '120'], 'answer': 2, 'explain': '84 ÷ 7 = 12.', 'level': 1}, {'id': 'v11', 'question': 'Pour vérifier 2,5 ÷ 0,5 = 5, on calcule…', 'options': ['5 + 0,5', '5 × 0,5', '2,5 × 0,5', '5 − 0,5'], 'answer': 1, 'explain': '5 × 0,5 = 2,5.', 'level': 1}, {'id': 'v12', 'question': 'Un ruban de 3,6 m est découpé en morceaux de 0,9 m. Nombre de morceaux ?', 'options': ['3', '4', '5', '9'], 'answer': 1, 'explain': '3,6 ÷ 0,9 = 36 ÷ 9 = 4.', 'level': 1}], 'priorites': [{'id': 'p01', 'question': '18 − 3 × 4 = ?', 'options': ['60', '6', '15', '24'], 'answer': 1, 'explain': '3 × 4 = 12, puis 18 − 12 = 6.', 'level': 1}, {'id': 'p02', 'question': '(18 − 3) × 4 = ?', 'options': ['6', '15', '60', '72'], 'answer': 2, 'explain': 'Parenthèses : 18 − 3 = 15, puis × 4.', 'level': 1}, {'id': 'p03', 'question': '4 + 3 × 5 = ?', 'options': ['35', '19', '23', '20'], 'answer': 1, 'explain': '3 × 5 = 15, puis 4 + 15 = 19.', 'level': 1}, {'id': 'p04', 'question': '24 ÷ 3 × 2 = ?', 'options': ['4', '16', '12', '2'], 'answer': 1, 'explain': 'Division et multiplication ont même priorité : de gauche à droite.', 'level': 1}, {'id': 'p05', 'question': '20 − (6 + 4) = ?', 'options': ['10', '18', '22', '30'], 'answer': 0, 'explain': '6 + 4 = 10, puis 20 − 10 = 10.', 'level': 1}, {'id': 'p06', 'question': '7 + 12 ÷ 3 = ?', 'options': ['19', '11', '6', '7'], 'answer': 1, 'explain': '12 ÷ 3 = 4, puis 7 + 4 = 11.', 'level': 1}, {'id': 'p07', 'question': '5 × (3 + 2) = ?', 'options': ['17', '25', '20', '15'], 'answer': 1, 'explain': 'La parenthèse vaut 5, donc 5 × 5 = 25.', 'level': 1}, {'id': 'p08', 'question': '30 ÷ 5 + 2 × 4 = ?', 'options': ['32', '14', '8', '24'], 'answer': 1, 'explain': '6 + 8 = 14.', 'level': 1}, {'id': 'p09', 'question': '9 − 8 ÷ 2 + 1 = ?', 'options': ['2', '6', '7', '1'], 'answer': 1, 'explain': '9 − 4 + 1 = 6.', 'level': 1}, {'id': 'p10', 'question': 'Quelle expression vaut 21 ?', 'options': ['3 × (5 + 2)', '3 × 5 + 2', '(3 + 5) × 2', '3 + 5 × 2'], 'answer': 0, 'explain': '3 × 7 = 21.', 'level': 1}, {'id': 'p11', 'question': '(12 + 8) ÷ 4 = ?', 'options': ['6', '5', '8', '20'], 'answer': 1, 'explain': '20 ÷ 4 = 5.', 'level': 1}, {'id': 'p12', 'question': '36 ÷ (3 × 4) = ?', 'options': ['48', '12', '3', '9'], 'answer': 2, 'explain': '3 × 4 = 12, puis 36 ÷ 12 = 3.', 'level': 1}], 'distributivite': [{'id': 't01', 'question': '3 × (4 + 2) = ?', 'options': ['3 × 4 + 2', '3 × 4 + 3 × 2', '3 + 4 × 2', '3 × 6 + 2'], 'answer': 1, 'explain': 'Distribuer 3 sur les deux termes : 12 + 6 = 18.', 'level': 1}, {'id': 't02', 'question': '5 × (12 − 2) = ?', 'options': ['5 × 12 − 5 × 2', '5 × 12 − 2', '5 × 10 − 2', '12 × 2 − 5'], 'answer': 0, 'explain': '5 × 12 − 5 × 2 = 60 − 10 = 50.', 'level': 1}, {'id': 't03', 'question': '4 × (6 + 3) = ?', 'options': ['30', '36', '24', '45'], 'answer': 1, 'explain': '4 × 6 + 4 × 3 = 24 + 12 = 36.', 'level': 1}, {'id': 't04', 'question': '7 × 19 = ?', 'options': ['7 × (20 − 1)', '7 × (20 + 1)', '7 + 20 − 1', '20 × (7 + 1)'], 'answer': 0, 'explain': '19 = 20 − 1, donc 140 − 7 = 133.', 'level': 1}, {'id': 't05', 'question': 'Quelle expression est égale à 2 × 5 + 2 × 3 ?', 'options': ['2 × (5 × 3)', '2 × (5 + 3)', '(2 + 5) × 3', '2 + 5 + 3'], 'answer': 1, 'explain': '2 est un facteur commun : 2 × (5 + 3).', 'level': 1}, {'id': 't06', 'question': '6 × (10 + 4) = ?', 'options': ['64', '84', '68', '140'], 'answer': 1, 'explain': '60 + 24 = 84.', 'level': 1}, {'id': 't07', 'question': '8 × 99 = ?', 'options': ['8 × (100 + 1)', '8 × (100 − 1)', '8 × 9 × 9', '800 + 8'], 'answer': 1, 'explain': '800 − 8 = 792.', 'level': 1}, {'id': 't08', 'question': '3 × (7 − 2) = ?', 'options': ['3 × 7 − 2', '3 × 7 − 3 × 2', '3 × 7 + 3 × 2', '3 × (7 + 2)'], 'answer': 1, 'explain': '21 − 6 = 15.', 'level': 1}, {'id': 't09', 'question': '2,5 × (8 + 2) = ?', 'options': ['20', '25', '10', '250'], 'answer': 1, 'explain': '2,5 × 8 + 2,5 × 2 = 20 + 5 = 25.', 'level': 1}, {'id': 't10', 'question': 'Quel est le facteur commun dans 9 × 4 + 9 × 6 ?', 'options': ['4', '6', '9', '10'], 'answer': 2, 'explain': 'Les deux termes contiennent le facteur 9.', 'level': 1}, {'id': 't11', 'question': '15 × 12 − 15 × 2 = ?', 'options': ['15 × 10', '15 × 14', '13 × 10', '15 × 12 × 2'], 'answer': 0, 'explain': '15 × (12 − 2) = 15 × 10 = 150.', 'level': 1}, {'id': 't12', 'question': 'Le développement correct de 2 × (a + b) est…', 'options': ['2a + b', '2a + 2b', 'a + 2b', '2ab'], 'answer': 1, 'explain': 'On multiplie a ET b par 2.', 'level': 1}]}
from mathicap_qcm_banque_plus import enrichir_banque
enrichir_banque(QUESTION_BANK)

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
    /* Les commandes QCM sont stylisées une seule fois dans app.py. */
    @media (prefers-reduced-motion: reduce) { .mc-lecon-entete::before {animation:none !important} }
    @media (prefers-reduced-motion: no-preference) {
      .mc-lecon-entete {animation:mc-lesson-show .32s ease-out both}
      @keyframes mc-lesson-show {from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
    }
    @media(max-width:640px) {
       .mc-lecon-entete,.mc-lesson-block,.mc-quiz-box {padding:15px 13px;border-radius:15px}
       .mc-lecon-entete {margin-top:0}
    }
    /* En-têtes et menus : lecture renforcée, sans étirer sur grand écran */
    .mc-chapter-heading {max-width:900px;margin:12px 0 16px;
       padding:14px 18px;background:linear-gradient(100deg,#e3f0ff,#fff1d8);
       border-left:6px solid #2d7be8;border-radius:14px;color:#153763}
    .mc-chapter-heading .mc-chapter-name {display:block;font-size:clamp(1.15rem,3vw,1.5rem);font-weight:850}
    .mc-chapter-heading .mc-chapter-detail {display:block;margin-top:5px;font-size:.96rem;font-weight:650;color:#385778}
    .st-key-mc_choix_notion_cours, .st-key-mc_choix_notion_qcm {
       max-width:870px;padding:11px 15px 13px;background:#edf5ff;
       border:2px solid #7babee;border-radius:14px;margin:12px 0 18px}
    .st-key-mc_choix_notion_cours [data-testid="stWidgetLabel"] p,
    .st-key-mc_choix_notion_qcm [data-testid="stWidgetLabel"] p,
    .st-key-mc_choix_notion_cours label p,
    .st-key-mc_choix_notion_qcm label p {
       font-size:1.07rem!important;font-weight:800!important;color:#123b70!important}
    .st-key-mc_choix_notion_cours [data-baseweb="select"],
    .st-key-mc_choix_notion_qcm [data-baseweb="select"] {
       border-radius:10px;box-shadow:0 0 0 1px #a2c4ef55}
    .mc-remember {max-width:880px;padding:15px 18px;margin:10px 0 20px;
       background:#eaf7ed;border-left:5px solid #29a26b;color:#184d39;
       border-radius:13px;line-height:1.6;font-size:1.02rem;font-weight:700}
    .mc-operation-grid {max-width:880px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:13px;margin:14px 0}
    .mc-op-card {padding:14px;border:1px solid #cfdef4;background:#f4f8ff;
       border-radius:15px;box-shadow:0 3px 14px #16366a0d}
    .mc-op-card h4 {font-size:1.04rem;color:#163b72;margin:0 0 7px}
    .mc-op-card p {margin:9px 0 0;color:#314d72;font-size:.94rem;line-height:1.5}
    .mc-digit-table {border-collapse:separate;border-spacing:4px;margin:5px auto 0;
       font-size:clamp(1rem,2.3vw,1.25rem);font-weight:750;font-variant-numeric:tabular-nums}
    .mc-digit-table th {font-size:.75rem;color:#45647c;font-weight:750}
    .mc-digit-table td {width:30px;height:35px;min-width:30px;text-align:center;
       border:1px solid #b3c9e4;background:white;border-radius:5px;color:#153767}
    .mc-digit-table .mc-comma {background:#fff1bc;color:#9c5600;font-weight:850}
    .mc-digit-table .mc-result td {background:#d6f2e5;border-color:#58b78d}
    .mc-digit-table .mc-separator td {border-top:2px solid #6086b8}
    .mc-div-layout {display:grid;grid-template-columns:1fr 1fr;max-width:300px;
       margin:12px auto;font-size:1.6rem;color:#173b6f;font-weight:800;text-align:center;
       font-variant-numeric:tabular-nums}
    .mc-div-layout .mc-div-left {border-right:3px solid #5978a6;padding:5px 14px}
    .mc-div-layout .mc-div-right {border-bottom:3px solid #5978a6;padding:5px 14px}
    .mc-div-layout .mc-div-quotient {padding:10px 14px;background:#e1f0ff;border-radius:0 0 8px 0}
    .mc-div-layout .mc-div-reste {padding:9px 14px;color:#a8530b;background:#fff0d4;border-radius:0 0 0 8px}
    .mc-legend {max-width:880px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:12px 0}
    .mc-legend span {padding:9px 12px;background:#f2f7fc;border-radius:10px;line-height:1.45}
    .mc-legend b {color:#13589d}
    .mc-everyday {max-width:880px;background:#fff4dc;padding:14px 17px;
       border-radius:14px;margin:12px 0 18px;color:#624314;line-height:1.6}
    .mc-step {max-width:880px;padding:10px 14px;border-radius:11px;
       margin:9px 0;background:#edf5ff;color:#153a64;font-size:1.05rem}
    .mc-step strong {color:#075fae}
    .mc-divisible {border-collapse:separate;border-spacing:0;max-width:880px;
       width:100%;font-size:.94rem;border:1px solid #b8d0e8;border-radius:11px;overflow:hidden}
    .mc-divisible th,.mc-divisible td {text-align:left;padding:9px 11px;border-bottom:1px solid #d6e4f1}
    .mc-divisible th {background:#ddecff;color:#174374}
    .mc-divisible tr:last-child td {border-bottom:none}
    @media(max-width:640px){
      .mc-op-card{padding:10px 9px}.mc-digit-table{border-spacing:3px}
      .mc-digit-table td{min-width:26px;width:26px;height:32px}
      .mc-remember{padding:12px 14px}
      .st-key-mc_choix_notion_cours,.st-key-mc_choix_notion_qcm{padding:9px 10px}
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


def _chapitre_entete(type_page):
    st.html(
        '<div class="mc-chapter-heading">'
        '<span class="mc-chapter-name">📘 5e · Chapitre 1 : Opérations</span>'
        f'<span class="mc-chapter-detail">{escape(type_page)} · 5 notions à explorer</span>'
        '</div>'
    )


def _tableau_chiffres(titre, entetes, lignes, explication):
    """Calcul posé par cases, avec virgules alignées et résultat en couleur."""
    html = '<article class="mc-op-card"><h4>' + escape(titre) + '</h4>'
    html += '<table class="mc-digit-table"><thead><tr>'
    html += ''.join('<th>'+escape(h)+'</th>' for h in entetes)
    html += '</tr></thead><tbody>'
    for i, ligne in enumerate(lignes):
        cls = 'mc-result mc-separator' if i == len(lignes)-1 else ''
        html += f'<tr class="{cls}">'
        for char in ligne:
            cls2 = 'mc-comma' if char == ',' else ''
            html += f'<td class="{cls2}">' + escape(str(char)) + '</td>'
        html += '</tr>'
    html += '</tbody></table><p>' + escape(explication) + '</p></article>'
    return html


def _vie_quotidienne(texte):
    st.html('<div class="mc-everyday">🌍 <b>Dans la vie quotidienne :</b> '
            + escape(texte) + '</div>')


def _explications_detaillees(notion):
    """Illustrations et vocabulaire originaux inspirés du chapitre du manuel."""
    st.markdown('#### 🧮 Je vois comment poser le calcul')
    if notion == 'decimaux':
        tables = [
            _tableau_chiffres('➕ Addition posée', ['', 'D', 'U', ',', 'd', 'c'],
                [['', '1', '2', ',', '4', '0'],
                 ['+', '0', '3', ',', '7', '5'],
                 ['=', '1', '6', ',', '1', '5']],
                'Les virgules sont sous les virgules. On additionne de droite à gauche.'),
            _tableau_chiffres('➖ Soustraction posée', ['', 'D', 'U', ',', 'd', 'c'],
                [['', '2', '0', ',', '0', '0'],
                 ['−', '0', '7', ',', '8', '6'],
                 ['=', '1', '2', ',', '1', '4']],
                'On écrit 20,00 pour pouvoir soustraire 7,86. On emprunte si nécessaire.'),
            _tableau_chiffres('✖️ Multiplication posée', ['', 'C', 'D', 'U'],
                [['', '', '2', '4'],
                 ['×', '', '1', '5'],
                 ['', '1', '2', '0'],
                 ['+', '2', '4', '0'],
                 ['=', '3', '6', '0']],
                'On calcule 24 × 15 = 360 sans virgule. Deux chiffres après les virgules au départ : 3,60.'),
        ]
        st.html('<div class="mc-operation-grid">' + ''.join(tables) + '</div>')
        st.markdown('**Le nom des colonnes :** D = dizaines, U = unités, d = dixièmes, c = centièmes. La virgule est toujours dans sa propre colonne.')
        st.markdown('**Addition, case par case :** centièmes : 0 + 5 = 5 ; dixièmes : 4 + 7 = 11. J’écris 1 et je retiens 1 pour les unités. Puis 2 + 3 + 1 = 6. Résultat : **16,15**.')
        st.markdown('**Soustraction, case par case :** dans 20,00 − 7,86, le chiffre du haut est parfois trop petit. J’emprunte alors à la colonne de gauche. Je trouve, de droite à gauche, 4 centièmes, 1 dixième, 2 unités et 1 dizaine : **12,14**.')
        st.markdown('**Multiplication, case par case :** 24 × 5 = 120, puis 24 × 10 = 240 ; 120 + 240 = 360. Pour 2,4 × 1,5, il y a deux chiffres après les virgules des facteurs réunis : j’écris **3,60**, soit **3,6**.')
        _vie_quotidienne('À la boulangerie, tu achètes un pain à 1,25 € et un gâteau à 2,80 €. Au total, tu paies 4,05 €. Si tu donnes 5 €, on te rend 0,95 €.')
    elif notion == 'euclidienne':
        st.markdown('**Je pose la division de 77 par 9**')
        st.html("""<div class="mc-div-layout" role="img" aria-label="Division euclidienne posée : 77 divisé par 9, quotient 8, reste 5">
             <div class="mc-div-left">77<br><span style="color:#bd6a24">−72</span></div>
             <div class="mc-div-right">9</div>
             <div class="mc-div-reste">5</div><div class="mc-div-quotient">8</div></div>
             <div class="mc-legend"><span><b>77</b> : dividende, le nombre à partager</span>
             <span><b>9</b> : diviseur, la taille d’un groupe</span>
             <span><b>8</b> : quotient, le nombre de groupes</span>
             <span><b>5</b> : reste, ce qu’il reste</span></div>""")
        st.markdown('**Étape 1.** Je cherche dans la table de 9 : 9 × 8 = 72. Mais 9 × 9 = 81, c’est trop grand.')
        st.markdown('**Étape 2.** Je retire 72 à 77 : il reste 5.')
        st.markdown('**Étape 3.** Je vérifie : **77 = 9 × 8 + 5**. Le reste 5 est bien plus petit que 9.')
        st.markdown('**Autre exemple du manuel :** 269 ÷ 7. On trouve 38 groupes de 7 et il reste 3, car 7 × 38 = 266 puis 269 − 266 = 3.')
        _vie_quotidienne('Dans une sortie scolaire, 49 élèves doivent former des équipes de 6. On forme 8 équipes complètes et un élève reste à placer, car 49 = 6 × 8 + 1.')
        st.markdown('#### 🔎 Reconnaître facilement les nombres divisibles')
        st.markdown('Un nombre est **divisible** par un autre lorsque la division tombe juste : il ne reste rien.')
        st.html("""<table class="mc-divisible"><thead><tr><th>Divisible par…</th><th>Comment le reconnaître ?</th><th>Exemple</th></tr></thead><tbody>
          <tr><td><b>2</b></td><td>Le dernier chiffre est 0, 2, 4, 6 ou 8.</td><td>246</td></tr>
          <tr><td><b>5</b></td><td>Le dernier chiffre est 0 ou 5.</td><td>135</td></tr>
          <tr><td><b>10</b></td><td>Le dernier chiffre est 0.</td><td>190</td></tr>
          <tr><td><b>3</b></td><td>La somme des chiffres est divisible par 3.</td><td>123 : 1 + 2 + 3 = 6</td></tr>
          <tr><td><b>9</b></td><td>La somme des chiffres est divisible par 9.</td><td>234 : 2 + 3 + 4 = 9</td></tr>
          </tbody></table>""")
        st.markdown('**Multiple et diviseur :** comme 6 × 7 = 42, **42 est un multiple de 6** et **6 est un diviseur de 42**.')
    elif notion == 'division_decimale':
        st.markdown('**Exemple : 8,4 litres de jus à répartir dans des bouteilles de 0,7 litre.**')
        for n,txt in [('1', 'Je pars de 8,4 ÷ 0,7. Le dividende 8,4 ET le diviseur 0,7 ont une virgule. Je veux rendre le diviseur entier.'),
                      ('2', 'Je multiplie les deux nombres par 10 : 8,4 devient 84 et 0,7 devient 7. La division devient 84 ÷ 7.'),
                      ('3', 'Je calcule 84 ÷ 7 = 12. Le quotient ne change pas : je peux remplir 12 bouteilles.'),
                      ('4', 'Je vérifie : 12 × 0,7 = 8,4.')]:
            st.html(f'<div class="mc-step"><strong>Étape {n}.</strong> {escape(txt)}</div>')
        st.markdown('**Pourquoi est-ce autorisé ?** Multiplier le dividende et le diviseur par le même nombre ne change pas le quotient. En revanche, il serait faux de multiplier seulement le diviseur.')
        st.markdown('**Deuxième exemple : 1,26 ÷ 0,3 = 12,6 ÷ 3 = 4,2.**')
        st.markdown('Si le diviseur est **0,25**, je multiplie les deux nombres par **100** pour obtenir un diviseur entier de **25**.')
        _vie_quotidienne('Un ruban mesure 3,6 mètres. Tu coupes des morceaux de 0,9 mètre : 3,6 ÷ 0,9 = 36 ÷ 9 = 4 morceaux.')
    elif notion == 'priorites':
        st.markdown('**Deux calculs presque identiques peuvent donner des résultats différents.**')
        for n,txt in [('1', '18 − 3 × 4 : je fais d’abord 3 × 4 = 12.'),
                      ('2', 'Je calcule ensuite 18 − 12 = 6.'),
                      ('3', '(18 − 3) × 4 : les parenthèses passent d’abord. 18 − 3 = 15.'),
                      ('4', 'Je calcule ensuite 15 × 4 = 60.')]:
            st.html(f'<div class="mc-step"><strong>Étape {n}.</strong> {escape(txt)}</div>')
        st.markdown('**Attention :** multiplication et division ont la même priorité. Si elles se suivent, calcule de gauche à droite. Exemple : 24 ÷ 3 × 2 = 8 × 2 = 16.')
        _vie_quotidienne('Au musée, deux entrées coûtent 8 € chacune et tu achètes une boisson à 3 €. Tu paies 2 × 8 + 3 = 19 €, sans additionner 8 et 3 avant de multiplier.')
    elif notion == 'distributivite':
        st.markdown('**Un grand rectangle peut être découpé en deux petits rectangles.**')
        for n,txt in [('1', 'Le rectangle mesure 3 cm de haut et 4 + 2 = 6 cm de long.'),
                      ('2', 'Aire du grand rectangle : 3 × 6 = 18 cm².'),
                      ('3', 'Aire des deux parties : 3 × 4 = 12 cm² et 3 × 2 = 6 cm².'),
                      ('4', 'On retrouve 12 + 6 = 18 cm² : 3 × (4 + 2) = 3 × 4 + 3 × 2.')]:
            st.html(f'<div class="mc-step"><strong>Étape {n}.</strong> {escape(txt)}</div>')
        st.markdown('**Avec une soustraction :** 5 × (12 − 2) = 5 × 12 − 5 × 2 = 60 − 10 = 50.')
        st.markdown('**Et si tu vois des lettres ?** Elles servent simplement à désigner des nombres. Par exemple, 3 × (a + 2) signifie : trois fois le nombre a, puis trois fois 2.')
        _vie_quotidienne('Au cinéma, 3 amis prennent chacun un billet de 8 € et une boisson de 2 €. On calcule 3 × (8 + 2) = 3 × 8 + 3 × 2 = 30 €.')


def _illustrer_notion(notion):
    gauche, droite = FIGURES[notion]
    st.html(
        '<div class="mc-equation-demo" role="img" aria-label="Étape de calcul : '
        + gauche + ' donne ' + droite + '">'
        + '<span class="mc-equation-part">' + gauche + '</span>'
        + '<span class="mc-arrow" aria-hidden="true">→</span>'
        + '<span class="mc-equation-part">' + droite + '</span></div>'
    )


def _aller_du_cours_au_qcm(notion, aller_vers):
    """Préparer la navigation avant l'instanciation du menu Streamlit."""
    st.session_state['mathicap_qcm_notion'] = notion
    st.session_state.pop('mathicap_qcm_partie', None)
    if aller_vers:
        aller_vers('QCM')
    else:
        st.session_state['mathicap_page'] = 'QCM'


def _aller_du_qcm_au_cours(notion, aller_vers):
    """Même correction pour le bouton « Revoir le cours »."""
    if notion in COURSE_IDS:
        st.session_state['mathicap_cours_notion'] = notion
    if aller_vers:
        aller_vers('Cours')
    else:
        st.session_state['mathicap_page'] = 'Cours'


def afficher_cours(aller_vers=None):
    _style()
    st.subheader('Cours & points à retenir')
    _chapitre_entete('Cours expliqués pas à pas')
    with st.container(key='mc_choix_notion_cours'):
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
    _explications_detaillees(notion)
    with st.container(key='mc_exemples'):
        st.markdown('#### 🔎 Autres exemples guidés')
        for titre,formule,explication in l['exemples']:
            with st.expander('▸ '+titre,expanded=False):
                st.latex(formule)
                st.caption(explication)
    st.markdown('#### 📌 À retenir')
    note_html = '<br><br>'.join(escape(part) for part in NOTES_SIMPLES[notion].split('\n'))
    st.html('<div class="mc-remember">' + note_html + '</div>')
    st.markdown('#### ⚠️ Erreur à éviter')
    st.warning(l['erreur'], width=850)
    st.markdown('**Exemple pour comprendre :** ' + ERREURS_ILLUSTREES[notion])
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
    st.button(
        '✅ Passer au QCM de cette notion', key='mc_cours_vers_qcm',
        on_click=_aller_du_cours_au_qcm, args=(notion, aller_vers),
    )


def _tirer_questions(notion):
    """10 questions différentes, priorité aux questions non vues récemment."""
    hasard = random.SystemRandom()
    deja = set(st.session_state.get('mc_qcm_questions_deja_vues', set()))
    try:
        from mathicap_qcm_resultats import questions_deja_vues
        deja.update(questions_deja_vues(12))
    except Exception:
        pass  # Un incident de stockage ne doit pas bloquer un QCM.

    def choisir(nom, quantite):
        pool = QUESTION_BANK[nom]
        nouvelles = [q for q in pool if q['id'] not in deja]
        selection = hasard.sample(nouvelles, min(quantite, len(nouvelles)))
        if len(selection) < quantite:
            deja_choisies = {q['id'] for q in selection}
            autres = [q for q in pool if q['id'] not in deja_choisies]
            selection += hasard.sample(autres, quantite - len(selection))
        return selection

    if notion == ALL_KEY:
        questions = []
        for identifiant in COURSE_IDS:
            questions.extend(choisir(identifiant, 2))
        hasard.shuffle(questions)
    else:
        questions = choisir(notion, 10)

    resultat = []
    for question in questions:
        ordre = list(range(len(question['options'])))
        hasard.shuffle(ordre)
        copie = dict(question)
        copie['options'] = [question['options'][j] for j in ordre]
        copie['answer'] = ordre.index(question['answer'])
        resultat.append(copie)

    deja.update(q['id'] for q in resultat)
    st.session_state['mc_qcm_questions_deja_vues'] = deja
    return resultat

def _demarrer(notion):
    """Lance 10 questions sans afficher leur correction pendant le QCM."""
    st.session_state['mathicap_qcm_partie'] = {
        'id': uuid4().hex[:10],
        'notion': notion,
        'questions': _tirer_questions(notion),
        'index': 0,
        'reponses': {},
        'terminee': False,
        'revoir': False,
        'sauvegarde_tentee': False,
        'sauvegarde_confirmee': False,
    }
    _sauvegarder_partie_en_cours()


def _demarrer_depuis_bouton(notion):
    """Callback : une seule réexécution Streamlit après le clic."""
    _demarrer(notion)


def _sauvegarder_partie_en_cours():
    partie = st.session_state.get('mathicap_qcm_partie')
    if not partie or partie.get('terminee'):
        return
    try:
        from mathicap_qcm_resultats import enregistrer_partie
        ok, message = enregistrer_partie(partie)
        st.session_state['mc_qcm_etat_sauvegarde'] = (ok, message)
    except Exception:
        st.session_state['mc_qcm_etat_sauvegarde'] = (
            False, 'Enregistrement temporairement indisponible.'
        )


def _ouvrir_serie_qcm(partie_id):
    """Callback : recharge la série avant la création du sélecteur de notion."""
    from mathicap_qcm_resultats import charger_partie
    partie, message = charger_partie(partie_id)
    if not partie:
        st.session_state['mc_qcm_erreur_ouverture'] = message
        return
    st.session_state['mathicap_qcm_notion'] = partie['notion']
    st.session_state['mathicap_qcm_partie'] = partie
    st.session_state.pop('mc_qcm_erreur_ouverture', None)


def _memoriser_choix_qcm(ident, indice):
    """Mémorise le choix à chaque clic, même avant Changer de question."""
    partie = st.session_state.get('mathicap_qcm_partie')
    if not partie or partie.get('id') != ident or partie.get('terminee'):
        return
    questions = partie.get('questions', [])
    if not (0 <= indice < len(questions)):
        return
    cle = f'mc_qcm_radio_{ident}_{indice}'
    valeur = st.session_state.get(cle)
    options = questions[indice]['options']
    if valeur in options:
        nouvelle = options.index(valeur)
        if partie['reponses'].get(questions[indice]['id']) != nouvelle:
            partie['reponses'][questions[indice]['id']] = nouvelle
            _sauvegarder_partie_en_cours()


def _changer_question_qcm(ident, direction):
    """Navigation en callback : évite un rerun explicite supplémentaire."""
    partie = st.session_state.get('mathicap_qcm_partie')
    if not partie or partie.get('id') != ident or partie.get('terminee'):
        return
    questions = partie.get('questions', [])
    i = partie.get('index', 0)
    if not isinstance(i, int) or not (0 <= i < len(questions)):
        return
    if direction == -1:
        if i > 0:
            partie['index'] = i - 1
            _sauvegarder_partie_en_cours()
        return
    if direction != 1:
        return
    _memoriser_choix_qcm(ident, i)
    if i == len(questions) - 1:
        if _qcm_complet(partie):
            partie['terminee'] = True
            partie['index'] = len(questions)
            partie['sauvegarde_tentee'] = False
        else:
            st.session_state['mc_qcm_avertissement'] = (
                'Réponds aux dix questions avant de terminer.'
            )
    else:
        partie['index'] = i + 1
        _sauvegarder_partie_en_cours()


def _qcm_complet(partie):
    return (len(partie.get('questions', [])) == 10
            and all(q['id'] in partie.get('reponses', {})
                    for q in partie.get('questions', [])))


def _score_qcm(partie):
    return sum(partie.get('reponses', {}).get(q['id']) == q['answer']
               for q in partie.get('questions', []))


@st.fragment
def _afficher_question_interactive():
    """Réaffiche seulement le questionnaire lors des clics (pas toute la page)."""
    partie = st.session_state.get('mathicap_qcm_partie')
    if not partie:
        st.rerun()
    questions = partie['questions']
    ident = partie['id']
    # À la fin, relancer l'application une fois pour afficher le bilan.
    if partie.get('terminee') or partie.get('index', 0) >= len(questions):
        st.rerun()
    i = partie['index']
    q = questions[i]
    st.progress(i / 10, text=f'Question {i + 1} sur 10')
    st.caption(f"Réponses renseignées : {len(partie.get('reponses', {}))} sur 10 — corrections à la fin")
    etat_sauvegarde = st.session_state.get('mc_qcm_etat_sauvegarde')
    if etat_sauvegarde and not etat_sauvegarde[0]:
        st.caption('⚠️ ' + etat_sauvegarde[1])
    # Diagnostic facultatif pour comparer la durée de sauvegarde sur l'app réelle.
    # Ajouter ?mesure_qcm=1 (ou &mesure_qcm=1 si URL avec paramètres).
    if st.query_params.get('mesure_qcm') == '1':
        mesure = st.session_state.get('mc_qcm_temps')
        if mesure:
            st.caption(
                "Mesure sauvegarde — vérification session : "
                f"{mesure['session_ms']} ms ; écriture/lecture QCM : "
                f"{mesure['base_ms']} ms ; total : {mesure['total_ms']} ms "
                f"({mesure['action']})."
            )
    st.html('<div class="mc-quiz-box"><div class="mc-kicker">QUESTION '
            + str(i + 1) + '/10</div><h2>' + escape(str(q['question']))
            + '</h2></div>')
    champ = f'mc_qcm_radio_{ident}_{i}'
    precedente = partie['reponses'].get(q['id'])
    index_precedent = precedente if isinstance(precedente, int) and 0 <= precedente < len(q['options']) else None
    choix = st.radio('Choisis une seule réponse', q['options'], index=index_precedent,
                     key=champ, on_change=_memoriser_choix_qcm, args=(ident, i))
    if choix in q['options']:
        partie['reponses'][q['id']] = q['options'].index(choix)
    avertissement = st.session_state.pop('mc_qcm_avertissement', None)
    if avertissement:
        st.warning(avertissement)
    gauche, droite = st.columns(2, gap='small')
    with gauche:
        if i > 0:
            st.button('← Question précédente', key='mc_qcm_precedente',
                      on_click=_changer_question_qcm, args=(ident, -1))
    with droite:
        dernier = i == len(questions) - 1
        libelle = '✅ Terminer mon QCM' if dernier else 'Question suivante →'
        st.button(libelle, key='mc_qcm_suivante', disabled=(choix is None),
                  on_click=_changer_question_qcm, args=(ident, 1))


def afficher_qcm(aller_vers=None):
    _style()
    st.subheader('QCM rapides')
    _chapitre_entete('QCM : 10 questions, une seule bonne réponse par question')
    with st.container(key='mc_choix_notion_qcm'):
        select = _notion_selector('mathicap_qcm_notion', allow_all=True)
    partie = st.session_state.get('mathicap_qcm_partie')
    erreur_ouverture = st.session_state.pop('mc_qcm_erreur_ouverture', None)
    if erreur_ouverture:
        st.warning(erreur_ouverture, width=850)

    # Seules les parties en cours sont sauvegardées avec leurs dix questions.
    # Les QCM terminés gardent leur score en base, pas leurs contenus.
    if not partie:
        from mathicap_qcm_resultats import charger_parties
        parties_sauvees, erreur_sauvees = charger_parties(20)
        if parties_sauvees:
            with st.container(key='mc_qcm_reprise_zone'):
                st.markdown('### 📚 Reprendre mon QCM en cours')
                with st.expander('Afficher les QCM à reprendre', expanded=True):
                    for p in parties_sauvees[:10]:
                        st.button('▶️ Reprendre — ' + str(p.get('notion_label','QCM'))
                                  + ' · ' + str(p.get('nombre_reponses', 0)) + '/10 réponses',
                                  key='mc_reprise_' + p['partie_id'],
                                  on_click=_ouvrir_serie_qcm, args=(p['partie_id'],))
        elif erreur_sauvees and st.session_state.get('eleve_id'):
            st.caption('Séries QCM indisponibles : ' + erreur_sauvees)

    if not partie:
        from mathicap_qcm_resultats import charger_resultats, LABELS
        lignes, _ = charger_resultats(1)
        if lignes:
            dernier = lignes[0]
            st.info('Dernier QCM terminé : '
                    + LABELS.get(dernier['notion'], dernier['notion'])
                    + ' — ' + str(dernier['bonnes']) + '/10. '
                    'Le détail des réponses reste consultable uniquement pendant la session du QCM.')

    if partie and partie['notion'] != select:
        st.info('Une partie est en cours dans une autre notion. Démarre un nouveau QCM pour changer.', width=850)
    with st.container(key='mc_qcm_demarrer_zone'):
        st.button('🎯 Démarrer un nouveau QCM', key='mc_qcm_demarrer',
                  type='primary', width='stretch',
                  on_click=_demarrer_depuis_bouton, args=(select,))
    if not partie:
        st.info('Choisis une notion et commence. Réponds aux 10 questions : ton score et les corrections seront affichés seulement à la fin.', width=850)
        st.button('📖 Revoir le cours', key='mc_qcm_vers_cours',
                  on_click=_aller_du_qcm_au_cours, args=(select, aller_vers))
        return

    questions = partie['questions']
    ident = partie['id']
    terminee = bool(partie.get('terminee') or partie.get('index', 0) >= len(questions))

    if terminee:
        if not _qcm_complet(partie):
            st.warning('Le QCM est incomplet. Reviens répondre aux questions restantes.')
            if st.button('← Revenir aux questions', key='mc_qcm_revenir_questions'):
                partie['terminee'] = False
                partie['index'] = next((j for j, q in enumerate(questions)
                                         if q['id'] not in partie['reponses']), 0)
                st.rerun()
            return

        bonnes = _score_qcm(partie)
        score = int(100 * bonnes / len(questions))
        st.markdown('### 🏅 Ton QCM est terminé !')
        st.metric('Ton score', f'{bonnes} / 10')
        st.progress(score / 100, text=f'{score} % de bonnes réponses')
        if bonnes >= 8:
            st.success('Très bon travail !', width=850)
        elif bonnes >= 5:
            st.info('Bon début ! Tu peux revoir tes réponses et progresser.', width=850)
        else:
            st.info('Continue à t’entraîner : relis le cours, puis réessaie.', width=850)

        # Ne confirmer l'enregistrement que si Supabase a renvoyé la ligne enregistrée.
        from mathicap_qcm_resultats import enregistrer_resultat, charger_resultats, LABELS
        if not partie.get('sauvegarde_confirmee') and not partie.get('sauvegarde_tentee'):
            partie['sauvegarde_tentee'] = True
            (partie['sauvegarde_confirmee'],
             partie['sauvegarde_message']) = enregistrer_resultat(partie)
        if partie.get('sauvegarde_confirmee'):
            # Une seule notification par partie ; pas de répétition lors des reruns.
            if not partie.get('_notification_score_affichee'):
                st.toast('Score enregistré dans ton compte MathiCap.', icon='✅', duration=3)
                partie['_notification_score_affichee'] = True
        else:
            st.warning(partie.get('sauvegarde_message',
                                  'Score affiché, mais enregistrement non confirmé.'), width=850)
            if st.session_state.get('eleve_id'):
                if st.button('Réessayer l’enregistrement', key='mc_qcm_retenter_sauvegarde'):
                    partie['sauvegarde_tentee'] = False
                    st.rerun()

        # Toujours accessible après la dixième question, y compris après sauvegarde.
        if st.button('🔎 Revoir mes réponses', key='mc_qcm_revoir'):
            partie['revoir'] = not partie.get('revoir', False)
            st.rerun()
        if partie.get('revoir', False):
            st.markdown('#### Correction de tes 10 questions')
            for no, q in enumerate(questions, 1):
                choisie = partie['reponses'].get(q['id'])
                juste = choisie == q['answer']
                st.markdown(f"**Question {no} — {'✅ Bonne réponse' if juste else '❌ À revoir'}**")
                st.write(q['question'])
                st.write('**Ta réponse :** ' + (q['options'][choisie] if isinstance(choisie, int) and 0 <= choisie < len(q['options']) else 'Aucune'))
                st.write('**Bonne réponse :** ' + q['options'][q['answer']])
                st.caption('Explication : ' + q['explain'])
                if no < len(questions):
                    st.divider()

        resultat_lignes, erreur_resultats = charger_resultats(5)
        if resultat_lignes:
            with st.expander('📈 Mes derniers scores QCM'):
                for ligne in resultat_lignes:
                    st.write(f"{LABELS.get(ligne['notion'], ligne['notion'])} : "
                             f"{ligne['bonnes']} / {ligne['total']}")
        elif erreur_resultats:
            st.caption(erreur_resultats)
        st.button('📖 Revoir le cours', key='mc_qcm_cours_apres',
                  on_click=_aller_du_qcm_au_cours,
                  args=(partie.get('notion', select), aller_vers))
        return

    _afficher_question_interactive()
