# MathiCap — Dépôt de l'application

Application pédagogique de mathématiques (Streamlit, Supabase).

## Application
- `app.py` : interface, génération des séries, sauvegarde et reprise
- `banque_priorites.py` : banque des exercices du chapitre Opérations
- `mathicap_*.py` et `auth_persistante.py` : composants métier et authentification
- `requirements.txt` : dépendances de déploiement

## Tests automatiques (22 novembre 2026)
La commande `python -m unittest discover -p "test_*.py" -v`
exécute la suite actualisée. Elle vérifie les 26 modèles N7, 24 modèles N8
et 26 modèles N9, avec respectivement 4, 5 et 5 questions, ainsi que la
diversité, la reproductibilité, l'historique des tirages et la structure des
réponses. Trois modèles représentatifs font aussi l'objet de recalculs
indépendants à partir de leurs énoncés (100 tirages chacun).

Les contrôles structurels ne prouvent pas que tous les calculs des 76 modèles
sont exacts. Le recalcul indépendant doit encore être élargi aux autres modèles.

## Archives
- `archives/tests_historiques/` : six anciens tests conservés à titre
  documentaire. Ils étaient adaptés à des modèles/énoncés précédents et ne
  doivent pas être exécutés comme contrôle de la banque actuelle.
- `archives/outils_historiques/` : référentiel V1 et scripts historiques
  non importés dans l'application. Ils ne sont pas supprimés de Git.

Cette maintenance ne modifie ni `app.py`, ni `banque_priorites.py`,
ni l'authentification, ni les données Supabase.
