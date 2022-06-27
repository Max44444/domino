from abc import ABC, abstractmethod
from typing import List, Dict

class Solver(ABC):

    def __init__(self, N: int, start: int):
        if N < 0:
            raise Exception("N cannot be lower than zero")
        self.size = N + 1

        if start > N or 0 > start:
            raise Exception("Start point cannot be higher than %s or lower than zero" % N)
        self.start = start

    @abstractmethod
    def solve(self, graph: Dict[int, List[int]]):
        pass
