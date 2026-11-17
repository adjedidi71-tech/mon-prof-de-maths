"""Recalcul indépendant des derniers défis depuis le texte réellement affiché.
Une réponse attendue incorrecte ou une donnée manquante déclenche une erreur.
Ce contrôle ne constitue pas une validation psychométrique par des élèves.
"""
import re,math,random,collections
import banque_priorites as b

def val(p,texte,ident):
 m=re.search(p,texte,re.S|re.I)
 if not m: raise AssertionError(f'{ident}: extraction impossible: {p}')
 return m

def n(p,texte,ident):return int(val(p,texte,ident).group(1))

def eq(x,y,ident):
 if not math.isclose(x,y,abs_tol=0.00001):raise AssertionError(f'{ident}: valeur affichée {x}, calcul indépendant {y}')

c=collections.Counter()
for i in range(650):
 for fid,fn in [
  ('P9-M06',b.generer_modele_p9_spectacle),
  ('P9-M09',b.generer_modele_p9_drones),
  ('P9-M02',b.generer_modele_p9_tournoi),
  ('P9-M04',b.generer_modele_p9_cristaux),
  ('P9-M07',b.generer_modele_p9_recyclage),
  ('P9-M10',b.generer_modele_p9_mosaique),
  ('P9-M01',b.generer_modele_p9_potager),
  ('P9-M03',b.generer_modele_p9_festival),
  ('P9-M05',b.generer_modele_p9_bibliotheque),
  ('P8-M01',b.generer_modele_p8_clubs),
  ('P8-M07',b.generer_modele_p8_eau),
  ('P8-M06',b.generer_modele_p8_kits),
  ('P8-M03',b.generer_modele_p8_jeu_video),
  ('P8-M08',b.generer_modele_p8_parcours),
  ('P8-M10',b.generer_modele_p8_transport),
  ('P7-M23',b.generer_modele_p7_couture),
 ]:
  if fid.startswith('P9'):e=fn(i+154000)
  else:
   random.seed(i+150100)
   e=fn()
  t=e['enonce'];ans=e['champs_reponse'][-1]['attendu'];q=e['champs_reponse']
  if fid=='P9-M06':
   a=val(r'possède (\d+) rangées de (\d+) places\. (\d+) places sont réservées',t,fid)
   capacity=int(a[1])*int(a[2])-int(a[3])
   tarif=n(r'billets élèves à (\d+) €',t,fid)
   prog=n(r'coût de (\d+) € par programme',t,fid)
   base=n(r'bénéfice d.au moins (\d+) €',t,fid)
   benefice=q[3]['attendu'];vendus=q[0]['attendu']
   # Deux formulations selon que l'objectif initial est déjà atteint.
   complement=re.search(r'veut augmenter son bénéfice actuel d.au moins (\d+) €',t)
   gap=int(complement[1]) if complement else max(0,base-benefice)
   out=capacity-vendus-math.ceil(gap/(tarif-prog))
  elif fid=='P9-M09':
   hel=q[0]['attendu'];bat=q[1]['attendu']
   cible=n(r'construire (\d+) drones au total',t,fid)
   hm=val(r'sachets entiers de (\d+), à (\d+) €',t,fid)
   bm=val(r'boîtes entières de (\d+), à (\d+) €',t,fid)
   out=math.ceil(max(0,4*cible-hel)/int(hm[1]))*int(hm[2])+math.ceil(max(0,2*cible-bat)/int(bm[1]))*int(bm[2])
  elif fid=='P9-M02':
   entr=n(r'versent chacun \*\*(\d+) €',t,fid)
   objectif=n(r'bénéfice minimal de (\d+) €',t,fid)
   mauvais=val(r'organisateur (A|B), le moins rentable',t,fid)[1]
   variable=n(r'Organisateur '+mauvais+r' — Proposition.*?Fournitures : (\d+) € par joueur',t,fid)
   out=math.ceil((objectif-min(q[1]['attendu'],q[2]['attendu']))/(entr-variable))
  elif fid=='P9-M04':
   disponible=q[1]['attendu']
   cible=n(r'équiper (\d+) aventuriers',t,fid)
   bonus=n(r'reçoit (\d+) cristaux supplémentaires gratuitement',t,fid)
   prix=n(r'Un équipement coûte \*\*(\d+) cristaux',t,fid)
   reserve=n(r'conserver au moins \*\*(\d+) cristaux',t,fid)
   mission=n(r'rapportant chacune (\d+) cristaux',t,fid)
   out=math.ceil(max(0,cible*prix+reserve-disponible-bonus)/mission)
  elif fid=='P9-M07':
   ajout=float(val(r'reçoit après le tri (\d+,\d+) kg',t,fid)[1].replace(',','.'));total=int(round((q[1]['attendu']+ajout)*1000))
   A=val(r'\*\*Offre A\*\*.*?maximum (\d+,\d+) kg.*?Location : (\d+) €',t,fid)
   B=val(r'\*\*Offre B\*\*.*?maximum (\d+,\d+) kg.*?Location : (\d+) €',t,fid)
   cost=lambda p:(total+int(round(float(p[1].replace(',','.'))*1000))-1)//int(round(float(p[1].replace(',','.'))*1000))*int(p[2])
   out=min(cost(A),cost(B))
  elif fid=='P9-M10':
   base=q[0]['attendu'];extra=n(r'\*\*Nouveau défi :\*\* (\d+) carreaux supplémentaires',t,fid);besoin=base+extra
   A=val(r'\*\*Offre A\*\*.*?(\d+) carreaux par boîte.*?(\d+) € par boîte',t,fid)
   B=val(r'\*\*Offre B\*\*.*?(\d+) carreaux par boîte.*?(\d+) € par boîte',t,fid)
   na=math.ceil(besoin/int(A[1]));nb=math.ceil(besoin/int(B[1]))
   out=(na*int(A[1])-besoin) if na*int(A[2])<=nb*int(B[2]) else (nb*int(B[1])-besoin)
  elif fid=='P9-M01':
   budget=n(r'budget disponible est de \*\*(\d+) €',t,fid)
   chosen=min(q[2]['attendu'],q[3]['attendu'])
   a=val(r'Chaque nouvelle parcelle nécessite (\d+) plants à (\d+) € et (\d+) € de matériel',t,fid)
   out=(budget-chosen)//(int(a[1])*int(a[2])+int(a[3]))
  elif fid=='P9-M03':
   extra=n(r'\*\*Nouveau défi :\*\* (\d+) personnes supplémentaires',t,fid)
   d=val(r'Chaque personne paie (\d+) € d.entrée.*?et (\d+) € pour le repas',t,fid)
   per=int(d[1])+int(d[2]);bprice=n(r'\*\*Transport B\*\*.*?- (\d+) € par personne transportée',t,fid)
   out=abs((q[2]['attendu']+extra*per)-(q[3]['attendu']+extra*(per+bprice)))
  elif fid=='P9-M05':
   shelf=n(r'bibliothécaire compte \*\*(\d+) mangas sur les étagères',t,fid)
   loans=val(r'\*\*(\d+) classes\*\* empruntent chacune \*\*(\d+) mangas',t,fid)
   back=shelf+int(loans[1])*int(loans[2])
   tail=val(r'retire encore (\d+) mangas usés.*?au moins (\d+) mangas.*?colis contiennent (\d+) mangas',t,fid)
   out=math.ceil(max(0,int(tail[2])-(back-int(tail[1])))/int(tail[3]))
  elif fid=='P8-M01':
   a=val(r'\*\*Nouveau défi :\*\* chaque club voudrait finalement recevoir au moins (\d+) €',t,fid)
   clubs=n(r'Les (\d+) clubs',t,fid)
   out=max(0,int(a[1])*clubs-q[3]['attendu'])
  elif fid=='P8-M07':
   rob, minutes, days=map(int,val(r'(\d+) robinets sont utilisés chacun (\d+) minutes par jour pendant (\d+) jours',t,fid).groups())
   dd=re.findall(r'laisse couler(?: seulement)? (\d+,\d+) litre',t)
   diff=(float(dd[0].replace(',','.'))-float(dd[1].replace(',','.')))*minutes*days
   obj=float(val(r'\*\*Nouveau défi :\*\* le collège veut désormais économiser au moins (\d+,\d+) L',t,fid)[1].replace(',','.'))
   out=math.ceil((obj-q[3]['attendu'])/diff-1e-8)
  elif fid=='P8-M06':
   nteams=n(r'Il y a (\d+) équipes participantes',t,fid)
   extra=n(r'\*\*Nouveau défi :\*\* (\d+) nouvelles équipes',t,fid)
   parts=re.findall(r'- (\d+) [^\n]+? à (\d+) €',t)
   assert len(parts)==2,(fid,parts)
   one=sum(int(x)*int(y) for x,y in parts)
   off=n(r'réduction de (\d+) €',t,fid);shipping=n(r'frais de livraison sont de (\d+) €',t,fid);budget=n(r'budget de \*\*(\d+) €',t,fid)
   out=max(0,(nteams+extra)*one-off+shipping-budget)
  elif fid=='P8-M03':
   fee=n(r'péage imprévu de (\d+) pièces',t,fid)
   prev=val(r'facturé uniquement sur le chemin (A|B)',t,fid)[1]
   a=q[1]['attendu']-(fee if prev=='A' else 0)
   bb=q[2]['attendu']-(fee if prev=='B' else 0)
   out=abs(a-bb)
  elif fid=='P8-M08':
   tour=q[0]['attendu']
   rythme=n(r'allure régulière de (\d+) minutes par kilomètre',t,fid)
   pause=n(r'font une pause de (\d+) minutes',t,fid)
   detour=float(val(r'détour d.observation de (\d+,\d+) km',t,fid)[1].replace(',','.'))
   limite=n(r'en \*\*(\d+) minutes au maximum',t,fid)
   out=max(0,int((limite-detour*rythme+pause)//(tour*rythme+pause)))
  elif fid=='P8-M10':
   hausse=n(r'annonce une hausse de (\d+) €',t,fid)
   hausse_compagnie=val(r'\*\*Nouveau défi :\*\* l.entreprise (A|B)',t,fid)[1]
   a=q[1]['attendu']+(hausse if hausse_compagnie=='A' else 0)
   bb=q[2]['attendu']+(hausse if hausse_compagnie=='B' else 0)
   out=abs(a-bb)
  elif fid=='P7-M23':
   target=n(r'prépare (\d+) fanions identiques',t,fid)
   d=val(r'deux côtés de (\d+) cm et un côté de (\d+) cm',t,fid)
   p=2*int(d[1])+int(d[2]);r=n(r'rouleaux de (\d+) m',t,fid)*100
   noeud=n(r'nœuds de (\d+) cm',t,fid)
   per_roll=r//p;last=target%per_roll or per_roll
   out=(r-last*p)//noeud
  eq(ans,out,fid);c[fid]+=1
print('VALIDATION INDÉPENDANTE OK:',sum(c.values()),'cas,',len(c),'modèles:',dict(sorted(c.items())))
