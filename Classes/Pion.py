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

import tkinter as tk
from tkinter import simpledialog

# import pygame
# from pygame.locals import *
# import sys

# Classe Pion

class Pion(Piece):

    def __init__(self,case,couleur,poste):
        # Attributs
        super().__init__(case,couleur,poste)
        #self.numeroDucoup = 0 # utile pour 1er deplacement
        #
        #self.deplacementEffectueALInstantEtAvanceDeDeuxCase = False
        self.AAvanceDeDeuxCase = False
        #
        self.pieceDevant = False
        #
        self.deplacementPossible = []
        # Initialisation
        if self.couleur == "blanc":
            self.deplacementPossible = [(-1,0),(-2,0)]
            self.deplacementMangerPossible = [(-1,-1),(-1,1)]
        else:
            self.deplacementPossible = [(1,0),(2,0)]
            self.deplacementMangerPossible = [(1,1),(1,-1)]



    def caseOuLeDeplacementEstPossible(self,plateau,avecAffichage):#,gestionnaireEvenement):
        # Déplacement en avant
        caseActuelle = self.case.coordonnees_quadrillage
        casePossible = []
        for deplacement in self.deplacementPossible:
            if self.pieceDevant == False:
                newCasePossible = (caseActuelle[0]+deplacement[0],caseActuelle[1]+deplacement[1])
                if self.estDansPlateau(newCasePossible):
                    # Trouver la case associée
                    for case in plateau.casesEchiquier:
                        if newCasePossible == case.coordonnees_quadrillage:
                            laCaseRecherchee = case
                            # Regarder si une piece est sur cette case
                            if laCaseRecherchee.occupeePar!=None and laCaseRecherchee.occupeePar.couleur!=self.couleur:
                                # ie est occupee par un adversaire -> on ne peux pas y aller avec le déplacement standard du pion
                                self.pieceDevant = True
                                pass
                                #casePossible.append(laCaseRecherchee)
                                #if avecAffichage == True:
                                #    laCaseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":True,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
                            elif laCaseRecherchee.occupeePar!=None and laCaseRecherchee.occupeePar.couleur==self.couleur:
                                # ie est occupee par un camarade -> rien
                                self.pieceDevant = True
                                pass
                            else:
                                # ie est occupee par personne -> rond
                                casePossible.append(laCaseRecherchee)
                                if avecAffichage == True:
                                    laCaseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":True,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
                            break # pas utile de continuer a itérer puisqu'on a trouver la case
        self.pieceDevant = False
        # Manger en diagonale
        # Rajout vis-à-vis du déplacement pour manger particulier du pion
        # Si il y a une pieceAdversaire sur une des deux cases deplacementMangerPossible alors rajouter ces/cet case(s) au casePossible
        for deplacement in self.deplacementMangerPossible:
            newCasePossible = (caseActuelle[0]+deplacement[0],caseActuelle[1]+deplacement[1])
            if self.estDansPlateau(newCasePossible):
                # Trouver la case associée
                for case in plateau.casesEchiquier:
                    if newCasePossible == case.coordonnees_quadrillage:
                        laCaseRecherchee = case
                        # Regarder si une piece est sur cette case
                        if laCaseRecherchee.occupeePar!=None and laCaseRecherchee.occupeePar.couleur!=self.couleur:
                            # ie est occupee par un adversaire -> target
                            casePossible.append(laCaseRecherchee)
                            if avecAffichage == True:
                                laCaseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":True,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
                        elif laCaseRecherchee.occupeePar!=None and laCaseRecherchee.occupeePar.couleur==self.couleur:
                            # ie est occupee par un camarade -> rien
                            pass
                        else:
                            # ie est occupee par personne -> rien
                            pass
                            #casePossible.append(laCaseRecherchee)
                            #if avecAffichage == True:
                            #    laCaseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":True,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
                        break # pas utile de continuer a itérer puisqu'on a trouver la case
        #
        # Prise en passant # même déplacement qu'un deplacementMangerPossible
        # caseActuelle
        if self.couleur == "blanc":
            if caseActuelle[0]==4: # si mon pion est sur la bonne ligne
                #print("ici blanc !")
                caseADroite = (caseActuelle[0],caseActuelle[1]+1)
                caseAGauche = (caseActuelle[0],caseActuelle[1]-1)
                newCasesPossible = [caseADroite,caseAGauche]
                #print(newCasesPossible)
                for newCasePossible in newCasesPossible:
                    if self.estDansPlateau(newCasePossible):
                        # Trouver la case associée
                        for case in plateau.casesEchiquier:
                            if newCasePossible == case.coordonnees_quadrillage:
                                laCaseRecherchee = case
                                #print('ici')
                                if case.occupeePar != None: # si il y a une piece a coté de mon pion
                                    #print('ici')
                                    if case.occupeePar.poste == "pion" and case.occupeePar.couleur == "noir": # si cette pièce est un pion d'une couleur différente de moi
                                        #print('ici')
                                        #print(self.poste,self.couleur)
                                        #print(self.deplacementEffectueALInstantEtAvanceDeDeuxCase)
                                        #
                                        #if self.AAvanceDeDeuxCase and self.vientDEtreJoue: # si ce pion vient juste de se déplacer de deux cases
                                        if self.AAvanceDeDeuxCase and case==plateau.casesDeplacee[-1]:
                                            print('ici')
                                            print(self.poste,self.couleur)
                                            caseDeDeplacement = (newCasePossible[0]-1,newCasePossible[1]) #
                                            caseRecherchee = self.caseAssocieAUneCaseQuadrillage(caseDeDeplacement,plateau)
                                            #print(caseRecherchee.nom)
                                            casePossible.append(caseRecherchee)
                                            if avecAffichage == True:
                                                caseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":True,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
        else: # noir
            if caseActuelle[0]==5:
                #print("ici noir !")
                caseADroite = (caseActuelle[0],caseActuelle[1]+1)
                caseAGauche = (caseActuelle[0],caseActuelle[1]-1)
                newCasesPossible = [caseADroite,caseAGauche]
                for newCasePossible in newCasesPossible:
                    if self.estDansPlateau(newCasePossible):
                        # Trouver la case associée
                        for case in plateau.casesEchiquier:
                            if newCasePossible == case.coordonnees_quadrillage:
                                laCaseRecherchee = case
                                #print('ou la')
                                if case.occupeePar != None: # si il y a une piece a coté de mon pion
                                    if case.occupeePar.poste == "pion" and case.occupeePar.couleur == "blanc": # si cette pièce est un pion d'une couleur différente de moi
                                        #if self.AAvanceDeDeuxCase and self.vientDEtreJoue: # si ce pion vient juste de se déplacer de deux cases
                                        if self.AAvanceDeDeuxCase and case==plateau.casesDeplacee[-1]:
                                            caseDeDeplacement = (newCasePossible[0]+1,newCasePossible[1])
                                            caseRecherchee = self.caseAssocieAUneCaseQuadrillage(caseDeDeplacement,plateau)
                                            casePossible.append(caseRecherchee)
                                            if avecAffichage == True:
                                                caseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":True,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
        #
        return(casePossible)

    def caseAssocieAUneCaseQuadrillage(self,caseQuadrillage,plateau):
        for case in plateau.casesEchiquier:
            if caseQuadrillage == case.coordonnees_quadrillage:
                laCaseRecherchee = case
                return(case)


    def estDansPlateau(self,newCasePossible):
        if 1<=newCasePossible[0]<=8 and 1<=newCasePossible[1]<=8:
            return(True)
        else:
            return(False)

    def promotion(self,plateau):
        if self.couleur == "blanc":
            if self.case.coordonnees_quadrillage[0]==1:
                laPiece = self.processusDePromotion(plateau)
                # Ajouté la nouvelle pièce au différentes liste piecesEchiquier,piecesBlancEchiquier,piecesNoirEchiquier
                plateau.piecesEchiquier.append(laPiece)
                plateau.piecesBlancEchiquier.append(laPiece)
        else: # noir
            if self.case.coordonnees_quadrillage[0]==8:
                laPiece = self.processusDePromotion(plateau)
                # Ajouté la nouvelle pièce au différentes liste piecesEchiquier,piecesBlancEchiquier,piecesNoirEchiquier
                plateau.piecesEchiquier.append(laPiece)
                plateau.piecesNoirEchiquier.append(laPiece)

    def processusDePromotion(self,plateau):
        while True:
            # Création d'une fenêtre tkinter
            root = tk.Tk()
            root.withdraw()  # Cacher la fenêtre principale

            # Affichage d'une boîte de dialogue pour obtenir l'entrée de l'utilisateur
            pieceSouhaite = simpledialog.askstring("Promotion du pion", 
                                                "Choisissez votre pièce :\nReine : reine\nTour : tour\nFou : fou\nCavalier : cavalier\nPion : pion")

            # Déselection de la pièce associée à la case et suppression du pion
            self.case.occupeePar = None
            plateau.supprimerLaPiece(self)

            # Création d'une nouvelle pièce
            if pieceSouhaite == 'reine':
                piece = Reine(self.case, self.couleur, "reine")
            elif pieceSouhaite == 'tour':
                piece = Tour(self.case, self.couleur, "tour")
            elif pieceSouhaite == 'fou':
                piece = Fou(self.case, self.couleur, "fou")
            elif pieceSouhaite == 'cavalier':
                piece = Cavalier(self.case, self.couleur, "cavalier")
            elif pieceSouhaite == 'pion':
                piece = Pion(self.case, self.couleur, "pion")
            else:
                # Affiche un message d'erreur dans la fenêtre tkinter
                error_message = "Entrée non valide. Veuillez choisir parmi les options proposées."
                tk.messagebox.showerror("Erreur", error_message)
                continue

            # Informe la case qu'elle est occupée
            piece.case.occupeePar = piece
            return piece
