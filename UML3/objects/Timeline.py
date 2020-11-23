# -*- coding:utf-8 -*-
from util.theme import *
from tkinter.messagebox import showwarning, showerror, askyesno
from util.importPIL import *
from util.widgets.MoveableObject import *
from util.constants.arrowTypes import *

class Timeline(MoveableObject):
    """
    Classe représentant une classe ou un objet dans l'espace UML.
    """
    
    __NEW_ID = 0
    
    def __init__(self, app, canvas, nom = "", style = "class"):
        """
        @param canvas : le Canvas qui contient cette ligne de temps d'objet de classe.
        @param nom = "": le nom de la ligne de temps d'objet de classe.
        """
        # super() :
        super().__init__(canvas)
        # Attributs normaux.
        self.__can = canvas
        self.__app = app
        self.__x = 0
        self.__y = 0
        self.__nom = nom
        self.__style = style
        self.ID = Timeline.__NEW_ID
        Timeline.__NEW_ID += 1

        self.__contenu = Frame(self.__can) # ?
        self.__window = Window(self.__can, 0, 0, window = self.__contenu, anchor = "nw")
        
        self.redraw()
    
    def __str__(self):
        return self.__class__.__name__ + " instance ("+super().__str__()+")"

    @staticmethod
    def resetIDCount():
        AbstractObject.__NEW_ID = 0

#    @staticmethod
#    def load(app, can, o):
#        type = o["type"]
#        if type == "ClassObject":
#            obj = ClassObject.load(app, can, o)
#        elif type == "InterfaceObject":
#            obj = InterfaceObject.load(app, can, o)
#        elif type == "EnumObject":
#            obj = EnumObject.load(app, can, o)
#        else:
#            raise ValueError("Type d'objet inconnu")
#        
#        obj.ID = o["id"]
#        obj.moveto(o["x"], o["y"])
#        return obj
#    
#    def save(self):
#        return {
#            "id":self.ID,
#            "type": self.__class__.__name__,
#            "name": self.__nom,
#            "x": self.__x,
#            "y": self.__y,
#            "attributs": [a.save() for a in self.__attributs],
#            "methodes":  [m.save() for m in self.__methodes]
#        }

    def redraw(self):
        """
        Permet de redessiner l'objet.
        """
        self.__contenu.destroy()
        # Cadre de la classe. Comme on peut le bouger (via l'héritage), ça m'a fait pensé
        # à une fenêtre, donc le nom de la couleur est windowbg et windowtitlebg.
        self.__contenu = Frame(self.__can, relief = SOLID, bd = 2, bg = getColor("%sbg"%self.__style))
        
        # Widget :
        self.__label_nom =       Label(self.__contenu, text = self.__nom, bg = getColor("%stitlebg"%self.__style))
        
        # et Placements :
        self.__label_nom.pack(      side = TOP, fill = X)
        
        # Auto-placement de la classe dans le canvas.
        self.__window = Window(self.__can, self.__x, self.__y, window = self.__contenu, anchor = "nw")
        self.addtag_withtag(self.__window)

#        # Menu du clic-droit :
#        self.rmenu = RMenu(self.__contenu, andInside = True)
#        self.rmenu.add_command(label = "Ajouter un attribut", command = self.ajouter_attribut)
#        self.rmenu.add_command(label = "Ajouter une méthode", command = self.ajouter_methode)
#        self.rmenu.createLink = Menu(self.rmenu, tearoff=0)
#        self.rmenu.createLink.add_command(label=DEPENDANCE,         command = lambda : self.beginLink(DEPENDANCE),         image = getImage("assets/textures/menu_icons/arrows/dependance.png"))
#        self.rmenu.createLink.add_command(label=ASSOCIATION,        command = lambda : self.beginLink(ASSOCIATION),        image = getImage("assets/textures/menu_icons/arrows/association_simple.png"))
#        self.rmenu.createLink.add_command(label=DOUBLE_ASSOCIATION, command = lambda : self.beginLink(DOUBLE_ASSOCIATION), image = getImage("assets/textures/menu_icons/arrows/association_double.png"))
#        self.rmenu.createLink.add_command(label=INHERITANCE,        command = lambda : self.beginLink(INHERITANCE),        image = getImage("assets/textures/menu_icons/arrows/heritage.png"))
#        self.rmenu.createLink.add_command(label=AGGREGATION,        command = lambda : self.beginLink(AGGREGATION),        image = getImage("assets/textures/menu_icons/arrows/aggregation.png"))
#        self.rmenu.createLink.add_command(label=COMPOSITION,        command = lambda : self.beginLink(COMPOSITION),        image = getImage("assets/textures/menu_icons/arrows/composition.png"))
#        self.rmenu.add_cascade(label = "Créer un lien", menu = self.rmenu.createLink)
#        self.rmenu.add_command(label = "Renommer", command = self.renommer)
#        self.rmenu.add_command(label = "Supprimer", command = self.supprimer)
        
        # Ajouter les bindings :
        self._addBindings()
    
    def getMinX(self): return self.__x
    def getMinY(self): return self.__y
    def getMaxX(self): return self.__x + self.__contenu.winfo_width()
    def getMaxY(self): return self.__y + self.__contenu.winfo_height()

    def _addBindings(self):
        self.__contenu        .bind("<Button-1>", lambda e: self.clic(), add=1)
        self.__label_nom      .bind("<Button-1>", lambda e: self.clic(), add=1)
    
    def clic(self):
        self.__app.onClicOnObject(self)
    
    def acceptLinkTo(self, obj):
        raise NotImplementedError
    
    def getLinkClassTo(self):
        raise NotImplementedError

    def moveto(self, x, y):
        """Permet de bouger l'objet à une coordonnée absolue."""
        self.moveby(x - self.__x, y - self.__y)

    def moveby(self, x, y):
        """Permet de bouger l'objet par une quantitée relative."""
        self.move(x, y)
        self.__x += x
        self.__y += y
        self.__app.updateLinks()
    
    def __signalerErreursWarnings(self, nom, firstIsLower = True):
        """
        Indique via une boîte de dialogue s'il y a des erreurs/warnings
        dans le nom d'un attribut/méthode/classe etc.
        @param firsIsLower : True pour les noms d'attributs/méthodes,
        False pour les noms de classes ou autres types.
        @return True s'il y a une erreur dans le nom et qu'il n'est pas valide,
        False sinon.
        """
        if not nom: # si la chaîne est vide, ce n'est pas valide.
            showerror("Mauvais nom", "Le nom ne peut pas être vide.")
            return True
        if not re.match("^[A-Za-z_]", nom[0]): # en première position ne sont que des lettres ou "_".
            showerror("Mauvais nom", "Caractère interdit en première position: %s"%(nom[0] if nom[0] != " " else '<espace>'))
            return True
        if not re.match("^[A-Za-z_][A-Za-z0-9_]*$", nom): # le reste ne peut être que des lettres, des chiffres ou "_".
            showerror("Mauvais nom", "Caractère interdit.")
            return True
        if not re.match("[a-z]", nom[0]) and firstIsLower: # si la première casse ne correspond pas, warning.
            showwarning("Nom déconseillé", "Par convention, il est déconseillé de commencer le nom par une Majuscule ou par \"_\"")
        elif not re.match("[A-Z]", nom[0]) and not firstIsLower:
            showwarning("Nom déconseillé", "Par convention, il est déconseillé de commencer le nom par une minuscule ou par \"_\"")
        return False

    def beginLink(self, type):
        self._linkType = type
        self.__app.beginLink(self, self.__x + self.__contenu.winfo_width()//2, self.__y + self.__contenu.winfo_height()//2)

    def supprimer(self, confirmation = True):
        """
        Permet de supprimer l'objet.
        @param confirmation : True si on doit demmander une confirmation
        à l'utilisateur, False sinon.
        """
        if not confirmation or askyesno("Confirmation ?", "Êtes-vous sûr(e) de vouloir réellement supprimer cette timeline à tout jamais ?"):
            self.__app.removeObject(self)
            self.delete()

    def renommer(self):
        """
        Permet de renommer la timeline.
        @return True si ça a bien été renommé, False sinon.
        """
        while True:
            nom = askString(None, "Nom ?", "Veuiller entrer un nom")
            if nom is None : return False # si on appuie sur annuler.
            if nom:
                if not self.__signalerErreursWarnings(nom, firstIsLower=False): break
        self.__nom = nom
        self.__label_nom.config(text = nom)
        return True

from .ClassObject import *
from .EnumObject import *
from .InterfaceObject import *
