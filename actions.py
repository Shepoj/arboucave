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

    village = Village(zone, player)
    zone.type = "village"
    zone.master = village
    player.fief.append(village)
    
    return village


def tourSuivant():
    l_events =["epidemie","incendies","famine","pillage", "rien","récolte","vassalistaion"]
    event = random.choice(l_events)