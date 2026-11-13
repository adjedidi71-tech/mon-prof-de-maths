"""MathiCap — structure unique des problèmes créés à partir du 13/11/2026.

Une question = un champ évalué. Structure : 4 questions au niveau 7,
5 questions aux niveaux 8 et 9. La dernière est la résolution finale.

Ce module traite uniquement les NOUVEAUX exercices issus des 31 modèles
P7-Mxx/P8-Mxx/P9-Mxx du chapitre Opérations. Les séries déjà sauvegardées
contiennent leur propre copie des exercices et ne sont jamais modifiées.
"""

from copy import deepcopy
import re


# L'ordre est pédagogique (étapes préparatoires, puis résolution finale).
# Un texte de question ne réclame qu'une seule réponse évaluée.
# Les champs préexistants conservent leurs identifiants pour les corrections.
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
        ("r1", "Calcule le score final de l'équipe A."),
        ("r2", "Calcule le score final de l'équipe B."),
        ("r3", "Quelle équipe remporte le tournoi : A ou B ?"),
        ("r4", "De combien de points l'équipe gagnante devance-t-elle l'autre ?"),
    ],
    "P7-M04": [
        ("r1", "Combien coûte l'impression avec l'offre A ?"),
        ("r2", "Combien coûte l'impression avec l'offre B ?"),
        ("r3", "Quelle offre est la moins chère : A ou B ?"),
        ("r4", "Quelle économie le club réalisera-t-il en choisissant l'offre la moins chère ?"),
    ],
    "P7-M05": [
        ("r1", "Quelle est la distance de l'aller-retour jusqu'au parc ?"),
        ("r2", "Quelle distance totale a déjà été parcourue après les boucles dans le parc ?"),
        ("r3", "Quelle distance manque-t-il pour atteindre l'objectif ?"),
        ("r4", "Combien de petits tours complets faut-il encore faire, au minimum, pour atteindre l'objectif ?"),
    ],
    "P7-M06": [
        ("r1", "Quel est le montant total des recettes de la fête ?"),
        ("r2", "Quel est le montant total des dépenses de la fête ?"),
        ("r3", "Quelle somme reste-t-il dans la caisse après la fête ?"),
        ("choix", "Le club a-t-il atteint son objectif de réserve : oui ou non ?"),
    ],
    "P7-M07": [
        ("r1", "Combien de cartes achète-t-il au total ?"),
        ("r2", "Combien de nouvelles cartes conserve-t-il avant les échanges ?"),
        ("r3", "Combien de cartes différentes obtient-il grâce aux échanges ?"),
        ("r4", "Combien de cartes différentes possède-t-il finalement dans son album ?"),
    ],
    "P7-M08": [
        ("r1", "Combien de volants le club a-t-il achetés ?"),
        ("r2", "Combien de volants utilisables possède-t-il après avoir retiré les volants abîmés ?"),
        ("r3", "Combien de volants faut-il pour tous les matchs ?"),
        ("r5", "Quelle est la différence entre les volants disponibles et les volants nécessaires (manque ou reste) ?"),
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
        ("r3", "Combien de panneaux peuvent être entièrement remplis ?"),
        ("r4", "Combien de dessins seront placés sur le dernier panneau incomplet ?"),
        ("r5", "Combien de panneaux faudra-t-il au total pour exposer tous les dessins ?"),
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
        ("r6", "Quelle est la différence entre le budget disponible et la somme nécessaire pour les souvenirs et la réserve minimale ?"),
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
        ("r6", "Quel est l'écart en minutes entre la durée totale et le temps maximal autorisé ?"),
    ],
    "P8-M09": [
        ("r1", "Quel volume de boisson est obtenu avec une seule préparation, en cL ?"),
        ("r2", "Quel est le volume total préparé, en litres ?"),
        ("r3", "Combien de bouteilles peuvent être entièrement remplies ?"),
        ("r4", "Combien de cL faudra-t-il verser dans la dernière bouteille ?"),
        ("r5", "Combien de bouteilles sont nécessaires au total pour contenir toute la boisson ?"),
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
        ("r4", "Quel est le coût total du voyage avec la formule A ?"),
        ("r5", "Quel est le coût total du voyage avec la formule B ?"),
        ("r7", "Combien économise-t-on en choisissant la formule la moins chère ?"),
    ],
    "P9-M04": [
        ("r1", "Combien de cristaux l'aventurier gagne-t-il pendant les missions, bonus compris ?"),
        ("r2", "Combien de cristaux possède-t-il après le piège, avant les achats ?"),
        ("r3", "Combien d'équipements peut-il acheter au maximum en conservant sa réserve ?"),
        ("r4", "Combien de cristaux lui restera-t-il après ces achats ?"),
        ("r6", "Combien d'équipements lui manque-t-il pour équiper tous les aventuriers, si ce maximum ne suffit pas ?"),
    ],
    "P9-M05": [
        ("r1", "Combien de mangas contiennent tous les colis reçus ?"),
        ("r2", "Combien de mangas ont été prêtés au total aux classes ?"),
        ("r3", "Quelle est l'ampleur de la variation du nombre de mangas sur les étagères pendant la semaine ?"),
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
    "P7-M07": "Q Q Q Q", "P7-M08": "Q Q Q R", "P7-M09": "Q B R R",
    "P7-M10": "Q Q R R", "P7-M11": "Q Q Q R",
    "P8-M01": "B B B B L", "P8-M02": "Q Q L R L", "P8-M03": "Q Q Q C R",
    "P8-M04": "Q Q L B R", "P8-M05": "L B B B R", "P8-M06": "B B B C R",
    "P8-M07": "D Q Q R R", "P8-M08": "D D D D R", "P8-M09": "Q Q L R L",
    "P8-M10": "D B B C R",
    "P9-M01": "Q Q B B B", "P9-M02": "B B B R B", "P9-M03": "Q B B B R",
    "P9-M04": "Q Q L R L", "P9-M05": "Q Q R Q Q", "P9-M06": "Q B B B L",
    "P9-M07": "Q Q B B R", "P9-M08": "Q Q B B C", "P9-M09": "Q Q L R R",
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


def uniformiser_exercice(exercice):
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

    resultat["enonce"] = (
        blocs[0].rstrip() + "\n\n**Questions**\n\n"
        + "\n\n".join(lignes_questions)
        + "\n\n*Écris tes calculs et ton raisonnement au brouillon. "
        "Les champs de réponse sont notés automatiquement ; "
        "compare ta méthode avec la correction.*"
    )
    ancien_corrige = resultat.get("correction") or ""
    # Le raisonnement d'origine est conservé, mais les numéros de ses étapes
    # ne doivent pas entrer en contradiction avec les nouvelles questions.
    ancien_corrige = re.sub(r"(?m)^\*\*\d+\.\s*([^*\n]+)\*\*", r"**Étape : \1**", ancien_corrige)
    resultat["correction"] = (
        "**Réponses attendues — questions de ce problème**\n\n"
        + "\n\n".join(lignes_corrige)
        + "\n\n**Méthode et calculs détaillés**\n\n"
        + ancien_corrige
    )
    resultat["champs_reponse"] = nouveaux_champs
    resultat["mathicap_questions_uniformisees"] = 1
    return resultat
