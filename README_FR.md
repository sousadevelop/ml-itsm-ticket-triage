# Tri des Tickets de Support Informatique

## Résumé
Ce dépôt implémente un prototype de tri automatique des tickets de support en technologies de l’information en portugais brésilien, avec un focus sur la classification simultanée de la catégorie et de la priorité à partir de descriptions textuelles libres. La solution finale combine `Scikit-Learn` pour l’entraînement et la persistance du modèle avec `Streamlit` pour l’interface interactive d’inférence.

## 1. Vue d’ensemble
Le flux du projet a été organisé en deux étapes principales :

1. `train.py` crée un ensemble synthétique d’exemples en pt-BR, ajuste un pipeline supervisé et enregistre l’artefact `pipeline_itsm.joblib`.
2. `app.py` charge le pipeline enregistré avec `joblib`, expose l’interface via `Streamlit` et exécute l’inférence en temps réel.

Lorsque le fichier du modèle n’est pas présent dans le répertoire racine, l’application utilise une routine locale de démonstration uniquement pour conserver l’interface fonctionnelle. En conditions normales d’exécution, la prédiction doit être effectuée exclusivement par l’artefact entraîné.

## 2. Architecture finale
La solution finale adopte la chaîne de traitement suivante :

- saisie textuelle du ticket ;
- vectorisation avec `TfidfVectorizer` en unigrammes ;
- suppression manuelle des stop words en portugais ;
- classification multi-label avec `MultiOutputClassifier(RandomForestClassifier)` ;
- persistance du pipeline avec `joblib.dump` ;
- chargement à la demande dans `Streamlit` avec `@st.cache_resource` ;
- affichage des résultats de catégorie et de priorité dans des composants `metric`.

En pratique, le modèle reçoit uniquement la description de l’incident comme entrée. Les étiquettes de sortie sont conservées dans des colonnes séparées afin d’éviter toute fuite d’information et de préserver la séparation entre attributs et cible.

## 3. Structure des fichiers
```text
.
├── app.py
├── train.py
├── pipeline_itsm.joblib
├── README.md
└── .gitignore
```

Remarque : le fichier `pipeline_itsm.joblib` est l’artefact entraîné consommé par l’application. Le fichier `.gitignore` a été configuré pour isoler les environnements virtuels, les caches, les dépendances temporaires et les répertoires de données brutes.

## 4. Méthodologie
### 4.1 Base synthétique
L’entraînement utilise un ensemble synthétique en portugais brésilien contenant des descriptions typiques de tickets de support, avec des paires de sortie pour `categoria` et `prioridade`. L’objectif est de démontrer une chaîne d’inférence reproductible, et non de remplacer des bases institutionnelles réelles.

### 4.2 Représentation textuelle
Les descriptions sont transformées par `TfidfVectorizer` avec :

- normalisation en minuscules ;
- suppression des accents ;
- unigrammes uniquement ;
- une liste manuelle de stop words portugaises centrée sur les connecteurs et les termes fonctionnels peu informatifs.

Ce choix favorise les mots-clés techniques courts et réduit la dépendance aux phrases complètes, ce qui tend à améliorer la robustesse face aux variations de formulation et à diminuer le biais introduit par les connecteurs ou les formulations génériques.

### 4.3 Modèle supervisé
Le classificateur utilisé est `MultiOutputClassifier` encapsulant `RandomForestClassifier`. Cette combinaison permet de prédire plusieurs cibles à partir du même texte d’entrée, sans exiger d’architectures externes distinctes pour chaque étiquette.

### 4.4 Persistance et inférence
Après l’ajustement, le pipeline est enregistré sur disque avec `joblib`. L’application Streamlit réutilise le même artefact, évitant toute divergence entre l’entraînement et l’usage. Le chargement est mis en cache avec `@st.cache_resource` afin de réduire le coût d’initialisation.

## 5. Contrôle du data leakage
Le code d’entraînement a été structuré pour minimiser les fuites de données :

- seul le champ textuel `texto` est utilisé comme entrée du modèle ;
- les sorties `categoria` et `prioridade` restent séparées comme cibles ;
- la vectorisation fait partie du pipeline, ce qui évite la réutilisation abusive de transformations déjà ajustées sur des données extérieures au flux ;
- l’ensemble employé est synthétique et fermé, sans mélange avec des données de test issues de la production.

Comme limite méthodologique, ce dépôt n’implémente pas de séparation formelle entre entraînement, validation et test, ni de validation croisée. Dans une soumission expérimentale complète, cette étape devrait être ajoutée avec des métriques rapportées séparément.

## 6. Exécution
### 6.1 Environnement
Python 3.11 ou supérieur est recommandé, avec les bibliothèques suivantes :

- `scikit-learn`
- `streamlit`
- `joblib`
- `numpy`

### 6.2 Entraînement
```bash
python train.py
```

Cette commande génère ou met à jour `pipeline_itsm.joblib` dans le répertoire racine.

### 6.3 Application web
```bash
streamlit run app.py
```

Le navigateur affichera un formulaire pour saisir la description du ticket, puis renverra la catégorie et la priorité prédites par le pipeline.

### 7. Résultat

Lors de l'exécution du système, le résultat devrait être celui affiché ci-dessous :

![Interface de triage des appels - Résultat de la classification](assets/screenshots/triage-ticket.jpeg)

Lien pour consulter le déploiement officiel de la preuve de concept (PoC) via le Web : https://triage-ai.streamlit.app/

## 8. Limitations
Le système a été conçu comme une preuve de concept et présente des limites importantes :

- la base d’entraînement est synthétique et réduite ;
- la généralisation au langage réel d’exploitation n’a pas encore été mesurée ;
- il n’existe pas de calibration explicite des probabilités ;
- il n’existe pas d’intégration avec une file ITSM, une API d’entreprise ou un stockage persistant ;
- le fallback simulé n’existe que pour la démonstration, et non pour un usage opérationnel.

## 9. Reproductibilité
Pour une reproductibilité minimale :

- exécutez `train.py` pour générer l’artefact entraîné ;
- conservez la même version de Python et des bibliothèques ;
- préservez le fichier `pipeline_itsm.joblib` lorsque vous souhaitez reproduire l’inférence déjà ajustée ;
- consignez les versions des dépendances dans un fichier d’environnement ou `requirements.txt` si la soumission exige une traçabilité supplémentaire.

## 10. Références BibTeX
```bibtex
@misc{scikit-learn,
  author       = {{Scikit-learn developers}},
  title        = {Scikit-learn: Machine Learning in Python},
  year         = {2026},
  howpublished = {\url{https://scikit-learn.org/}},
  note         = {Consulté le 07 juin 2026}
}

@misc{streamlit,
  author       = {{Streamlit Inc.}},
  title        = {Streamlit: The fastest way to build and share data apps},
  year         = {2026},
  howpublished = {\url{https://streamlit.io/}},
  note         = {Consulté le 07 juin 2026}
}

@misc{joblib,
  author       = {{joblib developers}},
  title        = {joblib: Python utilities for lightweight pipelining},
  year         = {2026},
  howpublished = {\url{https://joblib.readthedocs.io/}},
  note         = {Consulté le 07 juin 2026}
}

@misc{python,
  author       = {{Python Software Foundation}},
  title        = {Python Language Reference},
  year         = {2026},
  howpublished = {\url{https://www.python.org/}},
  note         = {Consulté le 07 juin 2026}
}
```

## 11. Note de traduction
La traduction vers une autre langue doit être réalisée à partir de ce README en français, en préservant la structure modulaire et les citations BibTeX.
