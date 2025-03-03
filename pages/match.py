from joueur import Joueur
from ballon import Ballon
import random as r
import math
import config
import pygame
from typing import Tuple
import copy
import time


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
        self.chrono = 30*config.ticks
        self.ballon = Ballon((0,0))
        self.possesion = 0     # vaut 0 si personne, 1 si équie à dom, et -1 si équipe ext
        self.receveur = None
        self.emetteur = None
        self.passe_en_cours = False
        self.delai_passe = 0
        self.possession_precedente =0
        self.tir_en_cours = False
        self.score_dom = 0
        self.score_ext = 0

    def lancement_jeu(self) :
        self.placement_initial()
        self.lancement_balle()


        pygame.init()

        # Dimensions de la fenêtre (proportionnelles au terrain FINA 30m x 20m)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulation de Water-Polo")

        # Boucle de jeu
        running = True
        clock = pygame.time.Clock()
        self.afficher_terrain(self.screen)


        while running:
            # Gestion des événements (fermeture de la fenêtre)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for joueur in self.joueurs_dom :
                self.action(joueur, self.joueurs_dom)
            for joueur in self.joueurs_ext :
                self.action(joueur,self.joueurs_ext)
            self.update_chrono_attaque()
            self.afficher_terrain(self.screen)


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
        if self.possesion != self.possession_precedente and self.passe_en_cours == False:
            self.reinitialiser_affectations()
            self.possession_precedente = self.possesion
            self.chrono = 30*config.ticks
        if self.possesion == 1:
            if joueur in self.joueurs_dom :
                choix = self.choix_joueur(joueur)
                if choix == 2 :
                    chance = r.uniform(0, 1)
                    difficulte = self.tir(joueur)
                    if chance > 1 - difficulte:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_but_adverse(joueur))
                            self.afficher_terrain(self.screen)
                            #time.sleep(0.1)
                        self.score_dom+=1
                        print(f"But de {joueur.nom}. Score : {self.domicile} {self.score_dom} - {self.exterieur} {self.score_ext}")
                        joueur.a_le_ballon = False
                        self.tir_en_cours = False
                        self.engagement()
                        self.reinitialiser_affectations()
                        time.sleep(2)
                        for joueur in self.joueurs_ext :
                            if joueur.poste == "défenseur pointe" :
                                self.ballon.position = (joueur.position[0],joueur.position[1])
                                joueur.a_le_ballon = True
                        self.possesion = -1

                    else:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_gardien_adverse(joueur))
                            self.afficher_terrain(self.screen)
                        joueur.a_le_ballon = False
                        self.chrono =30*config.ticks
                        self.transferer_possession()
                if choix == 1 :
                    self.delai_passe = 30
                    self.emetteur = joueur
                    self.passe_en_cours = self.passe(self.emetteur,self.receveur)
                    self.possesion = 0
                else :
                    if joueur.poste != "gardien" :
                        cible = self.cible_attaque(joueur)
                        joueur.mouvement_vers(cible)
                        if joueur.a_le_ballon :
                            self.ballon.position = joueur.position
            else :
                if joueur.poste !="gardien":
                    cible = self.defense(joueur)
                    joueur.mouvement_vers(cible)
        elif self.possesion == -1 :
            if joueur in self.joueurs_ext :
                choix = self.choix_joueur(joueur)
                if choix == 2 :
                    chance = r.uniform(0, 1)
                    difficulte = self.tir(joueur)
                    if chance > difficulte:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_but_adverse(joueur))
                            self.afficher_terrain(self.screen)
                            #time.sleep(0.1)
                        self.score_ext+=1
                        print(f"But de {joueur.nom}. Score : {self.domicile} {self.score_dom} - {self.exterieur} {self.score_ext}")
                        joueur.a_le_ballon = False
                        self.engagement()
                        self.reinitialiser_affectations()
                        time.sleep(2)
                        for joueur in self.joueurs_dom :
                            if joueur.poste == "défenseur pointe" :
                                self.ballon.position = (joueur.position[0],joueur.position[1])
                                joueur.a_le_ballon = True
                        self.possesion = 1

                    else:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_gardien_adverse(joueur))
                            self.afficher_terrain(self.screen)
                        joueur.a_le_ballon = False
                        self.chrono =30*config.ticks
                        self.transferer_possession()


                if choix == 1 :
                    self.delai_passe = 30
                    self.emetteur = joueur
                    self.passe_en_cours = self.passe(self.emetteur,self.receveur)
                    self.possesion = 0
                else :
                    if joueur.poste != "gardien" :
                        cible = self.cible_attaque(joueur)
                        joueur.mouvement_vers(cible)
                        if joueur.a_le_ballon :
                            self.ballon.position = joueur.position
            else :
                if joueur.poste !="gardien":
                    cible = self.defense(joueur)
                    joueur.mouvement_vers(cible)

    def engagement(self):
        for joueur in self.joueurs_dom :
            joueur.position = (config.positions_dom[joueur.poste][0]-13,config.positions_dom[joueur.poste][1])
        for joueur in self.joueurs_ext :
            joueur.position = (config.positions_ext[joueur.poste][0]+13,config.positions_dom[joueur.poste][1])

    def cible_attaque(self, joueur):
        position_arrondie = (round(joueur.position[0]), round(joueur.position[1]))
        if joueur in self.joueurs_dom :
            equipe = self.joueurs_dom
        else :
            equipe = self.joueurs_ext
        equipe_sans_gardien = [j for j in equipe if j.poste != "gardien"]
        if not hasattr(self, 'affectations') or len(self.affectations) == 0:
            self.reinitialiser_affectations()

        for player in equipe_sans_gardien :
            if player.poste == "pointe":
                self.affectations[player] = (config.formations["pointe"][0]* - self.possesion +15, config.formations["pointe"][1])


        for poste, position in self.position_disponible.items():
            position = (position[0] * -self.possesion + 15,position[1])
            joueurs_non_places = [j for j in equipe_sans_gardien if j not in self.affectations]
            if not joueurs_non_places:
                break

            joueur_plus_proche = min(joueurs_non_places, key=lambda j: j.distance_au_point(position[0],position[1]))
            self.affectations[joueur_plus_proche] = position
        if joueur in self.affectations:
            if position_arrondie != (self.affectations[joueur][0],self.affectations[joueur][1]) :
                return (self.affectations[joueur][0],self.affectations[joueur][1])
            elif (joueur.poste != "pointe") and (joueur.distance_au_point(self.ballon.position[0],self.ballon.position[1])<10):
                return Match.position_aleatoire((self.affectations[joueur][0],self.affectations[joueur][1]),2)



        return joueur.position  # Si aucune position trouvée, le joueur reste en place

    def reinitialiser_affectations(self):
        self.position_disponible = {poste: pos for poste, pos in config.formations.items() if poste != "pointe"}
        self.affectations = {}

    def choix_joueur(self, joueur: Joueur):
        """Détermine l'action du joueur en possession du ballon (passe, tir ou avancer)."""
        if not joueur.a_le_ballon:
            return 0

        # Récupérer les coéquipiers et défenseurs
        equipe = self.joueurs_dom if joueur in self.joueurs_dom else self.joueurs_ext
        adversaires = self.joueurs_ext if joueur in self.joueurs_dom else self.joueurs_dom
        """if joueur.poste != "gardien" :
            tir = self.resultat_tir(joueur)
            if tir == True :
                return 2"""
        # Vérifier les options de passe
        if self.delai_passe == 0 :
            receveurs_potentiels = []
            for coequipier in equipe:
                if coequipier.poste != "gardien" :
                    if coequipier == joueur or coequipier.a_le_ballon:
                        continue

                    distance_coequipier = joueur.distance_au_joueur(coequipier)
                    defenseur_plus_proche = min(adversaires, key=lambda d: d.distance_au_joueur(coequipier))
                    distance_defenseur = defenseur_plus_proche.distance_au_joueur(coequipier)

                    if (distance_defenseur > 1 and coequipier.mieux_placé(joueur)) or (distance_defenseur >3 and abs(coequipier.position[0] - config.longueur_terrain) < abs(joueur.position[0] - config.longueur_terrain)) :
                        if coequipier.poste == "pointe":
                            if (self.possesion == 1 and 25 <= coequipier.position[0] <= 28) or (self.possesion == -1 and 2 <= coequipier.position[0] <= 5) :
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
        else :
            self.delai_passe-=1
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
            self.ballon.position = (self.ballon.position[0] + dx * 0.02, self.ballon.position[1] + dy * 0.02)  # Mise à jour de la position
            return True

    def update_chrono_attaque(self):

        if self.chrono > 0:
            self.chrono -= 1
        else:
            print("⏳ Temps d'attaque écoulé ! Changement de possession.")
            self.transferer_possession()

    def transferer_possession(self):
        joueur_actuel = next((j for j in self.joueurs_dom + self.joueurs_ext if j.a_le_ballon), None)
        if self.possesion == 1 :
            self.possesion = -1
        elif self.possesion == -1 :
            self.possesion = 1

        if joueur_actuel:
            joueur_actuel.a_le_ballon = False  # L'attaquant perd le ballon

            # Trouver le défenseur le plus proche
            if joueur_actuel in self.joueurs_dom:
                joueurs_defenseurs = self.joueurs_ext
            else:
                joueurs_defenseurs = self.joueurs_dom

            defenseur_proche = min(joueurs_defenseurs, key=lambda d: d.distance_au_joueur(joueur_actuel))

            # Nouveau porteur du ballon
            defenseur_proche.mouvement_vers(self.ballon.position)
            self.recup_ballon(defenseur_proche)
            self.ballon.position = defenseur_proche.position
            defenseur_proche.a_le_ballon = True
            self.chrono = 30*config.ticks  # Réinitialisation du chrono pour la nouvelle équipe
            print(f"🎯 {defenseur_proche.nom} récupère le ballon et la contre-attaque commence !")

    def defense(self, joueur):
        equipe = self.joueurs_dom if joueur in self.joueurs_dom else self.joueurs_ext
        adversaires = self.joueurs_ext if joueur in self.joueurs_dom else self.joueurs_dom
        but_dom = (config.longueur_terrain, config.largeur_terrain/2)
        but_ext = (0, config.largeur_terrain/2)
        but = but_dom if joueur in self.joueurs_dom else but_ext
        # Dictionnaire pour stocker les adversaires déjà attribués
        if not hasattr(self, 'marquages'):
            self.marquages = {}

        # Cas spécifique pour le défenseur pointe
        if joueur.poste == "défenseur pointe":
            for j in adversaires:
                if j.poste == "pointe":
                    self.marquages[joueur] = j  # Assignation unique
                    return self.placer_entre(j.position,but,0.90)

        # Filtrer les adversaires déjà pris
        adversaires_disponibles = [j for j in adversaires if j.poste != "gardien" and j.poste != "pointe"and j not in self.marquages.values()]

        # Si plus d'adversaires disponibles, on prend le plus proche
        if adversaires_disponibles:
            adversaire = min(adversaires_disponibles, key=lambda j: joueur.distance_au_joueur(j))
            self.marquages[joueur] = adversaire  # On assigne cet adversaire au joueur
            return self.placer_entre(adversaire.position,but,0.85)

        # Si tous les adversaires sont déjà assignés, on ne change rien
        if joueur in self.marquages:
            return self.placer_entre(self.marquages[joueur].position,but,0.85)

        return (0,0)  # Si aucun adversaire n'est disponible

    def placer_entre(self, adversaire_pos, but_pos, facteur):

        x = but_pos[0] + facteur * (adversaire_pos[0] - but_pos[0])
        y = but_pos[1] + facteur * (adversaire_pos[1] - but_pos[1])
        return (x, y)

    def tir(self, joueur):
        but_dom = (config.longueur_terrain, config.largeur_terrain/2)
        but_ext = (0, config.largeur_terrain/2)
        if joueur in self.joueurs_dom :
            for j in self.joueurs_ext :
                if j.poste=="gardien" :
                    gardien_adverse = j
        else :
            for j in self.joueurs_dom :
                if j.poste=="gardien" :
                    gardien_adverse = j

        but = but_ext if joueur in self.joueurs_dom else but_dom

        distance_au_but = joueur.distance_au_point(but[0],but[1])
        angle_but = abs(math.atan2(but[1] - joueur.position[1], but[0] - joueur.position[0]))
        max_distance = config.longueur_terrain
        max_angle = math.pi / 2

        facteur_puissance = max(0.5, 1 - joueur.puissance / 100)
        facteur_precision = max(0.5, 1 - joueur.precision / 100)
        impact_gardien = gardien_adverse.arret / 100

        difficulte_distance = (distance_au_but / max_distance) * facteur_puissance
        difficulte_angle = (1 - (angle_but / max_angle)) * facteur_precision

        difficulte = (0.4 * difficulte_distance) + (0.3 * difficulte_angle) + (0.3 * impact_gardien)
        difficulte = min(1, max(0, difficulte))

        return difficulte

    def resultat_tir(self,joueur):
        difficulte_tir = self.tir(joueur)
        if difficulte_tir <= 0.5:
            return True
        return False

    def deplacement_ballon(self,depart,arrivee):

        dx, dy =  (arrivee.position[0]-self.ballon.position[0]), (arrivee[1]-self.ballon.position[1])
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 0.75 :
            self.ballon.position = arrivee
            self.tir_en_cours = False
            return False
        else :
            dx, dy = dx / distance, dy / distance  # Normalisation
            self.ballon.position = (self.ballon.position[0] + dx * 0.01, self.ballon.position[1] + dy * 0.01)  # Mise à jour de la position
            return True

    def position_but_adverse(self,joueur):
        if joueur in self.joueurs_dom :
            return (0,15)
        else :
            return (30,15)