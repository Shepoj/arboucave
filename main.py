import tkinter as tk
import tkinter.messagebox as messagebox
import subprocess

import perlin
import actions
import math
import random

from projet import Player
from carte import Case, Village, carte, carte_coords
from actions import guerre, creer_village, construire_eglise
from divers import bouton_autodestruction, l_bouton_autodestruction

from config import *




#shape = (0.3,0.3)
#res = (84,112)
player: Player = None
players: list[Player] = []
playing=0

#perlin_noise = perlin.perlinGrid(-shape[0], -shape[1], shape[0], shape[1], res[0], res[1])






def start_game():
    canevas.bind("<MouseWheel>", do_zoom) 
    canevas.bind("<4>", do_zoom_in)
    canevas.bind("<5>", do_zoom_out) 

    canevas.bind("<ButtonPress-2>", lambda event: canevas.scan_mark(event.x, event.y))
    canevas.bind("<ButtonPress-3>", lambda event: canevas.scan_mark(event.x, event.y))
    canevas.bind("<B2-Motion>", lambda event: canevas.scan_dragto(event.x, event.y, gain=1))
    canevas.bind("<B3-Motion>", lambda event: canevas.scan_dragto(event.x, event.y, gain=1))

    for i in range(len(carte)):
        for j in range(len(carte[i])):
            case = carte[i][j]
            canevas.tag_bind(case.tk_fill, '<Enter>', lambda _, case=case: on_enter(case))
            canevas.tag_bind(case.tk_fill, '<Leave>', lambda _, case=case: on_leave(case))





def on_enter(case: Case):
    canevas.itemconfig(case.tk_fill, outline="red", width = 2)
    canevas.tag_raise(case.tk_fill, "all")

    canevas.itemconfig(carte_coords, text=f"{case}")

    if player is None:
        canevas.bind('<Button-1>', lambda _, case=case: create_players(case))
    else:
        canevas.bind('<Button-1>', lambda _, case=case: on_click(case))
    

def on_leave(case: Case):
    canevas.itemconfig(case.tk_fill, outline="")
    canevas.tag_lower(case.tk_fill)
    
    canevas.unbind('<Button-1>')


def on_click(case: Case):
    for child in panneau.winfo_children():
        child.destroy()
    
    x, y = case.coords
    squareData=tk.Label(panneau, text=f'Case {x}, {y}', bg='gray')
    squareData.pack(side="top")

    village_info(case)
    village_button(case)
    capture_button(case)

    showCollectButton(x,y,player)
    showEgliseButton(x,y,player)
    #showBuildButton(x,y,player)
    #showEndTurnButton()





def updateHeader():
    if player.j1:
        for child in donnees.winfo_children():
            child.destroy()

        money=tk.Label(donnees, text=f"      Argent: {player.village.chef.argent} ¤      ", bg='gray')
        money.pack(side="left")

        ressources=tk.Label(donnees, text=f"Ressources: {player.village.chef.ressources} ⁂", bg='gray')
        ressources.pack(side="left")

        ptAction=tk.Label(donnees, text=f"Points d\'action: {player.actions} ⓐ      ", bg='gray')
        ptAction.pack(side="right")





def village_info(case: Case):
    village = case.controle
    if village is None:
        return
    
    for child in panneau.winfo_children():
        child.destroy()

    i, j = case.coords
    
    label = tk.Label(panneau, text=f"Chef : {village.chef}", bg='gray')
    label.pack(side="top")
    if village == player.village:
        label.config(text=f"Chef : {village.chef}\n(votre village)")
    
    if village.a_eglise:
        label = tk.Label(panneau, text='Le village possède une église.', bg='gray')
        label.pack(side="top")
    
    label = tk.Label(panneau, text=f"Habitants : {len(village.habitants)}/{village.max_habitants}", bg='gray')
    label.pack(side="top")

    if village in player.fief:
        label = tk.Label(panneau, text=f"Votre armée : {player.armee}", bg='gray')
    else:
        label = tk.Label(panneau, text=f"Armée du village : {village.armee}", bg='gray')
    label.pack(side="top")

    if village in player.fief and village != player.village:
        label = tk.Label(panneau, text='Vassal de votre village.', bg='gray')
        label.pack(side="top")

        bouton = bouton_autodestruction("Collecter les impôts\n(coût 1 ⓐ)", lambda: impositionSeigneur(village.chef, player))
        bouton.pack()
        if player.actions<1:
            bouton.config(state='disabled')

    showImmigrationButton(i,j,player)
    showRecruitButton(i,j,player)
    showEndTurnButton()

    #guerre
    if village.chef.player != player:
        def f(): 
            player.actions += -3
            if guerre(player, village.chef.player):
                updateHeader()
                winCheck()
            else:
                print("Vous avez perdu")
                response = messagebox.askquestion("Game Over", "Vous avez perdu. Voulez-vous recommencer une partie ?")
                if response == 'yes':
                    win.destroy()
                    subprocess.call(["python3", "./main.py"])
                    return
                else:
                    win.destroy()
                    return
        
        bouton = bouton_autodestruction("Guerroyer", f)
        bouton.pack()
        if player.actions < 3 or player.armee == 0:
            bouton.config(state="disabled")





### capture (étendre territoire)

def capture_button(case: Case):
    x, y = case.coords
    if not case.controle:
        b = False
        if x > 0:
            b = b or carte[x-1][y].controle in player.fief
        if x < grille_w:
            b = b or carte[x+1][y].controle in player.fief
        if y > 0:
            b = b or carte[x][y-1].controle in player.fief
        if y < grille_h:
            b = b or carte[x][y+1].controle in player.fief

        if b:
            bouton = bouton_autodestruction("Annexer cette case\n(coût 1 ⓐ)", lambda: capture(case, player))
            bouton.pack()
            if player.actions < 1:
                bouton.config(state='disabled')
  
def capture(case: Case, player: Player):
    if case.sous_controle:
        return

    case.capture(player.village)
    player.actions += 1

    if player.j1:
        updateHeader()




    
def village_button(case: Case):
    i, j = case.coords

    minx, miny = max(0, i-2), max(0, j-2)
    maxx, maxy = min(grille_w, i+3), min(grille_h, j+3)
    aucun_village = True
    for x in range(minx, maxx):
        for y in range(miny, maxy):
            if isinstance(carte[x][y], Case):
                aucun_village = False
                break

    if aucun_village and case.controle is not None and case.controle in player.fief:
        bouton = bouton_autodestruction("Construire un village\n(coût 1 ⓐ, 10 ⁂)", lambda: Village(case, player))
        bouton.pack()

        if player.actions < 1 or player.village.chef.ressources < 10:
          bouton.config(state='disabled')





def showBuildButton(i,j,player):
    location=carte[i][j]
    if location.controle in player.fief and location.caseType!="village" and not location.built:
        buildButton=tk.Button(panneau, text="Construire sur cette case\n(coût 25 ⁂, 25 ¤, 1 ⓐ)", command=lambda: buildCase(i,j,player))
        buildButton.pack()
        if player.actions<1 or player.village.chef.ressources<25 or player.village.chef.argent<25:
            buildButton.config(state='disabled')

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



def showEgliseButton(i: int, j: int, player: Player):
    village = carte[i][j].controle
    
    # None not in player.fief
    if village in player.fief and not village.a_eglise:
        egliseButton = bouton_autodestruction("Construire une église\n(coût 1 ⓐ, 10 ⁂)", lambda: useEgliseButton(village, player))
        egliseButton.pack()
        if player.actions < 1 or player.village.chef.ressources < 10:
            egliseButton.config(state='disabled')

def useEgliseButton(village: Village, player):
    player = village.chef.player
    construire_eglise(village, player)
    village.redraw()

    i, j = village.coords
    if player.j1:
        updateHeader()
        showVillageInfo(i,j,player)



def useImmigrationButton(player, loc, immigrationType):
    village = loc.controle
    actions.immigration(player, village, immigrationType.get() == "Paysans")
    updateHeader()
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
        showVillageInfo(loc.coords[0], loc.coords[1], player)


def buildCase(i,j,player):
    location=carte[i][j]
    location.build()
    player.actions-=1
    updateHeader()
    drawBuilding(i,j,player)
    for child in panneau.winfo_children():
            if "Construire sur cette case\n(coût 25 ⁂, 25 ¤, 1 ⓐ)" in child.cget("text"):
                child.destroy()

def useRecruitButton(player, loc):
    village = loc.controle
    actions.recruterSoldat(player, village)
    updateHeader()
    for child in panneau.winfo_children():
        if "Recruter un soldat\n(coût 1 ⓐ, 10 ¤)" in child.cget("text"):
            child.destroy()
    if player.j1:
        showVillageInfo(loc.coords[0], loc.coords[1], player)

def drawBuilding(i,j,player):
    global taille_case
    tile=carte[i][j].tk_fill
    tilecos=canevas.coords(tile)
    draw_gear(canevas, tilecos[0]+taille_case/2, tilecos[1]+taille_case/2, taille_case/4, 4, taille_case/5, player.couleur)

def showCollectButton(i,j,player):
    location=carte[i][j]
    if location.controle in player.fief and location.caseType!="village":
        collectButton=tk.Button(panneau, text="Collecter les ressources\n(coût 2 ⓐ)", command=lambda: collectRessources(i,j,player))
        collectButton.pack()
        if player.actions<2:
            collectButton.config(state='disabled')

def collectRessources(i,j,player):
    location=carte[i][j]
    location.collecte()
    player.actions-=2
    updateHeader()
    for child in panneau.winfo_children():
            if "Collecter les ressources\n(coût 2 ⓐ)" in child.cget("text"):
                child.destroy()


def impositionSeigneur(vassal, player):
    vassal.imposition_seigneur()
    player.actions-=1
    updateHeader()
    for child in panneau.winfo_children():
            if "Collecter les impôts\n(coût 1 ⓐ)" in child.cget("text"):
                child.destroy()

def showEndTurnButton():
    for child in panneau.winfo_children():
        if "Fin de tour" in child.cget("text"):
            child.destroy()
    endTurnButton=tk.Button(panneau, text="Fin de tour", command=endTurns)
    endTurnButton.pack(side='bottom')
    

def updateCapturedOutline(player):
    for adelete in canevas.find_withtag('controleoutline*'+player):
        canevas.delete(adelete)
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            tile=carte[i][j].tk_fill
            tilecos=canevas.coords(tile)
            if 'controle' in canevas.gettags(tile):
                if 'controleby*'+player in canevas.gettags(tile):
                    if i==0:
                        canevas.create_line(tilecos[0],tilecos[1],tilecos[0],tilecos[3], fill=player, width=2, tags=['controleoutline*'+player])
                    else:
                        if 'controleby*'+player not in canevas.gettags(carte[i-1][j].tk_fill):
                            canevas.create_line(tilecos[0],tilecos[1],tilecos[0],tilecos[3], fill=player, width=2, tags=['controleoutline*'+player])
                    if j==0:
                        canevas.create_line(tilecos[0],tilecos[1],tilecos[2],tilecos[1], fill=player, width=2, tags=['controleoutline*'+player])
                    else: 
                        if 'controleby*'+player not in canevas.gettags(carte[i][j-1].tk_fill):
                            canevas.create_line(tilecos[0],tilecos[1],tilecos[2],tilecos[1], fill=player, width=2, tags=['controleoutline*'+player])
                    if i==len(carte)-1:
                        canevas.create_line(tilecos[2],tilecos[1],tilecos[2],tilecos[3], fill=player, width=2, tags=['controleoutline*'+player])
                    else:
                        if 'controleby*'+player not in canevas.gettags(carte[i+1][j].tk_fill):
                            canevas.create_line(tilecos[2],tilecos[1],tilecos[2],tilecos[3], fill=player, width=2, tags=['controleoutline*'+player])
                    if j==len(carte[i])-1:
                        canevas.create_line(tilecos[0],tilecos[3],tilecos[2],tilecos[3], fill=player, width=2, tags=['controleoutline*'+player])
                    else:
                        if 'controleby*'+player not in canevas.gettags(carte[i][j+1].tk_fill):
                            canevas.create_line(tilecos[0],tilecos[3],tilecos[2],tilecos[3], fill=player, width=2, tags=['controleoutline*'+player])


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





def do_zoom(event):
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    factor = 1.001 ** event.delta
    canevas.scale(tk.ALL, x, y, factor, factor)

def do_zoom_in(event):
    global taille_case
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    if taille_case<=70:
        factor = 1.1
        taille_case=taille_case*factor
        canevas.scale(tk.ALL, x, y, factor, factor) #https://stackoverflow.com/questions/48112492/canvas-scale-only-size-but-not-coordinates html
    

def do_zoom_out(event):
    global taille_case
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    if taille_case>=8:
        factor = 0.9
        taille_case=taille_case*factor
        canevas.scale(tk.ALL, x, y, factor, factor)

def test(event):
    print(canevas.canvasx(event.x),canevas.canvasy(event.y))





def create_players(case: Case):
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            canevas.unbind("<Button-1>")
            canevas.tag_bind(case.tk_fill, "<Enter>", lambda _, case=carte[i][j]: on_enter(case))
            canevas.tag_bind(case.tk_fill, "<Leave>", lambda _, case=carte[i][j]: on_leave(case))
    
    # peut etre associer player a son village des le debut
    global player
    player = Player("lime", None, True)
    player.village = Village(case, player)
    players.append(player)

    couleurs = ['red', 'sky blue', 'black', 'yellow', 'purple', 'orange', 'pink', 'brown', 'white']
    for i in range(9):
        x, y = random.randint(0,111), random.randint(0,83)
        case = carte[x][y]
        if case.controle:
            continue

        players.append(Player(couleurs[i], None, False))
        players[i+1].village = Village(case, players[i+1])
    newTurn()
    

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
                    win.destroy()
                    subprocess.call(["python3", "./main.py"])
                    break
                else:
                    win.destroy()
                    break
            if players[playing].j1:
                updateHeader()
            showEndTurnButton()
            return
        play(players[playing])
        updateCapturedOutline(players[playing].couleur)
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
        updateCapturedOutline(players[playing].couleur)
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
                capture(carte[x][y], bot)
        elif action == 'collecte' and bot.actions>=2:
            if bot.botCollecte():
                bot.actions -= 2
        elif action == 'build' and bot.actions>=1 and bot.village.chef.ressources>=25 and bot.village.chef.argent>=25:
            buildTile = bot.botBuild()
            if buildTile:
                x, y = buildTile.coords
                buildCase(x, y, bot)
        elif action == 'construire_eglise':
            evangelisation = bot.botConstruireEglise() 
            if evangelisation:
                useEgliseButton(evangelisation, bot)

        elif action == 'creer_village' and bot.actions>=1 and bot.village.chef.ressources>=10: 
            villageloc = bot.botCreerVillage(carte)
            if villageloc:
                x, y = villageloc.coords
                Village(carte[x][y], bot)
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
                    #repeindre_villages(village.chef.player.fief)
                    bot.actions -= 3
                else:
                    pass
                    #repeindre_villages(village.chef.player.fief)
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
            win.destroy()
            subprocess.call(["python3", "./main.py"])
            return
        else:
            win.destroy()
            return






start_game()

win.resizable(False,False)
win.mainloop()
