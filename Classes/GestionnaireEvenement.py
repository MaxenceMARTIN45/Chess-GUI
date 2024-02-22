from Classes.Plateau import *
import pygame
from pygame.locals import *
import copy

class GestionnaireEvenement:

    def __init__(self):
        # Initialisation des variables de gestion des événements
        self.pieceSelectionnee = None  # Pièce actuellement sélectionnée
        self.caseCliquee = None  # Case cliquée par le joueur
        self.tourDuJoueur = "blanc"  # Couleur du joueur dont c'est le tour
        self.casesAvancees = None  # Cases associées à un déplacement en cours
        self.casesPossibles = None  # Cases où la pièce sélectionnée peut se déplacer

    def gererEvenements(self, FenetrePrincipale):
        # Gestion des événements principaux du jeu
        for event in pygame.event.get():
            self.quitterSiInstruction(event, FenetrePrincipale)
            self.affichageEchec(FenetrePrincipale.plateau)
            self.enregistreLaCaseCliquee(event, FenetrePrincipale.plateau)
            self.regarderSiCorrespondAUnePieceASelectionner(FenetrePrincipale.plateau)
            self.regarderSiCorrespondAUnePieceAAttaquer(FenetrePrincipale.plateau)
            for piece in FenetrePrincipale.plateau.piecesEchiquier:
                if piece.poste == "pion":
                    piece.promotion(FenetrePrincipale.plateau)

    def quitterSiInstruction(self, event, FenetrePrincipale):
        # Vérifie si l'événement est de type QUIT (fermeture de fenêtre)
        if event.type == QUIT:
            FenetrePrincipale.afficher = False

    def enregistreLaCaseCliquee(self, event, plateau):
        # Enregistre la case cliquée lorsqu'un bouton de la souris est pressé
        if event.type == MOUSEBUTTONDOWN:
            for case in plateau.casesEchiquier:
                if pygame.Rect(case.rect_origine_pixel, case.rect_dimension).collidepoint(event.pos):
                    print("Tu as cliqué sur la case : ", case.nom)
                    self.caseCliquee = case

    def caseCliqueeCorrespondAUnePiece(self):
        # Vérifie si la case cliquée est occupée par une pièce
        return self.caseCliquee.occupeePar is not None

    def pasEncoreDePieceSelectionnee(self):
        # Vérifie s'il n'y a pas encore de pièce sélectionnée
        return self.pieceSelectionnee is None

    def bonneCouleur(self):
        # Vérifie si la couleur de la pièce sélectionnée correspond à la couleur du joueur en cours
        return self.caseCliquee.occupeePar.couleur == self.tourDuJoueur

    def regarderSiCorrespondAUnePieceASelectionner(self, plateau):
        # Logique pour sélectionner une pièce
        if (
            self.caseCliquee is not None
            and self.caseCliqueeCorrespondAUnePiece()
            and self.pasEncoreDePieceSelectionnee()
            and self.bonneCouleur()
        ):
            self.pieceSelectionnee = self.caseCliquee.occupeePar
            # Définir l'état d'affichage de la case sélectionnée
            self.pieceSelectionnee.case.etatAffichage = {
                "normal": False,
                "echec": False,
                "rond": False,
                "targetPiece": False,
                "apresDeplacement": False,
                "passageSourisSurRond": False,
                "selectionDePiece": True,
            }
            # Obtenir les cases où la pièce sélectionnée peut se déplacer
            self.casesPossibles = self.pieceSelectionnee.caseOuLeDeplacementEstPossible(
                plateau, avecAffichage=True
            )
            # Vérifier si ces déplacements ne mettent pas le joueur en échec
            casesPossiblesApresVerificationEchec, casesImpossibleApresVerification = self.verifieCasesPossiblesAvecEchecAuRoiPrisEnCompte(
                self.pieceSelectionnee, self.casesPossibles, plateau
            )
            # Mettre à jour l'état d'affichage des cases en conséquence
            for case in casesImpossibleApresVerification:
                case.etatAffichage = {
                    "normal": True,
                    "echec": False,
                    "rond": False,
                    "targetPiece": False,
                    "apresDeplacement": False,
                    "passageSourisSurRond": False,
                    "selectionDePiece": False,
                }
            self.casesPossibles = casesPossiblesApresVerificationEchec
            self.caseCliquee = None

    def caseCliqueeAppartientACasesPossibles(self):
        # Vérifie si la case cliquée fait partie des cases où la pièce peut se déplacer
        return self.caseCliquee in self.casesPossibles

    def indice(self, element, liste):
        # Retourne l'indice de la première occurrence de l'élément dans la liste
        return next((i for i, x in enumerate(liste) if x == element), None)

    def supprimerLaPiece(self, piece, plateau):
        # Supprime la pièce du plateau et de la liste correspondante (blanche ou noire)
        pieceASupprimer = piece
        indiDeLaPieceASupprimer = self.indice(pieceASupprimer, plateau.piecesEchiquier)
        plateau.piecesEchiquier.pop(indiDeLaPieceASupprimer)
        if pieceASupprimer.couleur == "blanc":
            indiDeLaPieceASupprimer = self.indice(
                pieceASupprimer, plateau.piecesBlancEchiquier
            )
            plateau.piecesBlancEchiquier.pop(indiDeLaPieceASupprimer)
        else:
            indiDeLaPieceASupprimer = self.indice(
                pieceASupprimer, plateau.piecesNoirEchiquier
            )
            plateau.piecesNoirEchiquier.pop(indiDeLaPieceASupprimer)

    def regarderSiCorrespondAUnePieceAAttaquer(self, plateau):
        # Logique pour attaquer une pièce
        if self.caseCliquee is not None and self.pieceSelectionnee is not None:
            self.pieceSelectionnee.case.etatAffichage = {
                "normal": True,
                "echec": False,
                "rond": False,
                "targetPiece": False,
                "apresDeplacement": False,
                "passageSourisSurRond": False,
                "selectionDePiece": False,
            }
            if (
                self.casesPossibles is not None
                and self.caseCliqueeAppartientACasesPossibles()
            ):
                if self.casesAvancees is not None:
                    for case in self.casesAvancees:
                        case.etatAffichage = {
                            "normal": True,
                            "echec": False,
                            "rond": False,
                            "targetPiece": False,
                            "apresDeplacement": False,
                            "passageSourisSurRond": False,
                            "selectionDePiece": False,
                        }
                self.casesAvancees = (self.pieceSelectionnee.case, self.caseCliquee)
                if self.pieceSelectionnee.poste == "pion":
                    if self.pionSeDeplaceEnDiagonale(self.casesAvancees):
                        if self.ilYAUnePieceEnDessousDeLuiDeCouleurDifferente(
                            self.caseCliquee, self.pieceSelectionnee, plateau
                        )[0]:
                            if self.caseCliquee.occupeePar is None:
                                laPieceEnDessous = self.ilYAUnePieceEnDessousDeLuiDeCouleurDifferente(
                                    self.caseCliquee, self.pieceSelectionnee, plateau
                                )[1]
                                self.supprimerLaPiece(laPieceEnDessous, plateau)
                                laPieceEnDessous.case.occupeePar = None
                if self.caseCliquee.occupeePar is not None:
                    self.supprimerLaPiece(self.caseCliquee.occupeePar, plateau)
                    self.caseCliquee.occupeePar = None
                if self.pieceSelectionnee.poste == "pion":
                    if (
                        abs(
                            self.casesAvancees[0].coordonnees_quadrillage[0]
                            - self.casesAvancees[1].coordonnees_quadrillage[0]
                        )
                        == 2
                    ):
                        self.pieceSelectionnee.AAvanceDeDeuxCase = True
                self.pieceSelectionnee.deplacer(self.caseCliquee)
                print("Déplacer en : ", self.caseCliquee.nom)
                plateau.casesDeplacee.append(self.caseCliquee)
                self.affichageEchec(plateau)
                for case in self.casesPossibles:
                    case.etatAffichage = {
                        "normal": True,
                        "echec": False,
                        "rond": False,
                        "targetPiece": False,
                        "apresDeplacement": False,
                        "passageSourisSurRond": False,
                        "selectionDePiece": False,
                    }
                for case in self.casesAvancees:
                    case.etatAffichage = {
                        "normal": False,
                        "echec": False,
                        "rond": False,
                        "targetPiece": False,
                        "apresDeplacement": True,
                        "passageSourisSurRond": False,
                        "selectionDePiece": False,
                    }
                if self.tourDuJoueur == "blanc":
                    self.tourDuJoueur = "noir"
                else:
                    self.tourDuJoueur = "blanc"
                self.caseCliquee.occupeePar = self.pieceSelectionnee
                self.pieceSelectionnee = None
                self.caseCliquee = None
            else:
                if self.casesPossibles is not None:
                    for case in self.casesPossibles:
                        case.etatAffichage = {
                            "normal": True,
                            "echec": False,
                            "rond": False,
                            "targetPiece": False,
                            "apresDeplacement": False,
                            "passageSourisSurRond": False,
                            "selectionDePiece": False,
                        }
                if self.casesAvancees is not None:
                    for case in self.casesAvancees:
                        case.etatAffichage = {
                            "normal": False,
                            "echec": False,
                            "rond": False,
                            "targetPiece": False,
                            "apresDeplacement": True,
                            "passageSourisSurRond": False,
                            "selectionDePiece": False,
                        }
                self.casesPossibles = None
                self.pieceSelectionnee = None
                self.caseCliquee = None

    def ilYAUnePieceEnDessousDeLuiDeCouleurDifferente(self, case, piece, plateau):
        # Vérifie s'il y a une pièce en dessous de la pièce actuelle de couleur différente
        if piece.couleur == "blanc":
            coord_quad = case.coordonnees_quadrillage
            case_en_dessous = (coord_quad[0] + 1, coord_quad[1])
            if self.estDedans(case_en_dessous):
                for caseN in plateau.casesEchiquier:
                    if caseN.coordonnees_quadrillage == case_en_dessous:
                        if caseN.occupeePar is not None:
                            if caseN.occupeePar.couleur == "noir":
                                return True, caseN.occupeePar
        else:
            coord_quad = case.coordonnees_quadrillage
            case_en_dessous = (coord_quad[0] - 1, coord_quad[1])
            if self.estDedans(case_en_dessous):
                for caseN in plateau.casesEchiquier:
                    if caseN.coordonnees_quadrillage == case_en_dessous:
                        if caseN.occupeePar is not None:
                            if caseN.occupeePar.couleur == "blanc":
                                return True, caseN.occupeePar
        return False, None

    def estDedans(self, positionQuadrillage):
        # Vérifie si une position donnée est à l'intérieur du quadrillage de l'échiquier
        return 1 <= positionQuadrillage[0] <= 8 and 1 <= positionQuadrillage[1] <= 8

    def pionSeDeplaceEnDiagonale(self, casesAvancees):
        # Vérifie si un pion se déplace en diagonale
        casesAvanceesQuadrillage = (
            casesAvancees[0].coordonnees_quadrillage,
            casesAvancees[1].coordonnees_quadrillage,
        )
        dx = abs(casesAvanceesQuadrillage[1][1] - casesAvanceesQuadrillage[0][1])
        dy = abs(casesAvanceesQuadrillage[1][0] - casesAvanceesQuadrillage[0][0])
        return dx == 1 and dy == 1

    def caseDuRoiDuJoueur(self, plateau):
        # Retourne la case du roi du joueur actuel
        if self.tourDuJoueur == "blanc":
            piecesEchiquierConsiderees = plateau.piecesBlancEchiquier
        else:
            piecesEchiquierConsiderees = plateau.piecesNoirEchiquier
        for piece in piecesEchiquierConsiderees:
            if piece.poste == "roi":
                return piece.case

    def joueurEstEchecEtPieceQuiCauseEchecAuRoi(self, plateau):
        # Vérifie si le joueur actuel est en échec et retourne la pièce qui cause l'échec
        if self.tourDuJoueur == "blanc":
            piecesAdversaire = plateau.piecesNoirEchiquier
        else:
            piecesAdversaire = plateau.piecesBlancEchiquier
        for piece in piecesAdversaire:
            self.simulation = True
            caseOuLeDeplacementEstPossiblePourAdversaire = piece.caseOuLeDeplacementEstPossible(
                plateau, avecAffichage=False
            )
            self.simulation = False
            for casePossiblePourAdversaire in caseOuLeDeplacementEstPossiblePourAdversaire:
                if casePossiblePourAdversaire == self.caseDuRoiDuJoueur(plateau):
                    return True, piece
        return False, None

    def affichageEchec(self, plateau):
        # Gère l'affichage de l'échec sur la case du roi du joueur actuel
        caseDuRoi = self.caseDuRoiDuJoueur(plateau)
        if self.joueurEstEchecEtPieceQuiCauseEchecAuRoi(plateau)[0]:
            caseDuRoi.etatAffichage = {
                "normal": False,
                "echec": True,
                "rond": False,
                "targetPiece": False,
                "apresDeplacement": False,
                "passageSourisSurRond": False,
                "selectionDePiece": False,
            }
        else:
            caseDuRoi.etatAffichage = {
                "normal": True,
                "echec": False,
                "rond": False,
                "targetPiece": False,
                "apresDeplacement": False,
                "passageSourisSurRond": False,
                "selectionDePiece": False,
            }

    def verifieCasesPossiblesAvecEchecAuRoiPrisEnCompte(
        self, piece, casesPossibles, plateau
    ):
        # Vérifie si les cases possibles ne mettent pas le roi en échec
        casesPossiblesApresVerificationEchec = []
        casesImpossibleApresVerification = []
        self.simulation = True
        for case in casesPossibles:
            copiePiece, copieCase, copiePlateau = self.copieProfondeDesArgumentsEtAssociation(
                piece, case, plateau
            )
            if copieCase.occupeePar is not None:
                self.supprimerLaPiece(copieCase.occupeePar, copiePlateau)
            copiePiece.deplacer(copieCase)
            if self.joueurEstEchecEtPieceQuiCauseEchecAuRoi(copiePlateau)[0]:
                casesImpossibleApresVerification.append(case)
            else:
                casesPossiblesApresVerificationEchec.append(case)
        self.simulation = False
        return casesPossiblesApresVerificationEchec, casesImpossibleApresVerification

    def copieProfondeDesArgumentsEtAssociation(
        self, pieceACopier, caseACopier, plateauACopier
    ):
        # Effectue une copie profonde des arguments et les associe aux nouvelles instances
        copiePlateau = copy.deepcopy(plateauACopier)
        for case in copiePlateau.casesEchiquier:
            if case.nom == pieceACopier.case.nom:
                copiePiece = case.occupeePar
            if case.nom == caseACopier.nom:
                copieCase = case
        return copiePiece, copieCase, copiePlateau
