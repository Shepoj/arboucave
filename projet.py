from __future__ import annotations

import random
from random import randint, shuffle, choice
from carte import Case, Village
from gens import Soldat





class Player():
    def __init__(self, couleur: str, village: Village | None = None, j1=False):
        self.couleur = couleur
        self.village = village
        self.fief = [village] if village else []
        self.actions=10
        self.j1=j1
        self.vaincu=False

        self.part = (randint(0, 10), randint(0, 10), randint(0, 10))
        self.ordre = [0, 1, 2]
        shuffle(self.ordre)

    @property
    def armee(self):
        return sum([village.armee for village in self.fief])
    
    def __repr__(self):
        return f"{self.__class__.__name__} {self.couleur}"

    def mort_soldats(self, pertes: int):
        non_vu = self.armee
        for village in self.fief:
            for habitant in village.habitants:
                if isinstance(habitant, Soldat):
                    proba = pertes/non_vu
                    if random.random() < proba:
                        habitant.mourir()
                        pertes += -1
                        print("SOLDAT MORT")
                    non_vu += -1
            
    def etendre_fief(self, village: Village):
        self.fief.append(village)
    

    def botCapture(self, carte):
        border_tiles = []
        for village in self.fief:
            for terre in village.terres:
                x, y = terre.coords
                neighbors = []
                if x > 0:
                    neighbors.append((x-1, y))
                if x < 110:
                    neighbors.append((x+1, y))
                if y > 0:
                    neighbors.append((x, y-1))
                if y < 82:
                    neighbors.append((x, y+1))
                neighbors=set(neighbors)
                for nx, ny in neighbors:
                    if (nx, ny) not in village.terres:
                        border_tiles.append((nx, ny))

        if border_tiles:
            target_tile = choice(border_tiles)
            return target_tile
        return 0
        

    def botCollecte(self):
        terres = []
        for village in self.fief:
            for terre in village.terres:
                terres.append(terre)
        if terres:
            target_tile = choice(terres)
            target_tile.collecte()
            return 1
        return 0
    

    def botBuild(self):
        unbuilt = []
        for village in self.fief:
            for terre in village.terres:
                if not terre.built and terre.caseType != "village":
                    unbuilt.append(terre)
        if unbuilt:
            target_tile = choice(unbuilt)
            return target_tile
        return 0
    

    def botConstruireEglise(self):
        unholy = []
        for village in self.fief:
            if not village.a_eglise:
                unholy.append(village)
        if unholy:  
            target_village = choice(unholy)
            return target_village
        return None
    
    def botCreerVillage(self, carte):
        villageable = []
        for village in self.fief:
            for terre in village.terres:
                if terre.caseType != "village":
                    i,j=terre.coords
                    w, h = len(carte),len(carte[0])
                    minx,miny=max(0,i-2),max(0,j-2)
                    maxx,maxy=min(w,i+3),min(h,j+3)
                    isVillage=False
                    for x in range(minx,maxx):
                        for y in range(miny,maxy):
                            if carte[x][y].caseType=="village":
                                isVillage=True
                    if not isVillage:
                        villageable.append(terre)
        if villageable:
            target_tile = choice(villageable)
            return target_tile
        return 0
    
    def botCollecteImpots(self):
        villages = []
        for village in self.fief:
            if village != self.village:
                villages.append(village)
        if villages:
            target_village = choice(villages)
            village.chef.imposition_seigneur()
            return 1
    def botGuerre(self, players):
        adversaire = random.choice(players)
        if adversaire != self:
            return adversaire
        return 0
    def botRecruterSoldat(self):
        villages = []
        for village in self.fief:
            if len(village.habitants) < village.max_habitants:
                villages.append(village)
        if villages:
            target_village = choice(villages)
            if target_village.chef.argent > 10:
                target_village.chef.argent += -10
                target_village.ajout_habitant(Soldat())
                return 1
        return 0


    def vaincre(self, vaincu: Player):
        print(f"{self} a vaincu {vaincu}")
        for village in vaincu.fief:
            village.chef.player = self
            village.redraw()

        self.fief += vaincu.fief
        vaincu.fief = []
        vaincu.village.chef.vassalisation(self.village.chef)
        vaincu.vaincu = True




#    def redraw(self, bord: tuple[bool, bool, bool, bool]):
#        # ordre W E N S
#        for ligne in self.outline:
#            if ligne is not None:
#                canevas.delete(ligne)
#        
#        [x1, y1, x2, y2] = canevas.coords(self.fill)
#        X = (x1, x2)
#        Y = (y1, y2)
#        for i in range(4):
#            if bord[i]:
#                self.outline[i] = None

if __name__ == "__main__":
    p = Player("lime")
    c = Case((0, 0), "eau")
    v = Village(c, p)