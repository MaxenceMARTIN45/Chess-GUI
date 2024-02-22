# Importation des modules nécessaires
from Classes.GestionnaireEvenement import *
from Classes.Plateau import *
import pygame
import sys
import os

# Définition de la classe FenetrePrincipale
class FenetrePrincipale:
    # Initialisation de la fenêtre principale avec des valeurs par défaut
    fenetre = pygame.display.set_mode((520, 520))
    afficher = True
    plateau = Plateau()
    gestionnaireEvenement = GestionnaireEvenement()

    def __init__(self):
        # Chargement de l'icône et configuration de la fenêtre
        self.icone = pygame.image.load(os.path.join(os.getcwd(), "Images", "icone.png")).convert_alpha()
        pygame.display.set_icon(self.icone)
        pygame.display.set_caption('Jeu d’échecs')

    def afficher(self):
        # Boucle principale d'affichage
        while FenetrePrincipale.afficher:
            # Gestion des événements avec le gestionnaire d'événements
            self.gestionnaireEvenement.gererEvenements(FenetrePrincipale)
            
            # Affichage du plateau dans la fenêtre principale
            self.plateau.afficher(FenetrePrincipale, FenetrePrincipale.fenetre)
            
            # Mise à jour de l'affichage
            pygame.display.flip()

        # Fermeture propre de la fenêtre
        pygame.display.flip()
        pygame.quit()
        sys.exit()

# Création d'une instance de la classe FenetrePrincipale
fen = FenetrePrincipale()

# Appel de la méthode afficher pour démarrer la boucle d'affichage
fen.afficher()
