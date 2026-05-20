# MGA802 — Mini-Projet A : Chiffrement de César

> **Cours :** MGA802 — Introduction à la programmation avec Python (ÉTS, Été 2026)
> **Équipe 1 :** Maxence Dubois, Jules Hua, Alexandre Hallonet

---

## Description

Ce programme Python implémente deux modes de chiffrement par substitution inspirés du chiffrement historique de César et de la machine Enigma :

- **Chiffrement de César** : chaque lettre est décalée d'un nombre fixe de positions dans l'alphabet (clé = 1 entier).
- **Chiffrement Enigma César** : variante où trois décalages sont appliqués en rotation, lettre par lettre (clé = 3 entiers séparés par des tirets, ex. `7-16-9`).

Pour chacun des deux modes, le programme permet :

1. De chiffrer et déchiffrer un message saisi directement dans la console ou en ligne de commande.
2. De chiffrer et déchiffrer le contenu d'un fichier texte (chemin fourni par l'utilisateur).
3. De retrouver la clé d'un message chiffré par **force brute** (César : 26 clés ; Enigma César : 26³ = 17 576 combinaisons).

---

## Installation

**Prérequis :** Python 3.8 ou supérieur.

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd <nom-du-depot>

# 2. Installer les dépendances (pytest pour les tests)
pip install -r requirements.txt
```

Aucune dépendance externe n'est requise pour l'exécution du programme lui-même : toutes les bibliothèques utilisées (`argparse`, `unicodedata`, `string`, `time`, `timeit`) font partie de la bibliothèque standard Python.

---

## Utilisation

### Mode interactif (console)

```bash
python main.py
```

Le programme vous guide pas à pas : choix du mode, de l'opération et de la clé.

### Ligne de commande

```bash
# Chiffrement de César
python main.py chiffrer   "Veni, vidi, vici!" --cle 42
python main.py dechiffrer "Ludy, lyty, lysy!" --cle 42

# Enigma César
python main.py enigma "MAISON" --cle 7-16-9

# Traitement d'un fichier texte
python main.py chiffrer message.txt --cle 13 --fichier
python main.py dechiffrer message_chiffre.txt --cle 13 --fichier

# Force brute (sans clé)
python main.py dechiffrer "Ludy, lyty, lysy!" --brute-force
python main.py enigma     "TQRZEW"            --brute-force

# Afficher l'aide
python main.py -h
```

**Arguments :**

| Argument | Description |
|---|---|
| `action` | `chiffrer`, `dechiffrer` ou `enigma` |
| `message` | Texte à traiter (entre guillemets) ou chemin de fichier si `--fichier` est activé |
| `-c` / `--cle` | Clé entière pour César (`42`, `-42`) ou trois entiers séparés par un tiret pour Enigma César (`7-16-9`) |
| `-f` / `--fichier` | Indique que `message` est un chemin vers un fichier texte |
| `--brute-force` | Active la recherche exhaustive de la clé (remplace `--cle`) |

---

## Exemples de chiffrement

**César :**

| Clé | Entrée | Sortie attendue |
|---:|---|---|
| 42 | `Veni, vidi, vici!` | `Ludy, lyty, lysy!` |
| -42 | `Veni, vidi, vici!` | `Foxs, fsns, fsms!` |

**Enigma César :**

| Clé | Entrée | Sortie attendue |
|---|---|---|
| `(7, 16, 9)` | `MAISON` | `TQRZEW` |

---

## Structure du projet

```
.
├── tests/
│   └── test_caesar.py       # Tests unitaires (pytest)
├── .gitignore               # Fichiers et dossiers ignorés par Git
├── LICENSE                  # Licence du projet
├── README.md                # Ce fichier
├── TESTS_GUIDE.md           # Guide d'utilisation des tests
├── main.py                  # Point d'entrée : fonctions de chiffrement + CLI (argparse)
├── message.txt              # Fichier texte d'exemple pour les tests de fichier
└── requirements.txt         # Dépendances (pytest)
```

Le code est organisé autour d'un seul module `main.py` qui regroupe :

- `enlever_caracteres_speciaux(mot)` — normalisation des accents via `unicodedata`
- `chiffrer(message, cle)` — chiffrement de César
- `dechiffrer(message, cle)` — déchiffrement de César (appel symétrique à `chiffrer`)
- `enigma_chiffrer(message, cles)` — chiffrement Enigma César (3 rotors)
- `_parse_cle(texte)` — conversion de la clé en `int` ou `tuple`
- `main(argv)` — interface ligne de commande via `argparse`

---

## Choix de conception

**Gestion des majuscules et minuscules :** La casse est conservée. Les lettres minuscules restent minuscules et les majuscules restent majuscules après chiffrement.

**Gestion des accents :** Les accents sont retirés avant le chiffrement grâce à `unicodedata.normalize('NFKD', ...)` et au filtrage des caractères combinants. Par exemple, `é` devient `e` avant d'être chiffré. Ce choix est documenté dans le README et reflété dans les tests.

**Caractères non-alphabétiques :** Les espaces, chiffres et signes de ponctuation sont conservés tels quels — ils ne sont pas décalés et ne font pas avancer le compteur de rotor en mode Enigma César.

**Clés arbitraires :** Toute clé entière est acceptée (positive, négative ou nulle). Le modulo 26 garantit un comportement correct pour les clés très grandes ou hors de \[-25, 25\].

**Déchiffrement :** La fonction `dechiffrer` réutilise `chiffrer` avec la clé opposée (`-cle`), ce qui évite la duplication de code.

**Enigma César — avancement du rotor :** Le compteur de rotor n'avance que sur les lettres alphabétiques. Les caractères spéciaux ne consomment pas de position de clé, conformément à la spec.

---

## Tests

```bash
# Lancer tous les tests
pytest -v

# Si pytest n'est pas dans le PATH
python -m pytest -v
```

Les tests couvrent les cas officiels de la spec ainsi que des cas supplémentaires :
- Majuscules et minuscules
- Ponctuation, espaces, accents et caractères spéciaux
- Clé 0 (identité) et très grandes clés positives et négatives
- Symétrie chiffrement/déchiffrement (round-trip)
- Force brute César et Enigma César
- Rejet d'une clé Enigma qui n'a pas exactement 3 entiers
- Chaîne vide et autres cas limites

---

## Auteurs et distribution des tâches

| Membre | Contributions principales |
|---|---|
| **Maxence Dubois** | Chiffrement/déchiffrement de César, gestion des accents, tests unitaires César |
| **Jules Hua** | Chiffrement Enigma César, interface `argparse` (CLI), lecture/écriture de fichiers |
| **Alexandre Hallonet** | Mode force brute (César et Enigma César), mesures de performance, rapport |

Chaque membre a également revu et testé le code des autres via des branches Git et des pull requests.