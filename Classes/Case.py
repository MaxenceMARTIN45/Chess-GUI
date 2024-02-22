import pygame
import os

class Case:
    def __init__(self, nom, couleur, origine_pixel, coordonnees_quadrillage):
        # Initialisation des attributs de la classe Case
        self.nom = nom
        self.couleur = couleur
        self.image = None
        self.origine_pixel = origine_pixel
        self.coordonnees_quadrillage = coordonnees_quadrillage
        self.dimension = 65
        self.rect_origine_pixel = (self.origine_pixel[0], self.origine_pixel[1])
        self.rect_dimension = (self.dimension, self.dimension)
        self.occupeePar = None
        # Un dictionnaire pour gérer les différents états d'affichage de la case
        self.etatAffichage = {"normal": True, "echec": False, "rond": False, "targetPiece": False, "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}

    def afficher(self, fenetrePrincipale, fenetre):
        # Méthode pour afficher la case en fonction de son état d'affichage
        for cle, valeur in self.etatAffichage.items():
            if valeur:
                # Construire le chemin de l'image en fonction de l'état
                self.image = os.path.join(os.getcwd(), "Images", "case " + self.couleur + " " + cle + ".png")
        # Afficher l'image sur la fenêtre principale à la position de la case
        fenetrePrincipale.fenetre.blit(pygame.image.load(self.image).convert_alpha(), self.origine_pixel)

    def estDedans(self, positionPixel):
        # Vérifier si une position en pixels est à l'intérieur de la case
        if self.origine_pixel[0] <= positionPixel[0] <= self.origine_pixel[0] + self.dimension and self.origine_pixel[1] <= positionPixel[1] <= self.origine_pixel[1] + self.dimension:
            return True
        return False

    def caseDejaOccupee(self, plateau):
        # Vérifier si la case est déjà occupée par une pièce sur le plateau
        for piece in plateau.piecesEchiquier:
            if self == piece.case:
                return True
        return False
