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
        
        # Attributs normaux
        self.__objects = []
        self.__links = []
        self.__saveLocation = ""
        
        # Canvas des dessins global
        self.__can = Canvas(self, relief = SUNKEN, bd = 3)
        self.__can.pack(expand = YES, fill = BOTH)
        self.__can.bind_all("<Escape>",   lambda e:self.cancelLink(), add=1)
        self.__can.bind_all("<Button-1>", self.clic, add=1)
        
        # RMenu (menu clic-droit) :
        self.__menu = RMenu(self)
        self.__menu.add_command(label = "Ajouter une Classe",    command = self.addClass)
        self.__menu.add_command(label = "Ajouter une Interface", command = self.addInterface)
        self.__menu.add_command(label = "Ajouter une Enum",      command = self.addEnum)
        
        # Liens en créations:
        self.__currentCreatingLink = None
        self.__currentCreatingLink_object = None
        self.__currentCreatingLink_x1 = -1
        self.__currentCreatingLink_y1 = -1
        self.__currentCreatingLink_binding = None

        # Barre de Menus :
        self.__menubar = MenuBar(self.winfo_toplevel(), self)
        self.winfo_toplevel().configure(menu=self.__menubar)
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.quitter)
        try:
            self.winfo_toplevel().state("zoomed") # Windows Only
        except:
            pass
    
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
            self.cancelLink()
            for o in reversed(self.__objects):
                o.delete()
                self.removeObject(o)
            self.__objects = []
            self.__links = []
            self.__saveLocation = ""
            self.clearUndoStack()
            AbstractObject.resetIDCount()
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
        @param confirmation=True: True si on doit demander
        à l'utilisateur une confirmation d'enregistrement
        avant d'ouvrir un fichier, False sinon.
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

    def getObjectWithID(self, id):
        for o in self.__objects:
            if o.ID == id:
                return o
    
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


