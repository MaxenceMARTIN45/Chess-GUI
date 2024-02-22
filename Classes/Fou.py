# Importing the Piece class from the specified module
from Classes.Piece import *

# Definition of the Fou class, which is a subclass of Piece
class Fou(Piece):

    # Constructor method to initialize the Fou object
    def __init__(self, case, couleur, poste):
        super().__init__(case, couleur, poste)
        # Possible trajectories for the Fou piece
        self.trajectoirePossible = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

    # Method to determine possible destination squares for the Fou piece
    def caseOuLeDeplacementEstPossible(self, plateau, avecAffichage):
        caseActuelle = self.case.coordonnees_quadrillage
        casePossible = []
        sortirDeLaBoucleDIterationDeTrajectoire = False

        # Iterate over possible trajectories
        for trajectoire in self.trajectoirePossible:
            for i in range(1, 8):
                # Calculate the new potential destination square
                newCasePossible = (caseActuelle[0] + i * trajectoire[0], caseActuelle[1] + i * trajectoire[1])

                # Check if the new square is within the chessboard
                if self.estDansPlateau(newCasePossible):
                    # Iterate over all squares on the chessboard
                    for case in plateau.casesEchiquier:
                        if newCasePossible == case.coordonnees_quadrillage:
                            laCaseRecherchee = case
                            # Check if the square is occupied by an opponent's piece
                            if laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur != self.couleur:
                                sortirDeLaBoucleDIterationDeTrajectoire = True
                                casePossible.append(laCaseRecherchee)
                                # Update the display state if required
                                if avecAffichage:
                                    laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": False, "targetPiece": True, "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}
                            # Check if the square is occupied by a piece of the same color
                            elif laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur == self.couleur:
                                sortirDeLaBoucleDIterationDeTrajectoire = True
                            else:
                                casePossible.append(laCaseRecherchee)
                                # Update the display state if required
                                if avecAffichage:
                                    laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": True, "targetPiece": False, "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}
                            break

                    # Exit the trajectory iteration if a valid move is found
                    if sortirDeLaBoucleDIterationDeTrajectoire:
                        sortirDeLaBoucleDIterationDeTrajectoire = False
                        break

        # Return the list of possible destination squares
        return casePossible

    # Method to check if a square is within the chessboard boundaries
    def estDansPlateau(self, newCasePossible):
        return 1 <= newCasePossible[0] <= 8 and 1 <= newCasePossible[1] <= 8
