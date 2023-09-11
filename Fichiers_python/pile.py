from listes import *

class Pile:
    def __init__(self):
        self.liste_chainee = liste_vide()
        self._taille = 0
        
    def get_taille(self):
        return self._taille
    
    def __str__(self) -> str:
        return affiche_liste_rec(self.liste_chainee)

    def empiler(self, valeur):
        self.liste_chainee = cellule(valeur, self.liste_chainee)
        self._taille +=1

    def dépiler(self):
        
        if self.est_vide():
            raise IndexError("La pile est vide")
        valeur = tête(self.liste_chainee)
        self.liste_chainee = queue(self.liste_chainee)
        self._taille -= 1
        return valeur

    def est_vide(self):
        self._taille = 0
        return est_vide(self.liste_chainee)

    def taille(self):
        return self._taille #longueur(self.liste_chainee)

    def consulter(self):
        if self.est_vide():
            raise IndexError("La pile est vide")
        return tête(self.liste_chainee)

    def vider(self):
        self.liste_chainee = liste_vide()
        self._taille = 0
        