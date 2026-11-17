"""Tests reproductibles pour la banque de problèmes MathiCap V3."""
import importlib.util
import random
import math
import re
import unittest
from collections import Counter
from pathlib import Path

SOURCE = Path(__file__).with_name('banque_priorites.py')
spec = importlib.util.spec_from_file_location('mathicap_banque_v3', SOURCE)
banque = importlib.util.module_from_spec(spec)
spec.loader.exec_module(banque)
GENERATEURS = {name: getattr(banque, name) for name in dir(banque)
               if name.startswith('generer_modele_p')}

class TestMathicapV3(unittest.TestCase):
    def test_structure_catalogue(self):
        self.assertEqual(len(GENERATEURS), 46)
        self.assertEqual({i: len(banque.generer_exercices_priorites(i,5)) for i in (1,2,3)}, {1:5,2:5,3:5})
        for name,fn in GENERATEURS.items():
            ex=fn()
            self.assertRegex(ex['id'],r'^P[789]-M\d\d$')

    def test_variantes_qa(self):
        n=1400
        counts=Counter()
        for nom, gen in GENERATEURS.items():
            for i in range(n):
                if nom.startswith('generer_modele_p9_'):
                    ex=gen(seed=i+73000)
                else:
                    random.seed((i+17000)*37)
                    ex=gen()
                original_id=ex['id']
                level=int(original_id[1])
                attendu_n=4 if level==7 else 5
                self.assertEqual(len(ex['champs_reponse']), attendu_n, f'{original_id} fields')
                qs=ex['enonce'].split('**Questions**')
                self.assertEqual(len(qs),2, f'{original_id} questions delimiter')
                numbered=re.findall(r'(?m)^([1-5])\.\s+',qs[1])
                self.assertEqual(numbered,list(map(str,range(1,attendu_n+1))),f'{original_id} question numbers')
                self.assertTrue(ex.get('correction','').strip(),original_id)
                self.assertNotIn('Exercices à développer',ex['enonce'])
                self.assertNotIn('Correction non disponible',ex['correction'])
                self.assertEqual(ex.get('mathicap_revision_pedagogique'),'v3.0')
                self.assertEqual(ex.get('mathicap_questions_uniformisees'),3)
                for num,ch in enumerate(ex['champs_reponse'],1):
                    self.assertEqual(ch['question'],num, f'{original_id} ch {ch}')
                    self.assertIn(ch['type'],('nombre','choix'))
                    self.assertIn('attendu',ch)
                    self.assertNotIn('dependances',ch)
                    self.assertIsInstance(ch.get('mathicap_competence'),str)
                    self.assertTrue(ch['mathicap_competence'])
                    v=ch['attendu']
                    if ch['type']=='nombre':
                        self.assertIsInstance(v,(int,float), f'{original_id}/{num} {v}')
                        self.assertTrue(math.isfinite(v), f'{original_id}/{num}')
                    else:
                        self.assertTrue(isinstance(v,str) and v.strip(), f'{original_id}/{num}')
                counts[original_id]+=1
                if original_id=='P9-M06':
                    self.assertIn('Nouveau défi',ex['enonce'])
                    self.assertIn('solde de places',ex['enonce'])
                if original_id=='P9-M09':
                    self.assertNotIn('0 hélices sont inutilisables',ex['enonce'])
                    self.assertNotIn('1 batteries défectueuses',ex['enonce'])
                    self.assertIn('boîtes entières',ex['enonce'])
                    self.assertGreater(ex['champs_reponse'][-1]['attendu'],0)
                if original_id=='P9-M02':
                    self.assertIn('bénéfice minimal',ex['enonce'])
                    self.assertIn('joueurs supplémentaires',ex['enonce'])
                    self.assertGreater(ex['champs_reponse'][-1]['attendu'],0)
        self.assertEqual(len(counts),46)

    def test_diversite_tarifs_tournoi(self):
        gagnants=Counter()
        for seed in range(2000):
            e=banque.generer_modele_p9_tournoi(seed)
            x=re.search(r'Organisateur A.*?Location : (\d+) €.*?Fournitures : (\d+) €',e['enonce'], re.S)
            y=re.search(r'Organisateur B.*?Location : (\d+) €.*?Fournitures : (\d+) €',e['enonce'], re.S)
            self.assertIsNotNone(x);self.assertIsNotNone(y)
            la,pa=map(int,x.groups());lb,pb=map(int,y.groups())
            self.assertTrue(la<lb and pa>pb)
            gagnants['A' if e['champs_reponse'][1]['attendu']>e['champs_reponse'][2]['attendu'] else 'B']+=1
        self.assertGreater(gagnants['A'],100)
        self.assertGreater(gagnants['B'],100)

    def test_banque_et_historique(self):
        for niveau, nombre in [(1,5),(2,5),(3,5)]:
            li=banque.generer_exercices_priorites(niveau,nombre)
            self.assertEqual(len({e['id'] for e in li}),nombre)
            hist=[e['id'] for e in li][:5]
            extrait=banque.generer_exercices_priorites(niveau,3,historique_modeles=hist)
            self.assertEqual(len(extrait),3)
            self.assertTrue(all(e['id'] not in hist for e in extrait))

if __name__=='__main__':
    unittest.main(verbosity=2)
