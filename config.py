from tkinter import Tk, Frame, Canvas




carte_w, carte_h = 112, 84

# traque l'origine et la taille des cases (obligé à cause du z##m)
taille_case = 35.
o_x, o_y = 0., 0.

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




fenetre_w, fenetre_h = 1200, 800
canevas_w, canevas_h = 1000, 750
ui_couleur = "lavender"

w = Tk()
w.resizable(False, False)

header = Frame(w, width=fenetre_w, height=fenetre_h-canevas_h, bg=ui_couleur)
header.pack_propagate(False)

canevas = Canvas(w, width=canevas_w, height=canevas_h, bg="white", highlightthickness=0) #scrollregion=(0, 0, carte_w*taille_case, carte_h*taille_case)
canevas.focus_set()

panneau = Frame(w, width=fenetre_w-canevas_w, height=canevas_h, bg=ui_couleur)
panneau.pack_propagate(False)

header.grid(column=0, row=0, columnspan=2)
canevas.grid(column=0, row=1)
panneau.grid(column=1, row=1)