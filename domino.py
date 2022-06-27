class Domino(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return "[%d|%d]" % (self.first, self.second)

    def __eq__(self, other):
        return (self.first, self.second) == (other.first, other.second) \
               or (self.first, self.second) == (other.second, other.first)

    def isMirror(self):
        return self.first == self.second
