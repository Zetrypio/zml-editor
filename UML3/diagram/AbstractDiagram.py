# -*- coding:utf-8 -*-
from util.theme import *

class AbstractDiagram(Canvas):
    def __init__(self, master = None, **kwargs):
        if self.__class__ == AbstractDiagram:
            raise RuntimeError("Can't instantiate abstract class AbstractDiagram directly.")
        super().__init__(master, **kwargs)
