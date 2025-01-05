import tkinter as tk
import perlin
import projet
import actions
import math
import random

from projet import Player, Village
from actions import guerre


shape = (0.3,0.3)
res = (84,112)
startpos=(0,0)
player=None
players=[]
playing=0

gx,gy=112,84

perlin_noise = perlin.generate_perlin_grid(84,112,16, 1.5)
#perlin_noise = perlin.perlinGrid(-shape[0], -shape[1], shape[0], shape[1], res[0], res[1])


win = tk.Tk()

donnees=tk.Frame(win, width=1182, height=40, bg='gray')
canevas=tk.Canvas(win, width=982, height=737, bg='white')
panneau=tk.Frame(win, width=200, height=737, bg='gray')
panneau.pack_propagate(False)
donnees.pack_propagate(False)



taillecase = 35
carte = []

for i in range(len(perlin_noise)):
    carte.append([])
    for j in range(len(perlin_noise[i])):
        
        couleur = max(0, min(255, int((perlin_noise[i][j]+0.5)*255)))
        test = canevas.create_rectangle(i*taillecase, j*taillecase, i*taillecase+taillecase, j*taillecase+taillecase, fill='gray' if couleur < 32 else 'green' if couleur < 210 else 'blue', outline='black')
        terrain = 'roche' if couleur < 32 else 'herbe' if couleur < 210 else 'eau'
        if couleur < 32:
            canevas.itemconfig(test, tags=['roche'])
        elif couleur < 210:
            canevas.itemconfig(test, tags=['herbe'])
        else:
            canevas.itemconfig(test, tags=['eau'])
        tile=projet.Case((i,j),test,terrain)
        carte[i].append(tile)


print(len(carte), len(carte[0]))

def on_enter(event, item):
    canevas.itemconfig(item.tkItem, outline='red', width = 2)
    canevas.tag_raise(item.tkItem,"all")
    #canevas.tag_raise("village")

    canevas.bind('<Button-1>', lambda event, item=item : on_click(item.coords))


def on_leave(event, item):
    canevas.itemconfig(item.tkItem, outline='black', width = 1)
    canevas.tag_lower(item.tkItem)
    
    canevas.unbind('<Button-1>')
    outlineontop()

def on_click(event):
    global player
    for child in panneau.winfo_children():
        child.destroy()
    x = event[0]
    y = event[1]
    squareData=tk.Label(panneau, text='Case '+str(x)+', '+str(y), bg='gray')
    squareData.pack(side="top")
    showVillageButton(x,y,player)
    showCaptureButton(x,y,player)
    showVillageInfo(x,y,player)
    showRecruitButton(x,y,player)
    showCollectButton(x,y,player)
    showBuildButton(x,y,player)
    showEndTurnButton()
    
def updateHeader(player):
    if player.j1:
        for child in donnees.winfo_children():
            child.destroy()
        money=tk.Label(donnees, text='Argent: '+str(player.village.chef.argent) + " ¤      ", bg='gray')
        money.pack(side="left")
        ressources=tk.Label(donnees, text='Ressources: '+str(player.village.chef.ressources) + " ⁂", bg='gray')
        ressources.pack(side="left")
        ptAction=tk.Label(donnees, text='Points d\'action: '+str(player.actions) + " ⓐ", bg='gray')
        ptAction.pack(side="right")
    
def outlineontop():
    pass
        
def capture(i,j,player, init=False):
    coul = canevas.itemcget(carte[i][j].tkItem, 'fill')
    if 'captured' in canevas.gettags(carte[i][j].tkItem):
        return
    color = tuple((c//256 for c in win.winfo_rgb(coul)))
    playcolor = tuple((c//256 for c in win.winfo_rgb(player.couleur)))
    final='#'
    for val in range(3):
        aadd=str(hex((color[val]+playcolor[val])//2))[-2:]
        if aadd.startswith('x'):
            aadd='0'+aadd[1:]
        final+=aadd
    canevas.itemconfig(carte[i][j].tkItem, fill=final, tags=list(canevas.gettags(carte[i][j].tkItem))+['captured', 'capturedby*'+player.couleur])
    carte[i][j].capture(player.village)
    if not init:
        player.actions-=1
    updateCapturedOutline(player.couleur)
    if player.j1:
        updateHeader(player)
        for child in panneau.winfo_children():
                if "Annexer cette case\n(coût 1 ⓐ)" in child.cget("text"):
                    child.destroy()
    

def drawVillage(i,j,player,init=False):
    global taillecase
    if not init:
        village=actions.creer_village(carte[i][j],player)
        village.chef.vassalisation(player.village.chef)
        updateHeader(player)
        for child in panneau.winfo_children():
            if "Construire un village\n(coût 1 ⓐ, 10 ⁂)" in child.cget("text"):
                child.destroy()
            elif "Collecter les ressources\n(coût 2 ⓐ)" in child.cget("text"):
                child.destroy()
    tile=carte[i][j].tkItem
    tilecos=canevas.coords(tile)
    canevas.create_polygon((tilecos[0]+taillecase/2),(tilecos[1]+taillecase/6),(tilecos[0]+taillecase/6),(tilecos[1]+taillecase*2/6),(tilecos[0]+taillecase/6),(tilecos[1]+taillecase*5/6),(tilecos[0]+taillecase*5/6),(tilecos[1]+taillecase*5/6),(tilecos[0]+taillecase*5/6),(tilecos[1]+taillecase*2/6), outline='black',fill=player.couleur,tags=["village"])

def captureButton(i,j,player):
    bouton=tk.Button(panneau, text="Annexer cette case\n(coût 1 ⓐ)", command=lambda: capture(i,j,player))
    bouton.pack()
    if player.actions<1:
        bouton.config(state='disabled')

def villageButton(i,j,player):
    global gx,gy
    tile=carte[i][j]
    minx,miny=max(0,i-2),max(0,j-2)
    maxx,maxy=min(gx,i+3),min(gy,j+3)
    isVillage=False
    for x in range(minx,maxx):
        for y in range(miny,maxy):
            if carte[x][y].caseType=="village":
                isVillage=True
    if not isVillage and carte[i][j].master in player.fief:
        bouton=tk.Button(panneau, text="Construire un village\n(coût 1 ⓐ, 10 ⁂)", command=lambda: drawVillage(i,j,player))
        bouton.pack()
        if player.actions<1 or player.village.chef.ressources<10:
            bouton.config(state='disabled')
            


def repeindre_villages(villages: list[Village]):
    print("repeindre")
    for village in villages:
        drawVillage(*village.coords, village.chef.player, True)

def showVillageInfo(i,j,player: Player):
    village=carte[i][j].master
    if village==None:
        return
    villageChief=carte[i][j].master.chef
    villageInfo=tk.Label(panneau, text='Chef : ' + villageChief.affiche_nom(), bg='gray')
    villageInfo.pack(side="top")
    if villageChief == player.village.chef:
        villageInfo.config(text='Chef : ' + villageChief.affiche_nom() + '\n(votre village)')
    if village.hasEglise:
        egliseInfo=tk.Label(panneau, text='Le village possède une église.', bg='gray')
        egliseInfo.pack(side="top")
    if village in player.fief and villageChief != player.village.chef:
        vassalInfo=tk.Label(panneau, text='Vassal de votre village.', bg='gray')
        vassalInfo.pack(side="top")
        impotButton=tk.Button(panneau, text="Collecter les impôts\n(coût 1 ⓐ)", command=lambda: impositionSeigneur(villageChief, player))
        impotButton.pack()
        if player.actions<1:
            impotButton.config(state='disabled')
 
    if village in player.fief:
        habitants_info = tk.Label(panneau, text=village.info_habitants(), bg="gray")
        habitants_info.pack(side="top")

    #guerre
    if village.chef.player != player:
        bouton = [None]
        def f(): 
            if guerre(player, village.chef.player):
                repeindre_villages(village.chef.player.fief)
            bouton[0].destroy()
        
        bouton_guerre = tk.Button(panneau, text="Guerroyer", command=f)
        bouton = [bouton_guerre]
        bouton_guerre.pack()
        if False and player.armee == 0:
            bouton_guerre.config(state="disabled")

def showBuildButton(i,j,player):
    location=carte[i][j]
    if location.master in player.fief and location.caseType!="village" and not location.built:
        buildButton=tk.Button(panneau, text="Construire sur cette case\n(coût 25 ⁂, 25 ¤, 1 ⓐ)", command=lambda: buildCase(i,j,player))
        buildButton.pack()
        if player.actions<1 or player.village.chef.ressources<25 or player.village.chef.argent<25:
            buildButton.config(state='disabled')

def showRecruitButton(i,j,player):
    location=carte[i][j]
    if location.master in player.fief and location.caseType=="village":
        recruitButton=tk.Button(panneau, text="Recruter un soldat\n(coût 1 ⓐ, 10 ¤)", command=lambda: useRecruitButton(player, location))
        recruitButton.pack()
        if player.actions<1 or player.village.chef.argent<10:
            recruitButton.config(state='disabled')

def buildCase(i,j,player):
    location=carte[i][j]
    location.build()
    player.actions-=1
    updateHeader(player)
    drawBuilding(i,j,player)
    for child in panneau.winfo_children():
            if "Construire sur cette case\n(coût 25 ⁂, 25 ¤, 1 ⓐ)" in child.cget("text"):
                child.destroy()

def useRecruitButton(player, loc):
    village = loc.master
    actions.recruterSoldat(player, village)
    updateHeader(player)
    for child in panneau.winfo_children():
        if "Recruter un soldat\n(coût 1 ⓐ, 10 ¤)" in child.cget("text"):
            child.destroy()
    if player.j1:
        showRecruitButton(loc.coords[0], loc.coords[1], player)


def drawBuilding(i,j,player):
    global taillecase
    tile=carte[i][j].tkItem
    tilecos=canevas.coords(tile)
    draw_gear(canevas, tilecos[0]+taillecase/2, tilecos[1]+taillecase/2, taillecase/4, 4, taillecase/5, player.couleur)

def showCollectButton(i,j,player):
    location=carte[i][j]
    if location.master in player.fief and location.caseType!="village":
        collectButton=tk.Button(panneau, text="Collecter les ressources\n(coût 2 ⓐ)", command=lambda: collectRessources(i,j,player))
        collectButton.pack()
        if player.actions<2:
            collectButton.config(state='disabled')

def collectRessources(i,j,player):
    location=carte[i][j]
    location.collecte()
    player.actions-=2
    updateHeader(player)
    for child in panneau.winfo_children():
            if "Collecter les ressources\n(coût 2 ⓐ)" in child.cget("text"):
                child.destroy()


def impositionSeigneur(vassal, player):
    vassal.imposition_seigneur()
    player.actions-=1
    updateHeader(player)
    for child in panneau.winfo_children():
            if "Collecter les impôts\n(coût 1 ⓐ)" in child.cget("text"):
                child.destroy()


def showVillageButton(i,j,player):
    if carte[i][j].master==player.village:
        villageButton(i,j,player)

def showEndTurnButton():
    endTurnButton=tk.Button(panneau, text="Fin de tour", command=endTurns)
    endTurnButton.pack(side='bottom')

def showCaptureButton(i,j,player):
    if not carte[i][j].captured: 
        if j == 0 and i == 0:
            if carte[i+1][j].master in player.fief or carte[i][j+1].master in player.fief:
                captureButton(i, j, player)
        elif j == 0:
            if carte[i][j + 1].master in player.fief or carte[i + 1][j].master in player.fief or carte[i - 1][j].master in player.fief:
                captureButton(i, j, player)
        elif i == 0:
            if carte[i + 1][j].master in player.fief or carte[i][j + 1].master in player.fief or carte[i][j - 1].master in player.fief:
                captureButton(i, j, player)
        elif i == len(carte) - 1 and j == len(carte[i]) - 1:
            if carte[i - 1][j].master in player.fief or carte[i][j - 1].master in player.fief:
                captureButton(i, j, player)
        elif i == len(carte) - 1:
            if carte[i - 1][j].master in player.fief or carte[i][j + 1].master in player.fief or carte[i][j - 1].master in player.fief:
                captureButton(i, j, player)
        elif j == len(carte[i]) - 1:
            if carte[i + 1][j].master in player.fief or carte[i][j - 1].master in player.fief or carte[i - 1][j].master in player.fief:
                captureButton(i, j, player)
        else:
            if carte[i + 1][j].master in player.fief or carte[i][j + 1].master in player.fief or carte[i][j - 1].master in player.fief or carte[i - 1][j].master in player.fief:
                captureButton(i, j, player)


def updateCapturedOutline(player):
    for adelete in canevas.find_withtag('capturedoutline*'+player):
        canevas.delete(adelete)
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            tile=carte[i][j].tkItem
            tilecos=canevas.coords(tile)
            if 'captured' in canevas.gettags(tile):
                if 'capturedby*'+player in canevas.gettags(tile):
                    if i==0:
                        canevas.create_line(tilecos[0],tilecos[1],tilecos[0],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i-1][j].tkItem):
                            canevas.create_line(tilecos[0],tilecos[1],tilecos[0],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    if j==0:
                        canevas.create_line(tilecos[0],tilecos[1],tilecos[2],tilecos[1], fill=player, width=2, tags=['capturedoutline*'+player])
                    else: 
                        if 'capturedby*'+player not in canevas.gettags(carte[i][j-1].tkItem):
                            canevas.create_line(tilecos[0],tilecos[1],tilecos[2],tilecos[1], fill=player, width=2, tags=['capturedoutline*'+player])
                    if i==len(carte)-1:
                        canevas.create_line(tilecos[2],tilecos[1],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i+1][j].tkItem):
                            canevas.create_line(tilecos[2],tilecos[1],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    if j==len(carte[i])-1:
                        canevas.create_line(tilecos[0],tilecos[3],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])
                    else:
                        if 'capturedby*'+player not in canevas.gettags(carte[i][j+1].tkItem):
                            canevas.create_line(tilecos[0],tilecos[3],tilecos[2],tilecos[3], fill=player, width=2, tags=['capturedoutline*'+player])

def do_zoom(event):
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    factor = 1.001 ** event.delta
    canevas.scale(tk.ALL, x, y, factor, factor)

def do_zoom_in(event):
    global taillecase
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    if taillecase<=70:
        factor = 1.1
        taillecase=taillecase*factor
        canevas.scale(tk.ALL, x, y, factor, factor) #https://stackoverflow.com/questions/48112492/canvas-scale-only-size-but-not-coordinates html
    

def do_zoom_out(event):
    global taillecase
    x = canevas.canvasx(event.x)
    y = canevas.canvasy(event.y)
    if taillecase>=8:
        factor = 0.9
        taillecase=taillecase*factor
        canevas.scale(tk.ALL, x, y, factor, factor)

def test(event):
    print(canevas.canvasx(event.x),canevas.canvasy(event.y))




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












canevas.bind("<MouseWheel>", do_zoom) 

canevas.bind('<4>', do_zoom_in)
canevas.bind('<5>', do_zoom_out) 

canevas.bind('<ButtonPress-3>', test)
canevas.bind('<ButtonPress-2>', lambda event: canevas.scan_mark(event.x, event.y))
canevas.bind("<B2-Motion>", lambda event: canevas.scan_dragto(event.x, event.y, gain=1))



#canevas.config(scrollregion=(0,0,112*taillecase,84*taillecase))

def start_on_enter(event, item):
    canevas.itemconfig(item.tkItem, outline='red', width = 2)
    canevas.tag_raise(item.tkItem,"all")
    #canevas.tag_raise("village")

    canevas.bind('<Button-1>', lambda event, item=item : createPlayer(item.coords))


def start_on_leave(event, item):
    canevas.itemconfig(item.tkItem, outline='black', width = 1)
    canevas.tag_lower(item.tkItem)
    
    canevas.unbind('<Button-1>')
    outlineontop()

def createPlayer(cos):
    global startpos, player, players
    couls = ['red', 'sky blue', 'black', 'yellow', 'purple', 'orange', 'pink', 'brown', 'white']
    startpos=cos
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            item = carte[i][j]
            canevas.unbind('<Button-1>')
            canevas.tag_bind(item.tkItem, '<Enter>', lambda event, item=item: on_enter(event, item))
            canevas.tag_bind(item.tkItem, '<Leave>', lambda event, item=item: on_leave(event, item))
    player=projet.Player("lime",None, True)
    x,y=startpos
    village=actions.creer_village(carte[x][y],player, True)
    player.village=village
    capture(x,y,player, True)
    drawVillage(x,y,player,True)
    players.append(player)
    for i in range(9):
        players.append(projet.Player(couls[i],None, False))
        x,y = random.randint(0,111), random.randint(0,83)
        if carte[x][y].master:
            continue
        theirVillage=actions.creer_village(carte[x][y],players[i+1], True)
        players[i+1].village=theirVillage
        capture(x,y,players[i+1], True)
        drawVillage(x,y,players[i+1], True)
    newTurn()


def startGame():
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            item = carte[i][j]
            canevas.tag_bind(item.tkItem, '<Enter>', lambda event, item=item: start_on_enter(event, item))
            canevas.tag_bind(item.tkItem, '<Leave>', lambda event, item=item: start_on_leave(event, item))
    

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
            updateHeader(players[playing])
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
    all_actions = ['capture', 'collecte', 'build', 'construire_eglise', 'vassaliser', 'creer_village', 'collecte_impots', 'recruter_soldat']
    while bot.actions > 0:
        action = random.choice(all_actions)
        if action == 'capture' and bot.actions>=1:
            cos=bot.botCapture(carte)
            if cos:
                x,y=cos
                capture(x,y,bot)
        elif action == 'collecte' and bot.actions>=2:
            if bot.botCollecte():
                bot.actions -= 2
        elif action == 'build' and bot.actions>=1 and bot.village.chef.ressources>=25 and bot.village.chef.argent>=25:
            buildTile = bot.botBuild()
            if buildTile:
                x, y = buildTile.coords
                buildCase(x, y, bot)
        elif action == 'construire_eglise':
            bot.botConstruireEglise() #a faire bien
            bot.actions -= 1
        elif action == 'creer_village' and bot.actions>=1 and bot.village.chef.ressources>=10: 
            villageloc = bot.botCreerVillage(carte)
            if villageloc:
                x, y = villageloc.coords
                drawVillage(x, y, bot)
        elif action == 'collecte_impots' and bot.actions>=1:
            bot.botCollecteImpots()
            bot.actions -= 1
        elif action == 'recruter_soldat' and bot.actions>=1 and bot.village.chef.argent>=10:
            bot.botRecruterSoldat()
            bot.actions -= 1
        else:
            continue
    









donnees.grid(column=0,row=0,columnspan=2)
canevas.grid(column=0,row=1)
panneau.grid(column=1,row=1)

startGame()

win.resizable(False,False)
win.mainloop()
