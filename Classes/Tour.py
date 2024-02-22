# Importation des classes

from Classes.Piece import *

# Importation pour Pygame

# import pygame
# from pygame.locals import *
# import sys

# Classe Tour

class Tour(Piece):

    def __init__(self,case,couleur,poste):
        # Attributs
        super().__init__(case,couleur,poste)
        self.trajectoirePossible = [(1,0),(-1,0),(0,1),(0,-1)]


    def caseOuLeDeplacementEstPossible(self,plateau,avecAffichage):#,gestionnaireEvenement):
        caseActuelle = self.case.coordonnees_quadrillage
        casePossible = []
        sortirDeLaBoucleDIterationDeTrajectoire = False
        for trajectoire in self.trajectoirePossible:
            for i in range(1,8):
                newCasePossible = (caseActuelle[0]+i*trajectoire[0],caseActuelle[1]+i*trajectoire[1])
                if self.estDansPlateau(newCasePossible):
                    # Trouver la case associée
                    for case in plateau.casesEchiquier:
                        if newCasePossible == case.coordonnees_quadrillage:
                            laCaseRecherchee = case
                            # Regarder si une piece est sur cette case
                            if laCaseRecherchee.occupeePar!=None and laCaseRecherchee.occupeePar.couleur!=self.couleur:
                                # ie est occupee par un adversaire
                                sortirDeLaBoucleDIterationDeTrajectoire=True
                                casePossible.append(laCaseRecherchee)
                                if avecAffichage == True:
                                    laCaseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":False,"targetPiece":True,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
                            elif laCaseRecherchee.occupeePar!=None and laCaseRecherchee.occupeePar.couleur==self.couleur:
                                # ie est occupee par un camarade
                                sortirDeLaBoucleDIterationDeTrajectoire=True
                            else:
                                # ie est occupee par personne
                                casePossible.append(laCaseRecherchee)
                                if avecAffichage == True:
                                    laCaseRecherchee.etatAffichage = {"normal":False,"echec":False,"rond":True,"targetPiece":False,"apresDeplacement":False,"passageSourisSurRond":False,"selectionDePiece":False}
                            break # pas utile de continuer a itérer puisqu'on a trouver la case
                    if sortirDeLaBoucleDIterationDeTrajectoire==True:
                        sortirDeLaBoucleDIterationDeTrajectoire=False
                        break
        return(casePossible)


    def estDansPlateau(self,newCasePossible):
        if 1<=newCasePossible[0]<=8 and 1<=newCasePossible[1]<=8:
            return(True)
        else:
            return(False)



#p=Tour("b","bn","b")
#print(p)