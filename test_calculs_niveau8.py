"""Contrôles mathématiques indépendants des modèles P8-M01 à P8-M05.

Lancement : python -m unittest -v test_calculs_niveau8.py
Ces tests relisent les données numériques dans les énoncés, recalculent les
résultats et les comparent aux réponses attendues par Streamlit.
"""

from decimal import Decimal
import random
import re
import unittest

import banque_priorites as banque


VARIANTES_PAR_MODELE = 50


def extraire(texte, motif, identifiant):
    resultat = re.search(motif, texte, flags=re.IGNORECASE)
    if resultat is None:
        raise AssertionError(
            f"{identifiant} : information introuvable dans l'énoncé : {motif}"
        )
    return resultat.group(1)


def entier(texte, motif, identifiant):
    return int(extraire(texte, motif, identifiant))


def centimes(texte, motif, identifiant):
    valeur = extraire(texte, motif, identifiant).replace(",", ".")
    return int(Decimal(valeur) * 100)


def reponses(exercice):
    # Les expressions libres ne possèdent volontairement pas de clé "attendu".
    return {
        c["id"]: c["attendu"]
        for c in exercice["champs_reponse"]
        if c["type"] != "texte_libre"
    }


class TestsCalculsNiveau8(unittest.TestCase):
    def verifier_resultats(self, exercice, resultats):
        identifiant = exercice["id"]
        attendus = reponses(exercice)
        self.assertEqual(set(attendus), set(resultats),
                         f"{identifiant}: champs numériques/choix inattendus")
        for champ_id, attendu in resultats.items():
            with self.subTest(champ=champ_id):
                if isinstance(attendu, (int, float, Decimal)) and not isinstance(attendu, bool):
                    self.assertAlmostEqual(float(attendus[champ_id]), float(attendu), places=6,
                                           msg=f"{identifiant}/{champ_id}")
                else:
                    self.assertEqual(attendus[champ_id], attendu,
                                     f"{identifiant}/{champ_id}")

    def controler_p8_m01(self, ex):
        s, i = ex["enonce"], ex["id"]
        clubs = entier(s, r"Les (\d+) clubs du collège", i)
        billets = entier(s, r"- (\d+) billets d'entrée", i)
        prix_billet = entier(s, r"billets d'entrée à (\d+) €", i)
        gateaux = entier(s, r"- (\d+) parts de gâteau", i)
        prix_gateau = entier(s, r"parts de gâteau à (\d+) €", i)
        location = entier(s, r"- (\d+) € pour la location", i)
        lots = entier(s, r"- (\d+) lots de fournitures", i)
        prix_lot = entier(s, r"lots de fournitures à (\d+) €", i)
        reserve = entier(s, r"conserver (\d+) €", i)
        recettes = billets * prix_billet + gateaux * prix_gateau
        depenses = location + lots * prix_lot
        somme = recettes - depenses - reserve
        self.assertGreaterEqual(somme, 0)
        self.assertEqual((somme * 100) % clubs, 0,
                         "P8-M01 : partage impossible au centime près")
        self.verifier_resultats(ex, {
            "r1": recettes, "r2": depenses, "r3": somme, "r4": somme / clubs
        })

    def controler_p8_m02(self, ex):
        s, i = ex["enonce"], ex["id"]
        eleves = entier(s, r"(\d+) élèves participent", i)
        par_eleve = entier(s, r"Chacun réalise (\d+) dessins", i)
        anciens = entier(s, r"possède également (\d+) dessins", i)
        abimes = entier(s, r"- (\d+) dessins sont écartés", i)
        reserves = entier(s, r"- (\d+) dessins sont réservés", i)
        capacite = entier(s, r"au maximum (\d+) dessins", i)
        nouveaux = eleves * par_eleve
        disponibles = nouveaux + anciens - abimes - reserves
        complets, reste = divmod(disponibles, capacite)
        self.assertGreater(reste, 0, "P8-M02 : dernier panneau censé être incomplet")
        self.verifier_resultats(ex, {
            "r1": nouveaux, "r2": disponibles, "r3": complets,
            "r4": reste, "r5": complets + 1
        })

    def controler_p8_m03(self, ex):
        s, i = ex["enonce"], ex["id"]
        depart = entier(s, r"Au départ, il possède (\d+) pièces", i)
        missions = entier(s, r"termine (\d+) missions", i)
        par_mission = entier(s, r"gagne (\d+) pièces par mission", i)
        bonus = entier(s, r"bonus unique de (\d+) pièces", i)
        potions = entier(s, r"achète (\d+) potions", i)
        prix_potion = entier(s, r"potions à (\d+) pièces", i)
        cles = entier(s, r"- Acheter (\d+) clés", i)
        prix_cle = entier(s, r"clés à (\d+) pièces", i)
        coffres_a = entier(s, r"- ouvrir (\d+) coffres contenant chacun", i)
        gain_a = entier(s, r"coffres contenant chacun (\d+) pièces", i)
        entree_b = entier(s, r"- Payer (\d+) pièces pour entrer", i)
        # Deux occurrences "ouvrir ... coffres" : la seconde est le chemin B.
        coffres_b = entier(s, r"Chemin B[^\n]*[\s\S]*?- ouvrir (\d+) coffres", i)
        gain_b = entier(s, r"Chemin B[^\n]*[\s\S]*?coffres contenant chacun (\d+) pièces", i)
        commun = depart + missions * par_mission + bonus - potions * prix_potion
        solde_a = commun - cles * prix_cle + coffres_a * gain_a
        solde_b = commun - entree_b + coffres_b * gain_b
        self.assertNotEqual(solde_a, solde_b)
        self.verifier_resultats(ex, {
            "r1": commun, "r2": solde_a, "r3": solde_b,
            "r4": "A" if solde_a > solde_b else "B",
            "r5": abs(solde_a - solde_b)
        })

    def controler_p8_m04(self, ex):
        s, i = ex["enonce"], ex["id"]
        equipes = entier(s, r"(\d+) équipes participent", i)
        robots = entier(s, r"Chaque équipe possède (\d+) robots", i)
        par_robot = entier(s, r"a besoin de (\d+) batteries", i)
        reserve = entier(s, r"de (\d+) batteries de réserve", i)
        stock = entier(s, r"- (\d+) batteries en stock", i)
        anciennes_boites = entier(s, r"- (\d+) boîte(?:s)? de", i)
        capacite = entier(s, r"boîte(?:s)? de (\d+) batteries", i)
        abimees = entier(s, r"(\d+) batteries sont déclarées", i)
        prix_boite = entier(s, r"au prix de (\d+) € chacune", i)
        besoin = equipes * (robots * par_robot + reserve)
        utilisables = stock + anciennes_boites * capacite - abimees
        manque = besoin - utilisables
        self.assertGreater(manque, 0)
        boites = (manque + capacite - 1) // capacite
        reste = utilisables + boites * capacite - besoin
        self.assertGreaterEqual(reste, 0)
        self.assertLess(reste, capacite)
        self.verifier_resultats(ex, {
            "r1": besoin, "r2": utilisables, "r3": manque,
            "r4": boites, "r5": boites * prix_boite, "r6": reste
        })

    def controler_p8_m05(self, ex):
        s, i = ex["enonce"], ex["id"]
        equipes = entier(s, r"(\d+) équipes participent", i)
        postes = entier(s, r"comporte (\d+) postes", i)
        enveloppe = centimes(s, r"enveloppe coûte (\d+,\d{2}) €", i)
        pochette = centimes(s, r"pochette de matériel à (\d+,\d{2}) €", i)
        signalisation = centimes(s, r"signalisation du parcours coûte (\d+,\d{2}) €", i)
        budget = centimes(s, r"budget total de \*\*(\d+,\d{2}) €\*\*", i)
        souvenir = centimes(s, r"Chaque souvenir coûte (\d+,\d{2}) €", i)
        reserve = centimes(s, r"au moins \*\*(\d+,\d{2}) €\*\*", i)
        n_enveloppes = equipes * postes
        cout = n_enveloppes * enveloppe + equipes * pochette + signalisation
        disponible = budget - cout
        cadeaux = equipes * souvenir
        ecart = disponible - cadeaux - reserve
        self.verifier_resultats(ex, {
            "r1": n_enveloppes, "r2": cout / 100,
            "r3": disponible / 100, "r4": cadeaux / 100,
            "r5": "Oui" if ecart >= 0 else "Non", "r6": abs(ecart) / 100
        })

    def test_250_variantes_mathématiques_independantes(self):
        generateurs = {
            "P8-M01": (banque.generer_modele_p8_clubs, self.controler_p8_m01),
            "P8-M02": (banque.generer_modele_p8_manga, self.controler_p8_m02),
            "P8-M03": (banque.generer_modele_p8_jeu_video, self.controler_p8_m03),
            "P8-M04": (banque.generer_modele_p8_robotique, self.controler_p8_m04),
            "P8-M05": (banque.generer_modele_p8_jeu_piste, self.controler_p8_m05),
        }
        etat = random.getstate()
        try:
            for identifiant, (generateur, controle) in generateurs.items():
                for essai in range(VARIANTES_PAR_MODELE):
                    with self.subTest(modele=identifiant, essai=essai):
                        random.seed(200000 + essai)
                        exercice = generateur()
                        self.assertEqual(exercice["id"], identifiant)
                        controle(exercice)
        finally:
            random.setstate(etat)


if __name__ == "__main__":
    unittest.main(verbosity=2)
