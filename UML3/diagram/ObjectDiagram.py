# -*- coding: utf-8 -*-
from .AbstractDiagram import *

class ObjectDiagram(AbstractDiagram):
    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)
