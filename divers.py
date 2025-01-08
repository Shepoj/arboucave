from typing import Any, Callable
from tkinter import Button, Misc
from config import w, panneau

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
    r, g, b = w.winfo_rgb(couleur)
    return (r//256, g//256, b//256)

def mix_couleurs(a: str, b: str):
    a_rgb = str_to_rgb(a)
    b_rgb = str_to_rgb(b)

    final = "#"
    for a_c, b_c in zip(a_rgb, b_rgb):
        aadd = str(hex((a_c + b_c)//2))[-2:]
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



def bouton_autodestruction(parent: Misc, texte: str, command: Callable[[], Any]):
    def f(self: Button):
        self.destroy()
        command()
    
    bouton = Button(parent, text=texte)
    bouton.config(command=lambda self=bouton: f(self))
    return bouton