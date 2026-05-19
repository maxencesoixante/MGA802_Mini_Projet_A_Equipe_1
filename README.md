# MGA802 — Mini-Projet A : Chiffrement de César

Dépôt-modèle (template) pour le Mini-Projet A du cours **MGA802 — Introduction à
la programmation avec Python** à l'ÉTS.

> **Étudiants :** cliquez sur **« Use this template »** (en haut à droite) pour
> créer le dépôt de votre équipe. **Ne forkez pas** ce dépôt directement.

---

## À faire

Implémenter un programme Python qui chiffre et déchiffre du texte selon
**deux modes** :

1. Le **chiffrement de César** classique (clé = un seul entier)
2. Le **chiffrement Enigma César** (clé = trois entiers rotatifs)

### Fonctionnalités attendues

Pour **chacun des deux modes** :

1. Chiffrement / déchiffrement d'un message saisi dans la **console**
2. Chiffrement / déchiffrement d'un **fichier texte** (chemin fourni par
   l'utilisateur)
3. Acceptation de **n'importe quelle clé entière** (positive ou négative).
   Pour Enigma César : clé de **exactement 3 nombres** (ex : `42-21-7`).
4. Mode **brute-force** : retrouver la clé d'un message chiffré par chiffrement de César ou chiffrement Enigma César
5. **Messages clairs** à l'utilisateur (introduction, requêtes, info, erreurs)

> Le brute-force d'Enigma César balaie **26³ = 17 576 combinaisons**,
> soyez efficaces pour votre stratégie et mesurez le temps que cela prend (sur la même machine) pour différentes solutions dans votre rapport.

### Caractères utilisés pour tester

**César :**

| Clé | Entrée                  | Sortie attendue        |
|----:|-------------------------|------------------------|
| 42  | `Veni, vidi, vici!`     | `Ludy, lyty, lysy!`    |
| -42 | `Veni, vidi, vici!`     | `Foxs, fsns, fsms!`    |

**Enigma César :**

| Clé        | Entrée     | Sortie attendue |
|------------|------------|-----------------|
| `(7,16,9)` | `MAISON`   | `TQRZEW`        |

---

## Comment commencer

1. Cliquez **« Use this template »** (boutton vert en haut à droite de la fenêtre Github) → choisissez un nom pour le dépôt de
   votre équipe (par ex. `equipe-N-caesar-20262`)
2. **Ajoutez vos coéquipiers** comme collaborateurs (Settings → Collaborators). N'oubliez pas que vos collègues peuvent aussi forker le dépôt et proposer des mises à jour par PR.
3. Clonez le dépôt localement : `git clone <url>`
4. Discutez ensemble :
   - Comment découper le code en **fonctions et modules** ?
   - Qui fait quoi ?
   - Quelle stratégie pour le brute-force ?
5. Travaillez toujours avec des **branches** (`git checkout -b ma-fonctionnalite`) et faites
   des **pull requests** pour réviser le code de vos coéquipiers.

---

## Utilisation en ligne de commande

En plus du mode console interactif, le programme s'utilise directement depuis le
terminal grâce au module standard [`argparse`](https://docs.python.org/3/library/argparse.html).
Le point d'entrée (`main()` + `if __name__ == "__main__":`) est déjà fourni
dans `main.py` ; il appelle vos fonctions une fois implémentées.

```bash
python main.py chiffrer   "Veni, vidi, vici!" --cle 42
python main.py dechiffrer "Ludy, lyty, lysy!" --cle 42
python main.py enigma     "MAISON"            --cle 7-16-9
```

- `action` : `chiffrer`, `dechiffrer` ou `enigma`
- `message` : le texte à traiter (entre guillemets)
- `-c` / `--cle` : un entier pour César (ex. `42`, `-42`), ou trois entiers
  séparés par des tirets pour Enigma César (ex. `7-16-9`)

Affichez l'aide générée automatiquement avec :

```bash
python main.py -h
```

> Libre à vous d'ajouter d'autres arguments (ex. `--fichier`, `--brute-force`).

### Mesurer le temps d'exécution (brute-force)

Pour le rapport, mesurez le temps de votre brute-force avec la bibliothèque
standard :

```python
from time import perf_counter
tic = perf_counter()
# ... votre brute-force ...
print(f"Temps d'execution: {perf_counter() - tic} [s]")
```

ou, pour une mesure répétée plus fiable, avec
[`timeit`](https://docs.python.org/3/library/timeit.html) :

```python
from timeit import timeit
timeit('brute_force_cesar(message_chiffre)', globals=globals(), number=100)
```

> Indiquez la machine utilisée dans le rapport (les temps ne sont comparables
> que sur la même machine).

---

## Livrables (rappel)

- Le code source (Python)
- Ce `README.md` mis à jour avec :
  - Description du programme
  - Instructions d'installation et d'exécution
  - Auteurs (membres de l'équipe)
  - Choix de conception (par ex. comment vous gérez les majuscules / accents)
- Un dossier `tests/` avec quelques tests unitaires
- Un **rapport écrit de 3 pages max** (PDF, commité au dépôt, pas de page de garde, pas de conclusion, pas d'introduction) couvrant :
  structure, algorithmes, évaluation de performance, distribution des tâches

> Voir `Mini_Projet_A_Specs.md` (Moodle) pour le détail complet.

---

## Critères d'évaluation (résumé)

| Catégorie           | Points |
|---------------------|-------:|
| Code fonctionnel    |   3/10 |
| Tâche accomplie     |   2/10 |
| Commentaires        |   1/10 |
| Noms de variables   |   2/10 |
| Style               |   2/10 |

Voir `Mini_Projet_A_Grading_Rubric.md` (Moodle) pour les critères détaillés.

---

## Conseils

- Lisez la documentation Python sur le module
  [`string`](https://docs.python.org/3/library/string.html)
- Consultez le guide d'utilisation des tests : [`TESTS_GUIDE.md`](TESTS_GUIDE.md)
- Pour la lecture / écriture de fichiers texte, utilisez `with open(..., encoding="utf-8") as f:`
- **Testez votre code avant chaque commit**
- **Messages de commit clairs** (`feat: ...`, `fix: ...`, `docs: ...`)

Bonne programmation !
