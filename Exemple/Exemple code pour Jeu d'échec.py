print('Bonjour')

#Importation des bibliothèques nécessaires
import pygame
import sys

#Initialisation de la bibliothèque Pygame
pygame.init()

#Création de la fenêtre principale
fenetre = pygame.display.set_mode((1066, 535))

################################################### Création des différentes zones/boutons ########################################################

#Création des zones des différents boutons de sauvegarde
#Sauvegarder et Continuer
rectangle = pygame.Rect((1005,256),(41,40))
surface = pygame.Surface(rectangle.size)

############################################## Importation des images #############################################################################

#Interface de l'écran principale
fond = pygame.image.load("fondf.png").convert_alpha()

####################################################### Boucle infinie ###############################################################################

#Boucle infinie
afficher = True #Variable qui continue la boucle si = 1, stoppe si = 0

while afficher:

    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        if event.type == QUIT:     #Si un de ces événements est de type QUIT
            afficher = False      #On arrête la boucle

############################################## Chargement des affichages écrit ############################################################################################################

    #Chargement de l'affichage du nombre de ressources et diverses variable numérique
    font=pygame.font.Font(None, 50) # chiffre taille de la police #je met cette ligne que une fois vu que toute mes polices sont pareils
    ARB = font.render(str(RB),1,(0,0,0)) #les 3 chiffre = la couleur
    Afinfh = font.render("1",1,(0,0,0))



####################################### Blit de tout l'écran à chaque tour de boucle ##############################################################
    fenetre.blit(fond, (0,0))
    fenetre.blit(ARB, (144, 35)) #Affichage du bois
    #Rafraichissement
    pygame.display.flip()

########################################### Conséquence du clique de souris gauche ####################################################################

    #Conséquence du clique de souris gauche
    if event.type == MOUSEBUTTONDOWN: #Si clique souris
        if event.button == 1: #Si clique gauche
            ccs=0 #Compteur de clique souris remis à zéro pour chaque tour de boucle
                  #Le but est de ne pas améliorer le batiment au maximun en 1 clique si le joueur à toute les ressources nécessaire
                  #Cela permet une plus grande liberter pour le joueur

    #Conséquence du clique de souris gauche
    if event.type == MOUSEBUTTONUP: #Si clique souris #après relâchement de la touche
        if event.button == 1 and ccs==0: #Si clique gauche et si compteur clique souris est égale à 0

############################################## Dans le menu si clique sur fermeture ##########################################################################################################################

            if padi==2: #si menu
                if zfib.collidepoint(event.pos): #si zone de fermeture #zfib est une zone de clique
                    continuer=0 #Alors le programme se ferme

    #Rafraîchissement de l'écran
    pygame.display.flip()

pygame.display.flip()
pygame.quit()
sys.exit()
