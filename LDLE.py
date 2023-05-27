import matplotlib.pyplot as plt
import pprint
import pandas as pd
class Vertex:
    def __init__(self, tag, x=None, y=None, incident=[], v_type='n/a'):
        self.tag = tag
        self.x = x
        self.y = y
        self.incident = incident
        self.taip = v_type

    def __repr__(self):
        return f'{self.tag}<{self.taip}>({self.x}, {self.y}, {[i.label for i in self.incident]})'

    def toTuple(self):
        return (self.x, self.y)

    def plotter(self):
        types = {
            'n/a': 'o',
            'o': 'sg',  # start green square
            'e': 'sr',  # end red square
            's': '^k',
            'm': 'vy',
            'r': 'ob',
        }
        plt.plot(self.x, self.y, types[self.taip], label=self.tag)


class Edge:
    def __init__(self, start, end):
        self.start_point = start
        self.end_point = end

    def __repr__(self):
        return f'Edge({self.start_point}, {self.end_point})'

    def add2plot(self, color=''):  #Adding a segment to the current plot, using its start/end points and label if any
        plt.plot([self.start_point.x, self.end_point.x], [self.start_point.y, self.end_point.y], f'{color}-')


class SemiEdge:
    def __init__(self, label=None, start_point=None, prev=None, next=None, twin=None, face=None):
        self.label = label
        self.start_point = start_point
        self.prev = prev
        self.next = next
        self.twin = twin
        self.face = face

    def __repr__(self):
        if self.next:
            return f'{self.label}({self.start_point}, {self.next.start_point})'
        else:
            return f'{self.label}({self.start_point})'

    def add2plot(self, color=''):  #Adding a segment to the current plot, using its start/end points and label if any
        plt.plot([self.start_point.x, self.next.start_point.x], [self.start_point.y, self.next.start_point.y],
                 f'{color}-',
                 label=self.label)


class Face:
    def __init__(self, ext_frontier=[], inn_frontier=[]):
        self.ext_frontier = ext_frontier
        self.inn_frontier = inn_frontier

    def __repr__(self):
        return f'Face(inn: {self.inn_frontier}, ext: {self.ext_frontier})'


class LDLE:
    def __init__(self, vertices=[], semiedges=[], faces=[]):
        self.vertices = vertices
        self.semiedges = semiedges
        self.faces = faces