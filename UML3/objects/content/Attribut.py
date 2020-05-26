# -*- coding:utf-8 -*-
from util.theme import *

from util.constants.typeList import *
from util.constants.visibility import *
from util.widgets.RMenu import *

from .AbstractContent import *

class Attribut(AbstractContent):
    """Classe représentant un attribut."""
    def __init__(self, master, nom, visibilitee, type, style):
        super().__init__(master, nom, visibilitee, type, style)
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    @staticmethod
    def load(master, style, o):
        return [Attribut(master, a["name"], StringVar(value = a["visibility"]), StringVar(value = a["type"]), style)
                for a in o]
    
    def getCadre(self):
        return self.classe.getCadreAttributs()

    def updateText(self):
        prefix = {PUBLIC : "+",
                  PROTECTED : "#",
                  PACKAGE : "~",
                  PRIVATE : "-",
                  INNERCLASS : "$"
                  }
        self.label.config(text = prefix[self.visibility.get()]+self.nom+": "+self.type.get())
    
    def redraw(self):
        if super().redraw():
            # Menus (clic droit):
            self.rmenu = RMenu(self.label)
            self.rmenu.visibilitee = Menu(self.rmenu, tearoff=False)
            self.rmenu.visibilitee.add_radiobutton(variable = self.visibility, value = PRIVATE  , command = self.updateText, label = "Private")
            self.rmenu.visibilitee.add_radiobutton(variable = self.visibility, value = PROTECTED, command = self.updateText, label = "Protected")
            self.rmenu.visibilitee.add_radiobutton(variable = self.visibility, value = PUBLIC   , command = self.updateText, label = "Public")
            self.rmenu.visibilitee.add_radiobutton(variable = self.visibility, value = PACKAGE  , command = self.updateText, label = "Package")
            self.rmenu.type = Menu(self.rmenu, tearoff=False)
            self.rmenu.type.add_radiobutton(variable = self.type, value = BOOLEAN,   command = self.updateText, label = "boolean")
            self.rmenu.type.add_separator()
            self.rmenu.type.add_radiobutton(variable = self.type, value = CHAR   ,   command = self.updateText, label = "char")
            self.rmenu.type.add_radiobutton(variable = self.type, value = BYTE   ,   command = self.updateText, label = "byte")
            self.rmenu.type.add_radiobutton(variable = self.type, value = SHORT  ,   command = self.updateText, label = "short")
            self.rmenu.type.add_radiobutton(variable = self.type, value = INT    ,   command = self.updateText, label = "int")
            self.rmenu.type.add_radiobutton(variable = self.type, value = LONG   ,   command = self.updateText, label = "long")
            self.rmenu.type.add_separator()
            self.rmenu.type.add_radiobutton(variable = self.type, value = FLOAT  ,   command = self.updateText, label = "float")
            self.rmenu.type.add_radiobutton(variable = self.type, value = DOUBLE ,   command = self.updateText, label = "double")
            self.rmenu.type.add_separator()
            self.rmenu.type.add_radiobutton(variable = self.type, value = OBJECT ,   command = self.updateText, label = "object")
            self.rmenu.add_command(label = "Renommer")
            self.rmenu.add_command(label = "Supprimer l'attribut %s"%self.nom, command = self.delete)
            self.rmenu.add_cascade(label = "Type", menu = self.rmenu.type)
            self.rmenu.add_cascade(label = "Visibilitée", menu = self.rmenu.visibilitee)



