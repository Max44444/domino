from typing import Dict, List

from domino import Domino
from solver import Solver


class Greedy(Solver):

    def __init__(self, N: int, start: int):
        super().__init__(N, start)

    def solve(self, graph: Dict[int, List[int]]):
        connections = self._getConnectionDict(graph)
        result = []

        while True:
            last = result[-1].second if len(result) else self.start
            next = None

            if last in graph[last]:
                next = last
            else:
                for i in graph[last]:
                    if next is None or connections[i] > connections[next]:
                        next = i

            if next is None:
                break

            graph[last].remove(next)
            graph[next].remove(last)

            connections[last] -= 1
            connections[next] -= 1

            result.append(Domino(last, next))

        return result

    @staticmethod
    def _getConnectionDict(graph: Dict[int, List[int]]):
        return {i: len(j) for i, j in graph.items()}
