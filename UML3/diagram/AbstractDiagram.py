# -*- coding:utf-8 -*-
from util.theme import *

class AbstractDiagram(Canvas):
    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)
