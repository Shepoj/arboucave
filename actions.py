import random
from projet import Player, Roturier, Soldat, Ecclesiastique, Noble, Village


def creer_personne(statut: str, player = None):
    if statut == "roturier":
        return Roturier()
    elif statut == "soldat":
        return Soldat()
    elif statut == "ecclesiastique":
        return Ecclesiastique()
    elif statut == "noble":
        return Noble(player)


def immigration(village: Village, paysan = True):
    for _ in range(3):
        resultat = village.ajout_habitant(Roturier(paysan))
        if not resultat:
            print("Un habitant n'a pas pu être ajouté")
 

def construire_eglise(village: Village):
    village.construire_eglise()


def vassaliser(seigneur,vassal):
    pass


def creer_village(case, player: Player, init = False): #zone est une case
    if not init:
        player.actions += -1
        player.village.chef.ressources += -10

    return Village(case, player)


def collecte_impots(player: Player):
    for village in player.fief:
        village.chef.collecte_impots()
    
    for village in player.fief:
        village.chef.distribution_dime()

def doEvent(fun):
    pass

