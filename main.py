"""
MGA802 — Mini-Projet A : Chiffrement de César
Étudiants : Maxence Dubois, Jules Hua et Alexandre Hallonet
"""
import argparse
import unicodedata
from time import perf_counter

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
        raise ValueError("Erreur pour renseigner le nombre de variables ! \n"
                         "Il faut exactement 3 entiers pour les clés. Merci. ")
    elif len(cles) != 3 :
        raise ValueError("Erreur pour renseigner le type et le nombre de variables ! \n"
                         "Il faut exactement 3 entiers pour les clés. Merci. ")
    elif not all(isinstance(cle, int) for cle in cles) :
        raise ValueError("Erreur pour renseigner le type de variables ! \n"
                         "Il faut 3 entiers pour les clés. Merci. ")

    resultat = []
    index_rotor = 0  # Tourne de 0 à 2, uniquement sur les lettres

    # if all(isinstance(cle, int) for cle in cles) and len(cles) == 3:
    for caractere in message:
        if caractere.isalpha():
            cle_courante = cles[index_rotor % 3]
            resultat.append(chiffrer(caractere, cle_courante))
            index_rotor += 1
        else:
            resultat.append(caractere)

    return "".join(resultat)

def enigma_dechiffrer(message: str, cles: tuple) -> str:
    """
    Déchiffre un message chiffré par Enigma César.
    Astuce : déchiffrer revient à appliquer les clés opposées.
    """
    if len(cles) != 3:
        raise ValueError("La clé Enigma César doit contenir exactement 3 entiers.")

    cles_inverses = tuple(-c for c in cles)
    return enigma_chiffrer(message, cles_inverses)

def noter_decryptage(message: str) -> int :
    """
    Notation d'un décryptage simple et rapide pour détecter du français.
    Plus le score est élevée, plus le texte paraît bon

    La détection fonctionne sur les 10 lettres les plus fréquentes de la langue française :
    e, s, a, i, t, n, r, u, l et o source : https://www.apprendre-en-ligne.net/crypto/stat/batonsfr2.gif
    Le score de chaque lettre sera faible (On divise par 10 par rapport à la source citée)
    On va aussi effectuer un test sur la quantité de voyelles dans un texte en utilisant les mêmes données.
    D'après les données, les voyelles représentent environ 45 % des lettres dans un texte.
    On va ajouter une pénalité si on est en dehors de l'intervalle [25;65]

    La détection fonctionne également avec quelques mots très courants dans la langue française :
    le/la/l’, de, un/une, à (devient a), et, il, je, ne, pas, en
    source : https://www.ccfs-sorbonne.fr/quels-sont-les-mots-les-plus-utilises-de-la-langue-francaise/
    Le score de chacun de ces mots sera important comparativement aux lettres
    Ensuite je mets à + 10 par défaut si ces mots sont présents.
    """
    texte_test_enigmma = message.lower()
    note_decryptage = 0.0

    # =========================
    # 1. Lettres fréquentes et notation
    # =========================
    lettres_frequentes = {
        'e': 1.75, 's': .8125, 'a': .8125, 'i': .725,
        't': .7, 'n': .7, 'r': .65, 'u': .625,
        'l': .55, 'o': .5125
    }

    for c in texte_test_enigmma :
        note_decryptage += lettres_frequentes.get(c, 0)
        # Le 0 indique qu'il n'y a pas de pénalité pour les autres lettres

        # =========================
        # 2. Mots fréquents
        # =========================
        mots_frequents = ('le', 'la', 'de', 'un', 'une',
                          'a', 'et', 'il', 'je', 'ne', 'pas', 'en')

        mots_texte = texte_test_enigmma.split()
        for mot in mots_texte :
            if mot in mots_frequents :
                note_decryptage += 10

        # =========================
        # 3. Voyelles proportions
        # =========================
        voyelles = "aeiouy"
        nbre_de_voyelle = sum(1 for lettre in texte_test_enigmma if lettre in voyelles)

        if len(texte_test_enigmma) > 0 :
            proportion_voyelle = nbre_de_voyelle / len(texte_test_enigmma)

            if proportion_voyelle < 0.25 or proportion_voyelle > 0.65 :
                note_decryptage -= 5

            if len(texte_test_enigmma) > 4 : # Le plus long mot français avec seulement des voyelles est ouïe
                if proportion_voyelle < 0.15 or proportion_voyelle > 0.85 :
                    note_decryptage = 0

        # =========================
        # 4. Apostrophes interdites
        # =========================
        apostrophe_impossible = ("a'","b'","e'","f'","g'","h'","i'","k'","o'",
                                 "p'","q'","r'","u'","v'","w'","x'","y'","z'")
        for mot in apostrophe_impossible :
            if mot in texte_test_enigmma :
                note_decryptage = 0

    return note_decryptage

'''def test_bon_score(message: str, cle_enigma: tuple,meilleur_score) :
    texte_complet_enigmma = enigma_dechiffrer(message, cle_enigma)
    score_texte = noter_decryptage(texte_complet_enigmma)

    # On remplace les valeurs en fonction du meilleur résultat
    if score_texte > meilleur_score:
        meilleur_score = score_texte
        meilleur_texte = texte_complet_enigmma
        meilleure_cle = cle_enigma
    return (meilleur_score, meilleur_texte)'''

def brute_force_enigma(message: str) -> str:
    """
    Brute-force pour déchiffrer la version simplifiée d'Enigma.
    Retourne les meilleurs déchiffrements trouvés ainsi que les clés.
    """
    meilleurs_specs = []
    nombre_retenu = 5

    debut_brute_force = perf_counter()

    '''
    Essai de toutes les clés (26 ** 3)
    Pour se mettre dans un contexte plus proche du décryptage d'Enigma avec des capacités limitées,
    on ne parcourt l'entièreté du message que si il est prometteur.
    Pour éviter de craquer le code trop facilement, la dimension des messages étaient limitées
    (typiquement 200 caractères, source : https://www.cs.miami.edu/home/harald/enigma/ )
    On va donc décrypter dans un premier temps 100 caratères.
    '''
    for cle1 in range(26) :
        for cle2 in range(26) :
            for cle3 in range(26) :
                cle_enigma = (cle1, cle2, cle3)

                # Si la liste des n meilleures solutions des pas pleine, l'ajout est direct
                if len(meilleurs_specs) < nombre_retenu :
                    if len(message) > 100 :
                        """
                        Pour identifier si un texte de plus de 100 caractères est prometteurs, c'est fait en deux étapes
                        D'abord sur les 100 premiers caractères avec un score intermédiaire puis avec la décryption
                        totale et un score final.
                         """
                        # Section intermédiaire
                        extrait_texte_optimisation = message[:100]
                        texte_partiel_enigmma = enigma_dechiffrer(message, cle_enigma)
                        score_intermediaire = noter_decryptage(texte_partiel_enigmma)
                        # Section finale
                        texte_complet_enigmma = enigma_dechiffrer(message, cle_enigma)
                        score_final = noter_decryptage(texte_partiel_enigmma)

                        meilleurs_specs.append((score_intermediaire, score_final, cle_enigma, texte_complet_enigmma))
                    else :
                        texte_complet_enigmma = enigma_dechiffrer(message, cle_enigma)
                        score_texte = noter_decryptage(texte_complet_enigmma)
                        meilleurs_specs.append((score_texte, cle_enigma, texte_complet_enigmma))
                else :
                    """
                    meilleurs_specs est l'élément de référence, on prend un élément appelé specs.
                    C'est un tuple (score, cle, texte).
                    On récupère le score avec specs[0]. En ajoutant key = , on précise que le calcul de la fonction min
                    porte uniquement sur le score et ressort le tuple qui contient le score minimum.
                    D'où l'indexation [0] qui récupère seulement le score
                    """
                    pire_score = min(meilleurs_specs, key = lambda specs: specs[0])[0]

                    if len(message) > 100 :
                        extrait_texte_optimisation = message[:100]
                        texte_partiel_enigmma = enigma_dechiffrer(message, cle_enigma)
                        score_intermediaire = noter_decryptage(texte_partiel_enigmma)
                        # Seulement si le décryptage est prometteur va-t-on déchiffrer l'intégralité du message
                        if score_intermediaire > pire_score :
                            texte_complet_enigmma = enigma_dechiffrer(message, cle_enigma)
                            score_final = noter_decryptage(texte_complet_enigmma)
                            # Même méthodologie lambda que précédemment mais pour identifier le pire_score_final ici
                            pire_score_final = min(meilleurs_specs, key = lambda specs: specs[1])[1]

                            # On remplace les valeurs en fonction du meilleur résultat
                            if score_final > pire_score_final:
                                """
                                range(nombre_retenu) est l'élément de référence, il s'agit d'indice.
                                On prend un élément appelé index qui est un indice de meilleurs_specs.
                                On compare les valeurs de meilleurs_specs[index][1] pour trouver le minimum
                                et on renvoie l'indice correspondant.
                                """
                                # On remplace le pire des résultats
                                index_pire_combinaison = min(range(nombre_retenu),
                                                             key = lambda index: meilleurs_specs[index][1])
                                meilleurs_specs[index_pire_combinaison] = (score_intermediaire, score_final, cle_enigma,
                                                                           texte_complet_enigmma)
                    else :
                        texte_complet_enigmma = enigma_dechiffrer(message, cle_enigma)
                        score_texte = noter_decryptage(texte_complet_enigmma)

                        # On remplace les valeurs en fonction du meilleur résultat
                        if score_texte > pire_score:
                            index_pire_combinaison = min(range(nombre_retenu),
                                                         key = lambda index: meilleurs_specs[index][0])
                            meilleurs_specs[index_pire_combinaison] = (score_texte, cle_enigma,
                                                                       texte_complet_enigmma)

    if len(message) > 100:
        meilleurs_specs_triees = sorted(meilleurs_specs, key = lambda specs: specs[1], reverse=True)
    else :
        meilleurs_specs_triees = sorted(meilleurs_specs, key=lambda specs: specs[0], reverse=True)

    fin_brute_force = perf_counter()
    print(f"Temps d'exécution : {fin_brute_force - debut_brute_force:.4f} secondes")

    return meilleurs_specs_triees

def brute_force_cesar(message: str) -> str:
    """
    Brute-force pour déchiffrer le code César.
    Retourne les meilleurs déchiffrements trouvés ainsi que les clés.
    """
    meilleurs_specs = []
    nombre_retenu = 5

    debut_brute_force = perf_counter()

    '''
    Essaye toutes les clés (26)
    '''
    for cle in range(26) :
        # Si la liste des n meilleures solutions des pas pleine, l'ajout est direct
        if len(meilleurs_specs) < nombre_retenu :
            texte_complet = dechiffrer(message, cle)
            score_texte = noter_decryptage(texte_complet)
            meilleurs_specs.append((score_texte, cle, texte_complet))
        else :
            """
            meilleurs_specs est l'élément de référence, on prend un élément appelé specs.
            C'est un tuple (score, cle, texte).
            On récupère le score avec specs[0]. En ajoutant key = , on précise que le calcul de la fonction min
            porte uniquement sur le score et ressort le tuple qui contient le score minimum.
            D'où l'indexation [0] qui récupère seulement le score
            """
            pire_score = min(meilleurs_specs, key = lambda specs: specs[0])[0]

            texte_complet = dechiffrer(message, cle)
            score_texte = noter_decryptage(texte_complet)

            # On remplace les valeurs en fonction du meilleur résultat
            if score_texte > pire_score:
                index_pire_combinaison = min(range(nombre_retenu),
                                             key = lambda index: meilleurs_specs[index][0])
                meilleurs_specs[index_pire_combinaison] = (score_texte, cle, texte_complet)

    meilleurs_specs_triees = sorted(meilleurs_specs, key=lambda specs: specs[0], reverse=True)

    fin_brute_force = perf_counter()
    print(f"Temps d'exécution : {fin_brute_force - debut_brute_force:.4f} secondes")

    return meilleurs_specs_triees

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
        resultat = brute_force(texte_a_traiter)
    else:
        if args.action == "chiffrer":
            resultat = chiffrer(texte_a_traiter, cle)
        elif args.action == "dechiffrer":
            resultat = dechiffrer(texte_a_traiter, cle)
        else:  # args.action == "enigma"
            resultat = enigma_chiffrer(texte_a_traiter, cle)

    # === ÉTAPE 7 : Afficher le résultat ===
    print(resultat)


if __name__ == "__main__":
    main()