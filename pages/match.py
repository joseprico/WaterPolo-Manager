from joueur import Joueur
from ballon import Ballon
import random as r
import math
import config
import pygame
from typing import Tuple
import copy


WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 30 * config.longueur_terrain  # Largeur
SCREEN_HEIGHT = 30 * config.largeur_terrain  # Hauteur
# Facteur d'échelle pour transformer les mètres en pixels
SCALE_X = SCREEN_WIDTH / 30  # Terrain de 30m → largeur de la fenêtre
SCALE_Y = SCREEN_HEIGHT / 20  # Terrain de 20m → hauteur de la fenêtre


class Match :
    def __init__(self, equipe_A, equipe_B, JoueursA,JoueursB,):
        self.domicile = equipe_A
        self.exterieur = equipe_B
        self.joueurs_dom = JoueursA
        self.joueurs_ext = JoueursB
        self.chrono = 400
        self.ballon = Ballon((0,0))
        self.possesion = 0     # vaut 0 si personne, 1 si équie à dom, et -1 si équipe ext
        self.receveur = None
        self.emetteur = None
        self.passe_en_cours = False

    def lancement_jeu(self) :
        self.placement_initial()
        self.lancement_balle()


        pygame.init()

        # Dimensions de la fenêtre (proportionnelles au terrain FINA 30m x 20m)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulation de Water-Polo")

        # Boucle de jeu
        running = True
        clock = pygame.time.Clock()
        self.afficher_terrain(screen)


        while running:
            # Gestion des événements (fermeture de la fenêtre)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for joueur in self.joueurs_dom :
                self.action(joueur, self.joueurs_dom)
            for joueur in self.joueurs_ext :
                self.action(joueur,self.joueurs_ext)
            self.afficher_terrain(screen)
            #self.update_chrono_attaque()

            clock.tick(config.ticks*config.vitesse_du_jeu)

        pygame.quit()

    def afficher_terrain(self,screen):


        """Affiche le terrain, les lignes, les joueurs et le ballon"""
        screen.fill(BLUE)  # Fond bleu pour l'eau

        # Dessiner les cages
        cage_width = 2 * SCALE_X
        cage_height = config.taille_but * SCALE_Y
        pygame.draw.rect(screen, WHITE, (0, (SCREEN_HEIGHT - cage_height) // 2, cage_width, cage_height))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - cage_width, (SCREEN_HEIGHT - cage_height) // 2, cage_width, cage_height))

        pygame.draw.line(screen, RED, (2 * SCALE_X, 0), (2 * SCALE_X, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, RED, ((config.longueur_terrain - 2) * SCALE_X, 0), ((config.longueur_terrain - 2) * SCALE_X, SCREEN_HEIGHT), 2)

        pygame.draw.line(screen, YELLOW, (5 * SCALE_X, 0), (5 * SCALE_X, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, YELLOW, ((config.longueur_terrain - 5) * SCALE_X, 0), ((config.longueur_terrain - 5) * SCALE_X, SCREEN_HEIGHT), 2)

        pygame.draw.line(screen, GREEN, (6 * SCALE_X, 0), (6 * SCALE_X, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, GREEN, ((config.longueur_terrain - 6) * SCALE_X, 0), ((config.longueur_terrain - 6) * SCALE_X, SCREEN_HEIGHT), 2)

        pygame.draw.line(screen, WHITE, (config.longueur_terrain/2 * SCALE_X, 0), (config.longueur_terrain/2 * SCALE_X, SCREEN_HEIGHT), 2)

        # Dessiner les joueurs
        for joueur in self.joueurs_dom:
            x, y = joueur.position
            pygame.draw.circle(screen, RED, (int(x * SCALE_X), int(y * SCALE_Y)), 7)  # Rouge = Équipe domicile

        for joueur in self.joueurs_ext:
            x, y = joueur.position
            pygame.draw.circle(screen, YELLOW, (int(x * SCALE_X), int(y * SCALE_Y)), 7)  # Jaune = Équipe extérieure

        # Dessiner le ballon
        bx, by = self.ballon.position
        pygame.draw.circle(screen, WHITE, (int(bx * SCALE_X), int(by * SCALE_Y)), 3)

        pygame.display.flip()

    def placement_initial(self) :

        for joueur in self.joueurs_dom :
            joueur.position = Match.position_aleatoire(config.positions_dom[joueur.poste])
        for joueur in self.joueurs_ext :
            joueur.position = Match.position_aleatoire(config.positions_ext[joueur.poste])

    def lancement_balle(self):
        self.ballon.position =  Match.position_aleatoire((config.longueur_terrain//2, 1),0.2)

    def position_aleatoire(position: Tuple[float, float], facteur = config.fact_alea_pos) -> Tuple[float, float]:
        dx,dy = r.uniform(-1,1),+ r.uniform(-1,1)
        distance = (dx**2 + dy**2)**0.5 / facteur
        dx,dy = dx / distance, dy/distance
        return position[0] + dx, position[1]+dy

    def distance_ballon(self, joueur : Joueur) -> float:

        distance = ((self.ballon.position[0] - joueur.position[0])**2 + (self.ballon.position[1] - joueur.position[1])**2)**0.5
        return distance

    def recup_ballon(self, joueur : Joueur) :
        if (self.distance_ballon(joueur) < 0.25 or joueur.a_le_ballon == True) and (joueur!= self.emetteur):
            joueur.a_le_ballon = True
            if joueur in self.joueurs_dom :
                self.possesion = 1
            else :
                self.possesion = -1
            self.ballon.position = joueur.position

    def action(self, joueur : Joueur, joueurs : list[Joueur]) :
        if self.possesion == 0 :
            self.recup_ballon(joueur)
            if self.passe_en_cours :
                self.passe_en_cours = self.passe(self.emetteur, self.receveur)
                if self.passe_en_cours == False :
                    self.receveur = None
                    self.emetteur = None

            if min([self.distance_ballon(j) for j in joueurs]) == self.distance_ballon(joueur) :
                joueur.mouvement_vers(self.ballon.position)
            else :
                joueur.mouvement_vers((self.ballon.position[0],joueur.position[1]))
        if self.possesion == 1 or self.possesion == -1 :
            choix = self.choix_joueur(joueur)
            if choix == 1 :
                self.emetteur = joueur
                self.passe_en_cours = self.passe(self.emetteur,self.receveur)
                self.possesion = 0
            else :
                #joueur.mouvement_vers((13*-self.possesion+15,joueur.position[1]))
                cible = self.cible_attaque(joueur)
                if joueur.poste != "gardien" :
                    joueur.mouvement_vers(cible)
                if joueur.a_le_ballon :
                    self.ballon.position = joueur.position



    def cible_attaque(self,joueur):
        position_arrondie = (round(joueur.position[0]),round(joueur.position[1]))

        if joueur.poste == "pointe" :
            if position_arrondie != (config.formations["pointe"][0] * -self.possesion + 15, config.formations["pointe"][1]) :
                return (config.formations["pointe"][0] * -self.possesion + 15, config.formations["pointe"][1])
            else :
                return Match.position_aleatoire((config.formations["pointe"][0] * -self.possesion + 15, config.formations["pointe"][1]),6)
            return (config.formations["pointe"][0] * -self.possesion + 15,config.formations["pointe"][1])
        elif joueur.poste in config.formations:
            if joueur in self.joueurs_dom :
                joueurs = copy.deepcopy(self.joueurs_dom)
            else :
                joueurs = copy.deepcopy(self.joueurs_ext)
            formation = copy.deepcopy(config.formations)
            for cible_joueur in formation :

                if cible_joueur != "pointe" :
                    joueur_plus_proche = min(joueurs, key=lambda joueur: joueur.distance_au_point(config.formations[cible_joueur][0]* -self.possesion + 15,config.formations[cible_joueur][1]))
                    if joueur.position == joueur_plus_proche.position :
                        if position_arrondie != (config.formations[cible_joueur][0] * -self.possesion + 15, config.formations[cible_joueur][1]) :
                            return (config.formations[cible_joueur][0] * -self.possesion + 15, config.formations[cible_joueur][1])
                        else :
                            return Match.position_aleatoire((config.formations[cible_joueur][0] * -self.possesion + 15, config.formations[cible_joueur][1]),6)
                    else :
                        #del formation[cible_joueur]
                        joueurs.remove(joueur_plus_proche)
            else :
                return (self.ballon.position[0],7)



    def choix_joueur(self, joueur: Joueur):
        """Détermine l'action du joueur en possession du ballon (passe, tir ou avancer)."""
        if not joueur.a_le_ballon:
            return 0

        # Récupérer les coéquipiers et défenseurs
        equipe = self.joueurs_dom if joueur in self.joueurs_dom else self.joueurs_ext
        adversaires = self.joueurs_ext if joueur in self.joueurs_dom else self.joueurs_dom

        # Vérifier les options de passe
        receveurs_potentiels = []
        for coequipier in equipe:
            if coequipier.poste != "gardien" :
                if coequipier == joueur or coequipier.a_le_ballon:
                    continue

                distance_coequipier = joueur.distance_au_joueur(coequipier)
                defenseur_plus_proche = min(adversaires, key=lambda d: d.distance_au_joueur(coequipier))
                distance_defenseur = defenseur_plus_proche.distance_au_joueur(coequipier)

                if distance_defenseur > 0.7 and coequipier.mieux_placé(joueur) and distance_coequipier<13:
                    if coequipier.poste == "pointe":
                        if 0 <= coequipier.position[0] <= 5:
                            receveurs_potentiels.append((coequipier, distance_coequipier, distance_defenseur))
                    else :
                        receveurs_potentiels.append((coequipier, distance_coequipier, distance_defenseur))

        if receveurs_potentiels:
            receveurs_potentiels.sort(key=lambda x: (x[1]))   #et proximité
            self.receveur = receveurs_potentiels[0][0]
            print(f" {joueur.nom} passe à {self.receveur.nom} !")
            return 1
        else :
            return 0

    def position_gardien_adverse(self, joueur):
        if joueur in self.joueurs_dom:
            for j in self.joueurs_ext:
                if j.poste == "gardien":
                    return j.position[0]
        elif joueur in self.joueurs_ext:
            for j in self.joueurs_dom:
                if j.poste == "gardien":
                    return j.position
        else :
            return config.longueur_terrain // 2  # Retourne None si aucun gardien n'est trouvé

    def passe(self, emetteur, recepteur) :
        if emetteur.a_le_ballon :
            emetteur.a_le_ballon = False


        dx, dy =  (recepteur.position[0]-self.ballon.position[0]), (recepteur.position[1]-self.ballon.position[1])
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 0.75 :
            self.ballon.position = recepteur.position
            recepteur.a_le_ballon = True
            return False
        else :
            dx, dy = dx / distance, dy / distance  # Normalisation
            self.ballon.position = (self.ballon.position[0] + dx * 0.01, self.ballon.position[1] + dy * 0.01)  # Mise à jour de la position
            return True

    """def update_chrono_attaque(self):
        Met à jour le chrono d'attaque et force un changement de possession si 0
        if self.chrono > 0:
            self.chrono -= 1
        else:
            print("⏳ Temps d'attaque écoulé ! Changement de possession.")
            self.transferer_possession()

    def transferer_possession(self):
        Donne le ballon au défenseur le plus proche de l'attaquant
        joueur_actuel = next((j for j in self.joueurs_dom + self.joueurs_ext if j.a_le_ballon), None)

        if joueur_actuel:
            joueur_actuel.a_le_ballon = False  # L'attaquant perd le ballon

            # Trouver le défenseur le plus proche
            if joueur_actuel in self.joueurs_dom:
                joueurs_defenseurs = self.joueurs_ext
            else:
                joueurs_defenseurs = self.joueurs_dom

            defenseur_proche = min(joueurs_defenseurs, key=lambda d: d.distance_au_joueur(joueur_actuel))

            # Nouveau porteur du ballon
            defenseur_proche.a_le_ballon = True
            self.ballon = defenseur_proche.position
            self.chrono = 30  # Réinitialisation du chrono pour la nouvelle équipe
            print(f"🎯 {defenseur_proche.nom} récupère le ballon et la contre-attaque commence !")"""



