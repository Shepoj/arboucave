from __future__ import annotations

from config import canevas, taille_case, couleur_terrain, grille_w, grille_h
from divers import point, mix_couleurs
from carte import Case, Village
from projet import Player





class Case_gfx(Case):
    def __init__(self, coords: point, terrain: str, *args, **kwargs):
        super().__init__(coords, terrain, *args, **kwargs)

        self.draw()

    # TODO enum pour directions
    def bord(self, d: str):
        x, y = self.coords
        t = taille_case
        match d:
            case "w": return  x   *t,  y   *t,  x   *t, (y+1)*t
            case "s": return  x   *t, (y+1)*t, (x+1)*t, (y+1)*t
            case "e": return (x+1)*t, (y+1)*t, (x+1)*t,  y   *t
            case "n": return (x+1)*t,  y   *t,  x   *t,  y   *t
        raise ValueError

    def grille_coords(self, d: str):
        x, y = self.coords
        match d:
            case "w": return (x  , y  )
            case "s": return (x  , y+1)
            case "e": return (x+1, y+1)
            case "n": return (x+1, y  )
        raise ValueError
    
    def draw(self):
        self.draw_case()
        self.draw_bords()

    def redraw(self):
        self.redraw_case()
        pass

    def draw_case(self):
        x, y = self.coords
        t = taille_case

        self.tk_case =\
            canevas.create_rectangle(x*t, y*t, (x+1)*t, (y+1)*t,\
                outline="", tags="case")

        self.redraw_case()

    def redraw_case(self):
        couleur = couleur_terrain[self.terrain]
        if self.controle:
            couleur = mix_couleurs(couleur, self.controle.chef.player.couleur)
    
        canevas.itemconfig(self.tk_case, fill=couleur)

    def draw_bords(self):
        self.redraw_bords()

    def redraw_bords(self):
        if not self.controle:
            return
        couleur = self.controle.chef.player.couleur

        for d, case in self.cases_voisines.items():
            x, y = self.grille_coords(d)

            if case.controle is self.controle and grille[x][y] is not None:
                canevas.delete(grille[x][y])
            
            else:
                if grille[x][y] is None:
                    grille[x][y] = canevas.create_line(*self.bord(d), width=2)
                else:
                    if case.controle.chef.player is self.controle.chef.player:
                        dash = (5, 5)
                    else:
                        dash = None
                canevas.itemconfig(grille[x][y], fill=couleur, dash=dash)





class Village_gfx(Case_gfx, Village):
    def __init__(self, case: Case, player: Player):
        super().__init__(coords=case.coords, terrain=case.terrain, case=case, player=player)

    def draw(self):
        super().draw()
        self.draw_maison()

    def draw_maison(self):
        x, y = self.coords
        t = taille_case

        self.tk_maison =\
            canevas.create_polygon((x+1/2)*t, (y+1/6)*t, (x+1/6)*t, (y+2/6)*t, (x+1/6)*t, (y+5/6)*t, (x+5/6)*t, (y+5/6)*t, (x+5/6)*t, (y+2/6)*t,\
                outline="black", tags="village")
        
        self.tk_croix =\
            canevas.create_line((x+1/2)*t, (y+2.5/8)*t, (x+1/2)*t, (y+6/8)*t, width=2),\
            canevas.create_line((x+1/4)*t, (y+1/2)*t, (x+3/4)*t, (y+1/2)*t, width=2)
        
        self.redraw_maison()
        
    
    def redraw_maison(self):
        canevas.itemconfig(self.tk_maison, fill=self.chef.player.couleur)

        couleur = "white" if self.chef.player.couleur == "black" else "black"
        for c in self.tk_croix:
            canevas.itemconfig(c, fill=couleur)





grille: list[list[int]] = [[None for _ in range(grille_h+1)] for _ in range(grille_w+1)]