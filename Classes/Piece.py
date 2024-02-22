# Import des modules nécessaires
from Classes.Case import *
import pygame
import os

# Définition de la classe Piece
class Piece:
    # Constructeur de la classe Piece
    def __init__(self, case, couleur, poste):
        # Initialisation des attributs de la pièce
        self.case = case  # Case sur laquelle se trouve la pièce
        self.couleur = couleur  # Couleur de la pièce (blanc ou noir)
        self.poste = poste  # Type de la pièce (pion, tour, etc.)
        self.image = None  # Chemin de l'image représentant la pièce
        self.vientDEtreJoue = False  # Indicateur pour savoir si la pièce vient d'être jouée
        self.selectionne = False  # Indicateur pour savoir si la pièce est sélectionnée

    # Méthode pour afficher la pièce sur la fenêtre
    def afficher(self, fenetrePrincipale, fenetre):
        # Construction du chemin de l'image en fonction du type et de la couleur de la pièce
        self.image = os.path.join(os.getcwd(), "Images", self.poste + "-" + self.couleur + ".png")
        # Affichage de l'image sur la fenêtre principale à la position de la case de la pièce
        fenetrePrincipale.fenetre.blit(pygame.image.load(self.image).convert_alpha(), self.case.origine_pixel)

    # Méthode pour déplacer la pièce vers une nouvelle case
    def deplacer(self, nouvelle_case):
        # Libération de l'ancienne case
        self.case.occupeePar = None
        # Vérification si la nouvelle case n'est pas vide
        if nouvelle_case is not None:
            # Déplacement de la pièce vers la nouvelle case
            self.case = nouvelle_case
            # Mise à jour de la nouvelle case pour indiquer qu'elle est occupée par cette pièce
            self.case.occupeePar = self
            # Gestion spécifique pour les pions (réduction des déplacements possibles après le premier déplacement)
            if self.poste == "pion":
                if len(self.deplacementPossible) == 2:
                    self.deplacementPossible.pop()
        else:
            # Affichage d'une erreur si la nouvelle case est vide
            print('Erreur : la case est vide')
