"""Questions QCM complémentaires, originales, niveau 5e.

Calculs exacts et identifiants stables pour conserver les séries dans le temps.
Enrichit la banque existante sans modifier les 60 questions déjà publiées.
"""
from decimal import Decimal


def _d(valeur):
    return Decimal(str(valeur).replace(",", "."))


def _fr(valeur):
    n = _d(valeur)
    if n == 0:
        return '0'
    s = format(n.normalize(), 'f')
    return s.replace('.', ',')


def _valeurs(bonne, autres):
    correcte = _fr(bonne)
    propositions = [correcte]
    for v in autres:
        s = _fr(v)
        if s not in propositions and len(propositions) < 4:
            propositions.append(s)
    # Seulement si nécessaire : erreurs typiques de calcul à l'unité près.
    pas = _d('1')
    while len(propositions) < 4:
        s = _fr(_d(bonne) + pas)
        if s not in propositions:
            propositions.append(s)
        pas += 1
    return propositions


def _num(ident, question, bonne, mauvaises, explication, niveau=2):
    return dict(id=ident, question=question, options=_valeurs(bonne, mauvaises),
                answer=0, explain=explication, level=niveau)


def _texte(ident, question, bonne, mauvaises, explication, niveau=2):
    propositions = [bonne, *mauvaises]
    if len(propositions) != 4 or len(set(propositions)) != 4:
        raise ValueError(f'Options incorrectes pour {ident}')
    return dict(id=ident, question=question, options=propositions,
                answer=0, explain=explication, level=niveau)


def enrichir_banque(bank):
    a = {nom: [] for nom in ('decimaux', 'euclidienne', 'division_decimale',
                            'priorites', 'distributivite')}

    # Décimaux : additions, soustractions et multiplications, avec pièges de virgule.
    cas_add = [('7,8','2,35'),('12,5','3,75'),('0,8','0,65'),('15,09','4,7'),
               ('6,25','8,9'),('19,4','0,87'),('1,06','2,94'),('9,75','3,8'),
               ('14,6','5,45'),('0,09','1,7'),('28,35','4,65'),('3,07','0,93')]
    for i,(x,y) in enumerate(cas_add,1):
        b=_d(x)+_d(y)
        a['decimaux'].append(_num(f'plus_d_add_{i:02}',
            f'{x} + {y} = ?', b, [b+_d('0.9'),b-_d('0.1'), b*10],
            f'On place les virgules l’une sous l’autre : {x} + {y} = {_fr(b)}.'))
    cas_sous = [('10','2,75'),('12,3','4,85'),('7,5','0,68'),('20','6,49'),
                ('15,08','9,7'),('8,4','3,75'),('13,5','2,45'),('32,06','5,7'),
                ('9','1,92'),('17,25','8,9'),('25,1','9,63'),('42','18,75')]
    for i,(x,y) in enumerate(cas_sous,1):
        b=_d(x)-_d(y)
        a['decimaux'].append(_num(f'plus_d_sous_{i:02}',
            f'{x} − {y} = ?', b,[b+1,b-_d('0.1'),b*10],
            f'On complète avec des zéros si nécessaire, puis on calcule : {x} − {y} = {_fr(b)}.'))
    cas_mult = [('0,4','0,5'),('1,2','0,3'),('2,5','1,4'),('3,6','0,5'),
                 ('0,08','3'),('4,2','1,5'),('1,25','4'),('0,6','0,7'),
                 ('2,4','2,5'),('5,5','0,4'),('0,75','0,8'),('1,05','1,2')]
    for i,(x,y) in enumerate(cas_mult,1):
        b=_d(x)*_d(y)
        a['decimaux'].append(_num(f'plus_d_mult_{i:02}',
            f'{x} × {y} = ?', b,[b*10,b/10,b+_d('0.2')],
            f'On multiplie sans les virgules, puis on remet le nombre total de chiffres décimaux : {_fr(b)}.',3))

    # Euclidienne : poser un quotient / reste, tester la divisibilité et les diviseurs.
    cas_div = [(86,7),(59,8),(137,12),(101,9),(93,5),(74,6),(38,4),
               (128,10),(116,9),(64,7),(79,6),(145,12),(57,4),(215,11)]
    for i,(n,d) in enumerate(cas_div,1):
        q,r=divmod(n,d)
        a['euclidienne'].append(_num(f'plus_e_reste_{i:02}',
            f'Dans la division euclidienne de {n} par {d}, quel est le reste ?',
            r,[q, d, abs(n-d*q)+1],
            f'{n} = {d} × {q} + {r}. Le reste est {r} ; il est plus petit que {d}.'))
        a['euclidienne'].append(_num(f'plus_e_quot_{i:02}',
            f'{n} objets sont rangés par lots de {d}. Combien de lots complets peut-on faire ?',
            q,[q+1,q-1,r],
            f'On peut former {q} lots de {d} objets, il reste {r} objet(s).',2))
    cas_diviseurs = [(42,7,[8,9,10]),(54,9,[5,7,8]),(72,8,[5,7,11]),
                     (45,5,[4,7,8]),(63,7,[4,8,10]),(56,8,[5,9,11]),
                     (84,6,[5,9,11]),(90,10,[7,8,11]),(48,6,[5,7,10]),
                     (120,5,[7,9,11])]
    for i,(n,d,others) in enumerate(cas_diviseurs,1):
        assert n % d == 0 and all(n % t != 0 for t in others)
        a['euclidienne'].append(_texte(f'plus_e_diviseur_{i:02}',
             f'Lequel de ces nombres est un diviseur de {n} ?',str(d),[str(v) for v in others],
             f'{n} ÷ {d} = {n//d}, sans reste. Donc {d} est un diviseur de {n}.',2))
    nombres_neuf=[378,729,459,243,648,936,882,207,315,864]
    for i,n in enumerate(nombres_neuf,1):
        somme=sum(map(int,str(n)))
        assert somme%9==0
        a['euclidienne'].append(_texte(f'plus_e_neuf_{i:02}',
            f'Quel critère permet de montrer que {n} est divisible par 9 ?',
            f'La somme des chiffres est {somme}, un multiple de 9.',
            [f'{n} est un nombre {'pair' if n%2==0 else 'impair'}.',
             'Son chiffre des unités est plus petit que 9.',
             'Tous les nombres à trois chiffres sont divisibles par 9.'],
            f'On additionne les chiffres : {" + ".join(str(c) for c in str(n))} = {somme}. '
            f'Comme {somme} est un multiple de 9, {n} est divisible par 9.',3))

    # Division décimale : le choix de la transformation et le quotient.
    cas_decimal = [('0,7',12),('0,3',14),('0,4',9),('0,6',8),('0,25',24),
                   ('0,5',18),('1,2',7),('0,8',15),('1,5',6),('2,5',8),
                   ('0,09',20),('0,12',50),('0,15',16),('0,75',8),
                   ('0,2',35),('0,05',40),('0,45',6),('0,18',15)]
    for i,(d,q) in enumerate(cas_decimal,1):
        n=_d(d)*q
        a['division_decimale'].append(_num(f'plus_v_quot_{i:02}',
            f'{_fr(n)} ÷ {d} = ?',q,[q*10,q/10,q+1],
            f'On multiplie les deux nombres par 10 ou par 100 pour rendre le diviseur entier. '
            f'On obtient {q}.',2))
        coef=100 if _d(d)*10!=_d(d)*10//1 else 10
        # Calcul mécanique : le même facteur aux deux nombres.
        transform=_texte(f'plus_v_equiv_{i:02}',
            f'Quelle division est équivalente à {_fr(n)} ÷ {d} ?',
            f'{_fr(n*coef)} ÷ {_fr(_d(d)*coef)}',
            [f'{_fr(n)} ÷ {_fr(_d(d)*coef)}',
             f'{_fr(n*coef)} ÷ {d}',
             f'{_fr(n/coef)} ÷ {d}'],
            f'On multiplie le dividende ET le diviseur par {coef}. Le quotient ne change pas.',3)
        a['division_decimale'].append(transform)

    # Priorités : multiplication et division à égalité, parenthèses, pièges.
    cas_priorites = [(36,6,3),(48,8,2),(72,9,4),(64,4,5),(90,10,3),
                     (81,9,6),(56,7,3),(120,5,2),(96,12,4),(84,7,2)]
    for i,(n,d,m) in enumerate(cas_priorites,1):
        b=(n//d)*m
        a['priorites'].append(_num(f'plus_p_gd_{i:02}',
            f'{n} ÷ {d} × {m} = ?',b,[n//(d*m),n//d+m,n//d-m],
            f'÷ et × ont le même rang : de gauche à droite, {n} ÷ {d} = {n//d}, puis × {m} = {b}.',3))
    cas_moins = [(30,4,6),(50,7,5),(45,8,4),(100,12,7),(70,9,6),
                  (66,5,8),(80,3,9),(64,6,7),(90,4,13),(55,7,6)]
    for i,(n,b,c) in enumerate(cas_moins,1):
        r=n-b*c
        a['priorites'].append(_num(f'plus_p_moins_{i:02}',
            f'{n} − {b} × {c} = ?',r,[(n-b)*c,n-(b+c),r+10],
            f'On multiplie d’abord : {b} × {c} = {b*c}, puis {n} − {b*c} = {r}.',2))
    cas_par = [(3,8,4),(7,9,2),(5,12,6),(4,15,5),(6,8,7),
               (9,11,4),(8,20,5),(2,25,6),(5,16,9),(3,14,8)]
    for i,(a1,b,c) in enumerate(cas_par,1):
        r=a1*(b+c)
        a['priorites'].append(_num(f'plus_p_parentheses_{i:02}',
            f'{a1} × ({b} + {c}) = ?',r,[a1*b+c,(a1+b)*c,r+a1],
            f'On calcule la parenthèse en premier : {b}+{c}={b+c}, puis {a1}×{b+c}={r}.',2))

    # Distributivité : développer, factoriser et vérifier le résultat.
    cas_dist = [(2,7,9),(3,12,4),(5,8,6),(4,15,3),(6,11,7),
                (7,9,5),(8,12,6),(9,11,3),(3,18,7),(5,14,9)]
    for i,(m,b,c) in enumerate(cas_dist,1):
        r=m*(b+c)
        a['distributivite'].append(_num(f'plus_t_calcul_{i:02}',
            f'{m} × ({b} + {c}) = ?',r,[m*b+c,(m+b)*c,m*(b*c)],
            f'On multiplie chaque terme : {m}×{b} + {m}×{c} = {m*b}+{m*c} = {r}.',2))
        a['distributivite'].append(_texte(f'plus_t_develop_{i:02}',
            f'Comment développer {m} × ({b} + {c}) ?',
            f'{m} × {b} + {m} × {c}',
            [f'{m} × {b} + {c}',f'{m} + {b} × {c}',f'{m} × {b} × {c}'],
            'On multiplie les DEUX nombres de la parenthèse par le facteur placé devant.',3))
        r2=m*(b-c)
        a['distributivite'].append(_num(f'plus_t_soustraction_{i:02}',
            f'{m} × ({b} − {c}) = ?',r2,[m*b-c,m*b+m*c,r2+m],
            f'{m} × {b} − {m} × {c} = {m*b} − {m*c} = {r2}.',3))

    # Questions de raisonnement : énoncés volontairement variés et pièges courants.
    contextuelles = {
        'decimaux': [
            ('Pour poser 12,5 + 0,75 en colonnes, que doit-on aligner ?',
             'Les deux virgules.', ['Les derniers chiffres.','Les chiffres de gauche.','Les chiffres 5 et 5.'],
             'En addition, unités sous unités et virgules sous virgules.'),
            ('Pour calculer 2,4 × 1,5, faut-il aligner les virgules ?',
             'Non, on compte les chiffres décimaux du produit.',
             ['Oui, exactement comme pour l’addition.','Oui, mais seulement pour 1,5.','Non, on supprime la virgule définitivement.'],
             'On calcule 24 × 15 = 360 puis on place deux chiffres après la virgule : 3,60.'),
            ('Dans 8,50 − 2,75, pourquoi écrit-on 8,50 au lieu de 8,5 ?',
             'Pour avoir autant de chiffres après la virgule dans les colonnes.',
             ['Parce que 8,50 est plus grand que 8,5.','Parce qu’il faut toujours multiplier par 10.','Parce que la soustraction est impossible sans zéro.'],
             '8,5 = 8,50. Ajouter le zéro final ne change pas le nombre.'),
            ('Un jeu coûte 12,90 € et un bonus 3,45 €. Combien au total ?',
             '16,35 €', ['15,35 €','16,25 €','15,135 €'],
             '12,90 € + 3,45 € = 16,35 €.'),
            ('Un article coûte 20 €. On retire 7,85 €. Quel montant reste ?',
             '12,15 €', ['13,15 €','12,85 €','17,15 €'],
             '20,00 € − 7,85 € = 12,15 €.'),
            ('Pourquoi 0,3 × 0,2 n’est-il pas égal à 6 ?',
             'Parce que le résultat est 0,06.', ['Parce que le résultat est 0,6.','Parce que le résultat est 0,006.','Parce que cette multiplication est interdite.'],
             '3 × 2 = 6 et il y a deux chiffres après la virgule : 0,06.'),
            ('Un cahier coûte 2,50 €. Combien coûtent 4 cahiers ?',
             '10 €', ['6,50 €','100 €','8 €'],
             '2,50 × 4 = 10 €.'),
            ('Une bouteille contient 1,25 L. Quelle quantité pour 3 bouteilles ?',
             '3,75 L', ['2,75 L','37,5 L','3,25 L'],
             '1,25 × 3 = 3,75 L.'),
        ],
        'euclidienne': [
            ('Quel nombre est divisible par 2, mais pas par 5 ?',
             '318',['320','315','371'],
             '318 se termine par 8 (pair), mais pas par 0 ou 5.'),
            ('Quel nombre est divisible par 5, mais pas par 10 ?',
             '145',['150','144','142'],
             '145 se termine par 5, et non par 0.'),
            ('Quel nombre est divisible par 3, mais pas par 9 ?',
             '123',['126','121','127'],
             '1 + 2 + 3 = 6 : multiple de 3 mais pas de 9.'),
            ('Parmi ces nombres, lequel est divisible par 9 ?',
             '378',['376','371','379'],
             '3 + 7 + 8 = 18 : 18 est un multiple de 9.'),
            ('Une division euclidienne par 8 peut-elle avoir un reste de 9 ?',
             'Non : le reste doit être plus petit que 8.',
             ['Oui : tous les restes sont possibles.','Oui : si le quotient vaut 1.','Oui : seulement si le dividende est pair.'],
             'Avec un diviseur 8, le reste peut aller de 0 à 7.'),
            ('Quand une division euclidienne a un reste de 0, que sait-on ?',
             'Le diviseur est un diviseur exact du dividende.',
             ['Le quotient vaut forcément 0.','Le dividende vaut 0.','Le diviseur vaut forcément 1.'],
             'Exemple : 42 = 7 × 6 + 0, donc 7 divise exactement 42.'),
            ('Pourquoi 58 n’est-il pas divisible par 9 ?',
             '5 + 8 = 13, qui n’est pas un multiple de 9.',
             ['Parce que 58 est pair.','Parce que 58 se termine par 8.','Parce que 58 possède deux chiffres.'],
             'Le critère de 9 utilise la somme des chiffres.'),
            ('Un paquet contient 9 cartes. Avec 77 cartes, combien restent après 8 paquets ?',
             '5 cartes',['8 cartes','9 cartes','14 cartes'],
             '9 × 8 = 72, et 77 − 72 = 5.'),
        ],
        'division_decimale': [
            ('Pour transformer 8,4 ÷ 0,7 en division par un entier, que fait-on ?',
             'On multiplie les deux nombres par 10.',
             ['On multiplie seulement 0,7 par 10.','On multiplie seulement 8,4 par 10.','On enlève toutes les virgules sans réfléchir.'],
             '8,4 ÷ 0,7 = 84 ÷ 7 = 12.'),
            ('Comment transformer 6 ÷ 0,25 sans changer le résultat ?',
             '600 ÷ 25',['60 ÷ 25','6 ÷ 25','600 ÷ 0,25'],
             'On multiplie le dividende ET le diviseur par 100.'),
            ('Que vaut 8 ÷ 0,5 ?', '16',['4','1,6','40'],
             'Diviser par 0,5, c’est chercher combien de demi-unités il y a dans 8 : 16.'),
            ('Peut-on calculer 6,3 ÷ 0 ?',
             'Non : la division par zéro est impossible.',
             ['Oui : on obtient 0.','Oui : on obtient 6,3.','Oui : on obtient 63.'],
             'Aucun nombre multiplié par 0 ne permet de retrouver 6,3.'),
            ('Un ruban mesure 3,6 m. On coupe des morceaux de 0,9 m. Combien ?',
             '4 morceaux',['3 morceaux','9 morceaux','40 morceaux'],
             '3,6 ÷ 0,9 = 36 ÷ 9 = 4.'),
            ('Tu as 2,4 L de jus. Combien de verres de 0,3 L peux-tu remplir ?',
             '8 verres',['6 verres','0,8 verre','80 verres'],
             '2,4 ÷ 0,3 = 24 ÷ 3 = 8.'),
            ('Si le diviseur est 0,03, quel facteur le rend entier ?',
             '100',['10','1 000 000','0'],
             '0,03 × 100 = 3. On multiplie aussi le dividende par 100.'),
            ('Que vaut 0 ÷ 7 ?', '0',['7','Impossible','70'],
             '0 ÷ 7 = 0 ; ce qui est interdit, c’est de diviser PAR zéro.'),
        ],
        'priorites': [
            ('18 − 6 + 2 = ?', '14',['10','26','12'],
             'Additions et soustractions ont la même priorité : de gauche à droite, 18 − 6 + 2 = 14.'),
            ('32 − 12 + 3 = ?', '23',['17','29','20'],
             'On calcule 32 − 12 = 20, puis 20 + 3 = 23.'),
            ('Quelle règle est correcte pour × et ÷ ?',
             'Même priorité : on calcule de gauche à droite.',
             ['La multiplication passe toujours avant la division.','La division passe toujours avant la multiplication.','Il faut toujours commencer par l’opération de droite.'],
             'Exemple : 24 ÷ 3 × 2 = 8 × 2 = 16.'),
            ('Quelle règle est correcte pour + et − ?',
             'Même priorité : on calcule de gauche à droite.',
             ['On additionne toujours avant de soustraire.','On soustrait toujours avant d’additionner.','On choisit l’opération avec les plus grands nombres.'],
             'Dans 18 − 6 + 2, on obtient 14, pas 10.'),
            ('24 ÷ (3 × 2) = ?', '4',['16','10','12'],
             'Avec les parenthèses : 3 × 2 = 6, puis 24 ÷ 6 = 4.'),
            ('24 ÷ 3 × 2 = ?', '16',['4','12','8'],
             'Sans parenthèses, on fait d’abord 24 ÷ 3 = 8, puis 8 × 2 = 16.'),
            ('Pourquoi 7 + 3 × 4 vaut 19 et non 40 ?',
             'Parce que la multiplication se calcule avant l’addition.',
             ['Parce que 7 + 3 vaut 19.','Parce que le 4 ne compte pas.','Parce qu’il faut ajouter des parenthèses invisibles autour de 7 + 3.'],
             '3 × 4 = 12, puis 7 + 12 = 19.'),
            ('12 + 18 ÷ 3 × 2 = ?', '24',['20','36','12'],
             'On calcule 18 ÷ 3 = 6, puis 6 × 2 = 12, enfin 12 + 12 = 24.'),
        ],
        'distributivite': [
            ('Dans 4 × (5 + 3), quel terme faut-il multiplier par 4 ?',
             'Le 5 ET le 3.', ['Seulement le 5.','Seulement le 3.','Seulement le signe +.'],
             '4 × (5 + 3) = 4 × 5 + 4 × 3.'),
            ('Quelle écriture est équivalente à 7 × 19 ?',
             '7 × (20 − 1)', ['7 × (20 + 1)','7 + 20 − 1','7 × 20 − 1'],
             '19 = 20 − 1, donc 7 × 19 = 7 × 20 − 7.'),
            ('Quel est le piège dans 2 × (5 + 3) = 2 × 5 + 3 ?',
             'On a oublié de multiplier le 3 par 2.',
             ['Il fallait remplacer + par ÷.','On ne peut jamais calculer avec des parenthèses.','2 × 5 devrait donner 12.'],
             'La bonne écriture est 2 × 5 + 2 × 3 = 16.'),
            ('Quelle expression factorise 6 × 4 + 6 × 7 ?',
             '6 × (4 + 7)', ['6 × (4 × 7)','(6 + 4) × 7','6 + (4 + 7)'],
             'Le facteur commun est 6 : on le place devant la parenthèse.'),
            ('Pour calculer 8 × 99 facilement, quelle idée est bonne ?',
             '8 × (100 − 1)', ['8 × (100 + 1)','8 × (9 + 9)','8 + 100 − 1'],
             '8 × 99 = 8 × 100 − 8 = 792.'),
            ('Quelle écriture est égale à 5 × (12 − 2) ?',
             '5 × 12 − 5 × 2', ['5 × 12 − 2','5 × 12 + 5 × 2','12 × 2 − 5'],
             'On distribue 5 sur les deux termes avec le signe moins.'),
            ('On achète 3 menus contenant chacun un sandwich à 5 € et un jus à 2 €. Quel calcul convient ?',
             '3 × (5 + 2)', ['3 × 5 + 2','3 + 5 + 2','(3 + 5) × 2'],
             'Chaque menu coûte 7 €, et il y a 3 menus : 3 × 7 = 21 €.'),
            ('À quoi sert la distributivité ?',
             'À transformer un produit avec parenthèses en somme ou différence de produits.',
             ['À rendre tous les résultats plus grands.','À remplacer les multiplications par des divisions.','À supprimer les retenues de tous les calculs.'],
             'On peut calculer 6 × (10 + 2) comme 6 × 10 + 6 × 2.'),
        ],
    }
    for notion, situations in contextuelles.items():
        for j, (question, bonne, mauvaises, explication) in enumerate(situations, 1):
            a[notion].append(_texte(f'plus_{notion}_concept_{j:02}', question,
                                     bonne, mauvaises, explication, 3))

    for nom, ajout in a.items():
        existants = {q['id'] for q in bank[nom]}
        for q in ajout:
            if q['id'] in existants:
                raise ValueError(f'Identifiant déjà présent : {q["id"]}')
            if not (len(q['options']) == 4 and len(set(q['options'])) == 4):
                raise ValueError(f'Réponses ambiguës : {q["id"]}')
            bank[nom].append(q)
            existants.add(q['id'])
