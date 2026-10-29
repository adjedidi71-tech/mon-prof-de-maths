
import re
import unittest

from banque_priorites import (
    generer_modele_p9_potager,
    generer_modele_p9_tournoi,
    generer_modele_p9_festival,
    generer_modele_p9_cristaux,
    generer_modele_p9_bibliotheque,
    generer_modele_p9_spectacle,
    generer_modele_p9_recyclage,
    generer_modele_p9_salles,
    generer_modele_p9_drones,
    generer_modele_p9_mosaique,
)

NB_TIRAGES = 200


def nombres(texte, motif):
    correspondance = re.search(motif, texte, flags=re.DOTALL)
    if correspondance is None:
        raise AssertionError(
            f"Donnee introuvable dans l'enonce : {motif}"
        )
    valeurs = tuple(int(x) for x in correspondance.groups())
    return valeurs[0] if len(valeurs) == 1 else valeurs


class TestsCalculsNiveau9(unittest.TestCase):

    def verifier(
        self, exercice, identifiant, seed, resultats,
        dependances=None
    ):
        self.assertEqual(exercice["id"], identifiant)
        self.assertEqual(exercice["seed"], seed)
        self.assertTrue(exercice["enonce"])
        self.assertTrue(exercice["correction"])

        champs = exercice["champs_reponse"]
        ids = [champ["id"] for champ in champs]
        self.assertEqual(len(ids), len(set(ids)))

        par_id = {champ["id"]: champ for champ in champs}

        for id_champ, valeur in resultats.items():
            self.assertIn(id_champ, par_id)
            self.assertEqual(
                par_id[id_champ]["attendu"],
                valeur,
                f"{identifiant}, seed={seed}, champ={id_champ}"
            )

        for champ in champs:
            if champ["type"] == "texte_libre":
                self.assertNotIn("attendu", champ)

            if champ["type"] == "choix":
                self.assertIn(champ["attendu"], champ["options"])
                regle = (
                    dependances.get(champ["id"], [])
                    if isinstance(dependances, dict)
                    else (dependances or [])
                )

                self.assertEqual(
                    champ.get("dependances", []),
                    regle,
                    f"Dependances incorrectes : {identifiant}"
                )
                for autre in regle:
                    self.assertIn(autre, par_id)
                    self.assertEqual(par_id[autre]["type"], "nombre")

    def test_p9_m01_potager(self):
        choix_observes = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_potager(seed=seed)
            t = e["enonce"]

            n = nombres(
                t, r"prépare \*\*(\d+) parcelles identiques\*\*"
            )
            pa, prix_a, mat_a = nombres(
                t,
                r"\*\*Projet A\*\*.*?"
                r"(\d+) plants par parcelle, à (\d+) € le plant ;"
                r".*?(\d+) € de matériel complémentaire"
            )
            pb, prix_b, mat_b = nombres(
                t,
                r"\*\*Projet B\*\*.*?"
                r"(\d+) plants par parcelle, à (\d+) € le plant ;"
                r".*?(\d+) € de matériel complémentaire"
            )
            budget = nombres(
                t, r"budget disponible est de \*\*(\d+) €\*\*"
            )

            qa, qb = n * pa, n * pb
            ca = qa * prix_a + mat_a
            cb = qb * prix_b + mat_b

            self.assertNotEqual(ca, cb)
            self.assertGreaterEqual(budget, max(ca, cb))

            choix = "A" if ca < cb else "B"
            choix_observes.add(choix)

            self.verifier(e, "P9-M01", seed, {
                "r1": qa, "r2": qb,
                "r3": ca, "r4": cb,
                "r5": choix, "r6": abs(ca - cb),
                "r7": budget - min(ca, cb)
            }, ["r3", "r4"])

            self.assertEqual(
                e, generer_modele_p9_potager(seed=seed)
            )

        self.assertEqual(choix_observes, {"A", "B"})

    def test_p9_m02_tournoi(self):
        choix_observes = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_tournoi(seed=seed)
            t = e["enonce"]

            joueurs, entree, sponsor = nombres(
                t,
                r"\*\*(\d+) joueurs\*\*.*?"
                r"\*\*(\d+) €\*\* d.inscription"
                r".*?\*\*(\d+) €\*\* au club"
            )
            recompenses = nombres(
                t, r"récompenses coûtent \*\*(\d+) €\*\*"
            )
            location_a, par_joueur_a = nombres(
                t,
                r"\*\*Organisation A\*\*.*?"
                r"Location : (\d+) € ;.*?"
                r"Fournitures : (\d+) € par joueur"
            )
            location_b, par_joueur_b = nombres(
                t,
                r"\*\*Organisation B\*\*.*?"
                r"Location : (\d+) € ;.*?"
                r"Fournitures : (\d+) € par joueur"
            )

            recettes = joueurs * entree + sponsor
            dep_a = recompenses + location_a + joueurs * par_joueur_a
            dep_b = recompenses + location_b + joueurs * par_joueur_b
            ben_a = recettes - dep_a
            ben_b = recettes - dep_b

            self.assertNotEqual(ben_a, ben_b)
            self.assertGreaterEqual(min(ben_a, ben_b), 0)

            choix = "A" if ben_a > ben_b else "B"
            choix_observes.add(choix)

            self.verifier(e, "P9-M02", seed, {
                "r1": recettes,
                "r2": dep_a, "r3": dep_b,
                "r4": ben_a, "r5": ben_b,
                "r6": choix, "r7": abs(ben_a - ben_b)
            }, ["r4", "r5"])

            self.assertEqual(
                e, generer_modele_p9_tournoi(seed=seed)
            )

        self.assertEqual(choix_observes, {"A", "B"})

    def test_p9_m03_festival(self):
        choix_observes = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_festival(seed=seed)
            t = e["enonce"]

            eleves, adultes, km_aller = nombres(
                t,
                r"\*\*(\d+) élèves\*\*.*?"
                r"\*\*(\d+) adultes\*\*.*?"
                r"\*\*(\d+) km\*\*"
            )
            billet, repas = nombres(
                t,
                r"Chaque personne paie (\d+) € d.entrée"
                r" au festival.*?(\d+) € pour le repas"
            )
            fixe_a, prix_km = nombres(
                t,
                r"\*\*Transport A\*\*.*?"
                r"Frais fixes : (\d+) € ;.*?"
                r"(\d+) € par kilomètre parcouru"
            )
            fixe_b, prix_personne = nombres(
                t,
                r"\*\*Transport B\*\*.*?"
                r"Frais fixes : (\d+) € ;.*?"
                r"(\d+) € par personne transportée"
            )

            personnes = eleves + adultes
            distance = 2 * km_aller
            commun = personnes * (billet + repas)
            cout_a = fixe_a + distance * prix_km + commun
            cout_b = fixe_b + personnes * prix_personne + commun

            self.assertNotEqual(cout_a, cout_b)

            choix = "A" if cout_a < cout_b else "B"
            choix_observes.add(choix)

            self.verifier(e, "P9-M03", seed, {
                "r1": personnes,
                "r2": distance,
                "r3": commun,
                "r4": cout_a, "r5": cout_b,
                "r6": choix,
                "r7": abs(cout_a - cout_b)
            }, ["r4", "r5"])

            self.assertEqual(
                e, generer_modele_p9_festival(seed=seed)
            )

        self.assertEqual(choix_observes, {"A", "B"})

    def test_p9_m04_cristaux(self):
        choix_observes = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_cristaux(seed=seed)
            t = e["enonce"]

            stock = nombres(
                t, r"possède \*\*(\d+) cristaux\*\* au départ"
            )
            missions, gain = nombres(
                t,
                r"\*\*(\d+) missions\*\*.*?"
                r"\*\*(\d+) cristaux\*\*"
            )
            bonus = nombres(
                t, r"bonus unique de \*\*(\d+) cristaux\*\*"
            )
            perte = nombres(
                t, r"perdre (\d+) cristaux"
            )
            prix = nombres(
                t, r"équipement coûte \*\*(\d+) cristaux\*\*"
            )
            reserve = nombres(
                t, r"au moins \*\*(\d+) cristaux\*\*"
            )
            aventuriers = nombres(
                t, r"comprend \*\*(\d+) aventuriers\*\*"
            )

            gains = missions * gain + bonus
            disponibles = stock + gains - perte
            maximum = (disponibles - reserve) // prix
            restant = disponibles - maximum * prix

            self.assertGreaterEqual(restant, reserve)
            self.assertLess(restant, reserve + prix)

            choix = "Oui" if maximum >= aventuriers else "Non"
            choix_observes.add(choix)

            self.verifier(e, "P9-M04", seed, {
                "r1": gains,
                "r2": disponibles,
                "r3": maximum,
                "r4": restant,
                "r5": choix,
                "r6": abs(maximum - aventuriers)
            }, ["r3"])

            self.assertEqual(
                e, generer_modele_p9_cristaux(seed=seed)
            )

        self.assertEqual(choix_observes, {"Oui", "Non"})

    def test_p9_m05_bibliotheque(self):
        signes = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_bibliotheque(seed=seed)
            t = e["enonce"]

            colis, par_colis = nombres(
                t,
                r"\*\*(\d+) colis\*\* de \*\*(\d+) mangas\*\*"
            )
            dons = nombres(
                t, r"puis \*\*(\d+) mangas\*\* offerts"
            )
            abimes = nombres(
                t, r"retire \*\*(\d+) mangas abîmés\*\*"
            )
            classes, par_classe = nombres(
                t,
                r"\*\*(\d+) classes\*\* empruntent chacune"
                r" \*\*(\d+) mangas\*\*"
            )
            final = nombres(
                t,
                r"\*\*(\d+) mangas"
                r"(?:\*\* sur les étagères| sur les étagères\*\*)"
            )

            recus = colis * par_colis
            pretes = classes * par_classe
            variation = recus + dons - abimes - pretes
            initial = final - variation
            apres_retour = final + pretes

            self.assertGreaterEqual(initial, 0)
            signes.add(
                "negatif" if variation < 0 else "positif"
            )

            self.verifier(e, "P9-M05", seed, {
                "r1": recus,
                "r2": pretes,
                "r3": variation,
                "r4": initial,
                "r5": apres_retour
            })

            self.assertEqual(
                e, generer_modele_p9_bibliotheque(seed=seed)
            )

        self.assertEqual(signes, {"positif", "negatif"})

    def test_p9_m06_spectacle(self):
        decisions = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_spectacle(seed=seed)
            t = e["enonce"]

            rangees, places, reservees = nombres(
                t,
                r"salle possède (\d+) rangées de "
                r"(\d+) places\. (\d+) places sont réservées"
            )
            eleves, tarif_e, adultes, tarif_a = nombres(
                t,
                r"vend (\d+) billets élèves à (\d+) € et "
                r"(\d+) billets adultes à (\d+) €"
            )
            technique = nombres(
                t,
                r"(?:La technique|La location du matériel "
                r"de sonorisation et d.éclairage) coûte (\d+) €"
            )
            programme = nombres(
                t, r"pour (?:un coût de )?(\d+) € par programme"
            )
            objectif = nombres(
                t, r"bénéfice d.au moins (\d+) €"
            )

            vendables = rangees * places - reservees
            billets = eleves + adultes
            recettes = eleves * tarif_e + adultes * tarif_a
            depenses = technique + billets * programme
            benefice = recettes - depenses
            atteint = "Oui" if benefice >= objectif else "Non"

            decisions.add(atteint)
            self.assertLessEqual(billets, vendables)

            self.verifier(e, "P9-M06", seed, {
                "r1": vendables,
                "r2": billets,
                "r3": recettes,
                "r4": depenses,
                "r5": benefice,
                "r6": atteint,
                "r7": abs(benefice - objectif)
            }, ["r5"])

            self.assertIn(
                f"= {benefice} €", e["correction"]
            )
            self.assertEqual(
                e, generer_modele_p9_spectacle(seed=seed)
            )

        self.assertEqual(decisions, {"Oui", "Non"})

    def test_p9_m07_recyclage(self):
        def en_grammes(valeur):
            return round(
                float(valeur.replace(",", ".")) * 1000
            )

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_recyclage(seed=seed)
            t = e["enonce"]

            m = re.search(
                r"préparé (\d+) sacs de ([\d,]+) kg chacun et "
                r"(\d+) cartons de ([\d,]+) kg chacun",
                t
            )
            self.assertIsNotNone(m)
            sacs, kg_sac, cartons, kg_carton = m.groups()

            refus = re.search(
                r"Lors du tri, ([\d,]+) kg", t
            )
            capacite = re.search(
                r"au maximum ([\d,]+) kg", t
            )
            self.assertIsNotNone(refus)
            self.assertIsNotNone(capacite)

            brut = (
                int(sacs) * en_grammes(kg_sac)
                + int(cartons) * en_grammes(kg_carton)
            )
            valide = brut - en_grammes(refus.group(1))
            contenance = en_grammes(capacite.group(1))

            pleins, reste = divmod(valide, contenance)

            self.assertGreater(reste, 0)
            self.assertLess(reste, contenance)

            self.verifier(e, "P9-M07", seed, {
                "r1": brut / 1000,
                "r2": valide / 1000,
                "r3": pleins,
                "r4": reste / 1000,
                "r5": pleins + 1
            })

            self.assertIn(
                f"Quotient : {pleins}", e["correction"]
            )
            self.assertIn(
                f"Reste : {reste}", e["correction"]
            )
            self.assertEqual(
                e, generer_modele_p9_recyclage(seed=seed)
            )

    def test_p9_m08_salles(self):
        decisions = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_salles(seed=seed)
            t = e["enonce"]

            classes, eleves, adultes = nombres(
                t,
                r"(\d+) classes de (\d+) élèves.*?"
                r"accompagnées de (\d+) adultes"
            )
            budget = nombres(
                t, r"budget maximal de (\d+) €"
            )

            ra, pa, forfait_a, tarif_a = nombres(
                t,
                r"\*\*Salle A\*\*.*?"
                r"(\d+) rangées de (\d+) places ;"
                r".*?forfait de réservation : (\d+) € ;"
                r".*?(\d+) € par participant"
            )
            rb, pb, forfait_b, tarif_b = nombres(
                t,
                r"\*\*Salle B\*\*.*?"
                r"(\d+) rangées de (\d+) places ;"
                r".*?forfait de réservation : (\d+) € ;"
                r".*?(\d+) € par participant"
            )

            personnes = classes * eleves + adultes
            places_a = ra * pa
            places_b = rb * pb
            cout_a = forfait_a + personnes * tarif_a
            cout_b = forfait_b + personnes * tarif_b

            admissible_a = (
                places_a >= personnes and cout_a <= budget
            )
            admissible_b = (
                places_b >= personnes and cout_b <= budget
            )

            self.assertNotEqual(admissible_a, admissible_b)

            choix = "A" if admissible_a else "B"
            decisions.add(choix)

            self.verifier(e, "P9-M08", seed, {
                "r1": personnes,
                "r2": places_a,
                "r3": places_b,
                "r4": cout_a,
                "r5": cout_b,
                "r6": choix
            }, ["r1", "r2", "r3", "r4", "r5"])

            self.assertIn(
                f"Choix : salle {choix}", e["correction"]
            )
            self.assertEqual(
                e, generer_modele_p9_salles(seed=seed)
            )

        self.assertEqual(decisions, {"A", "B"})

    def test_p9_m09_drones(self):
        decisions = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_drones(seed=seed)
            t = e["enonce"]

            chassis, sachets, par_sachet, abimees = nombres(
                t,
                r"possède (\d+) châssis.*?"
                r"reçoit (\d+) sachets de (\d+) hélices, "
                r"mais (\d+) hélices"
            )
            boites, par_boite, defectueuses = nombres(
                t,
                r"reçoit aussi (\d+) boîtes de (\d+) batteries, "
                r"dont (\d+) batteries"
            )
            objectif = nombres(
                t, r"\*\*(\d+) drones complets\*\*"
            )

            helices = sachets * par_sachet - abimees
            batteries = boites * par_boite - defectueuses
            maximum = min(
                chassis, helices // 4, batteries // 2
            )
            atteint = "Oui" if maximum >= objectif else "Non"

            decisions.add(atteint)

            self.verifier(e, "P9-M09", seed, {
                "r1": helices,
                "r2": batteries,
                "r3": maximum,
                "r4": helices - 4 * maximum,
                "r5": batteries - 2 * maximum,
                "r6": atteint,
                "r7": abs(maximum - objectif)
            }, ["r3"])

            self.assertIn(
                f"Quotient : {helices // 4}",
                e["correction"]
            )
            self.assertIn(
                f"Quotient : {batteries // 2}",
                e["correction"]
            )
            self.assertEqual(
                e, generer_modele_p9_drones(seed=seed)
            )

        self.assertEqual(decisions, {"Oui", "Non"})

    def test_p9_m10_mosaique(self):
        decisions = set()

        for seed in range(1, NB_TIRAGES + 1):
            e = generer_modele_p9_mosaique(seed=seed)
            t = e["enonce"]

            lignes, colonnes = nombres(
                t,
                r"mosaïque de (\d+) rangées et (\d+) colonnes"
            )
            reserve = nombres(
                t, r"également (\d+) carreaux supplémentaires"
            )

            paquet_a, prix_a = nombres(
                t,
                r"\*\*Offre A\*\*.*?"
                r"(\d+) carreaux par boîte ;"
                r".*?(\d+) € par boîte"
            )
            paquet_b, prix_b = nombres(
                t,
                r"\*\*Offre B\*\*.*?"
                r"(\d+) carreaux par boîte ;"
                r".*?(\d+) € par boîte"
            )

            besoin = lignes * colonnes + reserve
            na = (besoin + paquet_a - 1) // paquet_a
            nb = (besoin + paquet_b - 1) // paquet_b
            cout_a = na * prix_a
            cout_b = nb * prix_b

            self.assertNotEqual(cout_a, cout_b)

            choix = "A" if cout_a < cout_b else "B"
            decisions.add(choix)

            surplus = (
                na * paquet_a
                if choix == "A"
                else nb * paquet_b
            ) - besoin

            self.assertGreaterEqual(surplus, 0)

            self.verifier(e, "P9-M10", seed, {
                "r1": besoin,
                "r2": na,
                "r3": nb,
                "r4": cout_a,
                "r5": cout_b,
                "r6": choix,
                "r7": abs(cout_a - cout_b),
                "r8": surplus
            }, ["r4", "r5"])

            self.assertEqual(
                e, generer_modele_p9_mosaique(seed=seed)
            )

        self.assertEqual(decisions, {"A", "B"})


if __name__ == "__main__":
    unittest.main()
