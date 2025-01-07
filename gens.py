from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from carte import Village
    from projet import Player

from random import randint, choice

from noms import noms, prenoms





class Personne():
    def __init__(self, village: Village):
        self.prenom = choice(prenoms)
        self.nom = choice(noms)
        self.ev = randint(30, 80)
        self.age = randint(0, self.ev)

        self.humeur = 5
        self.argent = 0
        self.ressources = 0

        self.village = village

    def __repr__(self):
        return f"{self.__class__.__name__} {self.argent}¤ {self.ressources}⁂"
    
    def __str__(self):
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
        else:
            self.mourir()
    
    def mourir(self):
        self.village.habitants.remove(self)





class Roturier(Personne):
    def __init__(self, village: Village):
        super().__init__(village)

        self.prod = 0

    def produire(self):
        self.ressources += self.prod
        self.argent += self.prod
    
    def payer_impot(self, montant: int):
        noble = self.village.chef

        if self.argent > 0:
            impot = int(montant * self.argent)
            self.argent += -impot
            noble.argent += impot
        elif self.ressources:
            impot = int(montant * self.ressources)
            self.ressources += impot
            noble.ressources += impot
        else:
            self.mourir()

class Paysan(Roturier):
    def __init__(self, village):
        super().__init__(village)

        self.argent = 0
        self.prod = randint(2, 5)

    def payer_impot(self):
        super().payer_impot(0.5)

class Artisant(Roturier):
    def __init__(self, village):
        super().__init__(village)

        self.argent = randint(5, 30)
        self.prod = randint(5, 10)
    
    def payer_impot(self):
        super().payer_impot(0.25)





class Soldat(Personne):
    def __init__(self, village):
        super().__init__(village)

    def consommer(self):
        if self.ressources > 0:
            self.ressources += -1
        elif self.village.chef.ressources > 0:
            self.village.chef.ressources += -1
        else:
            self.mourir()





class Ecclesiastique(Personne):
    def __init__(self, village):
        super().__init__(village)

        self.ressources = 1
        self.don = choice(["prod", "vie", "humeur", "guerre"])





class Noble(Personne):
    def __init__(self, village: Village, player: Player):
        super().__init__(village)

        self.argent = randint(10,50)
        self.ressources = randint(10,50)

        self.l_roturiers: list[Roturier] = []
        self.l_vassaux: list[Noble] = []
        self.soldats: list[Soldat] = []
        
        self.player = player
 
    def __str__(self):
        voy = "AEYUIOH"
        sep = " d'" if self.nom[0] in voy else " de "
        return f"{self.prenom}{sep}{self.nom}"

    @property
    def seigneur(self):
        return self.player.village.chef

    def collecte_impots(self):
        for roturier in self.l_roturiers:
            roturier.payer_impot(self)

    def distribution_dime(self):
        montant = 1
        if self.village.a_eglise:
            self.village.cure.ressources += montant
            self.ressources += -montant

    def vassalisation(self, seigneur: Noble):
        self.player.fief.remove(self.village)
        self.player = seigneur.player
        seigneur.l_vassaux.append(self)
        seigneur.player.fief.append(self.village)

    def imposition_seigneur(self):
        impot_argent = int(0.3*self.argent)
        impot_ressources = int(0.3*self.ressources)
        argent_a_payer = impot_argent if self.argent > impot_argent else self.argent
        ressources_a_donner = impot_ressources if self.ressources > impot_ressources else self.ressources
        
        self.argent += -argent_a_payer
        self.ressources += -ressources_a_donner
        self.seigneur.argent += argent_a_payer
        self.seigneur.ressources += ressources_a_donner