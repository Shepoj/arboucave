import projet
import random
import noms

<<<<<<< HEAD
from projet import Personne, Roturier, Soldat, Ecclesiastique, Noble
=======
from projet import Personne, Roturier, Soldat, Ecclesiastique, Noble, Village
>>>>>>> 796d987 (branche)

cout_action=0


<<<<<<< HEAD
def creer_personne(statut, player = None, paysan = True):
    if statut == "roturier":
        return Roturier("paysan" if paysan else "artisan")
=======
def creer_personne(statut: str, player = None, paysan = True):
    if statut == "roturier":
        return Roturier()
>>>>>>> 796d987 (branche)
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
<<<<<<< HEAD
    chef = creer_personne("noble", player)
    village = projet.Village(zone, chef)
    village.habitants = [chef]+[creer_personne("roturier") for i in range(4)]
    chef.village = village
=======

    village = Village(zone, player)
>>>>>>> 796d987 (branche)
    zone.type = "village"
    zone.master = village
    player.fief.append(village)
    
    return village


def tourSuivant():
    l_events =["epidemie","incendies","famine","pillage", "rien","récolte","vassalistaion"]
    event = random.choice(l_events)












