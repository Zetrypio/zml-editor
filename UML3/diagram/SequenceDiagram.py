# -*- coding:utf-8 -*-
from util.theme import *

from objects.Timeline import *

from util.widgets.RMenu import *
from util.log import * 

from .AbstractDiagram import *

class SequenceDiagram(AbstractDiagram):
    """Diagramme de séquence."""
    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)

        # Attributs normaux
        self.__objects = []
        self.__links = []
        self.__newXPos = 20

        # Canvas des dessins global
        self.__can = Canvas(self, relief = SUNKEN, bd = 3)
        self.__can.pack(expand = YES, fill = BOTH)
        self.__can.bind_all("<Escape>",   lambda e:self.cancelLink(), add=1)
        self.__can.bind_all("<Button-1>", self.clic, add=1)

        # RMenu (menu clic-droit) :
        self.__rmenu = RMenu(self)
        self.__rmenu.add_command(label = "Ajouter une timeline", command = self.addTimeline)

        # Liens en créations:
        self.__currentCreatingLink = {
            "id": None,
            "object": None,
            "x1": -1,
            "y1": -1,
            "binding": None,
        }

    def addTimeline(self):
        obj = Timeline(self, self.__can)
        obj.moveto(self.__newXPos, 20)
        self.__newXPos += 100
        self.__objects.append(obj)
        
        # Si on lui donne pas de nom, ça l'annule, sinon, ça l'ajoute :
        if not obj.renommer():
            obj.supprimer(confirmation = False)

    def getSaveName(self):
        return "sequence"

    def updateLinks(self):pass
    def onClicOnObject(self, object):pass
    def clic(self, e=None):pass
    def new(self):pass
    def load(self, data):pass
