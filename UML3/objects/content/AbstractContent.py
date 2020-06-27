# -*- coding:utf-8 -*-
from util.theme import *

from util.constants.typeList import *
from util.constants.visibility import *
from util.widgets.RMenu import *

class AbstractContent:
    """Classe représentant un contenu de classe comme un attribut ou une méthode."""
    def __init__(self, master, nom, visibilitee, modifiers, type, style):
        assert self.__class__ != AbstractContent
        # Attribut du parent :
        self.classe = master
        # Attributs normaux :
        self.__deleted = False
        self.nom = nom
        self.visibility = visibilitee
        self.modifiers = modifiers
        self.type = type
        self.__style = style
        
        self.redraw()
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    def save(self):
        return {
            "name": self.nom,
            "visibility": self.visibility.get(),
            "modifiers":self.getModifiers(),
            "type": self.type.get()
        }

    def getModifiers(self):
        modifiers = {}
        for m in self.modifiers:
            modifiers[m] = self.modifiers[m].get()
        return modifiers
    
    def getCadre(self):
        raise NotImplementedError

    def updateText(self):
        raise NotImplementedError

    def delete(self):
        if not self.__deleted:
            self.__deleted = True
            self.label.grid_forget()
            self.label.destroy()
            self.classe.removeAttribut(self)
            self.classe.redraw()
    
    def redraw(self):
        if not self.__deleted:
            # attributs graphiques
            italic = "italic" if self.modifiers.get("abstract", BooleanVar()).get() else ""
            underline = "underline" if self.modifiers.get("static", BooleanVar()).get() else ""
            font = "Arial 9 %s %s"%(italic, underline)
            self.label = Label(self.getCadre(), bg=getColor("%sbg"%self.__style), fg = getColor("fg"), font=font)
            self.label.grid(sticky = W)

            # setup label
            self.updateText()
            return True
        return False
