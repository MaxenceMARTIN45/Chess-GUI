# Importe la classe Piece du module Classes.Piece
from Classes.Piece import *

# Définit la classe Cavalier qui hérite de la classe Piece
class Cavalier(Piece):

    # Initialise un objet Cavalier avec une case, une couleur et un poste
    def __init__(self, case, couleur, poste):
        super().__init__(case, couleur, poste)
        # Définit les déplacements possibles pour un cavalier sous forme de tuples (déplacement en x, déplacement en y)
        self.deplacementPossible = [(1, 2), (2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1), (-1, 2), (-2, 1)]

    # Méthode pour obtenir les cases où le déplacement est possible
    def caseOuLeDeplacementEstPossible(self, plateau, avecAffichage):
        caseActuelle = self.case.coordonnees_quadrillage
        casePossible = []
        
        # Parcourt les déplacements possibles
        for deplacement in self.deplacementPossible:
            newCasePossible = (caseActuelle[0] + deplacement[0], caseActuelle[1] + deplacement[1])
            
            # Vérifie si la nouvelle case est dans le plateau
            if self.estDansPlateau(newCasePossible):
                
                # Parcourt toutes les cases de l'échiquier
                for case in plateau.casesEchiquier:
                    
                    # Vérifie si la nouvelle case correspond à une case de l'échiquier
                    if newCasePossible == case.coordonnees_quadrillage:
                        laCaseRecherchee = case
                        
                        # Vérifie si la case est occupée par une pièce adverse
                        if laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur != self.couleur:
                            casePossible.append(laCaseRecherchee)
                            if avecAffichage:
                                laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": False,
                                                                    "targetPiece": True, "apresDeplacement": False,
                                                                    "passageSourisSurRond": False, "selectionDePiece": False}
                        
                        # Vérifie si la case est occupée par une pièce de la même couleur (ne fait rien dans ce cas)
                        elif laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur == self.couleur:
                            pass
                        
                        # Si la case est libre, ajoute la case comme possible
                        else:
                            casePossible.append(laCaseRecherchee)
                            if avecAffichage:
                                laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": True,
                                                                    "targetPiece": False, "apresDeplacement": False,
                                                                    "passageSourisSurRond": False, "selectionDePiece": False}
                        break
        return casePossible

    # Méthode pour vérifier si une case est dans le plateau (valeurs de x et y entre 1 et 8 inclus)
    def estDansPlateau(self, newCasePossible):
        return 1 <= newCasePossible[0] <= 8 and 1 <= newCasePossible[1] <= 8
