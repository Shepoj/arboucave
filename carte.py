from __future__ import annotations

from gens import Personne, Roturier, Soldat, Ecclesiastique, Noble

from config import *
from divers import point, Once





class Case(metaclass=Once):
    def __init__(self, coords: point[int], terrain: str):
        self.coords = coords
        self.terrain = terrain
        self.controle: Village | None = None

        self.construite = False

    def __str__(self):
        x, y = self.coords
        return f"{x}, {y} : {self.__class__.__name__} {self.terrain}"
        
    def capture(self, village: Village):
        self.controle = village
        village.terres.append(self)

    def collecte(self, montant=10):
        if self.controle is not None:
            production = montant if self.terrain == "herbe" else montant//2
            if self.terrain == "roche":
                self.controle.chef.argent += production
            else:
                self.controle.chef.ressources += production





class Ferme(Case):
    def __init__(self, case: Case, couleur: str):
        assert case.controle

        Case.__init__(self, case.coords, case.terrain)
        self.controle = case.controle
        self.couleur = couleur

    def collecte(self, montant=20):
        Case.collecte(self, montant)





class Village(Case):
    def __init__(self, case: Case, couleur: str):
        Case.__init__(self, case.coords, case.terrain)
        self.controle = self
        self.couleur = couleur

        self.terres: list[Case] = [self]
        self.habitants: list[Personne] = []
        self.chef = Noble(self)
        self.cure: Ecclesiastique | None = None
        self.armee = 0
        
        self.ajout_habitant(self.chef)
        for _ in range(4):
            self.ajout_habitant(Roturier(self))

    @property
    def max_habitants(self):
        return 10 + sum((5 for c in self.terres if isinstance(c, Ferme)))
    
    @property
    def a_eglise(self):
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
        cure = Ecclesiastique(self)
        if self.ajout_habitant(cure):
            self.cure = cure
 
    def ajout_terre(self, terre: Case):
        if terre not in self.terres:
            self.terres.append(terre)
            return True
        return False

    def info_habitants(self) -> str:
        info = ""
        for habitant in self.habitants:
            info += f"{repr(habitant)}\n"
        return info