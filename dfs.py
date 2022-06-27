from typing import Dict, List

from domino import Domino
from solver import Solver


class DFS(Solver):

    def __init__(self, N: int, start: int):
        super().__init__(N, start)

    def solve(self, graph: Dict[int, List[int]]):
        paths = []

        def DFSHelper(firstSide, path):
            nonlocal paths
            for secondSide in graph[firstSide]:
                domino = Domino(firstSide, secondSide)

                if domino not in path:
                    DFSHelper(secondSide, path + [domino])

            if len(path) > len(paths):
                paths = path

        DFSHelper(self.start, [])
        return paths
