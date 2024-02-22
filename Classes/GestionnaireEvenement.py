# Importation pour Pygame

from Classes.Plateau import *

import pygame
from pygame.locals import *
# import sys
import copy
# import pickle

# Classe GestionnaireEvenement

class GestionnaireEvenement:

    #Constructeur

    def __init__(self):
        # Attributs
        self.pieceSelectionnee = None
        self.caseCliquee = None
        self.tourDuJoueur = "blanc"
        self.casesAvancees = None # tuple de cases
        self.casesPossibles = None # liste de cases
        #
        #self.casesDeplacee = []
        #
        #self.simulation = False

    def gererEvenements(self,FenetrePrincipale):
        #FenetrePrincipale.plateau.majEtatCase()
        for event in pygame.event.get():
            # Si Instruction de quitter
            self.quitterSiInstruction(event,FenetrePrincipale)
            #
            #self.gestionDesPiecesQuiViennentDEtreJouee(FenetrePrincipale.plateau)
            #print('bonjour')
            self.affichageEchec(FenetrePrincipale.plateau)
            #
            self.enregistreLaCaseCliquee(event,FenetrePrincipale.plateau)
            self.regarderSiCorrespondAUnePieceASelectionner(FenetrePrincipale.plateau)
            self.regarderSiCorrespondAUnePieceAAttaquer(FenetrePrincipale.plateau)
            #
            for piece in FenetrePrincipale.plateau.piecesEchiquier:
                if piece.poste == "pion":
                    piece.promotion(FenetrePrincipale.plateau)
            #self.gestionDesPiecesQuiViennentDEtreJouee(FenetrePrincipale.plateau)
            #
            #self.affichageEchec(FenetrePrincipale.plateau)
            #print(self.pieceSelectionnee,self.caseCliquee,self.tourDuJoueur,self.casesPossibles)

    def quitterSiInstruction(self,event,FenetrePrincipale):
        if event.type == QUIT:
            FenetrePrincipale.afficher = False

    def enregistreLaCaseCliquee(self,event,plateau):
        if event.type == MOUSEBUTTONDOWN:
            for case in plateau.casesEchiquier:
                if pygame.Rect(case.rect_origine_pixel,case.rect_dimension).collidepoint(event.pos):
                    print("Tu as cliqué sur la case : ", case.nom)
                    self.caseCliquee = case

    def caseCliqueeCorrespondAUnePiece(self):
        if self.caseCliquee.occupeePar != None:
            return(True)
        else:
            return(False)

    def pasEncoreDePieceSelectionnee(self):
        if self.pieceSelectionnee == None:
            return(True)
        else:
            return(False)

    def bonneCouleur(self):
        if self.caseCliquee.occupeePar.couleur == self.tourDuJoueur:
            return(True)
        else:
            return(False)

    def regarderSiCorrespondAUnePieceASelectionner(self,plateau):
        if self.caseCliquee !=None and self.caseCliqueeCorrespondAUnePiece() and self.pasEncoreDePieceSelectionnee() and self.bonneCouleur():
            self.pieceSelectionnee = self.caseCliquee.occupeePar
            self.pieceSelectionnee.case.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":True} # etatAffichage ne doit contenir que un élément True
            #
            #print('concret')
            self.casesPossibles = self.pieceSelectionnee.caseOuLeDeplacementEstPossible(plateau,avecAffichage=True)#,GestionnaireEvenement)
            # Modification
            casesPossiblesApresVerificationEchec,casesImpossibleApresVerification=self.verifieCasesPossiblesAvecEchecAuRoiPrisEnCompte(self.pieceSelectionnee,self.casesPossibles,plateau)
            for case in casesImpossibleApresVerification:
                case.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True
            self.casesPossibles = casesPossiblesApresVerificationEchec
            #
            self.caseCliquee = None
        #else:
        #    self.pieceSelectionnee = None

# verifieCasesPossiblesAvecEchecAuRoiPrisEnCompte(self,piece,casesPossibles,plateau)
# return(casesPossiblesApresVerificationEchec,casesImpossibleApresVerification)

    def caseCliqueeAppartientACasesPossibles(self):
        for case in self.casesPossibles:
            if case == self.caseCliquee:
                return(True)
        return(False)

    def indice(self,element,liste):
        compteur = 0
        for i in liste:
            if element==i:
                return(compteur)
            compteur += 1
        return(None)

    def supprimerLaPiece(self,piece,plateau):
        # Supprimer la piece qu'on mange dans piecesEchiquier
        pieceASupprimer = piece
        indiDeLaPieceASupprimer = GestionnaireEvenement.indice(self,pieceASupprimer,plateau.piecesEchiquier)
        plateau.piecesEchiquier.pop(indiDeLaPieceASupprimer)
        # Supprimer la piece qu'on mange dans piecesBlancEchiquier ou piecesNoirEchiquier
        if pieceASupprimer.couleur == "blanc":
            indiDeLaPieceASupprimer = GestionnaireEvenement.indice(self,pieceASupprimer,plateau.piecesBlancEchiquier)
            plateau.piecesBlancEchiquier.pop(indiDeLaPieceASupprimer)
        else: # noir
            indiDeLaPieceASupprimer = GestionnaireEvenement.indice(self,pieceASupprimer,plateau.piecesNoirEchiquier)
            plateau.piecesNoirEchiquier.pop(indiDeLaPieceASupprimer)

    def regarderSiCorrespondAUnePieceAAttaquer(self,plateau):
        if self.caseCliquee != None and self.pieceSelectionnee != None:
            #print(self.casesPossibles)
            # Désactiver l'affichage de sélection de la pièce
            self.pieceSelectionnee.case.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True
            if self.casesPossibles != None and self.caseCliqueeAppartientACasesPossibles():
                # Effacer les casesAvancees précedentes
                if self.casesAvancees != None:
                    for case in self.casesAvancees:
                        case.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True
                # Puis les remplacer par les nouvelles
                self.casesAvancees = (self.pieceSelectionnee.case,self.caseCliquee) # on écrase ici les précédents avancees


                # Si cas particulier de la prise en passant du pion
                # A IMPLEMENTER ICI ET PAS APRES !!!!
                if self.pieceSelectionnee.poste == "pion":
                    if self.pionSeDeplaceEnDiagonale(self.casesAvancees):
                        if self.ilYAUnePieceEnDessousDeLuiDeCouleurDifferente(self.caseCliquee,self.pieceSelectionnee,plateau)[0]:
                            if self.caseCliquee.occupeePar == None:
                                # Alors prise en passant
                                laPieceEnDessous = self.ilYAUnePieceEnDessousDeLuiDeCouleurDifferente(self.caseCliquee,self.pieceSelectionnee,plateau)[1]
                                print(laPieceEnDessous)
                                print(laPieceEnDessous.poste,laPieceEnDessous.couleur,laPieceEnDessous.case.nom)
                                #
                                self.supprimerLaPiece(laPieceEnDessous,plateau)
                                #
                                laPieceEnDessous.case.occupeePar = None
                                #
                                #print(laPieceEnDessous.poste,laPieceEnDessous.couleur,laPieceEnDessous.case.nom)

                # Si il y a une piece sur la case de déplacement la supprimer
                if self.caseCliquee.occupeePar != None:
                    self.supprimerLaPiece(self.caseCliquee.occupeePar,plateau)
                    self.caseCliquee.occupeePar = None
                # Cas Particulier du pion avec piece en passant, supprimer le pion derrière lui

                # Attributs deplacementEffectueALInstantEtAvanceDeDeuxCase
                if self.pieceSelectionnee.poste == "pion":
                    #print('bonjourno')
                    #print(self.casesAvancees[0].coordonnees_quadrillage[0])
                    #print(self.casesAvancees[1].coordonnees_quadrillage[0])
                    #print(self.casesAvancees[0].coordonnees_quadrillage[0]-self.casesAvancees[1].coordonnees_quadrillage[0])
                    if abs(self.casesAvancees[0].coordonnees_quadrillage[0]-self.casesAvancees[1].coordonnees_quadrillage[0])==2:
                        self.pieceSelectionnee.AAvanceDeDeuxCase = True
                        #print(self.pieceSelectionnee.deplacementEffectueALInstantEtAvanceDeDeuxCase)
                        #print(self.pieceSelectionnee.poste,self.pieceSelectionnee.couleur)
                        #print('la veridad')
                    #else:
                    #    self.pieceSelectionnee.deplacementEffectueALInstantEtAvanceDeDeuxCase = False
                #else: # on remet le caractère en question de tout les pions (de la même couleur?) à False
                #    for piece in plateau.piecesEchiquier:
                #        if piece.poste == "pion":
                #            piece.deplacementEffectueALInstantEtAvanceDeDeuxCase = False

                #

                # Puis se déplacer # Cas Particulier du pion !

                self.pieceSelectionnee.deplacer(self.caseCliquee)
                #print("piece : ",)
                print("Déplacer en : ",self.caseCliquee.nom)
                plateau.casesDeplacee.append(self.caseCliquee)
                #print(plateau.casesDeplacee)
                #########################################################################################
                #if self.simulation == False:
                #for piece in plateau.piecesEchiquier:
                #    piece.vientDEtreJoue = False
                #self.pieceSelectionnee.vientDEtreJoue = True
                # Juste après le déplacement mise à jour de l'affichage d'echec
                self.affichageEchec(plateau)
                #
                for case in self.casesPossibles:
                    case.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True
                #
                for case in self.casesAvancees:
                    case.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":True,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True
                #
                if self.tourDuJoueur == "blanc":
                    self.tourDuJoueur = "noir"
                else:
                    self.tourDuJoueur = "blanc"
                #
                self.caseCliquee.occupeePar = self.pieceSelectionnee
                self.pieceSelectionnee = None
                self.caseCliquee = None
            else:
                if self.casesPossibles != None:
                    for case in self.casesPossibles:
                        case.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True
                # réaffichage des casesAvancees
                if self.casesAvancees != None:
                    for case in self.casesAvancees:
                        case.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":True,"passageSourisSurRond":False,"selectionDePiece":False} # etatAffichage ne doit contenir que un élément True
                #
                self.casesPossibles = None
                self.pieceSelectionnee = None
                self.caseCliquee = None

    def ilYAUnePieceEnDessousDeLuiDeCouleurDifferente(self,case,piece,plateau):
        if piece.couleur == "blanc":
            coord_quad = case.coordonnees_quadrillage
            case_en_dessous = (coord_quad[0]+1,coord_quad[1])
            if self.estDedans(case_en_dessous):
                for caseN in plateau.casesEchiquier:
                    if caseN.coordonnees_quadrillage == case_en_dessous:
                        if caseN.occupeePar != None:
                            if caseN.occupeePar.couleur == "noir":
                                return(True,caseN.occupeePar)
        else: # noir
            coord_quad = case.coordonnees_quadrillage
            case_en_dessous = (coord_quad[0]-1,coord_quad[1])
            if self.estDedans(case_en_dessous):
                for caseN in plateau.casesEchiquier:
                    if caseN.coordonnees_quadrillage == case_en_dessous:
                        if caseN.occupeePar != None:
                            if caseN.occupeePar.couleur == "blanc":
                                return(True,caseN.occupeePar)
        return(False,None)

    def estDedans(self,positionQuadrillage):
        if 1<=positionQuadrillage[0]<=8 and 1<=positionQuadrillage[1]<=8:
            #print('true!')
            return(True)
        #print('false!')
        return(False)

#<GestionnaireEvenement.GestionnaireEvenement object at 0x0AAAB290>
#(<Case.Case object at 0x0A98F050>, <Case.Case object at 0x0A98BAF0>)
    def pionSeDeplaceEnDiagonale(self,casesAvancees):
        # self.casesAvancees
        #print(casesAvancees0,casesAvancees1)
        casesAvanceesQuadrillage = (casesAvancees[0].coordonnees_quadrillage,casesAvancees[1].coordonnees_quadrillage)
        dx = abs(casesAvanceesQuadrillage[1][1]-casesAvanceesQuadrillage[0][1])
        dy = abs(casesAvanceesQuadrillage[1][0]-casesAvanceesQuadrillage[0][0])
        if dx == 1 and dy ==1:
            return(True)
        else:
            return(False)




    def caseDuRoiDuJoueur(self,plateau):
        if self.tourDuJoueur == "blanc":
            piecesEchiquierConsiderees = plateau.piecesBlancEchiquier
        else:
            piecesEchiquierConsiderees = plateau.piecesNoirEchiquier
        for piece in piecesEchiquierConsiderees:
            if piece.poste == "roi":
                return(piece.case)

    def joueurEstEchecEtPieceQuiCauseEchecAuRoi(self,plateau):
        if self.tourDuJoueur == "blanc":
            piecesAdversaire = plateau.piecesNoirEchiquier
        else:
            piecesAdversaire = plateau.piecesBlancEchiquier
        for piece in piecesAdversaire:
            #print('simulation')
            self.simulation = True
            caseOuLeDeplacementEstPossiblePourAdversaire = piece.caseOuLeDeplacementEstPossible(plateau,avecAffichage=False)#,GestionnaireEvenement)
            self.simulation = False
            for casePossiblePourAdversaire in caseOuLeDeplacementEstPossiblePourAdversaire:
                if casePossiblePourAdversaire == self.caseDuRoiDuJoueur(plateau):
                    return(True,piece)
        return(False,None)

    def affichageEchec(self,plateau):
        caseDuRoi = self.caseDuRoiDuJoueur(plateau)
        if self.joueurEstEchecEtPieceQuiCauseEchecAuRoi(plateau)[0]:
            caseDuRoi.etatAffichage = {"normal":False,"echec":True,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
        else:
            caseDuRoi.etatAffichage = {"normal":True,"echec":False,"rond":False,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}


    def verifieCasesPossiblesAvecEchecAuRoiPrisEnCompte(self,piece,casesPossibles,plateau):
        casesPossiblesApresVerificationEchec = []
        casesImpossibleApresVerification = []
        self.simulation = True
        for case in casesPossibles:
            copiePiece,copieCase,copiePlateau=self.copieProfondeDesArgumentsEtAssociation(piece,case,plateau)
            # Si il existe une piece adversaire sur la case ou on va se déplacer, la supprimer
            if copieCase.occupeePar != None:
                self.supprimerLaPiece(copieCase.occupeePar,copiePlateau)
            # Puis se déplacer
            copiePiece.deplacer(copieCase)
            if self.joueurEstEchecEtPieceQuiCauseEchecAuRoi(copiePlateau)[0]:
                casesImpossibleApresVerification.append(case)
            else:
                casesPossiblesApresVerificationEchec.append(case)
        self.simulation = False
        return(casesPossiblesApresVerificationEchec,casesImpossibleApresVerification)

    def copieProfondeDesArgumentsEtAssociation(self,pieceACopier,caseACopier,plateauACopier):
        copiePlateau = copy.deepcopy(plateauACopier)
        for case in copiePlateau.casesEchiquier:
            if case.nom == pieceACopier.case.nom:
                copiePiece = case.occupeePar
            if case.nom == caseACopier.nom:
                copieCase = case
        return(copiePiece,copieCase,copiePlateau)
