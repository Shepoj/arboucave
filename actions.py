import projet
import random
import noms

from projet import Personne, Roturier, Soldat, Ecclesiastique, Noble, Village

cout_action=0


def creer_personne(statut: str, player = None, paysan = True):
    if statut == "roturier":
        return Roturier()
    elif statut == "soldat":
        return Soldat()
    elif statut == "ecclesiastique":
        return Ecclesiastique()
    elif statut == "noble":
        return Noble(player)


def immigration (village,statut) : 
    i=1
    cout_paysan  = 0
    cout_artisan = 0

    while len(village.habitants) <= village.maxhabitants and i <= 3:
        if statut == "paysan":
            cout_action-=cout_paysan
            village.habitants.append(creer_personne("roturier", None,"paysan"))
        else:
            cout_action-=cout_artisan
            personne=creer_personne("roturier", None,"artisan")
            village.habitants.append(personne)
            village.argent+=personne.argent
        i+=1
        

def vassaliser(seigneur,vassal):
    pass

def construire_eglise(village):
    village.hasEglise = True
    village.habitants.append(creer_personne("ecclesiastique"))


def creer_village(zone, player, init = False): #zone est une case
    if not init:
        player.actions -= 1
        player.village.chef.ressources -= 10

    village = Village(zone, player)
    zone.type = "village"
    zone.master = village
    player.fief.append(village)
    
    return village


def tourSuivant():
    pass











