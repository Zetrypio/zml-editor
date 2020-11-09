# -*- coding:utf-8 -*-

from .SimpleToMultipleDiagram import *

class DataFixRegistry:
    def __init__(self):
        self.__registry = []
        self.__registry.append(SimpleToMultipleDiagram())

    def getAllRegistries(self):
        return self.__registry[:]

REGISTRY = DataFixRegistry()
