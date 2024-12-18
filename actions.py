import projet
import random
import noms

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

def immigration (village) : ##idee generale
    for i in range(nb):
        if immigrant.statut == "paysan":
            cout_action-=X
            village.habitants+=[]
        else:
            cout_action-=Y
            village.habitants+=[]
            village.argent+=immigrant.argent


def construire_eglise(village):
    cout_action = cout_action -X
    village.hasEglise = True
    village.habitants.append(creer_personne("ecclesiastique"))


def create_village(case, init = False):
    if not init:
        cout_action = cout_action -X
    chef = creer_personne("noble")
    village = projet.Village(chef)
    village.habitants = [chef]+[creer_personne("roturier") for i in range(4)]
    case.type = "village"
    case.capture()
    return village

