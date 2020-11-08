# -*- coding:utf-8 -*-
import os
import json
from tkinter.messagebox import showerror, askyesnocancel
from tkinter.filedialog import askopenfilename, asksaveasfilename
from util.theme import *

from diagram.ObjectDiagram import *

from objects.AbstractObject import *
from objects.ClassObject import *
from objects.InterfaceObject import *

from util.widgets.RMenu import *
from util.log import * 

from MenuBar import *

class Application(Frame):
    """Classe principale de l'application globale tout entière."""
    def __init__(self, master = None, **args):
        """Constructeur de l'application."""
        super().__init__(master, **args)

        # Attributs normaux :
        self.__saveLocation = ""

        # Diagrams :
        self.__diagram = ObjectDiagram(self)
        self.__diagram.pack(expand = YES, fill = BOTH)

        # Barre de Menus :
        self.__menubar = MenuBar(self.winfo_toplevel(), self)
        self.winfo_toplevel().configure(menu=self.__menubar)
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.quitter)
        try:
            self.winfo_toplevel().state("zoomed") # Windows Only
        except:
            pass
    ""
    ##################################
    # Méthodes pour barre de Menus : #
    ##################################

    def new(self, confirmation = True):
        """
        Permet de créer un nouveau fichier.
        @param confirmation=True: True si on doit demander
        à l'utilisateur une confirmation d'enregistrement
        avant de créer un nouveau fichier, False sinon.
        @return True si le fichier a été créé avec succès, False sinon.
        """
        if not confirmation or self.confirmation("de créer un nouveau fichier"):
            self.__diagram.new()
            self.__saveLocation = ""
            self.clearUndoStack()
            return True
        return False

    def open(self, confirmation = True):
        """
        @param confirmation=True: True si on doit demander
        à l'utilisateur une confirmation d'enregistrement
        avant d'ouvrir un fichier, False sinon.
        @return True si le fichier a été ouvert avec succès, False sinon.
        """
        if not confirmation or self.confirmation("d'ouvrir un fichier"):
            location = askopenfilename(title="Ouvrir un fichier", filetypes = [("Fichiers ZML","*.zml"),
                                                                               ("Fichiers UCLS","*.ucls"),
                                                                               ("Fichiers QModel","*.qmodel"),
                                                                               ("Fichiers UML","*.uml"),
                                                                               ("Tout les fichiers UML supportés", "*.zml;*.ucls;*.qmodel;*.uml;")])
            return self.openfile(location)
        return False

    def openfile(self, loc):
        """
        @param loc : Chemin du fichier à ouvrir.
        @return True si le fichier a été ouvert avec succès, False sinon.
        """
        if self.new(confirmation=False):
            debug(loc)
            try:
                self.__saveLocation = ""
                if loc.endswith(".zml"):
                    self.__saveLocation = loc
                    with open(self.__saveLocation, "r", encoding="utf-8") as f:
                        loading = json.load(f)
                    if loading["version"] > 1.0 or loading["version"] < 1.0:
                        raise ValueError("Version du fichier non supportée.")
                    elif loading["version"] == 1.0:
                        for o in loading["objects"]:
                            self.__objects.append(AbstractObject.load(self, self.__can, o))
                        for l in loading["links"]:
                            self.__links.append(AbstractLink.load(self, self.__can, l))
                        # Reset des IDs dans le bon ordre :
                        for id, o in enumerate(self.__objects):
                            o.ID = id
                    self.after(100, self.updateLinks)
                else:
                    raise ValueError("Format de fichier non compatible.\nCe format de fichier n'est pas supporté pour le moment.")
            except Exception as e:
                self._report_exception()
                showerror("Erreur à l'ouverture du fichier", "Erreur à l'ouverture du fichier : \n%s"%err(e))
                return False
            return True
        return False

    def save(self, checklocation = True):
        """
        @param confirmation=True: True si on doit demander
        à l'utilisateur une confirmation d'enregistrement
        avant d'ouvrir un fichier, False sinon.
        @return True si le fichier a été ouvert avec succès, False sinon.
        """
        # Si l'application n'as pas de lieu d'enregistrement, on demande :
        if not self.__saveLocation or (checklocation and not os.path.exists(self.__saveLocation)):
            return self.saveas()
        try:
            # On obtient les données :
            saving = {
                "version": 1.0,
                "objects":[],
                "links":[]
            }
            for o in self.__objects:
                saving["objects"].append(o.save())
            for l in self.__links:
                saving["links"].append(l.save())

            # On enregistre :
            with open(self.__saveLocation, "w", encoding="utf-8") as f:
                json.dump(saving, f)

        except Exception as e:
            showerror("Erreur à la sauvegarde du fichier", "Erreur à l'enregistrement du fichier : \n%s"%err(e))
            return False
        return True

    def saveas(self):
        """
        @param confirmation=True: True si on doit demander
        à l'utilisateur une confirmation d'enregistrement
        avant d'ouvrir un fichier, False sinon.
        @return True si le fichier a été ouvert avec succès, False sinon.
        """
        location = asksaveasfilename(title="Enregistrer un fichier", filetypes= [("Fichiers ZML","*.zml")], defaultextension=".zml")
        if not location: return False
        self.__saveLocation = location
        return self.save(checklocation = False)

    def restart(self, confirmation = True):
        if not confirmation or self.confirmation("de restart"):
            self.quitter(confirmation = False)
            if self.__saveLocation:
                os.startfile(self.__saveLocation)
            else:
                os.startfile(sys.argv[0])

    def quitter(self, confirmation = True):
        if not confirmation or self.confirmation("de quitter"):
            self.quit()
            pass

    def confirmation(self, action):
        if self.hasChangeSinceLastSave():
            rep = askyesnocancel("Confirmation ?", "Voulez-vous enregistrer avant %s ?"%action)
            if rep is True:
                self.save()
            if rep is None:
                return False
        return True

    ""
    #####################################
    # Méthodes pour Undo Redo :         #
    # (Raccourcis vers le gestionnaire)?#
    #####################################

    def undo(self):
        pass

    def redo(self):
        pass

    def hasChangeSinceLastSave(self):
        return True

    def addUndoableAction(self, action):
        pass

    def clearUndoStack(self):
        # Si on peut plus undo, on peut plus redo non plus.
        self.clearRedoStack()

    def clearRedoStack(self):
        pass

    ""
    #################################
    # Méthode pour les sélections : #
    #################################

    def addToSelection(self, obj):
        pass

    def getSelection(self):
        pass

    def clearSelection(self):
        pass

    def selectOnly(self, obj):
        self.clearSelection()
        self.addToSelection(obj)

    ""
    #####################################
    # Méthodes pour Copier-Coller :     #
    # (Raccourcis vers le gestionnaire) #
    #####################################

    def copy(self):
        pass

    def cut(self):
        pass

    def paste(self):
        pass


