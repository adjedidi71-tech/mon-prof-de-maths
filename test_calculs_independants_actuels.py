"""Recalculs indépendants depuis l'énoncé de trois modèles représentatifs.

L'objectif est de compléter, et non remplacer, les contrôles structurels.
Ces vérifications ne lisent aucun chiffre dans la correction calculée.
"""
import random
import re
import unittest
import banque_priorites as banque


def capturer(texte, motif):
    m = re.search(motif, texte, re.IGNORECASE | re.DOTALL)
    if not m:
        raise AssertionError(f'Donnée introuvable : {motif}\n{texte[:900]}')
    return tuple(int(g) for g in m.groups())


def attendus(exercice):
    return [x['attendu'] for x in exercice['champs_reponse']]


class TestCalculsIndependantsActuels(unittest.TestCase):
    def test_n7_badminton_100_tirages(self):
        for graine in range(100):
            random.seed(4100 + graine)
            ex = banque.generer_modele_p7_badminton()
            s = ex['enonce']
            (initial,) = capturer(s, r'possède déjà (\d+) volants')
            boites, capacite = capturer(s, r'achète (\d+) boîtes? de (\d+) volants')
            (abimes,) = capturer(s, r'(\d+) volants sont déclarés abîmés')
            (matchs,) = capturer(s, r'comporte (\d+) matchs')
            (par_match,) = capturer(s, r'utiliser (\d+) volants pour chacun')
            achetes = boites * capacite
            disponibles = initial + achetes - abimes
            necessaires = matchs * par_match
            with self.subTest(graine=graine):
                self.assertEqual(attendus(ex), [achetes, disponibles, necessaires,
                    abs(disponibles - necessaires)])

    def test_n8_transport_100_tirages(self):
        for graine in range(100):
            random.seed(8100 + graine)
            ex = banque.generer_modele_p8_transport()
            s = ex['enonce']
            (distance,) = capturer(s, r'se trouve à (\d+) km du collège')
            (detour,) = capturer(s, r'un seul détour ajoute (\d+) km')
            loc_a, prix_a = capturer(s, r'Entreprise A.*?Frais fixes : (\d+) €.*?kilomètre parcouru : (\d+) €')
            loc_b, prix_b = capturer(s, r'Entreprise B.*?Frais fixes : (\d+) €.*?kilomètre parcouru : (\d+) €')
            changement = re.search(r'entreprise ([AB]) augmente ses frais fixes de (\d+) €', s)
            self.assertIsNotNone(changement)
            entreprise, montant = changement.groups()
            augmentation = int(montant)
            total = 2 * distance + detour
            cout_a = loc_a + total * prix_a
            cout_b = loc_b + total * prix_b
            cout_a_apres = cout_a + (augmentation if entreprise == 'A' else 0)
            cout_b_apres = cout_b + (augmentation if entreprise == 'B' else 0)
            with self.subTest(graine=graine):
                self.assertEqual(attendus(ex), [total, cout_a, cout_b,
                    'A' if cout_a < cout_b else 'B', cout_a_apres - cout_b_apres])

    def test_n9_tournoi_100_tirages(self):
        for graine in range(100):
            random.seed(9100 + graine)
            ex = banque.generer_modele_p9_tournoi()
            s = ex['enonce']
            (joueurs,) = capturer(s, r'\*\*(\d+) joueurs\*\* participent')
            (inscription,) = capturer(s, r'chacun \*\*(\d+) €\*\* d.inscription')
            (don,) = capturer(s, r'partenaire offre \*\*(\d+) €\*\*')
            (recompenses,) = capturer(s, r'récompenses coûtent \*\*(\d+) €\*\*')
            loc_a, cout_a = capturer(s, r'Organisateur A.*?Location : (\d+) €.*?Fournitures : (\d+) €')
            loc_b, cout_b = capturer(s, r'Organisateur B.*?Location : (\d+) €.*?Fournitures : (\d+) €')
            (pub,) = capturer(s, r'publicité à (\d+) €')
            (nouveaux,) = capturer(s, r'accueillir (\d+) joueurs supplémentaires')
            recettes = joueurs * inscription + don
            ba = recettes - recompenses - loc_a - joueurs * cout_a
            bb = recettes - recompenses - loc_b - joueurs * cout_b
            apres_a = recettes + nouveaux * inscription - recompenses - pub - loc_a - (joueurs + nouveaux) * cout_a
            apres_b = recettes + nouveaux * inscription - recompenses - pub - loc_b - (joueurs + nouveaux) * cout_b
            with self.subTest(graine=graine):
                self.assertEqual(attendus(ex), [recettes, ba, bb, abs(ba - bb),
                    max(ba, bb, apres_a, apres_b)])


if __name__ == '__main__':
    unittest.main()
