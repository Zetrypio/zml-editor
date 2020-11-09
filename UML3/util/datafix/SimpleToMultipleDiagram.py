# -*- coding:utf-8 -*-

from .AbstractDataFix import *

class SimpleToMultipleDiagram(AbstractDataFix):
    """
    Permet de corriger le fait que dans la version 1.0, il n'y a qu'un seul type de diagrams possibles.
    """
    def __init__(self):
        super().__init__(1.0)

    def fixData(self, data):
        data["diagrams"] = {
            "objects":{
                "objects": data["objects"],
                "links"  : data["links"]
            }
        }
        del data["objects"]
        del data["links"]
