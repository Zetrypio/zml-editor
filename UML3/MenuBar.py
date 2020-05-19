# -*- coding:utf-8 -*-
from util.theme import *

class MenuBar(Menu):
    def __init__(self, master = None, app = None, **kwargs):
        super().__init__(master, **kwargs)
        self.__app = app
        
        self.__menuFichier = Menu(self, tearoff=False)
        
        self.__menuFichier.add_command(accelerator = "Ctrl-N",     command = self.__app.new,     label="Nouveau")
        self.__menuFichier.add_command(accelerator = "Ctrl-O",     command = self.__app.open,    label="Ouvrir...")
        self.__menuFichier.add_command(accelerator = "Ctrl-S",     command = self.__app.save,    label="Enregistrer")
        self.__menuFichier.add_command(accelerator = "Ctrl-Maj-S", command = self.__app.saveas,  label="Enregistrer sous...")
        self.__menuFichier.add_separator()
        self.__menuFichier.add_command(accelerator = "Ctrl-R",     command = self.__app.restart, label="Restart")
        self.__menuFichier.add_command(accelerator = "Ctrl-Q",     command = self.__app.quitter, label="Quitter")
        
        self.add_cascade(label = "Fichier", menu = self.__menuFichier)