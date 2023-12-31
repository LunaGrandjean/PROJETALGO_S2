from random import shuffle
from listes import liste_vide, cellule, tête, queue, est_vide
from piles import Pile

class Carte:
    # Classe pour représenter une carte individuelle.
    
    # Constantes définissant les hauteurs et couleurs valides pour les cartes.
    valides_hauteurs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi", "as"]
    valides_couleurs = ["coeur", "carreau", "trefle", "pique"]
    symboles_couleurs = {"coeur": "♥", "carreau": "♦", "trefle": "♣", "pique": "♠"}

    def __init__(self, hauteur, couleur):
        # Constructeur pour la classe Carte.
        
        # Valide la hauteur et la couleur avant de les affecter.
        if hauteur not in self.valides_hauteurs or couleur not in self.valides_couleurs:
            raise ValueError("Hauteur ou couleur non valide")
        self._hauteur = hauteur
        self._couleur = couleur

    # Méthodes pour récupérer la hauteur et la couleur de la carte.
    def hauteur(self):
        return self._hauteur

    def couleur(self):
        return self._couleur

    # Méthodes pour représenter la carte sous forme de chaîne de caractères.
    def __str__(self):
        return f"{self._hauteur} de {self._couleur}"

    def __repr__(self):
        return f'Carte("{self._hauteur}", "{self._couleur}")'

    # Méthode pour obtenir la valeur numérique de la carte (utile pour le calcul des scores).
    def valeur(self):
        if self._hauteur in ["roi", "dame", "valet"]:
            return 10
        elif self._hauteur == "as":
            return 11
        else:
            return int(self._hauteur)

class FileDouble:
    # Classe pour représenter une file double. 
    
    def __init__(self):
        # La file double est représentée par deux piles.
        self.pioche = Pile()
        self.defausse = Pile()

    def enfiler(self, valeur):
        # Ajoute une valeur à la défausse.
        self.defausse.empiler(valeur)

    def defiler(self):
        # Retire et retourne une valeur de la pioche. 
        # Si la pioche est vide, transfère toutes les cartes de la défausse à la pioche.
        if self.pioche.est_vide():
            while not self.defausse.est_vide():
                self.pioche.empiler(self.defausse.dépiler())
        return self.pioche.dépiler() if not self.pioche.est_vide() else None

class Paquet:
    # Classe pour représenter un paquet complet de cartes.
    
    def __init__(self):
        self.file = FileDouble()
        # Crée un paquet complet de cartes.
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
    # Classe pour représenter la main d'un joueur.
    
    def __init__(self, cartes=[]):
        self.cartes = cartes

    def trier(self, desc=False, as_fort=True):
        # Trie les cartes de la main.
        
        self.cartes.sort(key=lambda carte: (Carte.valides_hauteurs.index(carte.hauteur()), Carte.valides_couleurs.index(carte.couleur())), reverse=desc)
        if not as_fort:
            as_carte = [carte for carte in self.cartes if carte.hauteur() == "as"]
            autres_cartes = [carte for carte in self.cartes if carte.hauteur() != "as"]
            self.cartes = autres_cartes + as_carte

    def enfiler(self, carte):
        # Ajoute une carte à la main.
        self.cartes.append(carte)

    def defiler(self):
        # Retire et retourne la première carte de la main.
        return self.cartes.pop(0) if self.cartes else None

    def est_vide(self):
        # Vérifie si la main est vide.
        return len(self.cartes) == 0

    def afficher(self):
        # Affiche toutes les cartes dans la main.
        return ", ".join(str(carte) for carte in self.cartes)

class Joueur:
    # Classe pour représenter un joueur.
    
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.main = Main([])

    def calculer_score(self):
        # Calcule le score total de la main.
        
        score = sum(carte.valeur() for carte in self.main.cartes)
        nombre_as = sum(1 for carte in self.main.cartes if carte.hauteur() == "as")
        while score > 21 and nombre_as:
            score -= 10
            nombre_as -= 1
        return score

    def jouer(self):
        # Permet au joueur de choisir une carte à jouer.
        
        if not self.main.cartes:
            print(f"{self.pseudo}, vous n'avez pas de cartes en main.")
            return None
        carte_choisie = input(f"{self.pseudo}, choisissez une carte à jouer (0-{len(self.main.cartes) - 1}): ")
        return self.main.cartes.pop(int(carte_choisie))

class JoueurIA(Joueur):
    # Classe pour représenter un joueur IA qui hérite de la classe Joueur.
    
    def jouer(self):
        # L'IA joue automatiquement en retirant la carte du haut.
        
        if not self.main.cartes:
            print("Erreur: Pas de cartes dans la main.")
            return None
        return self.main.cartes.pop()
