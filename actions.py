import projet
import random
import noms

cout_action=0


def creer_personne(statut, player=None, classe="paysan"):
    nom=random.choice(noms.noms)
    prenom=random.choice(noms.prenoms)
    ev = random.randint(30,80)
    age = random.randint(0,ev)
    nom_complet=prenom+" "+(nom if statut!="noble" else "de "+nom)
    if statut == "roturier":
        personne = projet.Roturier(classe,nom_complet,ev,age)
    elif statut == "soldat":
        personne = projet.Soldat(nom_complet,ev,age)
    elif statut == "ecclesiastique":
        personne = projet.Ecclesiastique(nom_complet,ev,age)
    elif statut == "noble":
        personne = projet.Noble(nom_complet,ev,age,player)
    return personne


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











