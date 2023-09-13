# Importation des modules nécessaires.
from listes import liste_vide, cellule, tête, queue, est_vide
from piles import Pile
from classes_cartes_bataille import Carte, JoueurIA, Paquet, Main

class Bataille:
    def __init__(self):
        # Initialiser le jeu de bataille.

        # Les deux joueurs, représentés par des IAs.
        self.joueur1 = JoueurIA("Joueur 1")
        self.joueur2 = JoueurIA("Joueur 2")

        # Le paquet de cartes, initialisé et mélangé.
        self.paquet = Paquet()
        self.paquet.melange()

        # Piles centrales pour la "bataille" : une pour les cartes visibles et une pour les cartes cachées.
        self.centre_visible = Pile()
        self.centre_cachee = Pile()

        # Compteur pour garder une trace du nombre de tours joués.
        self.nb_tours = 0

    def distribuer_cartes(self):
        # Distribuer 26 cartes à chaque joueur.
        for i in range(26):
            self.joueur1.main.enfiler(self.paquet.file.defiler())
            self.joueur2.main.enfiler(self.paquet.file.defiler())

    def jouer_carte(self, joueur):
        # Jouer une carte du dessus de la pile du joueur.
        return joueur.main.defiler()

    def comparer_cartes(self, carte1, carte2):
        # Compare deux cartes pour déterminer laquelle est la plus haute.
        # retourne 1 si carte1 est supérieure, 2 si carte2 est supérieure, 0 si égalité.
        if Carte.valides_hauteurs.index(carte1.hauteur()) > Carte.valides_hauteurs.index(carte2.hauteur()):
            return 1
        elif Carte.valides_hauteurs.index(carte1.hauteur()) < Carte.valides_hauteurs.index(carte2.hauteur()):
            return 2
        else:
            return 0

    def recueillir_cartes(self, gagnant):
        # Donner toutes les cartes du centre au gagnant du tour.
        while not self.centre_visible.est_vide():
            gagnant.main.enfiler(self.centre_visible.dépiler())
        while not self.centre_cachee.est_vide():
            gagnant.main.enfiler(self.centre_cachee.dépiler())

    def bataille(self):
        # Se produit lors d'une égalité. Chaque joueur met une carte face cachée puis une face visible.
        for _ in range(2):
            if not self.joueur1.main.est_vide():
                self.centre_cachee.empiler(self.joueur1.main.defiler())
            if not self.joueur2.main.est_vide():
                self.centre_cachee.empiler(self.joueur2.main.defiler())

            if not self.joueur1.main.est_vide():
                self.centre_visible.empiler(self.joueur1.main.defiler())
            if not self.joueur2.main.est_vide():
                self.centre_visible.empiler(self.joueur2.main.defiler())

    def jouer(self):
        # La logique principale du jeu.
        self.distribuer_cartes()

        # Tant que les deux joueurs ont des cartes...
        while not self.joueur1.main.est_vide() and not self.joueur2.main.est_vide():
            # Chaque joueur joue une carte.
            carte1 = self.jouer_carte(self.joueur1)
            carte2 = self.jouer_carte(self.joueur2)

            # Les cartes jouées sont placées au centre.
            self.centre_visible.empiler(carte1)
            self.centre_visible.empiler(carte2)

            # Augmenter le compteur de tours.
            self.nb_tours += 1

            print(f"{self.joueur1.pseudo} joue {carte1} et {self.joueur2.pseudo} joue {carte2}")

            # Comparaison des cartes jouées.
            resultat = self.comparer_cartes(carte1, carte2)
            if resultat == 1:
                print(f"{self.joueur1.pseudo} gagne ce tour.")
                self.recueillir_cartes(self.joueur1)
            elif resultat == 2:
                print(f"{self.joueur2.pseudo} gagne ce tour.")
                self.recueillir_cartes(self.joueur2)
            else:
                # En cas d'égalité, une bataille est déclenchée.
                print("Bataille !")
                self.bataille()

        # Annonce du gagnant à la fin du jeu.
        if not self.joueur1.main.est_vide():
            print(f"{self.joueur1.pseudo} remporte la partie après {self.nb_tours} tours!")
        elif not self.joueur2.main.est_vide():
            print(f"{self.joueur2.pseudo} remporte la partie après {self.nb_tours} tours!")
        else:
            print(f"C'est un match nul après {self.nb_tours} tours!")
