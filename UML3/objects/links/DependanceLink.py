# -*- coding:utf-8 -*-
from .AbstractLink import *

class DependanceLink(AbstractLink):
    def __init__(self, can, objA, objB):
        super().__init__(can, objA, objB)
    
    def _createLine(self):
        super()._createLine(width = 2, arrow = LAST, dash = 16)