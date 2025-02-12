from terrain import Terrain

class Joueur:
    def __init__(self, nom, equipe, poste, position, endurance, precision_tir, agressivite):
        self.nom = nom
        self.equipe = equipe
        self.poste = poste  # "gardien", "pointe", "ailier gauche", "ailier droit", "demi gauche", "demi droit", "défenseur pointe"
        self.position = position  # (x, y) sur le terrain
        self.endurance = endurance
        self.precision_tir = precision_tir
        self.agressivite = agressivite
        self.a_le_ballon = False
        self.exclu_pour = 0  # Durée de l’exclusion en ticks


    def se_deplacer_vers(self, cible_x, cible_y, vitesse):
        """Déplacement vers une position cible"""
        if self.position != (cible_x, cible_y):
            dx = cible_x - self.position[0]
            dy = cible_y - self.position[1]

            distance = (dx**2 + dy**2) ** 0.5
            if distance < 3 :
                new_x = cible_x
                new_y = cible_y
            elif distance > 0:
                dx = (dx / distance) * vitesse
                dy = (dy / distance) * vitesse

            new_x = self.position[0] + dx
            new_y = self.position[1] + dy


            if 0<new_x<30 and 0<new_y<20:
                self.position = (new_x, new_y)
                self.endurance -= 1





    def distance_au_joueur(self, autre_joueur):
        """Calcule la distance entre ce joueur et un autre joueur."""
        x1, y1 = self.position
        x2, y2 = autre_joueur.position
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def distance_au_point(self, x, y):
        """Calcule la distance entre ce joueur et un point (x, y)."""
        x1, y1 = self.position
        return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)