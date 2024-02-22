# Importation des classes

from Classes.GestionnaireEvenement import *
from Classes.Plateau import *

import pygame
# from pygame.locals import *
import sys
import os

# Classe FenetrePrincipale

class FenetrePrincipale:

    # Attributs

    fenetre = pygame.display.set_mode((520,520))
    #AttributeError: type object 'FenetrePrincipale' has no attribute 'fenetre'
    afficher = True
    #TypeError: 'bool' object is not callable # survient à fen.afficher()
    plateau = Plateau()
    #AttributeError: type object 'FenetrePrincipale' has no attribute 'plateau'
    gestionnaireEvenement = GestionnaireEvenement()

    # Constructeur

    def __init__(self):
        # Réglage de certains paramètres
        self.icone = pygame.image.load(os.path.join(os.getcwd(), "Images", "icone.png")).convert_alpha()
        pygame.display.set_icon(self.icone)
        pygame.display.set_caption('Jeu d’échecs') # titre

    # Méthodes

    def afficher(self):
        while FenetrePrincipale.afficher:
            # Gerer les évènements
            self.gestionnaireEvenement.gererEvenements(FenetrePrincipale)
            # Affichage du plateau
            self.plateau.afficher(FenetrePrincipale,FenetrePrincipale.fenetre)
            # Rafraichissement
            pygame.display.flip()

        # Au moment de quitter le jeu
        pygame.display.flip()
        pygame.quit()
        sys.exit()


fen=FenetrePrincipale()
fen.afficher()

