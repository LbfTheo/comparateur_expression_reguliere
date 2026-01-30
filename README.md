# Comparateur d'Expressions Régulières

Ce projet est un outil hybride (C et Python) permettant de vérifier l'équivalence mathématique de deux expressions régulières. 

Il fonctionne comme un **transpilateur** : l'analyseur syntaxique (C) lit les expressions régulières et génère un script Python qui construit les automates, les minimise et vérifie s'ils reconnaissent strictement le même langage.

## Fonctionnalités

* **Analyse Syntaxique :** Utilisation de Flex et Bison pour parser les expressions.
* **Transpilation :** Génération automatique d'un script Python (`main.py`) contenant la logique des automates.
* **Pipeline Automates complet (Python) :**
    * Conversion Regex → AFN (Automate Fini Non Déterministe).
    * Suppression des $\epsilon$-transitions.
    * Déterminisation (AFN → AFD).
    * Complétion et Minimisation.
    * **Test d'équivalence** par isomorphisme des automates minimaux.

## Technologies Utilisées

* **Flex** & **Bison** : Analyse lexicale et syntaxique.
* **C (GCC)** : Langage de l'analyseur généré.
* **Python 3** : Moteur de calcul des automates (`automate.py`).
* **Make** : Automatisation de la compilation.

## Prérequis

Assurez-vous d'avoir les outils suivants installés sur votre machine :
* `gcc`
* `make`
* `flex`
* `bison`
* `python3`

## Installation et Compilation

Grâce au `Makefile` inclus, la compilation est entièrement automatisée.

