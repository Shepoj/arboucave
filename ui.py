from typing import Any, Callable
from tkinter import Label, Button, BooleanVar, Radiobutton

from carte import Ferme, Village
from gfx import Case_gfx, Village_gfx, carte
from projet import Player
from actions import capture, collecte_ressources, construire_eglise, construire_ferme, construire_village, fin_tour, immigration, imposition_seigneur, recruter_soldat
from divers import adjacent
from config import header, panneau, carte_w, carte_h, ui_couleur



class UI():
    def __init__(self):
        self.player: Player | None = None
        self.selected: Case_gfx | None = None

        self.sym_argent = "¤"
        self.sym_ressource = "⁂"
        self.sym_action = "ⓐ"

        # header
        self.argent =     Label(header, bg=ui_couleur)
        self.ressources = Label(header, bg=ui_couleur)
        self.actions =    Label(header, bg=ui_couleur)
        self.argent.pack    (side="left")
        self.ressources.pack(side="left")
        self.actions.pack   (side="left")

        self.update_header()

        # panneau
        self.case = Label(panneau, bg=ui_couleur)
        self.case.pack(side="top")

        self.village_info = Label(panneau, bg=ui_couleur)
        self.village_info.pack(side="top")

        self.capture =  Button(panneau, text=f"Annexer cette case\n(coût 1 {self.sym_action})")
        self.collecte = Button(panneau, text=f"Collecter les ressources\n(coût 2 {self.sym_action})")
        self.ferme =    Button(panneau, text=f"Construire sur cette case\n(coût 1 {self.sym_action}, 25 {self.sym_ressource}, 10 {self.sym_argent})")
        self.village =  Button(panneau, text=f"Construire un village\n(coût 1 {self.sym_action} 25 {self.sym_ressource})")
        self.capture.pack (side="top")
        self.collecte.pack(side="top")
        self.ferme.pack   (side="top")
        self.village.pack (side="top")

        self.eglise = Button(panneau, text=f"Construire une église\n(coût 1 {self.sym_action}, 10 {self.sym_ressource})")
        self.impots = Button(panneau, text=f"Collecter les impôts\n(coût 1 {self.sym_action})")
        self.soldat = Button(panneau, text=f"Recruter un soldat\n(coût 1 {self.sym_action}, 10 {self.sym_argent})")
        self.eglise.pack(side="top")
        self.impots.pack(side="top")
        self.soldat.pack(side="top")

        self.immigration_type = BooleanVar(value=True)
        self.paysans =  Radiobutton(panneau, text=f"Paysans (1 {self.sym_action})", bg=ui_couleur,
            variable=self.immigration_type, value=True, command=lambda: self.immigration_type.set(True))
        self.artisans = Radiobutton(panneau, text=f"Artisans (2 {self.sym_action})", bg=ui_couleur,
            variable=self.immigration_type, value=False, command=lambda: self.immigration_type.set(False))
        self.paysans.pack()
        self.artisans.pack()
        self.immigration = Button(panneau, text="Immigrer")
        self.immigration.pack()

        self.hide_case()
        self.hide_village()

        def f():
            fin_tour()
            self.update_header()
        self.tour = Button(panneau, text="Fin de tour", command=f)
        self.tour.pack(side="bottom")


    def update_apres[T: Case_gfx](self, bouton: Button, action: Callable[[T, Player], Any], case: T):
        assert self.player is not None

        def f(case: T, player: Player):
            action(case, player)
            self.update_header()
            self.update_panneau(*case.coords)

        bouton.config(command=lambda c=case, p=self.player: f(c, p))

    def update_header(self):
        if self.player is None:
            return
        
        self.argent.config    (text=f"      Argent: {self.player.village.chef.argent} {self.sym_argent}")
        self.ressources.config(text=f"      Ressources: {self.player.village.chef.ressources} {self.sym_ressource}")
        self.actions.config   (text=f"      Actions: {self.player.actions} {self.sym_action}")

    def update_panneau(self, x: int, y: int):
        self.case.config(text=f"Case {x}, {y}")

        # select
        if self.selected:
            self.selected.select()
        self.selected = carte[x][y]
        self.selected.select()

        case = carte[x][y]
        if self.player is not None and case.controle is self.player.village:
            if isinstance(case, Village_gfx):
                self.hide_case()
                self.update_village(case)
            else:
                self.hide_village()
                self.update_case(case)

    def update_case(self, case: Case_gfx):
        assert self.player is not None

        # capture
        if case.controle is None:
            x, y = case.coords
            b = False
            for i, j in adjacent((x, y), (0, 0), (carte_w, carte_h)).values():
                if carte[i][j].controle in self.player.fief:
                    b = True
                    break
        
            if b:
                self.capture.pack()
                if self.player.actions < 1:
                    self.capture.config(state="disabled")
                else:
                    self.update_apres(self.capture, capture, case)
            else:
                self.capture.pack_forget()
        else:
            self.capture.pack_forget()

        # collecte
        if case.controle is not None and case.controle.couleur == self.player.village.couleur:
            self.collecte.pack()
            if self.player.actions < 2:
                self.collecte.config(state="disabled")
            else:
                self.update_apres(self.collecte, collecte_ressources, case)
        else:
            self.collecte.pack_forget()

        # ferme
        if case.controle in self.player.fief and not isinstance(case, Ferme):
            self.ferme.pack()
            if self.player.actions < 1 or self.player.village.chef.ressources < 25 or self.player.village.chef.argent < 10:
                self.ferme.config(state="disabled")
            else:
                self.update_apres(self.ferme, construire_ferme, case)
        else:
            self.ferme.pack_forget()

        # village
        if case.controle in self.player.fief and not isinstance(case, Ferme):
            x, y = case.coords
            b = True
            for i in range(max(0, x-2), min(carte_w, x+2)):
                for j in range(max(0, y-2), min(carte_h, y+2)):
                    if isinstance(carte[i][j], Village) and carte[i][j].controle is case.controle:
                        b = False
                        break
            if b:
                self.village.pack()
                if self.player.actions < 1 or self.player.village.chef.ressources < 25:
                    self.village.config(state="disabled")
                else:
                    self.update_apres(self.village, construire_village, case)
            else:
                self.village.pack_forget()
        else:
            self.village.pack_forget()

    def hide_case(self):
        self.capture.pack_forget()
        self.collecte.pack_forget()
        self.ferme.pack_forget()
        self.village.pack_forget()

    def update_village(self, village: Village_gfx):
        assert self.player is not None
        
        # info
        info = f"Chef : {village.chef}\n"
        if village is self.player.village:
            info += "(votre village)\n"
        elif village in self.player.fief:
            info += "(vassal de votre village)\n"
        if village.a_eglise:
            info += "Possède une église\n"
        info += f"Habitants : {len(village.habitants)}/{village.max_habitants}\n"

        if village in self.player.fief:
            info += f"Votre armée : {self.player.armee}\n"
        else:
            info += f"Armée du village : {village.armee}\n"

        self.village_info.config(text=info)

        # eglise
        if not village.a_eglise:
            self.eglise.pack()
            if self.player.actions < 1 or self.player.village.chef.ressources < 10:
                self.eglise.config(state="disabled")
            else:
                self.update_apres(self.eglise, construire_eglise, village)
        else:
            self.eglise.pack_forget()

        # impots seigneur
        if village is not self.player.village:
            self.impots.pack()
            if self.player.actions < 1:
                self.impots.config(state="disabled")
            else:
                self.update_apres(self.impots, imposition_seigneur, village)
        else:
            self.impots.pack_forget()

        # recrutement soldat
        if len(village.habitants) + 1 <= village.max_habitants:
            self.soldat.pack()
            if self.player.actions < 1 or self.player.village.chef.argent < 10:
                self.soldat.config(state="disabled")
            else:
                self.update_apres(self.soldat, recruter_soldat, village)
        else:
            self.soldat.pack_forget()

        # immigration        
        if len(village.habitants) + 3 <= village.max_habitants:
            self.paysans.pack()
            self.artisans.pack()
            self.immigration.pack()
            if self.player.actions < 1:
                self.immigration.config(state="disabled")
            else:
                self.update_apres(self.immigration, lambda v, p: immigration(v, p, self.immigration_type.get()), village)
        else:
            self.paysans.pack_forget()
            self.artisans.pack_forget()
            self.immigration.pack_forget()

    def hide_village(self):
        self.village_info.config(text="")
        self.eglise.pack_forget()
        self.impots.pack_forget()
        self.soldat.pack_forget()
        self.paysans.pack_forget()
        self.artisans.pack_forget()
        self.immigration.pack_forget()



ui = UI()