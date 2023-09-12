from random import shuffle
from listes import *
from piles import *

class Carte:
# Cette classe représente une carte de jeu.
# Elle a des attributs tels que la hauteur (2, 3, ..., roi, as) et la couleur (coeur, carreau, trefle, pique).
    
    valides_hauteurs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi", "as"]
    valides_couleurs = ["coeur", "carreau", "trefle", "pique"]
    symboles_couleurs = {"coeur": "♥", "carreau": "♦", "trefle": "♣", "pique": "♠"}

    def __init__(self, hauteur, couleur):
        if hauteur not in self.valides_hauteurs or couleur not in self.valides_couleurs:
            raise ValueError("Hauteur ou couleur non valide")
        self._hauteur = hauteur
        self._couleur = couleur

    def hauteur(self):
        return self._hauteur

    def couleur(self):
        return self._couleur

    def __str__(self):
        return f"{self._hauteur} de {self._couleur}"

    def __repr__(self):
        return f'Carte("{self._hauteur}", "{self._couleur}")'

    def valeur(self):
        if self._hauteur in ["roi", "dame", "valet"]:
            return 10
        elif self._hauteur == "as":
            return 11
        else:
            return int(self._hauteur)

class FileDouble:
# Cette classe représente une file double utilisée pour le mélange et la distribution de cartes.
    
    def __init__(self):
        self.pioche = Pile()
        self.defausse = Pile()

    def enfiler(self, valeur):
        # Ajoute une valeur à la file double.
        
        self.defausse.empiler(valeur)

    def defiler(self):
        # Retire une valeur de la file double.
        
        if self.pioche.est_vide():
            while not self.defausse.est_vide():
                self.pioche.empiler(self.defausse.dépiler())
        return self.pioche.dépiler() if not self.pioche.est_vide() else None

class Paquet:
# Cette classe représente un paquet de cartes.
# Elle génère un paquet complet de cartes, les mélange et les distribue.
    
    def __init__(self):
        self.file = FileDouble()
        for couleur in Carte.valides_couleurs:
            for hauteur in Carte.valides_hauteurs:
                self.file.enfiler(Carte(hauteur, couleur))

    def melange(self):
        # Mélange le paquet de cartes.
        
        cartes = []
        while True:
            carte = self.file.defiler()
            if carte is None:
                break
            cartes.append(carte)
        shuffle(cartes)
        for carte in cartes:
            self.file.enfiler(carte)

    def distribue(self, n):
        # Distribue n cartes du paquet.
        
        return [self.file.defiler() for _ in range(n)]

    def affichages(self):
        # Affiche l'état actuel de la pioche et de la défausse.
        return f"Pioche: {[str(carte) for carte in self.file.pioche.liste_chainee]}, Defausse: {[str(carte) for carte in self.file.defausse.liste_chainee]}"

class Main:
# Cette classe représente la main d'un joueur.
# Elle peut trier les cartes, ajouter une carte à la main ou retirer une carte de la main.
    
    def __init__(self, cartes=[]):
        self.cartes = cartes

    def trier(self, desc=False, as_fort=True):
        self.cartes.sort(key=lambda carte: (Carte.valides_hauteurs.index(carte.hauteur()), Carte.valides_couleurs.index(carte.couleur())), reverse=desc)
        if not as_fort:
            as_carte = [carte for carte in self.cartes if carte.hauteur() == "as"]
            autres_cartes = [carte for carte in self.cartes if carte.hauteur() != "as"]
            self.cartes = autres_cartes + as_carte

    def enfiler(self, carte):
        self.cartes.append(carte)

    def defiler(self):
        if self.cartes:
            return self.cartes.pop(0)
        return None

    def est_vide(self):
        return len(self.cartes) == 0

    def afficher(self):
        return ", ".join(str(carte) for carte in self.cartes)


class Joueur:
# Cette classe représente un joueur.
# Elle peut calculer le score de la main et choisir une carte à jouer.

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.main = Main([])

    def calculer_score(self):
        score = sum(carte.valeur() for carte in self.main.cartes)
        nombre_as = sum(1 for carte in self.main.cartes if carte.hauteur() == "as")
        while score > 21 and nombre_as:
            score -= 10  # Convertir un As de 11 points à 1 point
            nombre_as -= 1
        return score

    def jouer(self):
        if not self.main.cartes:
            print(f"{self.pseudo}, vous n'avez pas de cartes en main.")
            return None
        carte_choisie = input(f"{self.pseudo}, choisissez une carte à jouer (0-{len(self.main.cartes) - 1}): ")
        return self.main.cartes.pop(int(carte_choisie))


class JoueurIA(Joueur):
# Cette classe représente un joueur IA.
# Elle hérite des fonctionnalités du joueur standard et joue automatiquement en retirant la carte du haut.

    def jouer(self):
        if not self.main.cartes:
            print("Erreur: Pas de cartes dans la main.")
            return None
        return self.main.cartes.pop()

