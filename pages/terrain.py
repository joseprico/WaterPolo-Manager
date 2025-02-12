class Terrain:
    def __init__(self):
        """Dimensions FINA : 30m x 20m, avec zones réglementaires"""
        self.largeur = 20
        self.longueur = 30
        self.ligne_milieu = 15
        self.ligne_2m = 2
        self.ligne_5m = 5
        self.ligne_6m = 6

    def est_dans_limites(self, x, y):
        """Vérifie si une position est dans les limites du terrain"""
        return 0 <= x <= self.largeur and 0 <= y <= self.longueur
