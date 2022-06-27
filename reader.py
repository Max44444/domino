from collections import defaultdict
from typing import List, Tuple, Dict

DOMINO_DELIMITER = ","
SIDES_DELIMITER = "x"

class Reader:
    def __init__(self, source: str):
        self._source = source

    def getGraphFromSource(self):
        if self._source == "console":
            return self._readFromConsole()
        elif self._source == "file":
            return self._readFromFile()
        else:
            raise Exception("Unknown source: %s" % self._source)

    def _readFromConsole(self):
        return self._parseDominos(input("Please enter the domino set, separate each domino by ',' and numbers on the "
                                        "domino by 'x' symbol:\n"))

    def _readFromFile(self):
        with open(input("Please entre the filename with the domino set:\n"), "r") as f:
            return self._parseDominos(f.readline())

    @staticmethod
    def _parseDominos(inputStr: str) -> Dict[int, List[int]]:
        chunks: List[str] = inputStr.strip().split(DOMINO_DELIMITER)
        dominos = [(int(chunk[0]), int(chunk[1])) for chunk in [i.strip().split(SIDES_DELIMITER) for i in chunks]]

        matrix = defaultdict(list)

        for (i, j) in dominos:
            matrix[i].append(j)
            matrix[j].append(i)

        return matrix
