import projet
import random
import noms

cout_action=0


def creer_personne(statut, classe="paysan"):
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
        personne = projet.Noble(nom_complet,ev,age,random.randint(0,100))
    return personne


def immigration (village,statut) : 
    i=1
    cout_paysan  = 0
    cout_artisan = 0

    while len(village.habitants) <= village.maxhabitants and i <= 3:
        if statut == "paysan":
            cout_action-=cout_paysan
            village.habitants.append(creer_personne("paysan"))
        else:
            cout_action-=cout_artisan
            personne=creer_personne("artisan")
            village.habitants.append(personne)
            village.argent+=personne.argent
        i+=1
        

def vassaliser(seigneur,vassal):
    pass

def construire_eglise(village):
    cout_action = cout_action - X
    village.hasEglise = True
    village.habitants.append(creer_personne("ecclesiastique"))


def creer_village(zone, player, init = False): #zone est une case
    if not init:
        player.actions -= 1
        player.village.chef.ressources -= 10
    chef = creer_personne("noble")
    village = projet.Village(zone, chef)
    village.habitants = [chef]+[creer_personne("roturier") for i in range(4)]
    zone.type = "village"
    zone.master = village
    player.fief.append(village)
    
    return village


def tourSuivant():
    pass











