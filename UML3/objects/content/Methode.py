# -*- coding:utf-8 -*-
from .AbstractContent import *

class Methode(AbstractContent):
    def __init__(self, master, nom, visibilitee, type, style, *argsTypes):
        self.argsTypes = argsTypes
        super().__init__(master, nom, visibilitee, type, style)
    
    def save(self):
        saving = super().save()
        saving["args"] = []
        for arg in self.argsTypes:
            saving["args"].append({"type":arg, "name":""}) # TODO
        return saving

    @staticmethod
    def load(master, style, o):
        return [Methode(master, m["name"], StringVar(value = m["visibility"]), StringVar(value = m["type"]), style, *[t["type"] for t in m["args"]])
                for m in o]

    def getCadre(self):
        return self.classe.getCadreMethodes()

    def updateText(self):
        prefix = {PUBLIC : "+",
                  PROTECTED : "#",
                  PACKAGE : "~",
                  PRIVATE : "-",
                  INNERCLASS : "$"
                  }
        self.label.config(text = prefix[self.visibility.get()]
                                +self.nom
                                +"("
                                +(",".join("%s %s"%((i[0], i[1]) for i in self.argsTypes)) if len(self.argsTypes) else "") 
                                +")"
                                +": "
                                +self.type.get())

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
            self.rmenu.type.add_radiobutton(variable = self.type, value = VOID   ,   command = self.updateText, label = "void")
            self.rmenu.type.add_separator()
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
            self.rmenu.add_command(label = "Supprimer la méthode %s"%self.nom, command = self.delete)
            self.rmenu.add_cascade(label = "Type", menu = self.rmenu.type)
            self.rmenu.add_cascade(label = "Visibilitée", menu = self.rmenu.visibilitee)



