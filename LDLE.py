class Vertex:
    def __init__(self, x, y, semiedge=None):
        self.coord = (x, y)
        self.semiedge = semiedge

class Semiedge:
    def __init__(self, origin = None, twin = None, next= None, prev = None, face = None):
        self.origin = origin
        self.twin = twin
        self.next = next
        self.prev = prev
        self.face = face

class Face:
    def __init__(self, outerSemiEdge = None, innerSemiEdge = None):
        self.outerSemiEdge = outerSemiEdge
        self.innerSemiEdge = innerSemiEdge