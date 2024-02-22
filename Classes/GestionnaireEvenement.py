from Classes.Plateau import *
import pygame
from pygame.locals import *
import copy
import tkinter as tk

class GestionnaireEvenement:

    def __init__(self):
        # Initialisation des variables de gestion des événements
        self.pieceSelectionnee = None  # Pièce actuellement sélectionnée
        self.caseCliquee = None  # Case cliquée par le joueur
        self.tourDuJoueur = "blanc"  # Couleur du joueur dont c'est le tour
        self.casesAvancees = None  # Cases associées à un déplacement en cours
        self.casesPossibles = None  # Cases où la pièce sélectionnée peut se déplacer
        self.deja_afficher_echec_et_mat = 0  # Indicateur pour savoir si le message d'échec et mat a déjà été affiché

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
            if self.est_echec_et_mat(FenetrePrincipale.plateau):
                self.deja_afficher_echec_et_mat += 1
                if self.deja_afficher_echec_et_mat == 3:
                    self.afficher_message_echec_et_mat()

    def afficher_message_echec_et_mat(self):
        # Création de la fenêtre
        fenetre = tk.Tk()
        titre = "Échec et mat"
        fenetre.title(titre)

        # Ajout du texte et du bouton dans la fenêtre
        texte = "Échec et mat. Victoire des {} !".format("blancs" if self.tourDuJoueur == "noir" else "noirs")
        tk.Label(fenetre, text=texte).pack()
        tk.Button(fenetre, text="OK", command=fenetre.destroy).pack()

        # Centrer la fenêtre au milieu de l'écran
        largeur_fenetre = 300  # Remplacez par la largeur souhaitée
        hauteur_fenetre = 50  # Remplacez par la hauteur souhaitée

        # Calcul des coordonnées pour centrer la fenêtre
        x = (fenetre.winfo_screenwidth() - largeur_fenetre) // 2
        y = (fenetre.winfo_screenheight() - hauteur_fenetre) // 2

        # Définir la géométrie de la fenêtre pour la centrer
        fenetre.geometry('{}x{}+{}+{}'.format(largeur_fenetre, hauteur_fenetre, x, y))

        # Lancement de la boucle principale
        fenetre.mainloop()

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

    def est_echec_et_mat(self, plateau):
        # On copie le plateau afin de pouvoir simuler des déplacements
        copiePlateau = copy.deepcopy(plateau)

        # Recherche du roi sur le plateau
        case_du_roi = self.caseDuRoiDuJoueur(copiePlateau)
        roi = case_du_roi.occupeePar
        est_echec, piece_qui_cause_echec = self.joueurEstEchecEtPieceQuiCauseEchecAuRoi(copiePlateau)
        
        # Si le roi n'est pas en échec, la partie n'est pas en échec et mat
        if not est_echec:
            return False
        
        # Obtient les mouvements possibles du roi avant de vérifier l'échec
        mouvement_du_roi_avant_verification_echec = roi.caseOuLeDeplacementEstPossible(copiePlateau, avecAffichage=False)
        # Vérifie les cases possibles avec l'échec au roi pris en compte
        casesPossiblesApresVerificationEchec = self.verifieCasesPossiblesAvecEchecAuRoiPrisEnCompte(piece=roi, casesPossibles=mouvement_du_roi_avant_verification_echec, plateau=copiePlateau)[0]
        
        # Vérifie s'il y a des mouvements possibles pour le roi
        mouvements_possibles_du_roi = casesPossiblesApresVerificationEchec != []
        
        # Si le roi peut se déplacer, la partie n'est pas en échec et mat
        if mouvements_possibles_du_roi:
            return False

        # Vérifie si une pièce du joueur peut capturer la menace
        capture_menace_possible = False
        pieces = copiePlateau.piecesBlancEchiquier if self.tourDuJoueur == "blanc" else copiePlateau.piecesNoirEchiquier

        # Exclut le roi des pièces à considérer
        for piece in pieces:
            if piece.poste == "roi":
                pieces.remove(piece)
                break
        
        # Vérifie si une pièce peut capturer la menace
        for piece in pieces:
            casePossible = piece.caseOuLeDeplacementEstPossible(copiePlateau, avecAffichage=False)
            if piece_qui_cause_echec.case in casePossible:
                capture_menace_possible = True
                break
        
        # Si le roi est en échec et aucune pièce ne peut capturer la menace, alors c'est un échec et mat
        if est_echec and not mouvements_possibles_du_roi and not capture_menace_possible:
            return True
        else:
            return False
