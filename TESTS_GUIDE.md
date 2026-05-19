# Guide débutant : utiliser les tests python

Ce guide explique, étape par étape, comment exécuter et interpréter les tests du projet.

Objectif : vérifier rapidement le bon fonctionnement de votre code et identifier précisément les erreurs à corriger.

---

## 1. À quoi servent les tests ?

Un test est une vérification automatique.

Lorsque vous lancez les tests, Python exécute plusieurs scénarios et compare les résultats obtenus aux résultats attendus.

Les tests vous permettent de :
- valider votre code après une modification
- éviter de casser une fonctionnalité qui fonctionnait déjà
- localiser plus rapidement l'origine d'une erreur

---

## 2. Où se trouvent les tests dans ce projet ?

Les tests sont regroupés dans le fichier `tests/test_caesar.py`.

Le projet utilise l'outil `pytest` (déjà listé dans `requirements.txt`).

---

## 3. Installation (à faire une seule fois)

Ouvrez un terminal dans le dossier du projet, puis exécutez :

```bash
python3 -m pip install -r requirements.txt
```

Détail de la commande :
- `python3` : lance l'interpréteur Python 3 installé sur votre machine.
- `-m` : demande à Python d'exécuter un module comme un programme.
- `pip` : module de gestion des paquets Python (installation de bibliothèques).
- `install` : action demandée à `pip` (installer des paquets).
- `-r requirements.txt` : indique à `pip` de lire la liste des paquets à installer depuis le fichier `requirements.txt`.

En pratique, cette commande installe automatiquement toutes les dépendances nécessaires au projet, en une seule étape.

Si cette commande ne fonctionne pas sur votre machine, essayez, à partir de votre projet (environnement virtuel) PyCharms :

```bash
pip3 install -r requirements.txt
```

---

## 4. Lancer les tests

Depuis la racine du projet, exécutez :

```bash
pytest -v
```

Explication :
- `pytest` : lance tous les tests
- `-v` : affiche le détail test par test (mode verbeux)

---

## 5. Comprendre le résultat

### Cas 1 : tous les tests passent

Vous verrez des lignes marquées `PASSED`, puis un résumé de ce type :

```text
5 passed in 0.10s
```

Cela signifie que tous les tests actuellement écrits sont validés.

### Cas 2 : un ou plusieurs tests échouent

Vous verrez une ou plusieurs lignes `FAILED`, avec un message indiquant :
- ce que le test attendait
- ce que votre code a réellement produit

Commencez par lire :
- le nom du test en échec
- la ligne concernée dans `tests/test_caesar.py`

Corrigez ensuite votre code, puis relancez :

```bash
pytest -v
```

---

## 6. Méthode de travail recommandée

Après chaque petite modification :

1. modifiez votre code
2. lancez `pytest -v`
3. corrigez si nécessaire
4. relancez les tests
5. validez vos changements uniquement lorsque les tests passent

Cette méthode limite les régressions et facilite le débogage.

---

## 7. Exécuter un seul test (plus rapide)

Pour exécuter un test précis :

```bash
pytest -v tests/test_caesar.py::test_cesar_round_trip
```

Pour exécuter uniquement le fichier de tests principal :

```bash
pytest -v tests/test_caesar.py
```

---

## 8. Ajouter vos propres tests (fortement recommandé)

Dans `tests/test_caesar.py`, ajoutez progressivement des tests pour couvrir :
- les majuscules et les minuscules
- la ponctuation et les espaces
- les accents et les caractères spéciaux
- les grandes clés positives et négatives
- les cas limites (chaîne vide, clé 0, etc.)

Un bon test est :
- court
- clair
- centré sur un seul comportement à vérifier

---

## 9. Problèmes fréquents et solutions

### Erreur : `ModuleNotFoundError: No module named pytest`

Installez les dépendances :

```bash
python3 -m pip install -r requirements.txt
```

### Erreur : `command not found: pytest`

Exécutez pytest via Python :

```bash
python3 -m pytest -v
```

### Plusieurs tests échouent

C'est normal si votre implémentation n'est pas terminée.
Procédez test par test : corrigez un point, relancez, puis continuez.

---

## 10. Rappel important

Les tests ne remplacent pas la réflexion algorithmique, mais ils permettent de travailler de façon plus fiable et plus structurée.

Règle simple :
- coder un peu
- tester
- corriger
- recommencer
