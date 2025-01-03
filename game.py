import random
import projet


"""
class Personne():
    def __init__(self, nom,ev,age):
        self.nom= nom #a generer
        self.ev=ev
        self.age=age
        self.humeur = 5
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
    def __init__(self, nom,ev,age):
        super().__init__(nom,ev,age)
        self.don=random.choice(["prod","vie","humeur","guerre"])

class Noble(Personne):
    def __init__(self,terres, nom,ev,age):
        super().__init__(nom,ev,age)
        self.argent=random.randint(10,50)
        self.ressources=random.randint(10,50)
        self.terres=terres

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
    def __init__(self,chef,coords,terrain):
        super().__init__(coords,terrain)
        self.type="village"
        self.chef=chef
        self.habitants=[]

"""
