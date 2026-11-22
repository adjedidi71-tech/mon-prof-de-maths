#!/usr/bin/env python3
"""Audit hors-ligne des modèles MathiCap 7, 8 et 9 (aucune écriture Supabase).

Usage : python auditer_difficulte_mathicap.py --banque banque_priorites.py --tests 200
Dépendances : bibliothèque standard Python uniquement.

Les scores proviennent de métadonnées pédagogiques documentées, non d'une
prétendue reconnaissance automatique fiable du raisonnement dans un texte.
"""
import argparse
import ast
import csv
import hashlib
import importlib.util
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent
GRILLE = DIR / 'referentiel_difficulte_mathicap_v1.json'
QUANTITE_MODELES = {7:26, 8:10, 9:10}


def donnees_ref(path=GRILLE):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if set(data['criteres']) != {'autonomie','enchaînement','contraintes','stratégies','résolution_finale','numérique'}:
        raise ValueError('Critères du référentiel incomplets ou inattendus')
    if sum(c['poids'] for c in data['criteres'].values()) != 100:
        raise ValueError('La somme des pondérations ne vaut pas 100')
    ids=[entry['id'] for entry in data['modeles']]
    if len(ids)!=len(set(ids)):
        raise ValueError('Identifiants dupliqués dans le référentiel')
    for entry in data['modeles']:
        if entry['niveau_declare'] != int(entry['id'][1]):
            raise ValueError(f"Niveau incohérent : {entry['id']}")
        if set(entry['notes'])!=set(data['criteres']):
            raise ValueError(f"Critères incomplets : {entry['id']}")
        if any(type(x) is not int or x<0 or x>4 for x in entry['notes'].values()):
            raise ValueError(f"Les notes doivent être des entiers de 0 à 4 : {entry['id']}")
        if not entry.get('justification'):
            raise ValueError(f"Justification absente : {entry['id']}")
    return data


def calculer_score(entry, cfg):
    return round(sum(entry['notes'][k]*cfg['criteres'][k]['poids']/4 for k in cfg['criteres']),2)


def niveau_estime(score):
    if score < 35: return 'hors 7–9'
    if score < 55: return '7'
    if score < 75: return '8'
    return '9'


def frontiere(score, marge):
    return any(abs(score-b)<=marge for b in (35,55,75))


def decouvrir_generateurs(chemin):
    source=Path(chemin).read_text(encoding='utf-8')
    arbre=ast.parse(source,filename=str(chemin))
    cible=next((n for n in arbre.body if isinstance(n,ast.FunctionDef) and n.name=='generer_exercices_priorites'),None)
    if cible is None: raise ValueError('Fonction generer_exercices_priorites introuvable')
    noms=[]
    for node in ast.walk(cible):
        if (isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute)
            and node.func.attr=='append' and node.args and isinstance(node.args[0],ast.Call)
            and isinstance(node.args[0].func,ast.Name)
            and re.fullmatch(r'generer_modele_p[789]_\w+',node.args[0].func.id)):
            noms.append(node.args[0].func.id)
    if len(noms)!=len(set(noms)):
        raise ValueError('Fonction génératrice référencée plusieurs fois')
    if not noms:raise ValueError('Aucun générateur actif détecté')
    return noms


def lire_module(chemin):
    spec=importlib.util.spec_from_file_location('mathicap_banque_audit_local',str(chemin))
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def controle_exercice(ex, identifiant, regles):
    erreurs=[]
    n=4 if identifiant.startswith('P7-') else 5
    if not isinstance(ex,dict): return ['La fonction n’a pas renvoyé un dictionnaire'],[]
    if ex.get('id')!=identifiant: erreurs.append(f"ID généré {ex.get('id')!r} au lieu de {identifiant}")
    enonce=ex.get('enonce','')
    correction=ex.get('correction','')
    if enonce.count('**Questions**')!=1: erreurs.append('Bloc Questions absent ou dupliqué')
    bloc=enonce.split('**Questions**')[-1]
    lignes=re.findall(r'(?m)^([1-5])\.\s+(.+?)\s*$',bloc)
    if len(lignes)!=n or [int(x[0]) for x in lignes]!=list(range(1,n+1)):
        erreurs.append(f'Numérotation des questions incorrecte (attendu {n})')
    champs=ex.get('champs_reponse',[])
    if len(champs)!=n: erreurs.append(f'Nombre de champs incorrect : {len(champs)} au lieu de {n}')
    if len({c.get('id') for c in champs})!=len(champs): erreurs.append('Champs dupliqués')
    if [c.get('question') for c in champs]!=list(range(1,n+1)):
        erreurs.append('Position des champs incohérente')
    if not ex.get('mathicap_questions_uniformisees'):
        erreurs.append('Uniformisation non confirmée')
    if identifiant not in regles: erreurs.append('Règles de questions absentes')
    else:
        if [c.get('id') for c in champs]!=[key for key,_ in regles[identifiant]]:
            erreurs.append('Ordre des champs différent des règles')
        # Les formulations peuvent être adaptées par des règles conditionnelles.
        if len(regles[identifiant])!=n: erreurs.append('Nombre de règles différent du niveau')
    if 'Réponses attendues' not in correction: erreurs.append('Bloc des réponses attendues absent')
    for i,c in enumerate(champs,1):
        if c.get('type') not in ('nombre','choix'):
            erreurs.append(f'Champ {i} non automatiquement évaluable')
        if c.get('attendu') is None:
            erreurs.append(f'Attendu absent pour Q{i}')
        if c.get('type')=='choix' and c.get('attendu') not in c.get('options',[]):
            erreurs.append(f'Réponse Q{i} absente des choix')
        if not re.search(rf'\*\*Question {i} — ',correction):
            erreurs.append(f'Réponse Q{i} absente du résumé de correction')
    if not correction.strip(): erreurs.append('Correction vide')
    return erreurs,champs


def evaluer(cfg, banque, tests):
    module=lire_module(banque)
    noms=decouvrir_generateurs(banque)
    cibles={e['id']:e for e in cfg['modeles']}
    candidats={}
    erreurs_globales=[]
    for nom in noms:
        generateur=getattr(module,nom,None)
        if not callable(generateur):
            erreurs_globales.append(f'Fonction manquante : {nom}');continue
        try:ex=generateur()
        except Exception as err:
            erreurs_globales.append(f'Génération impossible pour {nom}: {err}');continue
        identifiant=ex.get('id','?')
        if identifiant in candidats: erreurs_globales.append(f'Modèle dupliqué {identifiant}')
        candidats[identifiant]=(nom,generateur,ex)
    missing=set(cibles)-set(candidats)
    extra=set(candidats)-set(cibles)
    if missing:erreurs_globales.append('Modèles référencés absents du code : '+', '.join(sorted(missing)))
    if extra:erreurs_globales.append('Nouveaux modèles non étalonnés : '+', '.join(sorted(extra)))
    for n,count in QUANTITE_MODELES.items():
        nb=sum(int(id_[1])==n for id_ in candidats if re.fullmatch(r'P[789]-M\d+',id_))
        if nb!=count:erreurs_globales.append(f'Niveau {n} : {nb} générateurs au lieu de {count}')
    lignes=[]
    for identifiant in sorted(cibles):
        e=cibles[identifiant]
        niveau=e['niveau_declare']
        score=calculer_score(e,cfg)
        classe=niveau_estime(score)
        avis='à reclasser / renforcer / revoir' if classe!=str(niveau) else 'dans la plage proposée'
        if frontiere(score,cfg['zone_frontiere_points']):avis+=' ; proche frontière'
        erreurs=[]; finals=[]; titres=[]; tous_corriges=[]
        if identifiant in candidats:
            nom,gen,_=candidats[identifiant]
            for i in range(tests):
                try:
                    ex=gen()
                    err,champs=controle_exercice(ex,identifiant,module.REGLES)
                    titres.append(ex.get('titre',''))
                    if champs:
                        val=champs[-1]['attendu']
                        finals.append(str(val))
                    if err:
                        erreurs.extend(f'Tirage {i+1}: {msg}' for msg in err)
                except Exception as exc:
                    erreurs.append(f'Tirage {i+1}: erreur de génération {type(exc).__name__}: {exc}')
            if len(set(titres))>1:
                erreurs.append('Titre instable entre variantes')
        else:
            erreurs.append('Modèle non trouvé dans le code')
        distinct=len(set(finals))
        # Une réponse catégorielle peut naturellement n'avoir que 2 valeurs.
        variation='faible' if finals and distinct<max(3,min(6,tests//10)) else 'correcte'
        lignes.append({
            'id':identifiant,'titre':titres[0] if titres else '',
            'niveau_actuel':niveau,'score_sur_100':score,'niveau_suggere':classe,
            'proximite_frontiere':'oui' if frontiere(score,cfg['zone_frontiere_points']) else 'non',
            'avis_pedagogique':avis,'statut_notes':e['evaluation'],
            'generations_testees':tests,'valeurs_finales_distinctes':distinct,
            'diversite_finale':variation,'erreurs_structurelles':len(erreurs),
            'details_erreurs':' | '.join(erreurs[:5]),'justification':e['justification'],
        })
    return lignes,erreurs_globales


def exporter(lignes, erreurs_globales, dossier, cfg, banque, tests):
    dossier=Path(dossier); dossier.mkdir(parents=True,exist_ok=True)
    csvfile=dossier/'rapport_difficulte_46_modeles.csv'
    with csvfile.open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(lignes[0]),delimiter=';');writer.writeheader();writer.writerows(lignes)
    stats=Counter(str(r['niveau_actuel']) for r in lignes)
    incoherents=[r for r in lignes if str(r['niveau_actuel'])!=r['niveau_suggere']]
    tranches=defaultdict(list)
    for r in lignes:tranches[int(r['niveau_actuel'])].append(r)
    nb_erreurs=sum(r['erreurs_structurelles'] for r in lignes)+len(erreurs_globales)
    lines=[
        '# Audit du référentiel de difficulté MathiCap',
        '', '**Statut : étalonnage provisoire, aucun reclassement automatique.**',
        f'Code audité : `{Path(banque).name}` ; SHA-256 : `{hashlib.sha256(Path(banque).read_bytes()).hexdigest()}`.',
        f'Variantes testées par modèle : {tests}.',
        f'Modèles analysés : {len(lignes)} ; distribution : '+', '.join(f'N{k}={v}' for k,v in sorted(stats.items()))+'.',
        f'Alertes d’écart de classe : {len(incoherents)} (à étudier, ne sont pas des erreurs certaines).',
        f'Erreurs de structure : {nb_erreurs} (détails CSV).','',
        '## Pourquoi les scores ne sont pas encore définitifs',
        'Chaque modèle comporte six notes pédagogiques proposées par analyse humaine des mécanismes du code, et non calculées fiablement à partir du texte libre. L’automatisation recalcule **de façon déterministe** le score à partir de ces notes, vérifie le nombre de questions, les champs et la correction sur des variantes, puis signale les écarts avec le niveau déclaré. Les notes et les seuils doivent être validés avant utilisation comme bloqueur de publication.','',
        '## Synthèse des trois niveaux','',
        '| Niveau | Modèles | Score médian | Scores min–max | Hors plage proposée |','|---|---:|---:|---:|---:|'
    ]
    for n in (7,8,9):
        v=sorted(x['score_sur_100'] for x in tranches[n]);median=v[len(v)//2] if len(v)%2 else (v[len(v)//2-1]+v[len(v)//2])/2
        hors=sum(x['niveau_suggere']!=str(n) for x in tranches[n]);lines.append(f'| {n} | {len(v)} | {median:.1f} | {min(v):g}–{max(v):g} | {hors} |')
    lines.extend(['','## Alertes de classement initiales','', '| Modèle | Niveau déclaré | Score | Classe proposée |','|---|---:|---:|---|'])
    for row in incoherents:
        lines.append(f"| {row['id']} – {row['titre']} | {row['niveau_actuel']} | {row['score_sur_100']:.2f} | {row['niveau_suggere']} |")
    lines.extend(['','## Étapes avant de figer le barème','',
      '1. Examiner les modèles signalés, en particulier les fanions, le club de robotique N7 et les modèles N8 trop guidés.',
      '2. Valider ou corriger **chaque** note avec un exemple de raisonnement réel (au moins plusieurs variantes).',
      '3. Vérifier la distribution des scores et adapter les seuils une seule fois, puis versionner la grille.',
      '4. Ajouter un blocage de publication pour les nouveaux modèles sans métadonnées ou avec erreur structurelle ; n’utiliser l’écart de niveau pour bloquer qu’après validation de l’étalonnage.',
      '5. Plus tard, comparer les scores théoriques aux résultats anonymisés des élèves, sur un échantillon suffisant.',
      '', '## Erreurs globales',''] )
    lines.extend(f'- {x}' for x in erreurs_globales) if erreurs_globales else lines.append('- Aucune.')
    (dossier/'rapport_synthese.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    summary={'mode':'provisoire','nombre_modeles':len(lignes),'tests_par_modele':tests,'erreurs_structurelles':nb_erreurs,'alertes_de_niveau':len(incoherents),'source_sha256':hashlib.sha256(Path(banque).read_bytes()).hexdigest()}
    (dossier/'resultats_audit.json').write_text(json.dumps({'resume':summary,'erreurs_globales':erreurs_globales,'modeles':lignes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--banque',type=Path,default=DIR/'banque_priorites.py',help='Version de banque_priorites.py à auditer')
    a.add_argument('--referentiel',type=Path,default=GRILLE)
    a.add_argument('--sortie',type=Path,default=DIR/'resultats')
    a.add_argument('--tests',type=int,default=200)
    a.add_argument('--strict-niveau',action='store_true',help='Active le blocage sur écarts de niveaux — après validation humaine uniquement')
    args=a.parse_args()
    if not 1<=args.tests<=10000: a.error('--tests doit être compris entre 1 et 10000')
    if not args.banque.is_file(): a.error(f'Fichier banque introuvable : {args.banque}')
    cfg=donnees_ref(args.referentiel)
    lignes,erreurs_globales=evaluer(cfg,args.banque,args.tests)
    resume=exporter(lignes,erreurs_globales,args.sortie,cfg,args.banque,args.tests)
    print(json.dumps(resume,ensure_ascii=False,indent=2))
    if resume['erreurs_structurelles']:
        print('ECHEC : anomalies structurelles — corriger avant tout déploiement.')
        return 2
    if args.strict_niveau and resume['alertes_de_niveau']:
        print('ECHEC : écarts de difficulté avec le classement déclaré (barème à valider).')
        return 3
    print('CONTRÔLE STRUCTUREL RÉUSSI. Le classement pédagogique reste provisoire.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
