# genetic_algorithm.py
import random
from snake import Snake
from neural_network import NeuralNetwork
from game import Game  # Nécessaire pour simuler les parties dans evaluate

class GeneticAlgorithm:
    def __init__(self, size=50):
        self.size = size
        self.population = [Snake() for _ in range(size)]
        self.generation = 1
        self.best_fitness = 0
        self.history = []

    def evaluate(self):
        """
        Fait jouer chaque serpent de la population et calcule sa fitness.
        """
        best_gen_fitness = 0
        
        for snake in self.population:
            # On s'assure que le serpent est prêt (utile si on réutilise des instances)
            # Bien que reproduce crée de nouvelles instances, c'est une sécurité.
            if not snake.alive:
                snake.reset()
            
            # Création de l'environnement de jeu pour ce serpent
            game = Game(snake)
            
            # Boucle de jeu rapide (sans affichage) jusqu'à la mort du serpent
            while snake.alive:
                game.update()
            
            # Calcul de la fitness une fois la partie terminée
            fitness = snake.calculate_fitness()
            
            # Mise à jour du meilleur score de la génération
            if fitness > best_gen_fitness:
                best_gen_fitness = fitness
        
        self.best_fitness = best_gen_fitness
        self.history.append(best_gen_fitness)
        print(f"Génération {self.generation} : Meilleure Fitness = {self.best_fitness:.2f}")

    def select(self):
        """
        Sélectionne les meilleurs serpents pour la reproduction.
        Ici, on trie la population par fitness et on garde les 20% meilleurs.
        """
        # Tri décroissant basé sur la fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Sélection du top 20% (ajustable)
        selection_size = max(2, int(self.size * 0.2))
        selected = self.population[:selection_size]
        
        return selected

    def reproduce(self, selected):
        """
        Crée la prochaine génération via crossover et mutation.
        """
        new_population = []
        
        # Élitisme : On garde les parents sélectionnés tels quels dans la nouvelle population
        # pour ne pas perdre les meilleures solutions trouvées.
        # Vous pouvez choisir de ne garder que le tout meilleur si vous préférez.
        new_population.extend([Snake(s.network) for s in selected]) # Copie propre des réseaux
        
        # Remplissage du reste de la population avec des enfants
        while len(new_population) < self.size:
            # Choix de deux parents au hasard parmi la sélection
            p1 = random.choice(selected)
            p2 = random.choice(selected)
            
            # Croisement des cerveaux (Réseaux de neurones)
            child_net = NeuralNetwork.crossover(p1.network, p2.network)
            
            # Mutation pour introduire de la variation
            child_net.mutate(rate=0.1)
            
            # Création du nouveau serpent enfant
            new_population.append(Snake(network=child_net))
            
        self.population = new_population
        self.generation += 1