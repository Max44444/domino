from random import random, choice
from typing import List, Dict
from copy import deepcopy

from domino import Domino
from solver import Solver


class AntColony(Solver):
    def __init__(self, alpha: float, beta: float, iterations: int, N: int, start: int):
        super().__init__(N, start)
        self._alpha = alpha
        self._beta = beta
        self._iterations = iterations
        self._k = 0.3
        self._q = (N + 1) * (N + 2)
        self._pheromones: List[List[float]] = [[]]

    def solve(self, graph: Dict[int, List[int]]):
        self._pheromones = [[0.1 for _ in range(self.size)] for _ in range(self.size)]

        for _ in range(self._iterations):
            paths = []

            for v in graph[self.start]:
                graphForAnt = deepcopy(graph)
                graphForAnt[self.start].remove(v)
                graphForAnt[v].remove(self.start)

                path = [Domino(self.start, v)]
                last = v

                while True:
                    weights = {next: self._getEdgeWight(graphForAnt, last, next) for next in graphForAnt[last]}

                    if not weights:
                        break

                    next = self._chooseVertex(weights)
                    path.append(Domino(last, next))

                    graphForAnt[last].remove(next)
                    graphForAnt[next].remove(last)

                    last = next

                paths.append(path)

            self._updatePheromones(paths)
        return self._choosePath(graph)

    def _updatePheromones(self, paths: List[List[Domino]]):
        self._pheromones = [[i * self._k for i in j] for j in self._pheromones]

        for path in paths:
            for domino in path:
                self._pheromones[domino.first][domino.second] += len(path) / self._q
                if not domino.isMirror():
                    self._pheromones[domino.second][domino.first] += len(path) / self._q

    def _getEdgeWight(self, graph: Dict[int, List[int]],  last: int, next: int):
        p = self._pheromones[last][next]
        connections = len([i for i in graph[next]])
        return p ** self._alpha * connections ** self._beta

    @staticmethod
    def _chooseVertex(weights: Dict[int, float]):
        total = sum([v for _, v in weights.items()])
        rand = random()

        for k, v in weights.items():
            rand -= v / total

            if rand <= 0:
                return k

        return choice(list(weights))

    def _choosePath(self, graph: Dict[int, List[int]]):
        result = []
        last = self.start

        while True:
            weights = {next: self._pheromones[last][next] for next in graph[last]}

            if not weights:
                break

            next = last if last in graph[last] else max(weights, key=weights.get)

            result.append(Domino(last, next))

            graph[last].remove(next)
            graph[next].remove(last)
            last = next

        return result
