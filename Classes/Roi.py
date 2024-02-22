from Classes.Piece import *

class Roi(Piece):

    def __init__(self, case, couleur, poste):
        super().__init__(case, couleur, poste)
        self.numeroDucoup = 0
        self.deplacementPossible = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    def caseOuLeDeplacementEstPossible(self, plateau, avecAffichage):
        # Obtient les coordonnées actuelles du roi sur le quadrillage
        caseActuelle = self.case.coordonnees_quadrillage
        # Liste pour stocker les cases où le déplacement est possible
        casePossible = []

        # Parcours de tous les déplacements possibles
        for deplacement in self.deplacementPossible:
            # Calcul des nouvelles coordonnées possibles après le déplacement
            newCasePossible = (caseActuelle[0] + deplacement[0], caseActuelle[1] + deplacement[1])

            # Vérifie si la nouvelle case est dans le plateau
            if self.estDansPlateau(newCasePossible):
                # Parcours de toutes les cases du plateau
                for case in plateau.casesEchiquier:
                    # Vérifie si la case actuelle correspond à la nouvelle case possible
                    if newCasePossible == case.coordonnees_quadrillage:
                        laCaseRecherchee = case
                        # Vérifie si la case est occupée par une pièce de couleur opposée
                        if laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur != self.couleur:
                            casePossible.append(laCaseRecherchee)
                            if avecAffichage:
                                laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": False,
                                                                    "targetPiece": True, "apresDeplacement": False,
                                                                    "passageSourisSurRond": False, "selectionDePiece": False}
                        # Vérifie si la case est occupée par une pièce de la même couleur
                        elif laCaseRecherchee.occupeePar is not None and laCaseRecherchee.occupeePar.couleur == self.couleur:
                            pass  # Ne fait rien dans ce cas
                        else:
                            casePossible.append(laCaseRecherchee)
                            if avecAffichage:
                                laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": True,
                                                                    "targetPiece": False, "apresDeplacement": False,
                                                                    "passageSourisSurRond": False, "selectionDePiece": False}
                        break  # Sort du boucle dès qu'une case est trouvée

        return casePossible

    def estDansPlateau(self, newCasePossible):
        # Vérifie si les coordonnées sont dans les limites du plateau (entre 1 et 8 inclus)
        return 1 <= newCasePossible[0] <= 8 and 1 <= newCasePossible[1] <= 8
