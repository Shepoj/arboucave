from __future__ import annotations

import random
from random import randint, choice
from noms import prenoms, noms

class Player():
    def __init__(self, couleur, village: Village, j1=False):
        self.couleur=couleur
        self.village=village
        self.fief = [village] if village else []
        self.actions=10
        self.j1=j1

    def etendre_fief(self, village: Village):
        self.fief.append(village)



class Personne():
    def __init__(self,
        prenom: str | None = None,
        nom: str | None = None,
        age: int | None = None,
        ev = randint(30, 80)):

        self.prenom = choice(prenoms) if prenom is None else prenom
        self.nom = choice(noms) if nom is None else nom
        self.age = randint(0, ev) if age is None else age
        self.ev = ev

        self.village: Village = None
        self.humeur = 5
        self.argent = 0

    def __repr__(self):
        return f"{self.__class__.__name__} {self.argent}ⓐ"
    
    def __str__(self):
        return self.affiche_nom()
    
    def affiche_nom(self) -> str:
        return f"{self.nom} {self.prenom}"

    def vieillir(self):
        self.age += 1
        if self.age > self.ev:
            self.mourir()


class Roturier(Personne):
    def __init__(self, paysan = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statut = "paysan" if paysan else "artisan"

        if self.statut == "paysan":
            self.argent = 0
            self.ressources = 0
            self.prod=random.randint(2,5)
        else:  
            self.argent= random.randint(5,30)
            self.ressources = 0
            self.prod=random.randint(5,10)

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
    pass


class Ecclesiastique(Personne):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.argent = 0 # pas defini avant
        self.don = choice(["prod","vie","humeur","guerre"])


class Noble(Personne):
    def __init__(self, player: Player | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.argent = random.randint(10,50)
        self.ressources = random.randint(10,50)

        self.seigneur = None
        self.player = player
        self.l_roturiers: list[Roturier] = []
        self.l_vassaux: list[Noble] = []

    def affiche_nom(self):
        voy = "AEYUIOH"
        sep = " d'" if self.nom[0] in voy else " de "
        return f"{self.prenom}{sep}{self.nom}"

    def collecte_impots(self):
        for roturier in self.l_roturiers:
            roturier.payer_impot(self)

    def distribution_dime(self):
        montant = 15
        if self.village is not None and self.village.hasEglise:
            self.village.cure.argent += montant
            self.argent += -montant

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
        self.argent -= impotArgent
        self.ressources -= impotRessources
        self.seigneur.argent += impotArgent
        self.seigneur.ressources += impotRessources




        
class Case():
    def __init__(self, coords, tkItem, terrain):
        self.coords=coords
        self.terrain=terrain
        self.captured=False
        self.master=None
        self.tkItem=tkItem
        self.type=None
        self.built=False
        
    def capture(self,village):
        self.captured=True
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
        
            
        
class Village(Case):
    def __init__(self, case: Case, player: Player):
        self.type="village"

        self.lieu = case
        self.coords = case.coords
        self.terres = [case.coords]

        self.habitants: list[Personne] = []
        self.chef = Noble(player)
        self.ajout_habitant(self.chef)
        for _ in range(4):
            self.ajout_habitant(Roturier())
        
        self.cure = None
        self.armee = 0
        self.vassaux = []

        case.type = "village"
        case.master = self
        player.etendre_fief(self)

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
            return True
        return False
    
    def construire_eglise(self):
        if not self.hasEglise:
            cure = Ecclesiastique()
            if self.ajout_habitant(self, cure):
                self.cure = cure
 
    def ajoutTerres(self,terre):
        self.terres.append(terre)

    def info_habitants(self) -> str:
        info = ""
        for habitant in self.habitants:
            info += f"{repr(habitant)}\n"
        return info


if __name__ == "__main__":
    p1 = Noble()
    p2 = Roturier()
    print(repr(p1))
    print(repr(p2))