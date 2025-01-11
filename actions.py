from projet import Player
from gens import Roturier, Soldat, Ecclesiastique, Noble
from carte import Case, Village
from gfx import Case_gfx, Ferme_gfx, Village_gfx, carte





# TODO prochaine etape

# case
def capture(case: Case, player: Player):
    player.actions += -1
    case.capture(player.village)

def collecte_ressources(case: Case, player: Player):
    player.actions += -2
    case.collecte()

def construire_ferme(case: Case_gfx, player: Player):
    assert case.controle
    
    player.actions += -1
    case.controle.chef.argent += -10
    case.controle.chef.ressources += -25

    f = Ferme_gfx(case, player.couleur)
    x, y = f.coords
    carte[x][y] = f
    case.controle.terres.remove(case)
    case.controle.terres.append(f)
    f.draw()
    f.redraw()
    return f

def construire_village(case: Case_gfx, player: Player):
    player.actions += -1
    player.village.chef.ressources += -10

    v = Village_gfx(case, player.couleur)
    x, y = v.coords
    carte[x][y] = v
    player.fief.append(v)
    v.draw()
    return v
    

# village
def construire_eglise(village: Village, player: Player):
    player.actions += -1
    village.construire_eglise()

def imposition_seigneur(village: Village, player: Player):
    player.actions += -1
    village.chef.imposition_seigneur()

def recruter_soldat(village: Village, player: Player):
    player.actions += -1
    village.chef.argent += -10
    village.ajout_habitant(Soldat(village))




# chaque tour
def collecte_impots(player: Player):
    for village in player.fief:
        village.chef.collecte_impots()
    
    for village in player.fief:
        village.chef.distribution_dime()


def immigration(player, village: Village, paysan = True):
    player.actions += -1 if paysan else -2
    for _ in range(3):
        if village.max_habitants > len(village.habitants):
                village.ajout_habitant(Roturier(village))
                """if not resultat:
            print("Un habitant n'a pas pu être ajouté") #FENETRE"""
 


def vassaliser(seigneur,vassal):
    pass

def villagerEachTurn(player: Player):
    for village in player.fief:
        for villageois in village.habitants:
            if type(villageois) == Roturier:
                villageois.produire()
                if villageois.vieillir():
                    continue
            villageois.consommer()
            

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