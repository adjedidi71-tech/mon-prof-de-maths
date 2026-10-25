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
    banque.append(generer_modele_p7_sciences())
    banque.append(generer_modele_p7_patisserie())

    exercices = random.sample(banque, k=nombre)

    for exercice in exercices:
        if "champs_reponse" not in exercice:
            exercice["champs_reponse"] = deepcopy(
                REPONSES_PRIORITES[exercice["id"]]
            )

    return exercices


