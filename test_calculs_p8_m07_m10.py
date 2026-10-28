"""Tests indépendants groupés : 200 variantes de chacun des modèles P8-M07 à P8-M10.

Utilisation : python -m unittest -v test_calculs_p8_m07_m10.py
Compatible avec la commande GitHub Actions : python -m unittest discover -p 'test_*.py' -v
"""

import re
import unittest
from decimal import Decimal

from banque_priorites import (
    generer_modele_p8_eau,
    generer_modele_p8_parcours,
    generer_modele_p8_boissons,
    generer_modele_p8_transport,
)


NB_VARIANTES = 200


def extraire(texte, motif):
    """Retourne les groupes capturés dans l'énoncé ; échoue clairement si le texte change."""
    trouve = re.search(motif, texte, flags=re.DOTALL)
    if trouve is None:
        raise AssertionError(f"Information introuvable dans l'énoncé : {motif}")
    return trouve.groups()


def nombre(texte):
    """Interprète exactement les valeurs écrites en notation française."""
    return Decimal(texte.replace(" ", "").replace(",", "."))


class TestCalculsP8M07M10(unittest.TestCase):
    def verifier(self, exercice, identifiant, attendus, dependances=None):
        self.assertEqual(exercice["id"], identifiant)
        champs = {c["id"]: c for c in exercice["champs_reponse"]}
        self.assertEqual(len(champs), len(exercice["champs_reponse"]))

        for cle, attendu in attendus.items():
            self.assertIn(cle, champs)
            reel = champs[cle]["attendu"]
            if isinstance(attendu, str):
                self.assertEqual(reel, attendu, msg=f"{identifiant}, {cle}")
            else:
                self.assertEqual(
                    nombre(str(reel)), attendu,
                    msg=f"{identifiant}, {cle}: attendu {attendu}, reçu {reel}",
                )

        if dependances is not None:
            champ_choix = next(c for c in champs.values() if c["type"] == "choix")
            self.assertEqual(champ_choix.get("dependances"), dependances)

    def test_p8_m07_economies_eau(self):
        situations = set()
        for seed in range(NB_VARIANTES):
            with self.subTest(modele="P8-M07", seed=seed):
                ex = generer_modele_p8_eau(seed=seed)
                texte = ex["enonce"]
                robinets, minutes, jours = map(int, extraire(
                    texte,
                    r"Dans [^\n]+, (\d+) robinets sont utilisés chacun (\d+) minutes "
                    r"par jour pendant (\d+) jours",
                ))
                ancien = nombre(extraire(
                    texte, r"chaque robinet laisse couler\s+([\d,]+) litre d'eau par minute"
                )[0])
                nouveau = nombre(extraire(
                    texte, r"chaque robinet laisse couler seulement\s+([\d,]+) litre par minute"
                )[0])
                objectif = nombre(extraire(
                    texte, r"\*\*([\d,]+) litres d'eau\*\*"
                )[0])
                duree = robinets * minutes * jours
                avant = duree * ancien
                apres = duree * nouveau
                economie = avant - apres
                choix = "Oui" if economie >= objectif else "Non"
                situations.add(choix)
                self.verifier(ex, "P8-M07", {
                    "r1": Decimal(duree), "r2": avant, "r3": apres,
                    "r4": economie, "r5": choix, "r6": abs(economie - objectif),
                }, ["r4"])
                texte_correction = ex["correction"]
                self.assertIn(f"Économies réalisées : {economie:.2f}".replace(".", ",") + " L", texte_correction)
                self.assertIn("**Expression complète :**", texte_correction)
                self.assertEqual(ex, generer_modele_p8_eau(seed=seed))
        self.assertEqual(situations, {"Oui", "Non"})

    def test_p8_m08_parcours(self):
        situations = set()
        for seed in range(NB_VARIANTES):
            with self.subTest(modele="P8-M08", seed=seed):
                ex = generer_modele_p8_parcours(seed=seed)
                texte = ex["enonce"]
                partie_a = nombre(extraire(texte, r"premier chemin de ([\d,]+) km")[0])
                partie_b = nombre(extraire(texte, r"second chemin de ([\d,]+) km")[0])
                tours = int(extraire(texte, r"\*\*(\d+) tours complets\*\*")[0])
                minutes_km = int(extraire(texte, r"de (\d+) minutes par kilomètre")[0])
                pause = int(extraire(texte, r"pause de (\d+) minutes")[0])
                limite = int(extraire(texte, r"\*\*(\d+) minutes au maximum\*\*")[0])
                distance_tour = partie_a + partie_b
                distance = distance_tour * tours
                marche = distance * minutes_km
                total = marche + (tours - 1) * pause
                choix = "Oui" if total <= limite else "Non"
                situations.add(choix)
                self.verifier(ex, "P8-M08", {
                    "r1": distance_tour, "r2": distance, "r3": marche,
                    "r4": total, "r5": choix, "r6": abs(total - limite),
                }, ["r4"])
                self.assertIn(f"= {total} minutes.", ex["correction"])
                self.assertIn("**Expression complète :**", ex["correction"])
                self.assertEqual(ex, generer_modele_p8_parcours(seed=seed))
        self.assertEqual(situations, {"Oui", "Non"})

    def test_p8_m09_boissons(self):
        for seed in range(NB_VARIANTES):
            with self.subTest(modele="P8-M09", seed=seed):
                ex = generer_modele_p8_boissons(seed=seed)
                texte = ex["enonce"]
                fruits = re.findall(r"- (\d+) cL de [^\n;]+;", texte)
                self.assertEqual(len(fruits), 2, "On attend deux jus de fruits")
                eau = int(extraire(texte, r"- (\d+) cL d'eau")[0])
                preparations = int(extraire(
                    texte, r"\*\*(\d+) préparations identiques\*\*"
                )[0])
                capacite = int(extraire(texte, r"bouteilles de (\d+) cL chacune")[0])
                par_preparation = sum(map(int, fruits)) + eau
                volume_cl = preparations * par_preparation
                quotient, reste = divmod(volume_cl, capacite)
                self.assertGreater(reste, 0)
                self.verifier(ex, "P8-M09", {
                    "r1": Decimal(par_preparation),
                    "r2": Decimal(volume_cl) / 100,
                    "r3": Decimal(quotient), "r4": Decimal(reste),
                    "r5": Decimal(quotient + 1),
                })
                self.assertIn(f"Quotient : {quotient} — Reste : {reste}", ex["correction"])
                self.assertIn("**Expression complète :**", ex["correction"])
                self.assertEqual(ex, generer_modele_p8_boissons(seed=seed))

    def test_p8_m10_transport(self):
        gagnants = set()
        for seed in range(NB_VARIANTES):
            with self.subTest(modele="P8-M10", seed=seed):
                ex = generer_modele_p8_transport(seed=seed)
                texte = ex["enonce"]
                aller = int(extraire(texte, r"se trouve à (\d+) km du collège")[0])
                detour = int(extraire(texte, r"détour supplémentaire de (\d+) km")[0])
                fixe_a, km_a = map(int, extraire(
                    texte,
                    r"\*\*Entreprise A\*\*.*?Frais fixes : (\d+) €.*?"
                    r"Prix par kilomètre parcouru : (\d+) €",
                ))
                fixe_b, km_b = map(int, extraire(
                    texte,
                    r"\*\*Entreprise B\*\*.*?Frais fixes : (\d+) €.*?"
                    r"Prix par kilomètre parcouru : (\d+) €",
                ))
                distance = aller * 2 + detour
                cout_a = fixe_a + distance * km_a
                cout_b = fixe_b + distance * km_b
                self.assertNotEqual(cout_a, cout_b)
                self.assertTrue(3 <= abs(cout_a - cout_b) <= 60)
                meilleur = "A" if cout_a < cout_b else "B"
                gagnants.add(meilleur)
                self.verifier(ex, "P8-M10", {
                    "r1": Decimal(distance), "r2": Decimal(cout_a),
                    "r3": Decimal(cout_b), "r4": meilleur,
                    "r5": Decimal(abs(cout_a - cout_b)),
                }, ["r2", "r3"])
                self.assertIn(f"Entreprise A : {cout_a} €", ex["correction"])
                self.assertIn(f"Entreprise B : {cout_b} €", ex["correction"])
                self.assertIn("**Expression complète :**", ex["correction"])
                self.assertEqual(ex, generer_modele_p8_transport(seed=seed))
        self.assertEqual(gagnants, {"A", "B"})


if __name__ == "__main__":
    unittest.main()
