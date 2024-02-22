# Importation des classes

# from Classes.Case import *
# from Classes.Cavalier import *
# from Classes.FenetrePrincipale import *
# from Classes.Fou import *
# from Classes.GestionnaireEvenement import *
# from Classes.Piece import *
# from Classes.Pion import *
# from Classes.Plateau import *
# from Classes.Reine import *
# from Classes.Roi import *
# from Classes.Tour import *

import Classes.FenetrePrincipale as fn

def main():
    # fenetrePrincipale=Classes.FenetrePrincipale.FenetrePrincipale()
    fenetrePrincipale = fn.FenetrePrincipale()
    # fenetrePrincipale=c.FenetrePrincipale()
    fenetrePrincipale.afficher()

if __name__ == "__main__":
    main()
else:
    print("Une erreur s'est produite")
