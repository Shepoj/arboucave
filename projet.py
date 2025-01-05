from __future__ import annotations

import random
from random import randint, shuffle, choice
from noms import prenoms, noms
from config import canevas, taillecase

class Player():
    def __init__(self, couleur, village: Village, j1=False):
        self.couleur=couleur
        self.village=village
        self.fief = [village] if village else []
        self.actions=10
        self.j1=j1

        self.part = (randint(0, 10), randint(0, 10), randint(0, 10))
        self.ordre = [0, 1, 2]
        shuffle(self.ordre)

    @property
    def armee(self):
        return sum([village.armee for village in self.fief])
    
    def mort_soldats(self, pertes: int):
        non_vu = self.armee
        for village in self.fief:
            for habitant in village.habitants:
                if isinstance(habitant, Soldat):
                    proba = pertes/non_vu
                    if random.random() < proba:
                        habitant.mourir()
                        pertes += -1
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
            if not village.hasEglise:
                unholy.append(village)
        if unholy:  
            target_village = choice(unholy)
            return target_village
        return 0
    
    def botCreerVillage(self, carte):
        villageable = []
        for village in self.fief:
            for terre in village.terres:
                if terre.caseType != "village":
                    i,j=terre.coords
                    gx,gy=len(carte),len(carte[0])
                    minx,miny=max(0,i-2),max(0,j-2)
                    maxx,maxy=min(gx,i+3),min(gy,j+3)
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
        for village in vaincu.fief:
            village.chef.player = self
        self.fief += vaincu.fief
        vaincu.fief = []
        vaincu.village.chef.vassalisation(self.village.chef)



class Personne():
    def __init__(self,
        village: Village | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        age: int | None = None,
        ev = randint(30, 80)):

        self.prenom = choice(prenoms) if prenom is None else prenom
        self.nom = choice(noms) if nom is None else nom
        self.age = randint(0, ev) if age is None else age
        self.ev = ev
        self.humeur = 5
        self.argent = 0
        self.ressources = 0

        self.village = village

    def __repr__(self):
        return f"{self.__class__.__name__} {self.argent}¤ {self.ressources}⁂"
    
    def __str__(self):
        return self.affiche_nom()
    
    def affiche_nom(self) -> str:
        return f"{self.nom} {self.prenom}"

    def vieillir(self):
        self.age += 1
        if self.age > self.ev:
            self.mourir()
            return True
        return False
    def consommer(self):
        if self.ressources > 0:
            self.ressources += -1
        elif type(self)==Soldat and self.village.chef.ressources > 0:
            self.village.chef.ressources += -1
        else:
            self.mourir()
    def mourir(self):
        self.village.habitants.remove(self)


class Roturier(Personne):
    def __init__(self, paysan = True, **kwargs):
        super().__init__(**kwargs)
        self.statut = "paysan" if paysan else "artisan"
        if self.statut == "paysan":
            self.argent = 0
            self.ressources = 0
            self.prod=random.randint(2,5)
        else:  
            self.argent= random.randint(5,30)
            self.ressources = 0
            self.prod=random.randint(5,10)

    def produire(self):
        self.ressources += self.prod
        self.argent += self.prod
    def payer_impot(self, noble: Noble):
        cout = 0.5 if self.statut=="paysan" else 0.25
        if self.argent > 0:
            impot = int(cout*self.argent)
            self.argent += -impot
            noble.argent += impot
        elif self.ressources:
            impot = int(cout*self.ressources)
            self.ressources += impot
            noble.ressources += impot
        else:
            self.mourir()

    def mourir(self):
        pass


class Soldat(Personne):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Ecclesiastique(Personne):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.argent = 0
        self.ressources = 1 #pour manger
        self.don = choice(["prod","vie","humeur","guerre"])


class Noble(Personne):
    def __init__(self, player: Player | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.argent = random.randint(10,50)
        self.ressources = random.randint(10,50)

        self.player = player
        self.seigneur = None
        self.l_roturiers: list[Roturier] = []
        self.l_vassaux: list[Noble] = []
        self.soldats: list[Soldat] = []

    def affiche_nom(self):
        voy = "AEYUIOH"
        sep = " d'" if self.nom[0] in voy else " de "
        return f"{self.prenom}{sep}{self.nom}"

    def collecte_impots(self):
        for roturier in self.l_roturiers:
            roturier.payer_impot(self)

    def distribution_dime(self):
        montant = 1
        if self.village is not None and self.village.hasEglise:
            self.village.cure.ressources += montant
            self.ressources += -montant

    def vassalisation(self, seigneur):
        self.seigneur=seigneur
        seigneur.l_vassaux.append(self)
        seigneur.player.fief.append(self.village)

        if self.player:
            self.player.fief.remove(self.village)
        self.player=seigneur.player

    def imposition_seigneur(self):
        impotArgent = int(0.3*self.argent)
        impotRessources = int(0.3*self.ressources)
        aImposerArgent = impotArgent if max(self.argent-impotArgent, 0) else self.argent
        aImposerRessources = impotRessources if max(self.ressources-impotRessources, 0) else self.ressources
        self.argent -= aImposerArgent
        self.ressources -= aImposerRessources
        self.seigneur.argent += aImposerArgent
        self.seigneur.ressources += aImposerRessources





class Case():
    def __init__(self, coords: tuple[int, int], terrain: str, couleur: str):
        self.coords = coords
        self.terrain=terrain
        self.master=None
        self.type=None
        self.caseType=None
        self.built=False

        self.tkItem = self.draw(couleur)
        canevas.itemconfig(self.tkItem, tags=self.terrain)

    @property
    def captured(self):
        return self.master is not None
        
    def capture(self, village: Village):
        self.master=village
        self.master.ajoutTerres(self)

    def collecte(self):
        if self.master:
            production=10 if self.terrain=="herbe" else 15 if self.built else 5
            if self.terrain=="roche":
                self.master.chef.argent+=production
            else:
                self.master.chef.ressources+=production

    def build(self):
        if self.master:
            self.built=True
            self.master.chef.argent-=25
            self.master.chef.ressources-=25

    def draw(self, couleur):
        i, j = self.coords
        return canevas.create_rectangle(i*taillecase, j*taillecase, i*taillecase+taillecase, j*taillecase+taillecase,
            fill=couleur, outline="")
        
            

# je pense pas que ça doive heriter
class Village():
    def __init__(self, case: Case, player: Player):
        self.caseType="village"

        self.case = case
        self.coords = case.coords
        self.terres = []
        self.master = None
        #self.terres = [case]
        #case.master = self

        self.habitants: list[Personne] = []
        self.chef = Noble(player, self)
        self.ajout_habitant(self.chef)
        for _ in range(4):
            self.ajout_habitant(Roturier(self))
        
        self.cure = None
        self.armee = 0

        case.type = "village"
        case.capture(self)
        player.etendre_fief(self)

        # init
        self.tkItem = self.draw()

    @property
    def max_habitants(self):
        return 20 * len(self.terres)
    
    @property
    def hasEglise(self):
        return self.cure is not None

    def ajout_habitant(self, arrivant: Personne):
        if len(self.habitants) < self.max_habitants:
            self.habitants.append(arrivant)
            arrivant.village = self

            if isinstance(arrivant, Soldat):
                self.armee += 1
            return True
        return False
    
    def construire_eglise(self):
        if not self.hasEglise:
            cure = Ecclesiastique(self)
            self.max_habitants += 1
            if self.ajout_habitant(self, cure):
                self.cure = cure
 
    def ajoutTerres(self,terre):
        self.terres.append(terre)
        self.terres = list(set(self.terres))

    def info_habitants(self) -> str:
        info = ""
        for habitant in self.habitants:
            info += f"{repr(habitant)}\n"
        return info

    def draw(self):
        tilecos = canevas.coords(self.case.tkItem)
        return canevas.create_polygon((tilecos[0]+taillecase/2),(tilecos[1]+taillecase/6),(tilecos[0]+taillecase/6),(tilecos[1]+taillecase*2/6),(tilecos[0]+taillecase/6),(tilecos[1]+taillecase*5/6),(tilecos[0]+taillecase*5/6),(tilecos[1]+taillecase*5/6),(tilecos[0]+taillecase*5/6),(tilecos[1]+taillecase*2/6),
            fill=self.chef.player.couleur, tags=["village"], outline="")







if __name__ == "__main__":
    p1 = Noble()
    p2 = Roturier()
    print(repr(p1))
    print(repr(p2))