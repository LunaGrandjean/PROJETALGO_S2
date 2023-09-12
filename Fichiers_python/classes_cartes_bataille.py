from random import shuffle
from listes import *
from piles import *

class Carte:
# Classe représentant une carte de jeu.
# Elle a des valeurs de hauteur, de couleur, et une méthode pour afficher la carte sous forme de chaîne de caractères.
    
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

class FileDouble:
# Classe représentant une file double utilisée pour gérer les cartes.
# Elle a une pioche et une défausse pour gérer les cartes.
 
    def __init__(self):
        self.pioche = Pile()
        self.defausse = Pile()

    def enfiler(self, valeur):
        # Ajoute une valeur à la défausse.
        self.defausse.empiler(valeur)

    def defiler(self):
        # Récupère une carte de la pioche ou la récupère de la défausse si la pioche est vide.
        
        if self.pioche.est_vide():
            while not self.defausse.est_vide():
                self.pioche.empiler(self.defausse.dépiler())
        return self.pioche.dépiler() if not self.pioche.est_vide() else None

class Paquet:
    # Classe représentant un paquet de cartes.
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
        return f"Pioche: {[str(carte) for carte in self.file.pioche.liste_chainee]}, Defausse: {[str(carte) for carte in self.file.defausse.liste_chainee]}"

class Main:
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
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.score = 0
        self.main = Main([])

    def jouer(self):
        if not self.main.cartes:
            print(f"{self.pseudo}, vous n'avez pas de cartes en main.")
            return None
        carte_choisie = input(f"{self.pseudo}, choisissez une carte à jouer (0-{len(self.main.cartes) - 1}): ")
        return self.main.cartes.pop(int(carte_choisie))

class JoueurIA(Joueur):
    def jouer(self):
        if not self.main.cartes:
            print("Erreur: Pas de cartes dans la main.")
            return None
        return self.main.cartes.pop()
