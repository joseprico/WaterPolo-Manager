from terrain import Terrain
from joueur import Joueur
import random as r
import math

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
        self.chrono_attaque = 15

    def position_depart(self):
        """Position initiale des joueurs sur la ligne de but."""
        base_x_ext = r.uniform(0,1)  # Ligne de but domicile
        base_x_dom = r.uniform(self.terrain.longueur -1, self.terrain.longueur)  # Ligne de but extérieur


        positions_dom = {
            "gardien": (base_x_dom, self.terrain.largeur // 2),
            "ailier gauche": (base_x_dom, 18),
            "ailier droit": (base_x_dom, r.uniform(0, 2)),
            "pointe": (base_x_dom, 12),
            "demi gauche": (base_x_dom, 16),
            "demi droit": (base_x_dom, 5),
            "défenseur pointe": (base_x_dom, 8)
        }

        # Positionnement des joueurs extérieur
        positions_ext = {
            "gardien": (base_x_ext, self.terrain.largeur // 2),
            "ailier gauche": (base_x_ext, r.uniform(0, 2)),
            "ailier droit": (base_x_ext, 18),
            "pointe": (base_x_ext,12),
            "demi gauche": (base_x_ext,5),
            "demi droit": (base_x_ext, 16),
            "défenseur pointe": (base_x_ext, 8)
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
        self.ballon = (self.terrain.longueur // 2,1)  # Ballon au centre du terrain

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
        aillier_ext.se_deplacer_vers(x, y, 1)



        # Déplacement des autres joueurs vers le centre du terrain
        for joueur in self.joueurs_dom:
            if joueur != aillier_dom and joueur.poste !="gardien":
                jx, jy = joueur.position
                joueur.se_deplacer_vers(self.terrain.longueur // 2, jy,1)

        for joueur in self.joueurs_ext:
            if joueur != aillier_ext and joueur.poste !="gardien":
                jx, jy = joueur.position
                joueur.se_deplacer_vers(self.terrain.longueur // 2, jy,1)

        # Vérifier la possession du ballon
        if aillier_dom.position == self.ballon or aillier_ext.position == self.ballon:
            if aillier_dom.position == self.ballon:
                aillier_dom.a_le_ballon = True
            else:
                aillier_ext.a_le_ballon = True
            self.engagement_en_cours = False  # L'engagement est terminé
            print("Engagement terminé !")
            return True

        return False

    def equipe_en_possession(self,equipe):
        rep = False
        for joueur in equipe :
            if(joueur.a_le_ballon == True):
                rep = True
        return rep



    def se_placer_en_attaque(self):
        if self.equipe_en_possession(self.joueurs_ext) == True:
            formations = {
                "ailier gauche": (r.uniform(self.terrain.longueur-3,self.terrain.longueur-2),r.uniform(2,3)),
                "ailier droit": (r.uniform(self.terrain.longueur-3,self.terrain.longueur-2),r.uniform(17,18)),
                "pointe": (r.uniform(self.terrain.longueur-3,self.terrain.longueur-2), r.uniform(9,11)),
                "demi gauche": (r.uniform(self.terrain.longueur-7,self.terrain.longueur-6), r.uniform(5,6)),
                "demi droit": (r.uniform(self.terrain.longueur-7,self.terrain.longueur-6),r.uniform(16,17)),
                "défenseur pointe": (r.uniform(self.terrain.longueur-9,self.terrain.longueur-7), r.uniform(9,11))
            }
            joueurs_en_attaque = self.joueurs_ext

        else :

            formations = {
                "ailier gauche": (r.uniform(2,3),r.uniform(17,18)),
                "ailier droit": (r.uniform(2,3), r.uniform(2,3)),
                "pointe": (r.uniform(2,3),  r.uniform(9,11)),
                "demi droit": (r.uniform(6,7),  r.uniform(5,6)),
                "demi gauche": (r.uniform(6,7),r.uniform(16,17)),
                "défenseur pointe": (r.uniform(7,9), r.uniform(9,11))
            }
            joueurs_en_attaque = self.joueurs_dom

        for joueur in joueurs_en_attaque :
            if joueur.poste in formations:
                cible_x, cible_y = formations[joueur.poste]
                avait_le_ballon = joueur.a_le_ballon
                joueur.se_deplacer_vers(cible_x, cible_y,2)
                if avait_le_ballon :
                    self.ballon = joueur.position



    def se_placer_en_defense(self):
        """Chaque défenseur suit son adversaire respectif selon la stratégie définie."""
        if self.equipe_en_possession(self.joueurs_ext):
            joueurs_defenseurs = self.joueurs_dom  # Équipe domicile en défense
            joueurs_attaquants = self.joueurs_ext  # Équipe extérieure en attaque
        else:
            joueurs_defenseurs = self.joueurs_ext  # Équipe extérieure en défense
            joueurs_attaquants = self.joueurs_dom  # Équipe domicile en attaque

        # Définition des correspondances défensives
        correspondances = {
            "ailier gauche": "demi droit",
            "ailier droit": "demi gauche",
            "demi gauche": "ailier droit",
            "demi droit": "ailier gauche",
            "pointe": "défenseur pointe",
            "défenseur pointe": "pointe"
        }

        # Assigner chaque défenseur à son attaquant
        for defenseur in joueurs_defenseurs:
            if defenseur.poste in correspondances:  # Vérifier que le poste a une correspondance
                adversaire_poste = correspondances[defenseur.poste]

                # Trouver l'adversaire correspondant
                adversaire = next((j for j in joueurs_attaquants if j.poste == adversaire_poste), None)
                decalage_x = r.uniform(-0.5, 0.5)
                decalage_y = r.uniform(-0.5, 0.5)
                if adversaire:
                    # Déplacement du défenseur vers son adversaire
                    defenseur.se_deplacer_vers(adversaire.position[0] + decalage_x,adversaire.position[1] + decalage_y, 2)

    def update_chrono_attaque(self):
        """Met à jour le chrono d'attaque et force un changement de possession si 0"""
        if self.chrono_attaque > 0:
            self.chrono_attaque -= 1
        else:
            print("⏳ Temps d'attaque écoulé ! Changement de possession.")
            self.transferer_possession()

    def transferer_possession(self):
        """Donne le ballon au défenseur le plus proche de l'attaquant"""
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
            self.chrono_attaque = 30  # Réinitialisation du chrono pour la nouvelle équipe
            print(f"🎯 {defenseur_proche.nom} récupère le ballon et la contre-attaque commence !")


