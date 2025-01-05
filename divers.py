from typing import Any, Callable
from tkinter import Button
from config import panneau


def argmax[T](d: dict[int, T]):
    # élément avec la plus grand clé
    m = list(d.keys())[0]
    for key in d:
        if key > m:
            m = key
    return d[m]



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