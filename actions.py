import projet
import random
import noms

from projet import Personne, Roturier, Soldat, Ecclesiastique, Noble

cout_action=0


def creer_personne(statut, paysan = True):
    if statut == "roturier":
        return Roturier("paysan" if paysan else "artisan")
    elif statut == "soldat":
        return Soldat()
    elif statut == "ecclesiastique":
        return Ecclesiastique()
    elif statut == "noble":
        return Noble()


def immigration (village,statut) : 
    i=0
    while i<3 and len(village.habitants)<village.maxHabitants:
        pass
        

def vassaliser(seigneur,vassal):
    pass

def construire_eglise(village):
    village.hasEglise = True
    village.habitants.append(creer_personne("ecclesiastique"))


def creer_village(zone, player, init = False): #zone est une case
    if not init:
        player.actions -= 1
        player.village.chef.ressources -= 10
    chef = creer_personne("noble", player)
    village = projet.Village(zone, chef)
    village.habitants = [chef]+[creer_personne("roturier") for i in range(4)]
    chef.village = village
    zone.type = "village"
    zone.master = village
    player.fief.append(village)
    
    return village


def tourSuivant():
    pass











