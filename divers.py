from typing import Any, Callable
from tkinter import Button, Misc
from config import w

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
    r, g, b = (c//256 for c in w.winfo_rgb(couleur))
    return (r, g, b)

def mix_couleurs(a: str, b: str):
    a_rgb = str_to_rgb(a)
    b_rgb = str_to_rgb(b)

    final = 0
    for a_c, b_c in zip(a_rgb, b_rgb):
        c = (a_c + b_c)//2
        final <<= 8
        final += c
    
    # https://docs.python.org/3/library/functions.html#format 
    return f"#{final:0{6}x}"



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



# toute classe ayant Once pour metaclasse est garantie d'avoir un seul appel de SON PROPRE __init__
# par instance (utile pour les sous classes qui se recoupent)

class Once(type):
    class_id = 0

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]):
        __init__ = namespace["__init__"]
        attr = f"{name}_{Once.class_id}"
        Once.class_id += 1

        def once(self, *args):
            if not hasattr(self, attr):
                setattr(self, attr, ())
                __init__(self, *args)

        namespace["__init__"] = once
        return super().__new__(cls, name, bases, namespace)