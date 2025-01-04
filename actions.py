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











