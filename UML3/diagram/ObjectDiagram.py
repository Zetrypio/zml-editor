# -*- coding: utf-8 -*-
from util.theme import *

from objects.AbstractObject import *
from objects.ClassObject import *
from objects.InterfaceObject import *

from util.widgets.RMenu import *
from util.log import * 

from .AbstractDiagram import *

class ObjectDiagram(AbstractDiagram):
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
        self.__rmenu.add_command(label = "Ajouter une Classe",    command = self.addClass)
        self.__rmenu.add_command(label = "Ajouter une Interface", command = self.addInterface)
        self.__rmenu.add_command(label = "Ajouter une Enum",      command = self.addEnum)
        
        # Liens en créations:
        self.__currentCreatingLink = None
        self.__currentCreatingLink_object = None
        self.__currentCreatingLink_x1 = -1
        self.__currentCreatingLink_y1 = -1
        self.__currentCreatingLink_binding = None
    
    "" # Note : Ces marques me servent uniquement pour que le repli de code de mon éditeur fasse ce que je veux.
    ##########################
    # Méthodes Pour Ajouts : #
    ##########################

    def addClass(self):
        """Permet d'ajouter une classe."""
        # On crée l'objet
        obj = ClassObject(self, self.__can)
        obj.moveto(self.winfo_pointerx()-self.winfo_rootx(), self.winfo_pointery()-self.winfo_rooty())
        self.__objects.append(obj)
        
        # Si on lui donne pas de nom, ça l'annule, sinon, ça l'ajoute :
        if not obj.renommer():
            obj.supprimer(confirmation = False)

    def addInterface(self):
        """Permet d'ajouter une interface."""
        # On crée l'objet
        obj = InterfaceObject(self, self.__can)
        obj.moveto(self.winfo_pointerx()-self.winfo_rootx(), self.winfo_pointery()-self.winfo_rooty())
        self.__objects.append(obj)
        
        # Si on lui donne pas de nom, ça l'annule, sinon, ça l'ajoute :
        if not obj.renommer():
            obj.supprimer(confirmation = False)

    def addEnum(self):
        """Permet d'ajouter une enum."""
        # On crée l'objet
        obj = EnumObject(self, self.__can)
        obj.moveto(self.winfo_pointerx()-self.winfo_rootx(), self.winfo_pointery()-self.winfo_rooty())
        self.__objects.append(obj)
        
        # Si on lui donne pas de nom, ça l'annule, sinon, ça l'ajoute :
        if not obj.renommer():
            obj.supprimer(confirmation = False)

    def removeObject(self, object):
        """Permet de supprimer un objet"""
        self.__objects.remove(object)
        for l in reversed(self.__links):
            if l.isLinkedTo(object):
                l.delete()
                self.__links.remove(l)
    ""
    #############################
    # Méthodes pour les liens : #
    #############################

    def beginLink(self, object, x, y):
        if self.__currentCreatingLink is not None:
            self.cancelLink()
        self.__currentCreatingLink_object = object
        self.__currentCreatingLink_x1 = x
        self.__currentCreatingLink_y1 = y
        self.__currentCreatingLink = self.__can.create_line(x, y, x, y, fill="#00BB00", width = 2)
        self.__currentCreatingLink_binding = self.__can.bind("<Motion>", lambda e: self.__moveLink(e.x, e.y), add=1)
        self.__moveLink(self.__can.winfo_pointerx() - self.__can.winfo_rootx(), self.__can.winfo_pointery() - self.__can.winfo_rooty())
    
    def __moveLink(self, x, y):
        # Si c'est pas en cours on annule rien.
        if self.__currentCreatingLink is None:
            return
        self.__can.coords(self.__currentCreatingLink, self.__currentCreatingLink_x1, self.__currentCreatingLink_y1, x, y)

    def cancelLink(self):
        """Permet d'annuler la création d'un lien en cours."""
        # Si c'est pas en cours on annule rien.
        if self.__currentCreatingLink is None:
            return False
        # On debind et efface tout :
        self.__can.delete(self.__currentCreatingLink)
        self.__can.unbind(self.__currentCreatingLink_binding)

        # On reset les variables :
        self.__currentCreatingLink = None
        self.__currentCreatingLink_object = None
        self.__currentCreatingLink_x1 = -1
        self.__currentCreatingLink_y1 = -1
        self.__currentCreatingLink_binding = None
        
        return True

    def clic(self, event):
        if self.cancelLink(): return

    def onClicOnObject(self, obj):
        if self.__currentCreatingLink is not None:
            if self.__currentCreatingLink_object.acceptLinkTo(obj):
                info("Création d'un lien de %s à %s."%(self.__currentCreatingLink_object, obj))
                LinkType = self.__currentCreatingLink_object.getLinkClassTo(obj)
                l = LinkType(self.__can, self.__currentCreatingLink_object, obj)
                self.__links.append(l)
            else:
                showerror("Lien impossible", "Il est impossible de créer un lien de cette sorte entre ces 2 objets.")
    
    def updateLinks(self):
        for l in self.__links:
            l.redraw()

    ""
    #####################################
    # Méthodes de la barre de menus de  #
    # manière spécifique à ce diagramme #
    #####################################
    
    def new(self):
        self.cancelLink()
        for o in reversed(self.__objects):
            o.delete()
            self.removeObject(o)
        self.__objects = []
        self.__links = []
        AbstractObject.resetIDCount()

    def getObjectWithID(self, id):
        for o in self.__objects:
            if o.ID == id:
                return o

