# -*- coding:utf-8 -*-
from util.theme import *

from util.log import * 

from .AbstractDiagram import *

class SequenceDiagram(AbstractDiagram):
    """Diagramme de séquence."""
    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Attributs normaux
        self.__objects = []
        self.__links = []
        
        # Canvas des dessins global
        self.__can = Canvas(self, relief = SUNKEN, bd = 3)
        self.__can.pack(expand = YES, fill = BOTH)
        self.__can.bind_all("<Escape>",   lambda e:self.cancelLink(), add=1)
        self.__can.bind_all("<Button-1>", self.clic, add=1)
        
        # RMenu (menu clic-droit) :
        self.__rmenu = RMenu(self)
        self.__rmenu.add_command(label = "Ajouter un objet", command = self.addClass)
        
        # Liens en créations:
        self.__currentCreatingLink = {
            "id": None,
            "object": None,
            "x1": -1,
            "y1": -1,
            "binding": None,
        }
        