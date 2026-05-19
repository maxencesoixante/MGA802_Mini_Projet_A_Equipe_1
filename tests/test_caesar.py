"""Tests pour le Mini-Projet A.

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.

Pour lancer les tests :
    pip install pytest
    pytest -v
"""
import sys
import unicodedata
from pathlib import Path

# Permet d'importer main.py depuis le dossier parent
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import chiffrer, dechiffrer, enigma_chiffrer  # noqa: E402


# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer("Veni, vidi, vici!", 42) == "Ludy, lyty, lysy!"


def test_cesar_officiel_cle_neg_42():
    assert chiffrer("Veni, vidi, vici!", -42) == "Foxs, fsns, fsms!"


# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------

def test_enigma_officiel_maison():
    assert enigma_chiffrer("MAISON", (7, 16, 9)) == "TQRZEW"


# ---------- Cas standards (à compléter par votre équipe) ----------

def test_cesar_round_trip():
    """Chiffrer puis déchiffrer doit redonner le message original."""
    msg = "Bonjour le monde !"
    assert dechiffrer(chiffrer(msg, 7), 7) == msg


def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer("Tout pareil.", 0) == "Tout pareil."

'''
def test_cesar_majuscule(message,cle) :
    """Une majuscule doit rester une majuscule"""
    liste_maj_
    for caractere in message:
        # Vérifie si le caractère est une lettre minuscule (a-z)
        if caractere.islower():
            
        
    assert (chiffrer(message,cle)).isupper() == test_maj.isupper()

def test_cesar_minuscule() :
    pass
'''

def test_cesar_caractere_speciaux() :
    # assert chiffrer("C'est déjà là Noël. Où_tôt.", 1) == "D'ftu efkb mb Opfm. Pv_upu."
    assert chiffrer("C'est deja la Noel. Ou_tot.", 1) == "D'ftu efkb mb Opfm. Pv_upu."

def test_cesar_grande_cle() :
    pass

def test_cesar_brute_force_cesar() :
    pass

def test_cesar_brute_force_enigma() :
    pass

def test_cesar_cle_enigma() :
    pass

# TODO : ajoutez vos propres tests ci-dessous
#  - test pour les majuscules
#  - test pour les caractères spéciaux (accents, ponctuation)
#  - test pour les très grandes clés (positives et négatives)
#  - test pour le brute-force (César ET Enigma César)
#  - test que enigma_chiffrer rejette une clé qui n'a pas 3 nombres
