import tkinter as tk

win = tk.Tk()

donnees=tk.Frame(win, width=1182, height=40, bg='gray')
canevas=tk.Canvas(win, width=982, height=737, bg='white')
panneau=tk.Frame(win, width=200, height=737, bg='gray')
panneau.pack_propagate(False)
donnees.pack_propagate(False)

taillecase = 35