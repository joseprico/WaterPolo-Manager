from terrain import Terrain
from joueur import Joueur
import random as r

class Match :
    def __init__(self, equipe_A, equipe_B, JoueursA,JoueursB,Terrain):
        self.domicile = equipe_A
        self.exterieur = equipe_B
        self.joueurs_dom = JoueursA
        self.joueurs_ext = JoueursB
        self.temps_total = 480
        self.tick_actuel = 0
        self.terrain = Terrain
        self.ballon = (0,0)

    def position_depart(self):
        """Position initiale des joueurs sur la ligne de but."""
        base_x_dom = r.randint(0,1)  # Ligne de but domicile
        base_x_ext = r.randint(self.terrain.longueur -1, self.terrain.longueur)  # Ligne de but extérieur


        positions_dom = {
            "gardien": (base_x_dom, self.terrain.largeur // 2),
            "ailier gauche": (base_x_dom, r.randint(self.terrain.largeur - 2, self.terrain.largeur-1)),
            "ailier droit": (base_x_dom, r.randint(0, 1)),
            "pointe": (base_x_dom, r.randint(int((self.terrain.largeur / 2) - 1), int((self.terrain.largeur / 2) + 1))),
            "demi gauche": (base_x_dom, r.randint(self.terrain.largeur - 5, self.terrain.largeur - 4)),
            "demi droit": (base_x_dom, r.randint(4, 5)),
            "défenseur pointe": (base_x_dom, 9)
        }

        # Positionnement des joueurs extérieur
        positions_ext = {
            "gardien": (base_x_ext, self.terrain.largeur // 2),
            "ailier gauche": (base_x_ext, r.randint(0, 1)),
            "ailier droit": (base_x_ext, r.randint(self.terrain.largeur - 2, self.terrain.largeur-1)),
            "pointe": (base_x_ext, r.randint(int((self.terrain.largeur / 2) - 1), int((self.terrain.largeur / 2) + 1))),
            "demi gauche": (base_x_ext, r.randint(self.terrain.largeur - 5, self.terrain.largeur - 4)),
            "demi droit": (base_x_ext, r.randint(4, 5)),
            "défenseur pointe": (base_x_ext, 9)
        }

        # Attribution des positions aux joueurs domicile
        for joueur in self.joueurs_dom:
            if joueur.poste in positions_dom:
                joueur.position = positions_dom[joueur.poste]
                print(joueur.position)

        # Attribution des positions aux joueurs extérieur
        for joueur in self.joueurs_ext:
            if joueur.poste in positions_ext:
                joueur.position = positions_ext[joueur.poste]
                print(joueur.position)


    def joueur_en_possession(self,Joueur):
        return Joueur.position == self.ballon

    """def engagement_quart_temps(self):
        aillier_dom = next((j for j in self.joueurs_dom if j.poste == "ailier droit"),None)
        aillier_ext = next((j for j in self.joueurs_ext if j.poste == "ailier gauche"),None)
        print("info")
        print(aillier_dom.nom)
        print(aillier_ext.nom)
        self.ballon = (self.terrain.longueur//2,1)
        x,y = self.ballon
        print(x,y)
        while (self.joueur_en_possession(aillier_dom) == False and self.joueur_en_possession(aillier_ext) == False):
            aillier_dom.se_deplacer_vers(x,y,1)
            aillier_ext.se_deplacer_vers(x,y,2)
            print(aillier_dom.position)
            print(aillier_ext.position)
            for joueur in joueurs_dom :
                if(joueur != aillier_dom):
                    x,y = joueur.position
                    joueur.se_deplacer_vers(terrain.longueur//2,y)
            for joueur in joueurs_ext :
                if(joueur != aillier_ext):
                    x,y = joueur.position
                    joueur.se_deplacer_vers(terrain.longueur//2,y)"""

    def engagement_quart_temps(self):
        """Initialise l'engagement et place les joueurs au bon endroit"""
        self.engagement_en_cours = True
        self.ballon = (self.terrain.longueur // 2, 1)  # Ballon au centre du terrain

        # Sélection des joueurs en course pour l'engagement
        aillier_dom = next((j for j in self.joueurs_dom if j.poste == "ailier droit"), None)
        aillier_ext = next((j for j in self.joueurs_ext if j.poste == "ailier gauche"), None)

        print("Engagement - Joueurs en course :")
        print(f"{aillier_dom.nom} vs {aillier_ext.nom}")
        return aillier_dom,aillier_ext


    def update_engagement(self,aillier_dom,aillier_ext):
        """Met à jour les positions des joueurs pendant l'engagement et vérifie la possession"""
        if not self.engagement_en_cours:
            return True  # Engagement déjà terminé

        x, y = self.ballon  # Position du ballon

        # Déplacement des joueurs en course vers le ballon
        aillier_dom.se_deplacer_vers(x, y, 2)
        aillier_ext.se_deplacer_vers(x, y, 2)



        # Déplacement des autres joueurs vers le centre du terrain
        count1 = 0
        for joueur in self.joueurs_dom:
            if joueur != aillier_dom and joueur.poste !="gardien":
                jx, jy = joueur.position
                joueur.se_deplacer_vers(self.terrain.longueur // 2, jy,1)
                count1 +=1

            print(count1)

        count2 = 0
        for joueur in self.joueurs_ext:
            if joueur != aillier_ext and joueur.poste !="gardien":
                jx, jy = joueur.position
                joueur.se_deplacer_vers(self.terrain.longueur // 2, jy,1)
                count2+=1

        print(count2)
        # Vérifier la possession du ballon
        if self.joueur_en_possession(aillier_dom) or self.joueur_en_possession(aillier_ext):
            self.engagement_en_cours = False  # L'engagement est terminé
            print("Engagement terminé !")
            return True

        return False



