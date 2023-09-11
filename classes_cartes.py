import random


class Carte:
    COULEURS = ["trèfle", "coeur", "carreau", "pique"]
    HAUTEURS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi", "as"]
    COULEUR_SYMBOLS = {"trèfle": "♣", "coeur": "♥", "carreau": "♦", "pique": "♠"}

    def __init__(self, hauteur, couleur):
        if hauteur not in self.HAUTEURS or couleur not in self.COULEURS:
            raise ValueError("Hauteur ou couleur non valide.")
        self._hauteur = hauteur
        self._couleur = couleur

    def hauteur(self):
        return self._hauteur

    def couleur(self):
        return self._couleur

    def __str__(self):
        return f"{self._hauteur} {self.COULEUR_SYMBOLS[self._couleur]}"

    def __repr__(self):
        return f'Carte("{self._hauteur}", "{self._couleur}")'


class FileDouble:
    def __init__(self):
        self.pioche = []
        self.defausse = []

    def enfiler(self, carte):
        self.pioche.append(carte)

    def defiler(self):
        if not self.defausse:
            if not self.pioche:
                raise Exception("Les deux piles sont vides.")
            while self.pioche:
                self.defausse.append(self.pioche.pop())
        return self.defausse.pop()


class Paquet:
    def __init__(self):
        self.file = FileDouble()
        for couleur in Carte.COULEURS:
            for hauteur in Carte.HAUTEURS:
                self.file.enfiler(Carte(hauteur, couleur))

    def melange(self):
        temp = self.file.pioche + self.file.defausse
        random.shuffle(temp)
        self.file.pioche, self.file.defausse = temp, []

    def distribue(self, n):
        return [self.file.defiler() for _ in range(n)]

    def affichages(self):
        return {
            "pioche": [str(carte) for carte in self.file.pioche],
            "defausse": [str(carte) for carte in self.file.defausse],
        }


class Main:
    def __init__(self, cartes):
        self.cartes = cartes

    def tri(self, decroissant=False, as_faible=False):
        def cle_tri(carte):
            hauteur_value = Carte.HAUTEURS.index(carte.hauteur())
            if as_faible and carte.hauteur() == "as":
                hauteur_value = -1
            return hauteur_value, Carte.COULEURS.index(carte.couleur())

        self.cartes.sort(key=cle_tri, reverse=decroissant)

    def affichage(self):
        return " ".join(str(carte) for carte in self.cartes)


class Joueur:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.score = 0
        self.main = None

    def assigner_main(self, cartes):
        self.main = Main(cartes)

    def jouer(self):
        carte = input(f"{self.pseudo}, choisissez une carte de votre main: {self.main.affichage()}\n")
        # Validation de la carte et autres fonctionnalités peuvent être ajoutées ici.
        return carte


class JoueurIA(Joueur):
    def jouer_automatiquement(self):
        # Implémentation basique : choisir une carte au hasard.
        return random.choice(self.main.cartes)


if __name__ == "__main__":
    # Pour les tests
    carte = Carte("as", "trèfle")
    print(carte)