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
        self.__newXPos = 100

        # Canvas des dessins global
        self.__can = Canvas(self, relief = SUNKEN, bd = 3)
        self.__can.pack(expand = YES, fill = BOTH)
        self.__can.bind_all("<Escape>",   lambda e:self.cancelLink(), add=1)
        self.__can.bind_all("<Button-1>", self.clic, add=1)
#        self.__can.bind("<Configure>", self.__onSizeChanged)

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

    def removeObject(self, object):
        self.__objects.remove(object)

    def beginLink(self, object, x, y):
        if self.__currentCreatingLink["id"] is not None:
            self.cancelLink()
        self.__currentCreatingLink = {
            "id": self.__can.create_line(x, y, x, y, fill="#00BB00", width = 2),
            "object": object,
            "x1": x,
            "y1": y,
            "binding": self.__can.bind("<Motion>", lambda e: self.__moveLink(e.x, e.y), add=1)
        }
        self.__moveLink(self.__can.winfo_pointerx() - self.__can.winfo_rootx(), self.__can.winfo_pointery() - self.__can.winfo_rooty())

        return True

    def __moveLink(self, x, y):
        # Si c'est pas en cours on annule rien.
        if self.__currentCreatingLink["id"] is None:
            return
        self.__can.coords(self.__currentCreatingLink["id"], self.__currentCreatingLink["x1"], self.__currentCreatingLink["y1"], x, y)

    def cancelLink(self):
        """Permet d'annuler la création d'un lien en cours."""
        # Si c'est pas en cours on annule rien.
        if self.__currentCreatingLink["id"] is None:
            return False
        # On debind et efface tout :
        self.__can.delete(self.__currentCreatingLink["id"])
        self.__can.unbind(self.__currentCreatingLink["binding"])

        # On reset les variables :
        self.__currentCreatingLink = {
            "id": None,
            "object": None,
            "x1": -1,
            "y1": -1,
            "binding": None,
        }
        return True

    def clic(self, event):
        if self.cancelLink(): return

    def onClicOnObject(self, obj):
        if self.__currentCreatingLink["id"] is not None:
            if self.__currentCreatingLink["object"].acceptLinkTo(obj):
                info("Création d'un lien de %s à %s."%(self.__currentCreatingLink["object"], obj))
                LinkType = self.__currentCreatingLink["object"].getLinkClassTo(obj)
                l = LinkType(self.__can, self.__currentCreatingLink["object"], obj)
                self.__links.append(l)
            else:
                showerror("Lien impossible", "Il est impossible de créer un lien de cette sorte entre ces 2 objets.")

    def updateLinks(self):
        for l in self.__links:
            l.redraw()

#    def __onSizeChanged(self, event):
#        pass

    def getSaveName(self):
        return "sequence"

    def new(self):pass
    def load(self, data):pass
