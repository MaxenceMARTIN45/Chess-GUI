# Importation des classes

import pygame
# from pygame.locals import *
# import sys
import os

# Classe Case

class Case:

    # Constructeur

    def __init__(self,nom,couleur,origine_pixel,coordonnees_quadrillage):
        # Attributs
        self.nom = nom
        self.couleur = couleur
        self.image = None
        self.origine_pixel = origine_pixel # tuples # en pixel
        self.coordonnees_quadrillage = coordonnees_quadrillage # tuples # en entier (1,1) (1,8) (8,8)
        #
        self.dimension = 65 # en pixel
        self.rect_origine_pixel = (self.origine_pixel[0],self.origine_pixel[1])
        self.rect_dimension = (self.dimension,self.dimension)
        # zone = pygame.Rect(self.rect_origine_pixel,self.rect_dimension)
        #self.zone = pygame.Rect((self.origine_pixel[0],self.origine_pixel[1]),(self.dimension,self.dimension)) # (localisation horizontale,localisation verticale),(largeur,hauteur)
        #self.surface = pygame.Surface(self.zone.size)
        #
        self.occupeePar = None
        #self.selectionne = False
        #self.etatPiece = {"vide":True,"occupe":False} # etatPiece ne doit contenir que un élément True
        self.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True

    # Méthodes

    def afficher(self,fenetrePrincipale,fenetre):
        for cle,valeur in self.etatAffichage.items():
            if valeur: # == True
                # chemin = os.path.join(os.getcwd(), "Images", "ImagesOK", "case " + self.couleur + " " + cle + ".png")
                # self.image = pygame.image.load(chemin).convert_alpha()
                self.image = os.path.join(os.getcwd(), "Images", "case " + self.couleur + " " + cle + ".png")
        # Affichage
        fenetrePrincipale.fenetre.blit(pygame.image.load(self.image).convert_alpha(),self.origine_pixel)

    def estDedans(self,positionPixel):
        if self.origine_pixel[0]<=positionPixel[0]<=self.origine_pixel[0]+self.dimension and self.origine_pixel[1]<=positionPixel[1]<=self.origine_pixel[1]+self.dimension:
            #print('true!')
            return(True)
        #print('false!')
        return(False)

    def caseDejaOccupee(self,plateau):
        for piece in plateau.piecesEchiquier:
            if self==piece.case:
                return(True)
        return(False)

