"""Tests mathématiques du niveau 7 — Mon Prof de Maths.

À déposer à la racine du dépôt GitHub.
Exécution : python -m unittest -v test_calculs_niveau7.py
Le workflow existant (unittest discover -p 'test_*.py') le découvrira.

Contrôles :
- 50 variantes de chacun des 11 modèles (équations numériques des corrections) ;
- variation effective des énoncés ;
- recalcul indépendant à partir de l'énoncé pour P7-M07 à P7-M11.

Pour les autres modèles, les égalités vérifiées dans la correction ne sont
pas encore un recalcul indépendant depuis l'énoncé.
"""

import ast
from decimal import Decimal
import random
import re
import unittest

import banque_priorites as banque


MODELES_N7 = {
    "P7-M01": "generer_modele_p7_sciences",
    "P7-M02": "generer_modele_p7_patisserie",
    "P7-M03": "generer_modele_p7_enigmes",
    "P7-M04": "generer_modele_p7_photos",
    "P7-M05": "generer_modele_p7_velo",
    "P7-M06": "generer_modele_p7_fete",
    "P7-M07": "generer_modele_p7_cartes",
    "P7-M08": "generer_modele_p7_badminton",
    "P7-M09": "generer_modele_p7_jeu_video",
    "P7-M10": "generer_modele_p7_dessin",
    "P7-M11": "generer_modele_p7_tables_dessin",
}

VARIANTES = 50


def _expr_decimal(chaine):
    """Calcule uniquement +, -, *, / et des parenthèses ; aucun eval()."""
    chaine = chaine.strip().replace("×", "*").replace("÷", "/")
    chaine = chaine.replace("−", "-").replace("–", "-")
    chaine = re.sub(r"(?<=\d),(?=\d)", ".", chaine)
    chaine = chaine.replace(":", "/")
    chaine = chaine.rstrip(". ")
    if not chaine or not re.fullmatch(r"[0-9.() +*/-]+", chaine):
        raise ValueError("Expression non numérique")

    noeud = ast.parse(chaine, mode="eval").body

    def calculer(n):
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            return Decimal(str(n.value))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            valeur = calculer(n.operand)
            return valeur if isinstance(n.op, ast.UAdd) else -valeur
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            gauche, droite = calculer(n.left), calculer(n.right)
            if isinstance(n.op, ast.Add):
                return gauche + droite
            if isinstance(n.op, ast.Sub):
                return gauche - droite
            if isinstance(n.op, ast.Mult):
                return gauche * droite
            if droite == 0:
                raise ValueError("Division par zéro")
            return gauche / droite
        raise ValueError("Opération non prise en charge")

    return calculer(noeud)


def _egalites_verifiables(correction):
    """Extrait les égalités entièrement numériques, même avec × et −."""
    motif = re.compile(
        r"([\d(][\d() .,+\-−–×÷*/:]*?)\s*=\s*"
        r"([\d(][\d() .,+\-−–×÷*/:]*)"
    )
    for ligne in correction.splitlines():
        for resultat in motif.finditer(ligne):
            gauche, droite = resultat.group(1).strip(), resultat.group(2).strip()
            try:
                valeur_gauche = _expr_decimal(gauche)
                valeur_droite = _expr_decimal(droite)
            except (ValueError, SyntaxError, ArithmeticError, OverflowError):
                continue
            yield (gauche, droite, valeur_gauche, valeur_droite)


def _extraire(texte, motif, identifiant):
    resultat = re.search(motif, texte, flags=re.IGNORECASE | re.DOTALL)
    if resultat is None:
        raise AssertionError(
            f"{identifiant} : information introuvable dans l'énoncé : {motif}"
        )
    return tuple(int(x) for x in resultat.groups())


def _attendus(exercice):
    return {
        champ["id"]: champ["attendu"]
        for champ in exercice["champs_reponse"]
        if champ["type"] != "texte_libre"
    }


class TestsCalculsNiveau7(unittest.TestCase):
    def verifier_reponses(self, exercice, valeurs):
        attendus = _attendus(exercice)
        identifiant = exercice["id"]
        for champ, valeur in valeurs.items():
            self.assertIn(champ, attendus, f"{identifiant}: champ {champ} introuvable")
            self.assertEqual(attendus[champ], valeur,
                             f"{identifiant}/{champ} : réponse attendue incorrecte")

    def test_550_variantes_equations_et_diversite(self):
        """11 modèles × 50 tirages : corrections numériques et diversité."""
        etat = random.getstate()
        try:
            for rang, (identifiant, nom) in enumerate(MODELES_N7.items()):
                generateur = getattr(banque, nom)
                enonces = set()
                for essai in range(VARIANTES):
                    with self.subTest(modele=identifiant, essai=essai):
                        random.seed(710000 + rang * 1000 + essai)
                        ex = generateur()
                        self.assertEqual(ex["id"], identifiant)
                        enonces.add(ex["enonce"])
                        egalites = list(_egalites_verifiables(ex["correction"]))
                        self.assertGreater(
                            len(egalites), 0,
                            f"{identifiant} : aucune égalité numérique reconnue"
                        )
                        for gauche, droite, valeur_g, valeur_d in egalites:
                            self.assertLessEqual(
                                abs(valeur_g - valeur_d), Decimal("0.000001"),
                                f"{identifiant} : calcul faux : {gauche} = {droite}"
                            )
                self.assertGreater(
                    len(enonces), 1,
                    f"{identifiant} : les 50 générations produisent le même énoncé"
                )
        finally:
            random.setstate(etat)

    def test_p7_m07_cartes_doublons_pairs(self):
        """Un échange de deux doublons impose un nombre pair de doublons."""
        generateur = banque.generer_modele_p7_cartes
        for essai in range(VARIANTES):
            with self.subTest(essai=essai):
                ex = generateur()
                (doublons,) = _extraire(
                    ex["enonce"], r"Parmi les cartes achetées,\s*(\d+)\s+sont des doublons",
                    "P7-M07"
                )
                self.assertGreater(doublons, 0)
                self.assertEqual(doublons % 2, 0, "P7-M07 : doublons impairs")

    def test_p7_m08_badminton_recalcul_depuis_enonce(self):
        for essai in range(VARIANTES):
            with self.subTest(essai=essai):
                ex = banque.generer_modele_p7_badminton()
                s = ex["enonce"]
                (initial,) = _extraire(s, r"possède déjà\s+(\d+)\s+volants", "P7-M08")
                boites, capacite = _extraire(
                    s, r"achète\s+(\d+)\s+boîtes?\s+de\s+(\d+)\s+volants", "P7-M08"
                )
                (abimes,) = _extraire(s, r"(\d+)\s+volants sont déclarés abîmés", "P7-M08")
                (matchs,) = _extraire(s, r"(\d+)\s+matchs", "P7-M08")
                (par_match,) = _extraire(s, r"prévision de\s+(\d+)\s+volants utilisés par match", "P7-M08")
                achetes = boites * capacite
                utilisables = initial + achetes - abimes
                necessaires = matchs * par_match
                assez = utilisables >= necessaires
                self.verifier_reponses(ex, {
                    "r1": achetes, "r2": utilisables, "r3": necessaires,
                    "r4": "Oui" if assez else "Non", "r5": abs(utilisables - necessaires)
                })

    def test_p7_m09_jeu_video_recalcul_depuis_enonce(self):
        for essai in range(VARIANTES):
            with self.subTest(essai=essai):
                ex = banque.generer_modele_p7_jeu_video()
                s = ex["enonce"]
                (depart,) = _extraire(s, r"possède au départ\s+(\d+)\s+pièces", "P7-M09")
                niveaux, gain = _extraire(s, r"termine\s+(\d+)\s+niveaux et gagne\s+(\d+)\s+pièces", "P7-M09")
                (bonus,) = _extraire(s, r"bonus unique de\s+(\d+)\s+pièces", "P7-M09")
                potions, prix = _extraire(s, r"achète\s+(\d+)\s+potions à\s+(\d+)\s+pièces", "P7-M09")
                (perdues,) = _extraire(s, r"perd\s+(\d+)\s+pièces", "P7-M09")
                (equipement,) = _extraire(s, r"vendu\s+(\d+)\s+pièces", "P7-M09")
                gains = niveaux * gain + bonus
                depenses = potions * prix + perdues
                solde = depart + gains - depenses
                self.verifier_reponses(ex, {
                    "r1": gains, "r2": depenses, "r3": solde,
                    "r4": "Oui" if solde >= equipement else "Non",
                    "r5": abs(solde - equipement)
                })

    def test_p7_m10_dessin_recalcul_depuis_enonce(self):
        for essai in range(VARIANTES):
            with self.subTest(essai=essai):
                ex = banque.generer_modele_p7_dessin()
                s = ex["enonce"]
                (depart,) = _extraire(s, r"possède déjà\s+(\d+)\s+feuilles", "P7-M10")
                paquets, capacite = _extraire(s, r"achète\s+(\d+)\s+paquets contenant chacun\s+(\d+)\s+feuilles", "P7-M10")
                (abimees,) = _extraire(s, r"(\d+)\s+feuilles sont abîmées", "P7-M10")
                (groupes,) = _extraire(s, r"-\s*(\d+)\s+groupes participent", "P7-M10")
                (eleves,) = _extraire(s, r"chaque groupe comporte\s+(\d+)\s+élèves", "P7-M10")
                (par_eleve,) = _extraire(s, r"chaque élève utilise\s+(\d+)\s+feuilles", "P7-M10")
                (exposition,) = _extraire(s, r"nécessitant\s+(\d+)\s+feuilles supplémentaires", "P7-M10")
                achetees = paquets * capacite
                utilisees = groupes * eleves * par_eleve
                reste = depart + achetees - abimees - utilisees
                self.assertGreaterEqual(reste, 0)
                self.verifier_reponses(ex, {
                    "r1": achetees, "r2": utilisees, "r3": reste,
                    "r4": "Oui" if reste >= exposition else "Non",
                    "r5": abs(reste - exposition)
                })

    def test_p7_m11_tables_dessin_recalcul_depuis_enonce(self):
        for essai in range(VARIANTES):
            with self.subTest(essai=essai):
                ex = banque.generer_modele_p7_tables_dessin()
                s = ex["enonce"]
                tables, eleves = _extraire(s, r"avec\s+(\d+)\s+tables de\s+(\d+)\s+élèves chacune", "P7-M11")
                (par_eleve,) = _extraire(s, r"-\s*(\d+)\s+feuilles de papier pour chaque élève", "P7-M11")
                (essai_feuilles,) = _extraire(s, r"-\s*(\d+)\s+feuilles? supplémentaires?", "P7-M11")
                (initial,) = _extraire(s, r"dispose de\s+(\d+)\s+feuilles au départ", "P7-M11")
                par_table = eleves * par_eleve + essai_feuilles
                total = tables * par_table
                self.verifier_reponses(ex, {
                    "r1": par_table, "r2": total, "r3": initial - total
                })


if __name__ == "__main__":
    unittest.main(verbosity=2)
