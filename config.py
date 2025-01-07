from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from carte import Case

import tkinter as tk



win = tk.Tk()

donnees=tk.Frame(win, width=1182, height=40, bg='gray')
donnees.pack_propagate(False)

canevas = tk.Canvas(win, width=982, height=737, bg='white')

panneau=tk.Frame(win, width=200, height=737, bg='gray')
panneau.pack_propagate(False)



donnees.grid(column=0,row=0,columnspan=2)
canevas.grid(column=0,row=1)
panneau.grid(column=1,row=1)



grille_w, grille_h = 112, 84
taille_case = 35

seuils = {
    32: "roche",
    210: "herbe",
    1_000: "eau"
}

couleur_terrain = {
    "roche": "gray",
    "herbe": "green",
    "eau": "blue"
}