# Triage Automatique des Tickets IT

## Resume
Ce depot organise un prototype academique et professionnel de Machine Learning pour le triage automatique des tickets IT en portugais bresilien. L'application combine un pipeline `Scikit-Learn` entraine sur des tickets synthetiques avec une interface `Streamlit` pour la classification simultanee de la categorie et de la priorite.

## Probleme traite
Les centres de support recoivent souvent des descriptions d'incidents et de demandes courtes, bruitees et heterogenes. Ce projet vise a reduire le temps de routage initial en proposant une classification automatique basee sur des mots-cles techniques ITSM, sans dependre de phrases completes ni d'un contexte narratif long.

## Architecture de l'application
Le flux principal est compose de :

- saisie de texte dans `app.py` ;
- chargement de l'artefact `pipeline_itsm.joblib` avec `@st.cache_resource` ;
- vectorisation avec `TfidfVectorizer` en unigrammes ;
- suppression manuelle des stop words portugais ;
- classification multi-sortie avec `MultiOutputClassifier(RandomForestClassifier)` ;
- retour simultane de la `categorie` et de la `priorite`.

Le diagramme d'architecture est disponible dans `assets/diagrams/architecture.mmd`.

## Flux de classification
1. L'utilisateur saisit des mots-cles courts de l'incident, par exemple `vpn falha mfa dns`.
2. Le texte est normalise et transforme en vecteur TF-IDF.
3. Le classifieur multi-sortie estime la categorie operationnelle et la priorite du ticket.
4. L'interface affiche immediatement le resultat pour aider au routage initial.

## Types d'entree et de sortie
Entree :

- texte libre court avec jargon ITSM ;
- exemples : `reset senha ad`, `tela azul memoria`, `outlook erro smtp`.

Sortie :

- `categoria` : classe fonctionnelle predite ;
- `prioridade` : niveau initial de traitement predit.

## Installation locale
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python train.py
streamlit run app.py
```

## Deploiement Streamlit Cloud
1. Publier le depot sur GitHub.
2. Configurer l'application Streamlit Cloud vers `app.py`.
3. Verifier que `requirements.txt` se trouve a la racine du depot.
4. Definir, si necessaire, des variables a partir de `.env.example` uniquement pour des environnements de demonstration.
5. Redeployer a chaque modification du pipeline ou des dependances.

## Methodologie d'entrainement
L'entrainement utilise un jeu de donnees synthetique avec du jargon de support technique et d'operations IT. Le fichier `train.py` separe explicitement le texte des labels afin d'eviter toute fuite de donnees entre attributs et cibles.

### Representation textuelle
Le module textuel a ete concu pour privilegier la robustesse lexicale :

- normalisation en minuscules ;
- suppression des accents ;
- `TfidfVectorizer` avec unigrammes uniquement ;
- liste manuelle de stop words portugais ciblee sur les connecteurs et termes faiblement informatifs.

Cette configuration privilegie les mots-cles techniques courts et reduit le biais de classification base sur des formulations longues ou des phrases completes trop specifiques.

### Modele
Le classifieur utilise `MultiOutputClassifier` avec `RandomForestClassifier`, ce qui permet une inference conjointe de la categorie et de la priorite dans un seul pipeline.

## Resultats
L'interface de demonstration ci-dessous enregistre une classification executee localement par l'application Streamlit.

![Classification Streamlit](../../assets/screenshots/streamlit-classification.png)

## Limitations du modele

- la base d'entrainement est synthetique et ne remplace pas des tickets reels curates ;
- il n'existe pas encore d'evaluation statistique formelle de type apprentissage-validation-test ;
- le modele n'integre ni contexte temporel, ni historique utilisateur, ni relations entre incidents ;
- le comportement depend fortement de la couverture du vocabulaire technique dans la base synthetique.

## Risques ethiques dans les environnements de support

- des classifications incorrectes peuvent entrainer un routage inadequat et augmenter le temps de reponse ;
- les vocabulaires synthetiques peuvent refleter les biais du curateur et sous-representer certaines equipes ou certains services ;
- les predictions automatiques ne doivent pas remplacer l'analyse humaine dans des scenarios critiques ;
- les journaux, exemples et captures d'ecran doivent rester sanitises pour eviter toute exposition operationnelle.

## Prochaines etapes

- ajouter une evaluation quantitative avec des metriques par classe ;
- introduire des tests automatises de regression pour le pipeline ;
- incorporer une configuration externe des classes et priorites ;
- ajouter une API d'inference pour l'integration avec des plateformes ITSM ;
- evaluer des modeles lineaires et des embeddings legers a titre de comparaison.

## References BibTeX
```bibtex
@misc{python,
  author       = {{Python Software Foundation}},
  title        = {Python Language Reference},
  year         = {2026},
  howpublished = {\url{https://www.python.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{numpy,
  author       = {{NumPy Developers}},
  title        = {NumPy},
  year         = {2026},
  howpublished = {\url{https://numpy.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{joblib,
  author       = {{joblib developers}},
  title        = {joblib: Python utilities for lightweight pipelining},
  year         = {2026},
  howpublished = {\url{https://joblib.readthedocs.io/}},
  note         = {Accessed 2026-06-07}
}

@misc{scikit-learn,
  author       = {{Scikit-learn developers}},
  title        = {Scikit-learn: Machine Learning in Python},
  year         = {2026},
  howpublished = {\url{https://scikit-learn.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{streamlit,
  author       = {{Streamlit Inc.}},
  title        = {Streamlit: The fastest way to build and share data apps},
  year         = {2026},
  howpublished = {\url{https://streamlit.io/}},
  note         = {Accessed 2026-06-07}
}
```
