import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr : str ="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n : int = 1
        elif expr == "E":
            self.n : int = 1
        else:
            self.n : int = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final : list[int] = []
        elif expr == "E":
            self.final : list[int] = [0]
        else:
            self.final : list[int] = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition : dict[tuple[int, str] | tuple[tuple[int], str], list[int] | list[tuple[int]]] =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name : str = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0 : int, a : str, qlist: list):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})
    
    
def concatenation(a1 : automate, a2 : automate): 
    """Retourne l'automate qui reconnaît la concaténation des 
    langages reconnus par les automates a1 et a2"""
    #Ajouter une epsilon transition des anciens états finaux de a1 vers les états initiaux de a2
    for e_final in a1.final :
        a1.ajoute_transition(e_final, "E", [a1.n])
    
    #Ajouter les transitions de a2 dans l'automate a1
    for key, value in a2.transition.items():
        a1.ajoute_transition(a1.n+key[0], key[1], [a1.n+e for e in value])
    
    #Les états finaux de a1 ne sont plus finaux
    while len(a1.final) != 0:
        a1.final.pop()
    
    #Les états finaux de a2 deviennent les états finaux de a1
    for e_final in a2.final:
        a1.final.append(a1.n+e_final)
    
    #Mettre à jour le nombre d'état de l'automate
    a1.n += a2.n
    
    #Mettre à jour le nom de l'automate
    a1.name = "(" + a1.name.strip("()") + a2.name.strip("()") + ")"
    
    #Mettre à jour l'alphabet de l'automate
    for a in a2.alphabet:
        if a not in a1.alphabet:
            a1.alphabet.append(a)
    
    return a1


def union(a1 : automate, a2 : automate):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2"""
    #Initialisation de l'automate du language vide
    res = automate()
    
    #Determiner le nombre d'état de l'automate
    res.n = a1.n+a2.n+1
    
    #Determiner les états finaux de l'automate résultat
    res.final = [e+1 for e in a1.final] + [e+a1.n+1 for e in a2.final]
    
    #Ajout des epsilon transitions vers les deux automates
    res.ajoute_transition(0, "E", [1])
    res.ajoute_transition(0, "E", [a1.n+1])
    
    #Ajout des transitions de a1 dans res
    for key, value in a1.transition.items():
        res.ajoute_transition(key[0]+1, key[1], [e+1 for e in value])
    
    #Ajout des transitions de a2 dans res
    for key, value in a2.transition.items():
        res.ajoute_transition(key[0]+a1.n+1, key[1], [e+a1.n+1 for e in value] )
    
    #Mise à jour du nom de l'automate
    res.name = "(" +"[" + a1.name.strip("()") + "+" + a2.name.strip("()") + "]" +")"
    
    #Mettre à jour l'alphabet de l'automate
    res.alphabet = a1.alphabet
    for a in a2.alphabet:
        if a not in a1.alphabet:
            a1.alphabet.append(a)
    
    return res


def etoile(a : automate):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a"""
    for e_final in a.final :
        a.ajoute_transition(e_final, "E", [0])
    
    a.final.append(0)
    #Mise à jour du nom de l'automate
    a.name = "(" + "[" + a.name.strip("()") + "]" + "*" + ")"
    return a


def acces_epsilon(a : automate):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a : automate):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.alphabet = a.alphabet
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res
        
        
def determinisation(a: automate) -> automate:
    """
    Retourne l'automate équivalent déterministe.
    Tous les états sont accessibles.
    L'automate d'entrée ne doit pas contenir de epsilon-transitions.
    """
    # Supprimer les epsilon-transitions
    a_sans_e = supression_epsilon_transitions(a)
    
    # Initialiser l'automate déterministe
    res = automate()
    res.alphabet = a_sans_e.alphabet
    
    # Initialiser le tableau contenant tout les états pour le renommage des états
    tot_states : list[tuple[int, ...]] = []
    
    # État initial du déterminisé (tuple)
    initial = (0,)  # on part toujours de l'état initial 0 de l'AFN
    flag_setter: list[tuple[int, ...]] = [initial]
    seen_states: set[tuple[int, ...]] = {initial}
    
    # Ajouter état final si nécessaire
    if any(v in a_sans_e.final for v in initial) and initial not in res.final:
        res.final.append(initial)
    
    # Traitement des états accessibles
    while flag_setter:
        tmp_t = flag_setter.pop(0)
        for c in res.alphabet:
            tmp_arrival_set: set[int] = set()
            for v in tmp_t:
                if (v, c) in a_sans_e.transition:
                    tmp_arrival_set.update(a_sans_e.transition[(v, c)])
            
            if not tmp_arrival_set:
                continue  # pas de transition
            
            tmp_arrival = tuple(sorted(tmp_arrival_set))
            
            # Ajouter la transition
            res.ajoute_transition(tmp_t, c, [tmp_arrival])
            
            # Si l'état composé n'a pas déjà été vu
            if tmp_arrival not in seen_states:
                # Sauvegarder l'état dans la liste des états à traiter
                flag_setter.append(tmp_arrival)
                
                # Marquer l'état d'arrivé comme déjà vu
                seen_states.add(tmp_arrival)
                
                # Mettre à jour le nombre d'état total de l'automate
                res.n += 1
            
            # Ajouter état final si nécessaire
            if any(v in a_sans_e.final for v in tmp_arrival) and tmp_arrival not in res.final:
                res.final.append(tmp_arrival)
    
    # Renommage des états de l'automate
    tmp_translation = {state : code for code, state in enumerate(seen_states)}
    
    # Construction du dictionnaire de transition traduit
    tmp_transition = {(tmp_translation[key[0]], key[1]) : [tmp_translation[value[0]]] for key, value in res.transition.items()}
    
    # Construction de la liste des états finaux
    tmp_final = [tmp_translation[state] for state in res.final]
    
    # Remplacer la liste
    res.final = tmp_final
    
    # Remplacer le dictionnaire
    res.transition = tmp_transition
    
    #Mettre à jour le nom de l'automate
    res.name = a.name
    return res
    
    
def completion(a : automate):
    """ retourne l'automate a complété
        l'automate en entrée doit être déterministe
    """
    #Pour chacun des états ajouter une transition vers l'état poubelle s'il n'existe pas de transition avec c pour cet état de l'automate
    for state in range(a.n):
        for c in a.alphabet:
            if (state, c) not in a.transition.keys():
                a.ajoute_transition(state, c, [a.n])
    
    # Ajouter les boucles de l'état poubelle
    for c in a.alphabet:
        a.ajoute_transition(a.n, c, [a.n])
    
    #Mettre à jour le nombre d'automate de l'état
    a.n+=1
    return a


def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    
    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part
    # on réordonne la partition pour que le premier sous-ensemble soit celui qui contient l'état initial
    for i, e in enumerate(part):
        if 0 in e:
            part[0], part[i] = part[i], part[0]
            break
 
     
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res
    

def tout_faire(a : automate):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3) # Problème avec la minimisation de l'automate (ab)
    return a4


def egal(a1 : automate, a2 : automate):
    """ retourne True si a1 et a2 sont isomorphes
        a1 et a2 doivent être minimaux
    """
    # n'ont pas le même nombre d'états
    if a1.n != a2.n:
        return False
    
    # n'ont pas le même alphabet
    if a1.alphabet != a2.alphabet:
        return False
    
    # n'ont pas le même nombre d'état final
    if len(a1.final) != len(a2.final):
        return False
    
    # Dans cette partie on va déterminer f la fonction definie sur [0;a1.n] qui associe un état de a2 à un état de a1
    f = {0 : 0} # Initialiser -> f(état initial dans a1) = état initial dans a2

    for state in range(a1.n):
        for c in a1.alphabet:
            try :
                arrival_a1 = a1.transition[(state, c)][0]
            except KeyError :
                raise KeyError("L'automate a1 fourni n'est pas passé par la fonction tout_faire")
            try :
                arrival_a2 = a2.transition[(state, c)][0]
            except KeyError :
                raise KeyError("L'automate a2 fourni n'est pas passé par la fonction tout_faire")
            
            # l'état d'arrivé n'a pas encore d'image par f
            if arrival_a1 not in f:
                f[arrival_a1] = arrival_a2
            elif f[arrival_a1] != arrival_a2:
                    return False
    # pour chacun des états ei de a1, si ei est final dans a1 alors f[ei] est final dans a2
    for ei, fei in f.items():
        if (ei in a1.final) != (fei in a2.final):
            return False
    return True


# TESTS
# à écrire

def test_concatenation():
    a1 = automate("a")
    a2 = automate("b")
    res = concatenation(a1, a2)

    assert res.n == 4
    assert res.final == [3]
    assert (0, "a") in res.transition
    assert (1, "E") in res.transition
    assert (2, "b") in res.transition


def test_union():
    a1 = automate("a")
    a2 = automate("b")
    res = union(a1, a2)

    assert res.n == 5
    assert 1 in res.transition[(0, "E")]
    assert (0, "E") in res.transition
    assert set(res.final) == {2, 4}


def test_etoile():
    a = automate("a")
    res = etoile(a)

    assert 0 in res.final
    assert (1, "E") in res.transition
    assert res.transition[(1, "E")] == [0]

def test_determinisation():
    a1 = automate("a")
    a2 = automate("b")
    a3 = union(a1, a2)
    res = determinisation(a3)

    for (q, c), v in res.transition.items():
        assert len(v) == 1  # déterminisme


def test_completion():
    a = automate("a")
    a = determinisation(a)
    res = completion(a)

    for q in range(res.n):
        for c in res.alphabet:
            assert (q, c) in res.transition

    

def test_tout_faire():
    a1 = automate("a")
    a2 = automate("b")
    a = concatenation(a1, a2)
    res = tout_faire(a)

    for (q, c), v in res.transition.items():
        assert len(v) == 1  # automate déterministe


def test_egal():
    a1 = automate("a")
    a2 = automate("b")
    auto1 = tout_faire(concatenation(a1, a2))

    a3 = automate("a")
    a4 = automate("b")
    auto2 = tout_faire(concatenation(a3, a4))

    assert egal(auto1, auto2) is True

    
    
if __name__ == "__main__" :
    test_concatenation()
    test_union()
    test_etoile()
    test_determinisation()
    test_completion()
    test_tout_faire()
    test_egal()