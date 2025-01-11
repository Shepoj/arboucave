import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess
from typing import TYPE_CHECKING

import actions
import math
import random
import config

from projet import Player
from carte import Case, Village
from actions import guerre, creer_village
from divers import bouton_autodestruction

from gfx import Case_gfx, Village_gfx, carte

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


def create_players(case: Case_gfx):
    global player, ui
    v = Village_gfx(case, "lime")
    x, y = case.coords
    carte[x][y] = v
    player = Player("lime", v, True)
    players.append(player)
    ui.player = player

    couleurs = ["gray", "sky blue", "black", "yellow", "purple", "orange", "pink", "saddle brown", "white"]
    for couleur in couleurs:
        x, y = random.randint(1, carte_w-1), random.randint(1, carte_h-1)
        case = carte[x][y]
        if case.controle:
            continue

        v = Village_gfx(case, couleur)
        carte[x][y] = v
        p = Player(couleur, v, False)
        players.append(p)

    #newTurn()





def on_enter(x: int, y: int):
    case = carte[x][y]
    case.hover(False)

    if player is None:
        canevas.bind('<Button-1>', lambda _, case=case: create_players(case))
    else:
        canevas.bind('<Button-1>', lambda _, case=case: on_click(case))
    

def on_leave(x: int, y: int):
    case = carte[x][y]
    case.hover(True)
    canevas.unbind("<Button-1>")


def on_click(case: Case_gfx):
    ui.update_panneau(case)

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

    if village in player.fief and village != player.village:
        bouton = bouton_autodestruction(panneau, "Collecter les impôts\n(coût 1 ⓐ)", lambda: impositionSeigneur(village.chef, player))
        bouton.pack()
        if player.actions<1:
            bouton.config(state='disabled')

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






def build_bouton(case: Case):
    if case.controle in player.fief and not isinstance(case, Village) and not case.construite:
        bouton = bouton_autodestruction(panneau, "Construire sur cette case\n(coût 25 ⁂, 25 ¤, 1 ⓐ)", lambda: build_case(case))
        bouton.pack()
        if player.actions < 1 or player.village.chef.ressources < 25 or player.village.chef.argent < 25:
            bouton.config(state='disabled')

def build_case(case: Case):
    case.construire()
    player.actions += -1
    update_header()





def showRecruitButton(i,j,player):
    location=carte[i][j]
    if location.controle in player.fief and location.caseType=="village":
        recruitButton=tk.Button(panneau, text="Recruter un soldat\n(coût 1 ⓐ, 10 ¤)", command=lambda: useRecruitButton(player, location))
        recruitButton.pack()
        if player.actions<1 or player.village.chef.argent<10:
            recruitButton.config(state='disabled')

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

def useRecruitButton(player, loc):
    village = loc.controle
    actions.recruterSoldat(player, village)
    update_header()
    for child in panneau.winfo_children():
        if "Recruter un soldat\n(coût 1 ⓐ, 10 ¤)" in child.cget("text"):
            child.destroy()
    if player.j1:
        village_info(loc)

def drawBuilding(i,j,player):
    taille_case = config.taille_case
    tile=carte[i][j].tk_case
    tilecos=canevas.coords(tile)
    draw_gear(canevas, tilecos[0]+config.taille_case/2, tilecos[1]+taille_case/2, taille_case/4, 4, taille_case/5, player.couleur)


def impositionSeigneur(vassal, player):
    vassal.imposition_seigneur()
    player.actions-=1
    update_header()
    for child in panneau.winfo_children():
            if "Collecter les impôts\n(coût 1 ⓐ)" in child.cget("text"):
                child.destroy()

def showEndTurnButton():
    endTurnButton=tk.Button(panneau, text="Fin de tour", command=endTurns)
    endTurnButton.pack(side='bottom')
    

def draw_gear(canevas, x, y, radius, num_teeth, tooth_size, color):
    canevas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="black", width=2, fill=color)
    angle_step = 360 / num_teeth
    for i in range(num_teeth):
        angle = math.radians(i * angle_step)
        next_angle = math.radians((i + 1) * angle_step)
        inner_x1 = x + radius * math.cos(angle)
        inner_y1 = y + radius * math.sin(angle)
        inner_x2 = x + radius * math.cos(next_angle)
        inner_y2 = y + radius * math.sin(next_angle)
        outer_x1 = x + (radius + tooth_size) * math.cos(angle)
        outer_y1 = y + (radius + tooth_size) * math.sin(angle)
        outer_x2 = x + (radius + tooth_size) * math.cos(next_angle)
        outer_y2 = y + (radius + tooth_size) * math.sin(next_angle)
        canevas.create_polygon(inner_x1, inner_y1, outer_x1, outer_y1, outer_x2, outer_y2, inner_x2, inner_y2, fill=color, outline="black")






    

def newTurn():
    global playing
    playing=0
    fun = random.randint(0,100)
    actions.doEvent(fun)
    random.shuffle(players)
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
        action = random.choice(all_actions)
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
                creer_village(carte[x][y], bot)
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