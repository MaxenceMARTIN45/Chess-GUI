# Importe la classe Piece du module Classes.Piece
from Classes.Piece import *

# Définit une classe Tour qui hérite de la classe Piece
class Tour(Piece):

    # Initialise la Tour avec une case, une couleur et un poste
    def __init__(self, case, couleur, poste):
        super().__init__(case, couleur, poste)
        # Définit les trajectoires possibles pour la Tour (haut, bas, gauche, droite)
        self.trajectoirePossible = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Méthode pour déterminer les cases où le déplacement est possible
    def caseOuLeDeplacementEstPossible(self, plateau, avecAffichage):
        caseActuelle = self.case.coordonnees_quadrillage
        casePossible = []
        sortirDeLaBoucleDIterationDeTrajectoire = False
        
        # Parcours des trajectoires possibles
        for trajectoire in self.trajectoirePossible:
            for i in range(1, 8):
                newCasePossible = (caseActuelle[0] + i * trajectoire[0], caseActuelle[1] + i * trajectoire[1])
                
                # Vérifie si la nouvelle case est dans le plateau
                if self.estDansPlateau(newCasePossible):
                    for case in plateau.casesEchiquier:
                        if newCasePossible == case.coordonnees_quadrillage:
                            laCaseRecherchee = case
                            
                            # Vérifie si la case est occupée par une pièce ennemie
                            if laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur != self.couleur:
                                sortirDeLaBoucleDIterationDeTrajectoire = True
                                casePossible.append(laCaseRecherchee)
                                
                                # Modifie l'état d'affichage si nécessaire
                                if avecAffichage:
                                    laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": False,
                                                                       "targetPiece": True, "apresDeplacement": False,
                                                                       "passageSourisSurRond": False,
                                                                       "selectionDePiece": False}
                            # Vérifie si la case est occupée par une pièce de la même couleur
                            elif laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur == self.couleur:
                                sortirDeLaBoucleDIterationDeTrajectoire = True
                            else:
                                casePossible.append(laCaseRecherchee)
                                
                                # Modifie l'état d'affichage si nécessaire
                                if avecAffichage:
                                    laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": True,
                                                                       "targetPiece": False, "apresDeplacement": False,
                                                                       "passageSourisSurRond": False,
                                                                       "selectionDePiece": False}
                            break
                    if sortirDeLaBoucleDIterationDeTrajectoire:
                        sortirDeLaBoucleDIterationDeTrajectoire = False
                        break
        return casePossible

    # Méthode pour vérifier si une case est dans le plateau
    def estDansPlateau(self, newCasePossible):
        return 1 <= newCasePossible[0] <= 8 and 1 <= newCasePossible[1] <= 8
