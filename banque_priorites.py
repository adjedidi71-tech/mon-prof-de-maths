"""Banque vérifiée de problèmes — 5e, Opérations / Priorités opératoires.

Difficultés :
    1 = niveau 7 (Je résous des problèmes)
    2 = niveau 8
    3 = niveau 9

Les exercices sont écrits et conservés : aucune API d'IA n'est appelée.
Le nombre maximal de problèmes distincts par niveau est actuellement de 3.
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
    ],
}


def generer_exercices_priorites(difficulte, nombre=1):
    """Tire `nombre` problèmes distincts du niveau demandé.

    Cette banque contient pour le moment 3 exercices par niveau.
    Pour demander 4 ou 5 exercices sans répétition, il faudra d'abord
    enrichir la banque avec d'autres exercices validés.
    """
    if difficulte not in BANQUE_PRIORITES:
        raise ValueError("Difficulté attendue : 1, 2 ou 3.")
    if not isinstance(nombre, int) or not 1 <= nombre <= len(BANQUE_PRIORITES[difficulte]):
        raise ValueError(
            "Cette banque contient actuellement 3 exercices distincts par difficulté."
        )
    return deepcopy(random.sample(BANQUE_PRIORITES[difficulte], k=nombre))
