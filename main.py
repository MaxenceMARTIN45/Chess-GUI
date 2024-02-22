# Importe la classe FenetrePrincipale depuis le module Classes.FenetrePrincipale
import Classes.FenetrePrincipale as fn

# Fonction principale du programme
def main():
    # Crée une instance de la classe FenetrePrincipale
    fenetrePrincipale = fn.FenetrePrincipale()
    
    # Affiche la fenêtre principale
    fenetrePrincipale.afficher()

# Vérifie si le script est exécuté en tant que programme principal
if __name__ == "__main__":
    # Appelle la fonction main() si le script est exécuté directement
    main()
else:
    # Affiche un message d'erreur si le script est importé en tant que module
    print("Une erreur s'est produite")
