# -*- coding: utf-8 -*-
import pygame
import time
import os
from pygame.locals import *
from pygame.sprite import collide_rect
pygame.init()
pygame.font.init()


#Chargement des fichiers
sourceFileDir=os.path.dirname(os.path.abspath(__file__))
os.chdir(sourceFileDir)

#ecran
pygame.display.set_caption("StickMan Fithter Ultimate")
fenetre = pygame.display.set_mode((1280, 720))

#importation des fichiers

FondMenu=pygame.image.load("assets/MenuBackGround.png")
BoutonMenu=pygame.image.load("assets/BoutonJouer.png")
BackgroundChargement=pygame.image.load("assets/EcranChargementBackGround.png")
FondArene=pygame.image.load("assets/FondArene.png")
Compte1=pygame.image.load("assets/Compte1.png")
Compte2=pygame.image.load("assets/Compte2.png")
Compte3=pygame.image.load("assets/Compte3.png")
PersoBleu=pygame.image.load("assets/PersoBleu.png")
PersoRouge=pygame.image.load("assets/PersoRouge.png")
platforme=pygame.image.load("assets/platforme.png")
BoutonControle=pygame.image.load("assets/BoutonControle.png")
BoutonCroix=pygame.image.load("assets/BoutonCroix.png")
EcranCredits=pygame.image.load("assets/EcranCredit.png")
BoutonCredits=pygame.image.load("assets/BoutonCredits.png")
BoutonPause=pygame.image.load("assets/BoutonPause.png")
FondPause=pygame.image.load("assets/FondPause.png")
fondJoueurBleuGagne=pygame.image.load("assets/EcranBleuGagne.png")
fondJoueurRougeGagne=pygame.image.load("assets/EcranRougeGagne.png")
FondChoixCarte=pygame.image.load("assets/FondChoixDeCarte.png")
BoutonCarte1=pygame.image.load("assets/BoutonCarte1.png")
BoutonCarte2=pygame.image.load("assets/BoutonCarte2.png")
FondArene2=pygame.image.load("assets/FondArene2.png")
PlatformeArene2=pygame.image.load("assets/PlatformeArene2.png")
FondBob=pygame.image.load("assets/FondBob.png")
BoutonBob=pygame.image.load("assets/BoutonBob.png")
PlatformeBob=pygame.image.load("assets/PlatformeBob.png")

#gestion du temps

clock = pygame.time.Clock()
temps = pygame.time.get_ticks()

#liste

CompteurImage=[Compte3,Compte2,Compte1]

#variable

lancer=False
menu=True
menuPasser=False
jeuxCommence=False
chargementPasser=False
PartiCommence=False
compte=0
nombreSaut=0
fondactu=FondArene
attaqueJ1=False
attaqueJ2=False
client=True
CommentJouer=False
Credits=False
chronoGame=False
pause=False
joueur1Gagne=False
joueur2Gagne=False
ChoixCarte=False
CarteActu=FondArene
PlatformeChoisie=platforme
x=313
y=435


#Rect
rectFondActu=fondactu.get_rect()
rectBouton = BoutonMenu.get_rect()
rectBouton.move_ip(400,300)
rectBoutonControle = BoutonControle.get_rect()
rectBoutonControle.move_ip(0,632)
rectBoutonCroix = BoutonCroix.get_rect()
rectBoutonCroix.move_ip(1192,0)
rectBoutonCredits = BoutonCredits.get_rect()
rectBoutonCredits.move_ip(1192,0)
rectBoutonPause = BoutonPause.get_rect()
rectBoutonPause.move_ip(1192,0)
rectBoutonCarte1 = BoutonCarte1.get_rect()
rectBoutonCarte1.move_ip(210,263)
rectBoutonCarte2 = BoutonCarte2.get_rect()
rectBoutonCarte2.move_ip(410,263)
rectBoutonBob = BoutonBob.get_rect()
rectBoutonBob.move_ip(610,263)

#objets

class Personnage(pygame.sprite.Sprite):
    def __init__(self, persoImage,x,y):
        super().__init__
        self.vie=100
        self.vieRestante=3
        self.vitesse=6
        self.attaque=5
        self.persoDroite=persoImage
        self.rectDroite=self.persoDroite.get_rect()
        self.rectDroite.x=x
        self.rectDroite.y=y
        self.saut=0
        self.saut_montee=0
        self.saut_descente=3
        self.sauterVrai=False


    def deplacementDroite(self):
        self.rectDroite.x += self.vitesse
    def deplacementGauche(self):
        self.rectDroite.x -= self.vitesse
    def sauter(self):
        if self.sauterVrai==True:
            if self.saut_montee>=15:
               self.saut_descente -=3
               self.saut=self.saut_descente
            if self.saut_descente<0:
                self.saut_montee=0
                self.saut_descente=1
                self.sauterVrai = False
            else:
                self.saut_montee+=3
                self.saut=self.saut_montee
        self.rectDroite.y= self.rectDroite.y - (3* (self.saut / 2))


class platformeCombat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rectPlatforme=platforme.get_rect()
        self.rectPlatforme.x=x
        self.rectPlatforme.y=y
    def afficher(self):
        fenetre.blit(platforme, self.rectPlatforme)


class Jeux:
    def __init__(self):
        self.Joueur1=Personnage(PersoBleu,360,100)
        self.Joueur2=Personnage(PersoRouge,900,100)
        self.platformeCombat=platformeCombat()
        self.gravite= (0,6)
        self.resitance=(0,0)
        self.gravite2= (0,6)
        self.resitance2=(0,0)
        self.Police = pygame.font.SysFont('Comic Sans MS', 50)  
        self.chronoStart=False
        self.attaqueVrai=False
        self.repultionn=0
        self.repultion_montee=0
        self.repultion_descente=3
        self.graviteJeux()
        self.chrono()
        self.MortDansLeVide()
        self.j1Gagne()
        self.j2Gagne()
        self.afiicheNombreDeVieRestante1()
        self.afiicheNombreDeVieRestante2()
        self.collisonPlatforme= False
        self.testAppuie={}
    def graviteJeux(self):
        self.Joueur1.rectDroite.y += self.gravite[1]+ self.resitance[1]
        self.Joueur2.rectDroite.y += self.gravite2[1]+ self.resitance2[1]
    def MortDansLeVide(self):
        if not rectFondActu.colliderect(self.Joueur1.rectDroite):
            self.Joueur1.rectDroite.x=360
            self.Joueur1.rectDroite.y=100
            self.Joueur1.vieRestante-=1
            self.chronoStart=True
        if not rectFondActu.colliderect(self.Joueur2.rectDroite):
            self.Joueur2.rectDroite.x=900
            self.Joueur2.rectDroite.y=100
            self.Joueur2.vieRestante-=1
            self.chronoStart=True
    def repultion(self,rectPlayerAttaqued,rectPlayerAttack):
        if self.attaqueVrai==True and rectPlayerAttack.x >= rectPlayerAttaqued.x:
            rectPlayerAttaqued.x-=60
            rectPlayerAttaqued.y-=60
        if self.attaqueVrai==True and rectPlayerAttack.x <= rectPlayerAttaqued.x:
            rectPlayerAttaqued.x+=60
            rectPlayerAttaqued.y-=60       
    def chrono(self):
        if self.chronoStart==True:
            for i in range(4):
                fenetre.blit(CompteurImage[i-1], (400,250))
                pygame.display.update()
                clock.tick(1)
                if i==2:
                    self.chronoStart=False
    def j1Gagne(self):
        if self.Joueur2.vieRestante== 0:
            fenetre.blit(fondJoueurBleuGagne, (0,0))
    def j2Gagne(self):
        if self.Joueur1.vieRestante== 0:
            fenetre.blit(fondJoueurRougeGagne, (0,0))
    def afiicheNombreDeVieRestante1(self):
        VieJ1Texte = self.Police.render(str(self.Joueur1.vieRestante), False, (0, 0, 0))
        fenetre.blit(VieJ1Texte,(40,10))
    def afiicheNombreDeVieRestante2(self):
        VieJ1Texte = self.Police.render(str(self.Joueur2.vieRestante), False, (0, 0, 0))
        fenetre.blit(VieJ1Texte,(1207,10))


jeux= Jeux()



#boucle jeux

while client==True:
    fenetre.blit(FondMenu, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client = False
        if event.type == MOUSEBUTTONDOWN:
            if rectBouton.collidepoint(pygame.mouse.get_pos()):
                client = False
                ChoixCarte = True
        if event.type == MOUSEBUTTONDOWN:
            if rectBoutonControle.collidepoint(pygame.mouse.get_pos()):
                client=False
                CommentJouer=True
        if event.type == MOUSEBUTTONDOWN:
            if rectBoutonCredits.collidepoint(pygame.mouse.get_pos()):
                client=False
                Credits=True
                
    fenetre.blit(BoutonMenu, rectBouton)
    fenetre.blit(BoutonControle, rectBoutonControle)
    fenetre.blit(BoutonCredits, rectBoutonCredits)
    pygame.display.flip()

    while CommentJouer==True:
        fenetre.blit(BackgroundChargement, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                CommentJouer = False
            if event.type == MOUSEBUTTONDOWN:
                if rectBoutonCroix.collidepoint(pygame.mouse.get_pos()):
                    CommentJouer=False
                    client=True
        fenetre.blit(BoutonCroix, rectBoutonCroix)
        pygame.display.flip()

    while Credits==True:
        fenetre.blit(EcranCredits, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                CommentJouer = False
            if event.type == MOUSEBUTTONDOWN:
                if rectBoutonCroix.collidepoint(pygame.mouse.get_pos()):
                    Credits=False
                    client=True
        fenetre.blit(BoutonCroix, rectBoutonCroix)
        pygame.display.flip()

    while ChoixCarte==True:
        fenetre.blit(FondChoixCarte, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ChoixCarte = False
            if event.type == MOUSEBUTTONDOWN:
                if rectBoutonCarte1.collidepoint(pygame.mouse.get_pos()):
                    ChoixCarte=False
                    chronoGame=True
            if event.type == MOUSEBUTTONDOWN:
                if rectBoutonCarte2.collidepoint(pygame.mouse.get_pos()):
                    fondactu=FondArene2
                    platforme=PlatformeArene2
                    ChoixCarte=False
                    chronoGame=True
            if event.type == MOUSEBUTTONDOWN:
                if rectBoutonBob.collidepoint(pygame.mouse.get_pos()):
                    fondactu=FondBob
                    platforme=PlatformeBob
                    ChoixCarte=False
                    chronoGame=True
        fenetre.blit(BoutonCarte1, rectBoutonCarte1)
        fenetre.blit(BoutonCarte2, rectBoutonCarte2)
        fenetre.blit(BoutonBob, rectBoutonBob)
        pygame.display.flip()


    while chronoGame==True:
        fenetre.blit(fondactu, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chronoGame = False
        for i in range(4):
            fenetre.blit(CompteurImage[i-1], (400,250))
            pygame.display.update()
            clock.tick(1)
            if i==2:
                lancer=True
                chronoGame=False

    while lancer==True:
        fenetre.blit(fondactu, (0,0))
        jeux.platformeCombat.afficher()  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lancer = False
            if event.type == pygame.KEYDOWN:
                jeux.testAppuie[event.key]=  True
            elif event.type==KEYUP:
                jeux.testAppuie[event.key]=  False
            if event.type == KEYDOWN:
                if event.key==K_z:
                    jeux.Joueur1.sauterVrai=True
                    nombreSaut+=1
                if event.key==K_UP:
                    jeux.Joueur2.sauterVrai=True
                    nombreSaut+=1
            if event.type == pygame.KEYDOWN:
                if event.key==K_SPACE:
                    jeux.attaqueVrai=True
                    attaqueJ1=True
                if event.key==K_RSHIFT:
                    jeux.attaqueVrai=True
                    attaqueJ2=True
            
        if jeux.platformeCombat.rectPlatforme.colliderect(jeux.Joueur1.rectDroite):
            jeux.resitance=(0,-6)
            nombreSaut=0
            jeux.collisonPlatforme=True
        else:
            jeux.resitance=(0,0)

        if jeux.platformeCombat.rectPlatforme.colliderect(jeux.Joueur2.rectDroite):
            jeux.resitance2=(0,-6)
            nombreSaut=0
            jeux.collisonPlatforme=True
        else:
            jeux.resitance2=(0,0)

        if jeux.Joueur1.sauterVrai and jeux.collisonPlatforme == True:
            if nombreSaut < 1:
                jeux.Joueur1.sauter()

        if jeux.Joueur2.sauterVrai and jeux.collisonPlatforme == True:
            if nombreSaut < 1:
                jeux.Joueur2.sauter()
        if jeux.attaqueVrai==True and jeux.Joueur1.rectDroite.colliderect(jeux.Joueur2.rectDroite) and attaqueJ1==True:
            jeux.repultion(jeux.Joueur2.rectDroite,jeux.Joueur1.rectDroite)
            pygame.display.update()
            jeux.attaqueVrai=False
            attaqueJ1=False

        if jeux.attaqueVrai==True and jeux.Joueur2.rectDroite.colliderect(jeux.Joueur1.rectDroite) and attaqueJ2==True:
            jeux.repultion(jeux.Joueur1.rectDroite,jeux.Joueur2.rectDroite)
            pygame.display.update()
            jeux.attaqueVrai=False
            attaqueJ1=True
        

        if jeux.testAppuie.get(pygame.K_d):
            jeux.Joueur1.deplacementDroite()
        if jeux.testAppuie.get(pygame.K_q):
            jeux.Joueur1.deplacementGauche()
        if jeux.testAppuie.get(pygame.K_RIGHT):
            jeux.Joueur2.deplacementDroite()
        if jeux.testAppuie.get(pygame.K_LEFT):
            jeux.Joueur2.deplacementGauche()
        fenetre.blit(jeux.Joueur1.persoDroite, jeux.Joueur1.rectDroite)
        fenetre.blit(jeux.Joueur2.persoDroite, jeux.Joueur2.rectDroite)
        jeux.graviteJeux()
        jeux.MortDansLeVide()
        jeux.chrono()
        jeux.j1Gagne()
        jeux.j2Gagne()
        
        jeux.afiicheNombreDeVieRestante1()
        jeux.afiicheNombreDeVieRestante2()
        pygame.display.flip()
        clock.tick(60)

pygame.quit()