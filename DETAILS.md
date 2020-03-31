# Description des algorithmes implémentés

## Logique de jeu
Toute la logique de jeu est située dans un objet `Game` (`models/Game.py`). On y retrouve notamment :
- les fonctions permettant de communiquer avec le socket serveur;
- la carte actualisée nous permettant de déterminer les positions des différentes populations.

Dans le constructeur de cette classe, on trouve la logique permettant d'initialiser chaque partie. Elle dispose
également de méthodes nous permettant de transmettre les mouvements pour le tour actuel ou encore de mettre à jour
la carte stockée en mémoire.


## Helpers

### Positions
Dans `lib/positions` on trouve les fonctions permettant à partir d'une carte donnée de récupérer les positions
des humains, des vampires ou des loups-garous.

### Split groups
`lib/compute_split_moves` contient les fonctions utilisées pour générer toutes les combinaisons de coups possibles
en donnant la possibilité à chaque groupe de se diviser en 2. `lib/test_compute_split_moves` contient les tests
unitaires pour ces fonctions.

### Timeout
`lib/TimeoutException` contient la classe `TimeoutException`. Cette exception sera soulevée lorsque l'algorithme d'IA
met trop de temps à répondre. Nous devons en effet répondre au serveur en moins de 2 secondes et nous retournerons
alors le meilleur coup déjà analysé sans parcourir la suite des coups possibles.

### Util
Dans `lib/util` se trouvent toutes les fonctions de base pouvant être réutilisées par différents algorithmes.
Par exemple, `distance_nb_moves` qui retourne la distance en nombre de mouvements pour aller d'une position A à une
position B.

### Constantes
`lib/constants.py` contient simplement toutes les constantes partagées à l'échelle de l'application.

## Constitution de l’arbre des états possibles

Pour une carte connue, il nous faut évaluer tous les états successifs possibles. Si on considère tous les déplacements
possibles de toutes les divisions possibles pour un de nos groupes, nous aboutissons à une trop grande quantité d’états.
Cela rend l’algorithme incapable de répondre en moins de 2 secondes.

Nous avons une fonction `compute_all_available_moves` dans `lib/compute_split_moves` permettant de calculer toutes
les combinaisons possibles de déplacements avec une séparation en 2 groupes maximum à chaque tour. Mais là encore
le temps de calcul n'est pas envisageable.

Nous avons pensé à réduire le facteur de branchement de l'arbre des possibles en réalisant une première estimation
de la pertinence d'une carte mais nous avons manqué de temps pour l'implémenter.

Nous avons donc gardé l'implémentation naïve de ne pas se diviser et de considérer uniquement les 8 positions
voisines comme coups possibles.


## Algorithme d’IA

### Alpha Beta

Notre IA repose sur l'algorithme MiniMax avec élagage alpha-beta vu en cours.

Notre implémentation de la fonction de maximisation peut-être résumée comme suit :
- Si on approche les 2 secondes limites d'analyse, soulève une `TimeoutException`
- Si on atteint un état final (partie terminée ou profondeur max atteinte), retourne le score calculé, la carte
évaluée ainsi que les coups à jouer pour en arriver là
- Sinon on génère tous les états successeurs et calcule leur score en appelant la fonction de minimisation sur chacun.
On cherche ensuite le maximum parmi chacun de ces scores et on retourne la carte et les coups associés.

La fonction de minimisation fonctionne de la même façon en inversant les procédés de maximisation et minimisation.

Compte tenu des limites de temps de calcul imposées (2 secondes par tour), nous pouvons explorer l’arbre des états sur
une profondeur de 4 niveaux, soit deux tours pour nous et deux tours pour l’adversaire.
Finalement, on choisira le successeur (la carte) ayant le meilleur alpha.

L’algorithme alpha-beta est implémenté dans le fichier `alpha_beta.py` dans la fonction `alphabeta_search`.


### Résolution de conflits

Il arrive qu'en générant les états successeurs d'une carte, on déplace un groupe sur une case où il y a des humains
ou des adversaires. Cela implique qu'il faut résoudre le conflit en anticipant le combat qui aura lieu côté serveur.
Notre approche est plus limitée qu'une bataille aléatoire pour ne pas favoriser les situations où la probabilité
de gagner est très faible.

- Si on est certain de gagner contre des humains (> 1) ou contre des adversaires (> 1.5), le combat est gagné.
- Si on est moins nombreux que des humains ou que l'adversaire est 1.5 fois plus nombreux que nous, le combat est perdu.
- Dans le cas où l'on est plus nombreux que l'adversaire mais pas 1.5 fois plus nombreux, le combat est gagné avec des
pertes d'unités de notre côté.
- De même si l'on est moins nombreux mais pas 1.5 fois moins nombreux, le combat est perdu avec des pertes de leur
côté.

# Heuristique et stratégie de l’IA

## Heuristique

Une heuristique est implémentée afin d’évaluer le potentiel de chaque état possible en calculant un score pour chaque
carte. L’algorithme alpha-beta utilise ces différents scores soit en le minimisant quand c’est au tour de l’adversaire
soit en le maximisant quand c’est notre tour. In fine, on choisira la carte offrant le plus haut alpha.

L’heuristique prend en compte trois éléments dans le calcul du score :
- l’effectif total de notre espèce par rapport aux ennemis
- les effectifs humains à proximité : on privilégie les groupes d’humains les plus gros et les plus proches,
sans toutefois s’intéresser aux groupes plus nombreux que nous.
- les effectifs ennemis à proximité : même stratégie en observant le facteur 1.5. Si les ennemis sont 1.5 fois plus
nombreux que nous, l’heuristique prend en compte un malus de score.

Celle-ci est implémentée dans `heuristics/monogroup.py`.
