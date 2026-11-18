"""Banque vérifiée de problèmes — 5e, Opérations / Priorités opératoires.

Difficultés :
    1 = niveau 7 (Je résous des problèmes)
    2 = niveau 8
    3 = niveau 9

Les exercices sont écrits et conservés : aucune API d'IA n'est appelée.
Modèles actifs du chapitre : 26 au niveau 7 ; 25 aux niveaux 8 et 9.
"""

from copy import deepcopy
import random
import re
import math


BANQUE_PRIORITES = {
    1: [
        {
            "id": "P7-01",
            "titre": "La fête du collège",
            "enonce": """**La fête du collège**

Le club de théâtre du collège organise une fête. Il dispose déjà de **180 €** dans sa caisse.

Pour cette fête, il vend :
- 14 billets pour les élèves à 6 € chacun ;
- 9 billets pour les parents à 8 € chacun.

Il dépense ensuite :
- 65 € pour louer la salle ;
- 28 € pour acheter les décorations.

**Questions**

1. Combien d'argent le club a-t-il gagné grâce à la vente des billets ?
2. Quel est le montant total des dépenses ?
3. Combien reste-t-il dans la caisse du club après la fête ? Écris une expression numérique avec des parenthèses.""",
            "correction": """**1. Argent gagné grâce aux billets**

14 × 6 + 9 × 8 = 84 + 72 = **156 €**

**2. Dépenses totales**

65 + 28 = **93 €**

**3. Argent restant dans la caisse**

Le club possédait déjà 180 €. On ajoute les recettes, puis on retire les dépenses.

180 + 156 − 93 = **243 €**

**Expression complète :**

180 + (14 × 6 + 9 × 8) − (65 + 28) = **243 €**

**Réponse :** Il reste **243 €** dans la caisse du club.""",
            "reponse_attendue": None,
        },
        {
            "id": "P7-02",
            "titre": "Une collection de cartes",
            "enonce": """**Une collection de cartes**

Adam possède **120 cartes** à collectionner.

Il ouvre 3 paquets contenant chacun 8 nouvelles cartes.

Ensuite, il échange 2 lots de 7 cartes contre un lot de 18 cartes.

**Questions**

1. Combien de cartes possède-t-il après avoir ouvert les paquets ?
2. Combien de cartes donne-t-il et combien en reçoit-il lors de l'échange ?
3. Combien de cartes possède-t-il finalement ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Après ouverture des paquets**

120 + 3 × 8 = 120 + 24 = **144 cartes**

**2. Pendant l'échange**

Cartes données : 2 × 7 = **14 cartes**.

Cartes reçues : **18 cartes**.

**3. Nombre final de cartes**

144 − 14 + 18 = **148 cartes**

**Expression complète :**

120 + (3 × 8) − (2 × 7) + 18 = **148**

**Réponse :** Adam possède finalement **148 cartes**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P7-03",
            "titre": "Le tournoi de badminton",
            "enonce": """**Le tournoi de badminton**

Le club de badminton du collège possède **40 volants** dans sa réserve.

Pour organiser un tournoi, il achète :
- 3 tubes contenant chacun 12 volants ;
- 2 tubes contenant chacun 6 volants.

À la fin du tournoi, 25 volants sont trop abîmés pour être réutilisés.

**Questions**

1. Combien de volants le club a-t-il achetés ?
2. Combien de volants possède-t-il avant le tournoi ?
3. Combien de volants utilisables lui reste-t-il après le tournoi ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Volants achetés**

3 × 12 + 2 × 6 = 36 + 12 = **48 volants**

**2. Total avant le tournoi**

40 + 48 = **88 volants**

**3. Volants restants**

88 − 25 = **63 volants**

**Expression complète :**

40 + (3 × 12 + 2 × 6) − 25 = **63**

**Réponse :** Le club dispose encore de **63 volants utilisables**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P7-04",
            "titre": "Une aventure en jeu vidéo",
            "enonce": """**Une aventure en jeu vidéo**

Dans un jeu vidéo, Lina possède **150 pièces d'or**.

Elle gagne :
- 25 pièces d'or pour chacune des 3 quêtes terminées ;
- 15 pièces d'or pour chacun des 2 défis réussis.

Elle achète ensuite 4 potions à 18 pièces d'or chacune.

**Questions**

1. Combien de pièces d'or Lina a-t-elle gagnées ?
2. Combien a-t-elle dépensé pour les potions ?
3. Combien de pièces d'or lui reste-t-il ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Pièces d'or gagnées**

3 × 25 + 2 × 15 = 75 + 30 = **105 pièces**.

**2. Pièces d'or dépensées**

4 × 18 = **72 pièces**.

**3. Pièces d'or restantes**

150 + 105 − 72 = **183 pièces**.

**Expression complète :**

150 + (3 × 25 + 2 × 15) − (4 × 18) = **183**.

**Réponse :** Lina possède finalement **183 pièces d'or**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P7-05",
            "titre": "L'atelier de dessin",
            "enonce": """**L'atelier de dessin**

Le collège organise un atelier de dessin avec **4 tables de 6 élèves** chacune.

Le professeur prévoit :
- 3 feuilles de papier pour chaque élève ;
- 2 feuilles supplémentaires par table pour faire des essais.

Le professeur dispose de **100 feuilles** au départ.

**Questions**

1. Combien de feuilles faut-il pour une table de 6 élèves, en comptant les feuilles d'essai ?
2. Combien de feuilles faut-il pour les 4 tables ?
3. Combien de feuilles restera-t-il au professeur ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Feuilles nécessaires pour une table**

6 × 3 + 2 = 18 + 2 = **20 feuilles**.

**2. Feuilles nécessaires pour les 4 tables**

4 × 20 = **80 feuilles**.

**3. Feuilles restantes**

100 − 80 = **20 feuilles**.

**Expression complète :**

100 − 4 × (6 × 3 + 2) = **20**.

**Réponse :** Il reste **20 feuilles** au professeur.""",
            "reponse_attendue": None,
        },

    ],
    2: [
        {
            "id": "P8-01",
            "titre": "La fête des clubs du collège",
            "enonce": """**La fête des clubs du collège**

Quatre clubs du collège (échecs, dessin, théâtre et lecture) organisent ensemble une fête.

Ils disposent au départ d'une caisse commune de **150 €**.

Pendant la fête, ils vendent :
- 16 billets pour les élèves à 7 € chacun ;
- 12 billets pour les parents à 9 € chacun.

Pour organiser la fête, ils dépensent :
- 85 € pour louer une salle ;
- 5 jeux de cartes à 9 € chacun, destinés aux gagnants des jeux organisés pendant la fête.

À la fin, les quatre clubs décident de se partager équitablement tout l'argent restant.

**Questions**

1. Combien d'argent les clubs ont-ils gagné grâce à la vente des billets ?
2. Quel est le montant total des dépenses ?
3. Combien d'argent reçoit chaque club ? Écris une expression numérique avec des parenthèses.""",
            "correction": """**1. Argent gagné grâce aux billets**

16 × 7 + 12 × 9 = 112 + 108 = **220 €**

**2. Dépenses totales**

85 + 5 × 9 = 85 + 45 = **130 €**

**3. Argent reçu par chaque club**

Argent disponible : 150 + 220 − 130 = **240 €**.

Partage : 240 ÷ 4 = **60 €**.

**Expression complète :**

(150 + (16 × 7 + 12 × 9) − (85 + 5 × 9)) ÷ 4 = **60 €**

**Réponse :** Chaque club reçoit **60 €**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P8-02",
            "titre": "Le club manga",
            "enonce": """**Le club manga**

Le club manga du collège prépare une exposition de dessins.

Six élèves réalisent chacun 8 dessins. Parmi ces six élèves, trois réalisent ensuite 4 dessins supplémentaires chacun.

Le club réserve 5 dessins pour décorer l'entrée de l'exposition.

Les autres dessins sont répartis équitablement sur 5 panneaux.

**Questions**

1. Combien de dessins les élèves ont-ils réalisés au total ?
2. Combien de dessins restent disponibles pour les panneaux ?
3. Combien de dessins seront exposés sur chaque panneau ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Nombre total de dessins**

6 × 8 + 3 × 4 = 48 + 12 = **60 dessins**

**2. Dessins disponibles pour les panneaux**

60 − 5 = **55 dessins**

**3. Nombre de dessins par panneau**

55 ÷ 5 = **11 dessins**

**Expression complète :**

((6 × 8 + 3 × 4) − 5) ÷ 5 = **11**

**Réponse :** Chaque panneau présentera **11 dessins**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P8-03",
            "titre": "Une aventure en jeu vidéo",
            "enonce": """**Une aventure en jeu vidéo**

Quatre amis jouent en équipe à un jeu vidéo d'aventure.

Leur équipe gagne :
- 4 missions rapportant chacune 35 pièces d'or ;
- 3 défis rapportant chacun 20 pièces d'or.

Les quatre amis utilisent ensuite leur trésor commun pour acheter 2 équipements à 22 pièces d'or chacun.

Ils décident de partager équitablement les pièces restantes entre eux.

**Questions**

1. Combien de pièces d'or l'équipe a-t-elle gagnées au total ?
2. Combien de pièces d'or a-t-elle dépensées pour les équipements ?
3. Combien de pièces d'or chaque ami reçoit-il ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Pièces d'or gagnées**

4 × 35 + 3 × 20 = 140 + 60 = **200 pièces**

**2. Pièces d'or dépensées**

2 × 22 = **44 pièces**

**3. Partage entre les quatre amis**

Pièces restantes : 200 − 44 = **156 pièces**.

Chaque ami reçoit : 156 ÷ 4 = **39 pièces**.

**Expression complète :**

((4 × 35 + 3 × 20) − (2 × 22)) ÷ 4 = **39**

**Réponse :** Chaque ami reçoit **39 pièces d'or**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P8-04",
            "titre": "Le club de robotique",
            "enonce": """**Le club de robotique**

Le club de robotique du collège organise un atelier pour **6 équipes d'élèves**.

Pour alimenter leurs petits robots, le professeur dispose de :
- 4 boîtes contenant chacune 12 piles ;
- 3 boîtes contenant chacune 8 piles.

Il garde 12 piles en réserve pour remplacer celles qui pourraient tomber en panne.

Il partage équitablement toutes les autres piles entre les 6 équipes.

**Questions**

1. Combien de piles le professeur possède-t-il au total ?
2. Combien de piles peut-il distribuer après avoir constitué sa réserve ?
3. Combien de piles chaque équipe reçoit-elle ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Nombre total de piles**

4 × 12 + 3 × 8 = 48 + 24 = **72 piles**.

**2. Piles disponibles pour les équipes**

72 − 12 = **60 piles**.

**3. Piles reçues par chaque équipe**

60 ÷ 6 = **10 piles**.

**Expression complète :**

(4 × 12 + 3 × 8 − 12) ÷ 6 = **10**.

**Réponse :** Chaque équipe reçoit **10 piles**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P8-05",
            "titre": "Le jeu de piste du collège",
            "enonce": """**Le jeu de piste du collège**

Des élèves organisent un jeu de piste au collège. Ils disposent d'un budget de **120 €**.

Pour les 5 équipes participantes, ils préparent un kit par équipe contenant :
- 2 carnets à 6 € chacun ;
- 3 stylos à 2 € chacun.

Le magasin accorde une réduction de **10 € sur la commande totale**, mais facture **8 € de frais de livraison**.

**Questions**

1. Combien coûte le matériel pour une équipe ?
2. Quel est le montant total à payer pour les 5 équipes, après la réduction et les frais de livraison ?
3. Combien restera-t-il sur le budget ? Écris une seule expression numérique avec des parenthèses.""",
            "correction": """**1. Prix du matériel pour une équipe**

2 × 6 + 3 × 2 = 12 + 6 = **18 €**.

**2. Montant total de la commande**

Prix des 5 kits : 5 × 18 = **90 €**.

Après réduction et frais de livraison : 90 − 10 + 8 = **88 €**.

**3. Argent restant**

120 − 88 = **32 €**.

**Expression complète :**

120 − (5 × (2 × 6 + 3 × 2) − 10 + 8) = **32**.

**Réponse :** Il restera **32 €** pour organiser le jeu de piste.""",
            "reponse_attendue": None,
        },

    ],
    3: [
        {
            "id": "P9-01",
            "titre": "Le potager du collège",
            "enonce": """**Le potager du collège**

Le collège souhaite aménager un potager avec **4 parcelles**.

Pour chaque parcelle, les élèves prévoient :
- 3 rangées de 8 salades ;
- 2 rangées de 6 salades.

Le collège dispose de **15 plateaux contenant chacun 12 plants de salade**.

Les élèves aimeraient agrandir leurs plantations. Ils hésitent entre deux possibilités :
- **Projet A :** ajouter une rangée de 8 salades à chaque parcelle ;
- **Projet B :** ajouter deux rangées de 6 salades à chaque parcelle.

**Questions**

1. Combien de plants faut-il pour réaliser les 4 parcelles avant leur agrandissement ?
2. Calcule le nombre total de plants nécessaires pour chaque projet.
3. Quel projet peut être réalisé avec les plants disponibles ? Combien de plants restera-t-il ou manquera-t-il ? Justifie avec des calculs.""",
            "correction": """**1. Plants nécessaires au départ**

Pour une parcelle : 3 × 8 + 2 × 6 = 24 + 12 = **36 plants**.

Pour les 4 parcelles : 4 × 36 = **144 plants**.

**2. Comparaison des projets**

Projet A : 4 × (36 + 8) = **176 plants**.

Projet B : 4 × (36 + 2 × 6) = **192 plants**.

**3. Quel projet choisir ?**

Plants disponibles : 15 × 12 = **180 plants**.

Projet A : 180 − 176 = **4 plants restants**.

Projet B : 192 − 180 = **12 plants manquants**.

**Expression complète pour le projet A :**

15 × 12 − 4 × (3 × 8 + 2 × 6 + 8) = **4**

**Réponse :** Seul le projet A peut être réalisé. Il restera **4 plants**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P9-02",
            "titre": "Le tournoi de jeux vidéo",
            "enonce": """**Le tournoi de jeux vidéo**

Le club de jeux vidéo du collège organise un tournoi réunissant **24 élèves répartis en 4 équipes de 6 joueurs**.

Le club dispose d'un budget de **280 €**.

Il prévoit :
- un badge à 2 € pour chaque participant ;
- la location d'une salle à 65 €.

Pour récompenser les 4 équipes, le club hésite entre deux choix :
- **Choix A :** offrir à chaque équipe un trophée à 18 € et un paquet de cartes à collectionner à 12 € ;
- **Choix B :** offrir à chaque équipe un trophée à 25 € et un paquet d'autocollants à 7 €.

Le club souhaite conserver **au moins 40 €** après toutes les dépenses.

**Questions**

1. Calcule le montant des dépenses pour chaque choix.
2. Combien d'argent restera-t-il avec chacun des deux choix ?
3. Quel choix permet de conserver au moins 40 € ? Justifie ta réponse.""",
            "correction": """**1. Dépenses**

Dépenses communes : 24 × 2 + 65 = 48 + 65 = **113 €**.

Choix A : 113 + 4 × (18 + 12) = **233 €**.

Choix B : 113 + 4 × (25 + 7) = **241 €**.

**2. Argent restant**

Choix A : 280 − 233 = **47 €**.

Choix B : 280 − 241 = **39 €**.

**3. Décision**

Le choix A laisse 47 €, ce qui respecte la condition d'au moins 40 €.

Le choix B laisse seulement 39 €.

**Expression complète pour le choix A :**

280 − (24 × 2 + 65 + 4 × (18 + 12)) = **47 €**

**Réponse :** Le club choisit **A** pour conserver au moins 40 €.""",
            "reponse_attendue": None,
        },
        {
            "id": "P9-03",
            "titre": "Une sortie au festival du manga",
            "enonce": """**Une sortie au festival du manga**

Quatre classes de 18 élèves organisent une sortie au festival du manga. Six adultes les accompagnent.

Le collège dispose de **550 €** pour le transport.

Deux possibilités sont proposées :
- **Choix A :** louer 3 cars de 28 places à 180 € chacun ;
- **Choix B :** louer 2 cars de 38 places à 240 € chacun.

Tous les élèves et les adultes doivent avoir une place assise.

**Questions**

1. Combien de personnes participent à la sortie ?
2. Pour chaque choix, calcule le nombre de places disponibles et le prix total du transport.
3. Quel choix permet de transporter tout le monde sans dépasser le budget ? Justifie ta réponse.""",
            "correction": """**1. Nombre de participants**

Élèves : 4 × 18 = **72 élèves**.

Avec les six adultes : 72 + 6 = **78 personnes**.

**2. Comparaison des deux choix**

Choix A : 3 × 28 = **84 places**, pour 3 × 180 = **540 €**.

Places restantes : 84 − 78 = **6 places**.

Choix B : 2 × 38 = **76 places**, pour 2 × 240 = **480 €**.

Places manquantes : 78 − 76 = **2 places**.

**3. Quel choix retenir ?**

Le choix A a assez de places et coûte 540 €, soit moins que le budget de 550 €.

Le choix B coûte moins cher, mais il manque 2 places.

**Expressions complètes pour le choix A :**

3 × 28 − (4 × 18 + 6) = **6 places restantes**.

550 − 3 × 180 = **10 € restants**.

**Réponse :** Le collège doit choisir **A**.""",
            "reponse_attendue": None,
        },
        {
            "id": "P9-04",
            "titre": "Les cristaux du jeu vidéo",
            "enonce": """**Les cristaux du jeu vidéo**

Dans un jeu vidéo d'aventure, Maya possède **90 cristaux**.

Elle gagne ensuite :
- 30 cristaux pour chacune des 4 quêtes terminées ;
- 15 cristaux pour chacun des 3 défis réussis.

Pour accéder à l'atelier de fabrication, elle doit payer **28 cristaux**.

Dans cet atelier, chaque équipement complet comprend :
- une épée coûtant 18 cristaux ;
- un bouclier coûtant 22 cristaux.

Maya souhaite fabriquer le plus d'équipements complets possible, tout en conservant **au moins 25 cristaux**.

**Questions**

1. Combien de cristaux Maya possède-t-elle après les quêtes et les défis ?
2. Combien de cristaux peut-elle utiliser pour fabriquer ses équipements, en tenant compte de l'accès à l'atelier et des 25 cristaux à conserver ?
3. Quel est le nombre maximal d'équipements complets qu'elle peut fabriquer ? Combien de cristaux lui restera-t-il réellement ?""",
            "correction": """**1. Total des cristaux**

90 + 4 × 30 + 3 × 15 = 90 + 120 + 45 = **255 cristaux**.

**2. Cristaux disponibles pour la fabrication**

Après avoir payé 28 cristaux pour l'accès et réservé 25 cristaux :

255 − (28 + 25) = **202 cristaux**.

**3. Nombre maximal d'équipements**

Un équipement coûte 18 + 22 = **40 cristaux**.

5 équipements coûtent 5 × 40 = **200 cristaux**.

6 équipements coûteraient 6 × 40 = **240 cristaux**, ce qui dépasse les 202 cristaux disponibles.

Maya peut donc fabriquer au maximum **5 équipements complets**.

Cristaux réellement restants :

255 − 28 − 5 × (18 + 22) = **27 cristaux**.

**Réponse :** Maya peut fabriquer **5 équipements complets** et conserver **27 cristaux**, donc au moins 25.""",
            "reponse_attendue": None,
        },
        {
            "id": "P9-05",
            "titre": "La bibliothèque de mangas",
            "enonce": """**La bibliothèque de mangas**

Le club manga du collège possède une collection de mangas.

Il reçoit une livraison contenant :
- 4 cartons de 12 mangas ;
- 3 cartons de 8 mangas.

Le club prête ensuite **2 lots de 15 mangas** à deux classes du collège.

Il range tous les mangas qui lui restent sur **6 étagères**, avec exactement **14 mangas par étagère**.

**Questions**

1. Combien de mangas restent au club après les prêts ?
2. Combien de mangas le club possédait-il avant la livraison ? Explique ton raisonnement.
3. Écris une seule expression numérique avec des parenthèses permettant de retrouver le nombre initial de mangas.""",
            "correction": """**1. Mangas restants**

6 × 14 = **84 mangas**.

**2. Retrouver la collection initiale**

On raisonne à l'envers.

Avant les prêts, le club possédait 84 + 2 × 15 = 84 + 30 = **114 mangas**.

La livraison contenait 4 × 12 + 3 × 8 = 48 + 24 = **72 mangas**.

Avant la livraison, le club possédait donc 114 − 72 = **42 mangas**.

**3. Expression complète**

6 × 14 + (2 × 15) − (4 × 12 + 3 × 8) = **42**.

**Vérification :** 42 + 72 − 30 = **84 mangas**.

**Réponse :** Le club possédait **42 mangas avant la livraison**.""",
            "reponse_attendue": None,
        },

    ],
}


# Réponses pour une future correction interactive.
# Les champs « nombre » et « choix » peuvent être vérifiés automatiquement.
# « texte_libre » permet d'écrire une expression ou justification ; elle ne doit
# PAS être jugée correcte par une simple comparaison de texte.
# Ces champs sont invisibles à l'élève tant que l'interface ne les affiche pas.
REPONSES_PRIORITES = {'P7-01': [{'id': 'r1',
            'question': 1,
            'libelle': 'Recettes de la vente des billets',
            'type': 'nombre',
            'attendu': 156,
            'unite': '€'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Dépenses totales',
            'type': 'nombre',
            'attendu': 93,
            'unite': '€'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Argent restant',
            'type': 'nombre',
            'attendu': 243,
            'unite': '€'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P7-02': [{'id': 'r1',
            'question': 1,
            'libelle': 'Cartes après ouverture des paquets',
            'type': 'nombre',
            'attendu': 144,
            'unite': 'cartes'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Cartes données',
            'type': 'nombre',
            'attendu': 14,
            'unite': 'cartes'},
           {'id': 'r3',
            'question': 2,
            'libelle': 'Cartes reçues',
            'type': 'nombre',
            'attendu': 18,
            'unite': 'cartes'},
           {'id': 'r4',
            'question': 3,
            'libelle': 'Cartes possédées finalement',
            'type': 'nombre',
            'attendu': 148,
            'unite': 'cartes'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P7-03': [{'id': 'r1',
            'question': 1,
            'libelle': 'Volants achetés',
            'type': 'nombre',
            'attendu': 48,
            'unite': 'volants'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Volants avant le tournoi',
            'type': 'nombre',
            'attendu': 88,
            'unite': 'volants'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Volants utilisables restants',
            'type': 'nombre',
            'attendu': 63,
            'unite': 'volants'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P7-04': [{'id': 'r1',
            'question': 1,
            'libelle': 'Pièces d’or gagnées',
            'type': 'nombre',
            'attendu': 105,
            'unite': 'pièces'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Pièces dépensées',
            'type': 'nombre',
            'attendu': 72,
            'unite': 'pièces'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Pièces restantes',
            'type': 'nombre',
            'attendu': 183,
            'unite': 'pièces'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P7-05': [{'id': 'r1',
            'question': 1,
            'libelle': 'Feuilles nécessaires pour une table',
            'type': 'nombre',
            'attendu': 20,
            'unite': 'feuilles'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Feuilles nécessaires pour les quatre tables',
            'type': 'nombre',
            'attendu': 80,
            'unite': 'feuilles'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Feuilles restantes',
            'type': 'nombre',
            'attendu': 20,
            'unite': 'feuilles'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P8-01': [{'id': 'r1',
            'question': 1,
            'libelle': 'Recettes des billets',
            'type': 'nombre',
            'attendu': 220,
            'unite': '€'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Dépenses totales',
            'type': 'nombre',
            'attendu': 130,
            'unite': '€'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Part reçue par chaque club',
            'type': 'nombre',
            'attendu': 60,
            'unite': '€'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P8-02': [{'id': 'r1',
            'question': 1,
            'libelle': 'Dessins réalisés au total',
            'type': 'nombre',
            'attendu': 60,
            'unite': 'dessins'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Dessins disponibles pour les panneaux',
            'type': 'nombre',
            'attendu': 55,
            'unite': 'dessins'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Dessins par panneau',
            'type': 'nombre',
            'attendu': 11,
            'unite': 'dessins'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P8-03': [{'id': 'r1',
            'question': 1,
            'libelle': 'Pièces d’or gagnées',
            'type': 'nombre',
            'attendu': 200,
            'unite': 'pièces'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Pièces d’or dépensées',
            'type': 'nombre',
            'attendu': 44,
            'unite': 'pièces'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Pièces d’or reçues par ami',
            'type': 'nombre',
            'attendu': 39,
            'unite': 'pièces'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P8-04': [{'id': 'r1',
            'question': 1,
            'libelle': 'Piles disponibles au départ',
            'type': 'nombre',
            'attendu': 72,
            'unite': 'piles'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Piles à distribuer',
            'type': 'nombre',
            'attendu': 60,
            'unite': 'piles'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Piles reçues par équipe',
            'type': 'nombre',
            'attendu': 10,
            'unite': 'piles'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P8-05': [{'id': 'r1',
            'question': 1,
            'libelle': 'Prix du kit pour une équipe',
            'type': 'nombre',
            'attendu': 18,
            'unite': '€'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Montant à payer pour les cinq équipes',
            'type': 'nombre',
            'attendu': 88,
            'unite': '€'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Argent restant sur le budget',
            'type': 'nombre',
            'attendu': 32,
            'unite': '€'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P9-01': [{'id': 'r1',
            'question': 1,
            'libelle': 'Plants nécessaires avant agrandissement',
            'type': 'nombre',
            'attendu': 144,
            'unite': 'plants'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Plants nécessaires pour le projet A',
            'type': 'nombre',
            'attendu': 176,
            'unite': 'plants'},
           {'id': 'r3',
            'question': 2,
            'libelle': 'Plants nécessaires pour le projet B',
            'type': 'nombre',
            'attendu': 192,
            'unite': 'plants'},
           {'id': 'r4',
            'question': 3,
            'libelle': 'Plants restants avec le projet A',
            'type': 'nombre',
            'attendu': 4,
            'unite': 'plants'},
           {'id': 'r5',
            'question': 3,
            'libelle': 'Plants manquants pour le projet B',
            'type': 'nombre',
            'attendu': 12,
            'unite': 'plants'},
           {'id': 'choix',
            'question': 3,
            'libelle': 'Projet réalisable',
            'type': 'choix',
            'attendu': 'A',
            'options': ['A', 'B']},
           {'id': 'justification',
            'question': 3,
            'libelle': 'Ma justification (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P9-02': [{'id': 'r1',
            'question': 1,
            'libelle': 'Dépenses du choix A',
            'type': 'nombre',
            'attendu': 233,
            'unite': '€'},
           {'id': 'r2',
            'question': 1,
            'libelle': 'Dépenses du choix B',
            'type': 'nombre',
            'attendu': 241,
            'unite': '€'},
           {'id': 'r3',
            'question': 2,
            'libelle': 'Somme restante avec le choix A',
            'type': 'nombre',
            'attendu': 47,
            'unite': '€'},
           {'id': 'r4',
            'question': 2,
            'libelle': 'Somme restante avec le choix B',
            'type': 'nombre',
            'attendu': 39,
            'unite': '€'},
           {'id': 'choix',
            'question': 3,
            'libelle': 'Choix qui conserve au moins 40 €',
            'type': 'choix',
            'attendu': 'A',
            'options': ['A', 'B']},
           {'id': 'justification',
            'question': 3,
            'libelle': 'Ma justification (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P9-03': [{'id': 'r1',
            'question': 1,
            'libelle': 'Nombre total de participants',
            'type': 'nombre',
            'attendu': 78,
            'unite': 'personnes'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Nombre de places avec le choix A',
            'type': 'nombre',
            'attendu': 84,
            'unite': 'places'},
           {'id': 'r3',
            'question': 2,
            'libelle': 'Coût du choix A',
            'type': 'nombre',
            'attendu': 540,
            'unite': '€'},
           {'id': 'r4',
            'question': 2,
            'libelle': 'Nombre de places avec le choix B',
            'type': 'nombre',
            'attendu': 76,
            'unite': 'places'},
           {'id': 'r5',
            'question': 2,
            'libelle': 'Coût du choix B',
            'type': 'nombre',
            'attendu': 480,
            'unite': '€'},
           {'id': 'choix',
            'question': 3,
            'libelle': 'Choix qui respecte places et budget',
            'type': 'choix',
            'attendu': 'A',
            'options': ['A', 'B']},
           {'id': 'justification',
            'question': 3,
            'libelle': 'Ma justification (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P9-04': [{'id': 'r1',
            'question': 1,
            'libelle': 'Cristaux après les quêtes et les défis',
            'type': 'nombre',
            'attendu': 255,
            'unite': 'cristaux'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Cristaux disponibles pour fabriquer',
            'type': 'nombre',
            'attendu': 202,
            'unite': 'cristaux'},
           {'id': 'r3',
            'question': 3,
            'libelle': 'Nombre maximal d’équipements',
            'type': 'nombre',
            'attendu': 5,
            'unite': 'équipements'},
           {'id': 'r4',
            'question': 3,
            'libelle': 'Cristaux réellement restants',
            'type': 'nombre',
            'attendu': 27,
            'unite': 'cristaux'},
           {'id': 'justification',
            'question': 3,
            'libelle': 'Ma justification (à comparer avec la correction)',
            'type': 'texte_libre'}],
 'P9-05': [{'id': 'r1',
            'question': 1,
            'libelle': 'Mangas restants après les prêts',
            'type': 'nombre',
            'attendu': 84,
            'unite': 'mangas'},
           {'id': 'r2',
            'question': 2,
            'libelle': 'Mangas possédés avant livraison',
            'type': 'nombre',
            'attendu': 42,
            'unite': 'mangas'},
           {'id': 'expression',
            'question': 3,
            'libelle': 'Mon expression numérique (à comparer avec la correction)',
            'type': 'texte_libre'}]}

def generer_modele_p7_sciences():
    groupes = random.randint(6, 10)
    eleves_par_groupe = random.choice([4, 5])
    piles_par_eleve = 2

    stock = random.randint(7, 17)
    capacite_paquet = random.choice([10, 12])
    prix_paquet = random.randint(7, 12)
    frais = random.randint(10, 25)

    eleves = groupes * eleves_par_groupe
    necessaires = eleves * piles_par_eleve
    a_acheter = necessaires - stock

    quotient, reste = divmod(a_acheter, capacite_paquet)
    paquets = quotient + (1 if reste > 0 else 0)

    depense = paquets * prix_paquet + frais
    # Marge budgétaire plus diversifiée, adaptée au coût de l'atelier.
    budget = depense + random.randint(12, 95)
    restant = budget - depense

    enonce = (
        "**L'atelier de sciences**\n\n"
        f"Un collège organise un atelier avec {groupes} groupes "
        f"de {eleves_par_groupe} élèves.\n\n"
        f"Chaque élève a besoin de {piles_par_eleve} piles "
        "pour son expérience.\n\n"
        f"Le collège possède déjà {stock} piles.\n"
        f"Les piles sont vendues par paquets de "
        f"{capacite_paquet}, à {prix_paquet} € le paquet.\n\n"
        f"Le matériel supplémentaire coûte {frais} €.\n"
        f"Le budget total est de {budget} €.\n\n"
        "**Questions**\n\n"
        "1. Combien de piles faut-il pour tous les élèves ?\n\n"
        "2. Combien de paquets faut-il acheter au minimum ?\n\n"
        "3. Combien restera-t-il sur le budget après "
        "l'achat des paquets et du matériel supplémentaire ?"
    )

    correction = (
        "**1. Nombre de piles nécessaires**\n\n"
        f"Élèves : {groupes} × {eleves_par_groupe} "
        f"= {eleves}.\n"
        f"Piles : {eleves} × {piles_par_eleve} "
        f"= {necessaires} piles.\n\n"
        "**2. Piles supplémentaires nécessaires**\n\n"
        f"Le collège possède déjà {stock} piles sur les {necessaires} nécessaires.\n"
        f"Il manque donc {necessaires} − {stock} = {a_acheter} piles.\n\n"
        "**3. Nombre minimal de paquets**\n\n"
        f"Les piles sont vendues par paquets de {capacite_paquet}.\n"
        f"Division : {a_acheter} ÷ {capacite_paquet}.\n"
        f"Quotient entier : {quotient}, reste : {reste}.\n"
        f"Il faut acheter {paquets} paquets.\n\n"
        "**4. Budget restant**\n\n"
        f"Prix des paquets : {paquets} × {prix_paquet} "
        f"= {paquets * prix_paquet} €.\n"
        f"Dépense totale : {paquets * prix_paquet} "
        f"+ {frais} = {depense} €.\n"
        f"Budget restant : {budget} - {depense} "
        f"= {restant} €."
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M01",
        "titre": "L'atelier de sciences",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Piles nécessaires",
                "type": "nombre",
                "attendu": necessaires,
                "unite": "piles"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Paquets à acheter",
                "type": "nombre",
                "attendu": paquets,
                "unite": "paquets"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Budget restant",
                "type": "nombre",
                "attendu": restant,
                "unite": "€"
            }
        ]
    })


def generer_modele_p7_patisserie():
    plateaux = random.randint(6, 10)
    par_plateau = 12
    reserves = random.randint(7, 16)
    par_sachet = random.choice([4, 5, 6])
    prix_sachet = random.randint(5, 8)
    cout_ingredients = random.randint(20, 35)

    total = plateaux * par_plateau
    disponibles = total - reserves
    # Maintenir une vraie question sur les biscuits hors sachets.
    if disponibles % par_sachet == 0:
        reserves += 1
        disponibles -= 1
    sachets, reste = divmod(disponibles, par_sachet)
    recette = sachets * prix_sachet
    benefice = recette - cout_ingredients

    enonce = (
        "**Le stand de pâtisserie**\n\n"
        f"Pour une fête du collège, un club prépare {plateaux} "
        f"plateaux de {par_plateau} biscuits chacun.\n\n"
        f"Il réserve {reserves} biscuits pour les bénévoles.\n\n"
        f"Les autres biscuits sont vendus par sachets de "
        f"{par_sachet}, au prix de {prix_sachet} € le sachet.\n\n"
        "Seuls les sachets complets peuvent être vendus.\n\n"
        f"Les ingrédients ont coûté {cout_ingredients} €.\n"
        "Tous les sachets préparés sont vendus.\n\n"
        "**Questions**\n\n"
        "1. Combien de biscuits sont disponibles pour la vente ?\n\n"
        "2. Combien de sachets complets peut-on préparer ? "
        "Combien de biscuits restent hors des sachets ?\n\n"
        "3. Quel bénéfice le club réalise-t-il après "
        "avoir payé les ingrédients ?"
    )

    correction = (
        "**1. Biscuits disponibles**\n\n"
        f"{plateaux} × {par_plateau} = {total} biscuits.\n\n"
        f"{total} − {reserves} = {disponibles} biscuits.\n\n"
        "**2. Préparation des sachets**\n\n"
        f"Division euclidienne : {disponibles} ÷ {par_sachet}.\n\n"
        f"Quotient = {sachets}, reste = {reste}.\n\n"
        f"Vérification : {disponibles} = "
        f"{par_sachet} × {sachets} + {reste}.\n\n"
        f"On peut vendre {sachets} sachets complets.\n"
        f"{reste} biscuits restent hors des sachets.\n\n"
        "**3. Bénéfice du club**\n\n"
        f"Recette : {sachets} × {prix_sachet} "
        f"= {recette} €.\n\n"
        f"Bénéfice : {recette} − {cout_ingredients} "
        f"= {benefice} €.\n\n"
        f"**Réponse :** Le bénéfice est de {benefice} €."
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M02",
        "titre": "Le stand de pâtisserie",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Biscuits disponibles",
                "type": "nombre",
                "attendu": disponibles,
                "unite": "biscuits"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Sachets complets",
                "type": "nombre",
                "attendu": sachets,
                "unite": "sachets"
            },
            {
                "id": "r3",
                "question": 2,
                "libelle": "Biscuits hors des sachets",
                "type": "nombre",
                "attendu": reste,
                "unite": "biscuits"
            },
            {
                "id": "r4",
                "question": 3,
                "libelle": "Bénéfice du club",
                "type": "nombre",
                "attendu": benefice,
                "unite": "€"
            }
        ]
    })

def generer_modele_p7_enigmes():
    """N7 : scores, écart, puis manche décisive à 2 ou 3 énigmes faciles."""
    points_facile = random.choice([6, 8, 10, 12])
    points_difficile = random.choice([p for p in [12, 14, 15, 18, 20] if p > points_facile])
    penalite = random.choice([2, 3, 4, 5])
    for _ in range(3000):
        faciles_a = random.randint(3, 9)
        difficiles_a = random.randint(1, 5)
        indices_a = random.randint(0, 3)
        faciles_b = random.randint(3, 9)
        difficiles_b = random.randint(1, 5)
        indices_b = random.randint(0, 3)
        score_a = faciles_a * points_facile + difficiles_a * points_difficile - indices_a * penalite
        score_b = faciles_b * points_facile + difficiles_b * points_difficile - indices_b * penalite
        ecart = abs(score_a - score_b)
        if 10 < ecart <= 30:
            break
    else:
        raise ValueError("Impossible de trouver une manche décisive cohérente")

    gagnant = "A" if score_a > score_b else "B"
    perdant = "B" if gagnant == "A" else "A"
    points_manche = 10
    faciles_pour_egaliser = (ecart + points_manche - 1) // points_manche
    def ligne_indice(n):
        return f"{n} indice{'s' if n != 1 else ''} utilisé{'s' if n != 1 else ''}"
    enonce = (
        "**Le tournoi d'énigmes**\n\n"
        "Deux équipes participent à un tournoi d'énigmes au collège.\n\n"
        "Le règlement prévoit :\n"
        f"- {points_facile} points par énigme facile résolue ;\n"
        f"- {points_difficile} points par énigme difficile résolue ;\n"
        f"- {penalite} points retirés pour chaque indice utilisé.\n\n"
        "**Équipe A :**\n"
        f"- {faciles_a} énigmes faciles ;\n"
        f"- {difficiles_a} énigmes difficiles ;\n"
        f"- {ligne_indice(indices_a)}.\n\n"
        "**Équipe B :**\n"
        f"- {faciles_b} énigmes faciles ;\n"
        f"- {difficiles_b} énigmes difficiles ;\n"
        f"- {ligne_indice(indices_b)}.\n\n"
        "**Manche décisive :** l'équipe perdante, pour rattraper son retard, "
        "peut répondre avant son adversaire à trois nouvelles énigmes faciles "
        "consécutives. Chaque réponse juste rapporte 10 points, et aucun indice "
        "n'est utilisé.\n\n"
        "**Questions**\n\n"
        "1. Quel est le score de l'équipe A ?\n\n"
        "2. Quel est le score de l'équipe B ?\n\n"
        "3. Quel est l'écart de points entre les deux équipes ?\n\n"
        "4. À combien de nouvelles énigmes faciles l'équipe en retard doit-elle "
        "répondre correctement de suite pour au moins égaliser le score ?"
    )
    correction = (
        "**1. Score de l'équipe A**\n\n"
        f"{faciles_a} × {points_facile} + {difficiles_a} × {points_difficile} "
        f"− {indices_a} × {penalite} = {score_a} points.\n\n"
        "**2. Score de l'équipe B**\n\n"
        f"{faciles_b} × {points_facile} + {difficiles_b} × {points_difficile} "
        f"− {indices_b} × {penalite} = {score_b} points.\n\n"
        "**3. Écart de points**\n\n"
        f"L'équipe {gagnant} mène : {max(score_a,score_b)} − {min(score_a,score_b)} "
        f"= {ecart} points d'avance.\n\n"
        "**4. Manche décisive**\n\n"
        f"L'équipe {perdant} doit rattraper {ecart} points. "
        f"Chaque énigme de la manche décisive vaut 10 points.\n"
        f"{ecart} ÷ 10 : on arrondit au nombre entier supérieur "
        f"pour obtenir {faciles_pour_egaliser} énigmes.\n"
        f"Avec {faciles_pour_egaliser} énigmes, elle gagne "
        f"{faciles_pour_egaliser * points_manche} points et peut au moins égaliser."
    )
    return _mc_uniformiser_exercice({
        "id":"P7-M03", "titre":"Le tournoi d'énigmes", "enonce":enonce,
        "correction":correction, "reponse_attendue":None,
        "champs_reponse":[
            {"id":"r1", "question":1, "libelle":"Score de l'équipe A", "type":"nombre", "attendu":score_a, "unite":"points"},
            {"id":"r2", "question":2, "libelle":"Score de l'équipe B", "type":"nombre", "attendu":score_b, "unite":"points"},
            {"id":"r3", "question":3, "libelle":"Équipe gagnante", "type":"choix", "attendu":gagnant, "options":["A","B"]},
            {"id":"r4", "question":3, "libelle":"Écart de points", "type":"nombre", "attendu":ecart, "unite":"points"},
            {"id":"r5", "question":4, "libelle":"Énigmes faciles à résoudre", "type":"nombre", "attendu":faciles_pour_egaliser, "unite":"énigmes"},
        ],
    })

def generer_modele_p7_photos():
    def euros(centimes):
        return f"{centimes / 100:.2f}".replace(".", ",")

    while True:
        nb_photos = random.randint(12, 28)

        frais_a = random.randint(4, 8)
        tarif_a = random.choice([80, 90, 100, 110])

        frais_b = random.randint(10, 15)
        tarif_b = random.choice([40, 50, 60, 70])

        cout_a = frais_a * 100 + nb_photos * tarif_a
        cout_b = frais_b * 100 + nb_photos * tarif_b

        if abs(cout_a - cout_b) >= 150:
            break

    gagnant = "A" if cout_a < cout_b else "B"
    economie = abs(cout_a - cout_b)

    formule_a = (
        f"({frais_a} + {nb_photos} × {euros(tarif_a)})"
    )
    formule_b = (
        f"({frais_b} + {nb_photos} × {euros(tarif_b)})"
    )

    enonce = (
        "**L'exposition de photos**\n\n"
        "Le club photo du collège prépare une exposition.\n\n"
        f"Il souhaite faire imprimer {nb_photos} photos.\n\n"
        "Deux imprimeurs proposent la même qualité :\n\n"
        "**Offre A :**\n"
        f"- {frais_a} € de frais fixes ;\n"
        f"- {euros(tarif_a)} € par photo.\n\n"
        "**Offre B :**\n"
        f"- {frais_b} € de frais fixes ;\n"
        f"- {euros(tarif_b)} € par photo.\n\n"
        "**Questions**\n\n"
        "1. Quel est le coût total avec l'offre A ?\n\n"
        "2. Quel est le coût total avec l'offre B ?\n\n"
        "3. Quelle offre est la moins chère ? "
        "Combien le club économise-t-il ? "
        "Écris une expression numérique avec des "
        "parenthèses pour justifier la différence."
    )

    if gagnant == "A":
        expression_ecart = f"{formule_b} − {formule_a}"
    else:
        expression_ecart = f"{formule_a} − {formule_b}"

    correction = (
        "**1. Coût de l'offre A**\n\n"
        f"Frais fixes : {frais_a} €.\n\n"
        f"Prix des photos : {nb_photos} × "
        f"{euros(tarif_a)} = "
        f"{euros(nb_photos * tarif_a)} €.\n\n"
        f"Total : {formule_a} = {euros(cout_a)} €.\n\n"
        "**2. Coût de l'offre B**\n\n"
        f"Frais fixes : {frais_b} €.\n\n"
        f"Prix des photos : {nb_photos} × "
        f"{euros(tarif_b)} = "
        f"{euros(nb_photos * tarif_b)} €.\n\n"
        f"Total : {formule_b} = {euros(cout_b)} €.\n\n"
        "**3. Comparaison des offres**\n\n"
        f"Offre A : {euros(cout_a)} €.\n\n"
        f"Offre B : {euros(cout_b)} €.\n\n"
        f"L'offre {gagnant} est la moins chère.\n\n"
        "**Expression numérique :**\n\n"
        f"{expression_ecart} = {euros(economie)} €.\n\n"
        f"**Réponse :** Le club choisit l'offre "
        f"{gagnant} et économise {euros(economie)} €."
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M04",
        "titre": "L'exposition de photos",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Coût de l'offre A",
                "type": "nombre",
                "attendu": round(cout_a / 100, 2),
                "unite": "€"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Coût de l'offre B",
                "type": "nombre",
                "attendu": round(cout_b / 100, 2),
                "unite": "€"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Offre la moins chère",
                "type": "choix",
                "attendu": gagnant,
                "options": ["A", "B"]
            },
            {
                "id": "r4",
                "question": 3,
                "libelle": "Économie réalisée",
                "type": "nombre",
                "attendu": round(economie / 100, 2),
                "unite": "€"
            },
            {
                "id": "expression",
                "question": 3,
                "libelle": "Mon expression numérique (à comparer avec la correction)",
                "type": "texte_libre"
            }
        ]
    })

def generer_modele_p7_velo():
    """Défi collectif : le nombre de cyclistes intervient réellement dans le calcul."""

    def km(valeur):
        return f"{valeur / 10:.1f}".replace(".", ",")

    # Distances en dixièmes de kilomètre : pas d'erreurs d'arrondi.
    nb_cyclistes = random.randint(3, 5)
    trajet = random.randint(32, 68)
    boucle = random.randint(18, 36)
    nb_boucles = random.randint(2, 4)
    petit_tour = random.randint(12, 23)

    aller_retour = 2 * trajet                   # par cycliste
    distance_individuelle = aller_retour + nb_boucles * boucle
    distance_collective = nb_cyclistes * distance_individuelle

    quotient_voulu = random.randint(1, 4)
    reste_voulu = random.randint(1, petit_tour - 1)
    manque_par_cycliste = quotient_voulu * petit_tour + reste_voulu
    manque_collectif = nb_cyclistes * manque_par_cycliste
    objectif_collectif = distance_collective + manque_collectif

    quotient, reste = divmod(manque_par_cycliste, petit_tour)
    tours = quotient + (1 if reste else 0)

    enonce = (
        "**Le rallye à vélo**\n\n"
        f"{nb_cyclistes} amis participent à un défi collectif à vélo. "
        "Chacun emprunte le même parcours. "
        "Pour ce défi, leurs distances parcourues s'additionnent.\n\n"
        f"Chaque cycliste parcourt {km(trajet)} km pour rejoindre un parc, "
        "puis suit le même trajet au retour.\n\n"
        f"Dans le parc, chacun effectue {nb_boucles} boucles "
        f"de {km(boucle)} km.\n\n"
        f"En additionnant les distances de tous les cyclistes, "
        f"le groupe veut parcourir au moins {km(objectif_collectif)} km.\n\n"
        "Après ce parcours, chaque cycliste peut effectuer le même nombre "
        f"de petits tours supplémentaires de {km(petit_tour)} km chacun.\n\n"
        "**Questions**\n\n"
        "1. Quelle distance représente l'aller-retour entre le départ et le parc "
        "pour un cycliste ?\n\n"
        "2. Quelle distance le groupe a-t-il parcourue au total, "
        "en additionnant les distances de tous les cyclistes ?\n\n"
        "3. Quelle distance manque-t-il au groupe pour atteindre son objectif ?\n\n"
        "4. Combien de petits tours supplémentaires chaque cycliste "
        "doit-il effectuer au minimum pour atteindre l'objectif du groupe ?"
    )

    correction = (
        "**1. Aller-retour pour un cycliste**\n\n"
        f"2 × {km(trajet)} = {km(aller_retour)} km.\n\n"
        "**2. Distance cumulée par le groupe**\n\n"
        f"Chaque cycliste parcourt {km(aller_retour)} + "
        f"{nb_boucles} × {km(boucle)} = {km(distance_individuelle)} km.\n\n"
        f"Les {nb_cyclistes} cyclistes parcourent au total "
        f"{nb_cyclistes} × {km(distance_individuelle)} = "
        f"{km(distance_collective)} km.\n\n"
        "**3. Distance manquante pour le groupe**\n\n"
        f"{km(objectif_collectif)} − {km(distance_collective)} "
        f"= {km(manque_collectif)} km.\n\n"
        "**4. Nombre minimal de petits tours par cycliste**\n\n"
        f"Puisque les {nb_cyclistes} cyclistes effectueront le même nombre "
        f"de tours, il manque {km(manque_collectif)} ÷ "
        f"{nb_cyclistes} = {km(manque_par_cycliste)} km par cycliste.\n\n"
        "**Division avec quotient entier et reste :**\n\n"
        f"{km(manque_par_cycliste)} ÷ {km(petit_tour)} : "
        f"quotient entier {quotient} ; reste {km(reste)} km.\n\n"
        f"Vérification : {km(manque_par_cycliste)} = "
        f"{km(petit_tour)} × {quotient} + {km(reste)}.\n\n"
        + (
            f"Après {quotient} tour{'s' if quotient > 1 else ''} par cycliste, "
            f"il manque encore {km(reste)} km à chacun. "
            "Un tour supplémentaire est nécessaire.\n\n"
            if reste else
            f"Le reste est nul : les {quotient} tours calculés suffisent, "
            "sans ajouter de tour au quotient.\n\n"
        )
        + f"**Réponse :** Chaque cycliste doit effectuer au minimum "
          f"{tours} petit{'s' if tours > 1 else ''} "
          f"tour{'s' if tours > 1 else ''}."
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M05",
        "titre": "Le rallye à vélo",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Aller-retour d'un cycliste", "type": "nombre", "attendu": aller_retour / 10, "unite": "km"},
            {"id": "r2", "question": 2, "libelle": "Distance cumulée du groupe", "type": "nombre", "attendu": distance_collective / 10, "unite": "km"},
            {"id": "r3", "question": 3, "libelle": "Distance manquante du groupe", "type": "nombre", "attendu": manque_collectif / 10, "unite": "km"},
            {"id": "r4", "question": 4, "libelle": "Petits tours par cycliste", "type": "nombre", "attendu": tours, "unite": "tours"},
        ],
    })

def generer_modele_p7_fete():
    # Stock initial plus varié, sans dépasser les montants plausibles
    # pour un club scolaire.
    caisse = random.randint(160, 340)

    eleves = random.randint(14, 22)
    parents = random.randint(8, 14)

    prix_eleve = random.randint(5, 8)
    prix_parent = random.randint(9, 12)

    salle = random.randint(70, 110)
    decoration = random.randint(20, 45)
    prix_badge = random.randint(1, 3)

    participants = eleves + parents

    recettes = eleves * prix_eleve + parents * prix_parent

    cout_badges = participants * prix_badge
    depenses = salle + decoration + cout_badges

    restant = caisse + recettes - depenses

    # L'ancien tirage indépendant de la réserve donnait presque toujours
    # « Oui ». Équilibrer les situations sans limiter l'écart final à
    # quelques réponses : la réserve reste positive et plausible.
    if random.choice((True, False)):
        reserve_minimale = restant - random.randint(8, min(115, restant - 60))
    else:
        reserve_minimale = restant + random.randint(8, 125)

    objectif_atteint = (
        "Oui" if restant >= reserve_minimale else "Non"
    )

    enonce = (
        "**La fête du collège**\n\n"
        f"Le club de théâtre possède déjà {caisse} € "
        "dans sa caisse.\n\n"
        "Pour organiser une fête, il vend :\n"
        f"- {eleves} billets élèves à {prix_eleve} € chacun ;\n"
        f"- {parents} billets parents à {prix_parent} € chacun.\n\n"
        "Pour cette fête, le club doit payer :\n"
        f"- {salle} € pour la salle ;\n"
        f"- {decoration} € pour les décorations ;\n"
        f"- {prix_badge} € par participant pour un badge.\n\n"
        "Chaque personne ayant acheté un billet "
        "reçoit un badge.\n\n"
        "Le club souhaite conserver au moins "
        f"{reserve_minimale} € pour un prochain projet.\n\n"
        "**Questions**\n\n"
        "1. Quel est le montant total des recettes ?\n\n"
        "2. Quel est le montant total des dépenses ?\n\n"
        "3. Combien reste-t-il dans la caisse ? "
        "Le club peut-il conserver la somme souhaitée ? "
        "Justifie par une expression numérique."
    )

    correction = (
        "**1. Recettes de la fête**\n\n"
        f"Billets élèves : {eleves} × {prix_eleve} "
        f"= {eleves * prix_eleve} €.\n\n"
        f"Billets parents : {parents} × {prix_parent} "
        f"= {parents * prix_parent} €.\n\n"
        f"Recettes totales : {recettes} €.\n\n"

        "**2. Dépenses de la fête**\n\n"
        f"Participants : {eleves} + {parents} "
        f"= {participants}.\n\n"
        f"Badges : {participants} × {prix_badge} "
        f"= {cout_badges} €.\n\n"
        f"Dépenses totales : {salle} + {decoration} "
        f"+ {cout_badges} = {depenses} €.\n\n"

        "**3. Argent restant**\n\n"
        f"{caisse} + {recettes} - {depenses} "
        f"= {restant} €.\n\n"

        "**Expression complète :**\n\n"
        f"{caisse} + ({eleves} × {prix_eleve} + "
        f"{parents} × {prix_parent}) "
        f"- ({salle} + {decoration} + "
        f"({eleves} + {parents}) × {prix_badge}) "
        f"= {restant} €.\n\n"

        f"Le club souhaite conserver au moins "
        f"{reserve_minimale} €.\n\n"
        f"Il lui reste {restant} €.\n\n"
        f"**Objectif atteint : {objectif_atteint}.**"
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M06",
        "titre": "La fête du collège",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Recettes totales",
                "type": "nombre",
                "attendu": recettes,
                "unite": "€"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Dépenses totales",
                "type": "nombre",
                "attendu": depenses,
                "unite": "€"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Argent restant",
                "type": "nombre",
                "attendu": restant,
                "unite": "€"
            },
            {
                "id": "choix",
                "question": 3,
                "libelle": "Le club atteint-il son objectif ?",
                "type": "choix",
                "attendu": objectif_atteint,
                "options": ["Oui", "Non"]
            },
            {
                "id": "expression",
                "question": 3,
                "libelle": "Mon expression et ma justification",
                "type": "texte_libre"
            }
        ]
    })

def generer_modele_p7_cartes():
    """Achats, échanges et division entière pour compléter l'album."""

    cartes_depart = random.randint(65, 110)
    paquets = random.randint(5, 9)
    cartes_paquet = random.choice([6, 8])
    cartes_achetees = paquets * cartes_paquet

    # Un nombre pair de doublons permet réellement de tous les échanger par 2.
    doublons = random.choice([8, 10, 12, 14, 16, 18, 20])
    nouvelles_apres_achats = cartes_achetees - doublons
    cartes_echangees = doublons // 2
    cartes_ajoutees = nouvelles_apres_achats + cartes_echangees
    total_collection = cartes_depart + cartes_ajoutees

    capacites_possibles = (160, 180, 200, 220, 240, 260, 280)
    capacites_valides = [
        capacite for capacite in capacites_possibles
        if 15 <= capacite - total_collection <= 100
    ]
    if not capacites_valides:
        raise ValueError("Aucune capacité d'album adaptée au tirage")
    capacite_album = random.choice(capacites_valides)
    emplacements_vides = capacite_album - total_collection

    cartes_par_lot = random.choice([n for n in (5, 6, 8, 10, 12)
                                    if emplacements_vides % n != 0])
    quotient, reste = divmod(emplacements_vides, cartes_par_lot)
    lots_necessaires = quotient + (1 if reste else 0)

    enonce = (
        "**Une collection de cartes**\n\n"
        f"Un collégien possède déjà {cartes_depart} cartes différentes dans son album.\n\n"
        f"Il achète {paquets} paquets de {cartes_paquet} cartes chacun.\n\n"
        f"Parmi les cartes achetées, {doublons} sont des doublons "
        "(il les possède déjà dans son album).\n\n"
        "Il échange ensuite **tous ses doublons** avec un ami : "
        "pour **2 doublons donnés**, il reçoit **1 nouvelle carte** "
        "qu'il ne possède pas encore.\n\n"
        f"Son album contient {capacite_album} emplacements. "
        "Pour le compléter, il peut aussi acheter des lots de "
        f"{cartes_par_lot} cartes. "
        "Toutes les cartes de ces lots sont garanties différentes "
        "et absentes de son album.\n\n"
        "**Questions**\n\n"
        "1. Combien de cartes achète-t-il ?\n\n"
        "2. Combien de nouvelles cartes ajoute-t-il à son album grâce "
        "aux achats et aux échanges ?\n\n"
        "3. Combien d'emplacements restent vides dans son album "
        "après les achats et les échanges ?\n\n"
        "4. Combien de lots supplémentaires doit-il acheter au minimum "
        "pour obtenir assez de nouvelles cartes et remplir son album ?"
    )

    correction = (
        "**1. Cartes achetées**\n\n"
        f"{paquets} × {cartes_paquet} = {cartes_achetees} cartes.\n\n"
        "**2. Cartes ajoutées grâce aux achats et aux échanges**\n\n"
        f"Les cartes non doublons : {cartes_achetees} − {doublons} "
        f"= {nouvelles_apres_achats} cartes.\n\n"
        f"Les échanges : {doublons} ÷ 2 = {cartes_echangees} nouvelles cartes.\n\n"
        f"Il ajoute donc {nouvelles_apres_achats} + {cartes_echangees} "
        f"= {cartes_ajoutees} cartes à son album.\n\n"
        "**3. Emplacements encore vides**\n\n"
        f"Après les achats et les échanges, il possède "
        f"{cartes_depart} + {cartes_ajoutees} = {total_collection} cartes.\n\n"
        f"Il reste {capacite_album} − {total_collection} "
        f"= {emplacements_vides} emplacements vides.\n\n"
        "**4. Nombre minimal de lots supplémentaires**\n\n"
        "Division avec quotient entier et reste :\n\n"
        f"{emplacements_vides} : {cartes_par_lot} → "
        f"quotient {quotient}, reste {reste}.\n\n"
        + (
            f"Après {quotient} lots, il manque encore {reste} cartes. "
            "Un dernier lot est donc nécessaire.\n\n"
            if reste else
            f"Le reste est nul : {quotient} lots suffisent.\n\n"
        )
        + f"**Réponse :** Il faut au minimum {lots_necessaires} "
          f"lot{'s' if lots_necessaires > 1 else ''} supplémentaires. "
          "Les cartes en trop, s'il y en a, "
          "restent hors de l'album."
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M07",
        "titre": "Une collection de cartes",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Cartes achetées", "type": "nombre", "attendu": cartes_achetees, "unite": "cartes"},
            {"id": "r2", "question": 2, "libelle": "Cartes ajoutées à l'album", "type": "nombre", "attendu": cartes_ajoutees, "unite": "cartes"},
            {"id": "r3", "question": 3, "libelle": "Emplacements encore vides", "type": "nombre", "attendu": emplacements_vides, "unite": "emplacements"},
            {"id": "r4", "question": 4, "libelle": "Lots supplémentaires nécessaires", "type": "nombre", "attendu": lots_necessaires, "unite": "lots"},
        ],
    })

def generer_modele_p7_badminton():

    while True:
        stock_initial = random.randint(9, 21)
        nb_boites = random.randint(4, 7)
        volants_par_boite = 12
        volants_abimes = random.randint(6, 18)

        nb_matchs = random.randint(6, 10)
        volants_par_match = random.randint(7, 11)

        volants_achetes = nb_boites * volants_par_boite

        volants_utilisables = (
            stock_initial + volants_achetes - volants_abimes
        )

        volants_necessaires = nb_matchs * volants_par_match

        ecart = abs(volants_utilisables - volants_necessaires)

        if ecart >= 3:
            break

    suffisant = (
        "Oui" if volants_utilisables >= volants_necessaires
        else "Non"
    )

    if suffisant == "Oui":
        question_finale = "Combien de volants restera-t-il au club après le tournoi ?"
        conclusion = (
            f"Il restera {ecart} volants utilisables "
            "après le tournoi."
        )
        libelle_ecart = "Nombre de volants restants"
    else:
        question_finale = "Combien de volants manque-t-il au club pour tous les matchs ?"
        conclusion = (
            f"Il manque {ecart} volants pour organiser "
            "tous les matchs prévus."
        )
        libelle_ecart = "Nombre de volants manquants"

    enonce = (
        "**Le tournoi de badminton**\n\n"
        "Le collège organise un tournoi de badminton.\n\n"
        f"Le club possède déjà {stock_initial} volants.\n\n"
        f"Il achète {nb_boites} boîtes de "
        f"{volants_par_boite} volants chacune.\n\n"
        f"Lors de la vérification du matériel, "
        f"{volants_abimes} volants sont déclarés "
        "abîmés et ne peuvent pas être utilisés.\n\n"
        f"Le tournoi comporte {nb_matchs} matchs. "
        f"Le club prévoit d'utiliser {volants_par_match} "
        "volants pour chacun de ces matchs.\n\n"
        "**Questions**\n\n"
        "1. Combien de volants le club a-t-il achetés ?\n\n"
        "2. Combien de volants utilisables possède-t-il "
        "après avoir retiré les volants abîmés ?\n\n"
        "3. Combien de volants faut-il prévoir "
        "pour tous les matchs ?\n\n"
        f"4. {question_finale}"
    )

    correction = (
        "**1. Volants achetés**\n\n"
        f"{nb_boites} × {volants_par_boite} "
        f"= {volants_achetes} volants.\n\n"

        "**2. Volants utilisables**\n\n"
        f"{stock_initial} + {volants_achetes} "
        f"− {volants_abimes} "
        f"= {volants_utilisables} volants.\n\n"

        "**3. Volants nécessaires**\n\n"
        f"{nb_matchs} × {volants_par_match} "
        f"= {volants_necessaires} volants.\n\n"

        "**4. Vérification des quantités**\n\n"
        f"Volants disponibles : {volants_utilisables}.\n\n"
        f"Volants nécessaires : {volants_necessaires}.\n\n"
        f"Différence : {ecart} volants.\n\n"
        f"**Le stock est-il suffisant ? {suffisant}.**\n\n"
        f"{conclusion}"
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M08",
        "titre": "Le tournoi de badminton",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Volants achetés",
                "type": "nombre",
                "attendu": volants_achetes,
                "unite": "volants"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Volants utilisables",
                "type": "nombre",
                "attendu": volants_utilisables,
                "unite": "volants"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Volants nécessaires",
                "type": "nombre",
                "attendu": volants_necessaires,
                "unite": "volants"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Le stock est-il suffisant ?",
                "type": "choix",
                "attendu": suffisant,
                "options": ["Oui", "Non"]
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": libelle_ecart,
                "type": "nombre",
                "attendu": ecart,
                "unite": "volants"
            }
        ]
    })

def generer_modele_p7_jeu_video():

    univers = random.choice([
        "le royaume des cristaux",
        "l'île des robots",
        "le labyrinthe des dragons"
    ])

    pieces_depart = random.randint(80, 135)
    niveaux = random.randint(3, 5)
    pieces_par_niveau = random.randint(17, 29)
    bonus = random.randint(10, 24)

    potions = random.randint(2, 3)
    prix_potion = random.randint(15, 25)
    pieces_perdues = random.randint(8, 23)

    gains = niveaux * pieces_par_niveau + bonus
    cout_potions = potions * prix_potion
    depenses_et_pertes = cout_potions + pieces_perdues

    solde = pieces_depart + gains - depenses_et_pertes

    # Les écarts étaient limités à 10, 20 ou 30 pièces.
    # Désormais : écarts variés, prix positif et achat possible / impossible
    # dans des proportions équilibrées. Les quatre réponses restent entières.
    if random.choice((True, False)):
        variation_prix = -random.randint(7, min(85, solde - 20))
    else:
        variation_prix = random.randint(7, 95)
    prix_equipement = solde + variation_prix

    achat_possible = "Oui" if solde >= prix_equipement else "Non"
    difference = abs(solde - prix_equipement)

    if achat_possible == "Oui":
        libelle_difference = "Pièces restantes après l'achat"
        conclusion = (
            f"Le joueur peut acheter l'équipement. "
            f"Il lui restera {difference} pièces."
        )
    else:
        libelle_difference = "Pièces manquantes"
        conclusion = (
            f"Le joueur ne peut pas acheter l'équipement. "
            f"Il lui manque {difference} pièces."
        )

    enonce = (
        "**Une aventure en jeu vidéo**\n\n"
        f"Dans le jeu vidéo « {univers} », "
        "un joueur possède au départ "
        f"{pieces_depart} pièces d'or.\n\n"
        f"Il termine {niveaux} niveaux et gagne "
        f"{pieces_par_niveau} pièces à chaque niveau.\n\n"
        f"Il reçoit également un bonus unique de "
        f"{bonus} pièces.\n\n"
        "Pendant son aventure :\n"
        f"- il achète {potions} potions à "
        f"{prix_potion} pièces chacune ;\n"
        f"- il perd {pieces_perdues} pièces "
        "dans un piège.\n\n"
        "À la fin, il découvre un équipement spécial "
        f"vendu {prix_equipement} pièces.\n\n"
        "**Questions**\n\n"
        "1. Combien de pièces gagne-t-il au total, "
        "bonus compris ?\n\n"
        "2. Combien de pièces dépense-t-il ou "
        "perd-il pendant son aventure ?\n\n"
        "3. Combien de pièces lui reste-t-il "
        "avant l'achat de l'équipement spécial ?\n\n"
        "4. Peut-il acheter cet équipement ? "
        "Combien de pièces lui restera-t-il "
        "ou combien lui en manquera-t-il ?"
    )

    correction = (
        "**1. Pièces gagnées**\n\n"
        f"{niveaux} × {pieces_par_niveau} + {bonus} "
        f"= {gains} pièces.\n\n"

        "**2. Dépenses et pertes**\n\n"
        f"Potions : {potions} × {prix_potion} "
        f"= {cout_potions} pièces.\n\n"
        f"Total dépensé ou perdu : "
        f"{cout_potions} + {pieces_perdues} "
        f"= {depenses_et_pertes} pièces.\n\n"

        "**3. Pièces restantes**\n\n"
        f"{pieces_depart} + {gains} "
        f"− {depenses_et_pertes} "
        f"= {solde} pièces.\n\n"
        "**Expression complète :**\n\n"
        f"{pieces_depart} + "
        f"({niveaux} × {pieces_par_niveau} + {bonus}) "
        f"− ({potions} × {prix_potion} "
        f"+ {pieces_perdues}) "
        f"= {solde}.\n\n"

        "**4. Achat de l'équipement**\n\n"
        f"Pièces disponibles : {solde}.\n\n"
        f"Prix de l'équipement : {prix_equipement}.\n\n"
        f"Différence : {difference} pièces.\n\n"
        f"**Achat possible : {achat_possible}.**\n\n"
        f"{conclusion}"
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M09",
        "titre": "Une aventure en jeu vidéo",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Total des pièces gagnées",
                "type": "nombre",
                "attendu": gains,
                "unite": "pièces"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Pièces dépensées ou perdues",
                "type": "nombre",
                "attendu": depenses_et_pertes,
                "unite": "pièces"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Pièces restantes avant l'achat",
                "type": "nombre",
                "attendu": solde,
                "unite": "pièces"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Achat possible ?",
                "type": "choix",
                "attendu": achat_possible,
                "options": ["Oui", "Non"]
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": libelle_difference,
                "type": "nombre",
                "attendu": difference,
                "unite": "pièces"
            }
        ]
    })

def generer_modele_p7_dessin():

    while True:
        feuilles_depart = random.randint(20, 55)
        nb_paquets = random.randint(3, 6)
        feuilles_par_paquet = random.choice([20, 25, 30])

        nb_groupes = random.randint(4, 8)
        eleves_par_groupe = random.randint(3, 5)
        feuilles_par_eleve = random.randint(2, 4)

        feuilles_abimees = random.randint(5, 13)

        feuilles_achetees = nb_paquets * feuilles_par_paquet

        feuilles_utilisees = (
            nb_groupes * eleves_par_groupe * feuilles_par_eleve
        )

        feuilles_restantes = (
            feuilles_depart
            + feuilles_achetees
            - feuilles_abimees
            - feuilles_utilisees
        )

        if 20 <= feuilles_restantes <= 90:
            break

    # Anciennement : réponse finale toujours égale à 8 ou 12 feuilles.
    # Choisir un déficit ou un surplus plausible, avec davantage de valeurs.
    if random.choice((True, False)):
        variation = -random.randint(4, min(55, feuilles_restantes - 3))
    else:
        variation = random.randint(4, 65)
    feuilles_exposition = feuilles_restantes + variation

    suffisant = (
        "Oui" if feuilles_restantes >= feuilles_exposition
        else "Non"
    )

    difference = abs(feuilles_restantes - feuilles_exposition)

    if suffisant == "Oui":
        libelle_difference = "Feuilles restantes après l'exposition"
        conclusion = (
            f"Le club dispose de suffisamment de feuilles. "
            f"Il lui en restera {difference}."
        )
    else:
        libelle_difference = "Feuilles manquantes"
        conclusion = (
            f"Le club ne dispose pas de suffisamment de feuilles. "
            f"Il lui en manque {difference}."
        )

    enonce = (
        "**L'atelier de dessin**\n\n"
        "Le club de dessin du collège prépare un atelier.\n\n"
        f"Il possède déjà {feuilles_depart} feuilles de papier.\n\n"
        f"Il achète {nb_paquets} paquets contenant chacun "
        f"{feuilles_par_paquet} feuilles.\n\n"
        f"Avant l'atelier, {feuilles_abimees} feuilles "
        "sont abîmées et ne peuvent plus être utilisées.\n\n"
        f"Pendant l'atelier, {nb_groupes} groupes participent.\n"
        f"Chaque groupe compte {eleves_par_groupe} élèves.\n"
        f"Chaque élève utilise {feuilles_par_eleve} feuilles.\n\n"
        "Après l'atelier, le club souhaite préparer une exposition "
        f"pour laquelle il faudra {feuilles_exposition} feuilles.\n\n"
        "**Questions**\n\n"
        "1. Combien de feuilles le club a-t-il achetées ?\n\n"
        "2. Combien de feuilles les élèves utilisent-ils "
        "pendant l'atelier ?\n\n"
        "3. Combien de feuilles restent disponibles "
        "après l'atelier ?\n\n"
        "4. Le club possède-t-il suffisamment de feuilles "
        "pour préparer l'exposition ? "
        "Combien lui en restera-t-il ou combien "
        "lui en manquera-t-il ?"
    )

    correction = (
        "**1. Feuilles achetées**\n\n"
        f"{nb_paquets} × {feuilles_par_paquet} "
        f"= {feuilles_achetees} feuilles.\n\n"

        "**2. Feuilles utilisées pendant l'atelier**\n\n"
        f"Nombre d'élèves : {nb_groupes} × "
        f"{eleves_par_groupe} "
        f"= {nb_groupes * eleves_par_groupe}.\n\n"
        f"Feuilles utilisées : "
        f"{nb_groupes * eleves_par_groupe} × "
        f"{feuilles_par_eleve} "
        f"= {feuilles_utilisees} feuilles.\n\n"

        "**3. Feuilles restantes**\n\n"
        f"Stock initial : {feuilles_depart} feuilles.\n\n"
        f"Feuilles achetées : {feuilles_achetees}.\n\n"
        f"Feuilles abîmées : {feuilles_abimees}.\n\n"
        f"Feuilles utilisées : {feuilles_utilisees}.\n\n"
        f"{feuilles_depart} + {feuilles_achetees} "
        f"− {feuilles_abimees} "
        f"− {feuilles_utilisees} "
        f"= {feuilles_restantes} feuilles.\n\n"

        "**4. Préparation de l'exposition**\n\n"
        f"Feuilles disponibles : {feuilles_restantes}.\n\n"
        f"Feuilles nécessaires : {feuilles_exposition}.\n\n"
        f"Différence : {difference} feuilles.\n\n"
        f"**Stock suffisant : {suffisant}.**\n\n"
        f"{conclusion}"
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M10",
        "titre": "L'atelier de dessin",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Feuilles achetées",
                "type": "nombre",
                "attendu": feuilles_achetees,
                "unite": "feuilles"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Feuilles utilisées",
                "type": "nombre",
                "attendu": feuilles_utilisees,
                "unite": "feuilles"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Feuilles restantes après l'atelier",
                "type": "nombre",
                "attendu": feuilles_restantes,
                "unite": "feuilles"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Stock suffisant pour l'exposition ?",
                "type": "choix",
                "attendu": suffisant,
                "options": ["Oui", "Non"]
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": libelle_difference,
                "type": "nombre",
                "attendu": difference,
                "unite": "feuilles"
            }
        ]
    })

def generer_modele_p7_tables_dessin():

    nb_tables = random.randint(3, 6)
    eleves_par_table = random.randint(4, 7)
    feuilles_par_eleve = random.randint(2, 4)
    feuilles_essai = random.randint(1, 3)

    feuilles_par_table = (
        eleves_par_table * feuilles_par_eleve
        + feuilles_essai
    )

    feuilles_necessaires = nb_tables * feuilles_par_table

    feuilles_restantes = random.randint(12, 40)
    stock_initial = feuilles_necessaires + feuilles_restantes

    enonce = (
        "**Les tables de dessin**\n\n"
        "Le collège organise un atelier de dessin "
        f"avec {nb_tables} tables de "
        f"{eleves_par_table} élèves chacune.\n\n"

        "Le professeur prévoit :\n"
        f"- {feuilles_par_eleve} feuilles de papier "
        "pour chaque élève ;\n"
        f"- {feuilles_essai} "
        f"feuille{'s' if feuilles_essai > 1 else ''} "
        f"supplémentaire{'s' if feuilles_essai > 1 else ''} "
        "par table pour faire des essais.\n\n"

        f"Le professeur dispose de {stock_initial} "
        "feuilles au départ.\n\n"

        "**Questions**\n\n"
        f"1. Combien de feuilles faut-il pour une table "
        f"de {eleves_par_table} élèves, en comptant "
        "les feuilles d'essai ?\n\n"

        f"2. Combien de feuilles faut-il pour "
        f"les {nb_tables} tables ?\n\n"

        "3. Combien de feuilles restera-t-il "
        "au professeur ? Écris une seule expression "
        "numérique avec des parenthèses."
    )

    correction = (
        "**1. Feuilles nécessaires pour une table**\n\n"
        f"{eleves_par_table} × {feuilles_par_eleve} "
        f"+ {feuilles_essai} "
        f"= {feuilles_par_table} feuilles.\n\n"

        "**2. Feuilles nécessaires pour toutes les tables**\n\n"
        f"{nb_tables} × {feuilles_par_table} "
        f"= {feuilles_necessaires} feuilles.\n\n"

        "**3. Feuilles restantes**\n\n"
        f"{stock_initial} − {feuilles_necessaires} "
        f"= {feuilles_restantes} feuilles.\n\n"

        "**Expression complète avec parenthèses :**\n\n"
        f"{stock_initial} − {nb_tables} × "
        f"({eleves_par_table} × {feuilles_par_eleve} "
        f"+ {feuilles_essai}) "
        f"= {feuilles_restantes}.\n\n"

        f"**Réponse :** Il restera "
        f"{feuilles_restantes} feuilles au professeur."
    )

    return _mc_uniformiser_exercice({
        "id": "P7-M11",
        "titre": "Les tables de dessin",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Feuilles nécessaires par table",
                "type": "nombre",
                "attendu": feuilles_par_table,
                "unite": "feuilles"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Feuilles nécessaires au total",
                "type": "nombre",
                "attendu": feuilles_necessaires,
                "unite": "feuilles"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Feuilles restantes",
                "type": "nombre",
                "attendu": feuilles_restantes,
                "unite": "feuilles"
            },
            {
                "id": "expression",
                "question": 3,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            }
        ]
    })

# ---------------------------------------------------------------
# MathiCap : nouveaux modèles N7 (P7-M12 à P7-M16).
# Même contrat de champs et de correction que les modèles existants.
# ---------------------------------------------------------------

def generer_modele_p7_planetarium():
    classes = random.randint(2, 4)
    eleves_classe = random.randint(22, 30)
    accompagnateurs = random.randint(3, 7)
    places_car = random.choice([40, 48, 52, 55])
    prix_eleve = random.randint(8, 15)
    prix_adulte = random.randint(12, 19)
    cout_car = random.randint(180, 330)

    eleves = classes * eleves_classe
    personnes = eleves + accompagnateurs
    cars, reste = divmod(personnes, places_car)
    cars += int(reste > 0)
    billets = eleves * prix_eleve + accompagnateurs * prix_adulte
    cout_total = billets + cars * cout_car
    ecart = random.randint(24, 195)
    budget_suffisant = random.choice([True, False])
    budget = cout_total + ecart if budget_suffisant else cout_total - ecart
    assert budget > 0
    question_finale = (
        "Quelle somme restera-t-il dans le budget après avoir payé les billets et les cars ?"
        if budget_suffisant else
        "Combien d'euros manque-t-il pour financer les billets et les cars ?"
    )
    conclusion = (
        f"Il restera {ecart} € dans le budget."
        if budget_suffisant else
        f"Il manquera {ecart} € pour financer la sortie."
    )
    enonce = (
        "**La sortie au planétarium**\n\n"
        f"Le collège organise une sortie avec {classes} classes de {eleves_classe} élèves chacune "
        f"et {accompagnateurs} adultes accompagnateurs.\n\n"
        f"Un car peut transporter au maximum {places_car} personnes et coûte {cout_car} €.\n\n"
        f"L'entrée coûte {prix_eleve} € par élève et {prix_adulte} € par adulte. "
        f"Le collège dispose d'un budget de {budget} € pour les transports et les entrées.\n\n"
        "**Questions**\n\n"
        "1. Combien de personnes participeront à la sortie ?\n\n"
        "2. Combien de cars sont nécessaires au minimum ?\n\n"
        "3. Quel sera le coût de tous les billets d'entrée ?\n\n"
        f"4. {question_finale}"
    )
    correction = (
        "**1. Participants**\n\n"
        f"{classes} × {eleves_classe} + {accompagnateurs} = {personnes} personnes.\n\n"
        "**2. Nombre de cars**\n\n"
        f"{personnes} ÷ {places_car} : quotient entier {personnes // places_car}, "
        f"reste {personnes % places_car}.\n"
        f"Il faut {cars} cars pour transporter tout le monde.\n\n"
        "**3. Billets d'entrée**\n\n"
        f"{eleves} × {prix_eleve} + {accompagnateurs} × {prix_adulte} "
        f"= {billets} €.\n\n"
        "**4. Bilan du budget**\n\n"
        f"Transport : {cars} × {cout_car} = {cars * cout_car} €.\n"
        f"Total à payer : {billets} + {cars * cout_car} = {cout_total} €.\n"
        f"Budget : {budget} €.\n"
        f"Différence : {ecart} €. {conclusion}"
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M12", "titre": "La sortie au planétarium",
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "mathicap_budget_suffisant": budget_suffisant,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Participants", "type": "nombre", "attendu": personnes, "unite": "personnes"},
            {"id": "r2", "question": 2, "libelle": "Cars nécessaires", "type": "nombre", "attendu": cars, "unite": "cars"},
            {"id": "r3", "question": 3, "libelle": "Coût des billets", "type": "nombre", "attendu": billets, "unite": "€"},
            {"id": "r4", "question": 4, "libelle": "Écart avec le budget", "type": "nombre", "attendu": ecart, "unite": "€"},
        ],
    })


def generer_modele_p7_robotique():
    """N7 : une seule catégorie de matériel manque pour l'objectif."""
    objectif = random.randint(8, 17)
    type_manquant = random.choice(("moteurs", "batteries"))
    manque = random.randint(2, 9)
    # Génération explicite : une ressource strictement insuffisante,
    # la seconde suffisante, éventuellement exactement.
    if type_manquant == "moteurs":
        moteurs_utilisables = 2 * objectif - manque
        batteries_utilisables = 3 * objectif + random.randint(0, 12)
    else:
        moteurs_utilisables = 2 * objectif + random.randint(0, 8)
        batteries_utilisables = 3 * objectif - manque
    moteurs_abimes = random.randint(2, 10)
    batteries_abimees = random.randint(2, 12)
    moteurs = moteurs_utilisables + moteurs_abimes
    batteries = batteries_utilisables + batteries_abimees
    robots = min(moteurs_utilisables // 2, batteries_utilisables // 3)
    manque_moteurs = max(0, 2 * objectif - moteurs_utilisables)
    manque_batteries = max(0, 3 * objectif - batteries_utilisables)
    robots_restants = objectif - robots
    moteurs_restants = moteurs_utilisables - 2 * robots
    batteries_restantes = batteries_utilisables - 3 * robots
    besoin_moteurs_restants = 2 * robots_restants
    besoin_batteries_restantes = 3 * robots_restants
    assert max(0, besoin_moteurs_restants - moteurs_restants) == manque_moteurs
    assert max(0, besoin_batteries_restantes - batteries_restantes) == manque_batteries
    assert (manque_moteurs > 0) != (manque_batteries > 0)
    assert manque_moteurs + manque_batteries == manque
    assert robots < objectif
    texte_moteurs_a_acheter = (
        f"- Moteurs : {besoin_moteurs_restants} nécessaires, {moteurs_restants} disponibles. "
        f"Il manque {besoin_moteurs_restants} − {moteurs_restants} = "
        f"**{manque_moteurs} moteurs**.\n"
        if manque_moteurs else
        f"- Moteurs : {besoin_moteurs_restants} nécessaires, {moteurs_restants} disponibles. "
        "Il n'en manque aucun.\n"
    )
    texte_batteries_a_acheter = (
        f"- Batteries : {besoin_batteries_restantes} nécessaires, {batteries_restantes} disponibles. "
        f"Il manque {besoin_batteries_restantes} − {batteries_restantes} = "
        f"**{manque_batteries} batteries**.\n"
        if manque_batteries else
        f"- Batteries : {besoin_batteries_restantes} nécessaires, {batteries_restantes} disponibles. "
        "Il n'en manque aucune.\n"
    )

    enonce = (
        "**Le club de robotique**\n\n"
        "Pour une démonstration, le club assemble des robots. "
        "Chaque robot nécessite 2 moteurs et 3 batteries.\n\n"
        f"Le club possède {moteurs} moteurs, dont {moteurs_abimes} hors d'usage, "
        f"et {batteries} batteries, dont {batteries_abimees} défectueuses.\n\n"
        f"Il souhaite fabriquer {objectif} robots. "
        "Pour atteindre cet objectif, une seule des deux ressources lui manque.\n\n"
        "**Questions**\n\n"
        "1. Combien de moteurs utilisables le club possède-t-il ?\n\n"
        "2. Combien de batteries utilisables possède-t-il ?\n\n"
        "3. Combien de robots complets peut-il assembler avec son matériel ?\n\n"
        "4. Combien de moteurs ou de batteries supplémentaires "
        "lui manque-t-il pour fabriquer le nombre de robots souhaité ?"
    )
    correction = (
        "**1. Moteurs utilisables**\n\n"
        f"{moteurs} − {moteurs_abimes} = {moteurs_utilisables} moteurs.\n\n"
        "**2. Batteries utilisables**\n\n"
        f"{batteries} − {batteries_abimees} = {batteries_utilisables} batteries.\n\n"
        "**3. Robots réalisables**\n\n"
        f"Avec les moteurs : {moteurs_utilisables} ÷ 2, soit "
        f"{moteurs_utilisables // 2} robots complets.\n"
        f"Avec les batteries : {batteries_utilisables} ÷ 3, soit "
        f"{batteries_utilisables // 3} robots complets.\n"
        f"On retient le plus petit nombre : {robots} robots.\n\n"
        "**4. Matériel manquant pour atteindre l'objectif**\n\n"
        f"Le club peut assembler {robots} robots, mais souhaite en fabriquer "
        f"{objectif}. Il manque donc {objectif} − {robots} = "
        f"**{robots_restants} robots** à fabriquer.\n\n"
        "Après fabrication des robots possibles avec le stock actuel :\n"
        f"- Moteurs restants : {moteurs_utilisables} − "
        f"({robots} × 2) = {moteurs_restants} moteurs.\n"
        f"- Batteries restantes : {batteries_utilisables} − "
        f"({robots} × 3) = {batteries_restantes} batteries.\n\n"
        f"Pour les {robots_restants} robots encore à fabriquer, il faut "
        f"{robots_restants} × 2 = {besoin_moteurs_restants} moteurs et "
        f"{robots_restants} × 3 = {besoin_batteries_restantes} batteries.\n\n"
        + texte_moteurs_a_acheter
        + texte_batteries_a_acheter
        + "\n"
        f"**Conclusion : il faut acheter {manque} {type_manquant} "
        "supplémentaires.**"
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M13", "titre": "Le club de robotique",
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Moteurs utilisables", "type": "nombre", "attendu": moteurs_utilisables, "unite": "moteurs"},
            {"id": "r2", "question": 2, "libelle": "Batteries utilisables", "type": "nombre", "attendu": batteries_utilisables, "unite": "batteries"},
            {"id": "r3", "question": 3, "libelle": "Robots réalisables", "type": "nombre", "attendu": robots, "unite": "robots"},
            {"id": "r4", "question": 4, "libelle": "Moteurs ou batteries manquants", "type": "nombre", "attendu": manque, "unite": type_manquant},
        ],
    })

def generer_modele_p7_collecte_solidaire():
    sacs = random.randint(15, 45)
    articles_par_sac = random.randint(8, 22)
    articles_abimes = random.randint(11, 48)
    capacite_carton = random.choice([10, 12, 15, 18, 20])
    cartons_par_trajet = random.randint(3, 8)

    total_articles = sacs * articles_par_sac
    articles_utilisables = total_articles - articles_abimes
    cartons, reste = divmod(articles_utilisables, capacite_carton)
    cartons += int(reste > 0)
    trajets, reste_trajets = divmod(cartons, cartons_par_trajet)
    trajets += int(reste_trajets > 0)
    enonce = (
        "**La collecte solidaire**\n\n"
        "Les élèves collectent des vêtements pour une association. "
        f"Ils réunissent {sacs} sacs contenant chacun {articles_par_sac} vêtements.\n\n"
        f"Lors du tri, {articles_abimes} vêtements ne peuvent pas être distribués.\n\n"
        f"Les autres vêtements sont rangés dans des cartons pouvant contenir "
        f"au maximum {capacite_carton} vêtements chacun. "
        "Un carton entamé doit lui aussi être transporté.\n\n"
        f"Une camionnette peut transporter au maximum {cartons_par_trajet} cartons par trajet.\n\n"
        "**Questions**\n\n"
        "1. Combien de vêtements les élèves ont-ils collectés ?\n\n"
        "2. Combien de vêtements peuvent être distribués après le tri ?\n\n"
        "3. Combien de cartons faut-il préparer au minimum ?\n\n"
        "4. Combien de trajets la camionnette doit-elle faire au minimum pour tout transporter ?"
    )
    correction = (
        "**1. Vêtements collectés**\n\n"
        f"{sacs} × {articles_par_sac} = {total_articles} vêtements.\n\n"
        "**2. Vêtements utilisables**\n\n"
        f"{total_articles} − {articles_abimes} = {articles_utilisables} vêtements.\n\n"
        "**3. Cartons nécessaires**\n\n"
        f"{articles_utilisables} ÷ {capacite_carton} : quotient entier "
        f"{articles_utilisables // capacite_carton}, "
        f"reste {articles_utilisables % capacite_carton}.\n"
        f"Il faut {cartons} cartons, y compris le dernier s'il n'est pas rempli.\n\n"
        "**4. Trajets nécessaires**\n\n"
        f"{cartons} ÷ {cartons_par_trajet} : quotient entier "
        f"{cartons // cartons_par_trajet}, reste {cartons % cartons_par_trajet}.\n"
        f"Il faut {trajets} trajets pour emporter tous les cartons."
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M14", "titre": "La collecte solidaire",
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Vêtements collectés", "type": "nombre", "attendu": total_articles, "unite": "vêtements"},
            {"id": "r2", "question": 2, "libelle": "Vêtements utilisables", "type": "nombre", "attendu": articles_utilisables, "unite": "vêtements"},
            {"id": "r3", "question": 3, "libelle": "Cartons nécessaires", "type": "nombre", "attendu": cartons, "unite": "cartons"},
            {"id": "r4", "question": 4, "libelle": "Trajets de camionnette", "type": "nombre", "attendu": trajets, "unite": "trajets"},
        ],
    })


def generer_modele_p7_repetitions():
    scenes = random.randint(4, 7)
    minutes_scene = random.randint(12, 23)
    minutes_pause = random.randint(5, 12)
    minutes_suppl = random.randint(9, 17)
    minutes_scenes = scenes * minutes_scene
    minutes_pauses = (scenes - 1) * minutes_pause
    minutes_total = minutes_scenes + minutes_pauses
    marge = random.randint(25, 105)
    minutes_creneau = minutes_total + marge
    repetitions = marge // minutes_suppl

    enonce = (
        "**Les répétitions de théâtre**\n\n"
        "Une troupe du collège répète un spectacle. "
        f"Elle travaille {scenes} scènes, pendant {minutes_scene} minutes par scène.\n\n"
        f"Elle fait une pause de {minutes_pause} minutes **entre deux scènes consécutives** "
        "(aucune pause après la dernière scène).\n\n"
        f"La salle est réservée pour {minutes_creneau} minutes. "
        f"Si du temps reste, la troupe souhaite répéter une dernière scène de "
        f"{minutes_suppl} minutes autant de fois que possible, sans pause supplémentaire.\n\n"
        "**Questions**\n\n"
        "1. Combien de minutes dure l'ensemble des premières répétitions, sans les pauses ?\n\n"
        "2. Combien de minutes durent les pauses au total ?\n\n"
        "3. Combien de minutes sont utilisées pour les scènes et les pauses ?\n\n"
        "4. Combien de fois peut-on répéter entièrement la dernière scène dans le temps restant ?"
    )
    correction = (
        "**1. Temps des premières scènes**\n\n"
        f"{scenes} × {minutes_scene} = {minutes_scenes} min.\n\n"
        "**2. Temps des pauses**\n\n"
        f"Il y a {scenes - 1} pauses, pas {scenes}. "
        f"{scenes - 1} × {minutes_pause} = {minutes_pauses} min.\n\n"
        "**3. Durée totale initiale**\n\n"
        f"{minutes_scenes} + {minutes_pauses} = {minutes_total} min.\n\n"
        "**4. Répétitions possibles dans le temps restant**\n\n"
        f"Temps disponible : {minutes_creneau} − {minutes_total} = {marge} min.\n"
        f"{marge} ÷ {minutes_suppl} : quotient entier {repetitions}, "
        f"reste {marge % minutes_suppl}.\n"
        f"La troupe peut répéter la dernière scène {repetitions} fois entièrement."
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M15", "titre": "Les répétitions de théâtre",
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Durée des scènes", "type": "nombre", "attendu": minutes_scenes, "unite": "min"},
            {"id": "r2", "question": 2, "libelle": "Durée des pauses", "type": "nombre", "attendu": minutes_pauses, "unite": "min"},
            {"id": "r3", "question": 3, "libelle": "Durée utilisée", "type": "nombre", "attendu": minutes_total, "unite": "min"},
            {"id": "r4", "question": 4, "libelle": "Répétitions supplémentaires", "type": "nombre", "attendu": repetitions, "unite": "répétitions"},
        ],
    })


def generer_modele_p7_plantations():
    """N7 : quatre étapes guidées, variantes de difficulté homogène.

    Le nombre de planches supplémentaires vaut de 1 à 4, avec un reste
    non nul. Les nouveaux tirages sont répartis équitablement entre
    ces quatre résultats, évitant les réponses quasi systématiques à 1.
    """
    cible_planches_supp = random.randint(1, 4)
    for _ in range(500):
        planches = random.randint(3, 6)
        rangs_par_planche = random.randint(3, 6)
        graines_par_rang = random.randint(7, 13)
        sachets = random.randint(5, 11)
        graines_par_sachet = random.choice([20, 25, 30, 36, 40])
        stock_initial = random.randint(12, 45)

        graines_planche = rangs_par_planche * graines_par_rang
        graines_total = planches * graines_planche
        graines_disponibles = stock_initial + sachets * graines_par_sachet
        while graines_disponibles < graines_total + graines_planche:
            sachets += 1
            graines_disponibles = stock_initial + sachets * graines_par_sachet
        graines_restantes = graines_disponibles - graines_total
        if graines_restantes % graines_planche == 0:
            stock_initial += 1
            graines_disponibles += 1
            graines_restantes += 1
        planches_supp = graines_restantes // graines_planche
        if planches_supp == cible_planches_supp:
            break
    else:
        raise ValueError("Aucun tirage cohérent pour les plantations N7")
    enonce = (
        "**Les plantations du collège**\n\n"
        f"Les élèves veulent préparer {planches} planches de culture. "
        f"Chaque planche contient {rangs_par_planche} rangs de {graines_par_rang} graines.\n\n"
        f"Le club possède déjà {stock_initial} graines et reçoit "
        f"{sachets} sachets de {graines_par_sachet} graines chacun.\n\n"
        "Après avoir semé les premières planches, le club envisage "
        "d'en préparer d'autres exactement de la même taille, sans acheter de graines.\n\n"
        "**Questions**\n\n"
        "1. Combien de graines faut-il pour les planches prévues au départ ?\n\n"
        "2. Combien de graines le club possède-t-il après avoir reçu les sachets ?\n\n"
        "3. Combien de graines restera-t-il après les premières plantations ?\n\n"
        "4. Combien de planches supplémentaires complètes pourra-t-il préparer au maximum ?"
    )
    correction = (
        "**1. Graines pour le projet initial**\n\n"
        f"{planches} × {rangs_par_planche} × {graines_par_rang} "
        f"= {graines_total} graines.\n\n"
        "**2. Stock après réception**\n\n"
        f"{stock_initial} + {sachets} × {graines_par_sachet} "
        f"= {graines_disponibles} graines.\n\n"
        "**3. Graines restantes**\n\n"
        f"{graines_disponibles} − {graines_total} = {graines_restantes} graines.\n\n"
        "**4. Planches supplémentaires possibles**\n\n"
        f"Il faut {rangs_par_planche} × {graines_par_rang} "
        f"= {graines_planche} graines par planche.\n"
        f"{graines_restantes} ÷ {graines_planche} : quotient entier {planches_supp}, "
        f"reste {graines_restantes % graines_planche}.\n"
        f"Il peut donc préparer {planches_supp} planches supplémentaires complètes."
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M16", "titre": "Les plantations du collège",
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Graines à semer", "type": "nombre", "attendu": graines_total, "unite": "graines"},
            {"id": "r2", "question": 2, "libelle": "Graines disponibles", "type": "nombre", "attendu": graines_disponibles, "unite": "graines"},
            {"id": "r3", "question": 3, "libelle": "Graines restantes", "type": "nombre", "attendu": graines_restantes, "unite": "graines"},
            {"id": "r4", "question": 4, "libelle": "Planches supplémentaires", "type": "nombre", "attendu": planches_supp, "unite": "planches"},
        ],
    })



# ================================================================
# Cinq nouveaux modèles N7 : diversité des raisonnements (P7-M17..M21).
# Chaque question comporte un champ numérique évalué indépendant.
# ================================================================


def _mc_question_finale_echecs(solde_positif):
    """Précise les recettes et le fonds initial dans la question de bilan."""
    if solde_positif:
        return (
            "En tenant compte de la caisse initiale et des recettes des inscriptions, "
            "combien d'euros restera-t-il au club après les dépenses du tournoi ?"
        )
    return (
        "En tenant compte de la caisse initiale et des recettes des inscriptions, "
        "combien d'euros manquera-t-il au club pour payer les dépenses du tournoi ?"
    )


def generer_modele_p7_echecs():
    """Compter des rencontres sans compter deux fois chaque paire."""
    while True:
        joueurs = random.randint(8, 16)
        prix_inscription = random.randint(3, 8)
        prix_recompense = random.randint(2, 6)
        location_salle = random.randint(35, 135)
        fonds_club = random.randint(100, 460)
        adversaires = joueurs - 1
        rencontres = joueurs * adversaires // 2
        recettes = joueurs * prix_inscription
        couts = rencontres * prix_recompense + location_salle
        solde = fonds_club + recettes - couts
        if 15 <= abs(solde) <= 240:
            break
    question_finale = _mc_question_finale_echecs(solde > 0)
    enonce = (
        "**Le tournoi d'échecs**\n\n"
        f"Un club organise un tournoi avec {joueurs} joueurs. "
        "Chaque joueur rencontre **une fois chacun des autres joueurs**, "
        "et une partie oppose exactement deux joueurs.\n\n"
        f"L'inscription coûte {prix_inscription} € par joueur. "
        f"Le club prévoit {prix_recompense} € de matériel de récompense pour chaque partie "
        f"et {location_salle} € pour la location de la salle. "
        f"Il possède déjà {fonds_club} € dans sa caisse.\n\n"
        "**Questions**\n\n"
        "1. Combien d'adversaires chaque joueur rencontrera-t-il ?\n\n"
        "2. Combien de parties seront jouées au total, sans compter deux fois la même partie ?\n\n"
        "3. Combien d'euros les inscriptions rapporteront-elles au club ?\n\n"
        f"4. {question_finale}"
    )
    conclusion = (
        f"Il restera {solde} € dans la caisse."
        if solde > 0 else
        f"Il manquera {-solde} € pour payer le tournoi."
    )
    correction = (
        "**1. Adversaires par joueur**\n\n"
        f"{joueurs} − 1 = {adversaires} adversaires.\n\n"
        "**2. Parties sans doublons**\n\n"
        f"{joueurs} × {adversaires} = {joueurs * adversaires} rencontres comptées par les joueurs. "
        "Chaque partie est comptée deux fois (par ses deux joueurs).\n"
        f"{joueurs * adversaires} ÷ 2 = {rencontres} parties distinctes.\n\n"
        "**3. Recettes des inscriptions**\n\n"
        f"{joueurs} × {prix_inscription} = {recettes} €.\n\n"
        "**4. Bilan financier du tournoi**\n\n"
        f"**Recettes des inscriptions :** {joueurs} × {prix_inscription} = {recettes} €.\n"
        f"**Caisse initiale :** {fonds_club} €.\n"
        f"**Somme disponible :** {fonds_club} + {recettes} = {fonds_club + recettes} €.\n\n"
        f"**Récompenses :** {rencontres} × {prix_recompense} = {rencontres * prix_recompense} €.\n"
        f"**Location de la salle :** {location_salle} €.\n"
        f"**Dépenses totales :** {rencontres * prix_recompense} + {location_salle} = {couts} €.\n\n"
        "**Expression complète du bilan :**\n"
        f"{fonds_club} + ({joueurs} × {prix_inscription}) − "
        f"(({rencontres} × {prix_recompense}) + {location_salle}) = {solde} €.\n"
        + (f"**Différence :** {fonds_club + recettes} − {couts} = {solde} €.\n"
           if solde > 0 else
           f"**Montant manquant :** {couts} − {fonds_club + recettes} = {-solde} €.\n")
        + f"**Conclusion :** {conclusion}"
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M17", "titre": "Le tournoi d'échecs", "mathicap_solde_positif": solde > 0,
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Adversaires par joueur", "type": "nombre", "attendu": adversaires, "unite": "adversaires"},
            {"id": "r2", "question": 2, "libelle": "Parties distinctes", "type": "nombre", "attendu": rencontres, "unite": "parties"},
            {"id": "r3", "question": 3, "libelle": "Recettes des inscriptions", "type": "nombre", "attendu": recettes, "unite": "€"},
            {"id": "r4", "question": 4, "libelle": "Écart après dépenses", "type": "nombre", "attendu": abs(solde), "unite": "€"},
        ],
    })


def generer_modele_p7_fresque():
    """Aire de rectangles, deux couches, pots entiers, budget."""
    while True:
        panneaux = random.randint(4, 9)
        longueur = random.randint(2, 5)
        hauteur = random.randint(2, 4)
        surface = panneaux * longueur * hauteur
        surface_peindre = 2 * surface
        couverture = random.randint(12, 25)
        pots = (surface_peindre + couverture - 1) // couverture
        prix_pot = random.randint(12, 28)
        cout = pots * prix_pot
        ecart = random.randint(17, 165)
        budget = cout + ecart if random.choice((True, False)) else cout - ecart
        if 4 <= pots <= 18 and budget >= 65 and surface_peindre % couverture != 0:
            break
    manque = budget < cout
    question_finale = (
        "Combien d'euros manque-t-il au collège pour acheter tous les pots nécessaires ?"
        if manque else
        "Combien d'euros restera-t-il du budget après l'achat des pots nécessaires ?"
    )
    enonce = (
        "**La fresque du préau**\n\n"
        f"Les élèves veulent peindre {panneaux} panneaux rectangulaires de "
        f"{longueur} m de long et {hauteur} m de haut. "
        "Chaque panneau doit recevoir **deux couches de peinture**.\n\n"
        f"Un pot permet de couvrir au maximum {couverture} m² pour une couche "
        f"et coûte {prix_pot} €. Le collège dispose d'un budget de {budget} €. "
        "Les pots s'achètent entiers.\n\n"
        "**Questions**\n\n"
        "1. Quelle est la surface totale des panneaux, en m² ?\n\n"
        "2. Quelle surface de peinture faut-il prévoir pour les deux couches, en m² ?\n\n"
        "3. Combien de pots de peinture faut-il acheter au minimum ?\n\n"
        f"4. {question_finale}"
    )
    correction = (
        "**1. Surface totale des panneaux**\n\n"
        f"{panneaux} × {longueur} × {hauteur} = {surface} m².\n\n"
        "**2. Deux couches de peinture**\n\n"
        f"{surface} × 2 = {surface_peindre} m² de couverture nécessaires.\n\n"
        "**3. Nombre minimal de pots**\n\n"
        f"{surface_peindre} ÷ {couverture} : quotient entier "
        f"{surface_peindre // couverture}, reste {surface_peindre % couverture}.\n"
        f"Il faut {pots} pots entiers pour les deux couches.\n\n"
        "**4. Bilan du budget**\n\n"
        f"**Coût total des pots :** {pots} × {prix_pot} = {cout} €.\n"
        f"**Budget disponible :** {budget} €.\n"
        + (f"**Différence :** {cout} − {budget} = {cout - budget} €.\n"
           if manque else
           f"**Différence :** {budget} − {cout} = {budget - cout} €.\n")
        + (
            f"**Conclusion :** Il manque {cout - budget} €."
            if manque else
            f"**Conclusion :** Il restera {budget - cout} €."
        )
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M18", "titre": "La fresque du préau", "mathicap_budget_suffisant": not manque,
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Surface totale", "type": "nombre", "attendu": surface, "unite": "m²"},
            {"id": "r2", "question": 2, "libelle": "Surface pour deux couches", "type": "nombre", "attendu": surface_peindre, "unite": "m²"},
            {"id": "r3", "question": 3, "libelle": "Pots nécessaires", "type": "nombre", "attendu": pots, "unite": "pots"},
            {"id": "r4", "question": 4, "libelle": "Écart avec le budget", "type": "nombre", "attendu": abs(budget - cout), "unite": "€"},
        ],
    })


def generer_modele_p7_carnets_transport():
    """N7 : trois offres A/B/C calculées, puis choix direct de la moins chère."""
    categorie = random.choice(["A", "B", "C"])
    voyageurs = random.randint(38, 116)
    while voyageurs % 5 == 0 or (categorie == "B" and (voyageurs*2) % 10 < 6):
        voyageurs = random.randint(38, 116)
    billets = voyageurs * 2
    carnets, billets_isoles = divmod(billets, 10)
    prix_unitaire = random.randint(2, 6)
    if categorie == "A":
        prix_carnet = random.randint(11*prix_unitaire, 13*prix_unitaire)
    elif categorie == "B":
        prix_carnet = random.randint(4*prix_unitaire, billets_isoles*prix_unitaire - 1)
    else:
        prix_carnet = random.randint(billets_isoles*prix_unitaire+1, 9*prix_unitaire)
    cout_unite = billets * prix_unitaire
    cout_carnets = (carnets + 1)*prix_carnet
    cout_mixte = carnets*prix_carnet + billets_isoles*prix_unitaire
    options = {"A":cout_unite, "B":cout_carnets, "C":cout_mixte}
    gagnant = min(options, key=options.get)
    enonce = (
        "**Les carnets de transport**\n\n"
        f"Un club prépare une sortie pour {voyageurs} participants. Chaque personne "
        "doit avoir un billet pour l'aller et un pour le retour.\n\n"
        f"Un billet à l'unité coûte {prix_unitaire} €. "
        f"Un carnet de 10 billets coûte {prix_carnet} €. "
        "Les billets non utilisés pourront servir lors d'une autre sortie.\n\n"
        "**Questions**\n\n"
        "1. **Choix A :** combien coûterait l'achat de tous les billets à l'unité ?\n\n"
        "2. **Choix B :** combien coûteraient des carnets entiers en quantité suffisante ?\n\n"
        "3. **Choix C :** combien coûteraient des carnets complets, "
        "complétés par les billets restants achetés à l'unité ?\n\n"
        "4. Quel est le choix le moins cher : A, B ou C ?"
    )
    correction = (
        "**1. Choix A — uniquement des billets à l'unité**\n\n"
        f"{voyageurs} × 2 = {billets} billets. "
        f"Coût : {billets} × {prix_unitaire} = {cout_unite} €.\n\n"
        "**2. Choix B — uniquement des carnets entiers**\n\n"
        f"{billets} ÷ 10 : quotient {carnets}, reste {billets_isoles}. "
        f"Il faut {carnets+1} carnets pour couvrir tous les billets.\n"
        f"Coût : {carnets+1} × {prix_carnet} = {cout_carnets} €.\n\n"
        "**3. Choix C — carnets et billets à l'unité**\n\n"
        f"{carnets} carnets et {billets_isoles} billets à l'unité.\n"
        f"Coût : {carnets} × {prix_carnet} + {billets_isoles} × {prix_unitaire} "
        f"= {cout_mixte} €.\n\n"
        "**4. Comparaison**\n\n"
        f"A : {cout_unite} € ; B : {cout_carnets} € ; C : {cout_mixte} €.\n"
        f"**Choix {gagnant}** : coût minimal {options[gagnant]} €."
    )
    return _mc_uniformiser_exercice({
        "id":"P7-M19", "titre":"Les carnets de transport", "enonce":enonce,
        "correction":correction, "reponse_attendue":None,
        "champs_reponse":[
            {"id":"r1", "question":1, "libelle":"Coût du choix A", "type":"nombre", "attendu":cout_unite, "unite":"€"},
            {"id":"r2", "question":2, "libelle":"Coût du choix B", "type":"nombre", "attendu":cout_carnets, "unite":"€"},
            {"id":"r3", "question":3, "libelle":"Coût du choix C", "type":"nombre", "attendu":cout_mixte, "unite":"€"},
            {"id":"r4", "question":4, "libelle":"Choix le moins cher", "type":"choix", "attendu":gagnant, "options":["A","B","C"]},
        ],
    })

def generer_modele_p7_course_solidaire():
    """Distances décimales et recettes d'un parrainage solidaire."""
    while True:
        eleves = [random.randint(8, 17) for _ in range(3)]
        tours_eleve = [random.randint(3, 7) for _ in range(3)]
        tours = sum(a*b for a,b in zip(eleves, tours_eleve))
        longueur_dixieme = random.choice([4, 5, 6, 8, 12])
        distance = tours * longueur_dixieme / 10
        euros_tour = random.randint(2, 5)
        frais = random.randint(90, 280)
        recettes = tours * euros_tour
        net = recettes - frais
        ecart = random.randint(25, 155)
        objectif = net - ecart if random.choice((True, False)) else net + ecart
        if net > 180 and objectif >= 70:
            break
    suffisant = net > objectif
    question_finale = (
        "De combien d'euros la somme disponible dépasse-t-elle l'objectif de don après les frais ?"
        if suffisant else
        "De combien d'euros la somme disponible est-elle inférieure à l'objectif de don après les frais ?"
    )
    equipes = "; ".join(
        f"{eleves[i]} élèves parcourent chacun {tours_eleve[i]} tours" for i in range(3)
    )
    longueur_texte = str(longueur_dixieme / 10).replace(".", ",")
    distance_texte = f"{distance:g}".replace(".", ",")
    enonce = (
        "**La course solidaire du collège**\n\n"
        "Trois groupes participent à une course parrainée : " + equipes + ".\n\n"
        f"Chaque tour mesure {longueur_texte} km. "
        f"Les parrains donnent {euros_tour} € pour chaque tour effectué, quel que soit le groupe. "
        f"L'organisation coûte {frais} €. Les élèves souhaitent remettre au moins "
        f"{objectif} € à une association après paiement de ces frais.\n\n"
        "**Questions**\n\n"
        "1. Combien de tours ont été réalisés par l'ensemble des groupes ?\n\n"
        "2. Quelle distance ont-ils parcourue au total, en kilomètres ?\n\n"
        "3. Quelle somme les parrains versent-ils au total, avant les frais ?\n\n"
        f"4. {question_finale}"
    )
    detail = " + ".join(f"{a} × {b}" for a,b in zip(eleves, tours_eleve))
    correction = (
        "**1. Tours parcourus**\n\n"
        f"{detail} = {tours} tours.\n\n"
        "**2. Distance cumulée**\n\n"
        f"{tours} × {longueur_texte} = {distance_texte} km.\n\n"
        "**3. Argent des parrains**\n\n"
        f"{tours} × {euros_tour} = {recettes} €.\n\n"
        "**4. Objectif après les frais**\n\n"
        f"**Recettes de parrainage :** {tours} × {euros_tour} = {recettes} €.\n"
        f"**Frais d'organisation :** {frais} €.\n"
        f"**Somme réellement disponible :** {recettes} − {frais} = {net} €.\n"
        f"**Objectif de don :** {objectif} €.\n"
        + (f"**Différence :** {net} − {objectif} = {ecart} €.\n"
           if suffisant else
           f"**Différence :** {objectif} − {net} = {ecart} €.\n")
        + (f"**Conclusion :** L'objectif est dépassé de {ecart} €."
           if suffisant else f"**Conclusion :** Il manque {ecart} € pour atteindre l'objectif.")
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M20", "titre": "La course solidaire du collège", "mathicap_objectif_atteint": suffisant,
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Tours parcourus", "type": "nombre", "attendu": tours, "unite": "tours"},
            {"id": "r2", "question": 2, "libelle": "Distance cumulée", "type": "nombre", "attendu": distance, "unite": "km"},
            {"id": "r3", "question": 3, "libelle": "Somme des parrainages", "type": "nombre", "attendu": recettes, "unite": "€"},
            {"id": "r4", "question": 4, "libelle": "Écart avec l'objectif", "type": "nombre", "attendu": ecart, "unite": "€"},
        ],
    })


def generer_modele_p7_refuge():
    """N7 : besoin quotidien, stock disponible, durée, quantité manquante en g."""
    adultes = random.randint(12, 25)
    jeunes = random.randint(9, 21)
    g_adulte = random.choice([120,140,160,180])
    g_jeune = random.choice([60,70,80,90,100])
    initial_kg = random.randint(22,65)
    livraison_kg = random.randint(8,25)
    ration = adultes*g_adulte + jeunes*g_jeune
    stock = (initial_kg+livraison_kg)*1000
    jours, reste = divmod(stock,ration)
    objectif_jours = jours + random.randint(3,10)
    manque = objectif_jours*ration-stock
    enonce = (
        "**Le refuge des lapins**\n\n"
        f"Le refuge accueille {adultes} lapins adultes et {jeunes} jeunes lapins. "
        f"Chaque adulte mange {g_adulte} g de granulés par jour et chaque jeune {g_jeune} g.\n\n"
        f"Le refuge possède {initial_kg} kg de granulés et reçoit une livraison "
        f"de {livraison_kg} kg. La prochaine livraison n'aura lieu que dans "
        f"{objectif_jours} jours.\n\n"
        "**Questions**\n\n"
        "1. Combien de grammes de granulés faut-il pour nourrir tous les lapins pendant un jour ?\n\n"
        "2. Combien de grammes le refuge possède-t-il après la livraison ?\n\n"
        "3. Pendant combien de jours complets ce stock suffit-il ?\n\n"
        "4. Combien de grammes de granulés manque-t-il pour tenir "
        "jusqu'à la prochaine livraison ?"
    )
    correction = (
        "**1. Ration quotidienne**\n\n"
        f"{adultes} × {g_adulte} + {jeunes} × {g_jeune} = {ration} g.\n\n"
        "**2. Stock disponible**\n\n"
        f"({initial_kg} + {livraison_kg}) × 1 000 = {stock} g.\n\n"
        "**3. Jours complets**\n\n"
        f"{stock} ÷ {ration} : quotient {jours}, reste {reste} g. "
        f"Le stock couvre {jours} jours complets.\n\n"
        "**4. Granulés manquants**\n\n"
        f"Besoin jusqu'à la prochaine livraison : {objectif_jours} × {ration} "
        f"= {objectif_jours*ration} g.\n"
        f"Il manque {objectif_jours*ration} − {stock} = {manque} g."
    )
    return _mc_uniformiser_exercice({
        "id":"P7-M21", "titre":"Le refuge des lapins", "enonce":enonce,
        "correction":correction, "reponse_attendue":None,
        "champs_reponse":[
            {"id":"r1", "question":1, "libelle":"Granulés par jour", "type":"nombre", "attendu":ration, "unite":"g"},
            {"id":"r2", "question":2, "libelle":"Stock disponible", "type":"nombre", "attendu":stock, "unite":"g"},
            {"id":"r3", "question":3, "libelle":"Jours complets", "type":"nombre", "attendu":jours, "unite":"jours"},
            {"id":"r4", "question":4, "libelle":"Granulés manquants", "type":"nombre", "attendu":manque, "unite":"g"},
        ],
    })

# ================================================================
# Cinq nouveaux modèles niveau 7 (P7-M22 à P7-M26).
# Situations distinctes, quatre questions indépendantes par modèle.
# ================================================================


def generer_modele_p7_defi_lecture():
    """Projet de lecture : retrouver le rythme quotidien minimal du groupe."""
    eleves = random.randint(5, 11)
    pages_deja = random.randint(18, 67)
    jours = random.randint(4, 8)
    pages_jour = random.randint(8, 20)
    lecture_initiale = eleves * pages_deja
    lecture_prevue = eleves * jours * pages_jour
    total_prevu = lecture_initiale + lecture_prevue

    # L'objectif impose un rythme de groupe supérieur à la prévision initiale.
    # Le reste crée des cas de division exacte et de division avec arrondi supérieur.
    surplus_quotidien = random.randint(5, 35)
    reste_cible = random.randint(0, jours - 1)
    rythme_minimum = eleves * pages_jour + surplus_quotidien
    objectif = lecture_initiale + jours * rythme_minimum - reste_cible
    pages_restantes = objectif - lecture_initiale
    rythme_calcule = (pages_restantes + jours - 1) // jours
    assert rythme_calcule == rythme_minimum

    enonce = (
        "**Le défi de lecture**\n\n"
        f"Un groupe de {eleves} collégiens participe à un défi de lecture. "
        f"Chacun a déjà lu {pages_deja} pages.\n\n"
        f"Pendant les {jours} prochains jours, chacun prévoit de lire "
        f"{pages_jour} pages par jour. L'objectif commun est d'atteindre "
        f"au moins {objectif} pages lues par le groupe, en comptant celles déjà lues.\n\n"
        "Le groupe décide de lire le même nombre total de pages chaque jour restant.\n\n"
        "**Questions**\n\n"
        "1. Combien de pages le groupe a-t-il déjà lues ?\n\n"
        "2. Combien de pages le groupe prévoit-il de lire au cours des jours restants, sans effort supplémentaire ?\n\n"
        "3. Combien de pages le groupe aura-t-il lues au total s'il respecte ce rythme ?\n\n"
        "4. Combien de pages le groupe doit-il lire par jour, au minimum, "
        "pour atteindre son objectif commun ?"
    )
    quotient, reste = divmod(pages_restantes, jours)
    correction = (
        "**1. Pages déjà lues par le groupe**\n\n"
        f"{eleves} × {pages_deja} = {lecture_initiale} pages.\n\n"
        "**2. Lecture prévue pour les prochains jours**\n\n"
        f"{eleves} × {jours} × {pages_jour} = {lecture_prevue} pages.\n\n"
        "**3. Lecture totale prévue**\n\n"
        f"{lecture_initiale} + {lecture_prevue} = {total_prevu} pages.\n\n"
        "**4. Pages à lire par jour pour le groupe**\n\n"
        f"Il reste {objectif} − {lecture_initiale} = {pages_restantes} pages "
        f"à lire pour atteindre l'objectif.\n"
        f"En les répartissant sur {jours} jours : {pages_restantes} ÷ {jours} "
        f"donne un quotient entier de {quotient} et un reste de {reste}.\n"
        + ("Comme le groupe doit atteindre au moins l'objectif et lire un nombre "
           "entier de pages par jour, on arrondit à l'entier supérieur.\n" if reste else
           "La division est exacte : aucun arrondi n'est nécessaire.\n")
        + f"**Réponse : {rythme_minimum} pages par jour pour tout le groupe.**\n"
        f"Vérification : {lecture_initiale} + {jours} × {rythme_minimum} "
        f"= {lecture_initiale + jours * rythme_minimum} pages, "
        f"soit au moins {objectif} pages."
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M22", "titre": "Le défi de lecture", "enonce": enonce,
        "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Pages déjà lues", "type": "nombre", "attendu": lecture_initiale, "unite": "pages"},
            {"id": "r2", "question": 2, "libelle": "Pages prévues", "type": "nombre", "attendu": lecture_prevue, "unite": "pages"},
            {"id": "r3", "question": 3, "libelle": "Total prévu", "type": "nombre", "attendu": total_prevu, "unite": "pages"},
            {"id": "r4", "question": 4, "libelle": "Pages du groupe par jour", "type": "nombre", "attendu": rythme_minimum, "unite": "pages"},
        ],
    })

def generer_modele_p7_couture():
    """N7 : rouleaux sans raccord, Q4 limitée au dernier rouleau."""
    for _ in range(3000):
        fanions = random.randint(10,55)
        petit = random.randint(18,46)
        grand = random.randint(45,102)
        if 2*petit <= grand:
            continue
        cm_fanion = 2*petit + grand
        m_rouleau = random.choice([5,6,8,10,12,15])
        cm_rouleau = 100*m_rouleau
        par_rouleau, chute_plein = divmod(cm_rouleau,cm_fanion)
        if par_rouleau < 2:continue
        rouleaux, reste_fanions = divmod(fanions,par_rouleau)
        rouleaux += int(reste_fanions>0)
        fanions_dernier = reste_fanions or par_rouleau
        chute_dernier = cm_rouleau-fanions_dernier*cm_fanion
        cm_noeud = random.choice([15,20,25,30,35,40])
        noeuds, reste_chute = divmod(chute_dernier,cm_noeud)
        if (2<=rouleaux<=18 and reste_fanions>0 and 1<=noeuds<=20):break
    else:raise ValueError("Aucun tirage valide de fanions")
    enonce=(
        "**Les fanions du club de couture**\n\n"
        f"Le club prépare {fanions} fanions triangulaires identiques. "
        f"Chaque fanion possède deux côtés de {petit} cm et un troisième de "
        f"{grand} cm. Un seul ruban continu décore ses trois côtés.\n\n"
        f"Le ruban est vendu par rouleaux de {m_rouleau} m. Chaque rouleau est "
        "utilisé pour fabriquer autant de fanions complets que possible "
        "avant de commencer le rouleau suivant. Les rubans ne sont pas raccordés.\n\n"
        f"On réalise des petits nœuds utilisant chacun {cm_noeud} cm de ruban, "
        "uniquement avec la chute du dernier rouleau.\n\n"
        "**Questions**\n\n"
        "1. Quelle longueur de ruban faut-il pour un fanion, en centimètres ?\n\n"
        "2. Quelle longueur de ruban faut-il pour tous les fanions ?\n\n"
        "3. Combien de rouleaux faut-il acheter au minimum ?\n\n"
        "4. Combien de petits nœuds complets peut-on fabriquer avec la chute "
        "du dernier rouleau ?"
    )
    correction=(
        "**1. Ruban pour un fanion**\n\n"
        f"2 × {petit} + {grand} = {cm_fanion} cm.\n\n"
        "**2. Ruban pour tous les fanions**\n\n"
        f"{fanions} × {cm_fanion} = {fanions*cm_fanion} cm.\n\n"
        "**3. Rouleaux nécessaires**\n\n"
        f"Un rouleau contient {cm_rouleau} cm, ce qui permet "
        f"{cm_rouleau} ÷ {cm_fanion}, soit {par_rouleau} fanions complets.\n"
        f"{fanions} ÷ {par_rouleau} : quotient entier {fanions//par_rouleau}, "
        f"reste {reste_fanions}. Il faut donc {rouleaux} rouleaux.\n\n"
        "**4. Nœuds du dernier rouleau**\n\n"
        f"Dans le dernier rouleau, on réalise {fanions_dernier} fanions. "
        f"Il reste {cm_rouleau} − {fanions_dernier} × {cm_fanion} "
        f"= {chute_dernier} cm.\n"
        f"{chute_dernier} ÷ {cm_noeud} : quotient {noeuds}, reste {reste_chute} cm. "
        f"On peut fabriquer {noeuds} nœuds complets."
    )
    return _mc_uniformiser_exercice({
        "id":"P7-M23", "titre":"Les fanions du club de couture", "enonce":enonce,
        "correction":correction, "reponse_attendue":None,
        "champs_reponse":[
            {"id":"r1", "question":1, "libelle":"Ruban par fanion", "type":"nombre", "attendu":cm_fanion, "unite":"cm"},
            {"id":"r2", "question":2, "libelle":"Ruban total", "type":"nombre", "attendu":fanions*cm_fanion, "unite":"cm"},
            {"id":"r3", "question":3, "libelle":"Rouleaux nécessaires", "type":"nombre", "attendu":rouleaux, "unite":"rouleaux"},
            {"id":"r4", "question":4, "libelle":"Nœuds du dernier rouleau", "type":"nombre", "attendu":noeuds, "unite":"nœuds"},
        ],
    })

def _mc_libelle_question_finale_casiers(suffisant):
    """Question finale : équipes supplémentaires au créneau le plus fréquenté."""
    return (
        "En tenant compte du créneau le plus chargé, combien d'équipes "
        "supplémentaires le gymnase peut-il accueillir en même temps ?"
    )


def generer_modele_p7_casiers():
    """N7 : comparer deux créneaux et compter des équipes supplémentaires."""
    # Les équipes des deux créneaux ont la même taille : une seule réponse
    # numérique à Q4, sans hypothèse à choisir sur la taille d'une équipe.
    eleves_par_equipe = random.randint(4, 7)
    equipes_matin = random.randint(4, 8)
    equipes_apres_midi = random.randint(4, 8)
    while equipes_apres_midi == equipes_matin:
        equipes_apres_midi = random.randint(4, 8)

    matin = equipes_matin * eleves_par_equipe
    apres_midi = equipes_apres_midi * eleves_par_equipe
    pic = max(matin, apres_midi)
    equipes_supplementaires = random.randint(1, 3)
    casiers_en_plus = equipes_supplementaires * eleves_par_equipe + random.randint(0, eleves_par_equipe - 1)
    utilisables = pic + casiers_en_plus
    hors_service = random.randint(3, 13)
    total_casiers = utilisables + hors_service
    libres = utilisables - pic
    assert libres >= eleves_par_equipe
    assert libres // eleves_par_equipe == equipes_supplementaires

    enonce = (
        "**Les casiers du gymnase**\n\n"
        "Chaque élève utilise un casier personnel. Le gymnase accueille deux "
        "créneaux distincts : le matin et l'après-midi. Les élèves du matin "
        "libèrent leur casier avant l'arrivée de ceux de l'après-midi.\n\n"
        f"Le matin, {equipes_matin} équipes de {eleves_par_equipe} élèves fréquentent le gymnase. "
        f"L'après-midi, ce sont {equipes_apres_midi} équipes de {eleves_par_equipe} élèves.\n\n"
        f"Le gymnase possède {total_casiers} casiers, dont {hors_service} hors service.\n\n"
        "Chaque nouvelle équipe comporte le même nombre d'élèves que les autres.\n\n"
        "**Questions**\n\n"
        "1. Combien d'élèves sont présents le matin ?\n\n"
        "2. Combien d'élèves sont présents l'après-midi ?\n\n"
        "3. Combien de casiers utilisables le gymnase possède-t-il ?\n\n"
        "4. En tenant compte du créneau le plus chargé, combien d'équipes "
        "supplémentaires le gymnase peut-il accueillir en même temps ?"
    )
    correction = (
        "**1. Élèves le matin**\n\n"
        f"{equipes_matin} × {eleves_par_equipe} = {matin} élèves.\n\n"
        "**2. Élèves l'après-midi**\n\n"
        f"{equipes_apres_midi} × {eleves_par_equipe} = {apres_midi} élèves.\n\n"
        "**3. Casiers utilisables**\n\n"
        f"{total_casiers} − {hors_service} = {utilisables} casiers.\n\n"
        "**4. Équipes supplémentaires possibles**\n\n"
        f"Le créneau le plus chargé rassemble {pic} élèves. "
        f"Il reste alors {utilisables} − {pic} = {libres} casiers libres.\n"
        f"Une équipe comprend {eleves_par_equipe} élèves. "
        f"{libres} ÷ {eleves_par_equipe} permet d'accueillir "
        f"**{equipes_supplementaires} "
        f"{'équipe supplémentaire complète' if equipes_supplementaires == 1 else 'équipes supplémentaires complètes'}**."
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M24", "titre": "Les casiers du gymnase",
        "mathicap_stock_suffisant": True,
        "enonce": enonce, "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Élèves le matin", "type": "nombre", "attendu": matin, "unite": "élèves"},
            {"id": "r2", "question": 2, "libelle": "Élèves l'après-midi", "type": "nombre", "attendu": apres_midi, "unite": "élèves"},
            {"id": "r3", "question": 3, "libelle": "Casiers utilisables", "type": "nombre", "attendu": utilisables, "unite": "casiers"},
            {"id": "r4", "question": 4, "libelle": "Équipes supplémentaires", "type": "nombre", "attendu": equipes_supplementaires, "unite": "équipe" if equipes_supplementaires == 1 else "équipes"},
        ],
    })

def generer_modele_p7_carte_orientation():
    """Échelle, déviation du retour et comparaison de trajets possibles."""
    retour_a_souhaite = random.choice([True, False])
    for _ in range(1000):
        a1, a2 = random.randint(3, 11), random.randint(3, 11)
        b1, b2, b3 = [random.randint(2, 8) for _ in range(3)]
        longueur_a = a1 + a2
        longueur_b = b1 + b2 + b3
        detour_cm = random.randint(2, 10)
        if (2 <= abs(longueur_a + detour_cm - longueur_b) <= 10
                and ((longueur_a + detour_cm < longueur_b) == retour_a_souhaite)):
            break
    else:
        raise ValueError("Pas de trajet d'orientation exploitable")
    coefficient_dixieme = random.choice([2, 3, 4, 5, 6])
    distance_a = round(longueur_a * coefficient_dixieme / 10, 1)
    distance_b = round(longueur_b * coefficient_dixieme / 10, 1)
    retour_a = round((longueur_a + detour_cm) * coefficient_dixieme / 10, 1)
    distance_parcourue = round(distance_a + min(retour_a, distance_b), 1)
    format_dec = lambda x: f"{x:.1f}".replace(".", ",")
    retour = "A, avec sa déviation" if retour_a < distance_b else "B"
    enonce = (
        "**La carte du parcours d'orientation**\n\n"
        "Deux sentiers relient le collège à un point d'arrivée. Sur la carte, "
        f"**1 cm représente {format_dec(coefficient_dixieme/10)} km** sur le terrain.\n\n"
        f"Le sentier A comprend deux portions de {a1} cm et {a2} cm sur la carte. "
        f"Le sentier B comprend trois portions de {b1} cm, {b2} cm et {b3} cm.\n\n"
        "La classe doit emprunter A à l'aller pour passer par un point de contrôle. "
        f"Pour le retour, des travaux imposent **{detour_cm} cm de détour sur la carte** "
        "si l'on choisit A. B ne comporte pas de détour.\n\n"
        "**Questions**\n\n"
        "1. Quelle est la distance réelle du sentier A, en kilomètres ?\n\n"
        "2. Quelle est la distance réelle du sentier B, en kilomètres ?\n\n"
        "3. Quelle serait la distance du retour par le sentier A, avec la déviation ?\n\n"
        "4. Quelle distance totale la classe parcourra-t-elle si elle choisit "
        "le trajet de retour le plus court ?"
    )
    correction = (
        "**1. Distance réelle du sentier A**\n\n"
        f"({a1} + {a2}) × {format_dec(coefficient_dixieme/10)} "
        f"= {format_dec(distance_a)} km.\n\n"
        "**2. Distance réelle du sentier B**\n\n"
        f"({b1} + {b2} + {b3}) × {format_dec(coefficient_dixieme/10)} "
        f"= {format_dec(distance_b)} km.\n\n"
        "**3. Retour par A avec déviation**\n\n"
        f"({a1} + {a2} + {detour_cm}) × {format_dec(coefficient_dixieme/10)} "
        f"= {format_dec(retour_a)} km.\n\n"
        "**4. Parcours total le plus court**\n\n"
        f"Retour par A avec déviation : {format_dec(retour_a)} km. "
        f"Retour par B : {format_dec(distance_b)} km.\n"
        f"Le plus court retour est **{retour}**.\n"
        f"Distance aller-retour : {format_dec(distance_a)} + "
        f"{format_dec(min(retour_a, distance_b))} = "
        f"**{format_dec(distance_parcourue)} km**."
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M25", "titre": "La carte du parcours d'orientation", "enonce": enonce,
        "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Distance du sentier A", "type": "nombre", "attendu": distance_a, "unite": "km"},
            {"id": "r2", "question": 2, "libelle": "Distance du sentier B", "type": "nombre", "attendu": distance_b, "unite": "km"},
            {"id": "r3", "question": 3, "libelle": "Retour A avec détour", "type": "nombre", "attendu": retour_a, "unite": "km"},
            {"id": "r4", "question": 4, "libelle": "Distance totale", "type": "nombre", "attendu": distance_parcourue, "unite": "km"},
        ],
    })


def generer_modele_p7_aquarium():
    """Volumes, bidons entiers et contrôle du budget disponible."""
    while True:
        capacite = random.randint(180, 420)
        eau_avant = random.randint(75, 179)
        eau_retiree = random.randint(14, 56)
        if eau_avant <= eau_retiree + 10 or eau_avant >= capacite:
            continue
        eau_apres = eau_avant - eau_retiree
        a_ajouter = capacite - eau_apres
        bidon_litres = random.choice([8, 10, 12, 15, 18, 20])
        bidons = (a_ajouter + bidon_litres - 1) // bidon_litres
        prix_bidon = random.randint(5, 13)
        filtre = random.randint(19, 58)
        cout = bidons * prix_bidon + filtre
        ecart = random.randint(16, 122)
        suffisant = random.choice([True, False])
        budget = cout + ecart if suffisant else cout - ecart
        if budget >= 65 and 6 <= bidons <= 48:
            break
    question_finale = (
        "Combien d'euros restera-t-il du budget après l'achat des bidons et du filtre ?"
        if suffisant else
        "Combien d'euros manque-t-il pour acheter tous les bidons et le filtre ?"
    )
    enonce = (
        "**L'aquarium du collège**\n\n"
        f"L'aquarium du collège peut contenir {capacite} litres d'eau. "
        f"Avant son entretien, il contient {eau_avant} litres. "
        f"Pour le nettoyer, on retire {eau_retiree} litres, "
        "puis on souhaite le remplir jusqu'à sa capacité maximale.\n\n"
        f"L'eau traitée est vendue par bidons entiers de {bidon_litres} litres, "
        f"à {prix_bidon} € le bidon. Il faut aussi remplacer un filtre coûtant "
        f"{filtre} €. Le collège dispose d'un budget de {budget} €.\n\n"
        "**Questions**\n\n"
        "1. Combien de litres d'eau restent dans l'aquarium après le nettoyage ?\n\n"
        "2. Combien de litres faut-il ajouter pour remplir l'aquarium ?\n\n"
        "3. Combien de bidons d'eau traitée faut-il acheter au minimum ?\n\n"
        f"4. {question_finale}"
    )
    quotient, reste = divmod(a_ajouter, bidon_litres)
    conclusion = (
        f"Il restera {ecart} € après les achats."
        if suffisant else
        f"Il manquera {ecart} € pour financer les achats."
    )
    correction = (
        "**1. Eau restante après le nettoyage**\n\n"
        f"{eau_avant} − {eau_retiree} = {eau_apres} L.\n\n"
        "**2. Eau nécessaire pour remplir l'aquarium**\n\n"
        f"{capacite} − {eau_apres} = {a_ajouter} L.\n\n"
        "**3. Bidons entiers à acheter**\n\n"
        f"{a_ajouter} ÷ {bidon_litres} : quotient entier {quotient}, reste {reste} L.\n"
        + (f"Comme le reste est non nul, il faut un bidon supplémentaire : "
           if reste else "La division est exacte : ")
        + f"**{bidons} bidons** au minimum.\n\n"
        "**4. Budget pour les achats**\n\n"
        f"**Eau traitée :** {bidons} × {prix_bidon} = {bidons * prix_bidon} €.\n"
        f"**Filtre :** {filtre} €.\n"
        f"**Dépenses :** {bidons * prix_bidon} + {filtre} = {cout} €.\n"
        f"**Budget :** {budget} €.\n"
        + (f"Différence : {budget} − {cout} = {ecart} €.\n" if suffisant else
           f"Différence : {cout} − {budget} = {ecart} €.\n")
        + f"**Conclusion :** {conclusion}"
    )
    return _mc_uniformiser_exercice({
        "id": "P7-M26", "titre": "L'aquarium du collège", "mathicap_budget_suffisant": suffisant, "enonce": enonce,
        "correction": correction, "reponse_attendue": None,
        "champs_reponse": [
            {"id": "r1", "question": 1, "libelle": "Eau restante", "type": "nombre", "attendu": eau_apres, "unite": "L"},
            {"id": "r2", "question": 2, "libelle": "Eau à ajouter", "type": "nombre", "attendu": a_ajouter, "unite": "L"},
            {"id": "r3", "question": 3, "libelle": "Bidons nécessaires", "type": "nombre", "attendu": bidons, "unite": "bidons"},
            {"id": "r4", "question": 4, "libelle": "Écart avec le budget", "type": "nombre", "attendu": ecart, "unite": "€"},
        ],
    })


def generer_modele_p8_clubs():

    while True:
        nb_clubs = random.randint(3, 5)

        billets = random.randint(36, 54)
        prix_billet = random.randint(5, 8)

        gateaux = random.randint(20, 35)
        prix_gateau = random.randint(3, 5)

        location = random.randint(75, 130)
        lots_materiel = random.randint(5, 8)
        prix_lot = random.randint(9, 16)

        reserve = random.randint(20, 65)

        recettes_billets = billets * prix_billet
        recettes_gateaux = gateaux * prix_gateau
        recettes = recettes_billets + recettes_gateaux

        depenses_materiel = lots_materiel * prix_lot
        depenses = location + depenses_materiel

        benefice = recettes - depenses
        somme_a_partager = benefice - reserve

        if (
            35 <= somme_a_partager / nb_clubs <= 100
            and (somme_a_partager * 100) % nb_clubs == 0
        ):
            break

    part = somme_a_partager / nb_clubs
    part_affichee = f"{part:.2f}".replace(".", ",")

    enonce = (
        "**La fête des clubs du collège**\n\n"
        f"Les {nb_clubs} clubs du collège organisent "
        "ensemble une fête pour financer leurs activités.\n\n"

        "Pendant la fête, ils vendent :\n"
        f"- {billets} billets d'entrée à "
        f"{prix_billet} € chacun ;\n"
        f"- {gateaux} parts de gâteau à "
        f"{prix_gateau} € chacune.\n\n"

        "Pour organiser la fête, ils paient :\n"
        f"- {location} € pour la location du matériel ;\n"
        f"- {lots_materiel} lots de fournitures "
        f"à {prix_lot} € chacun.\n\n"

        f"Après avoir payé toutes les dépenses, "
        f"les clubs décident de conserver {reserve} € "
        "dans une caisse commune.\n\n"

        "Ils veulent ensuite partager équitablement "
        "tout l'argent restant entre les clubs. "
        "Chaque club peut recevoir des euros "
        "et des centimes.\n\n"

        "**Questions**\n\n"
        "1. Quel est le montant total des recettes ?\n\n"
        "2. Quel est le montant total des dépenses ?\n\n"
        "3. Quelle somme reste-t-il à partager "
        "après les dépenses et la mise en réserve ? "
        "Écris une seule expression numérique "
        "avec des parenthèses.\n\n"
        "4. Quelle somme reçoit chaque club ?"
    )

    correction = (
        "**1. Recettes totales**\n\n"
        f"Billets : {billets} × {prix_billet} "
        f"= {recettes_billets} €.\n\n"
        f"Gâteaux : {gateaux} × {prix_gateau} "
        f"= {recettes_gateaux} €.\n\n"
        f"Total : {recettes_billets} + "
        f"{recettes_gateaux} = {recettes} €.\n\n"

        "**2. Dépenses totales**\n\n"
        f"Fournitures : {lots_materiel} × "
        f"{prix_lot} = {depenses_materiel} €.\n\n"
        f"Total : {location} + "
        f"{depenses_materiel} = {depenses} €.\n\n"

        "**3. Somme à partager**\n\n"
        f"Bénéfice après dépenses : "
        f"{recettes} − {depenses} = {benefice} €.\n\n"
        f"Après la mise en réserve : "
        f"{benefice} − {reserve} "
        f"= {somme_a_partager} €.\n\n"

        "**Expression complète :**\n\n"
        f"({billets} × {prix_billet} + "
        f"{gateaux} × {prix_gateau}) "
        f"− ({location} + "
        f"{lots_materiel} × {prix_lot}) "
        f"− {reserve} = {somme_a_partager}.\n\n"

        "**4. Partage entre les clubs**\n\n"
        f"Il faut partager {somme_a_partager} € "
        f"entre {nb_clubs} clubs.\n\n"
        f"{somme_a_partager} ÷ {nb_clubs} "
        f"= {part_affichee} €.\n\n"
        f"**Chaque club reçoit {part_affichee} €.**\n\n"
        "La somme est entièrement distribuée.\n\n"
        f"La caisse commune conserve la réserve "
        f"initiale de {reserve} €."
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M01",
        "titre": "La fête des clubs du collège",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Recettes totales",
                "type": "nombre",
                "attendu": recettes,
                "unite": "€"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Dépenses totales",
                "type": "nombre",
                "attendu": depenses,
                "unite": "€"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Somme à partager",
                "type": "nombre",
                "attendu": somme_a_partager,
                "unite": "€"
            },
            {
                "id": "expression",
                "question": 3,
                "libelle": "Mon expression numérique avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Somme reçue par chaque club",
                "type": "nombre",
                "attendu": part,
                "unite": "€"
            }
        ]
    })


def generer_modele_p8_manga():

    while True:
        nb_dessinateurs = random.randint(5, 8)
        dessins_par_eleve = random.randint(8, 13)

        anciens_dessins = random.randint(7, 20)
        dessins_ecartes = random.randint(4, 11)
        dessins_reserves = random.randint(3, 8)

        capacite_panneau = random.randint(9, 12)

        nouveaux_dessins = (
            nb_dessinateurs * dessins_par_eleve
        )

        total_dessins = (
            anciens_dessins + nouveaux_dessins
        )

        dessins_exposables = (
            total_dessins
            - dessins_ecartes
            - dessins_reserves
        )

        panneaux_complets, dessins_dernier = divmod(
            dessins_exposables,
            capacite_panneau
        )

        if (
            3 <= panneaux_complets <= 10
            and 2 <= dessins_dernier <= capacite_panneau - 2
        ):
            break

    panneaux_total = panneaux_complets + 1
    dessins_invites = random.randint(16, 44)
    panneaux_exposition = (dessins_exposables + dessins_invites + capacite_panneau - 1) // capacite_panneau

    enonce = (
        "**Le club manga**\n\n"
        "Le club manga du collège prépare une exposition "
        "de dessins réalisés par les élèves.\n\n"

        f"{nb_dessinateurs} élèves participent à la préparation. "
        f"Chacun réalise {dessins_par_eleve} dessins.\n\n"

        f"Le club possède également {anciens_dessins} dessins "
        "réalisés lors d'un précédent atelier.\n\n"

        "Avant l'exposition :\n"
        f"- {dessins_ecartes} dessins sont écartés "
        "car ils sont abîmés ;\n"
        f"- {dessins_reserves} dessins sont réservés "
        "pour illustrer le journal du collège.\n\n"

        "Les autres dessins seront exposés.\n\n"

        "Le club utilise des panneaux pouvant accueillir "
        f"chacun **au maximum {capacite_panneau} dessins**.\n\n"

        "Pour commencer, les organisateurs répartissent les seuls dessins du club. Ils remplissent autant "
        "de panneaux que possible, puis placent les "
        "dessins restants sur un dernier panneau.\n\n"
        f"Un collège partenaire apporte ensuite {dessins_invites} "
        "dessins supplémentaires. Pour l’exposition finale, tous les dessins sont répartis à nouveau sur les panneaux communs.\n\n"

        "**Questions**\n\n"

        "1. Combien de nouveaux dessins les élèves "
        "ont-ils réalisés ?\n\n"

        "2. Combien de dessins peuvent être exposés "
        "après les retraits ? "
        "Écris une seule expression numérique "
        "avec des parenthèses.\n\n"

        "3. Combien de panneaux peuvent être "
        "entièrement remplis ?\n\n"

        "4. Combien de dessins seront placés sur "
        "le dernier panneau ? "
        "Combien de panneaux faut-il au total ?"
    )

    correction = (
        "**1. Nouveaux dessins réalisés**\n\n"

        f"{nb_dessinateurs} × {dessins_par_eleve} "
        f"= {nouveaux_dessins} dessins.\n\n"

        "**2. Dessins pouvant être exposés**\n\n"

        f"Le club possède au total : "
        f"{anciens_dessins} + {nouveaux_dessins} "
        f"= {total_dessins} dessins.\n\n"

        f"Il retire {dessins_ecartes} dessins abîmés "
        f"et réserve {dessins_reserves} dessins.\n\n"

        f"{total_dessins} - {dessins_ecartes} "
        f"- {dessins_reserves} "
        f"= {dessins_exposables} dessins.\n\n"

        "**Expression complète :**\n\n"

        f"({anciens_dessins} + "
        f"{nb_dessinateurs} × {dessins_par_eleve}) "
        f"- ({dessins_ecartes} + {dessins_reserves}) "
        f"= {dessins_exposables}.\n\n"

        "**3. Panneaux entièrement remplis**\n\n"

        f"Chaque panneau peut contenir "
        f"{capacite_panneau} dessins.\n\n"

        f"{dessins_exposables} : {capacite_panneau}  —  "
        f"Quotient : {panneaux_complets}  —  "
        f"Reste : {dessins_dernier}\n\n"

        f"Il est donc possible de remplir entièrement "
        f"**{panneaux_complets} panneaux**.\n\n"

        "**4. Dessins sur le dernier panneau du club**\n\n"

        f"Il reste {dessins_dernier} dessins "
        "à placer sur un dernier panneau.\n\n"

        f"Nombre total de panneaux : "
        f"{panneaux_complets} + 1 "
        f"= {panneaux_total}.\n\n"

        f"Pour les dessins du club seul, il faudrait {panneaux_total} "
        f"panneaux, dont un dernier contenant {dessins_dernier} dessins.\n\n"
        "**5. Accueil des dessins du collège partenaire**\n\n"
        f"Dessins à exposer ensemble : {dessins_exposables} + {dessins_invites} "
        f"= {dessins_exposables + dessins_invites} dessins.\n\n"
        f"Division par {capacite_panneau} : quotient entier "
        f"{(dessins_exposables + dessins_invites) // capacite_panneau}, "
        f"reste {(dessins_exposables + dessins_invites) % capacite_panneau}.\n\n"
        f"**Il faudra {panneaux_exposition} panneaux au minimum** "
        "pour accueillir tous les dessins, y compris ceux du collège partenaire."
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M02",
        "titre": "Le club manga",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Nouveaux dessins réalisés",
                "type": "nombre",
                "attendu": nouveaux_dessins,
                "unite": "dessins"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Dessins pouvant être exposés",
                "type": "nombre",
                "attendu": dessins_exposables,
                "unite": "dessins"
            },
            {
                "id": "expression",
                "question": 2,
                "libelle": "Mon expression numérique avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Panneaux entièrement remplis",
                "type": "nombre",
                "attendu": panneaux_complets,
                "unite": "panneaux"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Dessins sur le dernier panneau",
                "type": "nombre",
                "attendu": dessins_dernier,
                "unite": "dessins"
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": "Panneaux pour tous les dessins",
                "type": "nombre",
                "attendu": panneaux_exposition,
                "unite": "panneaux"
            }
        ]
    })

def generer_modele_p8_jeu_video():

    while True:
        pieces_depart = random.randint(90, 150)

        missions = random.randint(3, 5)
        gain_mission = random.randint(18, 28)
        bonus = random.randint(12, 30)

        potions = random.randint(2, 4)
        prix_potion = random.randint(10, 17)

        cles_a = random.randint(2, 4)
        prix_cle = random.randint(12, 20)
        coffres_a = random.randint(3, 5)
        gain_coffre_a = random.randint(20, 34)

        entree_b = random.randint(30, 60)
        coffres_b = random.randint(2, 4)
        gain_coffre_b = random.randint(24, 40)

        gains_missions = missions * gain_mission + bonus
        cout_potions = potions * prix_potion

        solde_commun = (
            pieces_depart + gains_missions - cout_potions
        )

        cout_a = cles_a * prix_cle
        gains_a = coffres_a * gain_coffre_a
        solde_a = solde_commun - cout_a + gains_a

        cout_b = entree_b
        gains_b = coffres_b * gain_coffre_b
        solde_b = solde_commun - cout_b + gains_b

        difference = abs(solde_a - solde_b)

        if (
            solde_commun >= cout_a
            and solde_commun >= cout_b
            and solde_a > 0
            and solde_b > 0
            and difference >= 8
        ):
            break

    meilleur = "A" if solde_a > solde_b else "B"

    enonce = (
        "**Une aventure en jeu vidéo**\n\n"
        "Un joueur participe à un jeu d'aventure "
        "dans lequel il doit gérer ses pièces d'or.\n\n"

        f"Au départ, il possède {pieces_depart} pièces.\n\n"

        f"Il termine {missions} missions et gagne "
        f"{gain_mission} pièces par mission.\n\n"

        f"Il reçoit également un bonus unique de "
        f"{bonus} pièces.\n\n"

        f"Avant de poursuivre son aventure, il achète "
        f"{potions} potions à {prix_potion} pièces chacune.\n\n"

        "Il doit maintenant choisir entre deux chemins. "
        "Il ne peut en emprunter qu'un seul.\n\n"

        "**Chemin A — La forêt des coffres**\n\n"
        f"- Acheter {cles_a} clés à "
        f"{prix_cle} pièces chacune ;\n"
        f"- ouvrir {coffres_a} coffres contenant chacun "
        f"{gain_coffre_a} pièces.\n\n"

        "**Chemin B — La grotte secrète**\n\n"
        f"- Payer {entree_b} pièces pour entrer ;\n"
        f"- ouvrir {coffres_b} coffres contenant chacun "
        f"{gain_coffre_b} pièces.\n\n"

        "Dans les deux chemins, le joueur récupère "
        "toutes les pièces annoncées dans les coffres.\n\n"

        "**Questions**\n\n"

        "1. Combien de pièces possède-t-il après "
        "les missions, le bonus et l'achat des potions ? "
        "Écris une expression numérique avec "
        "des parenthèses.\n\n"

        "2. Combien de pièces posséderait-il "
        "à la fin du chemin A ?\n\n"

        "3. Combien de pièces posséderait-il "
        "à la fin du chemin B ?\n\n"

        "4. Quel chemin doit-il choisir pour avoir "
        "le plus de pièces ? "
        "Combien de pièces supplémentaires "
        "ce chemin lui permet-il d'obtenir "
        "par rapport à l'autre ?"
    )

    correction = (
        "**1. Solde après les missions et les potions**\n\n"

        f"Gains des missions : {missions} × {gain_mission} "
        f"= {missions * gain_mission} pièces.\n\n"

        f"Avec le bonus : {missions * gain_mission} "
        f"+ {bonus} = {gains_missions} pièces.\n\n"

        f"Coût des potions : {potions} × {prix_potion} "
        f"= {cout_potions} pièces.\n\n"

        "**Expression complète :**\n\n"

        f"{pieces_depart} + "
        f"({missions} × {gain_mission} + {bonus}) "
        f"− ({potions} × {prix_potion}) "
        f"= {solde_commun} pièces.\n\n"

        "**2. Solde avec le chemin A**\n\n"

        f"Prix des clés : {cles_a} × {prix_cle} "
        f"= {cout_a} pièces.\n\n"

        f"Gains des coffres : {coffres_a} × "
        f"{gain_coffre_a} = {gains_a} pièces.\n\n"

        f"{solde_commun} − {cout_a} + {gains_a} "
        f"= {solde_a} pièces.\n\n"

        "**3. Solde avec le chemin B**\n\n"

        f"Prix d'entrée : {cout_b} pièces.\n\n"

        f"Gains des coffres : {coffres_b} × "
        f"{gain_coffre_b} = {gains_b} pièces.\n\n"

        f"{solde_commun} − {cout_b} + {gains_b} "
        f"= {solde_b} pièces.\n\n"

        "**4. Comparaison des deux chemins**\n\n"

        f"Chemin A : {solde_a} pièces.\n\n"

        f"Chemin B : {solde_b} pièces.\n\n"

        f"Différence : {abs(solde_a - solde_b)} pièces.\n\n"

        f"**Le chemin {meilleur} est le plus avantageux.**\n\n"

        f"Il permet de terminer l'aventure avec "
        f"{difference} pièces de plus que l'autre chemin."
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M03",
        "titre": "Une aventure en jeu vidéo",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Pièces après missions et potions",
                "type": "nombre",
                "attendu": solde_commun,
                "unite": "pièces"
            },
            {
                "id": "expression",
                "question": 1,
                "libelle": "Mon expression numérique avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Solde final du chemin A",
                "type": "nombre",
                "attendu": solde_a,
                "unite": "pièces"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Solde final du chemin B",
                "type": "nombre",
                "attendu": solde_b,
                "unite": "pièces"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Chemin le plus avantageux",
                "type": "choix",
                "attendu": meilleur,
                "options": ["A", "B"],
                "dependances": ["r2", "r3"]
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": "Différence entre les deux chemins",
                "type": "nombre",
                "attendu": difference,
                "unite": "pièces"
            }
        ]
    })

def generer_modele_p8_robotique():

    while True:
        nb_equipes = random.randint(4, 6)
        robots_par_equipe = random.randint(2, 3)
        batteries_par_robot = random.randint(2, 3)
        batteries_reserve = random.randint(1, 2)

        stock_initial = random.randint(10, 23)
        boites_achetees = random.randint(1, 3)
        batteries_par_boite = random.choice([8, 10])
        batteries_abimees = random.randint(2, 5)
        prix_boite = random.randint(9, 16)

        batteries_robots = (
            nb_equipes * robots_par_equipe
            * batteries_par_robot
        )

        batteries_secours = (
            nb_equipes * batteries_reserve
        )

        besoin_total = batteries_robots + batteries_secours

        batteries_achetees = (
            boites_achetees * batteries_par_boite
        )

        stock_utilisable = (
            stock_initial + batteries_achetees
            - batteries_abimees
        )

        manque = besoin_total - stock_utilisable

        boites_supplementaires = (
            manque + batteries_par_boite - 1
        ) // batteries_par_boite

        reste = (
            stock_utilisable
            + boites_supplementaires * batteries_par_boite
            - besoin_total
        )

        cout = boites_supplementaires * prix_boite

        if (
            3 <= manque <= 22
            and manque % batteries_par_boite != 0
            and 1 <= boites_supplementaires <= 3
        ):
            break

    besoin_equipe = (
        robots_par_equipe * batteries_par_robot
        + batteries_reserve
    )

    enonce = (
        "**Le club de robotique**\n\n"
        "Le collège organise une compétition de robots.\n\n"

        f"{nb_equipes} équipes participent.\n\n"
        f"Chaque équipe possède {robots_par_equipe} robots.\n\n"
        f"Chaque robot a besoin de {batteries_par_robot} batteries "
        "pour fonctionner.\n\n"

        f"De plus, chaque équipe doit disposer de "
        f"{batteries_reserve} batterie{'s' if batteries_reserve != 1 else ''} de réserve.\n\n"

        "Le club possède déjà :\n"
        f"- {stock_initial} batteries en stock ;\n"
        f"- {boites_achetees} "
        f"boîte{'s' if boites_achetees > 1 else ''} de "
        f"{batteries_par_boite} batteries, "
        f"achetée{'s' if boites_achetees > 1 else ''} récemment.\n\n"

        f"Lors de la vérification de ce stock, "
        f"{batteries_abimees} batteries sont déclarées "
        "inutilisables.\n\n"

        "Pour compléter le stock, le club peut acheter "
        f"de nouvelles boîtes de {batteries_par_boite} "
        f"batteries, au prix de {prix_boite} € chacune.\n\n"

        "Toutes les batteries des nouvelles boîtes "
        "sont utilisables.\n\n"

        "**Questions**\n\n"

        "1. Combien de batteries faut-il au total "
        "pour équiper tous les robots et prévoir "
        "les batteries de réserve ? "
        "Écris une expression numérique avec "
        "des parenthèses.\n\n"

        "2. Combien de batteries utilisables "
        "le club possède-t-il actuellement ?\n\n"

        "3. Combien de batteries lui manque-t-il "
        "pour préparer la compétition ?\n\n"

        "4. Quel est le nombre minimal de boîtes "
        "supplémentaires à acheter ? "
        "Combien cet achat coûtera-t-il ? "
        "Combien de batteries restera-t-il "
        "après avoir équipé les équipes et "
        "prévu les batteries de réserve ?"
    )

    correction = (
        "**1. Batteries nécessaires**\n\n"

        f"Pour une équipe : "
        f"{robots_par_equipe} × {batteries_par_robot} "
        f"+ {batteries_reserve} "
        f"= {besoin_equipe} batteries.\n\n"

        "**Expression complète :**\n\n"

        f"{nb_equipes} × "
        f"({robots_par_equipe} × {batteries_par_robot} "
        f"+ {batteries_reserve}) "
        f"= {besoin_total} batteries.\n\n"

        "**2. Batteries utilisables**\n\n"

        f"Batteries achetées : {boites_achetees} × "
        f"{batteries_par_boite} "
        f"= {batteries_achetees}.\n\n"

        f"Stock utilisable : {stock_initial} "
        f"+ {batteries_achetees} "
        f"− {batteries_abimees} "
        f"= {stock_utilisable} batteries.\n\n"

        "**3. Batteries manquantes**\n\n"

        f"{besoin_total} − {stock_utilisable} "
        f"= {manque} batteries.\n\n"

        "**4. Boîtes supplémentaires**\n\n"

        f"Chaque boîte contient {batteries_par_boite} "
        "batteries.\n\n"

        f"{manque} : {batteries_par_boite} — "
        f"Quotient : {manque // batteries_par_boite} — "
        f"Reste : {manque % batteries_par_boite}\n\n"

        f"Il faut donc acheter au minimum "
        f"**{boites_supplementaires} "
        f"boîte{'s' if boites_supplementaires > 1 else ''}**.\n\n"

        f"Coût : {boites_supplementaires} × "
        f"{prix_boite} = {cout} €.\n\n"

        "Batteries restantes après répartition :\n\n"

        f"{stock_utilisable} + "
        f"{boites_supplementaires} × "
        f"{batteries_par_boite} "
        f"− {besoin_total} = {reste} batteries.\n\n"

        f"**Réponse :** Le club achète "
        f"{boites_supplementaires} "
        f"boîte{'s' if boites_supplementaires > 1 else ''} "
        f"pour {cout} €. Il lui restera {reste} "
        f"batterie{'s' if reste > 1 else ''}."
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M04",
        "titre": "Le club de robotique",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Batteries nécessaires au total",
                "type": "nombre",
                "attendu": besoin_total,
                "unite": "batteries"
            },
            {
                "id": "expression",
                "question": 1,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Batteries utilisables",
                "type": "nombre",
                "attendu": stock_utilisable,
                "unite": "batteries"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Batteries manquantes",
                "type": "nombre",
                "attendu": manque,
                "unite": "batteries"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Boîtes supplémentaires nécessaires",
                "type": "nombre",
                "attendu": boites_supplementaires,
                "unite": "boîtes"
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": "Coût des boîtes supplémentaires",
                "type": "nombre",
                "attendu": cout,
                "unite": "€"
            },
            {
                "id": "r6",
                "question": 4,
                "libelle": "Batteries restantes",
                "type": "nombre",
                "attendu": reste,
                "unite": "batteries"
            }
        ]
    })

def generer_modele_p8_jeu_piste():

    def euros(centimes):
        return f"{centimes / 100:.2f}".replace(".", ",")

    nb_equipes = random.randint(4, 7)
    nb_postes = random.randint(3, 5)

    prix_enveloppe = random.choice([50, 75, 100])
    prix_pochette = random.choice([300, 350, 400, 450])
    signalisation = random.randint(6, 12) * 100

    prix_souvenir = random.choice([200, 250, 300, 350])
    reserve = random.randint(4, 7) * 100

    # Dépenses obligatoires
    nb_enveloppes = nb_equipes * nb_postes
    cout_enveloppes = nb_enveloppes * prix_enveloppe
    cout_pochettes = nb_equipes * prix_pochette

    depenses = (
        cout_enveloppes
        + cout_pochettes
        + signalisation
    )

    # Souvenirs facultatifs
    cout_souvenirs = nb_equipes * prix_souvenir
    somme_necessaire = cout_souvenirs + reserve

    # Deux situations maintenues : achat possible ou non avec la réserve.
    # Si non, les souvenirs seuls restent finançables : c'est bien la
    # réserve qui interdit l'achat, pas un manque antérieur de budget.
    # Si oui, le montant au-delà de la réserve demeure varié.
    if random.choice([True, False]):
        variation = random.randrange(150, 1251, 10)
    else:
        # reserve >= 400 centimes : au moins 1 € reste après les souvenirs.
        variation = -random.randrange(100, reserve, 10)

    argent_disponible = somme_necessaire + variation
    budget = depenses + argent_disponible

    achat_possible = (
        "Oui" if variation > 0 else "Non"
    )

    difference = abs(variation)

    if achat_possible == "Oui":
        libelle_difference = "Excédent au-delà de la réserve"

        conclusion = (
            f"Le collège peut acheter les souvenirs "
            f"et conserver au moins {euros(reserve)} €.\n\n"
            f"Après l'achat des souvenirs, il lui reste "
            f"{euros(argent_disponible - cout_souvenirs)} €.\n\n"
            f"Il conserve donc {euros(difference)} € "
            "de plus que la réserve minimale."
        )
    else:
        libelle_difference = (
            "Montant manquant pour acheter les souvenirs "
            "et conserver la réserve"
        )
        conclusion = (
            f"Le collège ne peut pas acheter les souvenirs "
            f"tout en conservant {euros(reserve)} € "
            "de réserve.\n\n"
            f"Il lui manque {euros(difference)} € "
            "pour réaliser les deux objectifs.\n\n"
            "S'il renonce aux souvenirs, il conserve "
            f"{euros(argent_disponible)} €."
        )

    enonce = (
        "**Le jeu de piste du collège**\n\n"
        "Le collège organise un jeu de piste pour ses élèves.\n\n"

        f"{nb_equipes} équipes participent à l'activité.\n\n"

        f"Le parcours comporte {nb_postes} postes.\n\n"

        "Pour préparer le jeu :\n"
        "- chaque équipe reçoit une enveloppe d'indices "
        "à chaque poste ;\n"
        f"- chaque enveloppe coûte {euros(prix_enveloppe)} € ;\n"
        "- chaque équipe reçoit également une pochette "
        f"de matériel à {euros(prix_pochette)} € ;\n"
        f"- la signalisation du parcours coûte "
        f"{euros(signalisation)} €.\n\n"

        f"Le collège dispose d'un budget total de "
        f"**{euros(budget)} €**.\n\n"

        "Après les achats obligatoires, il aimerait "
        "offrir un souvenir supplémentaire à chaque équipe.\n\n"

        f"Chaque souvenir coûte {euros(prix_souvenir)} €.\n\n"

        "Cependant, le collège souhaite conserver "
        f"au moins **{euros(reserve)} €** de réserve.\n\n"

        "**Questions**\n\n"

        "1. Combien d'enveloppes d'indices faut-il "
        "préparer au total ?\n\n"

        "2. Quel est le coût total des achats "
        "obligatoires ? Écris une seule expression "
        "numérique avec des parenthèses.\n\n"

        "3. Combien d'argent reste-t-il après "
        "les achats obligatoires ?\n\n"

        "4. Combien coûteraient tous les souvenirs "
        "supplémentaires ?\n\n"

        "5. Le collège peut-il acheter ces souvenirs "
        "tout en conservant la réserve minimale ? "
        "De combien dépasse-t-il la somme nécessaire "
        "ou combien lui manque-t-il ?"
    )

    correction = (
        "**1. Nombre d'enveloppes**\n\n"

        f"{nb_equipes} × {nb_postes} "
        f"= {nb_enveloppes} enveloppes.\n\n"

        "**2. Coût des achats obligatoires**\n\n"

        f"Enveloppes : {nb_enveloppes} × "
        f"{euros(prix_enveloppe)} "
        f"= {euros(cout_enveloppes)} €.\n\n"

        f"Pochettes : {nb_equipes} × "
        f"{euros(prix_pochette)} "
        f"= {euros(cout_pochettes)} €.\n\n"

        f"Signalisation : {euros(signalisation)} €.\n\n"

        "**Expression complète :**\n\n"

        f"({nb_equipes} × {nb_postes} × "
        f"{euros(prix_enveloppe)} + "
        f"{nb_equipes} × {euros(prix_pochette)}) "
        f"+ {euros(signalisation)} "
        f"= {euros(depenses)} €.\n\n"

        "**3. Argent restant après les achats**\n\n"

        f"{euros(budget)} − {euros(depenses)} "
        f"= {euros(argent_disponible)} €.\n\n"

        "**4. Coût des souvenirs supplémentaires**\n\n"

        f"{nb_equipes} × {euros(prix_souvenir)} "
        f"= {euros(cout_souvenirs)} €.\n\n"

        "**5. Vérification du budget et de la réserve**\n\n"

        f"Souvenirs : {euros(cout_souvenirs)} €.\n\n"

        f"Réserve minimale : {euros(reserve)} €.\n\n"

        f"Somme nécessaire : "
        f"{euros(cout_souvenirs)} + {euros(reserve)} "
        f"= {euros(somme_necessaire)} €.\n\n"

        f"Argent disponible : "
        f"{euros(argent_disponible)} €.\n\n"

        f"Différence : {euros(difference)} €.\n\n"

        f"**Achat possible : {achat_possible}.**\n\n"

        f"{conclusion}"
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M05",
        "titre": "Le jeu de piste du collège",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Nombre d'enveloppes",
                "type": "nombre",
                "attendu": nb_enveloppes,
                "unite": "enveloppes"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Dépenses obligatoires",
                "type": "nombre",
                "attendu": depenses / 100,
                "unite": "€"
            },
            {
                "id": "expression",
                "question": 2,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Argent disponible après les achats",
                "type": "nombre",
                "attendu": argent_disponible / 100,
                "unite": "€"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Coût total des souvenirs",
                "type": "nombre",
                "attendu": cout_souvenirs / 100,
                "unite": "€"
            },
            {
                "id": "r5",
                "question": 5,
                "libelle": "Achat possible avec la réserve ?",
                "type": "choix",
                "attendu": achat_possible,
                "options": ["Oui", "Non"],
                "dependances": ["r3", "r4"]
            },
            {
                "id": "r6",
                "question": 5,
                "libelle": libelle_difference,
                "type": "nombre",
                "attendu": difference / 100,
                "unite": "€"
            }
        ]
    })

def generer_modele_p8_kits(seed=None):

    # Graine permettant de reproduire un exercice
    if seed is None:
        seed = random.randrange(1, 10**9)

    rng = random.Random(seed)

    # Différentes combinaisons de matériel
    articles = [
        (("carnet", "carnets"), ("stylo", "stylos")),
        (("cahier", "cahiers"), ("crayon", "crayons")),
        (("bloc-notes", "blocs-notes"), ("feutre", "feutres")),
        (("carte", "cartes"), ("badge", "badges"))
    ]

    (nom_a, nom_b) = rng.choice(articles)

    nb_equipes = rng.randint(4, 8)

    quantite_a = rng.randint(2, 4)
    prix_a = rng.randint(3, 7)

    quantite_b = rng.randint(2, 5)
    prix_b = rng.randint(1, 4)

    reduction = rng.choice([5, 10, 15, 20])
    livraison = rng.choice([4, 6, 8, 10, 12])

    # Calculs
    cout_a = quantite_a * prix_a
    cout_b = quantite_b * prix_b

    prix_kit = cout_a + cout_b
    prix_kits = nb_equipes * prix_kit

    # La réduction ne doit jamais dépasser
    # le prix de tous les kits
    reduction = min(reduction, prix_kits)

    total = prix_kits - reduction + livraison

    # Budget parfois suffisant, parfois insuffisant
    amplitude = min(rng.randint(4, 36), total - 5)
    variation = rng.choice([-1, 1]) * amplitude
    budget = total + variation

    difference = abs(variation)

    achat_possible = "Oui" if variation > 0 else "Non"

    # Accord singulier/pluriel
    article_a = nom_a[0] if quantite_a == 1 else nom_a[1]
    article_b = nom_b[0] if quantite_b == 1 else nom_b[1]

    if achat_possible == "Oui":
        conclusion = (
            f"Le budget est suffisant. "
            f"Il restera {difference} €."
        )
    else:
        conclusion = (
            f"Le budget est insuffisant. "
            f"Il manque {difference} €."
        )

    enonce = (
        "**Les kits du jeu de piste**\n\n"
        "Le collège prépare un jeu de piste.\n\n"

        f"Il y a {nb_equipes} équipes participantes.\n\n"

        "Chaque équipe doit recevoir un kit comprenant :\n"

        f"- {quantite_a} {article_a} à "
        f"{prix_a} € l'unité ;\n"

        f"- {quantite_b} {article_b} à "
        f"{prix_b} € l'unité.\n\n"

        f"Le magasin accorde une réduction de "
        f"{reduction} € sur la commande totale.\n\n"

        f"Les frais de livraison sont de {livraison} €.\n\n"

        f"Le collège dispose d'un budget de "
        f"**{budget} €**.\n\n"

        "**Questions**\n\n"

        "1. Combien coûte le matériel nécessaire "
        "pour une seule équipe ?\n\n"

        "2. Combien coûtent tous les kits "
        "avant la réduction et la livraison ?\n\n"

        "3. Quel est le montant total à payer "
        "après la réduction et les frais de livraison ? "
        "Écris une seule expression numérique "
        "avec des parenthèses.\n\n"

        "4. Le budget du collège est-il suffisant ? "
        "Quel est l'écart entre le budget "
        "et le montant à payer ?"
    )

    correction = (
        "**1. Prix du matériel pour une équipe**\n\n"

        f"{quantite_a} × {prix_a} + "
        f"{quantite_b} × {prix_b} "
        f"= {prix_kit} €.\n\n"

        "**2. Prix de tous les kits**\n\n"

        f"{nb_equipes} × {prix_kit} "
        f"= {prix_kits} €.\n\n"

        "**3. Montant à payer**\n\n"

        f"{prix_kits} − {reduction} + "
        f"{livraison} = {total} €.\n\n"

        "**Expression complète :**\n\n"

        f"{nb_equipes} × "
        f"({quantite_a} × {prix_a} + "
        f"{quantite_b} × {prix_b}) "
        f"− {reduction} + {livraison} "
        f"= {total} €.\n\n"

        "**4. Vérification du budget**\n\n"

        f"Budget disponible : {budget} €.\n\n"

        f"Montant à payer : {total} €.\n\n"

        f"Écart : {difference} €.\n\n"

        f"**Budget suffisant : {achat_possible}.**\n\n"

        f"{conclusion}"
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M06",
        "titre": "Les kits du jeu de piste",
        "seed": seed,
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Prix d'un kit",
                "type": "nombre",
                "attendu": prix_kit,
                "unite": "€"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Prix de tous les kits",
                "type": "nombre",
                "attendu": prix_kits,
                "unite": "€"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Montant total à payer",
                "type": "nombre",
                "attendu": total,
                "unite": "€"
            },
            {
                "id": "expression",
                "question": 3,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Budget suffisant ?",
                "type": "choix",
                "attendu": achat_possible,
                "options": ["Oui", "Non"],
                "dependances": ["r3"]
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": "Écart entre budget et montant à payer",
                "type": "nombre",
                "attendu": difference,
                "unite": "€"
            }
        ]
    })

def generer_modele_p8_eau(seed=None):

    if seed is None:
        seed = random.randrange(1, 10**9)

    rng = random.Random(seed)

    def litres(centilitres):
        return f"{centilitres / 100:.2f}".replace(".", ",")

    # Variation du contexte
    lieu = rng.choice([
        "le gymnase",
        "les vestiaires",
        "l'atelier de sciences",
        "le bâtiment principal"
    ])

    # Données aléatoires
    nb_robinets = rng.randint(4, 8)
    minutes_par_jour = rng.randint(6, 12)
    nb_jours = rng.choice([4, 5])

    # Débits exprimés en centilitres par minute
    debit_avant = rng.choice([100, 110, 120, 130, 140, 150])
    debit_apres = rng.choice([40, 50, 60, 70, 80])

    # Calculs effectués avec des nombres entiers
    minutes_totales = (
        nb_robinets * minutes_par_jour * nb_jours
    )

    consommation_avant = minutes_totales * debit_avant
    consommation_apres = minutes_totales * debit_apres

    economie = consommation_avant - consommation_apres

    # Objectif parfois atteint, parfois non
    # Écart de 1,80 à 13,00 litres, sans valeur finale prédéfinie.
    variation = rng.choice([-1, 1]) * rng.randrange(180, 1301, 10)
    objectif = economie + variation

    objectif_atteint = "Oui" if economie >= objectif else "Non"
    ecart = abs(economie - objectif)

    if objectif_atteint == "Oui":
        libelle_ecart = "Dépassement de l'objectif"
        conclusion = (
            f"L'objectif est atteint. "
            f"Le collège économise {litres(ecart)} L "
            "de plus que l'objectif."
        )
    else:
        libelle_ecart = "Manque pour atteindre l'objectif"
        conclusion = (
            f"L'objectif n'est pas atteint. "
            f"Il manque {litres(ecart)} L d'économies "
            "pour atteindre l'objectif."
        )
    enonce = (
        "**Le défi des économies d'eau**\n\n"

        "Le collège organise une semaine de sensibilisation "
        "aux économies d'eau.\n\n"

        f"Dans {lieu}, {nb_robinets} robinets sont utilisés "
        f"chacun {minutes_par_jour} minutes par jour "
        f"pendant {nb_jours} jours.\n\n"

        "Avant l'installation de nouveaux équipements, "
        "chaque robinet laisse couler "
        f"{litres(debit_avant)} litre d'eau par minute.\n\n"

        "Après l'installation d'économiseurs d'eau, "
        "chaque robinet laisse couler seulement "
        f"{litres(debit_apres)} litre par minute.\n\n"

        "La durée d'utilisation des robinets "
        "reste identique.\n\n"

        "Le collège souhaite économiser au moins "
        f"**{litres(objectif)} litres d'eau** "
        "sur cette période.\n\n"

        "**Questions**\n\n"

        "1. Quelle est la durée totale d'utilisation "
        "de tous les robinets pendant cette période, "
        "en minutes ?\n\n"

        "2. Quelle quantité d'eau aurait été consommée "
        "avec les anciens équipements, en litres ?\n\n"

        "3. Quelle quantité d'eau est consommée "
        "avec les nouveaux équipements, en litres ?\n\n"

        "4. Quelle quantité d'eau est économisée ? "
        "Écris une seule expression numérique "
        "avec des parenthèses.\n\n"

        "5. Le collège a-t-il atteint son objectif ? "
        "De combien le dépasse-t-il ou "
        "combien lui manque-t-il ?"
    )

    correction = (
        "**1. Durée totale d'utilisation**\n\n"

        f"{nb_robinets} × {minutes_par_jour} × "
        f"{nb_jours} = {minutes_totales} minutes.\n\n"

        "**2. Consommation avant les économies**\n\n"

        f"{minutes_totales} × {litres(debit_avant)} "
        f"= {litres(consommation_avant)} L.\n\n"

        "**3. Consommation après les économies**\n\n"

        f"{minutes_totales} × {litres(debit_apres)} "
        f"= {litres(consommation_apres)} L.\n\n"

        "**4. Quantité d'eau économisée**\n\n"

        f"{litres(consommation_avant)} − "
        f"{litres(consommation_apres)} "
        f"= {litres(economie)} L.\n\n"

        "**Expression complète :**\n\n"

        f"{nb_robinets} × {minutes_par_jour} × "
        f"{nb_jours} × "
        f"({litres(debit_avant)} − {litres(debit_apres)}) "
        f"= {litres(economie)} L.\n\n"

        "**5. Vérification de l'objectif**\n\n"

        f"Économies réalisées : {litres(economie)} L.\n\n"

        f"Objectif : {litres(objectif)} L.\n\n"

        f"Écart : {litres(ecart)} L.\n\n"

        f"**Objectif atteint : {objectif_atteint}.**\n\n"

        f"{conclusion}"
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M07",
        "titre": "Le défi des économies d'eau",
        "seed": seed,
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Durée totale d'utilisation",
                "type": "nombre",
                "attendu": minutes_totales,
                "unite": "minutes"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Consommation avec les anciens équipements",
                "type": "nombre",
                "attendu": consommation_avant / 100,
                "unite": "L"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Consommation avec les nouveaux équipements",
                "type": "nombre",
                "attendu": consommation_apres / 100,
                "unite": "L"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Quantité d'eau économisée",
                "type": "nombre",
                "attendu": economie / 100,
                "unite": "L"
            },
            {
                "id": "expression",
                "question": 4,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r5",
                "question": 5,
                "libelle": "Objectif atteint ?",
                "type": "choix",
                "attendu": objectif_atteint,
                "options": ["Oui", "Non"],
                "dependances": ["r4"]
            },
            {
                "id": "r6",
                "question": 5,
                "libelle": libelle_ecart,
                "type": "nombre",
                "attendu": ecart / 100,
                "unite": "L"
            }
        ]
    })

def generer_modele_p8_parcours(seed=None):
    """Distances, durées de marche et comparaison à un objectif."""
    if seed is None:
        seed = random.randrange(1, 10**9)
    rng = random.Random(seed)

    lieu = rng.choice([
        "le parc naturel", "la forêt communale",
        "le sentier botanique", "les environs du collège"
    ])
    nb_tours = rng.choice([2, 3])
    longueur_a_demi_km = rng.randint(2, 5)
    longueur_b_demi_km = rng.randint(1, 4)
    minutes_par_km = 12
    pause_minutes = rng.choice([6, 8, 10, 12])

    distance_un_tour = (
        longueur_a_demi_km + longueur_b_demi_km
    ) / 2
    distance_totale = nb_tours * distance_un_tour
    temps_marche = round(distance_totale * minutes_par_km)
    nb_pauses = nb_tours - 1
    temps_pause = nb_pauses * pause_minutes
    duree_totale = temps_marche + temps_pause

    detour_demi_km = rng.randint(1, 4)
    distance_detour = detour_demi_km / 2
    temps_detour = int(distance_detour * minutes_par_km)
    duree_avec_detour = duree_totale + temps_detour
    variation = rng.choice([-1, 1]) * rng.randint(4, 29)
    temps_maximal = duree_avec_detour + variation
    objectif_atteint = (
        "Oui" if duree_avec_detour <= temps_maximal else "Non"
    )
    ecart = abs(duree_avec_detour - temps_maximal)

    def km(valeur):
        return f"{valeur:.1f}".replace(".", ",")

    if objectif_atteint == "Oui":
        libelle_ecart = "Minutes d'avance sur la limite"
        conclusion = (
            f"Avec le détour, le groupe respecte la limite et termine "
            f"avec {ecart} minutes d'avance."
        )
    else:
        libelle_ecart = "Minutes de dépassement"
        conclusion = (
            f"Avec le détour, le groupe dépasse la limite de {ecart} minutes."
        )

    enonce = (
        "**Le parcours nature du collège**\n\n"
        f"Une classe participe à une randonnée dans {lieu}.\n\n"
        "Chaque tour du parcours comprend deux parties :\n"
        f"- un premier chemin de {km(longueur_a_demi_km / 2)} km ;\n"
        f"- un second chemin de {km(longueur_b_demi_km / 2)} km.\n\n"
        f"Les élèves effectuent **{nb_tours} tours complets**.\n\n"
        f"Ils marchent à une allure régulière de {minutes_par_km} minutes "
        "par kilomètre.\n\n"
        f"Entre deux tours, ils font une pause de {pause_minutes} minutes. "
        f"Ils ne font pas de pause après le dernier tour.\n\n"
        f"Après le parcours, ils envisagent un détour d’observation de "
        f"{km(distance_detour)} km, effectué à la même allure et sans pause.\n\n"
        f"Le groupe souhaite terminer le parcours en **{temps_maximal} "
        "minutes au maximum**, pauses comprises.\n\n"
        "**Questions**\n\n"
        "1. Quelle est la distance d'un tour complet, en kilomètres ?\n\n"
        "2. Quelle distance parcourent-ils pendant tous les tours ?\n\n"
        "3. Combien de minutes passent-ils à marcher ?\n\n"
        "4. Quelle est la durée totale, pauses comprises ? "
        "Écris une seule expression numérique avec des parenthèses.\n\n"
        "5. Respectent-ils le temps maximal prévu ? "
        "De combien de minutes sont-ils en avance ou en retard ?"
    )

    correction = (
        "**1. Distance d'un tour**\n\n"
        f"{km(longueur_a_demi_km / 2)} + {km(longueur_b_demi_km / 2)} "
        f"= {km(distance_un_tour)} km.\n\n"
        "**2. Distance totale parcourue**\n\n"
        f"{nb_tours} × {km(distance_un_tour)} "
        f"= {km(distance_totale)} km.\n\n"
        "**3. Temps de marche**\n\n"
        f"{km(distance_totale)} × {minutes_par_km} "
        f"= {temps_marche} minutes.\n\n"
        "**4. Durée totale avec les pauses**\n\n"
        f"Nombre de pauses : {nb_tours} − 1 = {nb_pauses}.\n\n"
        f"Durée des pauses : {nb_pauses} × {pause_minutes} "
        f"= {temps_pause} minutes.\n\n"
        f"Durée totale : {temps_marche} + {temps_pause} "
        f"= {duree_totale} minutes.\n\n"
        "**Expression complète :**\n\n"
        f"{nb_tours} × ({km(longueur_a_demi_km / 2)} + "
        f"{km(longueur_b_demi_km / 2)}) × {minutes_par_km} "
        f"+ ({nb_tours} − 1) × {pause_minutes} "
        f"= {duree_totale}.\n\n"
        "**5. Détour d’observation et durée maximale**\n\n"
        f"Temps du détour : {km(distance_detour)} × {minutes_par_km} "
        f"= {temps_detour} minutes.\n\n"
        f"Durée totale avec détour : {duree_totale} + {temps_detour} "
        f"= {duree_avec_detour} minutes.\n\n"
        f"Limite : {temps_maximal} minutes.\n\n"
        f"Écart : {ecart} minutes.\n\n"
        f"**Objectif atteint : {objectif_atteint}.**\n\n"
        f"{conclusion}"
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M08",
        "titre": "Le parcours nature du collège",
        "seed": seed,
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Distance d'un tour",
                "type": "nombre",
                "attendu": distance_un_tour,
                "unite": "km"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Distance totale",
                "type": "nombre",
                "attendu": distance_totale,
                "unite": "km"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Durée de marche",
                "type": "nombre",
                "attendu": temps_marche,
                "unite": "minutes"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Durée totale avec les pauses",
                "type": "nombre",
                "attendu": duree_totale,
                "unite": "minutes"
            },
            {
                "id": "expression",
                "question": 4,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r5",
                "question": 5,
                "libelle": "Temps maximal respecté ?",
                "type": "choix",
                "attendu": objectif_atteint,
                "options": ["Oui", "Non"],
                "dependances": ["r4"]
            },
            {
                "id": "r6",
                "question": 5,
                "libelle": libelle_ecart,
                "type": "nombre",
                "attendu": ecart,
                "unite": "minutes"
            }
        ]
    })

def generer_modele_p8_boissons(seed=None):
    """Mélanges en cL, conversion en L et division avec reste."""
    if seed is None:
        seed = random.randrange(1, 10**9)
    rng = random.Random(seed)

    parfums = rng.choice([
        ("jus de pomme", "jus d'orange"),
        ("jus d'ananas", "jus de mangue"),
        ("jus de raisin", "jus de poire")
    ])

    while True:
        nombre_preparations = rng.randint(4, 7)
        quantite_a = rng.randrange(45, 76, 5)
        quantite_b = rng.randrange(25, 56, 5)
        quantite_eau = rng.randrange(20, 46, 5)
        capacite_bouteille = rng.choice([50, 75])

        volume_preparation = (
            quantite_a + quantite_b + quantite_eau
        )
        volume_total = nombre_preparations * volume_preparation

        bouteilles_pleines, reste_cl = divmod(
            volume_total, capacite_bouteille
        )

        if (
            5 <= bouteilles_pleines <= 22
            and 1 <= reste_cl < capacite_bouteille
        ):
            break

    bouteilles_necessaires = bouteilles_pleines + 1
    bouteilles_par_lot = rng.choice([3, 4, 5, 6])
    lots_necessaires = (bouteilles_necessaires + bouteilles_par_lot - 1) // bouteilles_par_lot

    def litres(centilitres):
        return f"{centilitres / 100:.2f}".replace(".", ",")

    enonce = (
        "**L'atelier de boissons du collège**\n\n"
        "Pour une journée sportive, les élèves préparent une boisson "
        "sans alcool à base de fruits et d'eau.\n\n"
        "Pour **une préparation**, ils mélangent :\n"
        f"- {quantite_a} cL de {parfums[0]} ;\n"
        f"- {quantite_b} cL de {parfums[1]} ;\n"
        f"- {quantite_eau} cL d'eau.\n\n"
        f"Ils réalisent **{nombre_preparations} préparations identiques**.\n\n"
        f"Ils souhaitent utiliser des bouteilles de {capacite_bouteille} cL chacune. "
        "Ils remplissent d'abord le plus grand nombre possible de bouteilles "
        "complètes, puis mettent le reste dans une dernière bouteille.\n\n"
        f"Les bouteilles vides s’achètent par lots de {bouteilles_par_lot}. "
        "Il faut disposer de suffisamment de bouteilles pour toute la boisson.\n\n"
        "**Questions**\n\n"
        "1. Quel volume de boisson obtiennent-ils avec une seule "
        "préparation, en cL ?\n\n"
        "2. Quel volume total de boisson préparent-ils, en litres ? "
        "Écris une seule expression numérique avec des parenthèses.\n\n"
        "3. Combien de bouteilles peuvent-ils remplir complètement ?\n\n"
        "4. Combien de cL versent-ils dans la dernière bouteille ? "
        "Combien de bouteilles utilisent-ils au total ?"
    )

    correction = (
        "**1. Volume d'une préparation**\n\n"
        f"{quantite_a} + {quantite_b} + {quantite_eau} "
        f"= {volume_preparation} cL.\n\n"
        "**2. Volume total produit**\n\n"
        f"{nombre_preparations} × {volume_preparation} "
        f"= {volume_total} cL.\n\n"
        f"Conversion : {volume_total} cL "
        f"= {litres(volume_total)} L.\n\n"
        "**Expression complète :**\n\n"
        f"{nombre_preparations} × ({quantite_a} + {quantite_b} + "
        f"{quantite_eau}) ÷ 100 = {litres(volume_total)} L.\n\n"
        "**3. Bouteilles entièrement remplies**\n\n"
        f"{volume_total} : {capacite_bouteille} — "
        f"Quotient : {bouteilles_pleines} — "
        f"Reste : {reste_cl}\n\n"
        f"Il est possible de remplir **{bouteilles_pleines} bouteilles** "
        "entièrement.\n\n"
        "**4. Dernière bouteille et total**\n\n"
        f"Il reste {reste_cl} cL, versés dans une dernière bouteille.\n\n"
        f"Nombre total : {bouteilles_pleines} + 1 "
        f"= **{bouteilles_necessaires} bouteilles**.\n\n"
        "**5. Lots de bouteilles à acheter**\n\n"
        f"{bouteilles_necessaires} ÷ {bouteilles_par_lot} : quotient entier "
        f"{bouteilles_necessaires // bouteilles_par_lot}, "
        f"reste {bouteilles_necessaires % bouteilles_par_lot}.\n\n"
        f"Il faut **{lots_necessaires} lots** de bouteilles au minimum."
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M09",
        "titre": "L'atelier de boissons du collège",
        "seed": seed,
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Volume d'une préparation",
                "type": "nombre",
                "attendu": volume_preparation,
                "unite": "cL"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Volume total",
                "type": "nombre",
                "attendu": volume_total / 100,
                "unite": "L"
            },
            {
                "id": "expression",
                "question": 2,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Bouteilles entièrement remplies",
                "type": "nombre",
                "attendu": bouteilles_pleines,
                "unite": "bouteilles"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Volume de la dernière bouteille",
                "type": "nombre",
                "attendu": reste_cl,
                "unite": "cL"
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": "Lots de bouteilles à acheter",
                "type": "nombre",
                "attendu": lots_necessaires,
                "unite": "lots"
            }
        ]
    })

def generer_modele_p8_transport(seed=None):
    """Distance d'un aller-retour et comparaison de deux tarifs."""
    if seed is None:
        seed = random.randrange(1, 10**9)
    rng = random.Random(seed)

    evenement = rng.choice([
        "le spectacle de théâtre",
        "le festival des sciences",
        "la journée des associations",
        "l'exposition du collège"
    ])

    while True:
        distance_aller = rng.randint(3, 11)
        distance_detour = rng.randint(1, 4)
        distance_totale = 2 * distance_aller + distance_detour

        fixe_a = rng.randint(25, 45)
        prix_km_a = rng.randint(2, 3)
        fixe_b = rng.randint(5, 16)
        prix_km_b = rng.randint(4, 5)

        cout_a = fixe_a + distance_totale * prix_km_a
        cout_b = fixe_b + distance_totale * prix_km_b
        difference = abs(cout_a - cout_b)

        if 3 <= difference <= 60:
            break

    meilleur = "A" if cout_a < cout_b else "B"

    enonce = (
        "**Le transport du matériel**\n\n"
        f"Le collège doit transporter du matériel pour {evenement}.\n\n"
        f"Le lieu de l'événement se trouve à {distance_aller} km du collège. "
        "Le véhicule fait l'aller-retour par le même trajet, "
        "mais, sur l'ensemble de l'aller-retour, un seul détour ajoute "
        f"{distance_detour} km pour récupérer des accessoires.\n\n"
        "Deux entreprises proposent de louer un véhicule. "
        "Les tarifs comprennent tout le transport.\n\n"
        "**Entreprise A**\n\n"
        f"- Frais fixes : {fixe_a} € ;\n"
        f"- Prix par kilomètre parcouru : {prix_km_a} €.\n\n"
        "**Entreprise B**\n\n"
        f"- Frais fixes : {fixe_b} € ;\n"
        f"- Prix par kilomètre parcouru : {prix_km_b} €.\n\n"
        "**Questions**\n\n"
        "1. Quelle est la distance totale parcourue par le véhicule, "
        "en kilomètres ?\n\n"
        "2. Quel est le coût total avec l'entreprise A ? "
        "Écris une expression numérique avec des parenthèses.\n\n"
        "3. Quel est le coût total avec l'entreprise B ?\n\n"
        "4. Quelle entreprise est la moins chère ? "
        "Combien d'euros le collège économise-t-il en la choisissant ?"
    )

    correction = (
        "**1. Distance parcourue**\n\n"
        f"2 × {distance_aller} + {distance_detour} "
        f"= {distance_totale} km.\n\n"
        "**2. Coût avec l'entreprise A**\n\n"
        f"{fixe_a} + {distance_totale} × {prix_km_a} "
        f"= {cout_a} €.\n\n"
        "**Expression complète :**\n\n"
        f"{fixe_a} + (2 × {distance_aller} + {distance_detour}) "
        f"× {prix_km_a} = {cout_a} €.\n\n"
        "**3. Coût avec l'entreprise B**\n\n"
        f"{fixe_b} + {distance_totale} × {prix_km_b} "
        f"= {cout_b} €.\n\n"
        "**4. Comparaison des tarifs**\n\n"
        f"Entreprise A : {cout_a} €.\n\n"
        f"Entreprise B : {cout_b} €.\n\n"
        f"Différence : {difference} €.\n\n"
        f"**L'entreprise {meilleur} est la moins chère.** "
        f"Elle permet d'économiser {difference} €."
    )

    return _mc_uniformiser_exercice({
        "id": "P8-M10",
        "titre": "Le transport du matériel",
        "seed": seed,
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Distance totale",
                "type": "nombre",
                "attendu": distance_totale,
                "unite": "km"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Coût de l'entreprise A",
                "type": "nombre",
                "attendu": cout_a,
                "unite": "€"
            },
            {
                "id": "expression",
                "question": 2,
                "libelle": "Mon expression avec parenthèses",
                "type": "texte_libre"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Coût de l'entreprise B",
                "type": "nombre",
                "attendu": cout_b,
                "unite": "€"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Entreprise la moins chère",
                "type": "choix",
                "attendu": meilleur,
                "options": ["A", "B"],
                "dependances": ["r2", "r3"]
            },
            {
                "id": "r5",
                "question": 4,
                "libelle": "Économie réalisée",
                "type": "nombre",
                "attendu": difference,
                "unite": "€"
            }
        ]
    })

def _p9_rng(seed):
    if seed is None:
        seed = random.randrange(1, 10**9)
    return random.Random(seed), seed


def _p9_nombre(identifiant, numero, libelle, valeur, unite):
    return {
        "id": identifiant,
        "question": numero,
        "libelle": libelle,
        "type": "nombre",
        "attendu": valeur,
        "unite": unite
    }


def _p9_choix(identifiant, numero, libelle, valeur, dependances):
    return {
        "id": identifiant,
        "question": numero,
        "libelle": libelle,
        "type": "choix",
        "attendu": valeur,
        "options": (
            ["A", "B"] if valeur in ("A", "B")
            else ["Oui", "Non"]
        ),
        "dependances": dependances
    }


def _p9_expression(numero):
    return {
        "id": "expression",
        "question": numero,
        "libelle": "Mon expression avec parenthèses",
        "type": "texte_libre"
    }


def _p9_exercice(identifiant, titre, seed, enonce, correction, champs):
    return {
        "id": identifiant,
        "titre": titre,
        "seed": seed,
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": champs
    }

def generer_modele_p9_potager(seed=None):
    rng, seed = _p9_rng(seed)

    while True:
        parcelles = rng.randint(3, 6)
        plants_a = rng.randint(6, 10)
        plants_b = rng.randint(7, 12)
        prix_a = rng.randint(2, 5)
        prix_b = rng.randint(2, 5)
        materiel_a = rng.randint(35, 85)
        materiel_b = rng.randint(35, 85)

        quantite_a = parcelles * plants_a
        quantite_b = parcelles * plants_b
        cout_a = quantite_a * prix_a + materiel_a
        cout_b = quantite_b * prix_b + materiel_b

        ecart = abs(cout_a - cout_b)

        # Les projets doivent présenter un vrai arbitrage entre plants et matériel.
        # Rejette tout tirage où un seul projet est moins cher sur les deux postes.
        cout_plants_a = quantite_a * prix_a
        cout_plants_b = quantite_b * prix_b
        arbitrage_reel = (cout_plants_a - cout_plants_b) * (materiel_a - materiel_b) < 0
        if 10 <= ecart <= 125 and plants_a != plants_b and arbitrage_reel:
            break

    budget = max(cout_a, cout_b) + rng.randint(20, 70)
    meilleur = "A" if cout_a < cout_b else "B"
    reste_budget = budget - min(cout_a, cout_b)

    enonce = (
        "**Le potager du collège**\n\n"
        f"Le collège prépare **{parcelles} parcelles identiques** "
        "et hésite entre deux projets de plantation.\n\n"

        "**Projet A**\n\n"
        f"- {plants_a} plants par parcelle, à {prix_a} € le plant ;\n"
        f"- {materiel_a} € de matériel complémentaire.\n\n"

        "**Projet B**\n\n"
        f"- {plants_b} plants par parcelle, à {prix_b} € le plant ;\n"
        f"- {materiel_b} € de matériel complémentaire.\n\n"

        f"Le budget disponible est de **{budget} €**. Les deux projets "
        "permettent d'aménager toutes les parcelles.\n\n"

        "Le collège choisira **le projet le moins coûteux**.\n\n"

        "**Questions**\n\n"

        "1. Combien de plants faut-il pour chacun des projets ?\n\n"

        "2. Quel est le coût total du projet A ? Écris une expression "
        "numérique avec des parenthèses.\n\n"

        "3. Quel est le coût total du projet B ?\n\n"

        "4. Quel projet est le moins coûteux ? Combien d'euros "
        "économise-t-on par rapport à l'autre projet ?\n\n"

        "5. Combien d'euros reste-t-il du budget après avoir "
        "choisi ce projet ?"
    )

    correction = (
        "**1. Nombre de plants**\n\n"
        f"A : {parcelles} × {plants_a} = {quantite_a} plants.\n\n"
        f"B : {parcelles} × {plants_b} = {quantite_b} plants.\n\n"

        "**2. Coût total du projet A**\n\n"
        f"({parcelles} × {plants_a} × {prix_a}) + {materiel_a} "
        f"= {cout_a} €.\n\n"

        "**3. Coût total du projet B**\n\n"
        f"({parcelles} × {plants_b} × {prix_b}) + {materiel_b} "
        f"= {cout_b} €.\n\n"

        "**4. Comparaison des projets**\n\n"
        f"A : {cout_a} € ; B : {cout_b} €.\n\n"
        f"Différence : {max(cout_a, cout_b)} − {min(cout_a, cout_b)} "
        f"= {ecart} €.\n\n"
        f"**Le projet {meilleur} est le moins coûteux.**\n\n"

        "**5. Budget restant**\n\n"
        f"{budget} − {min(cout_a, cout_b)} = {reste_budget} €."
    )

    champs = [
        _p9_nombre("r1", 1, "Plants pour le projet A", quantite_a, "plants"),
        _p9_nombre("r2", 1, "Plants pour le projet B", quantite_b, "plants"),
        _p9_nombre("r3", 2, "Coût du projet A", cout_a, "€"),
        _p9_expression(2),
        _p9_nombre("r4", 3, "Coût du projet B", cout_b, "€"),
        _p9_choix(
            "r5", 4, "Projet le moins coûteux",
            meilleur, ["r3", "r4"]
        ),
        _p9_nombre("r6", 4, "Économie réalisée", ecart, "€"),
        _p9_nombre("r7", 5, "Budget restant", reste_budget, "€")
    ]

    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M01", "Le potager du collège",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_tournoi(seed=None):
    rng, seed = _p9_rng(seed)

    while True:
        joueurs = rng.randint(24, 42)
        entree = rng.randint(5, 8)
        sponsor = rng.randint(35, 75)
        prix = rng.randint(45, 85)

        location_a = rng.randint(30, 75)
        location_b = rng.randint(60, 110)
        # Compromis réel : A moins cher en fixe, B moins cher par joueur.
        fournitures_a = rng.choice([2, 3])
        fournitures_b = 1
        if not (location_a < location_b and
                24 <= (location_b - location_a) / (fournitures_a - fournitures_b) <= 42):
            continue

        recettes = joueurs * entree + sponsor
        depenses_a = prix + location_a + joueurs * fournitures_a
        depenses_b = prix + location_b + joueurs * fournitures_b

        benefice_a = recettes - depenses_a
        benefice_b = recettes - depenses_b
        ecart = abs(benefice_a - benefice_b)

        if min(benefice_a, benefice_b) >= 20 and 8 <= ecart <= 95:
            break

    meilleur = "A" if benefice_a > benefice_b else "B"
    objectif = min(benefice_a, benefice_b) + ecart // 2
    manque_objectif = objectif - min(benefice_a, benefice_b)

    enonce = (
        "**Le tournoi de jeux vidéo**\n\n"   
        "Le collège souhaite organiser un tournoi de jeux vidéo "
        "pour financer un projet.\n\n"
        "Il envisage de confier l'organisation à l'un de deux "
        "prestataires. Chacun propose un tarif comprenant "
        "la location de la salle et les fournitures.\n\n"

        f"**{joueurs} joueurs** participent et versent chacun "
        f"**{entree} €** d'inscription. Un partenaire offre "
        f"**{sponsor} €** au club.\n\n"

        f"Les récompenses coûtent **{prix} €**, quelle que soit "
        "l'organisation choisie.\n\n"

        "**Organisateur A — Proposition**\n\n"
        f"- Location : {location_a} € ;\n"
        f"- Fournitures : {fournitures_a} € par joueur.\n\n"

        "**Organisateur B — Proposition**\n\n"
        f"- Location : {location_b} € ;\n"
        f"- Fournitures : {fournitures_b} € par joueur.\n\n"

        "Le club veut choisir l'organisation qui laisse "
        "**le bénéfice le plus élevé**.\n\n"

        "**Questions**\n\n"

        "1. Quelles sont les recettes totales du tournoi ?\n\n"

        "2. Quelles sont les dépenses totales de chaque organisation, "
        "récompenses comprises ?\n\n"

        "3. Quel bénéfice reste-t-il avec l'organisation A et avec "
        "l'organisation B ? Écris une expression numérique avec "
        "des parenthèses pour le bénéfice de A.\n\n"

        "4. Quelle organisation donne le plus grand bénéfice ? "
        "De combien d'euros est-il supérieur à l'autre ?\n\n"
        
        f"5. Le collège souhaite obtenir un bénéfice d'au moins "
        f"{objectif} €. Si le collège retenait malgré tout "
        "l'organisateur le moins rentable, de combien faudrait-il "
        "augmenter les recettes du tournoi, sans modifier les "
        "dépenses, pour atteindre cet objectif ?"

    )

    correction = (
        "**1. Recettes**\n\n"
        f"{joueurs} × {entree} + {sponsor} = {recettes} €.\n\n"

        "**2. Dépenses des organisations**\n\n"
        f"A : {prix} + {location_a} + {joueurs} × {fournitures_a} "
        f"= {depenses_a} €.\n\n"
        f"B : {prix} + {location_b} + {joueurs} × {fournitures_b} "
        f"= {depenses_b} €.\n\n"

        "**3. Bénéfices**\n\n"
        f"A : {recettes} − {depenses_a} = {benefice_a} €.\n\n"
        f"B : {recettes} − {depenses_b} = {benefice_b} €.\n\n"

        "**Expression complète pour A :**\n\n"
        f"({joueurs} × {entree} + {sponsor}) − "
        f"({prix} + {location_a} + {joueurs} × {fournitures_a}) "
        f"= {benefice_a} €.\n\n"

        "**4. Meilleure organisation**\n\n"
        f"Écart : {max(benefice_a, benefice_b)} − "
        f"{min(benefice_a, benefice_b)} = {ecart} €.\n\n"
        f"**L'organisation {meilleur} est la plus avantageuse.**\n\n"

        "**5. Vérification de l'objectif**\n\n"
        f"Bénéfice minimal souhaité : {objectif} €.\n\n"
        f"Bénéfice de l'organisation la moins rentable : "
        f"{min(benefice_a, benefice_b)} €.\n\n"
        f"Montant manquant : {objectif} − "
        f"{min(benefice_a, benefice_b)} "
        f"= **{manque_objectif} €**.\n\n"
        "Cette organisation doit donc augmenter ses recettes "
        f"de {manque_objectif} € pour atteindre l'objectif."
    )

    champs = [
        _p9_nombre("r1", 1, "Recettes totales", recettes, "€"),
        _p9_nombre("r2", 2, "Dépenses de A", depenses_a, "€"),
        _p9_nombre("r3", 2, "Dépenses de B", depenses_b, "€"),
        _p9_nombre("r4", 3, "Bénéfice de A", benefice_a, "€"),
        _p9_nombre("r5", 3, "Bénéfice de B", benefice_b, "€"),
        _p9_expression(3),
        _p9_choix(
            "r6", 4, "Organisation la plus avantageuse",
            meilleur, ["r4", "r5"]
        ),
        _p9_nombre("r7", 4, "Écart entre les bénéfices", ecart, "€"),
        _p9_nombre(
            "r8", 5, "Recettes supplémentaires nécessaires",
            manque_objectif, "€"
        )
    ]

    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M02", "Le tournoi de jeux vidéo",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_festival(seed=None):
    rng, seed = _p9_rng(seed)

    while True:
        eleves = rng.randint(22, 34)
        adultes = rng.randint(2, 4)
        personnes = eleves + adultes

        km_aller = rng.randint(12, 30)
        km_total = km_aller * 2

        billets = rng.randint(4, 7)
        repas = rng.randint(5, 8)

        fixe_a = rng.randint(160, 240)
        prix_km_a = rng.randint(2, 4)
        fixe_b = rng.randint(80, 150)
        prix_personne_b = rng.randint(7, 11)

        frais_communs = personnes * (billets + repas)
        bus_a = fixe_a + km_total * prix_km_a
        bus_b = fixe_b + personnes * prix_personne_b

        cout_a = bus_a + frais_communs
        cout_b = bus_b + frais_communs
        ecart = abs(cout_a - cout_b)

        if 12 <= ecart <= 170:
            break

    meilleur = "A" if cout_a < cout_b else "B"

    enonce = (
        "**Une sortie au festival du manga**\n\n"

        f"Une classe de **{eleves} élèves**, accompagnée de "
        f"**{adultes} adultes**, se rend à un festival du manga "
        f"situé à **{km_aller} km** du collège.\n\n"

        "Le car effectue l'aller-retour par le même trajet.\n\n"

        f"Chaque personne paie {billets} € d'entrée au festival "
        f"et {repas} € pour le repas.\n\n"

        "Deux compagnies proposent le transport :\n\n"

        "**Transport A**\n\n"
        f"- Frais fixes : {fixe_a} € ;\n"
        f"- {prix_km_a} € par kilomètre parcouru.\n\n"

        "**Transport B**\n\n"
        f"- Frais fixes : {fixe_b} € ;\n"
        f"- {prix_personne_b} € par personne transportée "
        "pour l'ensemble de l'aller-retour.\n\n"

        "On choisira la formule donnant le **coût global le plus bas**, "
        "transport, entrées et repas compris.\n\n"

        "**Questions**\n\n"

        "1. Combien de personnes participent à la sortie ?\n\n"

        "2. Quelle distance le car parcourt-il au total ?\n\n"

        "3. Quel est le coût commun des entrées et des repas ?\n\n"

        "4. Quel est le coût global avec A, puis avec B ? "
        "Écris une expression numérique avec des parenthèses pour A.\n\n"

        "5. Quelle formule est la moins chère ? "
        "Combien d'euros permet-elle d'économiser ?"
    )

    correction = (
        "**1. Nombre de participants**\n\n"
        f"{eleves} + {adultes} = {personnes} personnes.\n\n"

        "**2. Distance aller-retour**\n\n"
        f"2 × {km_aller} = {km_total} km.\n\n"

        "**3. Entrées et repas**\n\n"
        f"{personnes} × ({billets} + {repas}) = {frais_communs} €.\n\n"

        "**4. Coûts globaux**\n\n"
        f"Transport A : {fixe_a} + {km_total} × {prix_km_a} "
        f"= {bus_a} €.\n\n"

        f"Transport B : {fixe_b} + {personnes} × {prix_personne_b} "
        f"= {bus_b} €.\n\n"

        f"A, entrées et repas compris : {bus_a} + {frais_communs} "
        f"= {cout_a} €.\n\n"

        f"B, entrées et repas compris : {bus_b} + {frais_communs} "
        f"= {cout_b} €.\n\n"

        "**Expression complète pour A :**\n\n"
        f"({fixe_a} + 2 × {km_aller} × {prix_km_a}) + "
        f"({eleves} + {adultes}) × ({billets} + {repas}) "
        f"= {cout_a} €.\n\n"

        "**5. Comparaison**\n\n"
        f"Écart : {max(cout_a, cout_b)} − {min(cout_a, cout_b)} "
        f"= {ecart} €.\n\n"

        f"**La formule {meilleur} est la moins chère.**"
    )

    champs = [
        _p9_nombre("r1", 1, "Nombre de participants", personnes, "personnes"),
        _p9_nombre("r2", 2, "Distance aller-retour", km_total, "km"),
        _p9_nombre("r3", 3, "Entrées et repas", frais_communs, "€"),
        _p9_nombre("r4", 4, "Coût global avec A", cout_a, "€"),
        _p9_nombre("r5", 4, "Coût global avec B", cout_b, "€"),
        _p9_expression(4),
        _p9_choix(
            "r6", 5, "Formule la moins chère",
            meilleur, ["r4", "r5"]
        ),
        _p9_nombre("r7", 5, "Économie réalisée", ecart, "€")
    ]

    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M03", "Une sortie au festival du manga",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_cristaux(seed=None):
    rng, seed = _p9_rng(seed)

    while True:
        stock = rng.randint(40, 85)
        missions = rng.randint(3, 6)
        gain_mission = rng.randint(9, 17)
        bonus = rng.randint(8, 20)
        perte = rng.randint(5, 14)
        prix_equipement = rng.randint(15, 25)
        reserve = rng.randint(10, 20)

        gains = missions * gain_mission + bonus
        disponibles = stock + gains - perte

        maximum = (disponibles - reserve) // prix_equipement
        reste = disponibles - maximum * prix_equipement

        if 3 <= maximum <= 9 and reserve <= reste < reserve + prix_equipement:
            break

    aventuriers = max(1, maximum + rng.choice([-2, -1, 1, 2]))
    possible = "Oui" if maximum >= aventuriers else "Non"
    ecart = abs(maximum - aventuriers)

    libelle = (
        "Équipements supplémentaires possibles"
        if possible == "Oui"
        else "Équipements manquants"
    )

    if possible == "Oui":
        conclusion = (
            f"Les {aventuriers} aventuriers peuvent être équipés. "
            f"En achetant seulement les équipements nécessaires "
            f"à l'équipe, le joueur pourrait en acheter {ecart} "
            "de plus tout en conservant la réserve."
        )
    else:
        conclusion = (
            f"Le joueur ne peut équiper que {maximum} aventurier(s). "
            f"Il manque {ecart} équipement(s) pour tous les équiper."
        )

    enonce = (
        "**Les cristaux du jeu vidéo**\n\n"

        f"Un joueur possède **{stock} cristaux** au départ.\n\n"

        f"Il termine **{missions} missions** qui rapportent chacune "
        f"**{gain_mission} cristaux**, puis reçoit un bonus unique "
        f"de **{bonus} cristaux**.\n\n"

        f"Un piège lui fait perdre {perte} cristaux.\n\n"

        f"Un équipement coûte **{prix_equipement} cristaux**. "
        f"Le joueur veut conserver au moins **{reserve} cristaux** "
        "après ses achats.\n\n"

        f"Son équipe comprend **{aventuriers} aventuriers**, "
        "et chacun doit recevoir un équipement.\n\n"

        "**Questions**\n\n"

        "1. Combien de cristaux gagne-t-il pendant les missions, "
        "bonus compris ?\n\n"

        "2. Combien de cristaux possède-t-il après le piège, "
        "avant d'acheter les équipements ? Écris une seule "
        "expression numérique avec des parenthèses.\n\n"

        "3. Combien d'équipements au maximum peut-il acheter "
        "en conservant la réserve minimale ?\n\n"

        "4. Combien de cristaux lui restera-t-il après "
        "l'achat de ce nombre maximal d'équipements ?\n\n"

        "5. Peut-il équiper tous les aventuriers ? "
        "S'il peut équiper tout le monde, combien d'équipements "
        "supplémentaires pourrait-il acheter ? Sinon, combien "
        "d'équipements lui manque-t-il ?"
    )

    correction = (
        "**1. Cristaux gagnés**\n\n"
        f"{missions} × {gain_mission} + {bonus} = {gains}.\n\n"

        "**2. Cristaux disponibles**\n\n"
        f"{stock} + {gains} − {perte} = {disponibles}.\n\n"

        "**Expression complète :**\n\n"
        f"{stock} + ({missions} × {gain_mission} + {bonus}) "
        f"− {perte} = {disponibles}.\n\n"

        "**3. Nombre maximal d'équipements**\n\n"
        f"Cristaux pouvant être dépensés : {disponibles} − "
        f"{reserve} = {disponibles - reserve}.\n\n"

        f"{disponibles - reserve} : {prix_equipement} — "
        f"Quotient : {maximum} — "
        f"Reste : {(disponibles - reserve) % prix_equipement}\n\n"

        f"Il peut acheter **{maximum} équipements** au maximum.\n\n"

        "**4. Cristaux réellement restants**\n\n"
        f"{disponibles} − {maximum} × {prix_equipement} "
        f"= {reste} cristaux.\n\n"
        f"Ce total comprend les {reserve} cristaux de réserve "
        f"et les {(disponibles - reserve) % prix_equipement} "
        "cristaux non utilisés pour fabriquer les équipements.\n\n"

        "**5. Équipement des aventuriers**\n\n"
        f"Équipements possibles : {maximum} ; aventuriers : "
        f"{aventuriers}.\n\n"

        f"**Équipe entièrement équipée : {possible}.**\n\n"

        f"Écart : {ecart} équipement(s).\n\n"
        f"{conclusion}"
    )

    champs = [
        _p9_nombre("r1", 1, "Cristaux gagnés", gains, "cristaux"),
        _p9_nombre(
            "r2", 2, "Cristaux disponibles avant achat",
            disponibles, "cristaux"
        ),
        _p9_expression(2),
        _p9_nombre(
            "r3", 3, "Équipements achetables au maximum",
            maximum, "équipements"
        ),
        _p9_nombre(
            "r4", 4, "Cristaux restants après achats",
            reste, "cristaux"
        ),
        _p9_choix(
            "r5", 5, "Tous les aventuriers équipés ?",
            possible, ["r3"]
        ),
        _p9_nombre("r6", 5, libelle, ecart, "équipements")
    ]

    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M04", "Les cristaux du jeu vidéo",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_bibliotheque(seed=None):
    rng, seed = _p9_rng(seed)

    stock_initial = rng.randint(55, 95)
    colis = rng.randint(3, 6)
    mangas_par_colis = rng.randint(6, 10)
    dons = rng.randint(7, 18)
    abimes = rng.randint(4, 12)
    classes = rng.randint(3, 5)
    prets_par_classe = rng.randint(5, 9)

    livres_recus = colis * mangas_par_colis
    livres_pretes = classes * prets_par_classe

    variation = livres_recus + dons - abimes - livres_pretes
    fin = stock_initial + variation
    apres_retour = fin + livres_pretes

    enonce = (
        "**La bibliothèque de mangas du collège**\n\n"

        "La bibliothèque possède déjà une collection de mangas "
        "rangés sur ses étagères, mais on ne connaît pas "
        "leur nombre initial.\n\n"
        "Au cours de la semaine, plusieurs mouvements "
        "de mangas ont lieu.\n\n"

        f"Elle reçoit **{colis} colis** de **{mangas_par_colis} mangas** "
        f"chacun, puis **{dons} mangas** offerts par des familles.\n\n"

        f"Elle retire **{abimes} mangas abîmés** de sa collection.\n\n"

        f"Ensuite, **{classes} classes** empruntent chacune "
        f"**{prets_par_classe} mangas**. Ces livres prêtés ne sont "
        "plus dans la bibliothèque pour le moment.\n\n"

        f"À la fin de la semaine, le bibliothécaire compte "
        f"**{fin} mangas sur les étagères** de la bibliothèque.\n\n"
        "Les mangas empruntés par les classes ne sont pas "
        "compris dans ce nombre.\n\n"

        "**Questions**\n\n"

        "1. Combien de mangas contiennent les colis reçus ?\n\n"

        "2. Combien de mangas ont été prêtés aux classes au total ?\n\n"

        "3. Le nombre de mangas sur les étagères a-t-il "
        "augmenté ou diminué au cours de la semaine ? "
        "De combien ?\n\n"

        "4. Combien de mangas la bibliothèque possédait-elle "
        "**avant tous ces mouvements** ? Écris une seule expression "
        "numérique avec des parenthèses.\n\n"

        "5. Combien de mangas se trouveront sur les étagères "
        "lorsque toutes les classes auront rapporté leurs emprunts "
        "(sans autre changement) ?"
    )

    correction = (
        "**1. Mangas reçus en colis**\n\n"
        f"{colis} × {mangas_par_colis} = {livres_recus} mangas.\n\n"

        "**2. Mangas prêtés**\n\n"
        f"{classes} × {prets_par_classe} = {livres_pretes} mangas.\n\n"

        "**3. Variation des mangas sur les étagères**\n\n"
        f"{livres_recus} + {dons} − {abimes} − {livres_pretes} "
        f"= {variation:+d} mangas.\n\n"

        "**4. Retrouver le stock initial**\n\n"
        f"Stock initial = stock final − variation = {fin} − "
        f"({variation:+d}) = {stock_initial}.\n\n"

        "**Expression complète :**\n\n"
        f"{fin} − ({colis} × {mangas_par_colis} + {dons} "
        f"− {abimes} − {classes} × {prets_par_classe}) "
        f"= {stock_initial} mangas.\n\n"

        "**5. Après le retour des emprunts**\n\n"
        f"{fin} + {livres_pretes} = {apres_retour} mangas."
    )

    champs = [
        _p9_nombre(
            "r1", 1, "Mangas reçus en colis",
            livres_recus, "mangas"
        ),
        _p9_nombre(
            "r2", 2, "Mangas prêtés",
            livres_pretes, "mangas"
        ),
        _p9_nombre(
            "r3", 3, "Variation des mangas sur les étagères",
            variation, "mangas"
        ),
        _p9_nombre(
            "r4", 4, "Stock initial de mangas",
            stock_initial, "mangas"
        ),
        _p9_expression(4),
        _p9_nombre(
            "r5", 5, "Mangas après le retour des prêts",
            apres_retour, "mangas"
        )
    ]

    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M05", "La bibliothèque de mangas",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_spectacle(seed=None):
    """Recettes, dépenses, bénéfice et objectif d'un spectacle."""
    rng, seed = _p9_rng(seed)
    while True:
        rangees = rng.randint(8, 12)
        places_par_rangee = rng.randint(13, 18)
        reservees = rng.randint(8, 20)
        billets_eleves = rng.randint(45, 90)
        billets_adultes = rng.randint(15, 35)
        tarif_eleve = rng.randint(4, 6)
        tarif_adulte = rng.randint(8, 11)
        technique = rng.randint(120, 230)
        programme = rng.choice([1, 2])
        places_disponibles = rangees * places_par_rangee - reservees
        billets_vendus = billets_eleves + billets_adultes
        recettes = billets_eleves * tarif_eleve + billets_adultes * tarif_adulte
        depenses = technique + billets_vendus * programme
        benefice = recettes - depenses
        if (2 <= places_disponibles - billets_vendus <= 35
                and 80 <= benefice <= 700):
            break

    objectif = benefice + rng.choice([-35, -20, 20, 35])
    atteint = "Oui" if benefice >= objectif else "Non"
    ecart = abs(benefice - objectif)
    
    if benefice < objectif:
        montant_a_financer = objectif - benefice
        situation_q7 = (
            f"Le collège n'a pas atteint son objectif initial "
            f"de {objectif} €. Il envisage de vendre des billets "
            "élèves supplémentaires pour l'atteindre."
        )
    else:
        # Scénarios situés de part et d'autre de la capacité disponible.
        # L'élève doit vérifier la faisabilité, pas seulement arrondir.
        places_libres = places_disponibles - billets_vendus
        gain_net = tarif_eleve - programme
        billets_vises = max(1, places_libres + rng.choice([-4, -3, 2, 3]))
        montant_a_financer = (billets_vises - 1) * gain_net + rng.randint(1, gain_net)
        situation_q7 = (
            f"Le collège a déjà atteint son objectif de {objectif} €. "
            f"Il souhaite maintenant augmenter encore son bénéfice "
            f"d'au moins {montant_a_financer} € grâce à la vente "
            "de billets élèves supplémentaires."
        )

    gain_par_billet = tarif_eleve - programme

    quotient, reste_division = divmod(
        montant_a_financer, gain_par_billet
    )

    billets_supp = quotient + (1 if reste_division > 0 else 0)

    places_libres = places_disponibles - billets_vendus

    places_suffisantes = (
        "Oui" if places_libres >= billets_supp else "Non"
    )
    but_q7 = (
        "atteindre l'objectif initial du collège"
        if benefice < objectif
        else "obtenir l'augmentation supplémentaire de bénéfice souhaitée"
    )
    enonce = (
        "**Le spectacle solidaire du collège**\n\n"
        f"La salle possède {rangees} rangées de {places_par_rangee} places. "
        f"{reservees} places sont réservées et ne peuvent pas être vendues.\n\n"
        f"Le collège vend {billets_eleves} billets élèves à {tarif_eleve} € "
        f"et {billets_adultes} billets adultes à {tarif_adulte} €.\n\n"
        f"La location du matériel de sonorisation et d'éclairage "
        f"coûte {technique} € au total.\n\n"
        f"Un programme imprimé est remis à chaque spectateur payant, "
        f"pour un coût de {programme} € par programme.\n\n"
        f"Le collège souhaite dégager un bénéfice d'au moins {objectif} €.\n\n"
        "**Questions**\n\n"
        "1. Combien de places peuvent être vendues au maximum ?\n\n"
        "2. Combien de billets ont effectivement été vendus ?\n\n"
        "3. Quel est le montant total des recettes ?\n\n"
        "4. Quelles sont les dépenses totales, programmes compris ?\n\n"
        "5. Quel bénéfice reste-t-il ? Écris une expression numérique "
        "avec des parenthèses.\n\n"
        "6. L'objectif de bénéfice est-il atteint ? De combien d'euros "
        "est-il dépassé ou combien manque-t-il ?\n\n" 
        f"{situation_q7}\n\n"

        "Chaque nouveau spectateur reçoit également un programme "
        "imprimé, au même coût qu'auparavant.\n\n"

        "7. Combien de billets élèves supplémentaires faut-il "
        f"vendre au minimum pour {but_q7} ? "
        "La salle dispose-t-elle de suffisamment de places "
        "pour accueillir ces nouveaux spectateurs ?"

    )
    correction = (
        "**1. Places vendables**\n\n"
        f"{rangees} × {places_par_rangee} − {reservees} = {places_disponibles}.\n\n"
        "**2. Billets vendus**\n\n"
        f"{billets_eleves} + {billets_adultes} = {billets_vendus}.\n\n"
        "**3. Recettes**\n\n"
        f"{billets_eleves} × {tarif_eleve} + {billets_adultes} × "
        f"{tarif_adulte} = {recettes} €.\n\n"
        "**4. Dépenses**\n\n"
        f"{technique} + {billets_vendus} × {programme} = {depenses} €.\n\n"
        "**5. Bénéfice**\n\n"
        f"{recettes} − {depenses} = {benefice} €.\n\n"
        "**Expression complète :**\n\n"
        f"({billets_eleves} × {tarif_eleve} + {billets_adultes} × "
        f"{tarif_adulte}) − ({technique} + "
        f"({billets_eleves} + {billets_adultes}) × {programme}) "
        f"= {benefice} €.\n\n"
        "**6. Objectif**\n\n"
        f"Bénéfice : {benefice} € ; objectif : {objectif} €. "
        f"**Objectif atteint : {atteint}.** Écart : {ecart} €.\n\n"

        "**7. Vente de billets supplémentaires**\n\n"

        f"Chaque billet élève rapporte {tarif_eleve} €, "
        f"mais le programme coûte {programme} €.\n\n"

        f"Bénéfice supplémentaire par billet : "
        f"{tarif_eleve} − {programme} = "
        f"{gain_par_billet} €.\n\n"
        f"Montant à obtenir grâce aux nouveaux billets : "
        f"{montant_a_financer} €.\n\n"
        f"Division : {montant_a_financer} : {gain_par_billet} — "
        f"Quotient : {quotient} — Reste : {reste_division}.\n\n"

        f"Il faut donc vendre au minimum "
        f"**{billets_supp} billets élèves supplémentaires**.\n\n"

        f"Places encore libres : "
        f"{places_disponibles} − {billets_vendus} "
        f"= {places_libres} places.\n\n"

        f"**Suffisamment de places disponibles : "
        f"{places_suffisantes}.**"

    )
    champs = [
        _p9_nombre("r1", 1, "Places vendables", places_disponibles, "places"),
        _p9_nombre("r2", 2, "Billets vendus", billets_vendus, "billets"),
        _p9_nombre("r3", 3, "Recettes", recettes, "€"),
        _p9_nombre("r4", 4, "Dépenses", depenses, "€"),
        _p9_nombre("r5", 5, "Bénéfice", benefice, "€"),
        _p9_expression(5),
        _p9_choix("r6", 6, "Objectif atteint ?", atteint, ["r5"]),
        _p9_nombre("r7", 6, "Écart avec l'objectif", ecart, "€"),
        _p9_nombre(
            "r8", 7, "Billets supplémentaires nécessaires",
            billets_supp, "billets"
        ),
        _p9_choix(
            "r9", 7, "Suffisamment de places disponibles ?",
            places_suffisantes, ["r1", "r2", "r8"]
        ),
    ]
    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M06", "Le spectacle solidaire du collège",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_recyclage(seed=None):
    """Mélange de masses, retrait et division euclidienne."""
    rng, seed = _p9_rng(seed)
    while True:
        sacs = rng.randint(6, 10)
        grammes_sac = rng.choice([1200, 1500, 1800, 2000])
        cartons = rng.randint(3, 7)
        grammes_carton = rng.choice([600, 800, 1000, 1200])
        grammes_refuses = rng.choice([400, 600, 800, 1000, 1200])
        capacite = rng.choice([2000, 2500, 3000])
        masse_brute = sacs * grammes_sac + cartons * grammes_carton
        masse_valide = masse_brute - grammes_refuses
        pleins, reste = divmod(masse_valide, capacite)
        if 4 <= pleins <= 13 and 0 < reste < capacite:
            break
    total_contenants = pleins + 1
    
    # Deux offres de location de conteneurs
    capacite_b = rng.choice([
        c for c in [2000, 2500, 3000, 3500, 4000]
        if c != capacite
    ])

    # Si B contient plus de matériaux, sa location unitaire est plus chère,
    # et réciproquement : aucune offre ne domine trivialement l'autre.
    prix_a = rng.randint(8, 13)
    total_b = (masse_valide + capacite_b - 1) // capacite_b
    cout_a = total_contenants * prix_a
    if capacite_b > capacite:
        choix_prix_b = range(prix_a + 1, 20)
    else:
        choix_prix_b = range(5, prix_a)
    candidats = [p for p in choix_prix_b if total_b * p != cout_a]
    prix_b = rng.choice(candidats)

    cout_b = total_b * prix_b

    meilleure_offre = "A" if cout_a < cout_b else "B"
    economie = abs(cout_a - cout_b)


    def kg(grammes):
        return f"{grammes / 1000:.2f}".replace(".", ",")

    enonce = (
        "**La collecte pour le recyclage**\n\n"
        "Plusieurs classes rassemblent des matériaux à recycler.\n\n"
        f"Elles ont préparé {sacs} sacs de {kg(grammes_sac)} kg chacun "
        f"et {cartons} cartons de {kg(grammes_carton)} kg chacun.\n\n"
        f"Lors du tri, {kg(grammes_refuses)} kg de matériaux sont écartés.\n\n"
        
        "Le collège doit maintenant louer des conteneurs "
        "pour stocker les matériaux conservés.\n\n"

        "Deux entreprises proposent les offres suivantes :\n\n"

        "**Offre A**\n\n"
        f"- Chaque conteneur peut recevoir au maximum {kg(capacite)} kg ;\n"
        f"- Location : {prix_a} € par conteneur.\n\n"

        "**Offre B**\n\n"
        f"- Chaque conteneur peut recevoir au maximum {kg(capacite_b)} kg ;\n"
        f"- Location : {prix_b} € par conteneur.\n\n"

        "Pour chaque offre, on remplit entièrement autant de "
        "conteneurs que possible, puis on place le reste "
        "dans un dernier conteneur si nécessaire.\n\n"

        "Pour les calculs, les masses seront exprimées en grammes. "
        "On rappelle que 1 kg = 1 000 g.\n\n"

        "**Questions**\n\n"
        "1. Quelle masse totale a été collectée, avant le tri, en kg ?\n\n"
        "2. Quelle masse reste-t-il après le tri, en kg ? Écris une "
        "expression numérique avec des parenthèses.\n\n"
        "3. Combien de conteneurs faut-il louer avec "
        "l'offre A et avec l'offre B ?\n\n"
        "4. Calcule le coût total de location de chacune "
        "des deux offres.\n\n"
        "5. Quelle offre est la moins chère ? Combien le "
        "collège économise-t-il en la choisissant ?"


    )
    correction = (
        "**1. Masse collectée**\n\n"
        f"{sacs} × {kg(grammes_sac)} + {cartons} × "
        f"{kg(grammes_carton)} = {kg(masse_brute)} kg.\n\n"
        "**2. Après le tri**\n\n"
        f"{kg(masse_brute)} − {kg(grammes_refuses)} "
        f"= {kg(masse_valide)} kg.\n\n"
        "**Expression complète :**\n\n"
        f"({sacs} × {kg(grammes_sac)} + {cartons} × "
        f"{kg(grammes_carton)}) − {kg(grammes_refuses)} "
        f"= {kg(masse_valide)} kg.\n\n"
        
        "**3. Nombre de conteneurs nécessaires**\n\n"

        f"Masse après le tri : {kg(masse_valide)} kg "
        f"= {masse_valide} g.\n\n"

        f"Offre A : {kg(capacite)} kg = {capacite} g.\n\n"

        f"{masse_valide} : {capacite} — "
        f"Quotient : {pleins} — Reste : {reste} g.\n\n"

        f"Il faut donc **{total_contenants} conteneurs** "
        f"avec l'offre A.\n\n"

        f"Offre B : {kg(capacite_b)} kg = {capacite_b} g.\n\n"

        f"{masse_valide} : {capacite_b} — "
        f"Quotient : {masse_valide // capacite_b} — "
        f"Reste : {masse_valide % capacite_b} g.\n\n"

        f"Il faut donc **{total_b} conteneurs** "
        f"avec l'offre B.\n\n"

        "**4. Coût total de chaque offre**\n\n"

        f"Offre A : {total_contenants} × {prix_a} "
        f"= {cout_a} €.\n\n"

        f"Offre B : {total_b} × {prix_b} "
        f"= {cout_b} €.\n\n"

        "**5. Comparaison des offres**\n\n"

        f"Économie réalisée : {max(cout_a, cout_b)} − "
        f"{min(cout_a, cout_b)} = {economie} €.\n\n"

        f"**L'offre {meilleure_offre} est la moins chère.**"


    )
    champs = [ 
        
        _p9_nombre(
            "r1", 1, "Masse totale avant le tri",
            masse_brute / 1000, "kg"
        ),
        _p9_nombre(
            "r2", 2, "Masse après le tri",
            masse_valide / 1000, "kg"
        ),
        _p9_expression(2),
        _p9_nombre(
            "r5", 3, "Conteneurs nécessaires avec l'offre A",
            total_contenants, "conteneurs"
        ),
        _p9_nombre(
            "r6", 3, "Conteneurs nécessaires avec l'offre B",
            total_b, "conteneurs"
        ),
        _p9_nombre(
            "r7", 4, "Coût total de l'offre A",
            cout_a, "€"
        ),
        _p9_nombre(
            "r8", 4, "Coût total de l'offre B",
            cout_b, "€"
        ),
        _p9_choix(
            "r9", 5, "Offre la moins chère",
            meilleure_offre, ["r7", "r8"]
        ),
        _p9_nombre(
            "r10", 5, "Économie réalisée",
            economie, "€"
        ),
    ]
    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M07", "La collecte pour le recyclage",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_salles(seed=None):
    """Comparer deux salles selon les places ET le budget."""
    rng, seed = _p9_rng(seed)
    while True:
        classes = rng.choice([2, 3])
        eleves_classe = rng.randint(18, 25)
        adultes = rng.randint(2, 5)
        personnes = classes * eleves_classe + adultes
        rangees_a = rng.randint(5, 10)
        sieges_a = rng.randint(7, 11)
        rangees_b = rng.randint(5, 10)
        sieges_b = rng.randint(7, 11)
        places_a = rangees_a * sieges_a
        places_b = rangees_b * sieges_b
        forfait_a = rng.randint(55, 155)
        forfait_b = rng.randint(55, 155)
        tarif_a = rng.randint(3, 7)
        tarif_b = rng.randint(3, 7)
        cout_a = forfait_a + personnes * tarif_a
        cout_b = forfait_b + personnes * tarif_b
        budget = rng.randint(225, 495)
        possible_a = places_a >= personnes and cout_a <= budget
        possible_b = places_b >= personnes and cout_b <= budget
        if possible_a != possible_b:
            break
    choix = "A" if possible_a else "B"

    enonce = (
        "**La projection de cinéma du collège**\n\n"
        f"{classes} classes de {eleves_classe} élèves participent à "
        f"une projection, accompagnées de {adultes} adultes.\n\n"
        "Chaque personne doit avoir une place assise. "
        f"Le collège dispose d'un budget maximal de {budget} €.\n\n"
        "Deux salles sont proposées :\n\n"
        "**Salle A**\n\n"
        f"- {rangees_a} rangées de {sieges_a} places ;\n"
        f"- forfait de réservation : {forfait_a} € ;\n"
        f"- {tarif_a} € par participant.\n\n"
        "**Salle B**\n\n"
        f"- {rangees_b} rangées de {sieges_b} places ;\n"
        f"- forfait de réservation : {forfait_b} € ;\n"
        f"- {tarif_b} € par participant.\n\n"
        "Le collège doit choisir une salle qui respecte **à la fois** "
        "le nombre de places et le budget.\n\n"
        "**Questions**\n\n"
        "1. Combien de personnes participent à la projection ?\n\n"
        "2. Combien de places sont proposées dans chaque salle ?\n\n"
        "3. Quel est le coût total de chaque salle ? "
        "Écris une expression numérique pour le coût de A.\n\n"
        "4. Quelle salle peut être choisie en respectant "
        "les deux contraintes ? Justifie ton choix."
    )
    correction = (
        "**1. Participants**\n\n"
        f"{classes} × {eleves_classe} + {adultes} = {personnes}.\n\n"
        "**2. Places**\n\n"
        f"A : {rangees_a} × {sieges_a} = {places_a} places.\n\n"
        f"B : {rangees_b} × {sieges_b} = {places_b} places.\n\n"
        "**3. Coûts**\n\n"
        f"A : {forfait_a} + {personnes} × {tarif_a} = {cout_a} €.\n\n"
        f"B : {forfait_b} + {personnes} × {tarif_b} = {cout_b} €.\n\n"
        "**4. Vérification des deux conditions**\n\n"
        f"A : places {'suffisantes' if places_a >= personnes else 'insuffisantes'}, "
        f"budget {'respecté' if cout_a <= budget else 'dépassé'}.\n\n"
        f"B : places {'suffisantes' if places_b >= personnes else 'insuffisantes'}, "
        f"budget {'respecté' if cout_b <= budget else 'dépassé'}.\n\n"
        f"**Choix : salle {choix}.** Elle seule respecte les deux conditions."
    )
    champs = [
        _p9_nombre("r1", 1, "Participants", personnes, "personnes"),
        _p9_nombre("r2", 2, "Places de la salle A", places_a, "places"),
        _p9_nombre("r3", 2, "Places de la salle B", places_b, "places"),
        _p9_nombre("r4", 3, "Coût total de la salle A", cout_a, "€"),
        _p9_nombre("r5", 3, "Coût total de la salle B", cout_b, "€"),
        _p9_expression(3),
        _p9_choix(
            "r6", 4, "Salle respectant les deux contraintes",
            choix, ["r1", "r2", "r3", "r4", "r5"]
        ),
        {
            "id": "justification",
            "question": 4,
            "libelle": "Ma justification (places et budget)",
            "type": "texte_libre"
        },
    ]
    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M08", "La projection de cinéma du collège",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_drones(seed=None):
    """Deux ressources limitantes et un objectif de fabrication."""
    rng, seed = _p9_rng(seed)
    while True:
        chassis = rng.randint(6, 12)
        sachets_helices = rng.randint(4, 8)
        helices_par_sachet = rng.choice([6, 8, 10])
        helices_abimees = rng.choice([0, 2, 4])
        boites_batteries = rng.randint(3, 7)
        batteries_par_boite = rng.choice([3, 4, 5])
        batteries_hs = rng.randint(0, 3)
        helices = sachets_helices * helices_par_sachet - helices_abimees
        batteries = boites_batteries * batteries_par_boite - batteries_hs
        max_drones = min(chassis, helices // 4, batteries // 2)
        if 3 <= max_drones <= 10:
            break
    objectif = max(1, max_drones + rng.choice([-2, -1, 1, 2]))
    atteint = "Oui" if max_drones >= objectif else "Non"
    ecart = abs(max_drones - objectif)
    helices_restantes = helices - 4 * max_drones
    batteries_restantes = batteries - 2 * max_drones

    enonce = (
        "**L'atelier de mini-drones**\n\n"
        "Le club de technologie veut fabriquer des mini-drones. "
        "Chaque drone nécessite un châssis, 4 hélices et 2 batteries.\n\n"
        f"Le club possède {chassis} châssis. Il reçoit {sachets_helices} "
        f"sachets de {helices_par_sachet} hélices, mais "
        + ("aucune hélice n'est inutilisable.\n\n" if helices_abimees == 0
           else f"{helices_abimees} hélices sont inutilisables.\n\n")
        + f"Il reçoit aussi {boites_batteries} boîtes de "
        f"{batteries_par_boite} batteries, dont "
        + ("aucune n'est défectueuse.\n\n" if batteries_hs == 0
           else f"{batteries_hs} batterie{' est' if batteries_hs == 1 else 's sont'} "
                f"défectueuse{' ' if batteries_hs == 1 else 's '}au total.\n\n")
        + f"L'objectif est de fabriquer **{objectif} drones complets**.\n\n"
        "**Questions**\n\n"
        "1. Combien d'hélices utilisables reste-t-il ?\n\n"
        "2. Combien de batteries utilisables reste-t-il ?\n\n"
        "3. Combien de drones complets le club peut-il fabriquer au maximum ? "
        "Vérifie séparément les châssis, les hélices et les batteries.\n\n"
        "4. Combien d'hélices et de batteries resteront après avoir "
        "fabriqué ce nombre maximal de drones ?\n\n"
        "5. L'objectif de fabrication est-il atteint ? "
        "De combien de drones le maximum dépasse-t-il l'objectif, "
        "ou combien de drones manquent-ils pour l'atteindre ?"
    )
    correction = (
        "**1. Hélices utilisables**\n\n"
        f"{sachets_helices} × {helices_par_sachet} − {helices_abimees} "
        f"= {helices}.\n\n"
        "**2. Batteries utilisables**\n\n"
        f"{boites_batteries} × {batteries_par_boite} − {batteries_hs} "
        f"= {batteries}.\n\n"
        "**3. Drones complets au maximum**\n\n"
        f"Châssis : {chassis} drones possibles.\n\n"
        f"- Hélices : {helices} : 4 — Quotient : {helices // 4} — "
        f"Reste : {helices % 4}. "
        f"Donc **{helices // 4} drones possibles**.\n\n"
        
        f"- Batteries : {batteries} : 2 — Quotient : {batteries // 2} — "
        f"Reste : {batteries % 2}. "
        f"Donc **{batteries // 2} drones possibles**.\n\n"

        f"Le plus petit des trois nombres est **{max_drones}**.\n\n"
        "**4. Matériel restant**\n\n"
        f"Hélices : {helices} − 4 × {max_drones} = {helices_restantes}.\n\n"
        f"Batteries : {batteries} − 2 × {max_drones} = "
        f"{batteries_restantes}.\n\n"
        "**5. Objectif**\n\n"
        f"Maximum : {max_drones} ; objectif : {objectif}. "
        f"**Objectif atteint : {atteint}.** Écart : {ecart} drone(s)."
    )
    ecart_libelle = (
        "Drones au-delà de l'objectif"
        if atteint == "Oui"
        else "Drones manquants pour l'objectif"
    )
    champs = [
        _p9_nombre("r1", 1, "Hélices utilisables", helices, "hélices"),
        _p9_nombre("r2", 2, "Batteries utilisables", batteries, "batteries"),
        _p9_nombre("r3", 3, "Drones complets possibles", max_drones, "drones"),
        _p9_nombre("r4", 4, "Hélices restantes", helices_restantes, "hélices"),
        _p9_nombre("r5", 4, "Batteries restantes", batteries_restantes, "batteries"),
        _p9_choix("r6", 5, "Objectif atteint ?", atteint, ["r3"]),
        _p9_nombre("r7", 5, ecart_libelle, ecart, "drones"),
    ]
    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M09", "L'atelier de mini-drones",
        seed, enonce, correction, champs
    ))

def generer_modele_p9_mosaique(seed=None):
    """Besoin en carreaux, boîtes et comparaison des offres."""
    rng, seed = _p9_rng(seed)
    while True:
        lignes = rng.randint(10, 18)
        colonnes = rng.randint(9, 16)
        reserve = rng.randint(8, 23)
        besoin = lignes * colonnes + reserve
        paquet_a = rng.choice([10, 12, 15])
        paquet_b = rng.choice([16, 18, 20])
        prix_a = rng.randint(8, 14)
        prix_b = rng.randint(13, 22)
        boites_a = (besoin + paquet_a - 1) // paquet_a
        boites_b = (besoin + paquet_b - 1) // paquet_b
        cout_a = boites_a * prix_a
        cout_b = boites_b * prix_b
        ecart = abs(cout_a - cout_b)
        surplus_optimal = (boites_a*paquet_a-besoin if cout_a < cout_b
                           else boites_b*paquet_b-besoin)
        if 5 <= ecart <= 120 and prix_a < prix_b and surplus_optimal > 0:
            break
    choix = "A" if cout_a < cout_b else "B"
    surplus = (
        boites_a * paquet_a - besoin
        if choix == "A"
        else boites_b * paquet_b - besoin
    )

    enonce = (
        "**La mosaïque du collège**\n\n"
        f"Les élèves fabriquent une mosaïque de {lignes} rangées "
        f"et {colonnes} colonnes de carreaux.\n\n"
        f"Ils prévoient également {reserve} carreaux supplémentaires "
        "en cas de casse.\n\n"
        "Deux magasins proposent des boîtes vendues uniquement entières :\n\n"
        "**Offre A**\n\n"
        f"- {paquet_a} carreaux par boîte ;\n"
        f"- {prix_a} € par boîte.\n\n"
        "**Offre B**\n\n"
        f"- {paquet_b} carreaux par boîte ;\n"
        f"- {prix_b} € par boîte.\n\n"
        "Le collège souhaite acheter assez de carreaux en dépensant "
        "le moins possible.\n\n"
        "**Questions**\n\n"
        "1. De combien de carreaux a-t-on besoin, réserve comprise ?\n\n"
        "2. Quel nombre minimal de boîtes faut-il acheter avec "
        "l'offre A et avec l'offre B ?\n\n"
        "3. Quel est le coût total pour chaque offre ? Écris "
        "une expression numérique pour le coût de A.\n\n"
        "4. Quelle offre est la moins chère et de combien ?\n\n"
        "5. Combien de carreaux non utilisés restera-t-il après "
        "l'achat avec l'offre retenue, réserve comprise dans le besoin ?"
    )
    correction = (
        "**1. Besoin total en carreaux**\n\n"
        f"{lignes} × {colonnes} + {reserve} = {besoin}.\n\n"
        "**2. Nombre de boîtes à acheter**\n\n"
        f"Offre A : {besoin} : {paquet_a} — Quotient : "
        f"{besoin // paquet_a} — Reste : {besoin % paquet_a}. "
        f"Il faut {boites_a} boîtes.\n\n"
        f"Offre B : {besoin} : {paquet_b} — Quotient : "
        f"{besoin // paquet_b} — Reste : {besoin % paquet_b}. "
        f"Il faut {boites_b} boîtes.\n\n"
        "**3. Coûts des deux offres**\n\n"
        f"A : {boites_a} × {prix_a} = {cout_a} €.\n\n"
        f"B : {boites_b} × {prix_b} = {cout_b} €.\n\n"
        "**4. Comparaison**\n\n"
        f"Différence : {max(cout_a, cout_b)} − {min(cout_a, cout_b)} "
        f"= {ecart} €. **L'offre {choix} est la moins chère.**\n\n"
        "**5. Carreaux supplémentaires non utilisés**\n\n"
        f"Quantité achetée avec l'offre {choix} : "
        f"{boites_a if choix == 'A' else boites_b} × "
        f"{paquet_a if choix == 'A' else paquet_b}.\n\n"
        f"Carreaux non utilisés : "
        f"{boites_a if choix == 'A' else boites_b} × "
        f"{paquet_a if choix == 'A' else paquet_b} − "
        f"{besoin} = **{surplus} carreau(x)**."
    )
    champs = [
        _p9_nombre("r1", 1, "Carreaux nécessaires", besoin, "carreaux"),
        _p9_nombre("r2", 2, "Boîtes nécessaires avec A", boites_a, "boîtes"),
        _p9_nombre("r3", 2, "Boîtes nécessaires avec B", boites_b, "boîtes"),
        _p9_nombre("r4", 3, "Coût total de A", cout_a, "€"),
        _p9_nombre("r5", 3, "Coût total de B", cout_b, "€"),
        _p9_expression(3),
        _p9_choix(
            "r6", 4, "Offre la moins chère",
            choix, ["r4", "r5"]
        ),
        _p9_nombre("r7", 4, "Économie réalisée", ecart, "€"),
        _p9_nombre(
            "r8", 5, "Carreaux supplémentaires non utilisés",
            surplus, "carreaux"
        ),
    ]
    return _mc_uniformiser_exercice(_p9_exercice(
        "P9-M10", "La mosaïque du collège",
        seed, enonce, correction, champs
    ))



# ================================================================
# MATHICAP — FORMAT UNIFIÉ DES NOUVEAUX PROBLÈMES, NIVEAUX 7 À 9
# Structure : niveau 7 = 4 questions ; niveaux 8 et 9 = 5.
# Une seule réponse évaluée par question, sans sous-questions A/B.
# La dernière question est consacrée à la résolution finale.
# Les exercices historiques déjà sauvegardés restent intacts.
# Les 46 modèles appellent directement _mc_uniformiser_exercice
# dans leur return : aucun nouveau module n'est nécessaire.
# ================================================================

REGLES = {
    # ---- Niveau 7 : exactement quatre questions ----
    "P7-M01": [
        ("r1", "Combien de piles faut-il au total pour tous les élèves ?"),
        ("r_manquantes", "Combien de piles supplémentaires faut-il prévoir après avoir utilisé le stock du collège ?"),
        ("r2", "Quel est le nombre minimal de paquets de piles à acheter ?"),
        ("r3", "Combien d'euros restera-t-il du budget après tous les achats ?"),
    ],
    "P7-M02": [
        ("r1", "Combien de biscuits peut-on mettre en vente ?"),
        ("r2", "Combien de sachets complets peut-on préparer ?"),
        ("r3", "Combien de biscuits resteront hors des sachets ?"),
        ("r4", "Quel bénéfice le club réalisera-t-il après le paiement des ingrédients ?"),
    ],
    "P7-M03": [
        ('r1', "Quel est le score de l'équipe A ?"),
        ('r2', "Quel est le score de l'équipe B ?"),
        ('r4', "Quel est l'écart de points entre les deux équipes ?"),
        ('r5', "Combien d'énigmes faciles au minimum l'équipe en retard doit-elle résoudre de suite pour au moins égaliser ?"),
    ],
    "P7-M04": [
        ("r1", "Combien coûte l'impression avec l'offre A ?"),
        ("r2", "Combien coûte l'impression avec l'offre B ?"),
        ("r3", "Quelle offre est la moins chère : A ou B ?"),
        ("r4", "Quelle économie le club réalisera-t-il en choisissant l'offre la moins chère ?"),
    ],
    "P7-M05": [
        ("r1", "Quelle est la distance de l'aller-retour jusqu'au parc ?"),
        ("r2", "Quelle distance le groupe a-t-il parcourue au total, en additionnant les distances de tous les cyclistes ?"),
        ("r3", "Quelle distance manque-t-il au groupe pour atteindre son objectif ?"),
        ("r4", "Combien de petits tours supplémentaires chaque cycliste doit-il effectuer au minimum pour atteindre l'objectif du groupe ?"),
    ],
    "P7-M06": [
        ("r1", "Quel est le montant total des recettes de la fête ?"),
        ("r2", "Quel est le montant total des dépenses de la fête ?"),
        ("r3", "Quelle somme reste-t-il dans la caisse après la fête ?"),
        ("choix", "Le club a-t-il atteint son objectif de réserve : oui ou non ?"),
    ],
    "P7-M07": [
        ('r1', 'Combien de cartes achète-t-il ?'),
        ('r2', 'Combien de nouvelles cartes ajoute-t-il grâce aux achats et aux échanges ?'),
        ('r3', "Combien d'emplacements restent vides dans son album ?"),
        ('r4', 'Combien de lots entiers doit-il acheter au minimum pour remplir les emplacements vides de son album ?'),
    ],
    "P7-M08": [
        ("r1", "Combien de volants le club a-t-il achetés ?"),
        ("r2", "Combien de volants utilisables possède-t-il après avoir retiré les volants abîmés ?"),
        ("r3", "Combien de volants faut-il pour tous les matchs ?"),
        ("r5", "Combien de volants manque-t-il ou restera-t-il au club ?"),
    ],
    "P7-M09": [
        ("r1", "Combien de pièces gagne-t-il au total au cours de son aventure ?"),
        ("r2", "Combien de pièces dépense-t-il ou perd-il ?"),
        ("r3", "Combien de pièces possède-t-il avant l'achat de l'équipement spécial ?"),
        ("r5", "Quelle est la différence entre le prix de l'équipement et les pièces disponibles (manque ou reste) ?"),
    ],
    "P7-M10": [
        ("r1", "Combien de feuilles le club a-t-il achetées ?"),
        ("r2", "Combien de feuilles les élèves utilisent-ils pendant l'atelier ?"),
        ("r3", "Combien de feuilles restent disponibles après l'atelier ?"),
        ("r5", "Combien de feuilles restera-t-il ou manquera-t-il pour préparer l'exposition ?"),
    ],
    "P7-M11": [
        ("r_eleves", "Combien de feuilles sont prévues pour les élèves d'une table, avant les feuilles d'essai ?"),
        ("r1", "Combien de feuilles faut-il au total pour une table, essais compris ?"),
        ("r2", "Combien de feuilles faut-il pour toutes les tables ?"),
        ("r3", "Combien de feuilles restera-t-il au professeur après l'atelier ?"),
    ],
    "P7-M12": [
        ("r1", "Combien de personnes participeront à la sortie ?"),
        ("r2", "Combien de cars sont nécessaires au minimum ?"),
        ("r3", "Quel sera le coût de tous les billets d'entrée ?"),
        ("r4", "Quelle est la différence entre le budget et les dépenses totales ?"),
    ],
    "P7-M13": [
        ('r1', 'Combien de moteurs utilisables possède-t-il ?'),
        ('r2', 'Combien de batteries utilisables possède-t-il ?'),
        ('r3', 'Combien de robots complets peut-il assembler ?'),
        ('r4', 'Combien de moteurs ou de batteries supplémentaires lui manque-t-il pour fabriquer le nombre de robots souhaité ?'),
    ],
    "P7-M14": [
        ("r1", "Combien de vêtements les élèves ont-ils collectés ?"),
        ("r2", "Combien de vêtements peuvent être distribués après le tri ?"),
        ("r3", "Combien de cartons faut-il préparer au minimum ?"),
        ("r4", "Combien de trajets la camionnette doit-elle faire au minimum pour tout transporter ?"),
    ],
    "P7-M15": [
        ("r1", "Combien de minutes dure l'ensemble des premières répétitions, sans les pauses ?"),
        ("r2", "Combien de minutes durent les pauses au total ?"),
        ("r3", "Combien de minutes sont utilisées pour les scènes et les pauses ?"),
        ("r4", "Combien de fois peut-on répéter entièrement la dernière scène dans le temps restant ?"),
    ],
    "P7-M16": [
        ("r1", "Combien de graines faut-il pour les planches prévues au départ ?"),
        ("r2", "Combien de graines le club possède-t-il après avoir reçu les sachets ?"),
        ("r3", "Combien de graines restera-t-il après les premières plantations ?"),
        ("r4", "Combien de planches supplémentaires complètes pourra-t-il préparer au maximum ?"),
    ],
    "P7-M17": [
        ("r1", "Combien d'adversaires chaque joueur rencontrera-t-il ?"),
        ("r2", "Combien de parties seront jouées au total, sans compter deux fois la même partie ?"),
        ("r3", "Combien d'euros les inscriptions rapporteront-elles au club ?"),
        ("r4", "En tenant compte de la caisse initiale et des recettes des inscriptions, quel est l'écart entre les ressources et les dépenses du tournoi ?"),
    ],
    "P7-M18": [
        ("r1", "Quelle est la surface totale des panneaux, en m² ?"),
        ("r2", "Quelle surface de peinture faut-il prévoir pour les deux couches, en m² ?"),
        ("r3", "Combien de pots de peinture faut-il acheter au minimum ?"),
        ("r4", "Quel est l'écart entre le budget et le coût de tous les pots ?"),
    ],
    "P7-M19": [
        ('r1', "Choix A — combien coûteraient tous les billets à l'unité ?"),
        ('r2', 'Choix B — combien coûteraient suffisamment de carnets entiers ?'),
        ('r3', "Choix C — combien coûteraient des carnets complétés par des billets à l'unité ?"),
        ('r4', 'Quel choix coûte le moins cher : A, B ou C ?'),
    ],
    "P7-M20": [
        ("r1", "Combien de tours ont été réalisés par l'ensemble des groupes ?"),
        ("r2", "Quelle distance ont-ils parcourue au total, en kilomètres ?"),
        ("r3", "Quelle somme les parrains versent-ils au total, avant les frais ?"),
        ("r4", "Quel est l'écart entre la somme disponible après les frais et l'objectif de don ?"),
    ],
    "P7-M21": [
        ('r1', 'Combien de grammes de granulés faut-il pour nourrir tous les lapins en une journée ?'),
        ('r2', 'Combien de grammes de granulés le refuge possède-t-il après la livraison ?'),
        ('r3', 'Pendant combien de jours complets ce stock suffit-il ?'),
        ('r4', "Combien de grammes de granulés manque-t-il pour tenir jusqu'à la prochaine livraison ?"),
    ],
    "P7-M22": [
        ("r1", "Combien de pages le groupe a-t-il déjà lues ?"),
        ("r2", "Combien de pages le groupe prévoit-il de lire au cours des jours restants, sans effort supplémentaire ?"),
        ("r3", "Combien de pages le groupe aura-t-il lues au total s'il respecte ce rythme ?"),
        ("r4", "Combien de pages le groupe doit-il lire par jour, au minimum, pour atteindre son objectif commun ?"),
    ],
    "P7-M23": [
        ('r1', 'Combien de centimètres de ruban faut-il pour un fanion ?'),
        ('r2', 'Combien de centimètres de ruban faut-il pour tous les fanions ?'),
        ('r3', 'Combien de rouleaux faut-il acheter au minimum ?'),
        ('r4', 'Combien de petits nœuds complets peut-on faire avec la chute du dernier rouleau ?'),
    ],
    "P7-M24": [
        ("r1", "Combien d'élèves sont présents le matin ?"),
        ("r2", "Combien d'élèves sont présents l'après-midi ?"),
        ("r3", "Combien de casiers utilisables le gymnase possède-t-il ?"),
        ("r4", _mc_libelle_question_finale_casiers(None)),
    ],
    "P7-M25": [
        ("r1", "Quelle est la longueur réelle du sentier A, en kilomètres ?"),
        ("r2", "Quelle est la longueur réelle du sentier B, en kilomètres ?"),
        ("r3", "Quelle serait la distance réelle du retour par le sentier A, détour compris, en kilomètres ?"),
        ("r4", "Quelle distance la classe parcourra-t-elle au total pour l'aller par A et le retour par le sentier le plus court ?"),
    ],
    "P7-M26": [
        ("r1", "Combien de litres d'eau restent dans l'aquarium après le nettoyage ?"),
        ("r2", "Combien de litres faut-il ajouter pour remplir l'aquarium ?"),
        ("r3", "Combien de bidons d'eau traitée faut-il acheter au minimum ?"),
        ("r4", "Quel est l'écart entre le budget et les dépenses pour acheter les bidons et le filtre ?"),
    ],
    # ---- Niveau 8 : exactement cinq questions ----
    "P8-M01": [
        ("r1", "Quel est le montant total des recettes ?"),
        ("r2", "Quel est le montant total des dépenses ?"),
        ("r_benefice", "Quel bénéfice reste-t-il avant de constituer la réserve commune ?"),
        ("r3", "Quelle somme reste-t-il à partager après la mise en réserve ?"),
        ("r4", "Quelle somme chaque club reçoit-il après le partage équitable ?"),
    ],
    "P8-M02": [
        ("r1", "Combien de nouveaux dessins les élèves ont-ils réalisés ?"),
        ("r2", "Combien de dessins peuvent être exposés après les retraits ?"),
        ("r3", "Avec les seuls dessins du club, combien de panneaux peuvent être entièrement remplis ?"),
        ("r4", "Avant d’ajouter les dessins invités, combien de dessins se trouvent sur le dernier panneau incomplet du club ?"),
        ("r5", "Combien de panneaux faut-il au minimum pour exposer ensemble les dessins du club et ceux du collège partenaire ?"),
    ],
    "P8-M03": [
        ("r1", "Combien de pièces possède-t-il après les missions, le bonus et l'achat des potions ?"),
        ("r2", "Combien de pièces aurait-il à la fin du chemin A ?"),
        ("r3", "Combien de pièces aurait-il à la fin du chemin B ?"),
        ("r4", "Quel chemin est le plus avantageux : A ou B ?"),
        ("r5", "Combien de pièces supplémentaires le meilleur chemin rapporte-t-il ?"),
    ],
    "P8-M04": [
        ("r1", "Combien de batteries faut-il pour la compétition, réserve comprise ?"),
        ("r2", "Combien de batteries utilisables le club possède-t-il déjà ?"),
        ("r4", "Combien de boîtes supplémentaires faut-il acheter au minimum ?"),
        ("r5", "Combien coûte cet achat de batteries supplémentaires ?"),
        ("r6", "Combien de batteries restera-t-il une fois tous les robots équipés et la réserve constituée ?"),
    ],
    "P8-M05": [
        ("r1", "Combien d'enveloppes d'indices faut-il préparer ?"),
        ("r2", "Combien coûtent tous les achats obligatoires ?"),
        ("r3", "Combien d'argent reste-t-il après ces achats ?"),
        ("r4", "Combien coûteraient tous les souvenirs supplémentaires ?"),
        ("r6", "Après les achats obligatoires, quel est l'écart entre l'argent restant et la somme nécessaire pour acheter les souvenirs tout en conservant la réserve minimale ?"),
    ],
    "P8-M06": [
        ("r1", "Combien coûte le matériel nécessaire pour une équipe ?"),
        ("r2", "Combien coûtent tous les kits avant la réduction et la livraison ?"),
        ("r3", "Combien faut-il payer au total après la réduction et les frais de livraison ?"),
        ("r4", "Le budget du collège est-il suffisant : oui ou non ?"),
        ("r5", "Quel est l'écart entre le budget et le montant total à payer ?"),
    ],
    "P8-M07": [
        ("r1", "Quelle est la durée cumulée d'utilisation des robinets, en minutes ?"),
        ("r2", "Quelle quantité d'eau les anciens équipements auraient-ils consommée ?"),
        ("r3", "Quelle quantité d'eau les nouveaux équipements consomment-ils ?"),
        ("r4", "Combien de litres d'eau ont été économisés ?"),
        ("r6", "De combien de litres l'économie obtenue dépasse-t-elle l'objectif ou lui manque-t-elle ?"),
    ],
    "P8-M08": [
        ("r1", "Quelle est la distance d'un tour complet du parcours ?"),
        ("r2", "Quelle distance est parcourue pendant tous les tours ?"),
        ("r3", "Combien de minutes les élèves passent-ils à marcher ?"),
        ("r4", "Quelle est la durée totale, pauses comprises ?"),
        ("r6", "En effectuant également le détour d’observation, quelle est la valeur absolue de la différence, en minutes, entre la durée réelle et la limite autorisée ?"),
    ],
    "P8-M09": [
        ("r1", "Quel volume de boisson est obtenu avec une seule préparation, en cL ?"),
        ("r2", "Quel est le volume total préparé, en litres ?"),
        ("r3", "Combien de bouteilles peuvent être entièrement remplies ?"),
        ("r4", "Combien de cL faudra-t-il verser dans la dernière bouteille ?"),
        ("r5", "Combien de lots de bouteilles vides faut-il acheter au minimum pour conditionner toute la boisson ?"),
    ],
    "P8-M10": [
        ("r1", "Quelle distance totale le véhicule parcourt-il ?"),
        ("r2", "Combien coûte le transport avec l'entreprise A ?"),
        ("r3", "Combien coûte le transport avec l'entreprise B ?"),
        ("r4", "Quelle entreprise est la moins chère : A ou B ?"),
        ("r5", "Combien d'euros le collège économise-t-il avec l'entreprise la moins chère ?"),
    ],
    # ---- Niveau 9 : exactement cinq questions ----
    "P9-M01": [
        ("r1", "Combien de plants faut-il pour le projet A ?"),
        ("r2", "Combien de plants faut-il pour le projet B ?"),
        ("r3", "Quel est le coût total du projet A ?"),
        ("r4", "Quel est le coût total du projet B ?"),
        ("r7", "Quelle somme restera-t-il du budget après le choix du projet le moins coûteux ?"),
    ],
    "P9-M02": [
        ("r1", "Quelles sont les recettes totales du tournoi ?"),
        ("r4", "Quel bénéfice apporte l'organisation A ?"),
        ("r5", "Quel bénéfice apporte l'organisation B ?"),
        ("r7", "Quelle est la différence entre les bénéfices des deux organisations ?"),
        ("r8", "De combien faudrait-il augmenter les recettes en choisissant l'organisation la moins rentable pour atteindre le bénéfice minimal souhaité ?"),
    ],
    "P9-M03": [
        ("r1", "Combien de personnes participent à la sortie au festival ?"),
        ("r3", "Quel est le coût commun des entrées et des repas ?"),
        ("r4", "Quel est le coût total avec la formule A, transport, entrées et repas compris ?"),
        ("r5", "Quel est le coût total avec la formule B, transport, entrées et repas compris ?"),
        ("r7", "Combien économise-t-on en choisissant la formule la moins chère ?"),
    ],
    "P9-M04": [
        ("r1", "Combien de cristaux le joueur gagne-t-il pendant les missions, bonus compris ?"),
        ("r2", "Combien de cristaux possède-t-il après le piège, avant les achats ?"),
        ("r3", "Combien d'équipements peut-il acheter au maximum en conservant sa réserve ?"),
        ("r4", "Combien de cristaux lui restera-t-il après ces achats ?"),
        ("r6", "Combien d'équipements lui manque-t-il pour équiper tous les aventuriers, si ce maximum ne suffit pas ?"),
    ],
    "P9-M05": [
        ("r1", "Combien de mangas contiennent tous les colis reçus ?"),
        ("r2", "Combien de mangas ont été prêtés au total aux classes ?"),
        ("r3", "Quelle est la variation signée du nombre de mangas sur les étagères pendant la semaine (positive si augmentation, négative si diminution, nulle si aucun changement) ?"),
        ("r4", "Combien de mangas la bibliothèque possédait-elle avant tous ces mouvements ?"),
        ("r5", "Combien de mangas seront présents quand les classes auront rendu leurs emprunts ?"),
    ],
    "P9-M06": [
        ("r2", "Combien de billets ont réellement été vendus ?"),
        ("r3", "Quel est le montant total des recettes du spectacle ?"),
        ("r4", "Quel est le total des dépenses, programmes compris ?"),
        ("r5", "Quel bénéfice reste-t-il après toutes les dépenses ?"),
        ("r8", "Combien de billets élèves supplémentaires faut-il vendre au minimum pour atteindre l'augmentation de bénéfice souhaitée ?"),
    ],
    "P9-M07": [
        ("r1", "Quelle masse totale a été collectée avant le tri ?"),
        ("r2", "Quelle masse reste-t-il après le tri ?"),
        ("r7", "Quel est le coût total avec l'offre A, après calcul du nombre de conteneurs nécessaires ?"),
        ("r8", "Quel est le coût total avec l'offre B, après calcul du nombre de conteneurs nécessaires ?"),
        ("r10", "Combien le collège économise-t-il en choisissant l'offre la moins chère ?"),
    ],
    "P9-M08": [
        ("r1", "Combien de personnes assistent à la projection ?"),
        ("r2", "Combien de places sont proposées dans la salle A ?"),
        ("r4", "Quel est le coût total de la salle A ?"),
        ("r5", "Quel est le coût total de la salle B ?"),
        ("r6", "Quelle salle respecte à la fois la capacité nécessaire et le budget : A ou B ?"),
    ],
    "P9-M09": [
        ("r1", "Combien d'hélices utilisables restent disponibles ?"),
        ("r2", "Combien de batteries utilisables restent disponibles ?"),
        ("r3", "Combien de drones complets le club peut-il fabriquer au maximum ?"),
        ("r4", "Combien d'hélices resteront après la fabrication de ces drones ?"),
        ("r7", "Combien de drones manquent-ils pour atteindre l'objectif de fabrication, s'il n'est pas atteint ?"),
    ],
    "P9-M10": [
        ("r1", "Combien de carreaux faut-il au total, réserve comprise ?"),
        ("r4", "Quel est le coût total des boîtes avec l'offre A ?"),
        ("r5", "Quel est le coût total des boîtes avec l'offre B ?"),
        ("r7", "Combien le collège économise-t-il en choisissant l'offre la moins chère ?"),
        ("r8", "Combien de carreaux resteront inutilisés une fois les boîtes achetées avec l'offre retenue ?"),
    ],
}


# Catégories reconnues par le diagnostic pédagogique existant.
# Contrairement à un classement déduit des positions, ces étiquettes sont
# explicitement associées aux quatre/cinq tâches de chaque modèle.
_CATEGORIES = {
    "Q": "Quantités et totaux",
    "B": "Coûts et budgets",
    "C": "Comparaisons et décisions",
    "D": "Durées et distances",
    "L": "Lots, capacités et partages",
    "R": "Restes et écarts",
}
_CATEGORIES_PAR_MODELE = {
    "P7-M01": "Q Q L B", "P7-M02": "Q L R B", "P7-M03": "Q Q C R",
    "P7-M04": "B B C R", "P7-M05": "D D D L", "P7-M06": "B B B C",
    "P7-M07": "Q Q R L", "P7-M08": "Q Q Q R", "P7-M09": "Q B R R",
    "P7-M10": "Q Q R R", "P7-M11": "Q Q Q R",
    "P7-M12": "Q L B B", "P7-M13": "Q L Q R",
    "P7-M14": "Q Q L L", "P7-M15": "D D D L",
    "P7-M16": "Q Q R L",
    "P7-M17": "Q Q B B", "P7-M18": "Q Q L B",
    "P7-M19": "Q L B B", "P7-M20": "Q D B B",
    "P7-M21": "Q Q L L",
    "P7-M22": "Q Q Q L", "P7-M23": "Q Q L L",
    "P7-M24": "Q Q Q L", "P7-M25": "D D D D", "P7-M26": "Q Q L B",
    "P8-M01": "B B B B B", "P8-M02": "Q Q L R L", "P8-M03": "Q Q Q C R",
    "P8-M04": "Q Q L B R", "P8-M05": "L B B B R", "P8-M06": "B B B C B",
    "P8-M07": "D Q Q R L", "P8-M08": "D D D D L", "P8-M09": "Q Q L R L",
    "P8-M10": "D B B C R",
    "P9-M01": "Q Q B B B", "P9-M02": "B B B R B", "P9-M03": "Q B B B R",
    "P9-M04": "Q Q L R L", "P9-M05": "Q Q R Q Q", "P9-M06": "Q B B B L",
    "P9-M07": "Q Q B B B", "P9-M08": "Q Q B B C", "P9-M09": "Q Q L R B",
    "P9-M10": "Q B B R R",
}


def _champs_ajoutes(exercice, par_id):
    """Deux modèles du niveau 7 et un modèle du niveau 8 nécessitent une étape calculée.

    Les valeurs proviennent des paramètres déjà affichés et des réponses
    générées par le modèle, sans recours à l'IA ou à une valeur inventée.
    """
    identifiant = exercice["id"]
    enonce = exercice["enonce"]
    if identifiant == "P7-M01":
        match = re.search(r"possède déjà\s+(\d+)\s+piles", enonce)
        if not match:
            raise ValueError("Stock de piles introuvable dans l'énoncé P7-M01")
        stock = int(match.group(1))
        total = par_id["r1"]["attendu"]
        valeur = total - stock
        if valeur <= 0:
            raise ValueError("Nombre de piles à acheter non positif")
        return {"r_manquantes": {
            "id": "r_manquantes", "type": "nombre", "attendu": valeur,
            "libelle": "Piles supplémentaires nécessaires", "unite": "piles",
        }}
    if identifiant == "P7-M11":
        tables = re.search(r"avec\s+(\d+)\s+tables\s+de\s+(\d+)\s+élèves", enonce)
        feuilles = re.search(r"-\s+(\d+)\s+feuilles de papier", enonce)
        if not tables or not feuilles:
            raise ValueError("Données des tables de dessin introuvables")
        nombre_eleves = int(tables.group(2))
        feuilles_par_eleve = int(feuilles.group(1))
        valeur = nombre_eleves * feuilles_par_eleve
        if valeur <= 0 or valeur >= par_id["r1"]["attendu"]:
            raise ValueError("Calcul des feuilles par table incohérent")
        return {"r_eleves": {
            "id": "r_eleves", "type": "nombre", "attendu": valeur,
            "libelle": "Feuilles pour les élèves d'une table", "unite": "feuilles",
        }}
    if identifiant == "P8-M01":
        valeur = par_id["r1"]["attendu"] - par_id["r2"]["attendu"]
        if valeur <= 0:
            raise ValueError("Bénéfice avant réserve non positif")
        return {"r_benefice": {
            "id": "r_benefice", "type": "nombre", "attendu": valeur,
            "libelle": "Bénéfice avant mise en réserve", "unite": "€",
        }}
    return {}


def _formater_reponse(champ):
    valeur = champ["attendu"]
    if isinstance(valeur, float):
        nombre = f"{valeur:.6f}".rstrip("0").rstrip(".").replace(".", ",")
    else:
        nombre = str(valeur)
    unite = champ.get("unite")
    return f"{nombre} {unite}" if unite else nombre




# ================================================================
# MATHICAP V3 — DIFFICULTÉ OBSERVABLE ET ÉNONCÉS COHÉRENTS
# Les identifiants sont conservés pour la reprise des séries et les
# variantes ; les exercices déjà enregistrés ne sont pas recalculés.
# Les défis ci-dessous sont dérivés des paramètres du tirage réel.
# ================================================================

def _mc_v3_champ(identifiant, valeur, libelle, unite):
    return {"id": identifiant, "type": "nombre", "attendu": valeur,
            "libelle": libelle, "unite": unite}


def _mc_v3_extraire(pattern, texte, contexte):
    match = re.search(pattern, texte, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("Donnée manquante pour " + contexte)
    return match


def _mc_v3_preparer(exercice, par_id, regles, blocs):
    """Révise le défi final sans changer le contrat d'API ni les anciens IDs.

    Chaque défi expose toutes les données nécessaires. La réponse attendue est
    recomputée indépendamment à partir des paramètres réellement tirés.
    """
    identifiant = exercice["id"]
    avant = blocs[0]
    original = blocs[1]
    contexte = ""
    calcul = ""

    if identifiant == "P9-M06":
        benefice = par_id["r5"]["attendu"]
        objectif = int(_mc_v3_extraire(r"bénéfice d'au moins\s+(\d+)\s*€", avant, identifiant).group(1))
        if benefice >= objectif:
            complement = int(_mc_v3_extraire(r"augmenter encore son bénéfice\s+d'au moins\s+(\d+)\s*€", original, identifiant).group(1))
            cible = benefice + complement
            contexte = (f"\n\n**Nouveau défi :** l'objectif initial est déjà atteint. "
                        f"Le collège veut augmenter son bénéfice actuel d'au moins {complement} € "
                        "en vendant davantage de billets élèves. Chaque nouveau spectateur "
                        "reçoit un programme imprimé au prix déjà indiqué.\n\n")
        else:
            cible = objectif
            contexte = ("\n\n**Nouveau défi :** le collège vendrait des billets élèves "
                        "supplémentaires pour atteindre son objectif initial. "
                        "Chaque nouveau spectateur reçoit un programme imprimé "
                        "au prix déjà indiqué.\n\n")
        tarif = int(_mc_v3_extraire(r"billets élèves à\s+(\d+)\s*€", avant, identifiant).group(1))
        cout_prog = int(_mc_v3_extraire(r"coût de\s+(\d+)\s*€\s+par programme", avant, identifiant).group(1))
        places = _mc_v3_extraire(r"possède\s+(\d+)\s+rangées de\s+(\d+)\s+places\.\s+(\d+)\s+places sont réservées", avant, identifiant)
        capacity = int(places.group(1))*int(places.group(2))-int(places.group(3))
        nb_vendus = par_id["r2"]["attendu"]
        missing = max(0,cible-benefice)
        gain = tarif-cout_prog
        nb_supp = (missing+gain-1)//gain
        bilan_places = capacity-nb_vendus-nb_supp
        par_id["mc_v3_q5"] = _mc_v3_champ("mc_v3_q5", bilan_places,"Solde projeté de places", "places")
        regles = [*regles[:-1],("mc_v3_q5", "Après la vente du plus petit nombre de billets élèves nécessaires pour cet objectif, quel serait le solde de places de la salle ? Indique un nombre positif s'il reste des places, 0 si elle est remplie, ou un nombre négatif s'il manquerait des places (vente alors impossible).")]
        calcul = ("**Nouveau défi — places :** "
                  f"bénéfice supplémentaire {missing} € ; gain net par nouveau billet "
                  f"{tarif} − {cout_prog} = {gain} € ; "
                  f"minimum de billets {missing} ÷ {gain} arrondi au supérieur = {nb_supp}. "
                  f"Places vendables : {capacity} ; déjà vendues : {nb_vendus}. "
                  f"Solde théorique = {capacity} − {nb_vendus} − {nb_supp} = **{bilan_places} places**.\n\n")

    elif identifiant == "P9-M09":
        helices = par_id["r1"]["attendu"]
        batteries = par_id["r2"]["attendu"]
        chassis = int(_mc_v3_extraire(r"possède\s+(\d+)\s+châssis", avant, identifiant).group(1))
        # On construit une situation où les DEUX ressources consommables sont
        # réellement limitantes ; on élimine ainsi le risque d'un Q5 trivial.
        cible = max(chassis, helices//4, batteries//2)+2
        gratuits = cible-chassis
        manque_hel = max(0,4*cible-helices)
        manque_bat = max(0,2*cible-batteries)
        taille_hel = next((v for v in (6,8,10) if manque_hel % v != 0),6)
        taille_bat = next((v for v in (3,4,5) if manque_bat % v != 0),3)
        prix_hel = 7+chassis%3
        prix_bat = 5+helices%4
        n_hel = (manque_hel+taille_hel-1)//taille_hel
        n_bat = (manque_bat+taille_bat-1)//taille_bat
        depense = n_hel*prix_hel+n_bat*prix_bat
        contexte = (f"\n\n**Nouveau défi :** le club souhaite désormais pouvoir construire "
                    f"{cible} drones au total. Un partenaire offre gratuitement {gratuits} châssis. "
                    f"Il est possible d'acheter des hélices par sachets entiers de "
                    f"{taille_hel}, à {prix_hel} € le sachet, et des batteries par "
                    f"boîtes entières de {taille_bat}, à {prix_bat} € la boîte. "
                    "Les pièces déjà disponibles sont utilisables pour ce nouvel objectif.\n\n")
        par_id["mc_v3_q5"] = _mc_v3_champ("mc_v3_q5",depense,"Coût minimal de composants", "€")
        regles = [*regles[:-1],("mc_v3_q5",f"Quel est le coût minimal des hélices et batteries supplémentaires à acheter pour fabriquer {cible} drones, compte tenu des châssis offerts et du matériel initial ?")]
        calcul = ("**Nouveau défi — achats :** "
                  f"hélices manquantes : 4 × {cible} − {helices} = {manque_hel} ; "
                  f"{n_hel} sachet(s) de {taille_hel} hélices. "
                  f"Batteries manquantes : 2 × {cible} − {batteries} = {manque_bat} ; "
                  f"{n_bat} boîte(s) de {taille_bat} batteries. "
                  f"Coût total : {n_hel} × {prix_hel} + {n_bat} × {prix_bat} "
                  f"= **{depense} €**.\n\n")

    elif identifiant == "P9-M02":
        objectif = int(_mc_v3_extraire(r"bénéfice d'au moins\s+(\d+)\s*€", original, identifiant).group(1))
        benefice_a = par_id["r4"]["attendu"]
        benefice_b = par_id["r5"]["attendu"]
        moins_rentable = "A" if benefice_a < benefice_b else "B"
        location_var = _mc_v3_extraire(rf"Organisateur {moins_rentable}\s+— Proposition.*?Fournitures\s*:\s*(\d+)\s*€\s*par joueur", avant, identifiant)
        variable = int(location_var.group(1))
        entree = int(_mc_v3_extraire(r"versent chacun\s*\*\*(\d+)\s*€", avant, identifiant).group(1))
        gain_nouveau = entree-variable
        manque = objectif-min(benefice_a,benefice_b)
        nouveaux = (manque+gain_nouveau-1)//gain_nouveau
        contexte = (f"\n\n**Nouveau défi :** le collège s'est fixé un bénéfice minimal "
                    f"de {objectif} €. Imagine qu'il retienne malgré tout "
                    f"l'organisateur {moins_rentable}, le moins rentable pour "
                    "le nombre actuel de joueurs. De nouveaux joueurs pourraient "
                    "s'inscrire au même tarif ; chaque nouveau joueur engendrerait "
                    "aussi le coût de fournitures prévu par cet organisateur. "
                    "Les récompenses et la location ne changeraient pas.\n\n")
        par_id["mc_v3_q5"] = _mc_v3_champ("mc_v3_q5",nouveaux,"Inscriptions supplémentaires nécessaires", "joueurs")
        regles = [*regles[:-1],("mc_v3_q5","Combien de joueurs supplémentaires devraient s'inscrire au minimum pour atteindre le bénéfice minimal souhaité avec cet organisateur ?")]
        calcul = ("**Nouveau défi — inscriptions :** "
                  f"bénéfice de {moins_rentable} : {min(benefice_a,benefice_b)} € ; "
                  f"objectif {objectif} € ; manque {manque} €. "
                  f"Chaque nouvel élève rapporte net {entree} − {variable} = "
                  f"{gain_nouveau} €. Il faut **{nouveaux} inscriptions** au minimum.\n\n")

    elif identifiant == "P9-M03":
        personnes=par_id["r1"]["attendu"]
        couta=par_id["r4"]["attendu"]
        coutb=par_id["r5"]["attendu"]
        frais=_mc_v3_extraire(r"Chaque personne paie\s+(\d+)\s*€ d'entrée.*?et\s+(\d+)\s*€ pour le repas", avant, identifiant)
        commun=int(frais.group(1))+int(frais.group(2))
        prix_b=int(_mc_v3_extraire(r"\*\*Transport B\*\*.*?-\s*(\d+)\s*€ par personne transportée", avant, identifiant).group(1))
        nouveaux=3+personnes%5
        nouveau_a=couta+nouveaux*commun
        nouveau_b=coutb+nouveaux*(commun+prix_b)
        economie=abs(nouveau_a-nouveau_b)
        if economie == 0:
            # Écarter le cas où la comparaison finale ne distingue pas les choix.
            nouveaux += 1
            nouveau_a=couta+nouveaux*commun
            nouveau_b=coutb+nouveaux*(commun+prix_b)
            economie=abs(nouveau_a-nouveau_b)
        contexte=(f"\n\n**Nouveau défi :** {nouveaux} personnes supplémentaires "
                  "rejoignent la sortie. Le nombre de kilomètres, les frais fixes, "
                  "les prix par kilomètre, par personne, les entrées et les repas "
                  "ne changent pas. Les deux formules restent accessibles.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",economie,"Économie après nouvelles inscriptions", "€")
        regles=[*regles[:-1],("mc_v3_q5","Avec ces participants supplémentaires, combien d'euros le collège économisera-t-il en retenant la formule de transport globalement la moins chère ?")]
        calcul=("**Nouveau défi — sortie :** "
                f"A = {couta} + {nouveaux} × {commun} = {nouveau_a} € ; "
                f"B = {coutb} + {nouveaux} × ({commun} + {prix_b}) = {nouveau_b} €. "
                f"Économie : **{economie} €**.\n\n")

    elif identifiant == "P8-M03":
        # Nouvelle condition après Q4 : refaire la comparaison au lieu de
        # se contenter de soustraire deux résultats déjà fournis.
        solde_a=par_id["r2"]["attendu"]
        solde_b=par_id["r3"]["attendu"]
        meilleur="A" if solde_a>=solde_b else "B"
        taxe=6+(int(par_id["r1"]["attendu"])%37)
        nouveau_a=solde_a-taxe if meilleur=="A" else solde_a
        nouveau_b=solde_b-taxe if meilleur=="B" else solde_b
        difference=abs(nouveau_a-nouveau_b)
        contexte=(f"\n\n**Nouveau défi :** un péage imprévu de {taxe} pièces "
                  f"est maintenant facturé uniquement sur le chemin {meilleur}, "
                  "celui qui paraissait le plus rentable auparavant. "
                  "Les autres gains, achats et pertes restent identiques.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",difference,"Écart après péage", "pièces")
        regles=[*regles[:-1],("mc_v3_q5","Après ce péage, combien de pièces séparent les deux soldes finaux ? Recalcule le meilleur choix si nécessaire.")]
        calcul=("**Nouveau défi — chemin et péage :** "
                f"nouveau solde A {nouveau_a}, nouveau solde B {nouveau_b}. "
                f"Écart absolu : **{difference} pièces**.\n\n")

    elif identifiant == "P8-M08":
        tour=par_id["r1"]["attendu"]
        rythme=int(_mc_v3_extraire(r"allure régulière de (\d+) minutes par kilomètre",avant,identifiant).group(1))
        pause=int(_mc_v3_extraire(r"font une pause de (\d+) minutes",avant,identifiant).group(1))
        detour=float(_mc_v3_extraire(r"détour d.observation de (\d+,\d+) km",avant,identifiant).group(1).replace(',','.'))
        limite=int(_mc_v3_extraire(r"en \*\*(\d+) minutes au maximum",avant,identifiant).group(1))
        # Le détours se fait une seule fois. Entre n tours, il y a n-1 pauses.
        max_tours=max(0,int((limite-detour*rythme+pause)//(tour*rythme+pause)))
        contexte=("\n\n**Nouveau défi :** avant de partir, les élèves souhaitent "
                  "déterminer le nombre maximal de tours complets qu'ils peuvent "
                  "effectuer en gardant le détour d'observation, les pauses "
                  "uniquement entre les tours, et la limite totale annoncée.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",max_tours,"Nombre maximal de tours", "tours")
        regles=[*regles[:-1],("mc_v3_q5","Combien de tours complets au maximum peuvent-ils prévoir sans dépasser la limite totale de durée, détour et pauses inclus ?")]
        calcul=("**Nouveau défi — maximum de tours :** "
                f"un tour dure {tour} × {rythme} = {tour*rythme} min ; "
                f"un détour dure {detour} × {rythme} = {detour*rythme} min. "
                f"Pour n tours, durée = n × {tour*rythme} + (n−1) × {pause} "
                f"+ {detour*rythme} min ; contrainte {limite} min. "
                f"Maximum entier : **{max_tours} tours**.\n\n")

    elif identifiant == "P8-M01":
        montant=par_id["r3"]["attendu"]
        clubs=int(_mc_v3_extraire(r"Les\s+(\d+)\s+clubs",avant,identifiant).group(1))
        objectif=math.ceil(montant/clubs)+5+(clubs%3)
        nouvelle_recette=max(0,objectif*clubs-montant)
        contexte=(f"\n\n**Nouveau défi :** chaque club voudrait finalement "
                  f"recevoir au moins {objectif} € après le partage, tout en "
                  "conservant la réserve commune. De nouvelles ventes sont "
                  "possibles et n'entraînent aucune dépense supplémentaire.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",round(nouvelle_recette,2),"Recettes complémentaires nécessaires", "€")
        regles=[*regles[:-1],("mc_v3_q5","Combien d'euros de recettes supplémentaires faut-il réaliser au minimum pour que chacun des clubs reçoive le montant souhaité ?")]
        calcul=("**Nouveau défi — partage :** "
                f"pour {clubs} clubs il faut {clubs} × {objectif} = {clubs*objectif} € "
                f"à partager ; le montant initial à partager est {montant} €. "
                f"Il faut **{nouvelle_recette:.2f} €** supplémentaires.\n\n")

    elif identifiant == "P8-M07":
        d=_mc_v3_extraire(r"(\d+) robinets sont utilisés chacun (\d+) minutes par jour pendant (\d+) jours", avant,identifiant)
        robinets,minutes,jours=map(int,d.groups())
        tarifs=re.findall(r"laisse couler(?: seulement)?\s+(\d+,\d+) litre",avant)
        if len(tarifs)!=2:raise ValueError("Débits d'eau introuvables")
        debit1, debit2=[float(v.replace(',','.')) for v in tarifs]
        gain_par_robinet=minutes*jours*(debit1-debit2)
        economie=par_id["r4"]["attendu"]
        besoin=2+robinets%3
        objectif=round(economie+gain_par_robinet*(besoin-0.25),2)
        objectif_affiche=f"{objectif:.2f}".replace(".", ",")
        contexte=(f"\n\n**Nouveau défi :** le collège veut désormais économiser "
                  f"au moins {objectif_affiche} L sur cette même période. Il peut "
                  "installer le même économiseur sur de nouveaux robinets identiques, "
                  "utilisés chacun pendant la même durée, aux mêmes débits "
                  "avant et après équipement.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",besoin,"Robinets supplémentaires", "robinets")
        regles=[*regles[:-1],("mc_v3_q5","Quel est le nombre minimal de robinets supplémentaires à équiper pour atteindre le nouvel objectif total d'économie d'eau ?")]
        calcul=("**Nouveau défi — nouveaux robinets :** "
                f"gain pour un robinet = {minutes} × {jours} × ({debit1} − {debit2}) "
                f"= {gain_par_robinet:.2f} L ; déjà économisés {economie} L ; "
                f"objectif {objectif:.2f} L ; nombre minimal **{besoin} robinets**.\n\n")

    elif identifiant == "P9-M07":
        masse_kg=par_id["r2"]["attendu"]
        modif=round(0.5+(int(round(masse_kg*10))%9)*0.2,2)
        texte=avant
        offre_a=_mc_v3_extraire(r"\*\*Offre A\*\*.*?au maximum\s+(\d+,\d+)\s+kg.*?Location\s*:\s*(\d+)\s*€",texte,identifiant)
        offre_b=_mc_v3_extraire(r"\*\*Offre B\*\*.*?au maximum\s+(\d+,\d+)\s+kg.*?Location\s*:\s*(\d+)\s*€",texte,identifiant)
        cap_a=float(offre_a.group(1).replace(',','.'))
        cap_b=float(offre_b.group(1).replace(',','.'))
        tarif_a=int(offre_a.group(2));tarif_b=int(offre_b.group(2))
        # Entiers en grammes pour éviter les imprécisions de seuil.
        total_g=int(round((masse_kg+modif)*1000))
        cout_a=((total_g+int(cap_a*1000)-1)//int(cap_a*1000))*tarif_a
        cout_b=((total_g+int(cap_b*1000)-1)//int(cap_b*1000))*tarif_b
        minimum=min(cout_a,cout_b)
        modif_affiche=f"{modif:.2f}".replace(".", ",")
        contexte=(f"\n\n**Nouveau défi :** le collège reçoit après le tri "
                  f"{modif_affiche} kg de matériaux recyclables supplémentaires. "
                  "Il doit désormais louer assez de conteneurs pour toute la quantité. "
                  "Chaque conteneur est facturé même s'il n'est pas rempli, "
                  "et le collège choisit librement l'une des deux offres, sans les mélanger.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",minimum,"Coût optimal après collecte", "€")
        regles=[*regles[:-1],("mc_v3_q5","Avec cette collecte supplémentaire, quel est le coût TOTAL minimal de location des conteneurs, en comparant les deux offres ?")]
        calcul=("**Nouveau défi — recalcul des deux offres :** "
                f"nouveau total {total_g} g ; offre A : {cout_a} € ; "
                f"offre B : {cout_b} € ; coût minimal **{minimum} €**.\n\n")

    elif identifiant == "P9-M10":
        besoin=par_id["r1"]["attendu"]
        offre_a=_mc_v3_extraire(r"\*\*Offre A\*\*.*?(\d+)\s+carreaux par boîte.*?(\d+)\s*€ par boîte",avant,identifiant)
        offre_b=_mc_v3_extraire(r"\*\*Offre B\*\*.*?(\d+)\s+carreaux par boîte.*?(\d+)\s*€ par boîte",avant,identifiant)
        qa,pa=map(int,offre_a.groups());qb,pb=map(int,offre_b.groups())
        ajout=5+besoin%11
        cible=besoin+ajout
        na=(cible+qa-1)//qa;nb=(cible+qb-1)//qb
        ca=na*pa;cb=nb*pb
        reste=na*qa-cible if ca<=cb else nb*qb-cible
        if reste == 0:
            # Une variante exacte ne doit pas supprimer le dernier reste.
            ajout += 1
            cible=besoin+ajout
            na=(cible+qa-1)//qa;nb=(cible+qb-1)//qb
            ca=na*pa;cb=nb*pb
            reste=na*qa-cible if ca<=cb else nb*qb-cible
        contexte=(f"\n\n**Nouveau défi :** {ajout} carreaux supplémentaires "
                  "s'avèrent nécessaires. Les prix et tailles des boîtes restent "
                  "identiques. La commande n'a pas encore été passée ; le collège "
                  "recompare les deux offres pour ce nouveau besoin. "
                  "Les offres ne peuvent pas être mélangées.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",reste,"Carreaux restants après nouveau choix", "carreaux")
        regles=[*regles[:-1],("mc_v3_q5","Après avoir sélectionné la nouvelle offre la moins chère pour tous les carreaux, combien en restera-t-il inutilisés ? En cas de prix égal, choisis l'offre A.")]
        calcul=("**Nouveau défi — nouvel achat :** "
                f"besoin {besoin}+{ajout}={cible} carreaux ; "
                f"offre A : {na} boîtes pour {ca} € ; "
                f"offre B : {nb} boîtes pour {cb} € ; "
                f"reste inutilisé dans l'offre retenue : **{reste} carreaux**.\n\n")

    elif identifiant == "P7-M23":
        # La version historique demandait de compter toutes les chutes de
        # rouleaux, avec un dernier rouleau traité différemment : niveau 9.
        # Pour N7, limiter Q4 à la chute du dernier rouleau ; Q1-Q3 restent.
        details=exercice["mathicap_decoupe_v3"]
        par_id["r4"]["attendu"]=details["noeuds_dernier"]
        par_id["r4"]["libelle"]="Nœuds depuis le dernier rouleau"
        regles=[*regles[:-1],(regles[-1][0],
            "Avec la chute du dernier rouleau uniquement, combien de nœuds complets peut-on fabriquer ? Calcule d'abord la longueur utilisée dans ce dernier rouleau, puis la longueur disponible pour les nœuds, sans raccorder les chutes.")]
        calcul=("**Défi final — chute du dernier rouleau :** "
                f"après {details['fanions_dernier']} fanions, il reste "
                f"{details['longueur_rouleau_cm']} − "
                f"{details['fanions_dernier']} × {details['ruban_un']} "
                f"= {details['chute_dernier']} cm. "
                f"Nœuds complets : {details['chute_dernier']} ÷ "
                f"{details['longueur_noeud']}, soit "
                f"**{details['noeuds_dernier']} nœuds**.\n\n")

    elif identifiant == "P7-M05":
        regles=[*regles[:-1],(regles[-1][0],
            "Combien de petits tours supplémentaires chaque cycliste doit-il effectuer au minimum ? Partage d'abord la distance manquante du groupe entre les cyclistes, puis calcule le nombre de petits tours complets nécessaires à chacun.")]

    elif identifiant == "P7-M21":
        regles=[*regles[:-1],(regles[-1][0],
            "Combien de sacs supplémentaires faut-il acheter ? Calcule d'abord la nourriture nécessaire pour tous les jours prévus, retire le stock disponible, puis compte les sacs entiers.")]
    elif identifiant == "P7-M13":
        regles=[*regles[:-1],(regles[-1][0],
            "Après la livraison, combien de robots le club pourrait-il fabriquer en plus de l'objectif, ou combien lui manquerait-il ? Calcule séparément la capacité après livraison avec les moteurs et avec les batteries, puis compare le minimum à l'objectif.")]

    elif identifiant == "P9-M04":
        # Planification à deux contraintes : réserve minimale et quêtes entières.
        disponibles=par_id["r2"]["attendu"]
        achetables=par_id["r3"]["attendu"]
        equipement=int(_mc_v3_extraire(r"Un équipement coûte\s+\*\*(\d+)\s+cristaux", avant, identifiant).group(1))
        reserve=int(_mc_v3_extraire(r"conserver au moins\s+\*\*(\d+)\s+cristaux",avant,identifiant).group(1))
        gain=int(_mc_v3_extraire(r"missions\*\* qui rapportent chacune\s+\*\*(\d+)\s+cristaux",avant,identifiant).group(1))
        membres=int(_mc_v3_extraire(r"comprend\s+\*\*(\d+)\s+aventuriers",avant,identifiant).group(1))
        cible=max(membres+2,achetables+2)
        bonus=3+(cible%5)
        manque=max(0,cible*equipement+reserve-disponibles-bonus)
        quetes=(manque+gain-1)//gain
        assert quetes>=1
        contexte=(f"\n\n**Nouveau défi :** avant d'acheter le moindre équipement, "
                  f"le groupe accueille des membres et souhaite équiper {cible} aventuriers. "
                  f"Le joueur reçoit {bonus} cristaux supplémentaires gratuitement. "
                  f"Il peut recommencer des missions, rapportant chacune {gain} cristaux, "
                  f"et veut toujours conserver au moins {reserve} cristaux de réserve "
                  "une fois tous les équipements achetés.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",quetes,"Missions supplémentaires minimales","missions")
        regles=[*regles[:-1],("mc_v3_q5","En repartant du stock de cristaux avant tout achat, quel nombre minimal de missions supplémentaires faut-il réussir pour équiper tous ces aventuriers et conserver la réserve ?")]
        calcul=("**Nouveau défi — missions :** "
                f"{cible} équipements coûtent {cible} × {equipement} = {cible*equipement} cristaux. "
                f"Il faut en outre la réserve de {reserve}. "
                f"Stock initial avant achats : {disponibles} + {bonus} = {disponibles+bonus}. "
                f"Cristaux à gagner : {manque} ; gain par mission : {gain}. "
                f"Nombre minimal de missions : **{quetes}**.\n\n")

    elif identifiant == "P9-M05":
        retour=par_id["r5"]["attendu"]
        retrait=5+(retour%7)
        taille=6+(retour%3)
        supplement=21+(retour%13)
        cible=retour-retrait+supplement
        manquant=cible-(retour-retrait)
        colis=(manquant+taille-1)//taille
        contexte=(f"\n\n**Nouveau défi :** après le retour de tous les livres prêtés, "
                  f"la bibliothèque retire encore {retrait} mangas usés. "
                  f"Elle souhaite alors disposer d'au moins {cible} mangas sur ses "
                  f"étagères. Les colis contiennent {taille} mangas et doivent "
                  "être achetés entiers.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",colis,"Nombre minimal de colis", "colis")
        regles=[*regles[:-1],("mc_v3_q5","Quel est le nombre minimal de colis supplémentaires à commander pour atteindre ce nouveau stock, après les retours et le retrait ?")]
        calcul=("**Nouveau défi — colis :** "
                f"stock après retours {retour} ; après retrait {retour-retrait} ; "
                f"mangas manquants {cible} − {retour-retrait} = {manquant} ; "
                f"colis entiers de {taille} mangas : **{colis} colis**.\n\n")

    elif identifiant == "P9-M01":
        reste=par_id["r7"]["attendu"]
        parcelle=5
        prix_plant=2+(reste%2)
        cout_parcelle=parcelle*prix_plant+7
        maxi=reste//cout_parcelle
        contexte=(f"\n\n**Nouveau défi :** après le choix du projet le moins "
                  "coûteux, le collège envisage des parcelles supplémentaires. "
                  f"Chaque nouvelle parcelle nécessite {parcelle} plants à "
                  f"{prix_plant} € et {7} € de matériel, sans autre frais. "
                  "Les parcelles ne peuvent pas être financées partiellement.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",maxi,"Parcelles supplémentaires", "parcelles")
        regles=[*regles[:-1],("mc_v3_q5","Combien de parcelles supplémentaires le collège peut-il financer au maximum avec le budget qui restera après le projet retenu ?")]
        calcul=("**Nouveau défi — parcelles :** "
                f"reste {reste} € ; coût par parcelle {parcelle} × {prix_plant} + 7 = "
                f"{cout_parcelle} € ; nombre maximal **{maxi}**.\n\n")

    elif identifiant == "P8-M06":
        equipe_cout=par_id["r1"]["attendu"]
        total=par_id["r3"]["attendu"]
        budget=int(_mc_v3_extraire(r"budget de\s*\*\*(\d+)\s*€",avant,identifiant).group(1))
        ajout_equipes=2+(int(equipe_cout)%3)
        nouveau_cout=total+ajout_equipes*equipe_cout
        complement=max(0,nouveau_cout-budget)
        contexte=(f"\n\n**Nouveau défi :** {ajout_equipes} nouvelles équipes "
                  "rejoignent le jeu de piste. Elles reçoivent les mêmes kits. "
                  "La remise accordée et les frais de livraison restent identiques, "
                  "et le collège conserve le même budget.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",complement,"Budget supplémentaire nécessaire", "€")
        regles=[*regles[:-1],("mc_v3_q5","Combien d'euros de financement supplémentaire faut-il trouver pour payer tous les kits, nouveaux kits compris ? Réponds 0 € si le budget initial suffit encore.")]
        calcul=("**Nouveau défi — budget :** "
                f"coût initial {total} € ; {ajout_equipes} × {equipe_cout} € "
                f"pour les nouveaux kits ; coût total {nouveau_cout} € ; "
                f"budget {budget} € ; manque **{complement} €**.\n\n")

    elif identifiant == "P8-M10":
        couta=par_id["r2"]["attendu"]
        coutb=par_id["r3"]["attendu"]
        meilleur="A" if couta<coutb else "B"
        # Le gagnant peut rester le même ou basculer après la modification.
        ecart_init=abs(couta-coutb)
        hausse=max(1, ecart_init + ((int(couta+coutb)%9)-4))
        couta2=couta+hausse if meilleur=="A" else couta
        coutb2=coutb+hausse if meilleur=="B" else coutb
        economie=abs(couta2-coutb2)
        contexte=(f"\n\n**Nouveau défi :** l'entreprise {meilleur}, "
                  f"initialement la moins chère, annonce une hausse "
                  f"de {hausse} € de ses seuls frais fixes. "
                  "Les conditions de l'autre entreprise sont inchangées.\n\n")
        par_id["mc_v3_q5"]=_mc_v3_champ("mc_v3_q5",economie,"Économie après nouveau tarif", "€")
        regles=[*regles[:-1],("mc_v3_q5","Après cette hausse, combien d'euros le collège économisera-t-il en choisissant la nouvelle offre la moins chère ?")]
        calcul=("**Nouveau défi — nouvelle comparaison :** "
                f"A vaut {couta2} € et B vaut {coutb2} € ; "
                f"écart et économie : **{economie} €**.\n\n")

    return regles, contexte, calcul



# ================================================================
# MATHICAP V3.1 — ARBITRAGE INDEPENDANT CLAUDE / GEMINI
# Ajustements localisés des variantes et clarifications des énoncés.
# Ne modifie ni l'ID historique, ni le contrat de sauvegarde Supabase.
# ================================================================
def _mc_v31_affiner(exercice, champs, regles, blocs, contexte, calcul):
    identifiant = exercice["id"]
    avant = blocs[0]

    if identifiant in ("P7-M10", "P7-M09"):
        # Le champ historique attend une VALEUR ABSOLUE. La consigne doit
        # donc interdire l'interprétation « résultat négatif ».
        cle=regles[-1][0]
        formulation=("Combien de feuilles manque-t-il ou reste-t-il pour préparer "
                     "l'exposition ? Indique le nombre de feuilles sous forme d'une "
                     "quantité positive ; explique au brouillon s'il s'agit d'un "
                     "manque ou d'un reste.") if identifiant=="P7-M10" else (
                     "Combien de pièces manque-t-il pour l'équipement, ou combien "
                     "en reste-t-il après l'achat ? Donne une quantité positive et "
                     "précise au brouillon s'il s'agit d'un manque ou d'un reste.")
        regles=[*regles[:-1], (cle, formulation)]

    elif identifiant == "P7-M07":
        cle=regles[-1][0]
        regles=[*regles[:-1], (cle, regles[-1][1] +
            " Pour chaque nouveau lot, tiens compte des doublons et des échanges "
            "comme pour les premiers achats ; arrondis le nombre de lots à l'entier supérieur.")]

    elif identifiant == "P7-M19":
        cle=regles[-1][0]
        regles=[*regles[:-1], (cle, regles[-1][1] +
            " Compare explicitement les deux achats possibles avant de calculer l'économie.")]

    elif identifiant == "P8-M05":
        reserve = _mc_v3_extraire(r"conserver au moins\s+\*\*(\d+,\d+)\s*€", avant, identifiant)
        reserve_val=float(reserve.group(1).replace(',','.'))
        solde=round(float(champs['r3']['attendu'])-float(champs['r4']['attendu'])-reserve_val,2)
        champs['r6']['attendu']=solde
        champs['r6']['libelle']='Solde signé après souvenirs et réserve'
        regles=[*regles[:-1], (regles[-1][0],
            "Après les achats obligatoires, quelle somme resterait après l'achat des souvenirs "
            "et le maintien de la réserve minimale ? Indique un nombre positif "
            "s'il reste de l'argent, 0 si le montant est exact, ou négatif "
            "s'il manque de l'argent.")]
        calcul += (f"**Convention de signe :** argent disponible après les achats "
                   f"obligatoires {champs['r3']['attendu']} € moins "
                   f"souvenirs {champs['r4']['attendu']} € moins réserve "
                   f"{reserve_val} € = **{solde} €**.\n\n")

    elif identifiant == "P8-M08":
        # En V3, résoudre une inéquation sur le nombre maximal de tours exigeait
        # une autonomie G3. Le niveau 8 fait ici un transfert temporel signé.
        rythme=int(_mc_v3_extraire(r"allure régulière de (\d+) minutes par kilomètre",avant,identifiant).group(1))
        detour=float(_mc_v3_extraire(r"détour d.observation de (\d+,\d+) km",avant,identifiant).group(1).replace(',','.'))
        limite=int(_mc_v3_extraire(r"en \*\*(\d+) minutes au maximum",avant,identifiant).group(1))
        t_base=float(champs['r4']['attendu'])
        t_detour=round(detour*rythme,4)
        marge=round(limite-t_base-t_detour,4)
        contexte=(f"\n\n**Nouveau défi :** les élèves maintiennent les tours déjà "
                  f"prévus et ajoutent le détour d'observation de {detour:.1f} km, "
                  "à la même allure. Aucune pause supplémentaire n'est ajoutée.\n\n")
        champs['mc_v3_q5']['attendu']=marge
        champs['mc_v3_q5']['libelle']='Marge signée sur la durée limite'
        regles=[*regles[:-1], ('mc_v3_q5',
            "Après les tours, les pauses et le détour, quel est l'écart signé "
            "avec la durée maximale ? Calcule « limite − durée totale » ; "
            "réponds positivement s'il reste du temps et négativement "
            "si la durée limite est dépassée.")]
        regles[3]=(regles[3][0],"Quelle est la durée totale des tours prévus, pauses comprises, mais sans le détour supplémentaire ?")
        calcul=(f"**Défi final — durée :** durée des tours et pauses {t_base} min ; "
                f"détour {detour} × {rythme} = {t_detour} min ; "
                f"limite {limite} min. Solde signé : {limite} − ({t_base} + {t_detour}) "
                f"= **{marge} min**.\n\n")

    elif identifiant == "P8-M03":
        a=float(champs['r2']['attendu']); b=float(champs['r3']['attendu'])
        meilleur='A' if a>b else 'B'
        # Le péage doit VRAIMENT faire reconsidérer le choix initial.
        taxe=abs(a-b)+3+((int(abs(a+b))%19))
        a2=a-taxe if meilleur=='A' else a
        b2=b-taxe if meilleur=='B' else b
        diff=round(abs(a2-b2),6)
        contexte=(f"\n\n**Nouveau défi :** le chemin {meilleur}, initialement "
                  f"le plus rentable, impose désormais un péage de {taxe:g} pièces. "
                  "L'autre chemin conserve ses conditions initiales.\n\n")
        champs['mc_v3_q5']['attendu']=diff
        regles=[*regles[:-1],('mc_v3_q5',
           "Quel est l'écart entre les soldes des deux chemins après le péage ? "
           "Recalcule le solde de chacun avant de comparer les deux choix.")]
        calcul=(f"**Défi final — choix révisé :** nouveau solde A {a2:g}, "
                f"nouveau solde B {b2:g} ; écart **{diff:g} pièces**.\n\n")

    elif identifiant == "P8-M10":
        a=float(champs['r2']['attendu']); b=float(champs['r3']['attendu'])
        meilleur='A' if a<b else 'B'
        hausse=abs(a-b)+3+((int(a+b)%19))
        a2=a+hausse if meilleur=='A' else a
        b2=b+hausse if meilleur=='B' else b
        diff=round(abs(a2-b2),6)
        contexte=(f"\n\n**Nouveau défi :** l'entreprise {meilleur}, "
                  f"initialement la moins chère, augmente ses frais fixes de "
                  f"{hausse:g} €. L'autre entreprise ne change pas ses prix.\n\n")
        champs['mc_v3_q5']['attendu']=diff
        regles=[*regles[:-1],('mc_v3_q5',
            "Après la hausse, quel montant le collège peut-il économiser en "
            "choisissant le transporteur le moins cher ? Recalcule les deux prix.")]
        calcul=(f"**Défi final — nouvelles offres :** A coûte {a2:g} € "
                f"et B {b2:g} € ; économie **{diff:g} €**.\n\n")

    elif identifiant == "P9-M01":
        contexte=contexte.replace(
            "Chaque nouvelle parcelle nécessite",
            "Le fournisseur accorde pour ces seules nouvelles parcelles un tarif spécifique, distinct des prix des deux projets initiaux. Chaque nouvelle parcelle nécessite")

    elif identifiant == "P8-M07":
        # L'ancien objectif n'est plus interrogé et interfère avec le nouvel
        # objectif Q5 : ne conserver qu'un seuil réellement utile à l'élève.
        blocs[0]=re.sub(
            r"\n\nLe collège souhaite économiser au moins\s+\*\*[\d,]+\s+litres d'eau\*\*\s+sur cette période\.",
            "", avant, flags=re.IGNORECASE)

    elif identifiant == "P9-M02":
        # Recette Q1 ambiguë : expliciter le don dans les recettes.
        blocs[0]=avant.replace("**Questions**", "").rstrip()+"\n\n**Précision comptable :** le don du partenaire est compté dans les recettes du tournoi.\n\n"

    elif identifiant == "P9-M03":
        regles[1]=(regles[1][0],"Quel est le coût TOTAL des entrées et repas pour l'ensemble des personnes participant à la sortie initiale ?")
        personnes=int(champs['r1']['attendu'])
        a=float(champs['r4']['attendu']); b=float(champs['r5']['attendu'])
        frais=_mc_v3_extraire(r"Chaque personne paie\s+(\d+)\s*€ d'entrée.*?et\s+(\d+)\s*€ pour le repas",avant,identifiant)
        commun=int(frais.group(1))+int(frais.group(2))
        prix_b=int(_mc_v3_extraire(r"\*\*Transport B\*\*.*?-\s*(\d+)\s*€ par personne transportée",avant,identifiant).group(1))
        nb=3+personnes%5
        a2=a+nb*commun;b2=b+nb*(commun+prix_b)
        meilleur='A' if a2<b2 else 'B'
        surcharge=abs(a2-b2)+3+(int(a2+b2)%29)
        a3=a2+surcharge if meilleur=='A' else a2
        b3=b2+surcharge if meilleur=='B' else b2
        diff=round(abs(a3-b3),6)
        contexte=(f"\n\n**Nouveau défi :** {nb} personnes supplémentaires rejoignent "
                  f"la sortie. La compagnie {meilleur}, qui serait initialement "
                  f"la moins chère pour ce nouvel effectif, annonce en outre "
                  f"une augmentation fixe de {surcharge:g} € de son forfait. "
                  "Les frais d'entrées et de repas restent inchangés par personne.\n\n")
        champs['mc_v3_q5']['attendu']=diff
        regles=[*regles[:-1],('mc_v3_q5',
            "Après l'arrivée des nouvelles personnes et l'augmentation des frais fixes, "
            "quelle économie réalise-t-on en sélectionnant la formule la moins chère ?")]
        calcul=(f"**Défi final — transports :** A = {a3:g} € ; B = {b3:g} € ; "
                f"la meilleure formule économise **{diff:g} €**.\n\n")

    elif identifiant == "P9-M07":
        masse=float(champs['r2']['attendu'])
        A=_mc_v3_extraire(r"\*\*Offre A\*\*.*?au maximum\s+(\d+,\d+)\s+kg.*?Location\s*:\s*(\d+)\s*€",avant,identifiant)
        B=_mc_v3_extraire(r"\*\*Offre B\*\*.*?au maximum\s+(\d+,\d+)\s+kg.*?Location\s*:\s*(\d+)\s*€",avant,identifiant)
        qa=int(round(float(A.group(1).replace(',','.'))*1000));pa=int(A.group(2))
        qb=int(round(float(B.group(1).replace(',','.'))*1000));pb=int(B.group(2))
        base=min(float(champs['r7']['attendu']),float(champs['r8']['attendu']))
        grammes=int(round(masse*1000))
        # Chercher la plus petite augmentation de 0,2 kg qui modifie
        # effectivement la meilleure dépense (et non un défi fictif).
        found=None
        for k in range(1,300):
            modif_g=200*k
            total=grammes+modif_g
            ca=((total+qa-1)//qa)*pa
            cb=((total+qb-1)//qb)*pb
            if min(ca,cb) != base:
                found=(modif_g,ca,cb);break
        if found is None:raise ValueError('P9-M07 aucun recalcul actif')
        m,ca,cb=found;cout=min(ca,cb)
        chaine=f"{m/1000:.1f}".replace('.',',')
        contexte=(f"\n\n**Nouveau défi :** le collège recueille {chaine} kg "
                  "supplémentaires de matériaux recyclables. Il faut louer des "
                  "conteneurs entiers pour tous les matériaux, et choisir une "
                  "seule des deux offres, sans les mélanger.\n\n")
        champs['mc_v3_q5']['attendu']=cout
        regles=[*regles[:-1],('mc_v3_q5',
            "Pour le nouveau total de matériaux, quel est le coût minimal de location "
            "des conteneurs, après comparaison des deux offres ?")]
        calcul=(f"**Défi final — nouveau volume :** total {grammes+m} g ; "
                f"offre A {ca} € ; offre B {cb} € ; minimum **{cout} €**.\n\n")

    elif identifiant == "P9-M10":
        besoin=int(champs['r1']['attendu'])
        a=_mc_v3_extraire(r"\*\*Offre A\*\*.*?(\d+)\s+carreaux par boîte.*?(\d+)\s*€ par boîte",avant,identifiant)
        b=_mc_v3_extraire(r"\*\*Offre B\*\*.*?(\d+)\s+carreaux par boîte.*?(\d+)\s*€ par boîte",avant,identifiant)
        qa,pa=map(int,a.groups());qb,pb=map(int,b.groups())
        base=min(int(champs['r4']['attendu']),int(champs['r5']['attendu']))
        # Le défi final demande un NOUVEAU budget, qui doit être différent
        # de l'ancien quel que soit le tirage.
        found=None
        for add in range(1,max(qa,qb)*5):
            n=besoin+add
            ca=((n+qa-1)//qa)*pa
            cb=((n+qb-1)//qb)*pb
            if ca>base and cb>base:
                found=(add,n,ca,cb);break
        if found is None:raise ValueError('P9-M10 aucun recalcul de coût actif')
        add,n,ca,cb=found;cout=min(ca,cb)
        contexte=(f"\n\n**Nouveau défi :** {add} carreaux supplémentaires "
                  "sont nécessaires avant la commande. Il faut recalculer le "
                  "nombre de boîtes entières de chaque offre. Les prix et "
                  "conditionnements restent inchangés. Les offres ne peuvent pas "
                  "être mélangées.\n\n")
        champs['mc_v3_q5']['attendu']=cout
        champs['mc_v3_q5']['libelle']='Coût minimal de commande révisée'
        regles=[*regles[:-1],('mc_v3_q5',
            "Pour le nouveau nombre de carreaux, quel est le coût total minimal "
            "de commande en comparant les deux offres ?")]
        calcul=(f"**Défi final — achat révisé :** besoin {n} carreaux ; "
                f"offre A : {ca} € ; offre B : {cb} € ; coût optimal **{cout} €**.\n\n")

    elif identifiant == "P8-M04":
        # Défi de transfert : un nouvel effectif modifie le besoin et deux
        # conditionnements doivent être comparés, sans toucher aux Q1-Q4.
        equipes=int(_mc_v3_extraire(r"(\d+) équipes participent",avant,identifiant).group(1))
        r=int(_mc_v3_extraire(r"Chaque équipe possède (\d+) robots",avant,identifiant).group(1))
        b=int(_mc_v3_extraire(r"Chaque robot a besoin de (\d+) batteries",avant,identifiant).group(1))
        reserve=int(_mc_v3_extraire(r"disposer de (\d+) batterie(?:s)? de réserve",avant,identifiant).group(1))
        boite=_mc_v3_extraire(r"nouvelles boîtes de (\d+) batteries, au prix de (\d+) €",avant,identifiant)
        taille,prix=map(int,boite.groups())
        ajout=2+(equipes%3)
        demande=(equipes+ajout)*(r*b+reserve)
        stock=int(champs['r2']['attendu'])
        manque=max(0,demande-stock)
        cout1=((manque+taille-1)//taille)*prix
        taille2=taille+3
        prix2=prix+5
        cout2=((manque+taille2-1)//taille2)*prix2
        cout=min(cout1,cout2)
        contexte=(f"\n\n**Nouveau défi :** {ajout} équipes supplémentaires "
                  f"rejoignent la compétition, chacune avec le même nombre de "
                  f"robots et de batteries de réserve. Aucune nouvelle boîte "
                  f"n'a encore été achetée. Le magasin propose maintenant deux "
                  f"offres non mélangeables : A, {taille} batteries par boîte "
                  f"à {prix} € ; B, {taille2} batteries par boîte à {prix2} €. "
                  "Les boîtes doivent être achetées entières et tous les "
                  "composants sont utilisables.\n\n")
        champs['mc_v31_q5']=_mc_v3_champ('mc_v31_q5',cout,
                       'Coût minimal des batteries après changement','€')
        regles=[*regles[:-1],('mc_v31_q5',
            "Quel est le coût total minimal pour compléter le stock après "
            "l'arrivée des nouvelles équipes, en comparant les deux offres ?")]
        calcul=(f"**Défi final — robots :** nouveau besoin {demande} ; "
                f"stock {stock} ; manque {manque} ; offre A {cout1} € ; "
                f"offre B {cout2} € ; minimum **{cout} €**.\n\n")

    elif identifiant == "P8-M06":
        cout_initial=float(champs['r3']['attendu'])
        unitaire=int(champs['r1']['attendu'])
        budget=int(_mc_v3_extraire(r"budget de\s*\*\*(\d+)\s*€",avant,identifiant).group(1))
        nouveaux=2+(unitaire%3)
        prix_lot=2*unitaire+3
        prix_unite=unitaire*nouveaux
        prix_gros=((nouveaux+2)//3)*prix_lot
        suplement=min(prix_unite,prix_gros)
        financement=round(max(0,cout_initial+suplement-budget),2)
        contexte=(f"\n\n**Nouveau défi :** {nouveaux} équipes de plus "
                  "s'inscrivent. Leurs kits peuvent être achetés à l'unité "
                  f"au coût initial de {unitaire} € par kit, ou par lots "
                  f"indivisibles de 3 kits au prix de {prix_lot} € le lot. "
                  "Le collège peut choisir l'un ou l'autre mode d'achat pour "
                  "ces nouveaux kits, sans les mélanger. La réduction et la "
                  "livraison appliquées à la commande initiale ne changent pas.\n\n")
        champs['mc_v3_q5']['attendu']=financement
        regles=[*regles[:-1],('mc_v3_q5',
            "En choisissant le mode d'achat le moins cher pour les nouveaux kits, "
            "combien de financement supplémentaire faut-il pour couvrir la "
            "commande initiale ET les nouveaux kits ? Réponds 0 € si le budget suffit.")]
        calcul=(f"**Défi final — lots :** {nouveaux} nouveaux kits : "
                f"{prix_unite} € à l'unité ou {prix_gros} € en lots de trois. "
                f"Achat minimal supplémentaire {suplement} €. Coût global "
                f"{cout_initial+suplement} € ; budget {budget} €. "
                f"Financement **{financement} €**.\n\n")

    elif identifiant == "P9-M04":
        # Deux types de quêtes ; rechercher parmi les combinaisons réalisables
        # plutôt que convertir directement un manque par une seule division.
        cible=int(_mc_v3_extraire(r"souhaite équiper (\d+) aventuriers",contexte,identifiant).group(1))
        membres=int(_mc_v3_extraire(r"comprend\s+\*\*(\d+)\s+aventuriers",avant,identifiant).group(1))
        bonus=int(_mc_v3_extraire(r"reçoit (\d+) cristaux supplémentaires gratuitement",contexte,identifiant).group(1))
        gain=int(_mc_v3_extraire(r"rapportant chacune (\d+) cristaux",contexte,identifiant).group(1))
        prix=int(_mc_v3_extraire(r"Un équipement coûte\s+\*\*(\d+) cristaux",avant,identifiant).group(1))
        reserve=int(_mc_v3_extraire(r"conserver au moins\s+\*\*(\d+) cristaux",avant,identifiant).group(1))
        base=int(champs['r2']['attendu'])
        reste=max(0,cible*prix+reserve-base-bonus)
        prime=2*gain-1
        options=[]
        for exceptionnelles in range(3):
            simples=max(0,(reste-exceptionnelles*prime+gain-1)//gain)
            options.append((exceptionnelles+simples,exceptionnelles,simples))
        total,rares,ordinaires=min(options)
        contexte=(f"\n\n**Nouveau défi :** {cible-membres} nouveaux aventuriers "
                  f"rejoignent l'équipe initiale. Le joueur veut tous les équiper, "
                  f"puis conserver {reserve} cristaux "
                  f"en réserve. Il reçoit gratuitement {bonus} cristaux "
                  f"avant tout achat. Pour gagner les cristaux manquants, "
                  f"il peut effectuer autant de missions ordinaires qu'il veut "
                  f"(gain de {gain} cristaux chacune) et au maximum deux "
                  f"missions rares (gain de {prime} cristaux chacune). "
                  "Chaque mission, quel que soit son type, compte pour une.\n\n")
        champs['mc_v3_q5']['attendu']=total
        champs['mc_v3_q5']['libelle']='Missions minimales (deux types)'
        regles=[*regles[:-1],('mc_v3_q5',
            "Quel est le nombre minimal de missions à réaliser au total pour "
            "équiper tous les aventuriers et garder la réserve, sachant qu'on "
            "peut choisir zéro, une ou deux missions rares ?")]
        calcul=(f"**Défi final — missions :** manque {reste} cristaux ; "
                f"mission normale {gain}, rare {prime} (au plus deux). "
                + "; ".join(f"{x} rares → {z} missions en tout" for z,x,y in options)
                + f". Minimum **{total} missions** ({rares} rares, {ordinaires} normales).\n\n")

    elif identifiant == "P9-M05":
        details=_mc_v3_extraire(r"retire encore (\d+) mangas usés.*?au moins (\d+) mangas.*?colis contiennent (\d+) mangas",contexte,identifiant)
        retrait,cible,taille=map(int,details.groups())
        actuel=int(champs['r5']['attendu'])-retrait
        manque=max(0,cible-actuel)
        a_taille=taille;a_prix=taille+5
        b_taille=2*taille-1;b_prix=2*taille+7
        candidats=[]
        for ca in range((manque+a_taille-1)//a_taille+3):
            for cb in range((manque+b_taille-1)//b_taille+3):
                if ca*a_taille+cb*b_taille>=manque:
                    candidats.append((ca*a_prix+cb*b_prix,ca,cb))
        prix,ca,cb=min(candidats)
        contexte=(f"\n\n**Nouveau défi :** après le retour de tous les "
                  f"emprunts, {retrait} mangas usés sont retirés. "
                  f"Il faut atteindre au moins {cible} mangas en rayon. "
                  f"Le fournisseur propose des colis A de {a_taille} mangas "
                  f"à {a_prix} € et des colis B de {b_taille} mangas "
                  f"à {b_prix} €. On peut mélanger les colis de deux types "
                  "mais pas acheter de fractions de colis.\n\n")
        champs['mc_v3_q5']['attendu']=prix
        champs['mc_v3_q5']['libelle']='Coût minimal des colis'
        regles=[*regles[:-1],('mc_v3_q5',
            "Quel est le coût minimal de commande pour atteindre le nouveau "
            "stock, en choisissant librement le nombre de colis A et B ?")]
        calcul=(f"**Défi final — colis à combiner :** stock après retour et retrait "
                f"{actuel} ; manque {manque} mangas. "
                f"Solution la moins chère : {ca} colis A et {cb} colis B "
                f"pour **{prix} €**.\n\n")

    elif identifiant == "P9-M08":
        participants=int(champs['r1']['attendu'])
        cap_a=int(champs['r2']['attendu'])
        raw_b=_mc_v3_extraire(r"\*\*Salle B\*\*.*?[- ]+(\d+) rangées de (\d+) places",avant,identifiant)
        cap_b=int(raw_b.group(1))*int(raw_b.group(2))
        adm_a=_mc_v3_extraire(r"\*\*Salle A\*\*.*?[- ]+(\d+) € par participant",avant,identifiant)
        adm_b=_mc_v3_extraire(r"\*\*Salle B\*\*.*?[- ]+(\d+) € par participant",avant,identifiant)
        pa=int(adm_a.group(1));pb=int(adm_b.group(1))
        extra=2+(participants%4)
        nouveau=participants+extra
        extension=10
        sur_a=28;sur_b=35
        ca=(float(champs['r4']['attendu'])+extra*pa + (sur_a if nouveau>cap_a else 0))
        cb=(float(champs['r5']['attendu'])+extra*pb + (sur_b if nouveau>cap_b else 0))
        possibilites=[]
        if nouveau<=cap_a+extension:possibilites.append(('A',ca))
        if nouveau<=cap_b+extension:possibilites.append(('B',cb))
        if not possibilites:raise ValueError('P9-M08 : aucune salle accessible')
        choix,c_min=min(possibilites,key=lambda item:item[1])
        budget_nouveau=max(0,int(c_min)-(8+((participants*pa+pb)%43)))
        complement=round(max(0,c_min-budget_nouveau),2)
        contexte=(f"\n\n**Nouveau défi :** {extra} participants s'ajoutent. "
                  f"Pour cet événement élargi, le collège dispose de {budget_nouveau} € "
                  f"de budget. Chaque salle peut, en option, ouvrir jusqu'à "
                  f"{extension} places supplémentaires : coût fixe {sur_a} € en A "
                  f"ou {sur_b} € en B. Cette option n'est facturée que si elle "
                  "est nécessaire. Les tarifs initiaux par participant et les "
                  "forfaits de réservation restent inchangés. Une salle doit "
                  "accueillir tout le monde, sans dépasser sa capacité étendue.\n\n")
        champs['mc_v31_q5']=_mc_v3_champ('mc_v31_q5',complement,
                        'Financement minimal de la projection élargie','€')
        regles=[*regles[:-1],('mc_v31_q5',
            "Quel financement supplémentaire minimal le collège doit-il obtenir "
            "pour accueillir tous les participants dans UNE salle, en choisissant "
            "la solution admissible la moins coûteuse (extension si nécessaire) ?")]
        calcul=(f"**Défi final — deux capacités et deux budgets :** "
                f"effectif {nouveau} ; capacité A {cap_a} (+{extension} avec option) ; "
                f"B {cap_b} (+{extension}). Coût étendu A {ca:g} € "
                f"{'(possible)' if nouveau<=cap_a+extension else '(impossible)'} ; "
                f"B {cb:g} € {'(possible)' if nouveau<=cap_b+extension else '(impossible)'} ; "
                f"retenu {choix} pour {c_min:g} € ; budget {budget_nouveau} € ; "
                f"manque **{complement:g} €**.\n\n")

    elif identifiant == "P9-M09":
        regles[3]=(regles[3][0],
            "Après la fabrication du nombre MAXIMAL de drones trouvé à la question 3, "
            "combien d'hélices resteront disponibles ?")

    return regles, contexte, calcul



def _mc_v32_finaliser(exercice, champs, regles, blocs, contexte, calcul):
    """Ajustements contrôlés après contre-expertise Claude/Gemini, 17/11/2026.

    N'altère ni ID historique ni tables Supabase. Ne concerne que les nouveaux
    tirages et préserve 4 questions N7 / 5 questions N8-N9, 1 champ/question.
    """
    identifiant = exercice["id"]
    avant = blocs[0]

    if identifiant == "P7-M07":
        # RV16 : le lot est annoncé garanti sans doublons, donc Q4 doit
        # s'appuyer sur ces cartes inédites (et non sur les premiers échanges).
        lots = _mc_v3_extraire(r"lots de (\d+) cartes.*?Toutes les cartes", avant, identifiant)
        taille = int(lots.group(1))
        vides = int(champs['r3']['attendu'])
        champs['r4']['attendu'] = (vides+taille-1)//taille
        regles = [*regles[:-1], ('r4',
            f"Les lots supplémentaires contiennent chacun {taille} cartes toutes inédites, sans doublon. "
            "Combien de lots entiers faut-il acheter au minimum pour remplir les emplacements vides de l'album ?")]
        calcul = (f"Les nouveaux lots ne contiennent aucun doublon : "
                  f"{vides} emplacements à compléter, {taille} cartes inédites par lot. "
                  f"Il faut **{champs['r4']['attendu']} lots** (arrondi supérieur).")

    elif identifiant in ('P7-M09','P7-M10'):
        # RV08/RV12 : le signe est nécessaire pour détecter une erreur de sens
        # dans la dernière question tout en conservant une seule réponse chiffrée.
        dispo = float(champs['r3']['attendu'])
        if identifiant == 'P7-M09':
            prix = int(_mc_v3_extraire(r'vendu (\d+) pièces',avant,identifiant).group(1))
            signe = dispo - prix
            unite = 'pièces'
            q = ("Quel est le solde signé après l'achat de l'équipement ? "
                 "Indique un nombre positif si l'achat laisse des pièces, "
                 "négatif si le joueur en manque, et 0 si le prix est exact.")
        else:
            besoin = int(_mc_v3_extraire(r'il faudra (\d+) feuilles',avant,identifiant).group(1))
            signe = dispo - besoin
            unite = 'feuilles'
            q = ("Quel est le solde signé entre le stock restant et les feuilles nécessaires "
                 "pour l'exposition ? Indique un nombre positif s'il reste des feuilles, "
                 "négatif s'il en manque, ou 0 si le stock est exact.")
        champs['r5']['attendu'] = int(signe) if float(signe).is_integer() else signe
        champs['r5']['libelle'] = 'Solde signé (reste ou manque)'
        regles = [*regles[:-1], ('r5',q)]
        calcul = (f"Calculer stock disponible moins besoin : **{signe:g} {unite}**. "
                  "Un résultat positif indique un reste ; un résultat négatif, un manque.")

    elif identifiant == 'P8-M05':
        # RV03 : le Q5 antérieur se résumait à une soustraction directe (G1).
        # Pour N8 : inscription d'autres équipes, dépenses obligatoires,
        # comparaison de conditionnements et réserve en une seule décision.
        equipes=int(_mc_v3_extraire(r'(\d+) équipes participent',avant,identifiant).group(1))
        postes=int(_mc_v3_extraire(r'parcours comporte (\d+) postes',avant,identifiant).group(1))
        def centimes(pattern):
            return int(round(float(_mc_v3_extraire(pattern,avant,identifiant).group(1).replace(',','.'))*100))
        enveloppe=centimes(r'chaque enveloppe coûte\s+(\d+,\d+) €')
        pochette=centimes(r'pochette de matériel à\s+(\d+,\d+) €')
        souvenir=centimes(r'Chaque souvenir coûte\s+(\d+,\d+) €')
        reserve=centimes(r'conserver au moins\s+\*\*(\d+,\d+) €\*\*')
        ajout=1+((equipes+postes)%3)
        total_equipes=equipes+ajout
        supplement_obligatoire=ajout*(postes*enveloppe+pochette)
        prix_lot=int(round(souvenir*2.8))
        unites=total_equipes*souvenir
        lots=math.ceil(total_equipes/3)*prix_lot
        restants=int(round(float(champs['r3']['attendu'])*100))
        solde=round((restants-supplement_obligatoire-min(unites,lots)-reserve)/100,2)
        contexte=(f"\n\n**Nouveau défi :** {ajout} équipes supplémentaires "
                  "s'inscrivent. Chacune doit recevoir toutes les enveloppes "
                  "et une pochette de matériel, aux prix déjà indiqués ; "
                  "la signalisation ne change pas. Le collège souhaite "
                  f"maintenant offrir un souvenir à chacune des {total_equipes} "
                  f"équipes. Les souvenirs peuvent être achetés à {souvenir/100:.2f} € "
                  f"l'unité, OU par lots indivisibles de 3 à {prix_lot/100:.2f} € "
                  "le lot (un seul mode d'achat, sans mélange). Le budget et "
                  "la réserve minimale restent inchangés.\n\n")
        champs['r6']['attendu']=solde
        champs['r6']['libelle']='Solde signé après nouvelles équipes et souvenirs'
        champs['r6']['unite']='€'
        regles=[*regles[:-1],('r6',
              "Après l'arrivée des équipes supplémentaires, quel est le SOLDE SIGNÉ "
              "du budget en achetant les souvenirs au coût minimal et en conservant "
              "la réserve ? Un solde négatif indique un financement manquant.")]
        calcul=(f"Dépenses supplémentaires obligatoires : {supplement_obligatoire/100:.2f} €. "
                f"{total_equipes} souvenirs à l'unité : {unites/100:.2f} € ; "
                f"en lots : {lots/100:.2f} €. Minimum : {min(unites,lots)/100:.2f} €. "
                f"Budget après achats initiaux : {restants/100:.2f} € ; "
                f"réserve : {reserve/100:.2f} €. "
                f"Solde final : **{solde:.2f} €**.")

    elif identifiant == 'P8-M07':
        # RV04 : éviter un objectif arrondi au centième alors que la valeur
        # exacte a une troisième décimale (.125 L, p.ex.).
        d=_mc_v3_extraire(r'(\d+) robinets sont utilisés chacun (\d+) minutes par jour pendant (\d+) jours',avant,identifiant)
        n0,minutes,jours=map(int,d.groups())
        debits=[float(x.replace(',','.')) for x in re.findall(r'laisse couler(?: seulement)?\s+(\d+,\d+) litre',avant)]
        if len(debits)!=2: raise ValueError('P8-M07: débits manquants')
        gain=minutes*jours*(debits[0]-debits[1]); base=float(champs['r4']['attendu'])
        nb=int(champs['mc_v3_q5']['attendu'])
        # Un objectif à une décimale, strictement entre nb-1 et nb robinets.
        cible=round(base+(nb-0.5)*gain,1)
        if not base+(nb-1)*gain < cible <= base+nb*gain:
            raise ValueError('P8-M07: objectif hors des limites')
        contexte=(f"\n\n**Nouveau défi :** le collège veut désormais économiser au moins "
                  f"{cible:.1f} L **au total, en comptant les {n0} robinets déjà équipés**. "
                  "Il peut équiper des robinets supplémentaires identiques, utilisés pendant la "
                  "même durée et avec les mêmes débits.\n\n")
        regles=[*regles[:-1],('mc_v3_q5',
               "Quel est le nombre minimal de robinets SUPPLÉMENTAIRES à équiper pour atteindre l'objectif total ?")]
        calcul=(f"Économie initiale {base:g} L ; économie par robinet ajouté {gain:g} L. "
                f"Objectif {cible:.1f} L ; il manque {cible-base:.1f} L. "
                f"Division et arrondi supérieur : **{nb} robinets supplémentaires**.")

    elif identifiant == 'P8-M08':
        # RV07 : comparaison de deux itinéraires de durée inconnue ;
        # le détour le plus court comporte une pause supplémentaire.
        temps_base=float(champs['r4']['attendu'])
        rythme=int(_mc_v3_extraire(r'allure régulière de (\d+) minutes par kilomètre',avant,identifiant).group(1))
        dA=float(_mc_v3_extraire(r'détour d.observation de (\d+,\d+) km',avant,identifiant).group(1).replace(',','.'))
        limite=int(_mc_v3_extraire(r'en \*\*(\d+) minutes au maximum',avant,identifiant).group(1))
        delta=0.5+((int(temps_base)+int(dA*2))%3)*0.5
        dB=dA+delta
        difference=delta*rythme
        ecart_pause=(-4,4,7)[int(temps_base+dA*2)%3]
        pauseA=int(difference+ecart_pause)
        if pauseA<0:pauseA=0
        tempsA=dA*rythme+pauseA
        tempsB=dB*rythme
        marge=round(limite-temps_base-min(tempsA,tempsB),4)
        contexte=(f"\n\n**Nouveau défi :** pour l'observation, la classe peut "
                  f"prendre le détour A de {dA:.1f} km déjà évoqué, mais "
                  f"une pause de {pauseA} minutes y est imposée ; OU emprunter "
                  f"un sentier B de {dB:.1f} km sans pause supplémentaire. "
                  "Les tours et leurs pauses habituelles ne changent pas. "
                  "Les deux choix sont possibles et l'allure reste la même.\n\n")
        champs['mc_v3_q5']['attendu']=marge
        champs['mc_v3_q5']['unite']='minutes'
        champs['mc_v3_q5']['libelle']='Marge signée après choix du détour le plus rapide'
        regles=[*regles[:-1],('mc_v3_q5',
              "Quelle marge de temps SIGNÉE reste-t-il par rapport à la limite, "
              "si la classe choisit le détour A ou B donnant la durée totale "
              "la plus courte ? Détermine les deux durées puis soustrais "
              "la durée minimale de la limite.")]
        calcul=(f"Détour A : {dA:.1f} km et pause {pauseA} min -> {tempsA:g} min. "
                f"Détour B : {dB:.1f} km sans pause -> {tempsB:g} min. "
                f"Durée des tours {temps_base:g} min ; "
                f"marge signée {limite} - ({temps_base:g} + {min(tempsA,tempsB):g}) "
                f"= **{marge:g} min**.")

    elif identifiant == 'P8-M06':
        # RV10 : deux ou cinq kits nouveaux, et un prix de lot qui peut
        # réellement gagner (5 kits) ou perdre (2 kits), sans domination fixe.
        unitaire=int(champs['r1']['attendu'])
        cout_initial=float(champs['r3']['attendu'])
        budget=int(_mc_v3_extraire(r'budget de\s*\*\*(\d+)\s*€',avant,identifiant).group(1))
        nouveaux=2 if unitaire%2==0 else 5
        prix_lot=2*unitaire+max(1,unitaire//4)
        prix_unites=nouveaux*unitaire
        prix_lots=((nouveaux+2)//3)*prix_lot
        finance=max(0,cout_initial+min(prix_unites,prix_lots)-budget)
        contexte=(f"\n\n**Nouveau défi :** {nouveaux} nouvelles équipes s'inscrivent. "
                  f"Leurs kits coûtent {unitaire} € chacun à l'unité, "
                  f"ou {prix_lot} € par lot indivisible de 3 kits. "
                  "Les deux modes d'achat ne peuvent pas être mélangés. "
                  "La réduction et la livraison de la commande initiale restent inchangées.\n\n")
        champs['mc_v3_q5']['attendu']=round(finance,2)
        regles=[*regles[:-1],('mc_v3_q5',
                "Quel financement supplémentaire faut-il pour payer l'ancienne commande "
                "ET les kits des nouvelles équipes au coût minimal ? Indique zéro si le budget suffit.")]
        calcul=(f"Nouveaux kits : {nouveaux} à l'unité -> {prix_unites} €, "
                f"ou {math.ceil(nouveaux/3)} lot(s) -> {prix_lots} €. "
                f"Minimum {min(prix_unites,prix_lots)} € ; commande initiale {cout_initial:g} € ; "
                f"budget {budget} € ; financement nécessaire **{finance:g} €**.")

    elif identifiant in ('P8-M03','P8-M10'):
        # RV06 / RV17 : ne pas annoncer avant la question 5 quelle option
        # était la meilleure ; demander un écart SIGNE pour capter le choix.
        match=re.search(r'\*\*Nouveau défi :\*\*\s*(?:le chemin|l.entreprise)\s+([AB])',contexte,re.I)
        if not match: raise ValueError('Révision tarif : option non retrouvée')
        if identifiant=='P8-M03':
            a=float(champs['r2']['attendu']);b=float(champs['r3']['attendu'])
            hausse=float(_mc_v3_extraire(r'péage de (\d+(?:\.\d+)?) pièces',contexte,identifiant).group(1))
            ca=a-(hausse if match.group(1)=='A' else 0)
            cb=b-(hausse if match.group(1)=='B' else 0)
            signed=ca-cb
            contexte=re.sub(r', initialement\s+le plus rentable', '', contexte)
            regles=[*regles[:-1],('mc_v3_q5',
              "Quelle est la différence signée entre le solde du chemin A et celui du chemin B "
              "après le péage (solde A moins solde B) ? Un résultat positif favorise A, "
              "un résultat négatif favorise B.")]
            unite='pièces'
        else:
            a=float(champs['r2']['attendu']);b=float(champs['r3']['attendu'])
            hausse=float(_mc_v3_extraire(r'frais fixes de (\d+(?:\.\d+)?) €',contexte,identifiant).group(1))
            ca=a+(hausse if match.group(1)=='A' else 0)
            cb=b+(hausse if match.group(1)=='B' else 0)
            signed=ca-cb
            contexte=re.sub(r',\s*initialement la moins chère', '', contexte)
            regles=[*regles[:-1],('mc_v3_q5',
              "Après la hausse, quelle est la différence signée entre le coût A et le coût B "
              "(coût A moins coût B) ? Un résultat positif signifie que B est moins cher, "
              "un résultat négatif que A est moins cher.")]
            unite='€'
        champs['mc_v3_q5']['attendu']=int(signed) if signed.is_integer() else signed
        champs['mc_v3_q5']['unite']=unite
        calcul=(f"Nouveau montant A : {ca:g} {unite} ; nouveau montant B : {cb:g} {unite}. "
                f"Différence signée A moins B = **{signed:g} {unite}**.")

    elif identifiant == 'P9-M02':
        # RV24 : passer du simple seuil à la comparaison de quatre stratégies.
        # Le coût de publicité est calibré entre les marges des prestataires.
        p=_mc_v3_extraire(r'\*\*(\d+) joueurs\*\*.*?chacun\s+\*\*(\d+) €',avant,identifiant)
        joueurs,entree=map(int,p.groups())
        offres=re.findall(r'\*\*Organisateur [AB] — Proposition\*\*.*?Fournitures\s*:\s*(\d+) € par joueur',avant,re.S)
        if len(offres)!=2:raise ValueError('P9-M02 : fournitures introuvables')
        unite_a,unite_b=map(int,offres)
        marge_a=entree-unite_a;marge_b=entree-unite_b
        ajoutes=3+joueurs%5
        cout_pub=int((ajoutes*marge_a+ajoutes*marge_b)/2)
        benef_a=int(champs['r4']['attendu']);benef_b=int(champs['r5']['attendu'])
        candidats=[('A, sans publicité',benef_a),('B, sans publicité',benef_b),
                   ('A, avec publicité',benef_a+ajoutes*marge_a-cout_pub),
                   ('B, avec publicité',benef_b+ajoutes*marge_b-cout_pub)]
        gagnant,benef_opt=max(candidats,key=lambda x:x[1])
        contexte=(f"\n\n**Nouveau défi :** avant le tournoi, le collège peut payer "
                  f"une campagne de publicité à {cout_pub} €. Si elle est choisie, "
                  f"elle apporte exactement {ajoutes} joueurs supplémentaires, qui paient "
                  "le même prix d'inscription et nécessitent les mêmes fournitures. "
                  "Les frais fixes de salle, le don du partenaire et les récompenses "
                  "restent identiques. Il est possible de choisir librement l'organisateur "
                  "A ou B, et de faire ou non la campagne.\n\n")
        champs['mc_v3_q5']['attendu']=benef_opt
        champs['mc_v3_q5']['libelle']='Bénéfice maximal parmi quatre stratégies'
        champs['mc_v3_q5']['unite']='€'
        regles=[*regles[:-1],('mc_v3_q5',
             "Quel bénéfice maximal le collège peut-il obtenir en comparant les "
             "quatre stratégies possibles (A/B avec ou sans publicité) ?")]
        calcul=("**Défi final — quatre stratégies :** " + "; ".join(
                f"{nom} = {v} €" for nom,v in candidats) +
                f". Maximum : **{benef_opt} €**, stratégie {gagnant}.")

    elif identifiant == 'P9-M03':
        # RV05 : ne pas donner le gagnant initial en affirmant qu'il est
        # le moins cher ; l'élève doit l'identifier par le calcul.
        contexte=re.sub(r', qui serait initialement\s+la moins chère pour ce nouvel effectif','',contexte)
        regles=[*regles[:-1],('mc_v3_q5',
                "Quel est l'écart POSITIF en euros entre les deux coûts globaux après le nouvel effectif "
                "et la hausse, une fois la formule la moins chère déterminée ?")]

    elif identifiant == 'P9-M04':
        # RV01 : n'acheter que des équipements utiles aux membres de l'équipe.
        membres=int(_mc_v3_extraire(r'comprend\s+\*\*(\d+)\s+aventuriers',avant,identifiant).group(1))
        cout=int(_mc_v3_extraire(r'Un équipement coûte\s+\*\*(\d+) cristaux',avant,identifiant).group(1))
        actuel=int(champs['r2']['attendu'])
        achetable=min(membres,int(champs['r3']['attendu']))
        champs['r3']['attendu']=achetable
        champs['r4']['attendu']=actuel-achetable*cout
        regles[2]=(regles[2][0],
            "Pour équiper les membres ACTUELS de l'équipe, combien d'équipements peut-il acheter "
            "au maximum, sans dépasser le nombre d'aventuriers et en conservant la réserve ?")
        regles[3]=(regles[3][0],"Combien de cristaux lui restera-t-il après ces achats utiles ?")
        # Écarter les défis dégénérés qui se résolvent en une seule mission.
        cible_0 = int(_mc_v3_extraire(r'\*\*Nouveau défi :\*\*\s*(\d+) nouveaux aventuriers',contexte,identifiant).group(1))
        bonus = int(_mc_v3_extraire(r'gratuitement (\d+) cristaux',contexte,identifiant).group(1))
        g = int(_mc_v3_extraire(r'gain de (\d+) cristaux chacune',contexte,identifiant).group(1))
        rare = int(_mc_v3_extraire(r'missions rares \(gain de (\d+) cristaux chacune\)',contexte,identifiant).group(1))
        reserve = int(_mc_v3_extraire(r'conserver au moins\s+\*\*(\d+) cristaux',avant,identifiant).group(1))
        ajouts = max(2, cible_0)
        for _ in range(15):
            manque = max(0,(membres+ajouts)*cout+reserve-actuel-bonus)
            alternatives = [(k+math.ceil(max(0,manque-k*rare)/g),k) for k in range(3)]
            missions_min = min(alternatives)[0]
            if missions_min >= 3: break
            ajouts += 1
        contexte = re.sub(r'\*\*Nouveau défi :\*\*\s*(\d+) nouveaux aventuriers',
                          f'**Nouveau défi :** {ajouts} nouveaux aventuriers',contexte)
        contexte=contexte.replace('**Nouveau défi :**',
             '**Nouveau défi :** on repart du stock de cristaux AVANT tout achat des questions 3 et 4. ',1)
        champs['mc_v3_q5']['attendu']=missions_min
        options=[(k, k+math.ceil(max(0,manque-k*rare)/g)) for k in range(3)]
        etapes=' ; '.join(f'{k} mission'+('s' if k>1 else '')+
                             f' rare'+('s' if k>1 else '')+
                             f' : {val} mission'+('s' if val>1 else '')+
                             ' au total' for k,val in options)
        calcul=(f'**Précision Q3/Q4 :** {membres} aventuriers actuels ; '
                f'{achetable} équipements utiles ; {actuel} - {achetable} x {cout} = '
                f'{champs["r4"]["attendu"]} cristaux après ces achats.\n\n'
                f'**Défi final :** en repartant du stock avant tout achat : '
                f'{membres+ajouts} aventuriers à équiper ; manque {manque} cristaux ; '
                f'gain ordinaire {g}, gain rare {rare}, au plus deux missions rares. '
                f'{etapes}. Minimum **{missions_min} missions**.')

    elif identifiant == 'P9-M06':
        # RV09 : un MÊME raisonnement pour tous les tirages, fondé sur
        # une amélioration du bénéfice actuel et la capacité résiduelle.
        p=_mc_v3_extraire(r'possède\s+(\d+)\s+rangées de\s+(\d+)\s+places\.\s+(\d+)\s+places sont réservées',avant,identifiant)
        capacite=int(p[1])*int(p[2])-int(p[3])
        ventes=int(champs['r2']['attendu']); benefice=float(champs['r5']['attendu'])
        tarif=int(_mc_v3_extraire(r'billets élèves à\s+(\d+)\s*€',avant,identifiant).group(1))
        prog=int(_mc_v3_extraire(r'coût de\s+(\d+)\s*€\s+par programme',avant,identifiant).group(1))
        marge=tarif-prog
        dispo=capacite-ventes
        delta=(-2,0,3)[int(benefice+capacite)%3]
        billets=max(1,dispo+delta)
        amelioration=(billets-1)*marge+1
        solde=dispo-billets
        contexte=(f"\n\n**Nouveau défi :** le collège aimerait accroître son bénéfice "
                  f"ACTUEL de **{amelioration} € au minimum** en vendant des billets élèves. "
                  "Chaque spectateur supplémentaire reçoit aussi un programme au prix annoncé. "
                  "Il faut tenir compte des places encore disponibles.\n\n")
        champs['mc_v3_q5']['attendu']=solde
        champs['mc_v3_q5']['unite']='places'
        regles=[*regles[:-1],('mc_v3_q5',
            "Si le collège essaye d'atteindre ce nouveau bénéfice, quel serait le solde SIGNÉ de places "
            "disponibles après la vente du nombre minimal de billets nécessaires ? "
            "Un solde négatif signifie que la vente est impossible faute de places.")]
        calcul=(f"Gain net par nouveau billet : {tarif} - {prog} = {marge} € ; "
                f"augmentation à financer : {amelioration} € ; "
                f"nombre minimal de billets : {billets} (arrondi supérieur). "
                f"Places : {capacite} - {ventes} - {billets} = **{solde} places**.")

    elif identifiant == 'P9-M07':
        # RV18 : vraie optimisation entière ; les conteneurs A et B peuvent
        # être mélangés pour la collecte étendue, et B bénéficie d'une promotion.
        pA=_mc_v3_extraire(r'\*\*Offre A\*\*.*?au maximum\s+(\d+,\d+)\s+kg.*?Location\s*:\s*(\d+)\s*€',avant,identifiant)
        pB=_mc_v3_extraire(r'\*\*Offre B\*\*.*?au maximum\s+(\d+,\d+)\s+kg.*?Location\s*:\s*(\d+)\s*€',avant,identifiant)
        capA=int(round(float(pA[1].replace(',','.'))*1000));capB=int(round(float(pB[1].replace(',','.'))*1000))
        prixA=int(pA[2]);prixB=int(pB[2]);base=float(champs['r2']['attendu'])
        ajoute=float(_mc_v3_extraire(r'recueille\s+(\d+,\d+)\s+kg supplémentaires',contexte,identifiant).group(1).replace(',','.'))
        total=int(round((base+ajoute)*1000))
        # Prix de B proche de son prix équivalent au kg, afin de rendre
        # possible un vrai arbitrage de conditionnement, non une domination.
        tarifB=max(2, round(prixA*capB/capA)+((total//100)%3-1))
        solutions=[]
        for nb in range((total+capB-1)//capB+2):
            na=(max(0,total-nb*capB)+capA-1)//capA
            solutions.append((na*prixA+nb*tarifB,na,nb))
        cout,na,nb=min(solutions)
        contexte=(f"\n\n**Nouveau défi :** le collège recueille {ajoute:.1f} kg "
                  "de matériaux recyclables en plus de la masse déjà triée. "
                  f"Pour la collecte élargie, le prix de l'offre A reste {prixA} € "
                  f"par conteneur, tandis que B propose une promotion à {tarifB} € "
                  "par conteneur. Les capacités ne changent pas. Cette fois, "
                  "le collège peut louer un nombre quelconque de conteneurs A "
                  "ET de conteneurs B, en les mélangeant, mais chaque conteneur "
                  "doit être loué entier.\n\n")
        champs['mc_v3_q5']['attendu']=cout
        champs['mc_v3_q5']['unite']='€'
        regles=[*regles[:-1],('mc_v3_q5',
              "Quel est le coût MINIMAL de location pour stocker tous les "
              "matériaux après la nouvelle collecte, en combinant librement "
              "les conteneurs A et B ?")]
        calcul=(f"**Défi final — location optimale :** masse {total} g ; "
                f"conteneur A {capA} g pour {prixA} € ; "
                f"conteneur B {capB} g pour {tarifB} €. "
                f"Choix minimal : {na} A et {nb} B, soit **{cout} €**.")

    elif identifiant == 'P9-M09':
        # RV23 : rendre le troisième composant potentiellement limitant.
        p=_mc_v3_extraire(r'possède\s+(\d+)\s+châssis',avant,identifiant)
        chassis=int(p.group(1))
        cible=int(_mc_v3_extraire(r'construire\s+(\d+)\s+drones au total',contexte,identifiant).group(1))
        h=_mc_v3_extraire(r'sachets entiers de (\d+), à (\d+) €',contexte,identifiant)
        b=_mc_v3_extraire(r'boîtes entières de (\d+), à (\d+) €',contexte,identifiant)
        helices=int(champs['r1']['attendu']);batteries=int(champs['r2']['attendu'])
        manque_hel=max(0,4*cible-helices);manque_bat=max(0,2*cible-batteries)
        cout_autres=((manque_hel+int(h[1])-1)//int(h[1]))*int(h[2])+((manque_bat+int(b[1])-1)//int(b[1]))*int(b[2])
        deficit_chassis=(chassis+cible)%3
        offerts=max(0,cible-chassis-deficit_chassis)
        manque_chassis=max(0,cible-chassis-offerts)
        prix_chassis=12+(chassis%6)
        total=cout_autres+manque_chassis*prix_chassis
        contexte=re.sub(r'Un partenaire offre gratuitement \d+ châssis\.',
              f"Un partenaire offre gratuitement {offerts} châssis. "
              f"D'autres châssis peuvent être achetés à {prix_chassis} € l'unité.",contexte)
        champs['mc_v3_q5']['attendu']=total
        champs['mc_v3_q5']['unite']='€'
        champs['mc_v3_q5']['libelle']='Coût minimal pour tous les composants'
        regles=[*regles[:-1],('mc_v3_q5',
               "Quel est le coût minimal des achats nécessaires (châssis, hélices et batteries) "
               f"pour fabriquer {cible} drones, en tenant compte des pièces déjà disponibles et offertes ?")]
        calcul=(f"Châssis à acheter : {manque_chassis} à {prix_chassis} € ; "
                f"hélices manquantes {manque_hel} en sachets de {h[1]} à {h[2]} € ; "
                f"batteries manquantes {manque_bat} en boîtes de {b[1]} à {b[2]} €. "
                f"Coût total minimal **{total} €**.")

    elif identifiant == 'P9-M10':
        # RV19 : optimisation entière avec possibilité de mélanger A/B pour Q5.
        pA=_mc_v3_extraire(r'\*\*Offre A\*\*.*?(\d+) carreaux par boîte.*?(\d+) € par boîte',avant,identifiant)
        pB=_mc_v3_extraire(r'\*\*Offre B\*\*.*?(\d+) carreaux par boîte.*?(\d+) € par boîte',avant,identifiant)
        aN,aP=map(int,pA.groups());bN,bP=map(int,pB.groups())
        besoin=int(champs['r1']['attendu']);extra=int(_mc_v3_extraire(r'\*\*Nouveau défi :\*\*\s*(\d+) carreaux supplémentaires',contexte,identifiant).group(1));total=besoin+extra
        candidats=[]
        for b in range((total+bN-1)//bN+2):
            a=(max(0,total-b*bN)+aN-1)//aN
            candidats.append((a*aP+b*bP,a,b))
        cout,qa,qb=min(candidats)
        contexte=(f"\n\n**Nouveau défi :** {extra} carreaux supplémentaires "
                  "sont nécessaires avant la commande. Pour ce nouveau besoin, "
                  "les deux magasins acceptent exceptionnellement une commande "
                  "MIXTE : le collège peut acheter autant de boîtes entières A "
                  "et B qu'il souhaite, même en combinant les deux formats. "
                  "Les capacités et les prix par boîte ne changent pas.\n\n")
        champs['mc_v3_q5']['attendu']=cout
        champs['mc_v3_q5']['unite']='€'
        champs['mc_v3_q5']['libelle']='Coût minimal pour un mélange de boîtes'
        regles=[*regles[:-1],('mc_v3_q5',
              "Quel est le coût minimal de commande pour ce nouveau nombre "
              "de carreaux en choisissant librement les quantités de boîtes A "
              "et B (les deux formats peuvent être mélangés) ?")]
        calcul=(f"**Défi final — deux formats combinables :** "
                f"besoin {total} carreaux ; boîte A : {aN} à {aP} €, "
                f"boîte B : {bN} à {bP} €. "
                f"Coût minimal : {qa} boîte(s) A et {qb} boîte(s) B "
                f"pour **{cout} €**.")

    elif identifiant == 'P9-M05':
        # RV20 : prix en euros et non nombre de colis.
        champs['mc_v3_q5']['unite']='€'

    elif identifiant == 'P8-M01':
        # RV14 : la mention « euros et centimes » correspond à une étape
        # facultative, sans question dédiée ; la retirer pour éviter l'attente.
        blocs[0]=avant.replace('Chaque club peut recevoir des euros et des centimes.',
                              'Le partage peut produire un montant non entier en euros.')

    return regles,contexte,calcul


_MC_N7_REVISIONS_CIBLEES = {
    "P7-M03", "P7-M07", "P7-M09", "P7-M10", "P7-M13",
    "P7-M19", "P7-M21", "P7-M23",
}



# ================================================================
# N8 : correction pédagogique compacte, une réponse + sa méthode.
# Ne modifie jamais le nombre de champs, ni les valeurs attendues.
# ================================================================
def _mc_n8_fr(v,decimales=2):
    if isinstance(v,int) or (isinstance(v,float) and v.is_integer()):
        return str(int(v))
    return (f"{v:.{decimales}f}".rstrip('0').rstrip('.')).replace('.',',')


def _mc_n8_compacter_texte(texte):
    texte=re.sub(r'\*\*Expression complète\s*:\*\*\s*', 'Expression complète : ', texte)
    texte=re.sub(r'\*\*Réponse\s*:\*\*\s*', '', texte)
    texte=re.sub(r'\*\*Défi final[^*]*\*\*\s*', '', texte)
    texte=re.sub(r'\*\*Nouveau défi[^*]*\*\*\s*', '', texte)
    texte=re.sub(r'\n\s*\n+', ' ', texte.strip())
    texte=re.sub(r'\s+', ' ', texte)
    texte=re.sub(r'(?<=\d)\.00(?=\s|\D)', ',00', texte)
    return texte.strip()


def _mc_n8_etapes_source(correction):
    if '**Méthode et calculs détaillés**' in correction:
        source=correction.split('**Méthode et calculs détaillés**',1)[1]
    else:
        source=correction
    parties=re.split(r'(?m)^\*\*Étape(?:\s*\d+\s*—|\s*:)\s*[^*\n]+\*\*\s*',source)
    return [_mc_n8_compacter_texte(p) for p in parties[1:] if p.strip()]


def _mc_n8_enrichir_dernier(ex,etapes):
    """Calculs explicites des questions finales, sans modifier les réponses."""
    nom=ex['id']; q=ex['champs_reponse']; t=ex['enonce']
    v=[c['attendu'] for c in q]
    f=_mc_n8_fr
    audit=ex.get('_mathicap_audit_nouveau',{})
    if nom=='P8-M03':
        m=re.search(r'chemin A,? impose désormais un péage de (\d+) pièces',t)
        if m:
            peage=int(m[1]);solde_a=v[1]-peage; solde_b=v[2]
            etapes[4]=(f'Chemin A après péage : {f(v[1])} − {peage} = {f(solde_a)} pièces. '
                       f'Chemin B inchangé : {f(solde_b)} pièces. '
                       f'Différence signée A − B : {f(solde_a)} − {f(solde_b)} = {f(v[4])} pièces.')
            ex['enonce']=ex['enonce'].replace('le chemin A, impose', 'le chemin A impose')
    if nom=='P8-M10':
        ex['enonce']=ex['enonce'].replace('l’entreprise A, augmente','l’entreprise A augmente').replace("l'entreprise A, augmente","l'entreprise A augmente")
    if nom=='P8-M04':
        # Reconstituer les deux devis à partir du besoin des nouvelles équipes.
        a=re.search(r'(\d+) équipes participent',t)
        b=re.search(r'(\d+) équipes supplémentaires rejoignent',t)
        c=re.search(r'A, (\d+) batteries par boîte à (\d+) € ; B, (\d+) batteries par boîte à (\d+) €',t)
        if a and b and c:
            equipes,ajout=int(a[1]),int(b[1]);need_per=v[0]//equipes
            need=(equipes+ajout)*need_per;stock=v[1];manque=max(0,need-stock)
            pa,ca,pb,cb=map(int,c.groups())
            qa=(manque+pa-1)//pa;qb=(manque+pb-1)//pb
            couta=qa*ca;coutb=qb*cb
            etapes[4]=(f'Besoin pour {equipes+ajout} équipes : {equipes+ajout} × {need_per} = {need} batteries. '
                       f'Stock utilisable : {stock} batteries ; il manque {need} − {stock} = {manque} batteries. '
                       f'Offre A : {qa} boîte(s) entières de {pa} batteries × {ca} € = {couta} €. '
                       f'Offre B : {qb} boîte(s) entières de {pb} batteries × {cb} € = {coutb} €. '
                       f'Le coût minimal est {f(min(couta,coutb))} €.')
        d=re.search(r'boîtes de \d+ batteries, au prix de (\d+) € chacune',t)
        if d:
            etapes[3]=f'{f(v[2])} boîte(s) × {d[1]} € = {f(v[3])} €.'
    elif nom=='P8-M05':
        m1=re.search(r'(\d+) équipes participent',t)
        m2=re.search(r'comporte (\d+) postes',t)
        m3=re.search(r'chaque enveloppe coûte ([\d,.]+)\s*€',t)
        m4=re.search(r'pochette de matériel à ([\d,.]+)\s*€',t)
        m5=re.search(r'(\d+) équipes supplémentaires',t)
        m6=re.search(r'souvenirs peuvent être achetés à ([\d,.]+)\s*€ l.unité',t)
        m7=re.search(r'lots indivisibles de (\d+) à ([\d,.]+)\s*€',t)
        m8=re.search(r'conserver au moins \*\*([\d,.]+)\s*€\*\* de réserve',t)
        if all([m1,m2,m3,m4,m5,m6,m7]):
            n,postes,ajout=map(lambda m:int(m.group(1)),[m1,m2,m5]); pe=float(m3.group(1).replace(',','.')); pp=float(m4.group(1).replace(',','.'))
            ps=float(m6.group(1).replace(',','.')); lot=int(m7.group(1)); pl=float(m7.group(2).replace(',','.'))
            extra=ajout*(postes*pe+pp); total=n+ajout; unites=total*ps; nb=(total+lot-1)//lot; lots=nb*pl
            reserve=float(m8.group(1).replace(',','.')) if m8 else 0
            etapes[4]=(f'Achats obligatoires des {ajout} nouvelles équipes : {ajout} × '
                       f'({postes} × {f(pe)} + {f(pp)}) = {f(extra)} €. '
                       f'Souvenirs pour {total} équipes : à l’unité {total} × {f(ps)} = {f(unites)} € ; '
                       f'par lots {nb} × {f(pl)} = {f(lots)} €. '
                       f'On retient {f(min(unites,lots))} €. '
                       f'Après les achats initiaux il reste {f(v[2])} €. '
                       f'Solde final : {f(v[2])} − {f(extra)} − {f(min(unites,lots))} − {f(reserve)} = {f(v[4])} €.')
    elif nom=='P8-M06':
        a=re.search(r'(\d+) nouvelles équipes',t)
        b=re.search(r'coûtent (\d+)\s*€ chacun à l.unité',t)
        c=re.search(r'(\d+)\s*€ par lot indivisible de (\d+) kits',t)
        d=re.search(r'budget de\s*\*\*(\d+)\s*€',t)
        if all([a,b,c,d]):
            n,pu,lotprix,taille,budget=int(a[1]),int(b[1]),int(c[1]),int(c[2]),int(d[1])
            lotnb=(n+taille-1)//taille; cu=n*pu; cl=lotnb*lotprix
            etapes[4]=(f'Commande initiale : {f(v[2])} € (remise et livraison déjà comptées). '
                       f'Commande complémentaire distincte, sans nouvelle remise ni frais de livraison : '
                       f'{n} kits à l’unité × {pu} € = {cu} € ; ou {lotnb} lot(s) de {taille} kits '
                       f'à {lotprix} € = {cl} €. Le moins cher coûte {min(cu,cl)} €. '
                       f'Coût des deux commandes : {f(v[2])} + {min(cu,cl)} = {f(v[2]+min(cu,cl))} €. '
                       f'Financement à trouver : max(0, {f(v[2]+min(cu,cl))} − {budget}) = {f(v[4])} €.')
            ex['enonce']=re.sub(r'(La réduction et la livraison de la commande initiale restent inchangées\.)',
                     ('La commande initiale conserve sa réduction et ses frais de livraison, déjà inclus dans son prix. '
                      'Les kits des nouvelles équipes font l’objet d’une commande complémentaire distincte, '
                      'sans nouvelle remise ni frais de livraison supplémentaires.'),ex['enonce'])
    elif nom=='P8-M07':
        a=re.search(r'Dans .*?, (\d+) robinets',t)
        b=re.search(r'au moins ([\d,.]+)\s*L',t)
        if a and b:
            n=int(a[1]); objectif=float(b[1].replace(',','.')); par=v[3]/n; manque=max(0,objectif-v[3])
            etapes[4]=(f'Économie par robinet sur la période : {f(v[3])} ÷ {n} = {f(par)} L. '
                       f'Objectif total : {f(objectif)} L ; les {n} robinets économisent déjà {f(v[3])} L. '
                       f'Économie restant à réaliser : {f(objectif)} − {f(v[3])} = {f(manque)} L. '
                       f'Nombre de robinets supplémentaires : {f(manque)} ÷ {f(par)} = '
                       f'{f(manque/par)} ; on arrondit à l’entier supérieur : {f(v[4])} robinets.')
    elif nom=='P8-M08':
        a=re.search(r'détour A de ([\d,.]+)\s*km.*?pause de (\d+) minutes',t,re.S)
        b=re.search(r'sentier B de ([\d,.]+)\s*km sans pause',t)
        c=re.search(r'allure régulière de (\d+) minutes',t)
        d=re.search(r'en \*\*(\d+) minutes au maximum',t)
        if all([a,b,c,d]):
            ka=float(a[1].replace(',','.'));pa=int(a[2]);kb=float(b[1].replace(',','.')); pace=int(c[1]);limit=int(d[1]);da=ka*pace+pa;db=kb*pace; total=v[3]+min(da,db)
            etapes[4]=(f'Détour A : {f(ka)} × {pace} + {pa} = {f(da)} min. '
                       f'Détour B : {f(kb)} × {pace} = {f(db)} min. '
                       f'On choisit le plus rapide ({f(min(da,db))} min). '
                       f'Durée totale : {f(v[3])} + {f(min(da,db))} = {f(total)} min. '
                       f'Différence avec la limite : {limit} − {f(total)} = {f(v[4])} min.')
    elif nom=='P8-M10':
        m=re.search(r'augmente ses frais fixes de (\d+)\s*€',t)
        if m:
            hausse=int(m[1]); etapes[4]=(f'Nouveau coût A : {f(v[1])} + {hausse} = {f(v[1]+hausse)} €. '
                       f'Le prix B reste {f(v[2])} €. Différence coût A − coût B : '
                       f'{f(v[1]+hausse)} − {f(v[2])} = {f(v[4])} €.')
    elif nom=='P8-M11' and audit:
        x=audit;teams=x['teams']; per=x['per'];extra=x['extra'];pack=x['pack']
        usable=x['stock']-x['bad'];initialboxes=v[3];after=usable+initialboxes*pack;need=(teams+extra)*per;missing=max(0,need-after)
        etapes[4]=(f'Pour {teams+extra} équipes il faut {teams+extra} × {per} = {need} badges. '
                   f'Après la première commande, {usable} + {initialboxes} × {pack} = {after} badges sont disponibles. '
                   f'Il manque {need} − {after} = {missing} badges. '
                   f'Chaque boîte contient {pack} badges : {missing} ÷ {pack} impose {f(v[4])} boîtes supplémentaires, en arrondissant au supérieur.')
    elif nom=='P8-M13' and audit:
        x=audit;boite=x['box']; add=x['add']; utilisables=x['frames']-x['bad']; besoin=x['sections']*x['per']
        n=(max(0,besoin-utilisables)+boite-1)//boite
        stock=utilisables+n*boite;reste=stock-besoin; manque=max(0,add-reste)
        etapes[4]=(f'Après l’achat initial, il reste {stock} − {besoin} = {reste} cadres. '
                   f'Pour les {add} nouvelles photos, il manque {add} − {reste} = {manque} cadres. '
                   f'Les boîtes contenant {boite} cadres, il faut {f(v[4])} boîte(s) supplémentaire(s), en arrondissant {manque} ÷ {boite} au supérieur.')
    elif nom=='P8-M15' and audit:
        x=audit;nm=max(0,x['target']*2-x['motors']);nb=max(0,x['target']*3-x['batteries'])
        lm=(nm+x['packmot']-1)//x['packmot'];lb=(nb+x['packbat']-1)//x['packbat']
        etapes[4]=(f'Pour {x["target"]} robots, il faut {x["target"]} × 2 = {x["target"]*2} moteurs '
                   f'et {x["target"]} × 3 = {x["target"]*3} batteries. '
                   f'Le stock contient {x["motors"]} moteurs et {x["batteries"]} batteries. '
                   f'Moteurs manquants : {nm}, soit {lm} lot(s) de {x["packmot"]}, à {x["costmot"]} € le lot : {lm*x["costmot"]} €. '
                   f'Batteries manquantes : {nb}, soit {lb} lot(s) de {x["packbat"]}, à {x["costbat"]} € le lot : {lb*x["costbat"]} €. '
                   f'Coût des deux achats : {lm*x["costmot"]} + {lb*x["costbat"]} = {f(v[4])} €.')
    elif nom=='P8-M19' and audit:
        x=audit; manque=v[2];eco_a=x['liters']*x['days'];eco_b=x['liters_b']*x['days']
        nb_a=(manque+eco_a-1)//eco_a;nb_b=(manque+eco_b-1)//eco_b
        total_a=nb_a*x['price_a']; total_b=nb_b*x['price_b']
        etapes[4]=(f'Pour économiser encore {manque} L, le modèle A économise {eco_a} L par appareil '
                   f'sur {x["days"]} jours : il en faut {nb_a}, coût {nb_a} × {x["price_a"]} = {total_a} €. '
                   f'Le modèle B économise {eco_b} L par appareil : il en faut {nb_b}, coût '
                   f'{nb_b} × {x["price_b"]} = {total_b} €. Le coût minimal est {f(v[4])} €.')
    elif nom=='P8-M18' and audit:
        km,pace,laps,pause,detour,limit=(audit[k] for k in ('km','pace','laps','pause','detour','limit'))
        after=v[3]+detour*pace
        etapes[4]=(f'Le détour prend {detour} × {pace} = {detour*pace} min. '
                    f'Durée totale après détour : {v[3]} + {detour*pace} = {after} min. '
                    f'Différence entre durée et limite : {after} − {limit} = {f(v[4])} min.')
        ex['enonce']=ex['enonce'].replace(
            'De combien de minutes la durée après détour dépasse-t-elle la limite (résultat positif), ou reste-t-elle en dessous (résultat négatif) ?',
            'Quelle est la différence, en minutes, entre la durée après le détour et la limite autorisée ?')
    elif nom=='P8-M20' and audit:
        n,cap,price,entry,carprice=(int(audit[k]) for k in ('classes','cap','ticket','ticket','buscost')) if False else (v[0],int(audit['cap']),int(audit['ticket']),v[1],int(audit['buscost']))
        quotient,reste=divmod(n,cap)
        etapes[2]=(f'{n} ÷ {cap} = {quotient}, reste {reste}. '
                   +(f'{quotient} cars ne suffisent pas pour les {reste} dernières personnes, donc il faut {quotient+1} cars.' if reste else f'La division est exacte : {quotient} cars suffisent.') )
        montantb=int(audit['groupbuscost']); coutb=entry+montantb
        etapes[4]=(f'Transport A : {v[2]} cars × {carprice} = {v[2]*carprice} €. '
                   f'Billets + transport A : {entry} + {v[2]*carprice} = {v[3]} €. '
                   f'Transport B : un car à {montantb} €. '
                   f'Billets + transport B : {entry} + {montantb} = {coutb} €. '
                   f'On compare {v[3]} € et {coutb} € : le budget minimal est {v[4]} €.')
    return etapes


def _mc_n8_polish(ex):
    """Une correction par question N8, concise, explicite, sans bloc de réponses doublé."""
    if int(ex.get('mathicap_niveau_pedagogique', 0))!=8:
        return ex
    champs=ex.get('champs_reponse',[])
    if len(champs)!=5:
        raise ValueError('N8 : cinq champs requis pour '+ex.get('id','?'))
    etapes=_mc_n8_etapes_source(ex.get('correction',''))
    if len(etapes)!=5:
        raise ValueError(f"N8 {ex['id']} : {len(etapes)} étapes, cinq attendues")
    f=_mc_n8_fr
    if ex['id']=='P8-M01':
        e3=champs[2]['attendu'];e4=champs[3]['attendu']
        reserve=e3-e4
        etapes[2]=f"Recettes {f(champs[0]['attendu'])} € − dépenses {f(champs[1]['attendu'])} € = {f(e3)} €."
        etapes[3]=(f"Bénéfice {f(e3)} € − réserve {f(reserve)} € = {f(e4)} € à partager. "
                   +etapes[3])
    if ex['id']=='P8-M04':
        t=ex['enonce'];a=re.search(r'boîtes de (\d+) batteries, au prix de (\d+) € chacune',t)
        if a:
            paquet,prix=int(a[1]),int(a[2]);need=max(0,champs[0]['attendu']-champs[1]['attendu'])
            quotient,reste=divmod(need,paquet)
            etapes[2]=(f'Batteries manquantes : {champs[0]["attendu"]} − {champs[1]["attendu"]} = {need}. '
                      f'Une boîte contient {paquet} batteries. Division : {need} ÷ {paquet} = '
                      f'{quotient}, reste {reste}. '
                      f'Il faut {champs[2]["attendu"]} boîtes entières au minimum.')
            etapes[3]=(f'{champs[2]["attendu"]} × {prix} = {f(champs[3]["attendu"])} €.')
        else:
            old=etapes[:]
            etapes[2]=old[2]+' '+re.split(r'Coût :',old[3])[0]
            etapes[3]=f"{f(champs[2]['attendu'])} boîte(s) × prix par boîte = {f(champs[3]['attendu'])} €."
    etapes=_mc_n8_enrichir_dernier(ex,etapes)
    # Correction compacte : la réponse chiffrée figure au début de son propre calcul.
    sorties=[]
    for i,(champ,exp) in enumerate(zip(champs,etapes),1):
        x=champ['attendu'];texte=f(x) if isinstance(x,(int,float)) and not isinstance(x,bool) else str(x)
        unite=champ.get('unite','')
        valeur=texte+((' '+unite) if unite else '')
        libelle=champ.get('libelle',f'Question {i}').strip().rstrip('?').rstrip(':').strip()
        sorties.append(f"**Réponse {i} — {libelle} : {valeur}.** {exp}")
    ex['correction']='\n\n'.join(sorties)
    ex['correction']=re.sub(r'(?<=\d)\.(?=\d)', ',', ex['correction'])
    ex['correction']=re.sub(r'⌈([^⌉]+)⌉', lambda m: 'arrondi à l’entier supérieur de ('+m.group(1).replace('/', ' ÷ ')+')', ex['correction'])
    # Accord des unités au singulier dans les corrections.
    for pluriel,singulier in [('boîtes','boîte'),('rouleaux','rouleau'),('lots','lot'),('cars','car'),('navettes','navette'),('économiseurs','économiseur'),('sacs','sac'),('bouteilles','bouteille')]:
        ex['correction']=re.sub(r'\b1 '+pluriel+r'\b', '1 '+singulier, ex['correction'])
    ex['correction']=ex['correction'].replace('1 nouvelles boîtes','1 nouvelle boîte').replace('1 boîte(s)','1 boîte').replace('1 lot(s)','1 lot')
    ex['correction']=re.sub(r'(\d+) boîte\(s\)', lambda m: m.group(1)+' '+('boîte' if m.group(1)=='1' else 'boîtes'), ex['correction'])
    ex['correction']=re.sub(r'(\d+) lot\(s\)', lambda m: m.group(1)+' '+('lot' if m.group(1)=='1' else 'lots'), ex['correction'])
    ex['enonce']=re.sub(r'\n{3,}', '\n\n', ex['enonce'])
    ex['enonce']=re.sub(r'(?<=\d)\.(?=\d)', ',', ex['enonce'])
    ex['mathicap_revision_corrections']='2026-11-18-n8-relecture-detaillee'
    return ex

def _mc_uniformiser_exercice(exercice):
    """Retourne une COPIE structurée, sans altérer l'exercice historique source."""
    if not isinstance(exercice, dict) or exercice.get("id") not in REGLES:
        return exercice
    if exercice.get("mathicap_questions_uniformisees"):
        return exercice
    resultat = deepcopy(exercice)
    identifiant = resultat["id"]
    regles = REGLES[identifiant]
    niveau = int(identifiant[1])
    nombre_attendu = 4 if niveau == 7 else 5
    if len(regles) != nombre_attendu:
        raise ValueError(f"Nombre de questions incorrect : {identifiant}")

    blocs = resultat["enonce"].split("**Questions**")
    if len(blocs) != 2:
        raise ValueError(f"Bloc de questions introuvable ou ambigu : {identifiant}")
    par_id = {champ["id"]: deepcopy(champ) for champ in resultat["champs_reponse"]}
    if len(par_id) != len(resultat["champs_reponse"]):
        raise ValueError(f"Identifiants de champs dupliqués : {identifiant}")
    par_id.update(_champs_ajoutes(resultat, par_id))
    if identifiant in _MC_N7_REVISIONS_CIBLEES:
        contexte_v3, calcul_v3 = "", ""
        regles = list(regles)
        if identifiant == "P7-M09":
            possible = par_id["r4"]["attendu"] == "Oui"
            regles[-1] = ("r5", (
                "Peut-il acheter l'équipement ? Si oui, combien de pièces lui restera-t-il ?"
                if possible else
                "Peut-il acheter l'équipement ? Combien de pièces lui manque-t-il ?"))
        elif identifiant == "P7-M10":
            possible = par_id["r4"]["attendu"] == "Oui"
            regles[-1] = ("r5", (
                "Combien de feuilles restera-t-il après avoir préparé l'exposition ?"
                if possible else
                "Combien de feuilles manquera-t-il pour préparer l'exposition ?"))
    else:
        regles, contexte_v3, calcul_v3 = _mc_v3_preparer(resultat, par_id, regles, blocs)
        regles, contexte_v3, calcul_v3 = _mc_v31_affiner(
            resultat, par_id, regles, blocs, contexte_v3, calcul_v3)
        regles, contexte_v3, calcul_v3 = _mc_v32_finaliser(
            resultat, par_id, regles, blocs, contexte_v3, calcul_v3)
    # Le tournoi peut présenter un manque ou un surplus selon le tirage.
    # La question finale pose une seule demande numérique et ne prescrit pas la méthode.
    if identifiant == "P7-M12":
        regles = [*regles[:-1], (
            "r4",
            "Combien d'euros restera-t-il du budget après paiement des billets et des cars ?"
            if resultat.get("mathicap_budget_suffisant") else
            "Combien d'euros manque-t-il pour payer les billets et les cars ?",
        )]

    if identifiant == "P7-M17":
        regles = [*regles[:-1], (
            "r4", _mc_question_finale_echecs(resultat["mathicap_solde_positif"]),
        )]
    if identifiant == "P7-M18":
        regles = [*regles[:-1], (
            "r4",
            "Combien d'euros restera-t-il du budget après l'achat des pots nécessaires ?"
            if resultat["mathicap_budget_suffisant"]
            else "Combien d'euros manque-t-il au collège pour acheter tous les pots nécessaires ?",
        )]
    if identifiant == "P7-M20":
        regles = [*regles[:-1], (
            "r4",
            "De combien d'euros la somme disponible dépasse-t-elle l'objectif de don après les frais ?"
            if resultat["mathicap_objectif_atteint"]
            else "De combien d'euros la somme disponible est-elle inférieure à l'objectif de don après les frais ?",
        )]
    if identifiant == "P7-M05":
        regles = [*regles[:-1], (
            "r4", "Combien de petits tours supplémentaires chaque cycliste doit-il effectuer au minimum pour atteindre l'objectif du groupe ?",
        )]
    if identifiant == "P7-M24":
        regles = [*regles[:-1], (
            "r4", _mc_libelle_question_finale_casiers(resultat["mathicap_stock_suffisant"]),
        )]
    if identifiant == "P7-M26":
        regles = [*regles[:-1], (
            "r4",
            "Combien d'euros restera-t-il du budget après l'achat des bidons et du filtre ?"
            if resultat["mathicap_budget_suffisant"]
            else "Combien d'euros manque-t-il pour acheter tous les bidons et le filtre ?",
        )]
    if identifiant == "P7-M08":
        stock_suffisant = par_id.get("r4", {}).get("attendu")
        if stock_suffisant not in ("Oui", "Non"):
            raise ValueError("Indicateur de stock absent pour P7-M08")
        formulation = (
            "Combien de volants restera-t-il au club après le tournoi ?"
            if stock_suffisant == "Oui"
            else "Combien de volants manque-t-il au club pour tous les matchs ?"
        )
        regles = [*regles[:-1], ("r5", formulation)]
    categories = _CATEGORIES_PAR_MODELE[identifiant].split()
    if len(categories) != nombre_attendu:
        raise ValueError(f"Catégories de compétences incomplètes : {identifiant}")
    nouveaux_champs = []
    lignes_questions = []
    lignes_corrige = []
    for position, (cle, libelle) in enumerate(regles, 1):
        if cle not in par_id:
            raise ValueError(f"Champ attendu absent : {identifiant}/{cle}")
        champ = par_id[cle]
        if champ["type"] not in ("nombre", "choix"):
            raise ValueError(f"Champ non automatiquement évalué : {identifiant}/{cle}")
        champ["question"] = position
        # Une réponse = une évaluation autonome, même pour une décision.
        # Sinon une erreur en Q3 pourrait invalider également une Q4 correcte.
        champ.pop("dependances", None)
        champ["mathicap_competence"] = _CATEGORIES[categories[position - 1]]
        nouveaux_champs.append(champ)
        lignes_questions.append(f"{position}. {libelle}")
        lignes_corrige.append(f"**Question {position} — {champ['libelle']} :** {_formater_reponse(champ)}")
    if len({c["id"] for c in nouveaux_champs}) != len(nouveaux_champs):
        raise ValueError(f"Champ sélectionné plusieurs fois : {identifiant}")

    # Le nouveau défi ne doit PAS modifier rétroactivement le sens de Q1-Q4.
    # Il est présenté entre la question précédente et la question finale.
    if contexte_v3:
        questions_affichees = (
            "\n\n".join(lignes_questions[:-1]) + contexte_v3
            + "\n\n" + lignes_questions[-1]
        )
    else:
        questions_affichees = "\n\n".join(lignes_questions)
    resultat["enonce"] = (
        blocs[0].rstrip() + "\n\n**Questions**\n\n"
        + questions_affichees
        + "\n\n*Écris tes calculs et ton raisonnement au brouillon. "
        "Les champs de réponse sont notés automatiquement ; "
        "compare ta méthode avec la correction.*"
    )
    ancien_corrige = resultat.get("correction") or ""
    # Le raisonnement d'origine est conservé, mais les numéros de ses étapes
    # ne doivent pas entrer en contradiction avec les nouvelles questions.
    ancien_corrige = re.sub(r"(?m)^\*\*\d+\.\s*([^*\n]+)\*\*", r"**Étape : \1**", ancien_corrige)
    # Si le défi final a été remplacé, ne pas afficher comme méthode
    # actuelle l'ancienne question finale, devenue étrangère à Q5.
    if calcul_v3:
        positions = list(re.finditer(r"(?m)^\*\*Étape : ", ancien_corrige))
        if len(positions) >= nombre_attendu:
            ancien_corrige = ancien_corrige[:positions[nombre_attendu - 1].start()].rstrip()
    if identifiant == 'P9-M04':
        ancien_corrige=ancien_corrige.split('**Étape : Nombre maximal d\'équipements**')[0].rstrip()
    # Réponses numériques affichées à leur position de question ; calculs détaillés
    # en dessous dans l'ordre, y compris lorsqu'une Q5 a été construite en V3.
    calcul_final = ("\n\n**Étape : Calcul de la dernière question**\n\n" + calcul_v3.strip()) if calcul_v3 else ""
    resultat["correction"] = (
        "**Réponses attendues — questions de ce problème**\n\n"
        + "\n\n".join(lignes_corrige)
        + "\n\n**Méthode et calculs détaillés**\n\n"
        + ancien_corrige + calcul_final
    )
    resultat["champs_reponse"] = nouveaux_champs
    resultat["mathicap_questions_uniformisees"] = 3
    resultat["mathicap_revision_pedagogique"] = (
        "v3.2-lot-n7-ajustements-20261117"
        if identifiant in {"P7-M03", "P7-M05", "P7-M13", "P7-M24"}
        else "v3.2-lot-n7-simplifie"
    )
    resultat["mathicap_niveau_pedagogique"] = niveau
    resultat["mathicap_referentiel_pedagogique"] = "MathiCap V3.2 — contre-expertise et cohérence des variantes"
    return _mc_n8_polish(resultat)


# ================================================================
# MATHICAP — 30 MODÈLES NOUVEAUX N8/N9 (15 par niveau)
# Chaque problème est une unité autonome : cinq questions, cinq
# réponses numériques ou choix, et correction détaillée ordonnée.
# ID historiques inchangés ; nouvelles références P8/P9-M11...M25.
# ================================================================

def _mc_new_ceil(a,b):
    return (a+b-1)//b


def _mc_new_problem(level, idx, seed, title, paragraphs, questions, answers, labels, units, competences, steps, audit):
    model_id=f"P{level}-M{idx:02d}"
    if not (len(questions)==len(answers)==len(labels)==len(units)==len(competences)==len(steps)==5):
        raise AssertionError(f"Structure incomplète {model_id}")
    champs=[]
    for j,(ans,label,unit,cat) in enumerate(zip(answers,labels,units,competences),1):
        if isinstance(ans,str):
            assert ans in ('A','B','C','Oui','Non'),(model_id,j,ans)
            options=['A','B','C'] if ans in ('A','B','C') else ['Oui','Non']
            champs.append({'id':f'r{j}','question':j,'libelle':label,'type':'choix','attendu':ans,'options':options,'mathicap_competence':_CATEGORIES[cat]})
        else:
            assert isinstance(ans,(int,float)) and math.isfinite(ans),(model_id,j,ans)
            champs.append({'id':f'r{j}','question':j,'libelle':label,'type':'nombre','attendu':ans,'unite':unit,'mathicap_competence':_CATEGORIES[cat]})
    stmt=f"**{title}**\n\n"+'\n\n'.join(paragraphs)+'\n\n**Questions**\n\n'+'\n\n'.join(f'{i}. {q}' for i,q in enumerate(questions,1))
    stmt+='\n\n*Écris tes calculs et ton raisonnement au brouillon. Les champs de réponse sont notés automatiquement ; compare ta méthode avec la correction.*'
    ans_lines=[]
    for j,(c,unit) in enumerate(zip(champs,units),1):
        value=c['attendu']; suffix=f' {unit}' if unit and not isinstance(value,str) else ''
        ans_lines.append(f"**Question {j} — {c['libelle']} :** {value}{suffix}")
    correction=("**Réponses attendues — questions de ce problème**\n\n"+'\n\n'.join(ans_lines)
        +'\n\n**Méthode et calculs détaillés**\n\n'
        +'\n\n'.join(f'**Étape {j} — {labels[j-1]}**\n\n{step}' for j,step in enumerate(steps,1)))
    return _mc_n8_polish({'id':model_id,'titre':title,'seed':seed,'enonce':stmt,'correction':correction,
        'reponse_attendue':None,'champs_reponse':champs,
        'mathicap_questions_uniformisees':3,'mathicap_revision_pedagogique':'v3.3-30-modeles-n8-n9',
        'mathicap_niveau_pedagogique':level,'mathicap_referentiel_pedagogique':'Progression N8 autonomie / N9 optimisation',
        '_mathicap_audit_nouveau':audit})


def _mc_new_combo(need,size_a,cost_a,size_b,cost_b,max_a=None,max_b=None,fee_b=0):
    """Minimise le coût entier sous besoin minimal et bornes éventuelles."""
    ceiling=need+max(size_a,size_b)*2
    lim_a=min(max_a if max_a is not None else _mc_new_ceil(ceiling,size_a),30)
    lim_b=min(max_b if max_b is not None else _mc_new_ceil(ceiling,size_b),30)
    possibilities=[]
    for a in range(lim_a+1):
        for b in range(lim_b+1):
            if a*size_a+b*size_b>=need:
                price=a*cost_a+b*cost_b+(fee_b if b else 0)
                possibilities.append((price,a+b,a,b,a*size_a+b*size_b-need))
    if not possibilities:raise ValueError('Aucune solution admissible')
    return min(possibilities)


def _mc_new_2d_combo(need_x,need_y,ax,ay,cost_a,bx,by,cost_b,max_a=16,max_b=16):
    possibilities=[]
    for a in range(max_a+1):
        for b in range(max_b+1):
            if a*ax+b*bx>=need_x and a*ay+b*by>=need_y:
                possibilities.append((a*cost_a+b*cost_b,a+b,a,b))
    if not possibilities:raise ValueError('Aucune solution deux ressources')
    return min(possibilities)


def _mc_new_choose_a_b(price_a,price_b):
    return 'A' if price_a<price_b else ('B' if price_b<price_a else 'C')


def _mc_new_n8(idx,seed=None):
    rng,seed=_p9_rng(seed)
    model_id=f'P8-M{idx:02d}'
    if idx==11:
        # Quantités + conditionnement + extension de commande.
        teams=rng.randint(5,10); per=rng.randint(5,8); stock=rng.randint(9,25);bad=rng.randint(1,5)
        pack=rng.choice([6,8,10]); extra=rng.randint(2,4)
        need=teams*per; usable=stock-bad; deficit=max(0,need-usable)
        boxes=_mc_new_ceil(deficit,pack); new_need=(teams+extra)*per; extra_boxes=_mc_new_ceil(max(0,new_need-(usable+boxes*pack)),pack)
        return _mc_new_problem(8,idx,seed,'Les badges du salon des sciences',[
            f'{teams} équipes de {per} élèves doivent recevoir chacune un badge.',
            f'Le club possède {stock} badges, dont {bad} sont abîmés. Les badges sont vendus par boîtes de {pack}.',
            f'Après la commande destinée aux {teams} équipes, {extra} équipes supplémentaires s’inscrivent. Les badges déjà achetés restent disponibles.'
        ],['Combien de badges faut-il pour les équipes initiales ?', 'Combien de badges du stock sont utilisables ?', 'Combien de badges manque-t-il avant l’achat ?', 'Combien de boîtes faut-il acheter pour les équipes initiales ?', 'Combien de boîtes supplémentaires faut-il commander pour les nouvelles équipes ?'],
        [need,usable,deficit,boxes,extra_boxes],['Badges nécessaires','Badges utilisables','Badges manquants','Boîtes initiales','Boîtes supplémentaires'],['badges','badges','badges','boîtes','boîtes'],['Q','Q','R','L','L'],[
            f'{teams} × {per} = {need}.',f'{stock} − {bad} = {usable}.',f'{need} − {usable} = {deficit}.',f'{deficit} ÷ {pack}, en arrondissant au supérieur, donne {boxes} boîtes.',f'Besoin après inscription : ({teams}+{extra})×{per}={new_need}. Stock après la première commande : {usable}+{boxes}×{pack}={usable+boxes*pack}. Il faut encore {_mc_new_ceil(max(0,new_need-(usable+boxes*pack)),pack)} boîtes.'
        ],dict(kind='n8_badges',teams=teams,per=per,stock=stock,bad=bad,pack=pack,extra=extra))
    elif idx==12:
        n=rng.randint(42,88);add=rng.randint(9,19); cap_a=rng.choice([18,24,30]);cap_b=rng.choice([28,36,40]);price_a=rng.randint(85,130);price_b=rng.randint(130,190)
        # Pour que le nouveau groupe oblige à réviser les deux capacités.
        add=max(add,_mc_new_ceil(n,cap_a)*cap_a-n+1,_mc_new_ceil(n,cap_b)*cap_b-n+1)
        a=_mc_new_ceil(n,cap_a)*price_a;b=_mc_new_ceil(n,cap_b)*price_b;nn=n+add;aa=_mc_new_ceil(nn,cap_a)*price_a;bb=_mc_new_ceil(nn,cap_b)*price_b
        return _mc_new_problem(8,idx,seed,'Les navettes du musée',[
            f'{n} collégiens doivent se rendre au musée. Le transporteur A propose une navette de {cap_a} places à {price_a} € par navette ; B propose une navette de {cap_b} places à {price_b} €.',
            f'Une navette ne peut pas dépasser sa capacité. Après le premier devis, {add} participants s’ajoutent au groupe.'
        ],['Combien de navettes A faut-il pour le groupe initial ?','Quel est le coût total avec A pour le groupe initial ?','Quel est le coût total avec B pour le groupe initial ?','Quel est le coût le plus bas pour le groupe initial ?','Quel est le coût minimal de transport après l’arrivée des nouveaux participants ?'],
        [_mc_new_ceil(n,cap_a),a,b,min(a,b),min(aa,bb)],['Navettes A','Coût A','Coût B','Coût initial minimal','Coût final minimal'],['navettes','€','€','€','€'],['L','B','B','C','C'],[
            f'Il faut ⌈{n}/{cap_a}⌉ = {_mc_new_ceil(n,cap_a)} navettes A.',f'{_mc_new_ceil(n,cap_a)} × {price_a} = {a} €.',f'B : ⌈{n}/{cap_b}⌉ = {_mc_new_ceil(n,cap_b)} navettes à {price_b} €, soit {b} €.',f'Minimum entre {a} et {b} : {min(a,b)} €.',f'Nouveau groupe : {nn}. A : ⌈{nn}/{cap_a}⌉ × {price_a} = {aa} € ; B : ⌈{nn}/{cap_b}⌉ × {price_b} = {bb} €. Minimum : {min(aa,bb)} €.'
        ],dict(kind='n8_navette',n=n,add=add,cap_a=cap_a,cap_b=cap_b,price_a=price_a,price_b=price_b))
    elif idx==13:
        sections=rng.randint(4,8); per=rng.randint(9,14); frames=rng.randint(10,30);bad=rng.randint(1,6);box=rng.choice([6,8,10]);price=rng.randint(9,19);add=rng.randint(4,15)
        need=sections*per;usable=frames-bad;missing=need-usable;boxes=_mc_new_ceil(missing,box)
        # Calibration : 1, 2, 3 ou 4 nouvelles boîtes réellement nécessaires.
        spare=usable+boxes*box-need;choice_boxes=rng.randint(1,4)
        add=spare+(choice_boxes-1)*box+rng.randint(1,box)
        newboxes=_mc_new_ceil(max(0,need+add-usable-boxes*box),box)
        return _mc_new_problem(8,idx,seed,'Les cadres de l’exposition',[
            f'Une exposition comprend {sections} panneaux portant chacun {per} photographies. Chaque photographie doit être encadrée.',
            f'Le collège possède {frames} cadres, dont {bad} inutilisables. Une boîte apporte {box} cadres pour {price} €.',
            f'Après la première commande, {add} nouvelles photographies seront ajoutées.'
        ],['Combien de cadres faut-il pour l’exposition initiale ?','Combien de cadres utilisables le collège possède-t-il ?','Combien de cadres manque-t-il avant les achats ?','Quel est le coût minimal des boîtes nécessaires pour l’exposition initiale ?','Combien de nouvelles boîtes faut-il encore acheter pour les photographies ajoutées ?'],
        [need,usable,missing,boxes*price,newboxes],['Besoin en cadres','Cadres utilisables','Cadres manquants','Coût initial','Boîtes supplémentaires'],['cadres','cadres','cadres','€','boîtes'],['Q','Q','R','B','L'],[
            f'{sections} × {per} = {need}.',f'{frames} − {bad} = {usable}.',f'{need} − {usable} = {missing}.',f'Il faut ⌈{missing}/{box}⌉ = {boxes} boîtes, pour {boxes}×{price}={boxes*price} €.',f'Après le premier achat il reste {usable+boxes*box-need} cadres. Il faut {add} nouveaux cadres, donc ⌈max(0,{add}−{usable+boxes*box-need})/{box}⌉ = {newboxes} nouvelles boîtes.'
        ],dict(kind='n8_cadres',sections=sections,per=per,frames=frames,bad=bad,box=box,price=price,add=add))
    elif idx==14:
        start=rng.randint(120,210); received=rng.randint(5,9)*rng.choice([8,10,12]);loans=rng.randint(60,120);reserved=rng.randint(25,55); box_a=rng.choice([8,10]); cost_a=rng.randint(9,14);box_b=rng.choice([12,15]);cost_b=rng.randint(16,22)
        now=start+received-loans;need=max(5,reserved-now);a=_mc_new_ceil(need,box_a)*cost_a;b=_mc_new_ceil(need,box_b)*cost_b
        # Recentrer pour que le stock réservé crée un vrai manque.
        reserved=now+rng.randint(16,65);need=reserved-now;a=_mc_new_ceil(need,box_a)*cost_a;b=_mc_new_ceil(need,box_b)*cost_b
        return _mc_new_problem(8,idx,seed,'La réserve de mangas du CDI',[
            f'Le CDI possède {start} mangas. Il reçoit {received} mangas et en prête {loans}.',
            f'Pour préparer une exposition, il veut disposer de {reserved} mangas en réserve. Il peut acheter des lots A de {box_a} mangas à {cost_a} € ou des lots B de {box_b} mangas à {cost_b} €, sans mélanger les offres.'
        ],['Combien de mangas le CDI possède-t-il après les arrivées ?','Combien reste-t-il de mangas après les prêts ?','Combien de mangas lui manque-t-il pour préparer sa réserve ?','Combien coûterait l’achat de lots A suffisants ?','Quel est le coût le plus faible entre des lots A ou des lots B pour compléter la réserve ?'],
        [start+received,now,need,a,min(a,b)],['Mangas après réception','Mangas disponibles','Mangas manquants','Coût des lots A','Coût minimal'],['mangas','mangas','mangas','€','€'],['Q','R','R','B','C'],[
            f'{start}+{received}={start+received}.',f'{start+received}−{loans}={now}.',f'{reserved}−{now}={need}.',f'A : ⌈{need}/{box_a}⌉ × {cost_a}={a} €.',f'A : {a} € ; B : ⌈{need}/{box_b}⌉ × {cost_b}={b} €. Minimum {min(a,b)} €.'
        ],dict(kind='n8_manga',start=start,received=received,loans=loans,reserved=reserved,box_a=box_a,cost_a=cost_a,box_b=box_b,cost_b=cost_b))
    elif idx==15:
        target=rng.randint(8,13); motors=rng.randint(14,22); batteries=rng.randint(15,26); motper=2;batper=3; packmot=rng.choice([4,5,6]);packbat=rng.choice([5,6,8]);costmot=rng.randint(11,17);costbat=rng.randint(13,21)
        maxrob=min(motors//motper,batteries//batper);missmot=max(0,target*2-motors);missbat=max(0,target*3-batteries);expense=_mc_new_ceil(missmot,packmot)*costmot+_mc_new_ceil(missbat,packbat)*costbat
        return _mc_new_problem(8,idx,seed,'Les robots de l’atelier numérique',[
            f'Le collège dispose de {motors} moteurs utilisables et de {batteries} batteries utilisables. Chaque robot utilise 2 moteurs et 3 batteries.',
            f'Il souhaite construire {target} robots. Les moteurs supplémentaires se vendent par lots de {packmot} à {costmot} € et les batteries par lots de {packbat} à {costbat} €.'
        ],['Combien de robots les moteurs permettent-ils de fabriquer ?','Combien de robots les batteries permettent-elles de fabriquer ?','Combien de robots complets sont réalisables actuellement ?','Combien de batteries manque-t-il pour atteindre l’objectif ?','Quel est le coût minimal des lots de moteurs et de batteries supplémentaires nécessaires à l’objectif ?'],
        [motors//2,batteries//3,maxrob,missbat,expense],['Capacité moteurs','Capacité batteries','Robots réalisables','Batteries manquantes','Coût des composants'],['robots','robots','robots','batteries','€'],['L','L','L','R','B'],[
            f'{motors} ÷ 2 donne {motors//2} robots.',f'{batteries} ÷ 3 donne {batteries//3} robots.',f'Le minimum entre {motors//2} et {batteries//3} est {maxrob}.',f'{target}×3−{batteries}={target*3-batteries}, donc {missbat} manquantes.',f'Moteurs manquants : max(0,{target}×2−{motors})={missmot}, donc {_mc_new_ceil(missmot,packmot)} lots. Batteries : {missbat}, donc {_mc_new_ceil(missbat,packbat)} lots. Coût = {expense} €.'
        ],dict(kind='n8_robots',target=target,motors=motors,batteries=batteries,packmot=packmot,packbat=packbat,costmot=costmot,costbat=costbat))
    elif idx==16:
        n=rng.randint(25,65);add=rng.randint(8,20);fee_a=rng.randint(60,110);fee_b=rng.randint(110,195);each_a=rng.randint(5,8);each_b=rng.randint(3,6)
        a=fee_a+n*each_a;b=fee_b+n*each_b;na=fee_a+(n+add)*each_a;nb=fee_b+(n+add)*each_b
        return _mc_new_problem(8,idx,seed,'Les deux tarifs du cinéma',[
            f'Pour une séance, {n} élèves vont au cinéma. L’offre A coûte {fee_a} € de réservation puis {each_a} € par élève. L’offre B coûte {fee_b} € de réservation puis {each_b} € par élève.',
            f'Un second groupe de {add} élèves rejoint la sortie ; les frais de réservation restent inchangés.'
        ],['Combien coûte l’offre A pour le premier groupe ?','Combien coûte l’offre B pour le premier groupe ?','Quel est le prix le plus bas pour le premier groupe ?','Quel est l’écart entre les deux devis initiaux ?','Quel est le prix le plus bas après l’arrivée du second groupe ?'],
        [a,b,min(a,b),abs(a-b),min(na,nb)],['Prix A','Prix B','Prix minimal initial','Écart de prix','Prix minimal final'],['€','€','€','€','€'],['B','B','C','R','C'],[
            f'{fee_a}+{n}×{each_a}={a} €.',f'{fee_b}+{n}×{each_b}={b} €.',f'Minimum({a},{b})={min(a,b)} €.',f'|{a}−{b}|={abs(a-b)} €.',f'Pour {n+add} élèves, A={na} € et B={nb} €. Le plus petit coût est {min(na,nb)} €.'
        ],dict(kind='n8_cinema',n=n,add=add,fee_a=fee_a,fee_b=fee_b,each_a=each_a,each_b=each_b))
    elif idx==17:
        flags=rng.randint(17,37);cut=rng.randint(40,80);roll=rng.choice([400,500,600]);ribbon=3*cut;perroll=roll//ribbon;extra=rng.randint(3,11)
        while perroll<2:roll+=100;perroll=roll//ribbon
        nroll=_mc_new_ceil(flags,perroll);extra_roll=_mc_new_ceil(flags+extra,perroll)-nroll
        return _mc_new_problem(8,idx,seed,'Les fanions du tournoi de lecture',[
            f'Le collège fabrique {flags} fanions identiques. Chaque fanion utilise trois morceaux de ruban de {cut} cm.',
            f'Le ruban est vendu par rouleaux de {roll} cm. On ne raccorde jamais deux rouleaux pour un même fanion. Après le premier achat, le club décide de fabriquer {extra} fanions supplémentaires.'
        ],['Combien de centimètres faut-il pour un fanion ?','Combien de fanions complets peut-on couper dans un rouleau ?','Combien de rouleaux faut-il acheter pour la première commande ?','Combien de centimètres reste-t-il sur le dernier rouleau après les fanions initialement prévus ?','Combien de rouleaux supplémentaires faut-il pour fabriquer les fanions ajoutés ?'],
        [ribbon,perroll,nroll,roll-(flags-(nroll-1)*perroll)*ribbon,extra_roll],['Ruban par fanion','Fanions par rouleau','Rouleaux initiaux','Chute dernier rouleau','Nouveaux rouleaux'],['cm','fanions','rouleaux','cm','rouleaux'],['Q','L','L','R','L'],[
            f'3×{cut}={ribbon} cm.',f'{roll} ÷ {ribbon} donne {perroll} fanions entiers.',f'⌈{flags}/{perroll}⌉={nroll} rouleaux.',f'Dernier rouleau : {flags-(nroll-1)*perroll} fanions, donc {roll}−{flags-(nroll-1)*perroll}×{ribbon}={roll-(flags-(nroll-1)*perroll)*ribbon} cm de chute.',f'Pour {flags+extra} fanions il faut {_mc_new_ceil(flags+extra,perroll)} rouleaux au total, soit {extra_roll} de plus.'
        ],dict(kind='n8_fanions',flags=flags,cut=cut,roll=roll,extra=extra))
    elif idx==18:
        km=rng.randint(3,7);pace=rng.choice([9,10,12]); laps=rng.randint(3,6);pause=rng.randint(5,10); detour=rng.randint(2,5);limit=(km*laps*pace+(laps-1)*pause+detour*pace)+rng.choice([-10,-5,10,20])
        walk=km*laps*pace;breaks=(laps-1)*pause;total=walk+breaks;last=total+detour*pace
        return _mc_new_problem(8,idx,seed,'Le sentier et les pauses',[
            f'Une équipe effectue {laps} tours de {km} km à {pace} minutes par kilomètre. Entre deux tours, elle fait une pause de {pause} minutes (aucune pause après le dernier tour).',
            f'La durée autorisée est {limit} minutes. Le guide propose ensuite un détour supplémentaire de {detour} km parcouru à la même allure.'
        ],['Quelle distance totale le groupe parcourt-il avant le détour ?','Combien de minutes dure la marche, sans les pauses ?','Combien de minutes durent toutes les pauses ?','Quelle est la durée totale initiale ?','De combien de minutes la durée après détour dépasse-t-elle la limite (résultat positif), ou reste-t-elle en dessous (résultat négatif) ?'],
        [km*laps,walk,breaks,total,last-limit],['Distance initiale','Durée de marche','Durée des pauses','Durée initiale','Écart à la limite'],['km','min','min','min','min'],['D','D','D','D','R'],[
            f'{km}×{laps}={km*laps} km.',f'{km*laps}×{pace}={walk} minutes.',f'({laps}−1)×{pause}={breaks} min.',f'{walk}+{breaks}={total} min.',f'Après détour : {total}+{detour}×{pace}={last}. Écart (durée − limite)={last}−{limit}={last-limit} min.'
        ],dict(kind='n8_rando',km=km,pace=pace,laps=laps,pause=pause,detour=detour,limit=limit))
    elif idx==19:
        faucets=rng.randint(4,10);liters=rng.randint(3,7);days=rng.choice([5,6,7])
        goal=(faucets+rng.randint(2,5))*liters*days-rng.randint(1,liters*days-1)
        savings=faucets*liters*days; deficit=goal-savings
        price_a=rng.randint(8,16);liters_b=liters+rng.randint(2,5);price_b=rng.randint(13,25)
        count_a=_mc_new_ceil(deficit,liters*days);count_b=_mc_new_ceil(deficit,liters_b*days)
        a=count_a*price_a;b=count_b*price_b
        return _mc_new_problem(8,idx,seed,'La campagne d’économie d’eau',[
            f'Le collège a installé {faucets} économiseurs A sur des robinets. Chaque économiseur A fait gagner {liters} litres par jour. On mesure l’économie pendant {days} jours.',
            f'L’objectif est d’économiser au moins {goal} litres. Pour équiper d’autres robinets, le collège peut choisir le modèle A à {price_a} € l’unité, ou un nouveau modèle B économisant {liters_b} litres par jour, à {price_b} € l’unité. Pour les nouveaux équipements, on choisit un seul modèle.'
        ],['Combien de litres un économiseur A fait-il économiser pendant toute la période ?','Combien de litres les économiseurs déjà installés font-ils économiser ensemble ?','Combien de litres manque-t-il pour atteindre l’objectif ?','Combien d’économiseurs A supplémentaires faudrait-il au minimum ?','Quel est le coût minimal des nouveaux économiseurs, en choisissant soit seulement A, soit seulement B ?'],
        [liters*days,savings,deficit,count_a,min(a,b)],['Économie d’un A','Économie totale','Économie manquante','Nombre de A supplémentaires','Coût minimal de l’équipement'],['L','L','L','économiseurs','€'],['Q','Q','R','L','C'],[
            f'{liters}×{days}={liters*days} L.',f'{faucets}×{liters*days}={savings} L.',f'{goal}−{savings}={deficit} L.',f'⌈{deficit}/{liters*days}⌉={count_a} économiseurs A.',f'Offre A : {count_a}×{price_a}={a} € ; offre B : ⌈{deficit}/({liters_b}×{days})⌉×{price_b}={count_b}×{price_b}={b} €. Choisir le coût minimal : {min(a,b)} €.'
        ],dict(kind='n8_eau',faucets=faucets,liters=liters,days=days,goal=goal,price_a=price_a,liters_b=liters_b,price_b=price_b))
    elif idx==20:
        classes=rng.randint(3,6);per=rng.randint(21,28);teachers=rng.randint(4,8); ticket=rng.randint(5,10); cap=rng.choice([36,40,48]);buscost=rng.randint(100,170);groupbuscost=rng.randint(280,500)
        n=classes*per+teachers;entry=n*ticket;nb=_mc_new_ceil(n,cap);regular=nb*buscost;plus=groupbuscost if groupbuscost<2*regular else groupbuscost
        return _mc_new_problem(8,idx,seed,'La sortie au planétarium',[
            f'{classes} classes de {per} élèves et {teachers} accompagnateurs visitent un planétarium. Chaque billet coûte {ticket} €.',
            f'Le transporteur A propose des cars de {cap} places pour {buscost} € chacun. Le transporteur B propose un car de grande capacité pour tout le groupe, à un tarif fixe de {groupbuscost} €.'
        ],['Combien de personnes participent à la sortie ?','Quel est le prix total des entrées ?','Combien de cars A faut-il louer ?','Quel est le budget total avec le transporteur A, billets compris ?','Quel est le budget total minimal en comparant A et B, billets compris ?'],
        [n,entry,nb,entry+regular,entry+min(regular,groupbuscost)],['Participants','Coût des entrées','Cars A','Budget avec A','Budget minimal'],['personnes','€','cars','€','€'],['Q','B','L','B','C'],[
            f'{classes}×{per}+{teachers}={n}.',f'{n}×{ticket}={entry} €.',f'⌈{n}/{cap}⌉={nb} cars.',f'{entry}+{nb}×{buscost}={entry+regular} €.',f'A : {entry+regular} € ; B : {entry+groupbuscost} €. Minimum {entry+min(regular,groupbuscost)} €.'
        ],dict(kind='n8_planet',classes=classes,per=per,teachers=teachers,ticket=ticket,cap=cap,buscost=buscost,groupbuscost=groupbuscost))
    elif idx==21:
        start=rng.randint(60,130);win=rng.randint(3,7);reward=rng.randint(10,20)
        loss=rng.randint(25,55);spent=rng.randint(20,45);goal=rng.randint(240,350)
        normal=rng.randint(18,27);rare=rng.randint(normal+7,normal+24)
        gains=win*reward;remaining=start+gains-loss-spent;miss=max(0,goal-remaining)
        only_normal=_mc_new_ceil(miss,normal)
        with_rare=1+_mc_new_ceil(max(0,miss-rare),normal)
        return _mc_new_problem(8,idx,seed,'La quête des cristaux du jeu vidéo',[
            f'Dans un jeu, Emma possède {start} cristaux. Elle en gagne {reward} pour chacune de {win} missions, en perd {loss} dans un piège puis dépense {spent} cristaux pour un équipement.',
            f'Elle souhaite posséder {goal} cristaux. Une mission ordinaire rapporte {normal} cristaux. Elle peut aussi réussir au plus une mission rare rapportant {rare} cristaux. Les deux types de missions comptent chacun pour une mission.'
        ],['Combien de cristaux Emma gagne-t-elle dans les premières missions ?','Combien conserve-t-elle après le piège ?','Combien lui reste-t-il après l’achat ?','Combien de cristaux manque-t-il pour atteindre l’objectif ?','Quel est le nombre minimal de missions supplémentaires en choisissant entre les missions ordinaires et l’unique mission rare possible ?'],
        [gains,start+gains-loss,remaining,miss,min(only_normal,with_rare)],['Cristaux gagnés','Cristaux après piège','Cristaux restants','Cristaux manquants','Missions minimales'],['cristaux','cristaux','cristaux','cristaux','missions'],['Q','R','R','R','C'],[
            f'{win}×{reward}={gains}.',f'{start}+{gains}−{loss}={start+gains-loss}.',f'{start+gains-loss}−{spent}={remaining}.',f'{goal}−{remaining}={miss}.',f'Sans rare : ⌈{miss}/{normal}⌉={only_normal} ordinaires. Avec une rare : 1+⌈max(0,{miss}−{rare})/{normal}⌉={with_rare} missions. Minimum : {min(only_normal,with_rare)} missions.'
        ],dict(kind='n8_jeu',start=start,win=win,reward=reward,loss=loss,spent=spent,goal=goal,normal=normal,rare=rare))
    elif idx==22:
        scale=rng.choice([10000,20000,25000]); a=rng.randint(12,30);b=rng.randint(13,31);detour=rng.randint(3,12)
        km_a=a*scale/100000;km_b=b*scale/100000;new_a=(a+detour)*scale/100000
        # distances en km arrondies exact au centième grâce aux échelles retenues
        return _mc_new_problem(8,idx,seed,'La carte du rallye d’orientation',[
            f'Une carte est à l’échelle 1:{scale}. Le sentier A mesure {a} cm sur la carte et le sentier B {b} cm.',
            f'Une déviation augmente le sentier A de {detour} cm sur cette même carte. On conserve les mêmes unités de conversion.'
        ],['Quelle est la longueur réelle du sentier A, en kilomètres ?','Quelle est la longueur réelle du sentier B, en kilomètres ?','Quelle sera la longueur réelle du sentier A après déviation ?','Quel sentier est le plus court après la déviation : A ou B (C s’ils sont égaux) ?','Quelle distance réelle sépare les deux sentiers après la déviation ?'],
        [km_a,km_b,new_a,_mc_new_choose_a_b(new_a,km_b),abs(new_a-km_b)],['Distance A','Distance B','Distance A modifiée','Sentier le plus court','Écart de distance'],['km','km','km','','km'],['D','D','D','C','D'],[
            f'{a}×{scale} cm = {km_a} km.',f'{b}×{scale} cm = {km_b} km.',f'({a}+{detour})×{scale} cm = {new_a} km.',f'Comparer {new_a} et {km_b} : réponse {_mc_new_choose_a_b(new_a,km_b)}.',f'|{new_a}−{km_b}|={abs(new_a-km_b)} km.'
        ],dict(kind='n8_orientation',scale=scale,a=a,b=b,detour=detour))
    elif idx==23:
        surface=rng.randint(35,80);qty=rng.randint(2,5);stock=rng.randint(20,60); bag_a=rng.choice([10,15]);price_a=rng.randint(8,14);bag_b=rng.choice([16,20]);price_b=rng.randint(14,23)
        need=surface*qty;missing=max(0,need-stock);a=_mc_new_ceil(missing,bag_a)*price_a;b=_mc_new_ceil(missing,bag_b)*price_b
        return _mc_new_problem(8,idx,seed,'Le compost du potager',[
            f'Le potager comporte {surface} m², avec un besoin de {qty} kg de compost par m².',
            f'Le collège possède {stock} kg. L’offre A vend des sacs de {bag_a} kg à {price_a} € ; l’offre B des sacs de {bag_b} kg à {price_b} €. On choisit un seul type de sac.'
        ],['Quelle masse de compost faut-il pour tout le potager ?','Quelle masse manque-t-il après utilisation du stock ?','Combien de sacs A faut-il au minimum ?','Combien coûteraient les sacs A nécessaires ?','Quel est le coût le plus faible entre les deux offres pour compléter le besoin ?'],
        [need,missing,_mc_new_ceil(missing,bag_a),a,min(a,b)],['Besoin de compost','Compost manquant','Sacs A','Coût A','Coût minimal'],['kg','kg','sacs','€','€'],['Q','R','L','B','C'],[
            f'{surface}×{qty}={need} kg.',f'{need}−{stock}={missing} kg.',f'⌈{missing}/{bag_a}⌉={_mc_new_ceil(missing,bag_a)} sacs.',f'{_mc_new_ceil(missing,bag_a)}×{price_a}={a} €.',f'B : ⌈{missing}/{bag_b}⌉×{price_b}={b} €. Minimum entre {a} et {b} : {min(a,b)} €.'
        ],dict(kind='n8_compost',surface=surface,qty=qty,stock=stock,bag_a=bag_a,price_a=price_a,bag_b=bag_b,price_b=price_b))
    elif idx==24:
        teams=rng.randint(5,9);matchtime=rng.choice([12,15,18]);courts=rng.choice([2,3,4]); breaktime=rng.choice([3,5]);duration=rng.randint(155,300)
        matches=teams*(teams-1)//2;slots=_mc_new_ceil(matches,courts);total=slots*matchtime+(slots-1)*breaktime
        return _mc_new_problem(8,idx,seed,'Le tournoi sur plusieurs terrains',[
            f'{teams} équipes doivent se rencontrer chacune une seule fois. Une rencontre dure {matchtime} minutes.',
            f'Le gymnase dispose de {courts} terrains ; il peut accueillir autant de matchs simultanés que de terrains. Entre deux séries de matchs, il y a {breaktime} minutes de pause, jamais après la dernière série.',
            f'La journée sportive réserve {duration} minutes à ce tournoi.'
        ],['Combien de rencontres faut-il organiser au total, sans compter deux fois les mêmes équipes ?','Combien de matchs peuvent se dérouler simultanément ?','Combien de séries de matchs faut-il au minimum ?','Quelle est la durée minimale du tournoi, pauses comprises ?','Quel est l’écart signé entre la durée réservée et la durée du tournoi (positif s’il reste du temps, négatif sinon) ?'],
        [matches,courts,slots,total,duration-total],['Nombre de rencontres','Matchs simultanés','Séries de matchs','Durée du tournoi','Écart de temps'],['matchs','matchs','séries','min','min'],['Q','L','L','D','R'],[
            f'{teams}×({teams}−1)÷2={matches} rencontres.',f'{courts} terrains donnent {courts} matchs simultanés.',f'⌈{matches}/{courts}⌉={slots} séries.',f'{slots}×{matchtime}+({slots}−1)×{breaktime}={total} min.',f'{duration}−{total}={duration-total} min.'
        ],dict(kind='n8_tournoi',teams=teams,matchtime=matchtime,courts=courts,breaktime=breaktime,duration=duration))
    elif idx==25:
        boxes=rng.randint(12,25);per=rng.randint(8,14); spoiled=rng.randint(7,25);target=rng.randint(220,360);pack_a=rng.choice([10,12]);cost_a=rng.randint(9,15);pack_b=rng.choice([15,18]);cost_b=rng.randint(16,25)
        stock=boxes*per-spoiled;target=max(target,stock+rng.randint(15,65));missing=target-stock;a=_mc_new_ceil(missing,pack_a)*cost_a;b=_mc_new_ceil(missing,pack_b)*cost_b
        return _mc_new_problem(8,idx,seed,'La collecte pour la cantine solidaire',[
            f'Une association reçoit {boxes} cartons de {per} portions alimentaires chacun. {spoiled} portions sont inutilisables.',
            f'Elle veut disposer de {target} portions. Un supplément peut être acheté en lots A de {pack_a} portions à {cost_a} €, ou en lots B de {pack_b} portions à {cost_b} €. Elle ne mélange pas les lots des deux offres.'
        ],['Combien de portions ont été reçues initialement ?','Combien de portions utilisables restent après le tri ?','Combien de portions manque-t-il pour atteindre l’objectif ?','Quel serait le coût total en choisissant seulement des lots A ?','Quel est le coût minimal entre les deux offres pour compléter le stock ?'],
        [boxes*per,stock,missing,a,min(a,b)],['Portions reçues','Portions utilisables','Portions manquantes','Coût A','Coût minimal'],['portions','portions','portions','€','€'],['Q','Q','R','B','C'],[
            f'{boxes}×{per}={boxes*per}.',f'{boxes*per}−{spoiled}={stock}.',f'{target}−{stock}={missing}.',f'⌈{missing}/{pack_a}⌉×{cost_a}={a} €.',f'B : ⌈{missing}/{pack_b}⌉×{cost_b}={b} €. Minimum : {min(a,b)} €.'
        ],dict(kind='n8_collecte',boxes=boxes,per=per,spoiled=spoiled,target=target,pack_a=pack_a,cost_a=cost_a,pack_b=pack_b,cost_b=cost_b))
    raise ValueError(f'Modèle N8 inconnu: {model_id}')

def _mc_new_mix_instance(rng, need_min=35, need_max=95, lo=5, hi=18, fee=0, max_b=None):
    """Retient un tirage où mélanger les offres améliore strictement les choix purs."""
    for _ in range(2000):
        a_size=rng.randint(lo,hi-3);b_size=rng.randint(a_size+2,hi+5)
        # On génère des prix unitaires comparables, sans gagnant évident.
        pa=rng.randint(a_size+2,2*a_size+6)
        pb=rng.randint(b_size+2,2*b_size+8)
        need=rng.randint(need_min,need_max)
        try:sol=_mc_new_combo(need,a_size,pa,b_size,pb,max_b=max_b,fee_b=fee)
        except ValueError:continue
        purea=_mc_new_ceil(need,a_size)*pa
        pureb=(_mc_new_ceil(need,b_size)*pb+fee) if max_b is None or _mc_new_ceil(need,b_size)<=max_b else 10**6
        if sol[2]>=1 and sol[3]>=1 and min(purea,pureb)-sol[0]>=2 and sol[2]+sol[3]<=13:
            return need,a_size,pa,b_size,pb,sol,purea,pureb
    raise AssertionError('Pas de variante mixte suffisamment intéressante')


def _mc_new_2d_instance(rng):
    """Deux ressources complémentaires, vrai calcul de combinaison."""
    for _ in range(2000):
        needx=rng.randint(19,43);needy=rng.randint(20,43)
        ax=rng.randint(5,10);ay=rng.randint(1,3)
        bx=rng.randint(1,3);by=rng.randint(5,10)
        pa=rng.randint(9,18);pb=rng.randint(9,18)
        sol=_mc_new_2d_combo(needx,needy,ax,ay,pa,bx,by,pb,max_a=15,max_b=15)
        cost_a_only=max(_mc_new_ceil(needx,ax),_mc_new_ceil(needy,ay))*pa
        cost_b_only=max(_mc_new_ceil(needx,bx),_mc_new_ceil(needy,by))*pb
        if sol[2]>=1 and sol[3]>=1 and min(cost_a_only,cost_b_only)-sol[0]>=5 and sol[2]+sol[3]<=13:
            return needx,needy,ax,ay,pa,bx,by,pb,sol,cost_a_only,cost_b_only
    raise AssertionError('Tirage deux ressources instable')


def _mc_new_n9(idx,seed=None):
    rng,seed=_p9_rng(seed)
    if idx==11:
        # Besoin construit à partir de mouvements ; combinaison de colis optimale.
        start=rng.randint(65,130); loan=rng.randint(38,77);received=rng.randint(15,37)
        net=start+received-loan
        need,a_size,pa,b_size,pb,sol,purea,pureb=_mc_new_mix_instance(rng,need_min=35,need_max=85)
        target=net+need
        return _mc_new_problem(9,idx,seed,'La réserve de bandes dessinées',[
            f'La bibliothèque possède {start} BD, en reçoit {received} et en prête {loan}. Elle souhaite posséder au moins {target} BD pour un événement.',
            f'Le fournisseur A vend des colis de {a_size} BD pour {pa} € ; B vend des colis de {b_size} BD pour {pb} €. Les deux formats peuvent être mélangés et chaque colis est indivisible.'
        ],['Quel stock reste-t-il après les prêts et les réceptions ?','Combien de BD faut-il acquérir au minimum pour atteindre l’objectif ?','Quel serait le coût si tous les colis achetés étaient du format A ?','Quel serait le coût si tous les colis achetés étaient du format B ?','Quel est le coût minimal en autorisant un mélange des colis A et B ?'],
        [net,need,purea,pureb,sol[0]],['Stock disponible','BD à acquérir','Coût A seul','Coût B seul','Coût optimal'],['BD','BD','€','€','€'],['Q','R','B','B','C'],[
            f'{start}+{received}−{loan}={net} BD.',f'{target}−{net}={need} BD.',f'⌈{need}/{a_size}⌉×{pa}={purea} €.',f'⌈{need}/{b_size}⌉×{pb}={pureb} €.',f'Rechercher les couples (A,B) couvrant au moins {need} BD. Le meilleur est {sol[2]} colis A et {sol[3]} colis B, pour {sol[2]}×{pa}+{sol[3]}×{pb}={sol[0]} € ; {sol[4]} BD en surplus.'
        ],dict(kind='n9_bd',start=start,loan=loan,received=received,target=target,a_size=a_size,pa=pa,b_size=b_size,pb=pb))
    elif idx==12:
        # Plusieurs recettes possibles, quota de billets adultes et contrainte de places.
        for _ in range(1000):
            rows=rng.randint(9,13);per=rng.randint(14,18); reserved=rng.randint(5,15)
            sold_students=rng.randint(35,68);sold_adults=rng.randint(15,32)
            usable=rows*per-reserved
            if usable-sold_students-sold_adults<12:continue
            price_s=rng.randint(4,7);price_a=rng.randint(8,12);program=rng.choice([1,2]);fixed=rng.randint(180,280)
            profit=sold_students*(price_s-program)+sold_adults*(price_a-program)-fixed
            extra_cap=rng.randint(3,7);remaining_seats=usable-sold_students-sold_adults
            extra_needed=rng.randint(33,75)
            # Q5: min billets pour gain au moins cible avec au plus extra_cap adultes; place physically possible.
            combos=[(s+a,-a,s,a) for a in range(extra_cap+1) for s in range(remaining_seats-a+1) if s*(price_s-program)+a*(price_a-program)>=extra_needed]
            if combos and 2<=min(combos)[2]+min(combos)[3]<=remaining_seats and min(combos)[2]>0 and min(combos)[3]>0:break
        else:raise AssertionError('spectacle combinaison manquante')
        best=min(combos);target=profit+extra_needed
        return _mc_new_problem(9,idx,seed,'Le spectacle solidaire et les dernières places',[
            f'Une salle a {rows} rangées de {per} places, dont {reserved} réservées et invendables. Le collège a déjà vendu {sold_students} billets élèves à {price_s} € et {sold_adults} billets adultes à {price_a} €.',
            f'Chaque spectateur reçoit un programme qui coûte {program} €. Les frais fixes du spectacle sont de {fixed} €. Le collège veut porter son bénéfice total à au moins {target} €.',
            f'Il ne peut encore vendre que {extra_cap} billets adultes au maximum. Les autres billets supplémentaires seraient des billets élèves, dans la limite des places disponibles.'
        ],['Combien de places peuvent être vendues au total ?','Quel est le bénéfice avec les billets déjà vendus, programmes et frais compris ?','Combien de places vendables restent libres ?','Combien d’euros de bénéfice supplémentaire faut-il obtenir pour atteindre l’objectif ?','Quel est le nombre minimal de billets supplémentaires à vendre en respectant la limite de billets adultes ?'],
        [usable,profit,remaining_seats,extra_needed,best[0]],['Places vendables','Bénéfice actuel','Places restantes','Bénéfice manquant','Billets supplémentaires'],['places','€','places','€','billets'],['L','B','R','R','L'],[
            f'{rows}×{per}−{reserved}={usable} places.',f'{sold_students}×({price_s}−{program})+{sold_adults}×({price_a}−{program})−{fixed}={profit} €.',f'{usable}−({sold_students}+{sold_adults})={remaining_seats} places.',f'{target}−{profit}={extra_needed} €.',f'Le billet élève rapporte {price_s-program} € nets, le billet adulte {price_a-program} €. Tester 0 à {extra_cap} billets adultes et compléter avec des billets élèves, en respectant les {remaining_seats} places. Minimum : {best[0]} billets ({best[2]} élèves, {best[3]} adultes).'
        ],dict(kind='n9_spectacle',rows=rows,per=per,reserved=reserved,sold_students=sold_students,sold_adults=sold_adults,price_s=price_s,price_a=price_a,program=program,fixed=fixed,target=target,extra_cap=extra_cap))
    elif idx==13:
        target=rng.randint(10,17);motors=rng.randint(8,18);batteries=rng.randint(14,32)
        target=max(target,motors//2+1,batteries//3+1)
        need_m=2*target-motors;need_b=3*target-batteries
        ms1=rng.choice([4,5,6]);ms2=ms1+rng.choice([2,3]);mp1=rng.randint(10,19);mp2=rng.randint(14,27)
        bs1=rng.choice([5,6,7]);bs2=bs1+rng.choice([2,3]);bp1=rng.randint(12,21);bp2=rng.randint(16,28)
        option_m=[(_mc_new_ceil(need_m,ms1)*mp1,'M1'),(_mc_new_ceil(need_m,ms2)*mp2,'M2')]
        option_b=[(_mc_new_ceil(need_b,bs1)*bp1,'B1'),(_mc_new_ceil(need_b,bs2)*bp2,'B2')]
        best_m=min(option_m);best_b=min(option_b);cost=best_m[0]+best_b[0]
        capacity=min(motors//2,batteries//3)
        return _mc_new_problem(9,idx,seed,'Les fournisseurs du laboratoire robotique',[
            f'Le laboratoire possède {motors} moteurs et {batteries} batteries. Chaque robot complet nécessite 2 moteurs et 3 batteries. Son objectif est de fabriquer {target} robots.',
            f'Pour les moteurs : lot M1 de {ms1} moteurs à {mp1} €, ou lot M2 de {ms2} moteurs à {mp2} €.',
            f'Pour les batteries : lot B1 de {bs1} batteries à {bp1} €, ou lot B2 de {bs2} batteries à {bp2} €.',
            'Chaque lot est indivisible. Pour un même composant, on choisit un seul format de lot, mais le format des moteurs peut être différent de celui des batteries.'
        ],['Combien de robots les moteurs actuels permettent-ils de fabriquer ?','Combien de robots les batteries actuelles permettent-elles de fabriquer ?','Combien de robots complets peut-on fabriquer aujourd’hui ?','Combien de batteries supplémentaires faut-il pour atteindre l’objectif ?','Quel est le coût total minimal des lots de moteurs et de batteries nécessaires en comparant les quatre formats disponibles ?'],
        [motors//2,batteries//3,capacity,need_b,cost],['Robots selon moteurs','Robots selon batteries','Robots complets','Batteries manquantes','Achats au coût minimal'],['robots','robots','robots','batteries','€'],['L','L','L','R','C'],[
            f'{motors} ÷ 2 = {motors//2} robots.',f'{batteries} ÷ 3 = {batteries//3} robots.',f'Le minimum est {capacity} robots.',f'{target}×3−{batteries}={need_b} batteries.',f'Moteurs manquants : {need_m}. M1 coûte {option_m[0][0]} €, M2 {option_m[1][0]} €. Batteries : B1 coûte {option_b[0][0]} €, B2 {option_b[1][0]} €. Retenir {best_m[1]} et {best_b[1]}, soit {cost} €.'
        ],dict(kind='n9_robotique',target=target,motors=motors,batteries=batteries,ms1=ms1,ms2=ms2,mp1=mp1,mp2=mp2,bs1=bs1,bs2=bs2,bp1=bp1,bp2=bp2))
    elif idx==14:
        for _ in range(200):
            teams=rng.randint(7,11);duration=rng.choice([10,12,15]);rest=rng.choice([3,4,5]);courts=rng.choice([2,3]);single=rng.randint(45,85)
            double=rng.randint(single+9,2*single-5)
            matches=teams*(teams-1)//2
            def duree(extra):
                slots=_mc_new_ceil(matches,courts+extra)
                return slots*duration+(slots-1)*rest
            initialdur=duree(0);min_dur=duree(3)
            if min_dur<initialdur-8:break
        limit=rng.randint(min_dur,initialdur-1)
        feasible=[]
        for pack2 in range(2):
            for singles in range(4):
                extra=2*pack2+singles
                if extra<=3 and duree(extra)<=limit:
                    feasible.append((pack2*double+singles*single,extra,singles,pack2,duree(extra)))
        assert feasible
        best=min(feasible)
        return _mc_new_problem(9,idx,seed,'Le championnat et les terrains à louer',[
            f'{teams} équipes jouent chacune contre toutes les autres une fois. Chaque match dure {duration} minutes. Entre deux séries de matchs, il faut {rest} minutes de pause, sauf après la dernière.',
            f'Le gymnase dispose de {courts} terrains. Le championnat doit finir en {limit} minutes au maximum.',
            f'Pour tout le tournoi, on peut louer un terrain supplémentaire pour {single} €, ou un ensemble de deux terrains pour {double} €. On peut combiner au maximum trois terrains supplémentaires ; au plus un ensemble de deux est proposé.'
        ],['Combien de matchs distincts faut-il organiser ?','Combien de séries faut-il avec les terrains actuels ?','Quelle serait la durée totale avec les terrains actuels, pauses comprises ?','Combien de minutes faudrait-il gagner sur cette durée initiale pour respecter la limite ?','Quel est le coût minimal de location de terrains supplémentaires, en comparant les terrains seuls et l’ensemble de deux ?'],
        [matches,_mc_new_ceil(matches,courts),initialdur,initialdur-limit,best[0]],['Nombre de matchs','Séries initiales','Durée initiale','Minutes à gagner','Coût minimal de location'],['matchs','séries','min','min','€'],['Q','L','D','R','C'],[
            f'{teams}×({teams}−1)÷2={matches} matchs.',f'⌈{matches}/{courts}⌉={_mc_new_ceil(matches,courts)} séries.',f'{_mc_new_ceil(matches,courts)}×{duration}+({_mc_new_ceil(matches,courts)}−1)×{rest}={initialdur} min.',f'{initialdur}−{limit}={initialdur-limit} min.',f'Tester 1 à 3 terrains supplémentaires, par terrain seul à {single} € ou par ensemble de 2 à {double} €. Le moins cher : {best[2]} terrain(s) seul(s) et {best[3]} ensemble(s) de 2, soit {best[1]} terrains ajoutés pour {best[0]} € ; durée {best[4]} min.'
        ],dict(kind='n9_terrains',teams=teams,duration=duration,rest=rest,courts=courts,limit=limit,single=single,double=double))
    elif idx==15:
        # Deux contraintes actives : missions rares limitées et énergie disponible.
        for _ in range(3000):
            regular=rng.randint(15,22);rare=rng.randint(33,47)
            energy_regular=2;energy_rare=rng.choice([4,5]);maxrare=rng.randint(2,3)
            energy_cap=rng.randint(16,28);needed=rng.randint(100,190)
            unconstrained=[(r+s,r,s) for r in range(maxrare+1) for s in range(16) if r*rare+s*regular>=needed]
            feasible=[(r+s,r,s) for r in range(maxrare+1) for s in range(16) if r*rare+s*regular>=needed and r*energy_rare+s*energy_regular<=energy_cap]
            if not feasible:continue
            best=min(feasible)
            if best[1]>0 and best[2]>0 and best[0]>min(unconstrained)[0] and best[0]<=13:break
        else:raise AssertionError('Mission stratégique sans contrainte énergétique active')
        gold=rng.randint(45,80);spent=rng.randint(17,34);target=gold-spent+needed
        return _mc_new_problem(9,idx,seed,'Les missions et la réserve d’énergie du jeu vidéo',[
            f'Le joueur possède {gold} cristaux et en dépense {spent}. Il veut disposer d’au moins {target} cristaux.',
            f'Une mission ordinaire rapporte {regular} cristaux et consomme {energy_regular} points d’énergie. Une mission rare rapporte {rare} cristaux et consomme {energy_rare} points d’énergie.',
            f'Il ne reste qu’au plus {maxrare} missions rares possibles. Le joueur possède {energy_cap} points d’énergie pour toutes les missions supplémentaires, sans possibilité de recharge.'
        ],['Combien de cristaux garde-t-il après son achat ?','Combien de cristaux doit-il encore gagner au minimum ?','Combien de missions ordinaires faudrait-il si l’énergie et les missions rares n’étaient pas limitées ?','Combien de points d’énergie consommeraient toutes les missions rares encore possibles ?','Quel est le nombre minimal de missions pour atteindre la cible en respectant à la fois l’énergie disponible et la limite des missions rares ?'],
        [gold-spent,needed,_mc_new_ceil(needed,regular),maxrare*energy_rare,best[0]],['Cristaux restants','Cristaux à gagner','Missions ordinaires sans limite','Énergie pour les rares','Minimum de missions faisables'],['cristaux','cristaux','missions','points','missions'],['R','R','L','Q','C'],[
            f'{gold}−{spent}={gold-spent} cristaux.',f'{target}−{gold-spent}={needed} cristaux.',f'⌈{needed}/{regular}⌉={_mc_new_ceil(needed,regular)} missions (sans limite d’énergie).',f'{maxrare}×{energy_rare}={maxrare*energy_rare} points.',f'Explorer 0 à {maxrare} rares et compléter par des ordinaires, en vérifiant les cristaux gagnés et l’énergie consommée. Le meilleur plan est {best[1]} rare(s) et {best[2]} ordinaire(s), soit {best[0]} missions, utilisant {best[1]*energy_rare+best[2]*energy_regular} points sur {energy_cap}.'
        ],dict(kind='n9_missions',gold=gold,spent=spent,target=target,regular=regular,rare=rare,maxrare=maxrare,energy_rare=energy_rare,energy_regular=energy_regular,energy_cap=energy_cap))
    elif idx==16:
        rows=rng.randint(10,15);cols=rng.randint(10,16);reserve=rng.randint(10,25);need=rows*cols+reserve
        # Optimisation sur les formats de boîtes adaptés au grand besoin.
        for _ in range(1000):
            a_size=rng.randint(9,15);b_size=rng.randint(16,25)
            pa=rng.randint(8,14);pb=rng.randint(14,23)
            sol=_mc_new_combo(need,a_size,pa,b_size,pb)
            purea=_mc_new_ceil(need,a_size)*pa;pureb=_mc_new_ceil(need,b_size)*pb
            if sol[2]>=1 and sol[3]>=1 and min(purea,pureb)>sol[0] and sol[2]+sol[3]<=20:break
        else:raise AssertionError('mosaïque sans combinaison utile')
        return _mc_new_problem(9,idx,seed,'La grande mosaïque du collège',[
            f'Une mosaïque comporte {rows} lignes de {cols} carreaux. Le club veut prévoir {reserve} carreaux supplémentaires pour les pertes.',
            f'La boîte A contient {a_size} carreaux et coûte {pa} €. La boîte B en contient {b_size} et coûte {pb} €. Il est possible de mélanger les deux offres.'
        ],['Combien de carreaux sont nécessaires pour la mosaïque seule ?','Quel est le besoin total, réserve comprise ?','Quel serait le coût si seuls des lots A étaient achetés ?','Quel serait le coût si seuls des lots B étaient achetés ?','Quel est le coût minimal en combinant librement les boîtes A et B ?'],
        [rows*cols,need,purea,pureb,sol[0]],['Carreaux de mosaïque','Carreaux nécessaires','Coût lots A','Coût lots B','Coût optimal'],['carreaux','carreaux','€','€','€'],['Q','Q','B','B','C'],[
            f'{rows}×{cols}={rows*cols}.',f'{rows*cols}+{reserve}={need}.',f'⌈{need}/{a_size}⌉×{pa}={purea} €.',f'⌈{need}/{b_size}⌉×{pb}={pureb} €.',f'Mélange optimal : {sol[2]} boîte(s) A et {sol[3]} boîte(s) B, soit {sol[0]} € au total ; le surplus est de {sol[4]} carreaux.'
        ],dict(kind='n9_mosaique',rows=rows,cols=cols,reserve=reserve,a_size=a_size,pa=pa,b_size=b_size,pb=pb))
    elif idx==17:
        for _ in range(1000):
            n=rng.randint(60,145);cap_a=rng.randint(16,26);cap_b=rng.randint(29,44);pa=rng.randint(90,140);pb=rng.randint(165,235)
            sol=_mc_new_combo(n,cap_a,pa,cap_b,pb,max_b=3)
            purea=_mc_new_ceil(n,cap_a)*pa
            pureb=_mc_new_ceil(n,cap_b)*pb if _mc_new_ceil(n,cap_b)<=3 else 10**6
            if sol[2]>=1 and sol[3]>=1 and min(purea,pureb)>sol[0] and sol[3]<=3:break
        else:raise AssertionError('navettes sans coût mixte utile')
        return _mc_new_problem(9,idx,seed,'Le transport du festival scolaire',[
            f'{n} participants doivent rejoindre un festival. Une navette A propose {cap_a} places pour {pa} € ; une navette B propose {cap_b} places pour {pb} €.',
            'Le collège peut louer autant de navettes A que nécessaire, mais le transporteur ne dispose que de trois navettes B. Les deux formats peuvent être combinés.'
        ],['Combien de navettes A sont nécessaires si on utilise seulement A ?','Quel serait le coût de la solution utilisant seulement A ?','Quelle est la capacité totale des trois navettes B ?','Combien de participants devraient être transportés par A si les trois B étaient louées ?','Quel est le coût minimal en combinant les deux types de navettes sous la limite de trois B ?'],
        [_mc_new_ceil(n,cap_a),purea,3*cap_b,max(0,n-3*cap_b),sol[0]],['Navettes A seules','Prix A seul','Capacité des B','Participants non couverts','Coût minimal'],['navettes','€','personnes','personnes','€'],['L','B','L','R','C'],[
            f'⌈{n}/{cap_a}⌉={_mc_new_ceil(n,cap_a)} navettes A.',f'{_mc_new_ceil(n,cap_a)}×{pa}={purea} €.',f'3×{cap_b}={3*cap_b} places.',f'Maximum(0,{n}−{3*cap_b})={max(0,n-3*cap_b)} personnes.',f'Tester 0, 1, 2 ou 3 navettes B, et compléter avec A en arrondissant au supérieur. Minimum : {sol[2]} A et {sol[3]} B, coût {sol[0]} €.'
        ],dict(kind='n9_navettes',n=n,cap_a=cap_a,cap_b=cap_b,pa=pa,pb=pb))
    elif idx==18:
        fee=rng.randint(15,25)
        need,a_size,pa,b_size,pb,sol,purea,pureb=_mc_new_mix_instance(rng,need_min=42,need_max=85,fee=fee)
        return _mc_new_problem(9,idx,seed,'Les accessoires du concours cosplay',[
            f'Un concours a besoin d’au moins {need} accessoires identiques. Le fournisseur A vend des paquets de {a_size} accessoires pour {pa} €.',
            f'Le fournisseur B vend des paquets de {b_size} accessoires pour {pb} €. Dès qu’au moins un paquet B est commandé, il facture en plus {fee} € de livraison, une seule fois. Les paquets des deux fournisseurs peuvent être mélangés.'
        ],['Combien de paquets A faudrait-il si l’on choisissait seulement A ?','Combien coûterait l’achat auprès de A uniquement ?','Combien de paquets B faudrait-il si l’on choisissait seulement B ?','Quel serait le coût total avec B seul, livraison comprise ?','Quel est le coût minimal en combinant les paquets A et B, livraison éventuelle comprise ?'],
        [_mc_new_ceil(need,a_size),purea,_mc_new_ceil(need,b_size),pureb,sol[0]],['Paquets A seuls','Prix A seul','Paquets B seuls','Prix B livré','Coût minimal'],['paquets','€','paquets','€','€'],['L','B','L','B','C'],[
            f'⌈{need}/{a_size}⌉={_mc_new_ceil(need,a_size)}.',f'{_mc_new_ceil(need,a_size)}×{pa}={purea} €.',f'⌈{need}/{b_size}⌉={_mc_new_ceil(need,b_size)}.',f'{_mc_new_ceil(need,b_size)}×{pb}+{fee}={pureb} €.',f'Comparer les combinaisons de paquets en comptant {fee} € une seule fois si B est utilisé : optimum {sol[2]} A + {sol[3]} B, coût {sol[0]} €.'
        ],dict(kind='n9_cosplay',need=need,a_size=a_size,pa=pa,b_size=b_size,pb=pb,fee=fee))
    elif idx==19:
        needx,needy,ax,ay,pa,bx,by,pb,sol,ca,cb=_mc_new_2d_instance(rng)
        return _mc_new_problem(9,idx,seed,'L’engrais du jardin pédagogique',[
            f'Le jardin a besoin d’au moins {needx} doses d’azote (N) et {needy} doses de potassium (K).',
            f'Le kit A fournit {ax} doses N et {ay} doses K pour {pa} €. Le kit B fournit {bx} doses N et {by} doses K pour {pb} €. Les kits sont indivisibles ; les deux composants doivent être suffisants.'
        ],['Quel est le nombre minimal de kits A pour satisfaire le besoin en azote, en ignorant le potassium ?','Quel est le nombre minimal de kits A pour satisfaire le besoin en potassium, en ignorant l’azote ?','Quel serait le coût total en choisissant seulement des kits A suffisants pour les deux besoins ?','Quel serait le coût total en choisissant seulement des kits B suffisants pour les deux besoins ?','Quel est le coût minimal d’un mélange de kits A et B couvrant simultanément les deux besoins ?'],
        [_mc_new_ceil(needx,ax),_mc_new_ceil(needy,ay),ca,cb,sol[0]],['A pour azote','A pour potassium','Coût A seul','Coût B seul','Coût optimal'],['kits','kits','€','€','€'],['L','L','B','B','C'],[
            f'⌈{needx}/{ax}⌉={_mc_new_ceil(needx,ax)}.',f'⌈{needy}/{ay}⌉={_mc_new_ceil(needy,ay)}.',f'Maximum des deux besoins en A : {max(_mc_new_ceil(needx,ax),_mc_new_ceil(needy,ay))} kits, coût {ca} €.',f'Maximum(⌈{needx}/{bx}⌉,⌈{needy}/{by}⌉) kits B, coût {cb} €.',f'Explorer les couples A/B admissibles : {sol[2]} kit(s) A et {sol[3]} kit(s) B satisfont les deux minima, coût {sol[0]} €.'
        ],dict(kind='n9_engrais',needx=needx,needy=needy,ax=ax,ay=ay,pa=pa,bx=bx,by=by,pb=pb))
    elif idx==20:
        n,a_size,pa,b_size,pb,sol,purea,pureb=_mc_new_mix_instance(rng,need_min=55,need_max=130,lo=9,hi=26,max_b=3)
        # Livraison associative en deux types de véhicules : capacité, nombre limité de B.
        return _mc_new_problem(9,idx,seed,'Les colis de la collecte solidaire',[
            f'Une association doit transporter {n} cartons alimentaires. Une camionnette A peut transporter {a_size} cartons pour {pa} € par trajet.',
            f'Un petit camion B transporte {b_size} cartons pour {pb} € par trajet. Seulement 3 trajets du camion B sont possibles ; les trajets des deux véhicules peuvent être combinés.'
        ],['Combien de trajets A faut-il si on utilise uniquement la camionnette ?','Quel est le coût de tous ces trajets A ?','Combien de cartons peuvent être transportés par trois trajets B ?','Combien de cartons resteraient à transporter par A après ces trois trajets B ?','Quel est le coût minimal des trajets A et B réunis, dans la limite des trois trajets B ?'],
        [_mc_new_ceil(n,a_size),purea,3*b_size,max(0,n-3*b_size),sol[0]],['Trajets A','Coût A seul','Capacité de trois B','Cartons restants','Coût optimal'],['trajets','€','cartons','cartons','€'],['L','B','L','R','C'],[
            f'⌈{n}/{a_size}⌉={_mc_new_ceil(n,a_size)} trajets.',f'{_mc_new_ceil(n,a_size)}×{pa}={purea} €.',f'3×{b_size}={3*b_size} cartons.',f'Maximum(0,{n}−{3*b_size})={max(0,n-3*b_size)} cartons.',f'Comparer 0 à 3 trajets B et compléter avec A : solution {sol[2]} trajet(s) A et {sol[3]} B, coût {sol[0]} €.'
        ],dict(kind='n9_collecte',n=n,a_size=a_size,pa=pa,b_size=b_size,pb=pb))
    elif idx==21:
        for _ in range(300):
            easy=rng.randint(6,11);hard=rng.randint(14,20)
            time_easy=rng.choice([5,6,7]);time_hard=rng.choice([9,10,11,12]);maxhard=rng.choice([2,3])
            limit=rng.randint(30,52)
            options=[(e*easy+h*hard,-(e+h),e,h) for h in range(maxhard+1) for e in range(limit//time_easy+1) if e*time_easy+h*time_hard<=limit]
            best=max(options)
            if best[2]>0 and best[3]>0:break
        score_a=rng.randint(65,105);score_b=rng.randint(100,150)
        return _mc_new_problem(9,idx,seed,'La manche chronométrée des énigmes',[
            f'Une équipe a {score_a} points et son adversaire {score_b}. Il reste {limit} minutes pour une manche décisive.',
            f'Une énigme facile prend {time_easy} minutes et rapporte {easy} points. Une énigme difficile prend {time_hard} minutes et rapporte {hard} points. Il reste au maximum {maxhard} énigmes difficiles, mais suffisamment de faciles.',
            'Chaque énigme commencée doit être entièrement résolue avant la fin du temps. Les énigmes rapportent leurs points uniquement si elles sont achevées.'
        ],['Quel écart de points sépare les deux équipes ?','Combien d’énigmes faciles peuvent être entièrement résolues si l’on ne fait que des faciles ?','Combien d’énigmes difficiles peut-on résoudre dans le temps imparti, en respectant leur nombre disponible ?','Combien de points rapporteraient les seules énigmes faciles complètes réalisables dans le temps disponible ?','Quel est le nombre maximal de points supplémentaires possible en combinant librement les énigmes faciles et difficiles pendant la manche ?'],
        [abs(score_a-score_b),limit//time_easy,min(maxhard,limit//time_hard),(limit//time_easy)*easy,best[0]],['Écart initial','Faciles possibles','Difficiles possibles','Points faciles seuls','Maximum de points'],['points','énigmes','énigmes','points','points'],['R','L','L','Q','C'],[
            f'|{score_a}−{score_b}|={abs(score_a-score_b)} points.',f'{limit}//{time_easy}={limit//time_easy} faciles.',f'Minimum({maxhard},{limit}//{time_hard})={min(maxhard,limit//time_hard)} difficiles.',f'{limit//time_easy}×{easy}={(limit//time_easy)*easy} points.',f'Explorer 0 à {maxhard} énigmes difficiles ; compléter les minutes restantes en faciles. Maximum : {best[2]} faciles et {best[3]} difficiles, pour {best[0]} points en {best[2]*time_easy+best[3]*time_hard} minutes.'
        ],dict(kind='n9_enigmes_temps',easy=easy,hard=hard,time_easy=time_easy,time_hard=time_hard,maxhard=maxhard,limit=limit,score_a=score_a,score_b=score_b))
    elif idx==22:
        # Paquets avec gaspillage limité : contrainte supplémentaire de surplus.
        for _ in range(1200):
            need=rng.randint(55,100);sza=rng.randint(7,11);szb=rng.randint(12,18);pa=rng.randint(7,14);pb=rng.randint(14,23);waste=rng.randint(1,5)
            feasible=[(a*pa+b*pb,a+b,a,b,a*sza+b*szb-need) for a in range(20) for b in range(20) if need<=a*sza+b*szb<=need+waste]
            if not feasible:continue
            best=min(feasible)
            if best[2]>=1 and best[3]>=1 and best[2]+best[3]<=12:break
        else:raise AssertionError('expo sans solution avec gaspillage limité')
        return _mc_new_problem(9,idx,seed,'Les tirages photographiques et les chutes',[
            f'L’exposition a besoin d’au moins {need} tirages photographiques. Le collège ne peut stocker que {waste} tirages supplémentaires au maximum.',
            f'Un lot A contient {sza} tirages et coûte {pa} €. Un lot B en contient {szb} et coûte {pb} €. Les deux types peuvent être combinés ; il faut satisfaire la demande sans dépasser le stock maximal.'
        ],['Combien de tirages faut-il au minimum pour l’exposition ?','Quel est le maximum de tirages autorisé, en comptant le surplus ?','Quel serait le nombre de lots A sans contrainte de surplus ?','Quel serait le nombre de lots B sans contrainte de surplus ?','Quel est le coût minimal des lots A et B combinés en respectant à la fois le minimum et le maximum de tirages ?'],
        [need,need+waste,_mc_new_ceil(need,sza),_mc_new_ceil(need,szb),best[0]],['Besoin minimal','Stock maximal','Lots A sans limite','Lots B sans limite','Coût admissible minimal'],['tirages','tirages','lots','lots','€'],['Q','Q','L','L','C'],[
            f'Le besoin est {need} tirages.',f'{need}+{waste}={need+waste} tirages au maximum.',f'⌈{need}/{sza}⌉={_mc_new_ceil(need,sza)}.',f'⌈{need}/{szb}⌉={_mc_new_ceil(need,szb)}.',f'Examiner les couples dont la quantité est entre {need} et {need+waste} : {best[2]} A + {best[3]} B donnent {need+best[4]} tirages pour {best[0]} €.'
        ],dict(kind='n9_photo',need=need,waste=waste,sza=sza,szb=szb,pa=pa,pb=pb))
    elif idx==23:
        for _ in range(300):
            needx=rng.randint(18,33);needy=rng.randint(18,33)
            ax=rng.randint(6,10);ay=rng.randint(1,3)
            bx=rng.randint(1,3);by=rng.randint(7,11)
            pa=rng.randint(8,17);pb=rng.randint(9,17);max_b=rng.choice([2,3,4])
            try:
                best=_mc_new_2d_combo(needx,needy,ax,ay,pa,bx,by,pb,max_a=28,max_b=max_b)
            except ValueError:
                continue
            purea=max(_mc_new_ceil(needx,ax),_mc_new_ceil(needy,ay))*pa
            if best[2]>0 and best[3]>0 and best[0]<purea:break
        else:raise AssertionError('Aucune combinaison faisable de coffres énergétiques')
        return _mc_new_problem(9,idx,seed,'La réserve énergétique du jeu vidéo',[
            f'Un niveau demande au moins {needx} unités de carburant et {needy} unités de bouclier.',
            f'Un coffre A fournit {ax} unités de carburant et {ay} de bouclier pour {pa} cristaux. Un coffre B fournit {bx} unités de carburant et {by} de bouclier pour {pb} cristaux.',
            f'Il ne reste que {max_b} coffres B dans le magasin, mais suffisamment de A. Les coffres sont indivisibles et on peut mélanger les deux types.'
        ],['Combien de coffres A faut-il pour le carburant seul ?','Combien de coffres B faut-il pour le bouclier seul, si la limite du magasin était ignorée ?','Combien coûterait une solution n’utilisant que A et couvrant les deux ressources ?','Combien de bouclier les coffres B disponibles peuvent-ils donner au maximum ?','Quel est le coût minimal en combinant A et B, avec au plus le nombre de coffres B disponibles ?'],
        [_mc_new_ceil(needx,ax),_mc_new_ceil(needy,by),purea,max_b*by,best[0]],['A pour carburant','B pour bouclier','Prix A seul','Bouclier maximal avec B','Coût optimal'],['coffres','coffres','cristaux','unités','cristaux'],['L','L','B','L','C'],[
            f'⌈{needx}/{ax}⌉={_mc_new_ceil(needx,ax)}.',f'⌈{needy}/{by}⌉={_mc_new_ceil(needy,by)}.',f'A seulement : {purea} cristaux pour couvrir les deux ressources.',f'{max_b}×{by}={max_b*by} boucliers.',f'Tester 0 à {max_b} coffres B, compléter par A pour les deux ressources. Le moins cher est {best[2]} A et {best[3]} B, soit {best[0]} cristaux.'
        ],dict(kind='n9_energy_capped',needx=needx,needy=needy,ax=ax,ay=ay,pa=pa,bx=bx,by=by,pb=pb,max_b=max_b))
    elif idx==24:
        people=rng.randint(52,84);extra=rng.randint(5,12)
        cap_a=people-rng.randint(0,8);upgrade=rng.randint(11,20)
        cap_b=people+extra+rng.randint(0,9)
        fee_a=rng.randint(110,210);each_a=rng.randint(3,7)
        fee_b=rng.randint(110,210);each_b=rng.randint(3,7)
        upgrade_fee=rng.randint(28,65)
        def cost_a(n):return fee_a+n*each_a+(upgrade_fee if n>cap_a else 0)
        def cost_b(n):return fee_b+n*each_b
        val_a_after=people+extra<=cap_a+upgrade
        candidates=([cost_a(people+extra)] if val_a_after else [])+[cost_b(people+extra)]
        best=min(candidates)
        budget=best-rng.randint(10,75)
        return _mc_new_problem(9,idx,seed,'La soirée cinéma et les changements de salle',[
            f'Pour une soirée cinéma, {people} personnes sont inscrites. La salle A possède {cap_a} places : location {fee_a} € puis {each_a} € par spectateur. Une extension de {upgrade} places coûte {upgrade_fee} € supplémentaires si elle est nécessaire.',
            f'La salle B dispose de {cap_b} places, pour {fee_b} € de réservation puis {each_b} € par spectateur, sans extension. Le collège a {budget} € de budget.',
            'La capacité de la salle choisie ne peut jamais être dépassée.'
        ],['Combien de spectateurs sont initialement inscrits ?','Combien de places la salle A peut-elle proposer avec l’extension ?','Quel est le prix complet de A pour le groupe initial (extension comprise si nécessaire) ?','Quel est le prix complet de B pour le groupe initial ?','Si '+str(extra)+' autres spectateurs s’inscrivent, quel est le financement supplémentaire minimal pour choisir la salle admissible la moins chère, en recalculant les deux devis ?'],
        [people,cap_a+upgrade,cost_a(people),cost_b(people),best-budget],['Spectateurs initiaux','Capacité A étendue','Coût A initial','Coût B initial','Financement après inscriptions'],['personnes','places','€','€','€'],['Q','L','B','B','C'],[
            f'{people} personnes.',f'{cap_a}+{upgrade}={cap_a+upgrade} places.',f'{fee_a}+{people}×{each_a}'+(f'+{upgrade_fee}' if people>cap_a else '')+f'={cost_a(people)} €.',f'{fee_b}+{people}×{each_b}={cost_b(people)} €.',f'Nouveau groupe {people+extra} : A coûte {cost_a(people+extra)} €'+(' et est admissible' if val_a_after else ' mais sa capacité est insuffisante')+f'; B coûte {cost_b(people+extra)} € et reste admissible. Meilleur devis : {best} € ; budget {budget} € ; manque {best-budget} €.'
        ],dict(kind='n9_cinema',people=people,extra=extra,budget=budget,fee_a=fee_a,each_a=each_a,cap_a=cap_a,fee_b=fee_b,each_b=each_b,cap_b=cap_b,upgrade=upgrade,upgrade_fee=upgrade_fee))
    elif idx==25:
        flags=rng.randint(33,85);side=rng.randint(30,55);base=rng.randint(45,70);perimeter=2*side+base
        for _ in range(1000):
            cap_a=rng.randint(5,9);cap_b=rng.randint(10,15)
            pa=rng.randint(7,16);pb=rng.randint(14,27)
            sol=_mc_new_combo(flags,cap_a,pa,cap_b,pb)
            purea=_mc_new_ceil(flags,cap_a)*pa;pureb=_mc_new_ceil(flags,cap_b)*pb
            if sol[2]>0 and sol[3]>0 and sol[0]<min(purea,pureb):break
        len_a=cap_a*perimeter+rng.randint(1,perimeter-1)
        len_b=cap_b*perimeter+rng.randint(1,perimeter-1)
        return _mc_new_problem(9,idx,seed,'La coupe des rubans pour les fanions',[
            f'Le collège prépare {flags} fanions triangulaires. Chaque fanion nécessite deux côtés de {side} cm et une base de {base} cm en ruban.',
            f'Un rouleau A contient {len_a} cm pour {pa} € ; un rouleau B contient {len_b} cm pour {pb} €.',
            'Un fanion doit être réalisé dans un seul rouleau, sans raccord. Les chutes d’un rouleau ne sont pas reportées sur un autre. On peut mélanger les achats de rouleaux A et B.'
        ],['Quelle longueur de ruban faut-il pour un fanion ?','Combien de fanions complets produit un rouleau A ?','Combien de fanions complets produit un rouleau B ?','Quel serait le coût en n’achetant que des rouleaux A ?','Quel est le coût minimal en combinant les rouleaux A et B, sans raccord entre rouleaux ?'],
        [perimeter,cap_a,cap_b,purea,sol[0]],['Ruban par fanion','Capacité A','Capacité B','Coût A seul','Coût optimal'],['cm','fanions','fanions','€','€'],['Q','L','L','B','C'],[
            f'2×{side}+{base}={perimeter} cm.',f'{len_a}//{perimeter}={cap_a} fanions complets.',f'{len_b}//{perimeter}={cap_b} fanions complets.',f'⌈{flags}/{cap_a}⌉×{pa}={purea} €.',f'Chercher le mélange le moins cher : {sol[2]} rouleau(x) A et {sol[3]} B permettent {sol[2]*cap_a+sol[3]*cap_b} fanions, coût {sol[0]} €.'
        ],dict(kind='n9_rubans',flags=flags,side=side,base=base,len_a=len_a,len_b=len_b,pa=pa,pb=pb))
    raise ValueError(f'Modèle N9 inconnu {idx}')

# Points d'entrée nommés : compatibles avec le tirage existant et les tests.
for _niveau,_fonction in ((8,_mc_new_n8),(9,_mc_new_n9)):
    for _index in range(11,26):
        def _fabrique(index=_index,niveau=_niveau):
            def _modele(seed=None):
                return _mc_new_n8(index,seed) if niveau==8 else _mc_new_n9(index,seed)
            _modele.__name__=f'generer_modele_p{niveau}_m{index:02d}'
            return _modele
        globals()[f'generer_modele_p{_niveau}_m{_index:02d}']=_fabrique()
del _niveau,_index,_fonction,_fabrique


def generer_exercices_priorites(difficulte, nombre=1, historique_modeles=None):
    """Tire des modèles distincts, en privilégiant les moins récemment vus.

    `historique_modeles` est une liste facultative des identifiants de modèles
    du même élève et du même niveau, du plus récent au plus ancien.
    Le comportement aléatoire historique demeure si cette liste est absente.
    """
    if difficulte not in BANQUE_PRIORITES:
        raise ValueError("Difficulté attendue : 1, 2 ou 3.")
    # 26 modèles N7, 25 N8 et 25 N9 : la banque statique contient seulement
    # cinq exemples historiques par niveau, remplacés par les générateurs.
    capacite_reelle = {1: 26, 2: 25, 3: 25}[difficulte]
    if not isinstance(nombre, int) or isinstance(nombre, bool) or not 1 <= nombre <= capacite_reelle:
        raise ValueError(
            "Nombre d’exercices demandé supérieur aux modèles disponibles pour ce niveau."
        )
    
    banque = deepcopy(BANQUE_PRIORITES[difficulte])
    if difficulte == 1:
        banque = [
            exercice for exercice in banque
            if exercice["id"] not in [
                "P7-01", "P7-02", "P7-03", "P7-04", "P7-05"
            ]
        ]

        banque.append(generer_modele_p7_fete())
        banque.append(generer_modele_p7_cartes())
        banque.append(generer_modele_p7_badminton())
        banque.append(generer_modele_p7_jeu_video())
        banque.append(generer_modele_p7_dessin())
        banque.append(generer_modele_p7_tables_dessin())
        banque.append(generer_modele_p7_sciences())
        banque.append(generer_modele_p7_patisserie())
        banque.append(generer_modele_p7_enigmes())
        banque.append(generer_modele_p7_photos())
        banque.append(generer_modele_p7_velo())
        banque.append(generer_modele_p7_planetarium())
        banque.append(generer_modele_p7_robotique())
        banque.append(generer_modele_p7_collecte_solidaire())
        banque.append(generer_modele_p7_repetitions())
        banque.append(generer_modele_p7_plantations())
        banque.append(generer_modele_p7_echecs())
        banque.append(generer_modele_p7_fresque())
        banque.append(generer_modele_p7_carnets_transport())
        banque.append(generer_modele_p7_course_solidaire())
        banque.append(generer_modele_p7_refuge())
        banque.append(generer_modele_p7_defi_lecture())
        banque.append(generer_modele_p7_couture())
        banque.append(generer_modele_p7_casiers())
        banque.append(generer_modele_p7_carte_orientation())
        banque.append(generer_modele_p7_aquarium())

    if difficulte == 2:
        banque = [
            exercice for exercice in banque
            if exercice["id"] not in [
                "P8-01", "P8-02", "P8-03", "P8-04", "P8-05"
            ]
        ]
        banque.append(generer_modele_p8_clubs())
        banque.append(generer_modele_p8_manga())
        banque.append(generer_modele_p8_jeu_video())
        banque.append(generer_modele_p8_robotique())
        banque.append(generer_modele_p8_jeu_piste())
        banque.append(generer_modele_p8_kits())
        banque.append(generer_modele_p8_eau())
        banque.append(generer_modele_p8_parcours())
        banque.append(generer_modele_p8_boissons())
        banque.append(generer_modele_p8_transport())
        # Quinze nouveaux modèles, sans suppression des dix modèles existants.
        banque.append(generer_modele_p8_m11())
        banque.append(generer_modele_p8_m12())
        banque.append(generer_modele_p8_m13())
        banque.append(generer_modele_p8_m14())
        banque.append(generer_modele_p8_m15())
        banque.append(generer_modele_p8_m16())
        banque.append(generer_modele_p8_m17())
        banque.append(generer_modele_p8_m18())
        banque.append(generer_modele_p8_m19())
        banque.append(generer_modele_p8_m20())
        banque.append(generer_modele_p8_m21())
        banque.append(generer_modele_p8_m22())
        banque.append(generer_modele_p8_m23())
        banque.append(generer_modele_p8_m24())
        banque.append(generer_modele_p8_m25())
        

    if difficulte == 3:
        banque = [
            exercice for exercice in banque
            if exercice["id"] not in [
                "P9-01", "P9-02", "P9-03", "P9-04", "P9-05"
            ]
        ]

        banque.append(generer_modele_p9_potager())
        banque.append(generer_modele_p9_tournoi())
        banque.append(generer_modele_p9_festival())
        banque.append(generer_modele_p9_cristaux())
        banque.append(generer_modele_p9_bibliotheque())
        banque.append(generer_modele_p9_spectacle())
        banque.append(generer_modele_p9_recyclage())
        banque.append(generer_modele_p9_salles())
        banque.append(generer_modele_p9_drones())
        banque.append(generer_modele_p9_mosaique())
        # Quinze nouveaux modèles, sans suppression des dix modèles existants.
        banque.append(generer_modele_p9_m11())
        banque.append(generer_modele_p9_m12())
        banque.append(generer_modele_p9_m13())
        banque.append(generer_modele_p9_m14())
        banque.append(generer_modele_p9_m15())
        banque.append(generer_modele_p9_m16())
        banque.append(generer_modele_p9_m17())
        banque.append(generer_modele_p9_m18())
        banque.append(generer_modele_p9_m19())
        banque.append(generer_modele_p9_m20())
        banque.append(generer_modele_p9_m21())
        banque.append(generer_modele_p9_m22())
        banque.append(generer_modele_p9_m23())
        banque.append(generer_modele_p9_m24())
        banque.append(generer_modele_p9_m25())
            
    # Même tirage aléatoire qu'avant en l'absence d'historique utilisable.
    # Chaque nouvelle série privilégie ensuite les modèles les moins récents.
    # Les entrées absentes de l'historique sont prioritaires ; les égalités
    # restent aléatoires afin de ne pas créer de séquence fixe entre élèves.
    historique = historique_modeles if isinstance(historique_modeles, (list, tuple)) else []
    derniere_apparition = {}
    for position, modele_id in enumerate(historique):
        if isinstance(modele_id, str) and modele_id not in derniere_apparition:
            derniere_apparition[modele_id] = position
    if derniere_apparition:
        random.shuffle(banque)
        priorite_inedit = len(historique) + 1
        banque.sort(
            key=lambda exercice: derniere_apparition.get(
                exercice.get("id"), priorite_inedit
            ),
            reverse=True,
        )
        exercices = banque[:nombre]
    else:
        exercices = random.sample(banque, k=nombre)
    for exercice in exercices:
        if "champs_reponse" not in exercice:
            exercice["champs_reponse"] = deepcopy(
                REPONSES_PRIORITES[exercice["id"]]
            )

    return exercices


