from __future__ import annotations
from typing import TYPE_CHECKING, Self
if TYPE_CHECKING:
    from projet import Player

from gens import Personne, Roturier, Soldat, Ecclesiastique, Noble
from config import *
from divers import argmax, bords_case, adjacent, mix_couleurs
from perlin import generate_perlin_grid

type point = tuple[int, int]




class Case():
    def __init__(self, coords: point, terrain: str):
        self.coords = coords
        self.terrain = terrain
        self.controle: Village | None = None

        # tkinter
        if self.__class__ == Case:
            self._draw()

    def __str__(self):
        x, y = self.coords
        return f"{x}, {y} : {self.__class__.__name__} {self.terrain}"

    @property
    def sous_controle(self):
        return self.controle is not None

    @property
    def cases_voisines(self):
        return {d: carte[x][y] for d, (x, y) in adjacent(self.coords, (0, 0), (grille_w-1, grille_h-1)).items()}
        
    def capture(self, village: Village):
        self.controle = village
        self.redraw()
        for case in self.cases_voisines.values():
            case.redraw()

    def collecte(self):
        if self.sous_controle:
            production=10 if self.terrain=="herbe" else 15 if self.built else 5
            if self.terrain=="roche":
                self.controle.chef.argent+=production
            else:
                self.controle.chef.ressources+=production

    def build(self):
        if self.sous_controle:
            self.built = True
            self.controle.chef.argent += -25
            self.controle.chef.ressources += -25

    def _draw(self):
        # appeler uniquement à l'initialisation
        i, j = self.coords
        self.tk_fill =\
            canevas.create_rectangle(i*taille_case, j*taille_case, i*taille_case+taille_case, j*taille_case+taille_case,\
                fill=couleur_terrain[self.terrain], outline="",
                tags="case")

        self.tk_outline = {d: None for d in ["w", "s", "e", "n"]}

    def redraw(self):
        if not self.sous_controle:
            return 
        
        couleur = self.controle.chef.player.couleur
        canevas.itemconfig(self.tk_fill, fill=mix_couleurs(couleur_terrain[self.terrain], couleur))

        coords = canevas.coords(self.tk_fill)
        nw, se = (coords[0], coords[1]), (coords[2], coords[3])
        bords = bords_case(nw, se)

        for d, case in self.cases_voisines.items():
            if case.controle != self.controle:
                if self.tk_outline[d] is None:
                    p, q = bords[d]
                    self.tk_outline[d] = canevas.create_line(*p, *q, fill=couleur, width=2)
                else:
                    canevas.itemconfig(self.tk_outline[d], fill=couleur)
        
            elif self.tk_outline[d] is not None:
                canevas.delete(self.tk_outline[d])





class Village(Case):
    def __init__(self, case: Case, player: Player, *args, **kwargs):
        super().__init__(case.coords, case.terrain, *args, **kwargs)
        self.controle = self

        self.terres: list[Case] = []
        self.habitants: list[Personne] = []
        self.chef = Noble(self, player)
        self.cure: Ecclesiastique | None = None
        self.armee = 0
        
        self.ajout_habitant(self.chef)
        for _ in range(4):
            self.ajout_habitant(Roturier(self))

        player.etendre_fief(self)

        x, y = self.coords
        carte[x][y] = self

        #tkinter
        canevas.delete(case.tk_fill)
        for x in case.tk_outline.values():
            if x is not None:
                canevas.delete(x)
    
        if self.__class__ == Village:
            self._draw()

    @property
    def max_habitants(self):
        return 20*len(self.terres) + (1 if self.a_eglise else 0)
    
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
    
    def _draw(self):
        super()._draw()
        super().redraw()

        tilecos = canevas.coords(self.tk_fill)

        self.maison =\
            canevas.create_polygon((tilecos[0]+taille_case/2),(tilecos[1]+taille_case/6),(tilecos[0]+taille_case/6),(tilecos[1]+taille_case*2/6),(tilecos[0]+taille_case/6),(tilecos[1]+taille_case*5/6),(tilecos[0]+taille_case*5/6),(tilecos[1]+taille_case*5/6),(tilecos[0]+taille_case*5/6),(tilecos[1]+taille_case*2/6),\
                fill=self.chef.player.couleur, tags=["village"], outline="black")

        self.croix =\
            canevas.create_line(tilecos[0]+taille_case/2,tilecos[1]+2.5*taille_case/8,tilecos[0]+taille_case/2,tilecos[1]+taille_case*6/8, fill="", width=2),\
            canevas.create_line(tilecos[0]+taille_case/4,tilecos[1]+taille_case/2,tilecos[0]+taille_case*3/4,tilecos[1]+taille_case/2, fill="", width=2)
         
    def redraw(self):
        super().redraw()

        canevas.itemconfig(self.maison, fill=self.chef.player.couleur)
        
        if self.a_eglise:
            couleur= 'black' if self.chef.player.couleur != 'black' else 'white'
            canevas.itemconfig(self.croix[0], fill=couleur)
            canevas.itemconfig(self.croix[1], fill=couleur)






## initialisation

def genere_carte(bruit: list[list[float]], seuils: dict[int, tuple[str, str]]):
    carte: list[list[Case]] = []

    for i in range(len(bruit)):
        ligne = []
        for j in range(len(bruit[i])):
            elevation = max(0, min(255, int((bruit[i][j]+0.5)*255)))

            terrain = argmax(seuils)
            for seuil in seuils:
                if elevation < seuil:
                    terrain = seuils[seuil]
                    break

            case = Case((i, j), terrain)
            ligne.append(case)
        carte.append(ligne)

    return carte



bruit = generate_perlin_grid(grille_w, grille_h, 16, 1.5)
carte = genere_carte(bruit, seuils)
carte_coords = canevas.create_text(6, 2, anchor="nw")