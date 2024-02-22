# Importe la classe Piece depuis le module Classes.Piece
from Classes.Piece import *

# Définit la classe Reine qui hérite de la classe Piece
class Reine(Piece):

    # Initialise une instance de la classe Reine avec une position, une couleur et un poste spécifiques
    def __init__(self, case, couleur, poste):
        # Appelle le constructeur de la classe mère (Piece) avec les paramètres appropriés
        super().__init__(case, couleur, poste)
        # Définit les trajectoires possibles pour la reine
        self.trajectoirePossible = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

    # Méthode pour obtenir les cases où le déplacement est possible
    def caseOuLeDeplacementEstPossible(self, plateau, avecAffichage):
        # Récupère les coordonnées de la case actuelle
        caseActuelle = self.case.coordonnees_quadrillage
        # Initialise une liste pour stocker les cases possibles
        casePossible = []
        # Variable pour sortir de la boucle d'itération de trajectoire
        sortirDeLaBoucleDIterationDeTrajectoire = False

        # Parcourt les trajectoires possibles
        for trajectoire in self.trajectoirePossible:
            # Parcourt les positions le long de la trajectoire jusqu'à 7 cases maximum
            for i in range(1, 8):
                # Calcule la nouvelle position possible
                newCasePossible = (caseActuelle[0] + i * trajectoire[0], caseActuelle[1] + i * trajectoire[1])

                # Vérifie si la nouvelle position est dans le plateau
                if self.estDansPlateau(newCasePossible):
                    # Parcourt les cases du plateau pour trouver la case correspondante
                    for case in plateau.casesEchiquier:
                        if newCasePossible == case.coordonnees_quadrillage:
                            # La case recherchée est trouvée
                            laCaseRecherchee = case

                            # Vérifie si la case est occupée par une pièce de couleur opposée
                            if laCaseRecherchee.occupeePar != None and laCaseRecherchee.occupeePar.couleur != self.couleur:
                                sortirDeLaBoucleDIterationDeTrajectoire = True
                                casePossible.append(laCaseRecherchee)
                                if avecAffichage:
                                    # Modifie l'état d'affichage de la case en conséquence
                                    laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": False, "targetPiece": True, "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}
                            # Vérifie si la case est occupée par une pièce de la même couleur
                            elif laCaseRecherchee.occupeePar != None and laCaseRecherchee.occupeePar.couleur == self.couleur:
                                sortirDeLaBoucleDIterationDeTrajectoire = True
                            else:
                                # La case est vide
                                casePossible.append(laCaseRecherchee)
                                if avecAffichage:
                                    # Modifie l'état d'affichage de la case en conséquence
                                    laCaseRecherchee.etatAffichage = {"normal": False, "echec": False, "rond": True, "targetPiece": False, "apresDeplacement": False, "passageSourisSurRond": False, "selectionDePiece": False}
                            break

                    # Sort de la boucle si une pièce a été trouvée
                    if sortirDeLaBoucleDIterationDeTrajectoire:
                        sortirDeLaBoucleDIterationDeTrajectoire = False
                        break

        # Retourne la liste des cases possibles
        return casePossible

    # Méthode pour vérifier si une nouvelle position est dans le plateau (entre 1 et 8 inclus)
    def estDansPlateau(self, newCasePossible):
        return 1 <= newCasePossible[0] <= 8 and 1 <= newCasePossible[1] <= 8
