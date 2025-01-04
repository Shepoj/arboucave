# TD IHM - Conception d’interface

## Exercice 1. Modèle conceptuel d’une application de gestion d’une société médiévale.** *(30 min)*  
Construire le modèle conceptuel de l’interface graphique de l’application en vous appuyant sur les informations données en annexe.  
1. Lister les fonctionnalités et les organiser. Inscrire également quand cela est nécessaire, les traitements et les réponses de l’application (le **feedback**).  
2. Concevoir un scénario d’utilisation permettant d’illustrer un enchaînement représentatif de tâches que l’utilisateur peut avoir à accomplir en utilisant l’application.  



## Exercice 2. Prototypage papier *(90 min)*  
Concevoir, à l’aide de papier quadrillé (ou d’une application dédiée comme [https://explaineverything.com](https://explaineverything.com) ou [https://sketchboard.io](https://sketchboard.io)), un prototype tel qu’il soit possible de jouer le scénario, puis organisez-vous en groupe de 3 devant l’interface papier que vous avez conçue et enrichie, avec un concepteur, un utilisateur et un scribe :  
- **Le concepteur** fait jouer le scénario à l’utilisateur, il doit se contenter d’indiquer à l’utilisateur la/les tâches à accomplir et de simuler le comportement de l’application (traitement, réponses, feedback).  
- **L’utilisateur** doit être pris **dans un autre groupe**, il est libre de son comportement.  
- **Le scribe** note le comportement de l’utilisateur (erreurs, hésitations, problèmes bloquants, aspects positifs, etc.).  



## Exercice 3. Walkthrough *(15 min)*  
Le walkthrough est l’examen de l’application par des pairs. Le but est de détecter le plus grand nombre de problèmes possible. Le walkthrough peut couvrir l’ensemble de l’application ou se limiter aux aspects décrits dans le scénario.  



## Exercice 4. Brainstorming *(15 min)*  
Les groupes doivent se reconstituer pour discuter des problèmes soulevés lors du walkthrough ou du prototypage. Le brainstorming doit se faire en deux étapes :  
1. Une discussion doit permettre de dégager le plus d’idées possible *(10 min)* sans juger de leur validité.  
2. Ensuite, il s’agit d’évaluer les idées et de voter pour déterminer quelles idées doivent être retenues *(5 min)*.  



# Annexe

Ce projet se base sur une modélisation grossière de la société médiévale. À partir de ce modèle, on souhaite créer un petit jeu qui fait évoluer un fief, constitué de villages, dans le but de le faire prospérer. Le joueur sera le seigneur en charge du fief, et aura à chaque tour la possibilité d’effectuer des actions en fonction de l’argent dont il dispose.

[Wikipédia] La société médiévale est une société d’ordres organisée autour des trois ordres suivants :  
- ceux qui prient : oratores (le clergé, les hommes d’église),  
- ceux qui combattent : bellatores (les nobles : prince, seigneurs, chevaliers),  
- ceux qui travaillent : laboratores (les paysans, les artisans et les serfs).

C’est un système destiné, lorsqu’il a été énoncé au XIe siècle, à amener la société vers une organisation dite parfaite.



## Personne
Une personne, dans le cadre du projet, est caractérisée par son nom, son statut, son espérance de vie (de 30 à 100), son âge, le montant des ressources et de l’argent dont il dispose, et son humeur (ou indice de bonheur, de 1 à 10, à sa création).

Et dans une gestion basique de ces paramètres, une personne est amenée à faire des échanges commerciaux en vendant ou en achetant des ressources, ou à travailler pour gagner des ressources ou de l’argent. Une personne, selon son statut, aura aussi à payer ou à recevoir un impôt (fief, église, etc.). Enfin, certaines personnes meurent au bout d’un certain temps, ce qui est simulé par un test d’espérance de vie (lié à l’âge, au statut et au montant de l’argent total).



## Roturier
[Wikipédia] Ce sont les paysans, les artisans, les marins, les bourgeois vivant de leurs biens et de leurs charges, et en général tous les habitants des seigneuries de la campagne, des bourgs et des cités, qui exercent des emplois utiles.

Dans le cadre de cette simulation, ils se distinguent principalement par leur revenu, mais on peut jouer sur d’autres paramètres (leur espérance de vie par exemple). Chaque roturier a une capacité de production (de valeur au moins égale à 2) qui lui permet d’augmenter ses ressources. Parmi les roturiers, on peut distinguer :  
- **les paysans**, qui ne disposent pas d’argent initialement,  
- **les artisans**, qui ont un pécule de départ (à déterminer) et une capacité de production supérieure.



## Noble
Un noble possède des terres (généralement octroyées par un seigneur), sur lesquelles sont fondés des villages qu’il administre. Le noble peut soumettre à l’impôt ses roturiers (c’est-à-dire leur confisquer des ressources ou de l’argent). Il prélève un impôt différent sur les paysans dont il confisque la moitié de leurs ressources, contre seulement un quart pour les autres roturiers.

Un **seigneur** est un noble qui possède un fief. Il possède en propre des terres et des villages mais il a également des vassaux (qui sont nobles), qu’il peut aussi soumettre à l’impôt (mais à un taux beaucoup plus bas à déterminer).

[Wikipédia] Les relations entre seigneurs de rangs différents, c’est-à-dire entre vassaux et suzerains jusqu’au roi, sont réglées notamment par des serments de fidélité. Vassal et suzerain se doivent des obligations mutuelles.



## Ecclésiastique
C'est un membre du clergé, ce dernier étant fortement hiérarchisé. On ne s'intéressera qu'au bas clergé (c'est-à-dire le curé) et ses supérieurs immédiats, qui se trouvent en bas de la hiérarchie religieuse et qui est un prêtre responsable d'une paroisse. Selon les ressources des paroissiens, il était souvent assez pauvre, ne vivant que de la portion congrue de la dîme.  

Dans le cadre de ce projet, chaque ecclésiastique possède un don particulier qui apporte un bénéfice à la paroisse dont il est responsable (augmentation de la production, augmentation de l'espérance de vie, amélioration de l'humeur, etc.).  



## Fief
Un fief est un territoire plus ou moins vaste, comportant des villages plus ou moins importants et des ressources. Il est constitué de plusieurs types de terrains tels que la plaine (unique terrain sur lequel on peut construire un village), la forêt, la montagne ou le lac (par souci de simplification) et qui apportent un facteur de ressources (génériques) différent.  

La représentation du territoire se fera grossièrement à partir d’une grille et sera générée de façon procédurale. Il faudra donc prendre garde aux proportions des différents types de terrains.  

Seule une partie du territoire constitue le fief de départ du joueur, avec un village habité par des paysans (au moins 10) et quelques ressources associées. D'autres villages, dirigés par des nobles indépendants ou des ecclésiastiques, peuvent être générés. Une distance minimale de déplacement est imposée entre chaque village.  



## Village
Un village, possédé par un noble, est composé de roturiers (se répartissant en paysans et artisans) et parfois d’un ecclésiastique.  

Un bénéfice est perceptible et souvent d’un ecclésiastique non imposable. Les impôts dépendent des terres qui lui sont attachées (de 1 à 9).  



## Déroulement d’une partie  
Une partie est décomposée en tours. Chaque tour est lui-même subdivisé en plusieurs étapes :  
1. Choix aléatoire d’un événement bénéfique (récolte abondante, immigration, vassalisation spontanée, …) ou néfaste (famines, épidémies, pillages, inondations, incendies, …).  
2. Actions du seigneur et des autres nobles dans un ordre aléatoire (construction d’un village, vassalisation d’un noble, déclaration de guerre, révolte, etc.).  
3. Réactions (guerre, révolte, …).  
4. Fin du tour.  

## Événements : 
Le choix de l’événement du tour peut se faire en effectuant un tirage aléatoire dans une table, telle que celle proposée ci-dessous :  
| 1D100 | Type      | Effet |
|-------|-----------|-------|
| 01-05 | Épidémies | Les personnes dont edv < X meurent. |
| 06-15 | Pillages  | Les habitants et les ressources d’un village sont volés. |
| 16-20 | Famines   | Les ressources des plaines sont divisées par deux. |
| 21-40 | Rien      | Aucun effet. |
| 41-64 | Récolte abondante | Les ressources des plaines sont doublées. |
| 65-99 | Vassalisation | Un noble se propose comme vassal. |

Chaque évènement bénéfique (ou néfaste) entraîne une **augmentation** (ou **diminution**) de l'humeur des personnes concernées.



## Actions

Les actions peuvent être initiées par le joueur ou par les autres nobles. Chaque action a un coût. Dans un premier temps, on considère qu'ils peuvent :

- Favoriser l'immigration
- Construire une église
- Vassaliser un noble
- Construire un nouveau village
- Prélever l'impôt
- Recruter des soldats
- Déclarer la guerre

### Immigration

Faire venir des paysans (coût : 1) ou des artisans (coût : 2) dans un village.

### Église

Construire une église dans un village, ce qui fait automatiquement venir un ecclésiastique (avec un don tiré au hasard).

### Vassaliser

Proposer des ressources, de l'argent et obligatoirement des terres à un noble. Celui-ci acceptera ou refusera en fonction de son influence (villages, ressources, argent, soldats).

### Village

Le coût d'un village (en ressources et en argent) dépend de sa taille, c'est-à-dire du nombre d'habitants initiaux (roturiers, ecclésiastiques) et des terres associées.

### Impôt

Prélever l'impôt dans chacun des villages sous l'autorité directe du noble (puis redistribution de la dime aux ecclésiastiques, dont c'est le seul moyen de subsistance).

### Soldat

Un soldat est une bouche à nourrir qui augmente l'autorité d'un noble et sera surtout utile à la guerre.

### Guerre

Un noble vassal doit répondre à l'appel de son seigneur pour la guerre (ban) avec un nombre convenu de soldats reflétant son importance. Des roturiers sont de plus réquisitionnés pour les charrois et le guet (droit de guet).

Les nobles s'affrontent avec leurs soldats et leurs chevaliers (eux-mêmes et leurs vassaux). Les confrontations sont individuelles et aléatoires. Trois cas sont possibles :

- Soldat contre soldat
- Soldat contre chevalier
- Chevalier contre chevalier (dans ce dernier cas, le vainqueur n'élimine pas son adversaire, mais demande une rançon)

Les chances de vaincre sont laissées à l'appréciation du concepteur. Le noble vaincu devient automatiquement vassal du noble vainqueur. Si le vainqueur est le joueur, la partie est terminée.



## Réaction

Les réactions sont des évènements qui sont les conséquences des actions des nobles. Pour le joueur, la partie se termine en cas d'échec.

### Révolte

Si l'humeur des habitants d'un village tombe en moyenne en dessous d'un certain seuil, il y a une révolte. Un affrontement a lieu entre le noble (chevalier), ses soldats et les roturiers du village. Si le noble n'a pas de soldat, il est automatiquement vaincu et son domaine revient au noble le plus puissant.

### Guerre

Il peut arriver qu'un noble prenne ombrage de la proposition de vassalisation du seigneur ou bien qu'il devienne suffisamment puissant pour déclarer la guerre au seigneur joueur.

## Fin du tour

Le dernier noble qui a terminé ses actions met fin au tour. On procède alors automatiquement aux actions suivantes dans l'ordre :

1. Des ressources sont produites par les roturiers (10 roturiers maximum par terre) et consommées par tous les individus (à raison d'1 ressource par personne).
2. Toutes les personnes vieillissent, certaines meurent lorsqu'elles atteignent leur espérance de vie ou si elles n'ont plus ni ressources, ni argent.
3. Des roturiers (paysans, artisans d'âge 20) viennent augmenter la population de tous les villages.