from typing import Callable

from projet import Player, Roturier, Soldat, Ecclesiastique, Noble, Case, Village


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


def creer_village(case: Case, player: Player, init = False):
    if not init:
        player.actions += -1
        player.village.chef.ressources += -10

    return Village(case, player)


def collecte_impots(player: Player):
    for village in player.fief:
        village.chef.collecte_impots()
    
    for village in player.fief:
        village.chef.distribution_dime()


def strategie(armee: int, part: tuple[int, int, int]):
    total = part[0] + part[1] + part[2]
    pierre = int((armee*part[0])/total)
    feuille = int((armee*part[1])/total)
    ciseau = armee - pierre - feuille
    return (pierre, feuille, ciseau)

def pfc(coup: int, ennemi: int):
    # 0: pierre, 1: papier, 2: ciseau
    return (ennemi+1)%3 == coup

def bataille(allie: int, ennemi: int, avantage: bool):
    if avantage:
        if 2*allie >= ennemi:
            return True, allie - ennemi//2
        return False, ennemi - 2*allie
    else:
        if allie >= 2*ennemi:
            return True, allie - 2*ennemi
        return False, ennemi - allie//2

def guerre(player: Player, cible: Player):
    allie = strategie(player.armee, player.part)
    ennemi = strategie(cible.armee, cible.part)
    score = 0

    for i, j in zip(player.ordre, cible.ordre):
        victoire, pertes = bataille(allie[i], ennemi[i], pfc(i, j))
        if victoire:
            score += 1
            player.mort_soldats(pertes)
        else:
            cible.mort_soldats(pertes)
            
        # arrete potentiellement prematurement pour eviter des pertes
        if score == 2:
            player.vaincre(cible)
            return True

    cible.vaincre(player)
    return False

def doEvent(fun):
    pass


if __name__ == "__main__":
    print(strategie(100, (1, 1, 2)))
    print(pfc(0, 1))
    print(bataille(20, 15, False))