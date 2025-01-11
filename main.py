import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess
from typing import TYPE_CHECKING

import config
import actions

from random import randint, choice, shuffle
from projet import Player
from carte import Case
from actions import guerre, construire_village
from divers import bouton_autodestruction

from gfx import Village_gfx, carte

from config import w, canevas, panneau, carte_w, carte_h
from ui import UI


if TYPE_CHECKING:
    player: Player
else:
    player = None
players: list[Player] = []
playing = 0
ui = UI()





def start_game():
    canevas.bind("<KP_Add>",      lambda e: zoom(e, 0.1))
    canevas.bind("<KP_Subtract>", lambda e: zoom(e, -0.1))

    #canevas.bind("<ButtonPress-2>", lambda event: canevas.scan_mark(event.x, event.y))
    canevas.bind("<ButtonPress-3>", lambda e: canevas.scan_mark(e.x, e.y))
    #canevas.bind("<B2-Motion>", lambda e: canevas.scan_dragto(e.x, e.y, gain=1))
    canevas.bind("<B3-Motion>", lambda e: canevas.scan_dragto(e.x, e.y, gain=1))

    for x in range(carte_w):
        for y in range(carte_h):
            case = carte[x][y]
            canevas.tag_bind(case.tag, '<Enter>', lambda _, x=x, y=y: on_enter(x, y))
            canevas.tag_bind(case.tag, '<Leave>', lambda _, x=x, y=y: on_leave(x, y))


def zoom(e: tk.Event, factor: float):
    x = canevas.canvasx(e.x)
    y = canevas.canvasy(e.y)
    canevas.scale("all", x, y, 1 + factor, 1 + factor)
    
    config.taille_case *= 1 + factor
    config.o_x += (config.o_x - x)*factor
    config.o_y += (config.o_y - y)*factor


def create_players(x: int, y: int):
    global player, ui
    v = Village_gfx(carte[x][y], "lime")
    carte[x][y] = v
    player = Player("lime", v, True)
    players.append(player)
    ui.player = player

    couleurs = ["gray", "sky blue", "black", "yellow", "purple", "orange", "pink", "saddle brown", "white"]
    for couleur in couleurs:
        x, y = randint(1, carte_w-1), randint(1, carte_h-1)
        case = carte[x][y]
        if case.controle:
            continue

        v = Village_gfx(case, couleur)
        carte[x][y] = v
        p = Player(couleur, v, False)
        players.append(p)

    #newTurn()





def on_enter(x: int, y: int):
    carte[x][y].hover(False)
    if player is None:
        canevas.bind('<Button-1>', lambda _, x=x, y=y: create_players(x, y))
    else:
        canevas.bind('<Button-1>', lambda _, x=x, y=y: on_click(x, y))
    

def on_leave(x: int, y: int):
    carte[x][y].hover(True)
    canevas.unbind("<Button-1>")


def on_click(x: int, y: int):
    ui.update_panneau(x, y)

    #village_info(case)
    #build_bouton(case)

    #showImmigrationButton(i,j,player)
    #showRecruitButton(i,j,player)
    #showEndTurnButton()




def update_header():
    if ui is not None:
        ui.update_header()





def village_info(case: Case):
    village = case.controle
    if village is None:
        return


    #guerre
    if village.couleur != player.couleur:
        def f(): 
            player.actions += -3
            if True:#guerre(player, village.player):
                update_header()
                winCheck()
            else:
                print("Vous avez perdu")
                response = messagebox.askquestion("Game Over", "Vous avez perdu. Voulez-vous recommencer une partie ?")
                if response == 'yes':
                    w.destroy()
                    subprocess.call(["python3", "./main.py"])
                    return
                else:
                    w.destroy()
                    return
        
        bouton = bouton_autodestruction(panneau, "Guerroyer", f)
        bouton.pack()
        if player.actions < 3 or player.armee == 0:
            bouton.config(state="disabled")












def showImmigrationButton(i,j,player):
    location=carte[i][j]
    if location.controle in player.fief and location.caseType=="village":
        def setImmigrationType(var, type):
            var.set(type)

        immigrationType = tk.StringVar(value="Paysans")
        paysansButton = tk.Radiobutton(panneau, text="Paysans (1 ⓐ)", variable=immigrationType, value="Paysans", bg='gray', command=lambda: setImmigrationType(immigrationType, "Paysans"))
        artisansButton = tk.Radiobutton(panneau, text="Artisans (2 ⓐ)", variable=immigrationType, value="Artisans", bg='gray', command=lambda: setImmigrationType(immigrationType, "Artisans"))
        paysansButton.pack()
        artisansButton.pack()
        immigrationButton=tk.Button(panneau, text="Immigrer", command=lambda: useImmigrationButton(player, location, immigrationType))
        immigrationButton.pack()
        if player.actions<1:
            immigrationButton.config(state='disabled')

def useImmigrationButton(player, loc, immigrationType):
    village = loc.controle
    actions.immigration(player, village, immigrationType.get() == "Paysans")
    update_header()
    if player.j1:
        for child in panneau.winfo_children():
            if "Immigrer" in child.cget("text"):
                child.destroy()
            elif "Paysans" in child.cget("text"):
                child.destroy()
            elif "Artisans" in child.cget("text"):
                child.destroy()
            elif "Recruter un soldat\n(coût 1 ⓐ, 10 ¤)" in child.cget("text"):
                child.destroy()
        village_info(loc)




def showEndTurnButton():
    endTurnButton=tk.Button(panneau, text="Fin de tour", command=endTurns)
    endTurnButton.pack(side='bottom')
    







    

def newTurn():
    global playing
    playing=0
    fun = randint(0,100)
    actions.doEvent(fun)
    shuffle(players)
    while playing<len(players):
        actions.villagerEachTurn(players[playing])
        actions.collecte_impots(players[playing])
        players[playing].actions=10
        if players[playing].j1:
            winCheck()
            if player.vaincu:
                print("Vous avez perdu")
                response = messagebox.askquestion("Game Over", "Vous avez perdu. Voulez-vous recommencer une partie ?")
                if response == 'yes':
                    w.destroy()
                    subprocess.call(["python3", "./main.py"])
                    break
                else:
                    w.destroy()
                    break
            if players[playing].j1:
                update_header()
            showEndTurnButton()
            return
        play(players[playing])
        playing+=1
            
def endTurns():
    global playing
    for child in panneau.winfo_children():
        child.destroy()
    playing+=1
    while playing<len(players):
        actions.villagerEachTurn(players[playing])
        actions.collecte_impots(players[playing])
        play(players[playing])
        playing+=1
    newTurn()

def play(bot):
    all_actions = ['capture', 'collecte', 'build', 'construire_eglise', 'guerre', 'creer_village', 'collecte_impots', 'recruter_soldat']
    while bot.actions > 0:
        action = choice(all_actions)
        if action == 'capture' and bot.actions>=1:
            cos=bot.botCapture(carte)
            if cos:
                x,y=cos
                #capture(carte[x][y], bot)
        elif action == 'collecte' and bot.actions>=2:
            if bot.botCollecte():
                bot.actions -= 2
        elif action == 'build' and bot.actions>=1 and bot.village.chef.ressources>=25 and bot.village.chef.argent>=25:
            buildTile = bot.botBuild()
            if buildTile:
                x, y = buildTile.coords
                #build_case(x, y, bot)
        elif action == 'construire_eglise':
            evangelisation = bot.botConstruireEglise() 
            if evangelisation:
                pass#useEgliseButton(evangelisation)

        elif action == 'creer_village' and bot.actions>=1 and bot.village.chef.ressources>=10: 
            villageloc = bot.botCreerVillage(carte)
            if villageloc:
                x, y = villageloc.coords
                construire_village(carte[x][y], bot)
        elif action == 'collecte_impots' and bot.actions>=1:
            bot.botCollecteImpots()
            bot.actions -= 1
        elif action == 'recruter_soldat' and bot.actions>=1 and bot.village.chef.argent>=10:
            bot.botRecruterSoldat()
            bot.actions -= 1
        elif action == 'guerre' and bot.actions>=3 and bot.armee > 0:
            adv = bot.botGuerre(players)
            if adv:
                village=adv.village
                winner = guerre(bot, adv)
                if winner:
                    bot.actions -= 3
                else:
                    pass
        else:
            continue
    




def winCheck():
    checker=True
    for player in players:
        if player.fief and not player.j1:
            print('il reste des joueurs' + player.couleur)
            checker=False
    if checker:
        response = messagebox.askquestion("Game Over", "Vous avez gagné ! Voulez-vous recommencer une partie ?")
        if response == 'yes':
            w.destroy()
            subprocess.call(["python3", "./main.py"])
            return
        else:
            w.destroy()
            return




start_game()

w.resizable(False, False)
w.mainloop()