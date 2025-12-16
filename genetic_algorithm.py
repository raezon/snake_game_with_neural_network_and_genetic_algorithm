# genetic_algorithm.py
import random
from snake import Snake
from neural_network import NeuralNetwork

class GeneticAlgorithm:
    def __init__(self, size=50):
        self.size = size
        self.population = [Snake() for _ in range(size)]
        self.generation = 1
        self.best_fitness = 0
        self.history = []

    def evaluate(self):
        return True

    def select(self):
       
        return []

    def reproduce(self, selected):
        return []
