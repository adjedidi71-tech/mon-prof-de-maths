"""Tests automatiques de Mon Prof de Maths — chapitre 1, niveaux 7 et 8.

Lancement : python -m unittest -v test_banque_priorites.py
Aucune dépendance externe nécessaire.
"""
import math
import re
import unittest

import banque_priorites as banque


MODELES = {
    "generer_modele_p7_sciences": "P7-M01",
    "generer_modele_p7_patisserie": "P7-M02",
    "generer_modele_p7_enigmes": "P7-M03",
    "generer_modele_p7_photos": "P7-M04",
    "generer_modele_p7_velo": "P7-M05",
    "generer_modele_p7_fete": "P7-M06",
    "generer_modele_p7_cartes": "P7-M07",
    "generer_modele_p7_badminton": "P7-M08",
    "generer_modele_p7_jeu_video": "P7-M09",
    "generer_modele_p7_dessin": "P7-M10",
    "generer_modele_p7_tables_dessin": "P7-M11",
    "generer_modele_p8_clubs": "P8-M01",
    "generer_modele_p8_manga": "P8-M02",
    "generer_modele_p8_jeu_video": "P8-M03",
    "generer_modele_p8_robotique": "P8-M04",
    "generer_modele_p8_jeu_piste": "P8-M05",
    "generer_modele_p8_kits": "P8-M06",
}

# Dépendances pédagogiques explicites pour les questions à choix.
DEPENDANCES_ATTENDUES = {
    ("P8-M03", "r4"): ["r2", "r3"],
    ("P8-M05", "r5"): ["r3", "r4"],
    ("P8-M06", "r4"): ["r3"],
}


def nombre_dans_enonce(motif, enonce):
    resultat = re.search(motif, enonce)
    if resultat is None:
        raise AssertionError(f"Motif introuvable dans l'énoncé : {motif}")
    return int(resultat.group(1))


class TestsBanque(unittest.TestCase):
    def verifier_structure(self, exercice, identifiant):
        self.assertEqual(exercice["id"], identifiant)
        for cle in ("titre", "enonce", "correction"):
            self.assertIsInstance(exercice[cle], str)
            self.assertTrue(exercice[cle].strip(), f"{identifiant}: {cle} vide")

        champs = exercice["champs_reponse"]
        self.assertIsInstance(champs, list)
        self.assertTrue(champs, f"{identifiant}: aucune réponse")
        ids = [champ["id"] for champ in champs]
        self.assertEqual(len(ids), len(set(ids)), f"{identifiant}: identifiants dupliqués")
        par_id = {champ["id"]: champ for champ in champs}

        for champ in champs:
            self.assertIn(champ["type"], ("nombre", "choix", "texte_libre"))
            self.assertIn("question", champ)
            self.assertTrue(champ["libelle"].strip())
            if champ["type"] == "nombre":
                attendu = champ["attendu"]
                self.assertIsInstance(attendu, (int, float))
                self.assertTrue(math.isfinite(attendu))
            if champ["type"] == "choix":
                self.assertIn(champ["attendu"], champ["options"])
                dependances = champ.get("dependances", [])
                self.assertEqual(len(dependances), len(set(dependances)))
                for dep in dependances:
                    self.assertIn(dep, par_id, f"{identifiant}: dépendance inconnue {dep}")
                    self.assertEqual(par_id[dep]["type"], "nombre")
                regle = DEPENDANCES_ATTENDUES.get((identifiant, champ["id"]))
                if regle is not None:
                    self.assertEqual(dependances, regle,
                                     f"{identifiant}: dépendances pédagogiques incorrectes")

    def test_chaque_modele_50_variantes(self):
        # 17 modèles x 50 variantes = 850 contrôles de structure.
        for nom, identifiant in MODELES.items():
            self.assertTrue(hasattr(banque, nom), f"Fonction absente : {nom}")
            for essai in range(50):
                with self.subTest(modele=identifiant, essai=essai):
                    exercice = getattr(banque, nom)()
                    self.verifier_structure(exercice, identifiant)

    def test_series_aleatoires(self):
        # Contrôle des séries de 5 exercices et absence d'anciens fixes.
        for niveau in (1, 2):
            for _ in range(30):
                exercices = banque.generer_exercices_priorites(niveau, 5)
                self.assertEqual(len(exercices), 5)
                ids = [e["id"] for e in exercices]
                self.assertEqual(len(ids), len(set(ids)))
                prefixe = "P7-M" if niveau == 1 else "P8-M"
                self.assertTrue(all(i.startswith(prefixe) for i in ids), ids)

    def test_kits_seed_reproductible(self):
        for seed in (1, 42, 12345, 20261027):
            premier = banque.generer_modele_p8_kits(seed=seed)
            second = banque.generer_modele_p8_kits(seed=seed)
            self.assertEqual(premier, second)
            self.assertEqual(premier["seed"], seed)

    def test_kits_300_calculs_independants(self):
        # Calculs recalculés à partir de l'énoncé, indépendamment des réponses générées.
        for seed in range(300):
            with self.subTest(seed=seed):
                exercice = banque.generer_modele_p8_kits(seed=seed)
                enonce = exercice["enonce"]
                equipes = nombre_dans_enonce(r"Il y a (\d+) équipes", enonce)
                articles = re.findall(
                    r"(?m)^- (\d+) [^\n]+? à (\d+) € l'unité", enonce
                )
                self.assertEqual(len(articles), 2, "Articles introuvables")
                prix_kit = sum(int(q) * int(p) for q, p in articles)
                prix_tous = equipes * prix_kit
                reduction = nombre_dans_enonce(r"réduction de (\d+) €", enonce)
                livraison = nombre_dans_enonce(r"frais de livraison sont de (\d+) €", enonce)
                budget = nombre_dans_enonce(r"budget de \*\*(\d+) €\*\*", enonce)
                total = prix_tous - reduction + livraison
                attendus = {c["id"]: c["attendu"] for c in exercice["champs_reponse"]}
                self.assertLessEqual(reduction, prix_tous)
                self.assertGreaterEqual(total, 0)
                self.assertEqual(attendus["r1"], prix_kit)
                self.assertEqual(attendus["r2"], prix_tous)
                self.assertEqual(attendus["r3"], total)
                self.assertEqual(attendus["r4"], "Oui" if budget >= total else "Non")
                self.assertEqual(attendus["r5"], abs(budget - total))
                self.assertIn(f"= {total} €", exercice["correction"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
