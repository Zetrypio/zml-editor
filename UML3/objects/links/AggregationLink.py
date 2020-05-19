# -*- coding:utf-8 -*-
import math

from util.util import *

from .AbstractLink import *

class AggregationLink(AbstractLink):
    def __init__(self, can, objA, objB):
        super().__init__(can, objA, objB)
    
    def _createLine(self):
        # Ligne parente :
        super()._createLine(width = 2, fill = "black")
        # Points de la flèche :
        a = self._points[-2]
        b = self._points[-1]
        # Distance :
        d = math.sqrt((b[1]-a[1])**2+(b[0]-a[0])**2)
        # Longueur sur la flèche qu'on veut :
        l1 = 24
        # Récupération de cette position :
        x1 = mymap(d-l1, 0, d, b[0], a[0])
        y1 = mymap(d-l1, 0, d, b[1], a[1])
        # Idem
        l2 = 0
        x2 = mymap(d-l2, 0, d, b[0], a[0])
        y2 = mymap(d-l2, 0, d, b[1], a[1])
        # Center point des 2 points :
        x = (x1+x2)/2
        y = (y1+y2)/2
        # Vector normal des 2 points :
        vx = (x1-x2)/(l2-l1)
        vy = (y1-y2)/(l2-l1)
        # Perpendiculaire :
        vx, vy = vy, -vx
        
        # Points 3 et 4 grace au center point et au vecteur perpendiculaire.
        l3 = 8
        x3 = x+l3*vx
        y3 = y+l3*vy
        x4 = x-l3*vx
        y4 = y-l3*vy
        
        # On trace notre bout de flèche :
        self._lines.append(self._can.create_polygon(x1, y1, x3, y3, x2, y2, x4, y4, width = 2, fill = "white", outline = "black"))
