# Partie 2 : Architecture de l’agent IA 

## 3.2 Questions d’architecture

### 1. Choix de l'architecture

**Choix : Agent Apprenant (Learning Agent)**
Plus spécifiquement, il s'agit d'une approche de **Neuroévolution** (Réseau de Neurones artificiel optimisé par Algorithme Génétique).

**Justification :**
* **Agent réactif simple :** Trop limité. Il ne réagit qu'à la case immédiatement adjacente. Il se retrouverait facilement bloqué dans des cul-de-sac ou des boucles infinies.
* **Agent à buts / Utilité :** Les algorithmes de recherche de chemin (A*, BFS) sont très coûteux en temps de calcul à chaque frame (surtout quand le serpent grandit).
* **Agent Apprenant :** C'est le choix idéal pour ce projet[cite: 493]. Il permet de généraliser des situations. Contrairement à un agent réactif qui a des règles "en dur" (if wall then turn), l'agent apprenant découvre lui-même des stratégies complexes (comme encercler la pomme ou zigzaguer) grâce à l'entraînement.

**Composants de l'architecture choisie[cite: 494]:**
1.  **Élément de performance (Le Cerveau) :** Un Réseau de Neurones (Neural Network) de type *Feed-Forward*. Il prend en entrée la "vision" du serpent (distances obstacles/pommes) et sort une direction.
2.  **Capteurs (Perception) :** Le système de vision qui scanne dans 8 directions (Haut, Bas, Gauche, Droite et diagonales) pour détecter les murs, le corps du serpent et la nourriture.
3.  **Critique (Fonction de Fitness) :** Elle évalue la qualité de la partie jouée (Score + Durée de vie). Elle ne dit pas *comment* jouer, mais *si* le résultat était bon.
4.  **Générateur d'apprentissage (Algorithme Génétique) :** Il modifie les composants de l'élément de performance (les poids du réseau) pour améliorer les résultats futurs.

---

### 2. Problématique d'apprentissage

**Problématique formulée :**
*"Apprentissage multi-objectifs : Équilibrer la prise de risque (Score) et la survie (Sécurité) dans un environnement dynamique."* [cite: 499]

**Explication de l'intérêt et du challenge[cite: 500]:**
Cette problématique est complexe car les deux objectifs sont souvent contradictoires :
* Pour maximiser le **Score**, le serpent doit prendre des risques, se déplacer rapidement vers la pomme et parfois passer dans des espaces étroits.
* Pour maximiser la **Sécurité**, le serpent aurait tendance à éviter les murs et à tourner en rond dans des espaces ouverts, quitte à ignorer la pomme.
* **Le challenge :** Si l'agent est trop prudent, il meurt de famine (compteur de mouvements épuisé). S'il est trop gourmand, il s'enferme et meurt. L'agent doit apprendre une planification implicite pour manger sans se bloquer pour le futur, alors que son corps grandit et modifie l'environnement en permanence.

---

### 3. Intégration avec l’algorithme génétique

**Combinaison de l'agent IA et de l'algorithme génétique[cite: 502]:**
L'agent IA (le Réseau de Neurones) est la structure "physique" qui prend les décisions. L'Algorithme Génétique est la méthode d'entraînement. On ne combine pas les deux en temps réel pendant le jeu, mais de manière cyclique : le GA agit *entre* les parties pour améliorer le cerveau de l'IA.

**Aspects optimisés génétiquement[cite: 503]:**
Ce sont les **Poids (Weights)** et les **Biais (Biases)** des connexions synaptiques du réseau de neurones. Ce sont ces valeurs numériques qui déterminent si le serpent décide de tourner à gauche ou à droite face à un mur.

**Schéma d'interaction[cite: 504]:**

1.  **Initialisation :** Création de N agents avec des cerveaux (poids) aléatoires.
2.  **Simulation (Jeu) :** Chaque agent joue sa partie de Snake de manière autonome en utilisant son réseau de neurones.
3.  **Évaluation :** À la mort du serpent, la fonction de Fitness calcule un score de performance.
4.  **Sélection & Reproduction (GA) :** L'algorithme génétique sélectionne les meilleurs cerveaux, croise leurs poids et applique des mutations.
5.  **Remplacement :** Les anciens agents sont remplacés par la nouvelle génération.
6.  **Boucle :** Retour à l'étape 2.

**Gestion du compromis Temps d'apprentissage / Performance[cite: 505]:**
* **Taille de population ajustée :** Une population trop grande (ex: 5000) ralentit l'apprentissage par génération. Une population trop petite (ex: 10) n'a pas assez de diversité. Une taille de 100 à 500 est un bon compromis.
* **Mécanisme de "Famine" (Starvation) :** Pour éviter que des serpents médiocres ne tournent en rond indéfiniment (ce qui allongerait inutilement le temps de simulation), on tue le serpent s'il ne mange pas de pomme après 100 mouvements. Cela force l'apprentissage rapide et réduit le temps de calcul.
* **Parallélisation :** Si possible, exécuter les parties des serpents en parallèle (multithreading) car elles sont indépendantes les unes des autres.