# -*- coding:utf-8 -*-
from util.theme import *
from util.log import *
from util.util import *

class AbstractLink:
    def __init__(self, can, objA, objB):
        if self.__class__ == AbstractLink:
            raise RuntimeError("Can't instantiate abstract class AbstractLink directly.")
        self._can = can
        self._objA = objA
        self._objB = objB
        self._articulations = []
        self._points = []
        self._lines = []
        self.redraw()
        self._selected = False
        self._can.tag_bind(self.getTag(), "<ButtonPress-1>", lambda e: self._can.after_idle(lambda: self.__onClic(e)))

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

        # Valeurs par défaut pour éviter des crashs :
        x1 = xminA
        y1 = yminA
        x2 = xmaxB
        y2 = ymaxB

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
        tag = self.getTag()
        for line in self._lines:
            self._can.addtag_withtag(tag, line)

    def _createLine(self, **kwargs):
        self._calculatePoints()
        self._lines.append(self._can.create_line(*self._points, **kwargs))

    def delete(self):
        for l in self._lines:
            self._can.delete(l)

    def isLinkedTo(self, obj):
        return self._objA is obj or self._objB is obj

    def getTag(self):
        """
        Getter pour obtenir le tag qui est présent sur tout les éléments du trait.
        """
        return "link_%s"%id(self)

    def isSelected(self):
        return self._selected

    def deselect(self):
        self._selected = False
        self._can.itemconfigure(self.getTag(), fill="#000000")        

    def __onClic(self, event):
        if not self._selected:
            self._selected = True
            self._can.itemconfigure(self.getTag(), fill="#0078FF")

        # Ajout d'une articulation :
        else:
            self._articulations.append((event.x, event.y))
            
        return "break"


from .AggregationLink import *
from .AssociationLink import *
from .DependanceLink import *
from .DoubleAssociationLink import *
from .CompositionLink import *
from .InheritanceLink import *
from .InterfaceImplementationLink import *


