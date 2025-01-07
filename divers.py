from typing import Any, Callable
from tkinter import Button
from config import win, panneau

type point[T] = tuple[T, T]
type rgb = tuple[int, int, int]



def argmax[T](d: dict[int, T]):
    # élément avec la plus grand clé
    m = list(d.keys())[0]
    for key in d:
        if key > m:
            m = key
    return d[m]
    


def str_to_rgb(couleur: str) -> rgb:
    return tuple(c//256 for c in win.winfo_rgb(couleur))

def mix_couleurs(a: str, b: str):
    a = str_to_rgb(a)
    b = str_to_rgb(b)

    final = "#"
    for ca, cb in zip(a, b):
        aadd = str(hex((ca + cb)//2))[-2:]
        if aadd.startswith("x"):
            aadd = "0" + aadd[1:]
        final += aadd
    
    return final



def bords_case[T](wn: point[T], se: point[T]):
    x1, y1 = wn
    x2, y2 = se

    return {
        "w": ((x1, y1), (x1, y2)),
        "s": ((x1, y2), (x2, y2)),
        "e": ((x2, y2), (x2, y1)),
        "n": ((x2, y1), (x1, y1))
    }



def adjacent(p: point[int], m: point[int], M: point[int]):
    d: dict[str, point[int]] = {}

    x, y = p
    mx, my = m
    Mx, My = M
    if x > mx:
        d["w"] = (x-1, y)
    if y > my:
        d["n"] = (x, y-1)
    if x < Mx:
        d["e"] = (x+1, y)
    if y < My:
        d["s"] = (x, y+1)

    return d



def bouton_autodestruction(texte: str, f: Callable[[], Any]):
    # appuyer un bouton le détruit
    magie = [None]
    
    def command():
        f()
        magie[0].destroy()
    bouton = Button(panneau, text=texte, command=command)
    magie = [bouton]

    # petite surprise si on utilise une référence au bouton après sa destruction
    return bouton



def l_bouton_autodestruction(l_texte: str, l_f: list[Callable[[], Any]]):
    # activer un bouton les détruits tous
    magie: list[Button] = []

    for i in range(len(l_f)):
        f = l_f[i]
        def command():
            f()
            for bouton in magie:
                bouton.destroy()
        
        bouton = Button(panneau, text=l_texte[i], command=command)
        magie.append(bouton)
    
    return magie