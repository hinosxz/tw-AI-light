# Description des algorithmes implémentés

## Constitution de l’arbre des états possibles

Pour une carte connue, il nous faut évaluer tous les états successifs possibles. Si on considère tous les déplacements
possibles de toutes les divisions possibles pour un de nos groupes, nous aboutissons à une trop grande quantité d’états.
Cela rend l’algorithme d’IA choisi peu performant.

Nous avons donc décidé de ne considérer que certains états “intelligents”. Ainsi le fichier `compute_groups` propose tous
les états pertinents, c’est à dire toutes les divisions pertinentes et les déplacements pertinents autour d’un groupe
initial. Pour ce faire, nous observons la carte avec les groupes d’ennemis et d’humains et on va ranger ces groupes par
taille croissante (en prenant en compte les coefficients nécessaires à la victoire lors d’un conflit). On a donc une
liste triée par taille des (tailles/ positions) des groupes d’humains et des (1.5*tailles/ positions) des groupes
d’ennemis.

On va parcourir cette liste pour former des séparations pertinentes de notre groupe. Pour chaque taille de groupe dans
la liste, on va vérifier qu’en formant une entité de cette taille sur la carte, on ne rende pas l’entité restante
vulnérable.

![Schema](images/schema.png)

Cet algorithme est implémenté dans le fichier compute_groups.py du dossier lib. Ce fichier comporte deux fonctions :
- la fonction compute_groups qui crée des sous-groupes intelligents comme on a pu le voir précédemment
- la fonction find_closest qui va proposer un placement intelligent pour chaque sous-groupe créé. Ainsi, on va déplacer
un sous-groupe dans la direction du groupe adversaire pour lequel il a été créé (cf fonctionnement de compute_groups).

De cette façon, on a beaucoup réduit le nombre d’états possibles.

L’obtention de tous les états possibles se fait grâce à la fonction get_successors du fichier `alpha_beta.py` du dossier
`lib`. Cette fonction utilise `compute_groups`.



## Algorithme d’IA


Notre IA repose sur un algorithme de recherche adversariale. Nous avons choisi l’algorithme alpha-beta.
Celui-ci explore l’arbre des états, calculant pour chaque état une heuristique. Lorsque c’est notre tour,
l’algorithme va maximiser l’heuristique c’est à dire retenir l’état (la carte) donnant l’heuristique maximale,
et lorsque c’est le tour de l’adversaire, l’algorithme retiendra l’heuristique minimale.

L’algorithme alpha-beta est plus performant que l’algorithme min-max car il élague l’arbre. C’est à dire qu’il ne va
pas explorer les successeurs d’un noeud dont on sait déjà qu’il ne sera pas choisi.

Compte tenu des limites de temps de calcul imposées (2 secondes par tour), nous pouvons explorer l’arbre des états sur
une profondeur de 4 niveaux, soit deux tours pour nous et deux tours pour l’adversaire.
Finalement, on choisira le successeur (la carte) ayant le meilleur alpha.

L’algorithme alpha-beta est implémenté dans le fichier `alpha_beta.py` dans la fonction `alphabeta_search`.


# Heuristique et stratégie de l’IA

## Heuristique

Une heuristique est implémentée afin d’évaluer le potentiel de chaque état possible en calculant un score pour chaque
carte. L’algorithme alpha-beta utilise ces différents scores soit en le minimisant quand c’est au tour de l’adversaire
soit en le maximisant quand c’est notre tour. In fine, on choisira la carte offrant le plus haut alpha.

L’heuristique prend en compte trois éléments dans le calcul du score :
- l’effectif total de notre espèce par rapport aux ennemis et aux humains
- les effectifs humains à proximité : on privilégie des groupes d’humains les plus gros et les plus proches,
sans toutefois s’intéresser aux groupes plus nombreux que nous.
- les effectifs ennemis à proximité : même stratégie en observant le facteur 1.5. Si les ennemis sont 1.5 fois plus
nombreux que nous, l’heuristique prend en compte un malus de score.

L’heuristique est implémentée dans `heuristics/heuristic_2.py`.
