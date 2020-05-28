# -*- coding:utf-8 -*-
from util.theme import *
from util.log import *
from util.util import *

class AbstractLink:
    def __init__(self, can, objA, objB):
        assert self.__class__ != AbstractLink
        self._can = can
        self._objA = objA
        self._objB = objB
        self._points = []
        self._lines = []
        self.redraw()
    
    def save(self):
        return {
            "from": self._objA.ID,
            "to":   self._objB.ID,
            "type": self.__class__.__name__
        }

    @staticmethod
    def load(app, can, o):
        objA = app.getObjectWithID(o["from"])
        objB = app.getObjectWithID(o["to"])
        if o["type"] == "AggregationLink":
            cls = AggregationLink
        elif o["type"] == "AssociationLink":
            cls = AssociationLink
        elif o["type"] == "DependanceLink":
            cls = DependanceLink
        elif o["type"] == "DoubleAssociationLink":
            cls = DoubleAssociationLink
        elif o["type"] == "CompositionLink":
            cls = CompositionLink
        elif o["type"] == "InheritanceLink":
            cls = InheritanceLink
        elif o["type"] == "InterfaceImplementationLink":
            cls = InterfaceImplementationLink
        else:
            raise ValueError("Type de Lien Inconnu")
        return cls(can, objA, objB)
    
    def _calculatePoints(self):
        xminA = self._objA.getMinX()
        yminA = self._objA.getMinY()
        xmaxA = self._objA.getMaxX()
        ymaxA = self._objA.getMaxY()

        xminB = self._objB.getMinX()
        yminB = self._objB.getMinY()
        xmaxB = self._objB.getMaxX()
        ymaxB = self._objB.getMaxY()

        # Cas des coins :
        if   xminA > xmaxB and yminA > ymaxB:
            x1 = xminA
            y1 = yminA
            x2 = xmaxB
            y2 = ymaxB
        elif xmaxA < xminB and yminA > ymaxB:
            x1 = xmaxA
            y1 = yminA
            x2 = xminB
            y2 = ymaxB
        elif xmaxA < xminB and ymaxA < yminB:
            x1 = xmaxA
            y1 = ymaxA
            x2 = xminB
            y2 = yminB
        elif xminA > xmaxB and ymaxA < yminB:
            x1 = xminA
            y1 = ymaxA
            x2 = xmaxB
            y2 = yminB
        # Cas des bords :
        elif yminA > ymaxB:
            x1 = x2 = mymap(xminB, xminA-(xmaxB-xminB), xmaxA, xminA, xmaxA)
            y1 = yminA
            y2 = ymaxB
        elif ymaxA < yminB:
            x1 = x2 = mymap(xminB, xminA-(xmaxB-xminB), xmaxA, xminA, xmaxA)
            y1 = ymaxA
            y2 = yminB
        elif xminA > xmaxB:
            y1 = y2 = mymap(yminB, yminA-(ymaxB-yminB), ymaxA, yminA, ymaxA)
            x1 = xminA
            x2 = xmaxB
        elif xmaxA < xminB:
            y1 = y2 = mymap(yminB, yminA-(ymaxB-yminB), ymaxA, yminA, ymaxA)
            x1 = xmaxA
            x2 = xminB
        
        self._points = []
        self._points.append((x1, y1))
        self._points.append((x2, y2))
    
    def redraw(self):
        self.delete()
        self._createLine()
    
    def _createLine(self, **kwargs):
        self._calculatePoints()
        self._lines.append(self._can.create_line(*self._points, **kwargs))
    
    def delete(self):
        for l in self._lines:
            self._can.delete(l)
    
    def isLinkedTo(self, obj):
        return self._objA is obj or self._objB is obj

from .AggregationLink import *
from .AssociationLink import *
from .DependanceLink import *
from .DoubleAssociationLink import *
from .CompositionLink import *
from .InheritanceLink import *
from .InterfaceImplementationLink import *


