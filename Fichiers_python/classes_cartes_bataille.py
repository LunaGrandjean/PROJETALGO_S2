from random import shuffle
# Importation des fonctionnalités nécessaires depuis les autres modules.
from listes import liste_vide, cellule, tête, queue, est_vide
from piles import Pile

class Carte:
    # Classe pour représenter une carte individuelle dans un jeu de cartes standard.
    
    # Les hauteurs et les couleurs valides pour toutes les cartes.
    valides_hauteurs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi", "as"]
    valides_couleurs = ["coeur", "carreau", "trefle", "pique"]
    
    # Symboles pour représenter visuellement chaque couleur.
    symboles_couleurs = {"coeur": "♥", "carreau": "♦", "trefle": "♣", "pique": "♠"}

    def __init__(self, hauteur, couleur):
        # Initialisation d'une carte avec une hauteur et une couleur spécifiées.
        # Si la hauteur ou la couleur ne sont pas valides, une erreur est levée.
        
        if hauteur not in self.valides_hauteurs or couleur not in self.valides_couleurs:
            raise ValueError("Hauteur ou couleur non valide")
        self._hauteur = hauteur
        self._couleur = couleur

    def hauteur(self):
        # Renvoie la hauteur de la carte.
        return self._hauteur

    def couleur(self):
        # Renvoie la couleur de la carte.
        return self._couleur

    def __str__(self):
        # Représentation sous forme de chaîne de caractères pour l'affichage.
        return f"{self._hauteur} de {self._couleur}"

    def __repr__(self):
        # Représentation formelle pour la carte.
        return f'Carte("{self._hauteur}", "{self._couleur}")'

class FileDouble:
    # Une structure de données qui utilise deux piles pour implémenter une file.
    
    def __init__(self):
        # Initialisation avec deux piles vides : pioche et défausse.
        self.pioche = Pile()
        self.defausse = Pile()

    def enfiler(self, valeur):
        # Ajoute une valeur à la défausse.
        self.defausse.empiler(valeur)

    def defiler(self):
        # Récupère une valeur de la pioche. Si la pioche est vide, renverse la défausse dans la pioche.
        
        if self.pioche.est_vide():
            while not self.defausse.est_vide():
                self.pioche.empiler(self.defausse.dépiler())
        return self.pioche.dépiler() if not self.pioche.est_vide() else None

class Paquet:
    # Classe pour représenter un jeu complet de cartes.
    
    def __init__(self):
        # Crée un paquet complet de cartes et les ajoute à la file.
        self.file = FileDouble()
        for couleur in Carte.valides_couleurs:
            for hauteur in Carte.valides_hauteurs:
                self.file.enfiler(Carte(hauteur, couleur))

    def melange(self):
        # Mélange le paquet de cartes en utilisant la fonction shuffle.
        
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
        # Distribue les n premières cartes du paquet.
        return [self.file.defiler() for _ in range(n)]

    def affichages(self):
        # Retourne une représentation sous forme de chaîne de caractères de la pioche et de la défausse.
        return f"Pioche: {[str(carte) for carte in self.file.pioche.liste_chainee]}, Defausse: {[str(carte) for carte in self.file.defausse.liste_chainee]}"

class Main:
    # Classe pour représenter la main d'un joueur.
    
    def __init__(self, cartes=[]):
        # Initialisation avec une liste de cartes.
        self.cartes = cartes

    def trier(self, desc=False, as_fort=True):
        # Trie les cartes en fonction de leur hauteur et couleur.
        
        self.cartes.sort(key=lambda carte: (Carte.valides_hauteurs.index(carte.hauteur()), Carte.valides_couleurs.index(carte.couleur())), reverse=desc)
        # Si l'As doit être considéré comme la plus faible carte, déplacez-le à la fin.
        if not as_fort:
            as_carte = [carte for carte in self.cartes if carte.hauteur() == "as"]
            autres_cartes = [carte for carte in self.cartes if carte.hauteur() != "as"]
            self.cartes = autres_cartes + as_carte

    def enfiler(self, carte):
        # Ajoute une carte à la main.
        self.cartes.append(carte)

    def defiler(self):
        # Retire et retourne la première carte de la main.
        if self.cartes:
            return self.cartes.pop(0)
        return None

    def est_vide(self):
        # Vérifie si la main est vide.
        return len(self.cartes) == 0

    def afficher(self):
        # Retourne une représentation sous forme de chaîne de caractères de toutes les cartes dans la main.
        return ", ".join(str(carte) for carte in self.cartes)

class Joueur:
    # Classe pour représenter un joueur humain.
    
    def __init__(self, pseudo):
        # Initialisation avec un pseudo, un score initialisé à 0 et une main vide.
        self.pseudo = pseudo
        self.score = 0
        self.main = Main([])

    def jouer(self):
        # Demande au joueur de choisir une carte à jouer.
        
        if not self.main.cartes:
            print(f"{self.pseudo}, vous n'avez pas de cartes en main.")
            return None
        carte_choisie = input(f"{self.pseudo}, choisissez une carte à jouer (0-{len(self.main.cartes) - 1}): ")
        return self.main.cartes.pop(int(carte_choisie))

class JoueurIA(Joueur):
    # Classe pour représenter un joueur géré par l'IA.
    
    def jouer(self):
        # L'IA joue automatiquement en retirant la carte du haut.
        
        if not self.main.cartes:
            print("Erreur: Pas de cartes dans la main.")
            return None
        return self.main.cartes.pop()
