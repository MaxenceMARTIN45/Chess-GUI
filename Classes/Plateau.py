# Importation des classes nécessaires
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
import json

# Définition de la classe Plateau
class Plateau:
    # Constructeur de la classe Plateau
    def __init__(self):
        # Initialisation des listes et chargement des données depuis les fichiers JSON
        self.casesEchiquier = []
        self.piecesEchiquier = []
        self.piecesBlancEchiquier = []
        self.piecesNoirEchiquier = []
        self.casesDeplacee = []

        with open(os.path.join(os.getcwd(), "Initialization Data", "dataPiece.json")) as json_data:
            dataPiece = json.load(json_data)

        with open(os.path.join(os.getcwd(), "Initialization Data", "dataCase.json")) as json_data:
            dataCase = json.load(json_data)

        for donnees in dataCase.values():
            origine_pixel_tuple = (donnees["origine_pixel"]["x"], donnees["origine_pixel"]["y"])
            coordonnees_quadrillage_tuple = (donnees["coordonnees_quadrillage"]["ligne"], donnees["coordonnees_quadrillage"]["colonne"])
            case = Case(donnees["nom"], donnees["couleur"], origine_pixel_tuple, coordonnees_quadrillage_tuple)
            self.casesEchiquier.append(case)

        for donnees in dataPiece.values():
            cases = donnees["caseInitialisation"]
            for case in cases:
                for caseEchiquier in self.casesEchiquier:
                    if caseEchiquier.nom == case:
                        if donnees['poste'] == "pion":
                            piece = Pion(caseEchiquier, donnees['couleur'], donnees['poste'])
                        elif donnees['poste'] == "roi":
                            piece = Roi(caseEchiquier, donnees['couleur'], donnees['poste'])
                        elif donnees['poste'] == "cavalier":
                            piece = Cavalier(caseEchiquier, donnees['couleur'], donnees['poste'])
                        elif donnees['poste'] == "tour":
                            piece = Tour(caseEchiquier, donnees['couleur'], donnees['poste'])
                        elif donnees['poste'] == "fou":
                            piece = Fou(caseEchiquier, donnees['couleur'], donnees['poste'])
                        elif donnees['poste'] == "reine":
                            piece = Reine(caseEchiquier, donnees['couleur'], donnees['poste'])
                        else:
                            print("Problème de création d'une piece")
                        
                        caseEchiquier.occupeePar = piece
                        self.piecesEchiquier.append(piece)
                        
                        if piece.couleur == "blanc":
                            self.piecesBlancEchiquier.append(piece)
                        else:
                            self.piecesNoirEchiquier.append(piece)

    # Méthode pour afficher le plateau
    def afficher(self, fenetrePrincipale, fenetre):
        for case in self.casesEchiquier:
            case.afficher(fenetrePrincipale, fenetrePrincipale.fenetre)

        for piece in self.piecesEchiquier:
            piece.afficher(fenetrePrincipale, fenetrePrincipale.fenetre)

    # Méthode de recherche de l'indice d'un élément dans une liste
    def indice(self, element, liste):
        compteur = 0
        for i in liste:
            if element == i:
                return(compteur)
            compteur += 1
        return(None)

    # Méthode de suppression d'une pièce du plateau
    def supprimerLaPiece(self, piece):
        pieceASupprimer = piece
        indiDeLaPieceASupprimer = self.indice(pieceASupprimer, self.piecesEchiquier)
        self.piecesEchiquier.pop(indiDeLaPieceASupprimer)

        if pieceASupprimer.couleur == "blanc":
            indiDeLaPieceASupprimer = self.indice(pieceASupprimer, self.piecesBlancEchiquier)
            self.piecesBlancEchiquier.pop(indiDeLaPieceASupprimer)
        else:
            indiDeLaPieceASupprimer = self.indice(pieceASupprimer, self.piecesNoirEchiquier)
            self.piecesNoirEchiquier.pop(indiDeLaPieceASupprimer)

    # Méthode de réinitialisation de l'affichage des cases
    def remiseAZeroAffichageCase(self):
        for case in self.casesEchiquier:
            case.etatAffichage = {"normal": True, "echec": False, "rond": False, "targetPiece": False,
                                  "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}

    # Méthode d'affichage d'une case en situation d'échec
    def affichageEchec(self, case):
        case.etatAffichage = {"normal": False, "echec": True, "rond": False, "targetPiece": False,
                              "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}

    # Méthode d'affichage d'une case comme possible pour le déplacement
    def affichageCaseDeplacementPossible(self, case):
        case.etatAffichage = {"normal": False, "echec": False, "rond": True, "targetPiece": False,
                              "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}

    # Méthode d'affichage d'une case comme cible de déplacement pour une pièce
    def affichageTargetPiece(self, case):
        case.etatAffichage = {"normal": False, "echec": False, "rond": False, "targetPiece": True,
                              "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}

    # Méthode d'affichage d'une case après le déplacement d'une pièce
    def affichageApresDeplacement(self, case):
        case.etatAffichage = {"normal": False, "echec": False, "rond": False, "targetPiece": False,
                              "apresDeplacement": True, "passageSourisSurRond": False, "selectionDePiece": False}

    # Méthode d'affichage d'une case lors du passage de la souris sur un rond
    def affichagePassageSourisSurRond(self, case):
        case.etatAffichage = {"normal": False, "echec": False, "rond": False, "targetPiece": False,
                              "apresDeplacement": False, "passageSourisSurRond": True, "selectionDePiece": False}

    # Méthode d'affichage d'une case lors de la sélection d'une pièce
    def affichageSelectionDePiece(self, case):
        case.etatAffichage = {"normal": False, "echec": False, "rond": False, "targetPiece": False,
                              "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": True}
