# Importation des classes

from Classes.Case import *
from Classes.Cavalier import *
from Classes.FenetrePrincipale import *
from Classes.Fou import *
from Classes.GestionnaireEvenement import *
from Classes.Piece import *
from Classes.Pion import *
from Classes.Plateau import *
from Classes.Reine import *
from Classes.Roi import *
from Classes.Tour import *

import os
# import pygame
# from pygame.locals import *
# import sys
import json

# Classe Plateau

class Plateau:

    # Constructeur

    def __init__(self):
        # Attributs
        self.casesEchiquier = []
        self.piecesEchiquier = []
        self.piecesBlancEchiquier = []
        self.piecesNoirEchiquier = []
        #
        self.casesDeplacee = []
        # Initialisation des attributs
        # Chargement des fichiers JSON
        with open(os.path.join(os.getcwd(), "Initialization Data", "dataPiece.json")) as json_data:
            dataPiece = json.load(json_data) # dictionnaire
        with open(os.path.join(os.getcwd(), "Initialization Data", "dataCase.json")) as json_data:
            dataCase = json.load(json_data)  # dictionnaire
        # Initialisation des Cases
        for donnees in dataCase.values():
            origine_pixel_tuple = (donnees["origine_pixel"]["x"],donnees["origine_pixel"]["y"])
            coordonnees_quadrillage_tuple = (donnees["coordonnees_quadrillage"]["ligne"],donnees["coordonnees_quadrillage"]["colonne"])
            case = Case(donnees["nom"],donnees["couleur"],origine_pixel_tuple,coordonnees_quadrillage_tuple)
            self.casesEchiquier.append(case)
        # Initialisation des Pieces
        for donnees in dataPiece.values():
            cases = donnees["caseInitialisation"] # plusieurs à priori
            for case in cases:
                for caseEchiquier in self.casesEchiquier:
                    if caseEchiquier.nom==case:
                        if donnees['poste'] == "pion":
                            piece = Pion(caseEchiquier,donnees['couleur'],donnees['poste'])
                        elif donnees['poste'] == "roi":
                            piece = Roi(caseEchiquier,donnees['couleur'],donnees['poste'])
                        elif donnees['poste'] == "cavalier":
                            piece = Cavalier(caseEchiquier,donnees['couleur'],donnees['poste'])
                        elif donnees['poste'] == "tour":
                            piece = Tour(caseEchiquier,donnees['couleur'],donnees['poste'])
                        elif donnees['poste'] == "fou":
                            piece = Fou(caseEchiquier,donnees['couleur'],donnees['poste'])
                        elif donnees['poste'] == "reine":
                            piece = Reine(caseEchiquier,donnees['couleur'],donnees['poste'])
                        else:
                            print("Problème de création d'une piece")
                        # On informe la case qu'elle est occupee
                        caseEchiquier.occupeePar = piece
                        # On ajoute la piece à l'échiquier
                        self.piecesEchiquier.append(piece)
                        if piece.couleur=="blanc":
                            self.piecesBlancEchiquier.append(piece)
                        else:
                            self.piecesNoirEchiquier.append(piece)

    # Méthodes

    def afficher(self,fenetrePrincipale,fenetre):
        # Affichage des cases
        for case in self.casesEchiquier:
            case.afficher(fenetrePrincipale,fenetrePrincipale.fenetre)
        # Affichage des pieces
        for piece in self.piecesEchiquier:
            piece.afficher(fenetrePrincipale,fenetrePrincipale.fenetre)

    def indice(self,element,liste):
        compteur = 0
        for i in liste:
            if element==i:
                return(compteur)
            compteur += 1
        return(None)

    def supprimerLaPiece(self,piece):
        # Supprimer la piece qu'on mange dans piecesEchiquier
        pieceASupprimer = piece
        indiDeLaPieceASupprimer = self.indice(pieceASupprimer,self.piecesEchiquier)
        self.piecesEchiquier.pop(indiDeLaPieceASupprimer)
        # Supprimer la piece qu'on mange dans piecesBlancEchiquier ou piecesNoirEchiquier
        if pieceASupprimer.couleur == "blanc":
            indiDeLaPieceASupprimer = self.indice(pieceASupprimer,self.piecesBlancEchiquier)
            self.piecesBlancEchiquier.pop(indiDeLaPieceASupprimer)
        else: # noir
            indiDeLaPieceASupprimer = self.indice(pieceASupprimer,self.piecesNoirEchiquier)
            self.piecesNoirEchiquier.pop(indiDeLaPieceASupprimer)

    def remiseAZeroAffichageCase(self):
        for case in self.casesEchiquier:
            case.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}

    def affichageEchec(self,case):
        case.etatAffichage = {"normal":False,"echec":True,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}

    def affichageCaseDeplacementPossible(self,case):
        case.etatAffichage = {"normal":False,"echec":False,"rond":True,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}

    def affichageTargetPiece(self,case):
        case.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":True,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}

    def affichageApresDeplacement(self,case):
        case.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":True,"passageSourisSurRond":False,"selectionDePiece":False}

    def affichagePassageSourisSurRond(self,case):
        case.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":True,"selectionDePiece":False}

    def affichageSelectionDePiece(self,case):
        case.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":True}
