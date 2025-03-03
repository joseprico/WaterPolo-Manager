from joueur import Joueur
from match import Match


# Ajout des joueurs avec leurs postes et côtés respectifs
joueurs_dom = [
    Joueur("Gardien A", "domicile", "gardien", (0, 0), 100, 0, 0,0,80),
    Joueur("Ailier Gauche A", "domicile", "ailier gauche", (0, 0), 100, 80, 20,65,0),
    Joueur("Ailier Droit A", "domicile", "ailier droit", (0, 0), 100, 80, 20,46,0),
    Joueur("Demi Gauche A", "domicile", "demi gauche", (0, 0), 100, 75, 15,70,0),
    Joueur("Demi Droit A", "domicile", "demi droit", (0, 0), 100, 75, 15,90,0),
    Joueur("Pointe A", "domicile", "pointe", (0, 0), 100, 90, 30,55,0),
    Joueur("Défenseur Pointe A", "domicile", "défenseur pointe", (0, 0), 100, 65, 40,70,0)
]

joueurs_ext = [
    Joueur("Gardien B", "exterieur", "gardien", (0, 0), 100, 0, 0,0,30),
    Joueur("Ailier Droit B", "exterieur", "ailier droit", (0, 0), 100, 80, 20,95,0),
    Joueur("Ailier Gauche B", "exterieur", "ailier gauche", (0, 0), 100, 80, 20,95,0),
    Joueur("Demi Droit B", "exterieur", "demi droit", (0, 0), 100, 75, 15,60,0),
    Joueur("Demi Gauche B", "exterieur", "demi gauche", (0, 0), 100, 75, 15,60,0),
    Joueur("Pointe B", "exterieur", "pointe", (0, 0), 100, 90, 30,70,0),
    Joueur("Défenseur Pointe B", "exterieur", "défenseur pointe", (0, 0), 100, 65, 40,80,0)
]
equipe_A = "Équipe A"
equipe_B = "Équipe B"
match = Match(equipe_A,equipe_B,joueurs_dom,joueurs_ext)
match.lancement_jeu()
