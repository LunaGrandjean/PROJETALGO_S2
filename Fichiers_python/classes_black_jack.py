from listes import liste_vide, cellule, tête, queue, est_vide
from piles import Pile
from classes_cartes import Paquet, Main, Joueur, JoueurIA

class BlackJack:
    def __init__(self, joueur, croupier):
        # Initialisation du jeu de BlackJack avec un joueur et un croupier
        self.joueur = joueur  # Objet Joueur
        self.croupier = croupier  # Objet Croupier (qui est aussi un Joueur)
        self.paquet = Paquet()  # Crée un paquet de cartes
        self.paquet.melange()  # Mélange le paquet

    def distribuer_cartes_initiales(self):
        # Distribuer deux cartes à chaque joueur (joueur et croupier) pour commencer le jeu
        for _ in range(2):
            self.joueur.main.enfiler(self.paquet.file.defiler())  # Le joueur prend une carte du paquet
            self.croupier.main.enfiler(self.paquet.file.defiler())  # Le croupier prend une carte du paquet

    def jouer(self):
        self.paquet.melange()  # Mélange le paquet à nouveau
        # Distribuer initialement 2 cartes pour le joueur et 1 carte pour le croupier
        self.joueur.main = Main(self.paquet.distribue(2))
        self.croupier.main = Main([self.paquet.file.defiler()])

        while True:
            # Affiche la main actuelle du joueur
            print(f"Main de {self.joueur.pseudo}: {self.joueur.main.afficher()}")
            # Demande au joueur s'il veut tirer une carte ou rester avec sa main actuelle
            action = input(f"{self.joueur.pseudo}, voulez-vous tirer (t) ou rester (r)? ")
            if action == 't':
                carte = self.paquet.file.defiler()  # Le joueur prend une carte du paquet
                print(f"{self.joueur.pseudo} a tiré {carte}.")
                self.joueur.main.enfiler(carte)  # La carte est ajoutée à la main du joueur
                
                # Calcule le score du joueur après avoir tiré la carte
                score_joueur = self.joueur.calculer_score()
                # Vérifie si le joueur dépasse 21 après avoir tiré la carte
                if score_joueur > 21:
                    print(f"{self.joueur.pseudo} dépasse 21. C'est une défaite!")
                    return  # Fin du jeu
            else:
                break  # Le joueur a décidé de rester avec sa main actuelle

        # Le croupier tire des cartes tant que son score est inférieur à 17
        while self.croupier.calculer_score() < 17:
            carte = self.paquet.file.defiler()  # Le croupier prend une carte du paquet
            print(f"Croupier a tiré {carte}.")
            self.croupier.main.enfiler(carte)  # La carte est ajoutée à la main du croupier
            # Note: la mise à jour du score du croupier se fait automatiquement à chaque tour de boucle avec calculer_score()
