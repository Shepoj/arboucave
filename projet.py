import random


class Personne():
    def __init__(self,nom,ev,age):
        self.nom= nom #a generer
        self.ev=ev
        self.age=age
        self.humeur = 5
    def __repr__(self):
        return self.nom
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
    def __init__(self,nom,ev,age,terres,l_roturiers):
        super().__init__(nom,ev,age)
        self.argent=random.randint(10,50)
        self.ressources=random.randint(10,50)
        self.terres=terres
        self.l_roturiers=l_roturiers

    def collecte_impots_roturier(self):
        for roturier in self.l_roturiers :
            somme_pay = 10
            somme_art = 5
            if roturier.statut == "paysan" :
                if routurier.ressources == 0 :
                    self.argent += (roturier.argent - somme_pay )
                    roturier.argent -= somme_pay 
                elif roturier.argent == 0 :
                    self.ressoures += ((0.5) * roturier.ressources)
                    roturier.ressources -= ((0.5) * roturier.ressources)
                else :
                    roturier.mourir()
                
            else :
                if routurier.ressources == 0 :
                    self.argent += (roturier.argent - somme_art)
                    roturier.argent -= somme_art
                elif roturier.argent == 0 :
                    self.ressoures += ((0.25) * roturier.ressources)
                    roturier.ressources -= ((0.25) * roturier.ressources)
                else :
                    roturier.mourir()
                    
    montant_dime= 15
    def distribution_dime(self, Ecclesiastique: ecclesiastique):
        ecclesiastique.argent += montant_dime
        self.argent -= montant_dime
        

class Vassal (Noble):
    def __init__(self,nom,ev,age,terres,l_roturiers,argent,ressources):
        super().__init__(nom,ev,age,terres,l_roturiers,argent,ressources)

    
class Seigneur(Noble):
    def __init__(self,nom,ev,age,terres,l_roturiers,argent,ressources,fief,l_vassaux):
        super().__init__(nom,ev,age,terres,l_roturiers,argent,ressources)
        self.fief=fief
        self.l_vassaux=l_vassaux
        

    def collecte_impots_vassal(self):
        for vassal in self.l_vassaux :
            self.ressoures += ((0.1) * vassal.ressources) ## 10% des ressources du vassal
            vassal.ressources -= ((0.1) * vassal.ressources)

        
class Case():
    def __init__(self,coords,tkItem,terrain):
        self.coords=coords
        self.terrain=terrain
        self.captured=False
        self.tkItem=tkItem
        self.type=None
    def capture(self):
        self.captured=True

class Village(Case):
    def __init__(self,chef):
        self.type="village"
        self.chef=chef
        self.hasEglise=False
        self.terres=[self.coords]
        self.chef.terres=[self.coords]
        self.habitants=[]
        
            








