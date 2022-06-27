import argparse
import random
from collections import defaultdict
from copy import deepcopy
from typing import List, Tuple
from time import time

from ants import AntColony
from dfs import DFS
from domino import Domino
from greedy import Greedy
from reader import Reader
from solverFactory import SolverFactory

DOMINO_DELIMITER = ","
SIDES_DELIMITER = "x"
SPACE = " "

MAX_NUMBER_ON_SIDE = 7
START_NUMBER = 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--from", dest="source", metavar="", default="console", help="From where the program "
                                                                                           "can get the domino set ("
                                                                                           "Available options: "
                                                                                           "console, file). Default: "
                                                                                           "console")
    parser.add_argument("-m", "--method", dest="method", metavar="", default="greedy", help="Set algorithm for "
                                                                                            "solving the problem ("
                                                                                            "Available options: "
                                                                                            "greedy, dfs, "
                                                                                            "ants). Default: greedy")
    parser.add_argument("-n", "--n", dest="N", metavar="", default="6", help="Max number on the domino side. Default: 6")
    parser.add_argument("-s", "--start", dest="start", metavar="", default="1", help="Start number. Default: 1")
    parser.add_argument("-a", "--alpha", dest="alpha", metavar="", default="0.6", help="Pheromone significance factor "
                                                                                       "(ant colony only). Default: "
                                                                                       "0.6")
    parser.add_argument("-b", "--beta", dest="beta", metavar="", default="0.4", help="Heuristic function significance "
                                                                                     "factor (ant colony only). "
                                                                                     "Default: 0.4")
    parser.add_argument("-i", "--iterations", dest="iter", metavar="", default="10", help="number of iterations (ant "
                                                                                          "colony only). Default: 10")
    parser.add_argument("-e", "--experiment", dest="exp", default=False, help="Run in the experiment mode", action='store_true')
    args = parser.parse_args()

    if args.exp:
        experiment()
    else:
        reader = Reader(args.source)
        solver = SolverFactory.getSolver(args.method, args)

        solution = solver.solve(reader.getGraphFromSource())
        print(SPACE.join(map(str, solution)))
        print("Chain length: ", len(solution))


def generateSample(N: int, n: int):
    dominos = []

    for i in range(N + 1):
        for j in range(i, N + 1):
            dominos.append(Domino(i, j))

    sample = random.sample(dominos, n)
    graph = defaultdict(list)

    for d in sample:
        graph[d.first].append(d.second)
        graph[d.second].append(d.first)

    return graph


def experiment():
    def solutionLengthWithTimeExecution(solver, graph):
        startTime = time()
        solution = solver.solve(deepcopy(graph))
        return len(solution) + 1.0, time() - startTime

    def executionTime(data):
        times = [time for delta, time in data]
        return round(sum(times) / len(times), 4)

    def deviation(data):
        deltas = [delta for delta, time in data]
        return round(sum(deltas) / len(deltas) * 100, 2)

    for n in [6, 10, 14, 18]:
        result = defaultdict(list)

        for _ in range(5):
            sample = generateSample(6, n)
            start = random.randint(0, 6)

            l1, t1 = solutionLengthWithTimeExecution(Greedy(6, start), deepcopy(sample))
            l2, t2 = solutionLengthWithTimeExecution(DFS(6, start), deepcopy(sample))
            l3, t3 = solutionLengthWithTimeExecution(AntColony(0.6, 0.4, 10, 6, start), deepcopy(sample))

            l = max([l1, l2, l3])

            result["greedy"].append(((l - l1) / l, t1))
            result["dfs"].append(((l - l2) / l, t2))
            result["ants"].append(((l - l3) / l, t3))

        print("\n", "=" * 120)
        print("The experiment results for number of domino = ", n)
        print("Greedy algorithm:")
        print("average execution time: ", executionTime(result["greedy"]), "s\t average deviation from the best result: ", deviation(result["greedy"]), "%")
        print("DFS:")
        print("average execution time: ", executionTime(result["dfs"]), "s\t average deviation from the best result: ", deviation(result["dfs"]), "%")
        print("Ant colony algorithm:")
        print("average execution time: ", executionTime(result["ants"]), "s\t average deviation from the best result: ", deviation(result["ants"]), "%")
        print("=" * 120, "\n")




def parseDominos(inputStr: str) -> List[Tuple[int, int]]:
    chunks: List[str] = inputStr.strip().split(DOMINO_DELIMITER)
    return [(int(chunk[0]), int(chunk[1])) for chunk in [i.strip().split(SIDES_DELIMITER) for i in chunks]]


if __name__ == '__main__':
    main()
