from listes import liste_vide, cellule, tête, queue, est_vide
from piles import Pile
from classes_cartes_black_jack import Paquet, Main, Joueur, Joueur

class BlackJack:
    def __init__(self, joueur, croupier):
        self.joueur = joueur
        self.croupier = croupier
        self.paquet = Paquet()
        self.paquet.melange()

    def distribuer_cartes_initiales(self):
        for _ in range(2):  # Distribuer 2 cartes à chaque joueur
            self.joueur.main.enfiler(self.paquet.file.defiler())
            self.croupier.main.enfiler(self.paquet.file.defiler())

    def jouer(self):
        self.paquet.melange()
        self.joueur.main = Main(self.paquet.distribue(2))
        self.croupier.main = Main([self.paquet.file.defiler()])

        while True:
            print(f"Main de {self.joueur.pseudo}: {self.joueur.main.afficher()}")
            action = input(f"{self.joueur.pseudo}, voulez-vous tirer (t) ou rester (r)? ")
            if action == 't':
                carte = self.paquet.file.defiler()
                print(f"{self.joueur.pseudo} a tiré {carte}.")
                self.joueur.main.enfiler(carte)
                
                score_joueur = self.joueur.calculer_score()  # calcul du score après avoir tiré une carte
                if score_joueur > 21:
                    print(f"{self.joueur.pseudo} dépasse 21. C'est une défaite!")
                    return
            else:
                break  # le joueur a choisi de "rester"

        while self.croupier.calculer_score() < 17:  # Le croupier tire tant que son score est inférieur à 17
            carte = self.paquet.file.defiler()
            print(f"Croupier a tiré {carte}.")
            self.croupier.main.enfiler(carte)
            # la mise à jour du score du croupier se fait automatiquement à chaque tour de boucle avec calculer_score()
