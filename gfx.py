from __future__ import annotations

import config

from math import radians, cos, sin
from carte import Case, Ferme, Village

from config import canevas, couleur_terrain, carte_w, carte_h, seuils, directions
from divers import point, mix_couleurs, argmax, adjacent
from perlin import generate_perlin_grid



grille: list[list[list[int | None]]] = [[[None, None] for _ in range(carte_h+1)] for _ in range(carte_w+1)]



class Case_gfx(Case):
    def __init__(self, coords: point[int], terrain: str):
        Case.__init__(self, coords, terrain)

        x, y = self.coords
        self.tag = f"{x} {y}"
        self.selected = False

        self.draw()
 
    def capture(self, village: Village):
        Case.capture(self, village)
        self.redraw()

    @property
    def coords_canevas(self):
        x, y = self.coords
        return config.o_x + x*config.taille_case, config.o_y + y*config.taille_case

    @property
    def cases_voisines(self):
        return {d: carte[x][y] for d, (x, y) in adjacent(self.coords, (0, 0), (carte_w-1, carte_h-1)).items()}

    @property
    def bords_coord(self):
        x, y = self.coords
        return {
            "w": (x  , y  , 1),
            "s": (x  , y+1, 0),
            "e": (x+1, y  , 1),
            "n": (x  , y  , 0)
        }

    # TODO enum pour directions
    def bord(self, d: str):
        x, y = self.coords_canevas
        t = config.taille_case
        match d:
            case "w": return x  , y  , x  , y+t
            case "s": return x  , y+t, x+t, y+t
            case "e": return x+t, y+t, x+t, y
            case "n": return x+t, y  , x  , y
        raise ValueError

    def hover(self, after: bool):
        if self.selected:
            return

        outline = "" if after else "red"
        canevas.tag_raise(self.tk_hover)
        canevas.itemconfig(self.tk_hover, outline=outline, dash=())

    def select(self):
        if self.selected:
            self.selected = False
            outline = ""
        else:
            self.selected = True
            outline = "red"
        canevas.itemconfig(self.tk_hover, outline=outline, dash=(5, 5))
 
    def draw(self):
        self.draw_case()
        self.draw_bords()

    def redraw(self):
        self.redraw_case()
        self.redraw_bords()

    def draw_case(self):
        x, y = self.coords_canevas
        t = config.taille_case

        self.tk_case =\
            canevas.create_rectangle(x, y, x+t, y+t,\
                outline="", width=2, tags=[self.tag, "case"])

        self.tk_hover =\
            canevas.create_rectangle(x, y, x+t, y+t,\
                outline="", width=2, tags=[self.tag, "hover"])

        self.redraw_case()

    def redraw_case(self):
        couleur = couleur_terrain[self.terrain]
        if self.controle:
            couleur = mix_couleurs(couleur, self.controle.couleur)
    
        canevas.itemconfig(self.tk_case, fill=couleur)

    def draw_bords(self):
        self.redraw_bords()

    def redraw_bords(self):
        if self.controle is None:
            return
        couleur = self.controle.couleur

        for d, case in self.cases_voisines.items():
            x, y, i = self.bords_coord[d]
            bord = grille[x][y][i]

            if case.controle is self.controle:
                if bord is not None:
                    canevas.delete(bord)
                continue

            if bord is None:
                bord = canevas.create_line(*self.bord(d), width=2, tags=[self.tag, case.tag, "bord"])
                grille[x][y][i] = bord

            dash = (5,5) if case.controle is not None and case.controle.couleur == self.controle.couleur else ()
            canevas.itemconfig(bord, fill=couleur, dash=dash)
        canevas.tag_raise(self.tk_hover)





class Ferme_gfx(Ferme, Case_gfx):
    def __init__(self, case: Case_gfx, couleur: str):
        Ferme.__init__(self, case, couleur)
        Case_gfx.__init__(self, case.coords, case.terrain)

        canevas.delete(case.tk_case)
        canevas.delete(case.tk_hover)

    def draw(self):
        Case_gfx.draw(self)
        self.draw_ferme()
    
    def redraw(self):
        Case_gfx.redraw(self)
        self.redraw_ferme()

    def draw_ferme(self):
        if not self.controle:
            return
        couleur = self.controle.couleur

        x, y = self.coords_canevas
        t = config.taille_case
        x, y = x + 1/2*t, y + 1/2*t

        self.tk_ferme: list[int] = []

        n = 5
        r, s = 1/4*t, 1/5*t
        pas = radians(360/n)
        for i in range(n):
            a = x +  r   *cos( i   *pas), y + r    *sin( i   *pas)
            b = x +  r   *cos((i+1)*pas), y + r    *sin((i+1)*pas)
            c = x + (r+s)*cos((i+1)*pas), y + (r+s)*sin((i+1)*pas)
            d = x + (r+s)*cos( i   *pas), y + (r+s)*sin( i   *pas)
            X = canevas.create_polygon(*a, *b, *c, *d, fill=couleur, outline="black", tags=[self.tag, "ferme"])
            self.tk_ferme.append(X)

    def redraw_ferme(self):
        if not self.controle:
            return
        couleur = self.controle.couleur

        for X in self.tk_ferme:
            canevas.itemconfig(X, fill=couleur)





class Village_gfx(Village, Case_gfx):
    def __init__(self, case: Case_gfx, couleur: str):
        Village.__init__(self, case, couleur)
        Case_gfx.__init__(self, case.coords, case.terrain)

        canevas.delete(case.tk_case)
        canevas.delete(case.tk_hover)
    
    def construire_eglise(self):
        Village.construire_eglise(self)
        self.redraw()
        
    def draw(self):
        Case_gfx.draw(self)
        self.draw_maison()

    def redraw(self):
        Case_gfx.redraw(self)
        self.redraw_maison()

    def draw_maison(self):
        x, y = self.coords_canevas
        t = config.taille_case

        self.tk_maison =\
            canevas.create_polygon(x+1/2*t, y+1/6*t, x+1/6*t, y+1/3*t, x+1/6*t, y+5/6*t, x+5/6*t, y+5/6*t, x+5/6*t, y+1/3*t,\
                outline="black", tags=[self.tag, "village"])
        
        # horizontal, vertical
        self.tk_croix =\
            canevas.create_line(x+1/3*t, y+0.45*t, x+2/3*t, y+0.45*t, width=2, tags=[self.tag]),\
            canevas.create_line(x+1/2*t, y+2.5/8*t, x+1/2*t, y+6/8*t, width=2, tags=[self.tag])
        
        self.redraw_maison()
    
    def redraw_maison(self):
        canevas.itemconfig(self.tk_maison, fill=self.couleur)

        if self.a_eglise:
            couleur = "white" if self.couleur == "black" else "black"
            for c in self.tk_croix:
                canevas.itemconfig(c, fill=couleur, state="normal")
        else:
            for c in self.tk_croix:
                canevas.itemconfig(c, state="hidden")





# initialisation

def genere_carte(bruit: list[list[float]], seuils: dict[int, str]) -> list[list[Case_gfx]]:
    carte = []

    for x in range(carte_w):
        ligne = []
        for y in range(carte_h):
            elevation = max(0, min(255, int((bruit[x][y]+0.5)*255)))

            terrain = argmax(seuils)
            for seuil in seuils:
                if elevation < seuil:
                    terrain = seuils[seuil]
                    break

            c = Case_gfx((x, y), terrain)
            ligne.append(c)
        carte.append(ligne)

    return carte

bruit = generate_perlin_grid(carte_w, carte_h, 16, 1.5)
carte = genere_carte(bruit, seuils)