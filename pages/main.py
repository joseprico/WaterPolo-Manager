import pygame
import random as r
from terrain import Terrain
from joueur import Joueur
from match import Match

pygame.init()

# Dimensions de la fenêtre (proportionnelles au terrain FINA 30m x 20m)
SCREEN_WIDTH = 900  # Largeur
SCREEN_HEIGHT = 600  # Hauteur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulation de Water-Polo")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Facteur d'échelle pour transformer les mètres en pixels
SCALE_X = SCREEN_WIDTH / 30  # Terrain de 30m → largeur de la fenêtre
SCALE_Y = SCREEN_HEIGHT / 20  # Terrain de 20m → hauteur de la fenêtre

equipe_A = "Équipe A"
equipe_B = "Équipe B"

# Ajout des joueurs avec leurs postes et côtés respectifs
joueurs_dom = [
    Joueur("Gardien A", "domicile", "gardien", (0, 0), 100, 0, 0),
    Joueur("Ailier Gauche A", "domicile", "ailier gauche", (0, 0), 100, 80, 20),
    Joueur("Ailier Droit A", "domicile", "ailier droit", (0, 0), 100, 80, 20),
    Joueur("Demi Gauche A", "domicile", "demi gauche", (0, 0), 100, 75, 15),
    Joueur("Demi Droit A", "domicile", "demi droit", (0, 0), 100, 75, 15),
    Joueur("Pointe A", "domicile", "pointe", (0, 0), 100, 90, 30),
    Joueur("Défenseur Pointe A", "domicile", "défenseur pointe", (0, 0), 100, 65, 40)
]

joueurs_ext = [
    Joueur("Gardien B", "exterieur", "gardien", (0, 0), 100, 0, 0),
    Joueur("Ailier Gauche B", "exterieur", "ailier gauche", (0, 0), 100, 80, 20),
    Joueur("Ailier Droit B", "exterieur", "ailier droit", (0, 0), 100, 80, 20),
    Joueur("Demi Gauche B", "exterieur", "demi gauche", (0, 0), 100, 75, 15),
    Joueur("Demi Droit B", "exterieur", "demi droit", (0, 0), 100, 75, 15),
    Joueur("Pointe B", "exterieur", "pointe", (0, 0), 100, 90, 30),
    Joueur("Défenseur Pointe B", "exterieur", "défenseur pointe", (0, 0), 100, 65, 40)
]
terrain = Terrain()
match = Match(equipe_A,equipe_B,joueurs_dom,joueurs_ext,terrain)
match.position_depart()

# Boucle de Pygame avec gestion de l'engagement
running = True
clock = pygame.time.Clock()

def afficher_terrain():
    """Affiche le terrain, les lignes, les joueurs et le ballon"""
    screen.fill(BLUE)  # Fond bleu pour l'eau

    # Dessiner les cages
    cage_width = 2 * SCALE_X
    cage_height = 5 * SCALE_Y
    pygame.draw.rect(screen, WHITE, (0, (SCREEN_HEIGHT - cage_height) // 2, cage_width, cage_height))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - cage_width, (SCREEN_HEIGHT - cage_height) // 2, cage_width, cage_height))

    # Dessiner les lignes réglementaires
    pygame.draw.line(screen, RED, (terrain.ligne_2m * SCALE_X, 0), (terrain.ligne_2m * SCALE_X, SCREEN_HEIGHT), 2)
    pygame.draw.line(screen, RED, ((terrain.longueur - terrain.ligne_2m) * SCALE_X, 0), ((terrain.longueur - terrain.ligne_2m) * SCALE_X, SCREEN_HEIGHT), 2)

    pygame.draw.line(screen, YELLOW, (terrain.ligne_5m * SCALE_X, 0), (terrain.ligne_5m * SCALE_X, SCREEN_HEIGHT), 2)
    pygame.draw.line(screen, YELLOW, ((terrain.longueur - terrain.ligne_5m) * SCALE_X, 0), ((terrain.longueur - terrain.ligne_5m) * SCALE_X, SCREEN_HEIGHT), 2)

    pygame.draw.line(screen, GREEN, (terrain.ligne_6m * SCALE_X, 0), (terrain.ligne_6m * SCALE_X, SCREEN_HEIGHT), 2)
    pygame.draw.line(screen, GREEN, ((terrain.longueur - terrain.ligne_6m) * SCALE_X, 0), ((terrain.longueur - terrain.ligne_6m) * SCALE_X, SCREEN_HEIGHT), 2)

    pygame.draw.line(screen, WHITE, (terrain.ligne_milieu * SCALE_X, 0), (terrain.ligne_milieu * SCALE_X, SCREEN_HEIGHT), 2)

    # Dessiner les joueurs
    for joueur in match.joueurs_dom:
        x, y = joueur.position
        pygame.draw.circle(screen, RED, (int(x * SCALE_X), int(y * SCALE_Y)), 10)  # Rouge = Équipe domicile

    for joueur in match.joueurs_ext:
        x, y = joueur.position
        pygame.draw.circle(screen, YELLOW, (int(x * SCALE_X), int(y * SCALE_Y)), 10)  # Jaune = Équipe extérieure

    # Dessiner le ballon
    bx, by = match.ballon
    pygame.draw.circle(screen, WHITE, (int(bx * SCALE_X), int(by * SCALE_Y)), 7)

    pygame.display.flip()

# Lancer l'engagement
aillier_dom, aillier_ext = match.engagement_quart_temps()

# Boucle de jeu
running = True
clock = pygame.time.Clock()

while running:
    # Gestion des événements (fermeture de la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mettre à jour l'engagement
    engagement_termine = match.update_engagement(aillier_dom, aillier_ext)

    # Afficher le terrain et les joueurs
    afficher_terrain()

    # Si l'engagement est terminé, sortir de la boucle
    if engagement_termine:
        match.se_placer_en_attaque()
        match.se_placer_en_defense()
        match.update_chrono_attaque()


    clock.tick(1)

pygame.quit()
