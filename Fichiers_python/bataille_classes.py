from listes import *
from piles import *
from classes_cartes import *

class Bataille:
    def __init__(self):
        # Initialiser les joueurs et leur main
        self.joueur1 = JoueurIA("Joueur 1")
        self.joueur2 = JoueurIA("Joueur 2")
        self.paquet = Paquet()
        self.paquet.melange()
        self.centre_visible = Pile()
        self.centre_cachee = Pile()

    def distribuer_cartes(self):
        for i in range(26):  # Distribuer 26 cartes à chaque joueur
            self.joueur1.main.enfiler(self.paquet.file.defiler())
            self.joueur2.main.enfiler(self.paquet.file.defiler())

    def jouer_carte(self, joueur):
        return joueur.main.defiler()

    def comparer_cartes(self, carte1, carte2):
        # retourner 1 si carte1 est supérieure, 2 si carte2 est supérieure, 0 si égalité
        if Carte.valides_hauteurs.index(carte1.hauteur()) > Carte.valides_hauteurs.index(carte2.hauteur()):
            return 1
        elif Carte.valides_hauteurs.index(carte1.hauteur()) < Carte.valides_hauteurs.index(carte2.hauteur()):
            return 2
        else:
            return 0

    def recueillir_cartes(self, gagnant):
        while not self.centre_visible.est_vide():
            gagnant.main.enfiler(self.centre_visible.dépiler())
        while not self.centre_cachee.est_vide():
            gagnant.main.enfiler(self.centre_cachee.dépiler())

    def bataille(self):
        for _ in range(2):  # Chaque joueur joue 2 cartes, une cachée et une visible
            if not self.joueur1.main.est_vide():
                self.centre_cachee.empiler(self.joueur1.main.defiler())
            if not self.joueur2.main.est_vide():
                self.centre_cachee.empiler(self.joueur2.main.defiler())

            if not self.joueur1.main.est_vide():
                self.centre_visible.empiler(self.joueur1.main.defiler())
            if not self.joueur2.main.est_vide():
                self.centre_visible.empiler(self.joueur2.main.defiler())

    def jouer(self):
        self.distribuer_cartes()
        while not self.joueur1.main.est_vide() and not self.joueur2.main.est_vide():
            carte1 = self.jouer_carte(self.joueur1)
            carte2 = self.jouer_carte(self.joueur2)
            self.centre_visible.empiler(carte1)
            self.centre_visible.empiler(carte2)

            print(f"{self.joueur1.pseudo} joue {carte1} et {self.joueur2.pseudo} joue {carte2}")

            resultat = self.comparer_cartes(carte1, carte2)
            if resultat == 1:
                print(f"{self.joueur1.pseudo} gagne ce tour.")
                self.recueillir_cartes(self.joueur1)
            elif resultat == 2:
                print(f"{self.joueur2.pseudo} gagne ce tour.")
                self.recueillir_cartes(self.joueur2)
            else:
                print("Bataille !")
                self.bataille()

        if not self.joueur1.main.est_vide():
            print(f"{self.joueur1.pseudo} remporte la partie!")
        elif not self.joueur2.main.est_vide():
            print(f"{self.joueur2.pseudo} remporte la partie!")
        else:
            print("C'est un match nul!")
