# Importation pour Pygame

from Classes.Case import *

import pygame
# from pygame.locals import *
# import sys
import os

# Classe Piece

class Piece:

    #Constructeur

    def __init__(self,case,couleur,poste):
        # Attributs
        self.case = case
        self.couleur = couleur
        self.poste = poste
        self.image = None
        #
        self.vientDEtreJoue = False
        #
        self.selectionne = False


    # Méthodes

    def afficher(self,fenetrePrincipale,fenetre):
        # chemin = os.path.join(os.getcwd(), "Images", "ImagesOK", self.poste + "-" + self.couleur + ".png")
        # self.image = pygame.image.load(chemin).convert_alpha()
        self.image = os.path.join(os.getcwd(), "Images", self.poste + "-" + self.couleur + ".png")
        fenetrePrincipale.fenetre.blit(pygame.image.load(self.image).convert_alpha(),self.case.origine_pixel)

    def deplacer(self,nouvelle_case):
        self.case.occupeePar=None
        if nouvelle_case != None:
            self.case=nouvelle_case
            self.case.occupeePar=self
            if self.poste == "pion":
                if len(self.deplacementPossible)==2:
                    self.deplacementPossible.pop()
        else:
            print('Erreur la case est vide')
