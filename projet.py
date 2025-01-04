import random
from random import randint, choice
from noms import prenoms, noms

class Player():
    def __init__(self,couleur,village, j1=False):
        self.couleur=couleur
        self.village=village
        self.fief=[village] if village else []
        self.actions=10
        self.j1=j1



class Personne():
    def __init__(self,
        prenom = choice(noms),
        nom = choice(prenoms),
        age: int | None = None,
        ev = randint(30, 80)):

        self.prenom = prenom
        self.nom = nom
        self.age = randint(0, ev) if age is None else age
        self.ev = ev
        self.humeur = 5

    def __repr__(self):
        return self.affiche_nom
    
    def __str__(self):
        return self.affiche_nom
    
    @property
    def affiche_nom(self) -> str:
        return f"{self.nom} {self.prenom}"

    def vieillir(self):
        self.age+=1
        if self.age>self.ev:
            self.mourir()

class Roturier(Personne):
    def __init__(self, statut, nom,ev,age):
        super().__init__(nom,ev,age)
        self.statut=statut
        if statut=="paysan":
            self.argent=0
            self.ressources=0
            self.prod=random.randint(2,5)
        else:
            self.argent= random.randint(5,30)
            self.ressources=0
            self.prod=random.randint(5,10)


class Soldat(Personne):
    def __init__(self, nom,ev,age):
        super().__init__(nom,ev,age)


class Ecclesiastique(Personne):
    def __init__(self, nom,ev,age,argent,):
        super().__init__(nom,ev,age)
        self.argent=argent
        self.don=random.choice(["prod","vie","humeur","guerre"])


class Noble(Personne):
    def __init__(self,nom,ev,age, player=None):
        super().__init__(nom,ev,age)
        self.argent=random.randint(10,50)
        self.ressources=random.randint(10,50)
        self.village=None
        self.seigneur=None
        self.player=player
        self.l_vassaux=[]

    def collecte_impots(self):
        for roturier in self.l_roturiers :
            somme_pay = 10
            somme_art = 5
            if roturier.statut == "paysan" :
                if roturier.ressources == 0 :
                    self.argent += (roturier.argent - somme_pay )
                    roturier.argent -= somme_pay 
                elif roturier.argent == 0 :
                    self.ressoures += ((0.5) * roturier.ressources)
                    roturier.ressources -= ((0.5) * roturier.ressources) # a refaire nul
                else :
                    roturier.mourir()
            else :
                if roturier.ressources == 0 :
                    self.argent += (roturier.argent - somme_art)
                    roturier.argent -= somme_art
                elif roturier.argent == 0 :
                    self.ressoures += ((0.25) * roturier.ressources)
                    roturier.ressources -= ((0.25) * roturier.ressources)
                else :
                    roturier.mourir()

    def distribution_dime(self, ecclesiastique):
        montant_dime= 15
        ecclesiastique.argent += montant_dime
        self.argent -= montant_dime

    def vassalisation(self,seigneur):
        self.seigneur=seigneur
        seigneur.l_vassaux.append(self)
        seigneur.player.fief.append(self.village)

    def imposition_seigneur(self):
        impotArgent = int(0.3*self.argent)
        impotRessources = int(0.3*self.ressources)
        self.argent -= impotArgent
        self.ressources -= impotRessources
        self.seigneur.argent += impotArgent
        self.seigneur.ressources += impotRessources




        
class Case():
    def __init__(self,coords,tkItem,terrain):
        self.coords=coords
        self.terrain=terrain
        self.captured=False
        self.master=None
        self.tkItem=tkItem
        self.type=None
    def capture(self,village):
        self.captured=True
        self.master=village
        self.master.ajoutTerres(self)
        
class Village(Case):
    def __init__(self,lieu,chef):
        self.type="village"
        self.chef=chef
        chef.village=self
        self.hasEglise=False
        self.lieu=lieu
        self.coords=lieu.coords
        self.terres=[lieu.coords]
        self.habitants=[]
        self.armee=0
        self.maxHabitants = len(self.terres)*20
        self.vassaux=[]
    def ajoutTerres(self,terre):
        self.terres.append(terre)


if __name__ == "__main__":
    p = Personne()
    print(p)
