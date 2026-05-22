"""
MGA802 — Mini-Projet A : Chiffrement de César
Étudiants : Maxence Dubois, Jules Hua et Alexandre Hallonet
"""
import argparse
import unicodedata


def enlever_caracteres_speciaux(mot):
    """Retire les accents d'une chaîne de caractères selon la méthode du cours."""
    normalized_word = unicodedata.normalize('NFKD', mot)
    return "".join([char for char in normalized_word if not unicodedata.combining(char)])


def chiffrer(message: str, cle: int) -> str:
    """
    Chiffre un message avec le chiffrement de César selon une clé donnée.
    Conserve la casse (majuscules/minuscules) et ignore les caractères spéciaux.
    """
    # 1. On commence par enlever les accents du message !
    message = enlever_caracteres_speciaux(message)

    resultat = []
    for caractere in message:
        # Vérifie si le caractère est une lettre minuscule (a-z)
        if caractere.islower():
            # ord('a') vaut 97. On ramène la lettre à un index de 0 à 25.
            # On ajoute la clé, on applique le modulo 26 pour le dépassement.
            nouvel_index = (ord(caractere) - ord('a') + cle) % 26
            # On reconvertit l'index en lettre ASCII
            resultat.append(chr(nouvel_index + ord('a')))
        # Vérifie si le caractère est une lettre majuscule (A-Z)
        elif caractere.isupper():
            # ord('A') vaut 65. Même logique que pour les minuscules.
            nouvel_index = (ord(caractere) - ord('A') + cle) % 26
            resultat.append(chr(nouvel_index + ord('A')))
        # Si c'est un espace, de la ponctuation, un chiffre ou un accent
        else:
            resultat.append(caractere)
    # On rassemble la liste de caractères en une seule chaîne de texte
    return "".join(resultat)


def dechiffrer(message: str, cle: int) -> str:
    """
    Déchiffre un message chiffré par César.
    Astuce : déchiffrer revient à chiffrer en inversant le sens du décalage.
    """
    return chiffrer(message, -cle)


def enigma_chiffrer(message: str, cles: tuple) -> str:
    """
    Chiffre un message avec le chiffrement Enigma César.
    La clé est un tuple de 3 entiers appliqués en rotation sur chaque lettre.
    Les caractères non-alphabétiques sont conservés sans décalage de rotor.

    Exemple : enigma_chiffrer("MAISON", (7, 16, 9)) -> "TQRZEW"
    """
if len(cles) != 3 and all(isinstance(cle, int) for cle in cles):
    raise ValueError(f"Erreur pour renseigner le nombre de variables ! \n"
                     "Il faut exactement 3 entiers pour les clés. Merci. ")
elif len(cles) != 3 :
    raise ValueError(f"Erreur pour renseigner le type et le nombre de variables ! \n"
                     "Il faut exactement 3 entiers pour les clés. Merci. ")
elif not all(isinstance(cle, int) for cle in cles) :
    raise ValueError(f"Erreur pour renseigner le type de variables ! \n"
                     "Il faut 3 entiers pour les clés. Merci. ")

resultat = []
    index_rotor = 0  # Tourne de 0 à 2, uniquement sur les lettres

    for caractere in message:
        if caractere.isalpha():
            cle_courante = cles[index_rotor % 3]
            resultat.append(chiffrer(caractere, cle_courante))
            index_rotor += 1
        else:
            resultat.append(caractere)

    return "".join(resultat)

"""
    elif not all(isinstance(cle, (int, float)) for cle in cles) and len(cles) != 3 :
        return f"\033[31m{("Erreur pour renseigner le type et le nombre de variables ! \n"
                           "Il faut des entiers ou des floats et 3 valeurs pour les clés. Merci. ")}\033[0m"
    elif len(cles) == 3 :
        return f"\033[31m{("Erreur pour renseigner le type de variables ! \n"
                           "Il faut des entiers ou des floats pour les clés. Merci. ")}\033[0m"
    else :
        return f"\033[31m{("Erreur pour renseigner le nombre de variables ! \n"
                           "Il faut 3 valeurs pour les clés. Merci. ")}\033[0m"
"""

def enigma_dechiffrer(message: str, cles: tuple) -> str:
    """
    Déchiffre un message chiffré par Enigma César.
    Astuce : déchiffrer revient à appliquer les clés opposées.
    """
    if len(cles) != 3:
        raise ValueError("La clé Enigma César doit contenir exactement 3 entiers.")

    cles_inverses = tuple(-c for c in cles)
    return enigma_chiffrer(message, cles_inverses)


def _parse_cle(texte: str):
    """Convertit l'argument --cle en clé utilisable.

    Cette fonction analyse la clé fournie par l'utilisateur en ligne de commande
    et la transforme en type Python approprié :
    - César           : un entier, ex. "42" ou "-42"
    - Enigma César    : trois entiers séparés par des tirets, ex. "7-16-9"

    Paramètre :
        texte (str) : la chaîne saisie par l'utilisateur après --cle.

    Retour :
        int   : une clé entière pour César
        tuple : un tuple de 3 entiers pour Enigma César

    Exemple :
        _parse_cle("42")    → 42      (int)
        _parse_cle("7-16-9") → (7, 16, 9) (tuple)
    """
    # Vérifier s'il y a un tiret dans la clé (sauf si c'est juste un signe négatif).
    # lstrip("-") enlève tous les tirets au début, pour distinguer :
    #   "-42"    (entier négatif, pas de tiret après le signe)
    #   "7-16-9" (trois nombres séparés par des tirets)
    if "-" in texte.lstrip("-"):
        # C'est une clé Enigma César : on coupe au niveau des "-" et on convertit en entiers.
        parties = texte.split("-")
        # Cas particulier : gérer les valeurs négatives dans le tuple (ex. "-7-16-9")
        # split("-") sur "-7-16-9" donne ['', '7', '16', '9'] → on filtre les chaînes vides
        entiers = [int(x) for x in parties if x != ""]
        # Si le texte commence par "-", le premier nombre est négatif
        if texte.startswith("-"):
            entiers[0] = -entiers[0]
        return tuple(entiers)
    # Sinon, c'est une clé César simple : on convertit en entier.
    return int(texte)


def main(argv=None):
    """Point d'entrée principal du programme en ligne de commande."""
    # === ÉTAPE 1 : Créer et configurer le parseur d'arguments ===
    parser = argparse.ArgumentParser(
        description="Mini-Projet A : chiffrement de César / Enigma César.")

    # === ÉTAPE 2 : Définir les arguments attendus ===
    # Argument positionnel "action" : l'opération à effectuer.
    parser.add_argument(
        "action",
        choices=["chiffrer", "dechiffrer", "enigma"],
        help="Opération à effectuer (chiffrer, dechiffrer ou enigma).")
    # Argument positionnel "message" : le texte OU le chemin du fichier à traiter.
    parser.add_argument(
        "message",
        help="Texte à traiter ou chemin du fichier texte (si --fichier est activé).")
    # Argument optionnel "--cle" (abréviation "-c") : la clé de chiffrement.
    # required=False pour permettre le mode brute-force sans clé.
    parser.add_argument(
        "-c", "--cle", required=False,
        help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")
    # Option pour indiquer qu'on traite un fichier
    parser.add_argument(
        "-f", "--fichier", action="store_true",
        help="Indique que le paramètre 'message' est un chemin vers un fichier texte.")
    # Option pour activer le mode brute-force
    parser.add_argument(
        "--brute-force", action="store_true",
        help="Active le mode force brute pour deviner la clé (César ou Enigma).")

    # === ÉTAPE 3 : Analyser les arguments ===
    args = parser.parse_args(argv)

    # Validation : on a besoin soit d'une clé, soit du mode brute-force
    if not args.cle and not args.brute_force:
        parser.error("Vous devez fournir une clé avec --cle OU activer le mode --brute-force.")

    # === ÉTAPE 4 : Gestion de la source du texte (console vs fichier) ===
    if args.fichier:
        try:
            with open(args.message, 'r', encoding='utf-8') as f:
                texte_a_traiter = f.read()
        except FileNotFoundError:
            print(f"Erreur : le fichier '{args.message}' est introuvable.")
            return
    else:
        texte_a_traiter = args.message

    # === ÉTAPE 5 : Convertir la clé (si elle est fournie) ===
    cle = _parse_cle(args.cle) if args.cle else None

    # === ÉTAPE 6 : Choisir et exécuter l'opération ===
    if args.brute_force:
        #TODO: implémenter le mode brute-force (César et Enigma César)
        resultat = "[Mode Brute-Force non encore implémenté]"
    else:
        if args.action == "chiffrer":
            resultat = chiffrer(texte_a_traiter, cle)
        elif args.action == "dechiffrer":
            resultat = dechiffrer(texte_a_traiter, cle)
        else:  # args.action == "enigma"
            resultat = enigma_chiffrer(texte_a_traiter, cle)

    # === ÉTAPE 7 : Afficher le résultat ===
    print(resultat)

enigma_chiffrer("Erreur pas clé pas 3 nbr.",(1,2))

if __name__ == "__main__":
    main()