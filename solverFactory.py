from ants import AntColony
from dfs import DFS
from greedy import Greedy


class SolverFactory:
    @staticmethod
    def getSolver(name: str, args):
        N = int(args.N)
        start = int(args.start)
        if name == "greedy":
            return Greedy(N, start)
        if name == "dfs":
            return DFS(N, start)
        if name == "ants":
            return AntColony(float(args.alpha), float(args.beta), int(args.iter), N, start)