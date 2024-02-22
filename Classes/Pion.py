# Importation des classes nécessaires depuis différents fichiers
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

# Importation du module tkinter pour l'interface graphique
import tkinter as tk
from tkinter import simpledialog

# Définition de la classe Pion, héritant de la classe Piece
class Pion(Piece):

    # Initialisation de l'objet Pion avec sa position, sa couleur et son poste
    def __init__(self, case, couleur, poste):
        super().__init__(case, couleur, poste)
        self.AAvanceDeDeuxCase = False
        self.pieceDevant = False
        self.deplacementPossible = []
        # Définition des déplacements possibles en fonction de la couleur du pion
        if self.couleur == "blanc":
            self.deplacementPossible = [(-1, 0), (-2, 0)]
            self.deplacementMangerPossible = [(-1, -1), (-1, 1)]
        else:
            self.deplacementPossible = [(1, 0), (2, 0)]
            self.deplacementMangerPossible = [(1, 1), (1, -1)]

    # Méthode pour déterminer les cases où le pion peut se déplacer
    def caseOuLeDeplacementEstPossible(self, plateau, avecAffichage):
        caseActuelle = self.case.coordonnees_quadrillage
        casePossible = []
        
        # Vérifier les déplacements simples
        for deplacement in self.deplacementPossible:
            if self.pieceDevant == False:
                newCasePossible = (caseActuelle[0] + deplacement[0], caseActuelle[1] + deplacement[1])
                if self.estDansPlateau(newCasePossible):
                    for case in plateau.casesEchiquier:
                        if newCasePossible == case.coordonnees_quadrillage:
                            laCaseRecherchee = case
                            if laCaseRecherchee.occupeePar != None and laCaseRecherchee.occupeePar.couleur != self.couleur:
                                self.pieceDevant = True
                            elif laCaseRecherchee.occupeePar != None and laCaseRecherchee.occupeePar.couleur == self.couleur:
                                self.pieceDevant = True
                            else:
                                casePossible.append(laCaseRecherchee)
                                if avecAffichage == True:
                                    laCaseRecherchee.etatAffichage = {
                                        "normal": False, "echec": False, "rond": True, "targetPiece": False,
                                        "apresDeplacement": False, "passageSourisSurRond": False,
                                        "selectionDePiece": False}
                            break
        self.pieceDevant = False
        
        # Vérifier les déplacements pour manger une pièce
        for deplacement in self.deplacementMangerPossible:
            newCasePossible = (caseActuelle[0] + deplacement[0], caseActuelle[1] + deplacement[1])
            if self.estDansPlateau(newCasePossible):
                for case in plateau.casesEchiquier:
                    if newCasePossible == case.coordonnees_quadrillage:
                        laCaseRecherchee = case
                        if laCaseRecherchee.occupeePar != None and laCaseRecherchee.occupeePar.couleur != self.couleur:
                            casePossible.append(laCaseRecherchee)
                            if avecAffichage == True:
                                laCaseRecherchee.etatAffichage = {
                                    "normal": False, "echec": False, "rond": False, "targetPiece": True,
                                    "apresDeplacement": False, "passageSourisSurRond": False,
                                    "selectionDePiece": False}
                        elif laCaseRecherchee.occupeePar != None and laCaseRecherchee.occupeePar.couleur == self.couleur:
                            pass
                        else:
                            pass
                        break
        
        # Vérifier la possibilité d'effectuer le "en passant" (pion double avancement)
        if self.couleur == "blanc":
            if caseActuelle[0] == 4:
                caseADroite = (caseActuelle[0], caseActuelle[1] + 1)
                caseAGauche = (caseActuelle[0], caseActuelle[1] - 1)
                newCasesPossible = [caseADroite, caseAGauche]
                for newCasePossible in newCasesPossible:
                    if self.estDansPlateau(newCasePossible):
                        for case in plateau.casesEchiquier:
                            if newCasePossible == case.coordonnees_quadrillage:
                                laCaseRecherchee = case
                                if case.occupeePar != None:
                                    if case.occupeePar.poste == "pion" and case.occupeePar.couleur == "noir":
                                        if self.AAvanceDeDeuxCase and case == plateau.casesDeplacee[-1]:
                                            caseDeDeplacement = (newCasePossible[0] - 1, newCasePossible[1])
                                            caseRecherchee = self.caseAssocieAUneCaseQuadrillage(caseDeDeplacement, plateau)
                                            casePossible.append(caseRecherchee)
                                            if avecAffichage == True:
                                                caseRecherchee.etatAffichage = {
                                                    "normal": False, "echec": False, "rond": True, "targetPiece": False,
                                                    "apresDeplacement": False, "passageSourisSurRond": False,
                                                    "selectionDePiece": False}
        else:
            if caseActuelle[0] == 5:
                caseADroite = (caseActuelle[0], caseActuelle[1] + 1)
                caseAGauche = (caseActuelle[0], caseActuelle[1] - 1)
                newCasesPossible = [caseADroite, caseAGauche]
                for newCasePossible in newCasesPossible:
                    if self.estDansPlateau(newCasePossible):
                        for case in plateau.casesEchiquier:
                            if newCasePossible == case.coordonnees_quadrillage:
                                laCaseRecherchee = case
                                if case.occupeePar != None:
                                    if case.occupeePar.poste == "pion" and case.occupeePar.couleur == "blanc":
                                        if self.AAvanceDeDeuxCase and case == plateau.casesDeplacee[-1]:
                                            caseDeDeplacement = (newCasePossible[0] + 1, newCasePossible[1])
                                            caseRecherchee = self.caseAssocieAUneCaseQuadrillage(caseDeDeplacement, plateau)
                                            casePossible.append(caseRecherchee)
                                            if avecAffichage == True:
                                                caseRecherchee.etatAffichage = {
                                                    "normal": False, "echec": False, "rond": True, "targetPiece": False,
                                                    "apresDeplacement": False, "passageSourisSurRond": False,
                                                    "selectionDePiece": False}
        return casePossible

    # Méthode pour associer une case à des coordonnées de quadrillage
    def caseAssocieAUneCaseQuadrillage(self, caseQuadrillage, plateau):
        for case in plateau.casesEchiquier:
            if caseQuadrillage == case.coordonnees_quadrillage:
                return case

    # Méthode pour vérifier si une case est dans le plateau
    def estDansPlateau(self, newCasePossible):
        if 1 <= newCasePossible[0] <= 8 and 1 <= newCasePossible[1] <= 8:
            return True
        else:
            return False

    # Méthode pour gérer la promotion du pion
    def promotion(self, plateau):
        if self.couleur == "blanc":
            if self.case.coordonnees_quadrillage[0] == 1:
                laPiece = self.processusDePromotion(plateau)
                plateau.piecesEchiquier.append(laPiece)
                plateau.piecesBlancEchiquier.append(laPiece)
        else:
            if self.case.coordonnees_quadrillage[0] == 8:
                laPiece = self.processusDePromotion(plateau)
                plateau.piecesEchiquier.append(laPiece)
                plateau.piecesNoirEchiquier.append(laPiece)

    # Méthode pour gérer le processus de promotion du pion
    def processusDePromotion(self, plateau):
        input_incorrecte = True
        while input_incorrecte:
            # Création d'une fenêtre de dialogue pour choisir la pièce de promotion
            root = tk.Tk()
            root.withdraw()
            choix_pieces = {
                'reine': Reine,
                'tour': Tour,
                'fou': Fou,
                'cavalier': Cavalier,
                'pion': Pion
            }
            pieceSouhaite = simpledialog.askstring("Promotion du pion",
                                                  "Choisissez votre pièce :\nReine : reine\nTour : tour\nFou : fou\nCavalier : cavalier\nPion : pion")
            if pieceSouhaite in choix_pieces:
                plateau.supprimerLaPiece(self)
                piece = choix_pieces[pieceSouhaite](self.case, self.couleur, pieceSouhaite)
                input_incorrecte = False
                self.case.occupeePar = piece
                return piece
            else:
                # Affichage d'une erreur si l'entrée n'est pas valide
                error_message = "Entrée non valide. Veuillez choisir parmi les options proposées."
                tk.messagebox.showerror("Erreur", error_message)
                continue
