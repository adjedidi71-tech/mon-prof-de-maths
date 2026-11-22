"""Contrats de la banque MathiCap actuelle (22 novembre 2026).

Ces tests suivent le niveau PEDAGOGIQUE de la série, pas le préfixe
historique P7/P8/P9 de l'identifiant (certains modèles sont reclassés).
Ils ne supposent pas une version rédactionnelle unique des énoncés.
"""
import math
import random
import re
import unittest
from collections import defaultdict

import banque_priorites as banque

CATALOGUE = {1: 26, 2: 24, 3: 26}  # catégories N7, N8, N9
NB_QUESTIONS = {1: 4, 2: 5, 3: 5}


def tirage_complet(niveau, seed):
    """Restaure le générateur global pour ne pas contaminer d'autres tests."""
    etat = random.getstate()
    try:
        random.seed(seed)
        return banque.generer_exercices_priorites(niveau, CATALOGUE[niveau])
    finally:
        random.setstate(etat)


class TestBanqueActuelle(unittest.TestCase):
    def test_catalogue_complet_et_reclassements(self):
        listes = {n: tirage_complet(n, 9000 + n) for n in CATALOGUE}
        for n, exercices in listes.items():
            self.assertEqual(len(exercices), CATALOGUE[n], f'Niveau {n}')
            self.assertEqual(len({x['id'] for x in exercices}), CATALOGUE[n])
            for x in exercices:
                self.assertEqual(x.get('mathicap_niveau_pedagogique'), n + 6)
        # Les modèles reclassés conservent leur identifiant historique.
        self.assertIn('P9-M01', {e['id'] for e in listes[2]})
        self.assertIn('P9-M13', {e['id'] for e in listes[2]})
        self.assertIn('P8-M03', {e['id'] for e in listes[3]})
        self.assertIn('P8-M05', {e['id'] for e in listes[3]})
        self.assertIn('P8-M06', {e['id'] for e in listes[3]})

    def test_structure_questions_et_reponses_sur_2280_exercices(self):
        for niveau in CATALOGUE:
            nombre = NB_QUESTIONS[niveau]
            for seed in range(30):
                for ex in tirage_complet(niveau, 100000 + seed):
                    with self.subTest(niveau=niveau, seed=seed, modele=ex['id']):
                        self.assertTrue(ex.get('titre', '').strip())
                        self.assertTrue(ex.get('enonce', '').strip())
                        self.assertTrue(ex.get('correction', '').strip())
                        self.assertIn('**Questions**', ex['enonce'])
                        lignes = re.findall(r'(?m)^([1-5])\.\s+', ex['enonce'])
                        self.assertEqual(lignes, [str(i) for i in range(1, nombre + 1)])
                        champs = ex['champs_reponse']
                        self.assertEqual(len(champs), nombre)
                        self.assertEqual([c.get('question') for c in champs], list(range(1, nombre + 1)))
                        self.assertEqual(len(set(c['id'] for c in champs)), nombre)
                        for champ in champs:
                            self.assertTrue(str(champ.get('libelle', '')).strip())
                            self.assertTrue(str(champ.get('mathicap_competence', '')).strip())
                            self.assertIn(champ['type'], ('nombre', 'choix'))
                            self.assertIn('attendu', champ)
                            if champ['type'] == 'nombre':
                                valeur = champ['attendu']
                                self.assertIsInstance(valeur, (int, float))
                                self.assertNotIsInstance(valeur, bool)
                                self.assertTrue(math.isfinite(valeur))
                            else:
                                self.assertIn(champ['attendu'], champ['options'])
                        self.assertNotIn('Correction non disponible', ex['correction'])

    def test_variation_de_tous_les_modeles(self):
        enonces = defaultdict(set)
        for niveau in CATALOGUE:
            for seed in range(16):
                for ex in tirage_complet(niveau, 280000 + seed * 7):
                    enonces[(niveau, ex['id'])].add(ex['enonce'])
        self.assertEqual(len(enonces), sum(CATALOGUE.values()))
        for cle, variantes in enonces.items():
            with self.subTest(modele=cle):
                self.assertGreaterEqual(len(variantes), 2, 'Modèle sans variation numérique')

    def test_historique_eviter_modeles_recents(self):
        for niveau in CATALOGUE:
            with self.subTest(niveau=niveau):
                premier = tirage_complet(niveau, 100 + niveau)[:5]
                historique = [x['id'] for x in premier]
                etat = random.getstate()
                try:
                    random.seed(900 + niveau)
                    suivants = banque.generer_exercices_priorites(
                        niveau, 5, historique_modeles=historique)
                finally:
                    random.setstate(etat)
                self.assertEqual(len(suivants), 5)
                self.assertFalse(set(historique).intersection({x['id'] for x in suivants}))

    def test_reproductibilite_des_tirages(self):
        for niveau in CATALOGUE:
            premier = tirage_complet(niveau, 700 + niveau)
            second = tirage_complet(niveau, 700 + niveau)
            self.assertEqual(premier, second, f'Graine non reproductible N{niveau + 6}')

    def test_arguments_invalides(self):
        for niveau in (0, 4, 7, 8, 9):
            with self.subTest(niveau=niveau):
                with self.assertRaises(ValueError):
                    banque.generer_exercices_priorites(niveau, 5)
        for niveau, capacite in CATALOGUE.items():
            for nombre in (0, capacite + 1, True, 2.5):
                with self.subTest(niveau=niveau, nombre=nombre):
                    with self.assertRaises(ValueError):
                        banque.generer_exercices_priorites(niveau, nombre)


if __name__ == '__main__':
    unittest.main()
