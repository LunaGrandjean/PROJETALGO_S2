from listes import liste_vide, cellule, tête, queue, est_vide
from piles import Pile
from classes_cartes_black_jack import Paquet, Main, Joueur, JoueurIA

class BlackJack:
    def __init__(self, joueur, croupier):
        self.joueur = joueur  # Objet Joueur
        self.croupier = croupier  # Objet Croupier (qui est aussi un Joueur)
        self.paquet = Paquet()  # Crée un paquet de cartes
        self.paquet.melange()  # Mélange le paquet

    def distribuer_cartes_initiales(self):
        for _ in range(2):
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
                
                score_joueur = self.joueur.calculer_score()
                if score_joueur > 21:
                    print(f"{self.joueur.pseudo} dépasse 21. C'est une défaite!")
                    return  
            else:
                break  

        while self.croupier.calculer_score() < 17:
            carte = self.paquet.file.defiler()  
            print(f"Croupier a tiré {carte}.")
            self.croupier.main.enfiler(carte)  

        # Une fois le tour du croupier terminé, on compare les scores pour déterminer le gagnant.
        score_joueur = self.joueur.calculer_score()
        score_croupier = self.croupier.calculer_score()

        if score_croupier > 21 or score_joueur > score_croupier:
            print(f"{self.joueur.pseudo} gagne avec un score de {score_joueur} contre {score_croupier} pour le croupier!")
        elif score_joueur < score_croupier:
            print(f"Croupier gagne avec un score de {score_croupier} contre {score_joueur} pour {self.joueur.pseudo}!")
        else:
            print("C'est une égalité!")
