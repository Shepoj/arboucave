from typing import TYPE_CHECKING

import tkinter as tk



carte_w, carte_h = 112, 84

if TYPE_CHECKING:
    from projet import Player

    player: Player
    players: list[Player]
else:
    player = None
    Players = []



taille_case = 35

seuils = {
    32: "roche",
    210: "herbe",
    1_000: "eau"
}

couleur_terrain = {
    "roche": "gray",
    "herbe": "green",
    "eau": "dark slate blue"
}

directions = ("w", "s", "e", "n")



w = tk.Tk()

donnees=tk.Frame(w, width=1182, height=40, bg='gray')
donnees.pack_propagate(False)

canevas = tk.Canvas(w, width=982, height=737, bg='white')

panneau=tk.Frame(w, width=200, height=737, bg='gray')
panneau.pack_propagate(False)

donnees.grid(column=0, row=0, columnspan=2)
canevas.grid(column=0, row=1)
panneau.grid(column=1, row=1)