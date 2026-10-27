"""Banque vérifiée de problèmes — 5e, Opérations / Priorités opératoires.

Difficultés :
    1 = niveau 7 (Je résous des problèmes)
    2 = niveau 8
    3 = niveau 9

Les exercices sont écrits et conservés : aucune API d'IA n'est appelée.
Le nombre maximal de problèmes distincts par niveau est de 5.
"""

from copy import deepcopy
import random


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
    budget = depense + random.randint(15, 45)
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
        "**2. Nombre de paquets**\n\n"
        f"Piles à acheter : {necessaires} - {stock} "
        f"= {a_acheter}.\n"
        f"Division : {a_acheter} ÷ {capacite_paquet}.\n"
        f"Quotient : {quotient}, reste : {reste}.\n"
        f"Il faut acheter {paquets} paquets.\n\n"
        "**3. Budget restant**\n\n"
        f"Prix des paquets : {paquets} × {prix_paquet} "
        f"= {paquets * prix_paquet} €.\n"
        f"Dépense totale : {paquets * prix_paquet} "
        f"+ {frais} = {depense} €.\n"
        f"Budget restant : {budget} - {depense} "
        f"= {restant} €."
    )

    return {
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
    }


def generer_modele_p7_patisserie():
    plateaux = random.randint(6, 10)
    par_plateau = 12
    reserves = random.randint(7, 16)
    par_sachet = random.choice([4, 5, 6])
    prix_sachet = random.randint(5, 8)
    cout_ingredients = random.randint(20, 35)

    total = plateaux * par_plateau
    disponibles = total - reserves
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

    return {
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
    }

def generer_modele_p7_enigmes():
    points_facile = 8
    points_difficile = 15
    penalite = 4

    faciles_a = random.randint(4, 8)
    difficiles_a = random.randint(2, 5)
    indices_a = random.randint(1, 3)

    while True:
        faciles_b = random.randint(4, 8)
        difficiles_b = random.randint(2, 5)
        indices_b = random.randint(1, 3)

        score_a = (
            faciles_a * points_facile
            + difficiles_a * points_difficile
            - indices_a * penalite
        )

        score_b = (
            faciles_b * points_facile
            + difficiles_b * points_difficile
            - indices_b * penalite
        )

        if score_a != score_b:
            break

    gagnant = "A" if score_a > score_b else "B"
    ecart = abs(score_a - score_b)

    enonce = (
        "**Le tournoi d'énigmes**\n\n"
        "Deux équipes participent à un tournoi "
        "d'énigmes organisé au collège.\n\n"
        "Le règlement prévoit :\n"
        f"- {points_facile} points par énigme facile résolue ;\n"
        f"- {points_difficile} points par énigme difficile résolue ;\n"
        f"- {penalite} points retirés pour chaque indice utilisé.\n\n"
        "**Équipe A :**\n"
        f"- {faciles_a} énigmes faciles résolues ;\n"
        f"- {difficiles_a} énigmes difficiles résolues ;\n"
        f"- {indices_a} indices utilisés.\n\n"
        "**Équipe B :**\n"
        f"- {faciles_b} énigmes faciles résolues ;\n"
        f"- {difficiles_b} énigmes difficiles résolues ;\n"
        f"- {indices_b} indices utilisés.\n\n"
        "**Questions**\n\n"
        "1. Calcule le score final de l'équipe A.\n\n"
        "2. Calcule le score final de l'équipe B.\n\n"
        "3. Quelle équipe remporte le tournoi ? "
        "Avec combien de points d'avance ?"
    )

    correction = (
        "**1. Score de l'équipe A**\n\n"
        f"({faciles_a} × {points_facile}) "
        f"+ ({difficiles_a} × {points_difficile}) "
        f"− ({indices_a} × {penalite})\n\n"
        f"= {score_a} points.\n\n"
        "**2. Score de l'équipe B**\n\n"
        f"({faciles_b} × {points_facile}) "
        f"+ ({difficiles_b} × {points_difficile}) "
        f"− ({indices_b} × {penalite})\n\n"
        f"= {score_b} points.\n\n"
        "**3. Équipe gagnante**\n\n"
        f"L'équipe A obtient {score_a} points.\n\n"
        f"L'équipe B obtient {score_b} points.\n\n"
        f"Écart : {max(score_a, score_b)} "
        f"− {min(score_a, score_b)} "
        f"= {ecart} points.\n\n"
        f"**Réponse :** L'équipe {gagnant} gagne "
        f"avec {ecart} points d'avance."
    )

    return {
        "id": "P7-M03",
        "titre": "Le tournoi d'énigmes",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Score de l'équipe A",
                "type": "nombre",
                "attendu": score_a,
                "unite": "points"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Score de l'équipe B",
                "type": "nombre",
                "attendu": score_b,
                "unite": "points"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Équipe gagnante",
                "type": "choix",
                "attendu": gagnant,
                "options": ["A", "B"]
            },
            {
                "id": "r4",
                "question": 3,
                "libelle": "Écart entre les deux équipes",
                "type": "nombre",
                "attendu": ecart,
                "unite": "points"
            }
        ]
    }

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

    return {
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
    }

def generer_modele_p7_velo():

    def km(valeur):
        return f"{valeur / 10:.1f}".replace(".", ",")

    # Distances exprimées en dixièmes de kilomètre
    trajet = random.randint(32, 68)
    boucle = random.randint(18, 36)
    nb_boucles = random.randint(2, 4)
    petit_tour = random.randint(12, 23)

    aller_retour = 2 * trajet
    distance_initiale = aller_retour + nb_boucles * boucle

    manque = random.randint(
        petit_tour + 2,
        petit_tour * 3 + 8
    )

    objectif = distance_initiale + manque

    tours = (manque + petit_tour - 1) // petit_tour

    enonce = (
        "**Le rallye à vélo**\n\n"
        "Trois amis organisent une sortie à vélo.\n\n"
        f"Ils parcourent {km(trajet)} km pour rejoindre "
        "un parc, puis empruntent le même trajet pour rentrer.\n\n"
        f"Dans le parc, ils effectuent {nb_boucles} boucles "
        f"de {km(boucle)} km chacune.\n\n"
        f"Leur objectif est de parcourir au moins "
        f"{km(objectif)} km au total.\n\n"
        "Pour compléter leur parcours, ils peuvent effectuer "
        f"des petits tours supplémentaires de {km(petit_tour)} km "
        "chacun, près de chez eux.\n\n"
        "**Questions**\n\n"
        "1. Quelle distance représente l'aller-retour "
        "jusqu'au parc ?\n\n"
        "2. Quelle distance totale ont-ils parcourue "
        "après les boucles dans le parc ?\n\n"
        "3. Quelle distance leur manque-t-il pour atteindre "
        "leur objectif ? Combien de petits tours complets "
        "doivent-ils effectuer au minimum pour atteindre "
        "ou dépasser cet objectif ?"
    )

    correction = (
        "**1. Distance aller-retour**\n\n"
        f"2 × {km(trajet)} = {km(aller_retour)} km.\n\n"

        "**2. Distance totale parcourue**\n\n"
        f"Distance des boucles : {nb_boucles} × "
        f"{km(boucle)} = {km(nb_boucles * boucle)} km.\n\n"
        f"Distance totale : {km(aller_retour)} + "
        f"{km(nb_boucles * boucle)} "
        f"= {km(distance_initiale)} km.\n\n"
        "**Expression complète :**\n\n"
        f"2 × {km(trajet)} + {nb_boucles} × "
        f"{km(boucle)} = {km(distance_initiale)} km.\n\n"

        "**3. Distance manquante et petits tours**\n\n"
        f"{km(objectif)} − {km(distance_initiale)} "
        f"= {km(manque)} km.\n\n"
        f"Chaque petit tour mesure {km(petit_tour)} km.\n\n"
        f"Avec {tours - 1} tour(s), ils parcourent "
        f"{km((tours - 1) * petit_tour)} km : "
        "ce n'est pas suffisant.\n\n"
        f"Avec {tours} tours, ils parcourent "
        f"{km(tours * petit_tour)} km : "
        "l'objectif est atteint ou dépassé.\n\n"
        f"**Réponse :** Ils doivent effectuer au minimum "
        f"{tours} petits tours complets."
    )

    return {
        "id": "P7-M05",
        "titre": "Le rallye à vélo",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Distance aller-retour",
                "type": "nombre",
                "attendu": aller_retour / 10,
                "unite": "km"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Distance totale parcourue",
                "type": "nombre",
                "attendu": distance_initiale / 10,
                "unite": "km"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Distance manquante",
                "type": "nombre",
                "attendu": manque / 10,
                "unite": "km"
            },
            {
                "id": "r4",
                "question": 3,
                "libelle": "Nombre minimal de petits tours",
                "type": "nombre",
                "attendu": tours,
                "unite": "tours"
            }
        ]
    }

def generer_modele_p7_fete():
    caisse = random.randint(160, 240)

    eleves = random.randint(14, 22)
    parents = random.randint(8, 14)

    prix_eleve = random.randint(5, 8)
    prix_parent = random.randint(9, 12)

    salle = random.randint(70, 110)
    decoration = random.randint(20, 45)
    prix_badge = random.randint(1, 3)

    reserve_minimale = random.randint(130, 230)

    participants = eleves + parents

    recettes = eleves * prix_eleve + parents * prix_parent

    cout_badges = participants * prix_badge
    depenses = salle + decoration + cout_badges

    restant = caisse + recettes - depenses

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

    return {
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
    }

def generer_modele_p7_cartes():

    cartes_depart = random.randint(65, 110)
    paquets = random.randint(5, 9)
    cartes_paquet = random.choice([6, 8])

    cartes_achetees = paquets * cartes_paquet

    doublons = random.choice([8, 10, 12, 14, 16, 18, 20])

    nouvelles_cartes = cartes_achetees - doublons

    cartes_echangees = doublons // 2
    doublons_restants = 0

    total_collection = (
        cartes_depart
        + nouvelles_cartes
        + cartes_echangees
    )

    enonce = (
        "**Une collection de cartes**\n\n"
        f"Un collégien possède déjà {cartes_depart} "
        "cartes différentes dans son album.\n\n"
        f"Il achète {paquets} paquets contenant chacun "
        f"{cartes_paquet} cartes.\n\n"
        f"Parmi les cartes achetées, {doublons} sont "
        "des doublons, c'est-à-dire des cartes qu'il "
        "possède déjà dans son album. "
        "Toutes les autres sont nouvelles "
        "pour sa collection.\n\n"
        "Il échange ensuite ses doublons avec un ami : "
        "pour **2 doublons donnés**, il reçoit "
        "**1 carte différente** qu'il ne possède pas encore.\n\n"
        "Son ami dispose de suffisamment de cartes "
        "pour réaliser tous les échanges possibles.\n\n"
        "**Questions**\n\n"
        "1. Combien de cartes achète-t-il au total ?\n\n"
        "2. Combien de nouvelles cartes conserve-t-il "
        "avant les échanges ?\n\n"
        "3. Combien de nouvelles cartes obtient-il "
        "grâce aux échanges ?\n\n"
        "4. Combien de cartes différentes possède-t-il "
        "finalement dans son album ?"
    )

    correction = (
        "**1. Nombre de cartes achetées**\n\n"
        f"{paquets} × {cartes_paquet} "
        f"= {cartes_achetees} cartes.\n\n"

        "**2. Nouvelles cartes avant les échanges**\n\n"
        f"{cartes_achetees} − {doublons} "
        f"= {nouvelles_cartes} cartes.\n\n"

        "**3. Cartes obtenues par échange**\n\n"
        f"Il possède {doublons} doublons.\n\n"
        f"En les regroupant par 2, il peut réaliser "
        f"{cartes_echangees} échanges.\n\n"
        f"Il obtient donc {cartes_echangees} "
        "nouvelles cartes.\n\n"
        f"Doublons non échangés : {doublons_restants}.\n\n"

        "**4. Collection finale**\n\n"
        f"{cartes_depart} + {nouvelles_cartes} "
        f"+ {cartes_echangees} "
        f"= {total_collection} cartes.\n\n"

        "**Expression complète :**\n\n"
        f"{cartes_depart} + "
        f"({paquets} × {cartes_paquet} − {doublons}) "
        f"+ {cartes_echangees} "
        f"= {total_collection}.\n\n"

        f"**Réponse :** Il possède finalement "
        f"{total_collection} cartes différentes."
    )

    return {
        "id": "P7-M07",
        "titre": "Une collection de cartes",
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": None,
        "champs_reponse": [
            {
                "id": "r1",
                "question": 1,
                "libelle": "Cartes achetées",
                "type": "nombre",
                "attendu": cartes_achetees,
                "unite": "cartes"
            },
            {
                "id": "r2",
                "question": 2,
                "libelle": "Nouvelles cartes avant échanges",
                "type": "nombre",
                "attendu": nouvelles_cartes,
                "unite": "cartes"
            },
            {
                "id": "r3",
                "question": 3,
                "libelle": "Cartes obtenues par échange",
                "type": "nombre",
                "attendu": cartes_echangees,
                "unite": "cartes"
            },
            {
                "id": "r4",
                "question": 4,
                "libelle": "Cartes différentes dans l'album",
                "type": "nombre",
                "attendu": total_collection,
                "unite": "cartes"
            }
        ]
    }

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
        conclusion = (
            f"Il restera {ecart} volants utilisables "
            "après le tournoi."
        )
        libelle_ecart = "Nombre de volants restants"
    else:
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
        "Le tournoi comporte :\n"
        f"- {nb_matchs} matchs ;\n"
        f"- une prévision de {volants_par_match} "
        "volants utilisés par match.\n\n"
        "**Questions**\n\n"
        "1. Combien de volants le club a-t-il achetés ?\n\n"
        "2. Combien de volants utilisables possède-t-il "
        "après avoir retiré les volants abîmés ?\n\n"
        "3. Combien de volants faut-il prévoir "
        "pour tous les matchs ?\n\n"
        "4. Le club dispose-t-il de suffisamment "
        "de volants ? Combien en restera-t-il "
        "ou combien en manquera-t-il ?"
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
        f"{conclusion}\n\n"

        "**Expression complète du stock disponible :**\n\n"
        f"{stock_initial} + "
        f"{nb_boites} × {volants_par_boite} "
        f"− {volants_abimes} "
        f"= {volants_utilisables}."
    )

    return {
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
    }

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

    variation_prix = random.choice([
        -30, -20, -10, 10, 20, 30
    ])
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

    return {
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
    }

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

    variation = random.choice([-12, -8, 8, 12])
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
        "Pendant l'atelier :\n"
        f"- {nb_groupes} groupes participent ;\n"
        f"- chaque groupe comporte {eleves_par_groupe} élèves ;\n"
        f"- chaque élève utilise {feuilles_par_eleve} feuilles.\n\n"
        "Après l'atelier, le club souhaite préparer "
        "une exposition nécessitant "
        f"{feuilles_exposition} feuilles supplémentaires.\n\n"
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

        "**Expression complète :**\n\n"
        f"{feuilles_depart} "
        f"+ ({nb_paquets} × {feuilles_par_paquet}) "
        f"− {feuilles_abimees} "
        f"− ({nb_groupes} × {eleves_par_groupe} "
        f"× {feuilles_par_eleve}) "
        f"= {feuilles_restantes}.\n\n"

        "**4. Préparation de l'exposition**\n\n"
        f"Feuilles disponibles : {feuilles_restantes}.\n\n"
        f"Feuilles nécessaires : {feuilles_exposition}.\n\n"
        f"Différence : {difference} feuilles.\n\n"
        f"**Stock suffisant : {suffisant}.**\n\n"
        f"{conclusion}"
    )

    return {
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
    }

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

    return {
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
    }

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

    return {
        "id": "P8-M01",
        "titre": "La fête des clubs du collège — TEST V2",
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
    }


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

        "Les organisateurs remplissent d'abord autant "
        "de panneaux que possible, puis placent les "
        "dessins restants sur un dernier panneau.\n\n"

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

        "**4. Dernier panneau et nombre total**\n\n"

        f"Il reste {dessins_dernier} dessins "
        "à placer sur un dernier panneau.\n\n"

        f"Nombre total de panneaux : "
        f"{panneaux_complets} + 1 "
        f"= {panneaux_total}.\n\n"

        f"**Réponse :** Il faut {panneaux_total} "
        f"panneaux au total, dont un dernier contenant "
        f"{dessins_dernier} dessins."
    )

    return {
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
                "libelle": "Nombre total de panneaux",
                "type": "nombre",
                "attendu": panneaux_total,
                "unite": "panneaux"
            }
        ]
    }

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

    return {
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
                "options": ["A", "B"]
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
    }

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
        f"{batteries_reserve} batteries de réserve.\n\n"

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

    return {
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
    }

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

    # Génère les deux situations : budget suffisant
    # ou insuffisant pour les souvenirs et la réserve.
    variation = random.choice([
        -500, -300, -200, 200, 300, 500
    ])

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

    return {
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
                "options": ["Oui", "Non"]
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
    }

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
    variation = rng.choice([-15, -10, -5, 5, 10, 15])
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

    return {
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
    }

def generer_exercices_priorites(difficulte, nombre=1):
    """Tire `nombre` problèmes distincts du niveau demandé.

    Cette banque contient 5 exercices distincts par niveau.
    """
    if difficulte not in BANQUE_PRIORITES:
        raise ValueError("Difficulté attendue : 1, 2 ou 3.")
    if not isinstance(nombre, int) or not 1 <= nombre <= len(BANQUE_PRIORITES[difficulte]):
        raise ValueError(
            "Cette banque contient 5 exercices distincts par difficulté."
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
    
    exercices = random.sample(banque, k=nombre)

    for exercice in exercices:
        if "champs_reponse" not in exercice:
            exercice["champs_reponse"] = deepcopy(
                REPONSES_PRIORITES[exercice["id"]]
            )

    return exercices


