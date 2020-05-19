# -*- coding:utf-8 -*-
from util.theme import *
import math

from util.widgets.Dialog import *
from util.log import *

inter = lambda l1, l2: (v for v in l1 if v in l2)

class DialogBuilder:
    __nativeTypes = ["boolean", "char", "byte", "short", "int", "long", "float", "double", "void"]
    def __init__(self, cls):
        """
        Basic dialog builder for user creation
        @param cls : class of the object to instanciate
        """
        assert issubclass(cls, object)
        self.__cls = cls
        self.__nom = "object"
        self.__leNom = "l'objet"
        self.__unNom = "un objet"
        self.__visibilitees = []
        self.__defautVisibilitee = "private"
        self.__typable = False
        self.__types = []
        self.__defautType = ""
        self.__modifiers = []
        self.__style = "class"
    
    def style(self, style):
        """
        Permet de configurer le style de l'objet à rajouter.
        @param style: le style à mettre sous forme de texte
        @return self for chaining
        """
        self.__style = style
        return self

    def name(self, nom, leNom, unNom):
        """
        Setter pour le nom de la chose à instancier.
        Utilisé dans le dialogue.
        @param nom : nom de l'objet (ex: "attribut")
        @param leNom : nom de l'objet avec un "le" (ex : "l'attribut")
        @param unNom : nom de l'objet avec un "un" (ex : "un attribut")
        @return self for chaining.
        """
        assert isinstance(nom, str)
        assert isinstance(leNom, str)
        assert isinstance(unNom, str)
        self.__nom = nom
        self.__leNom = leNom
        self.__unNom = unNom
        return self
    def visibilitee(self, *visibilitee):
        """
        Permet d'ajouter une visibilitée possible pour cette objet.
        Le choix de la visibilitée aparaîtra alors dans le dialogue pour l'utilisateur.
        @param *visibilitee : liste d'arguments correspondant aux visibilitées,
        sous forme de texte.
        @return self for chaining.
        """
        self.__visibilitees += visibilitee
        debug(self.__visibilitees)
        return self
    def visibiliteeDefaut(self, defautVisibilitee):
        """
        Permet de choisir la visibilitée par défaut.
        @param defautVisibilitee : la visibilitée par défaut sous forme de texte.
        @return self for chaining.
        """
        assert defautVisibilitee in self.__visibilitees
        self.__defautVisibilitee = defautVisibilitee
        return self
    def typable(self, typable):
        """
        Permet d'indiquer si l'objet est typable,
        une classe ne l'est pas par exemple.
        @param typable : True si l'objet est typable, False sinon.
        @return self for chaining
        """
        assert isinstance(typable, bool)
        self.__typable = typable
        return self
    def addTypes(self, *types):
        """
        Permet de choisir les types possibles pour cet objet.
        Ne pas confondre avec les types de généricité
        pour les classes comme ArrayList<?> par exemple.
        @param *types : liste d'arguments correspondants aux types,
        sous forme de texte.
        @return self for chaining.
        """
        self.__types += types
        return self
    def addPrimitiveTypes(self):
        """
        Permet d'ajouter automatiquement les types primitifs dans la liste des types possibles.
        @return self for chaining.
        """
        assert self.__typable
        self.__types += ["boolean", "char", "byte", "short", "int", "long", "float", "double"]
        return self
    def addVoidType(self):
        """
        Permet d'ajouter automatiquement le type void dans la liste des types possibles
        @return self for chaining
        """
        assert self.__typable
        self.__types.append("void")
        return self
    def typeDefaut(self, defautType):
        """
        Permet de choisir le type par défaut pour cet objet.
        @param defautType : le type par défaut, sous forme de texte.
        Doit être présent dans la liste des types.
        @return self for chaining.
        """
        assert isinstance(defautType, str)
        assert defautType in self.__types
        self.__defautType = defautType
        return self
    def modifiers(self, *modifiers):
        """
        Permet d'ajouter les modifiers, comme static, final, abstract, default, etc.
        @param modifiers : liste des modifiers, en tant que texte.
        @return self for chaining.
        """
        self.__modifiers += modifiers
        return self

    def create(self, master = None):
        """
        Méthode pour demander à l'utilisateur les informations
        nécéssaires pour créer et instancier un objet quelquonque.
        @param master : Objet contenant l'objet créé. Si il est null,
        il ne sera pas passé au constructeur.
        @return l'objet tout juste créé.
        """
        # Créer l'espace du dialogue :
        dialogue = Dialog(None, "Ajouter %s"%self.__unNom, ("Ok", "Annuler"))

        # Mettre des composants dessus :
        # Pour commencer, on demmande le nom (obligatoire).
        cadreNom = LabelFrame(dialogue, text = "Nom de %s"%self.__leNom)
        cadreNom.pack(side = TOP, expand =YES, fill = BOTH, padx = 5, pady = 5)
        etr = Entry(cadreNom)
        etr.pack(side = LEFT, expand =YES, fill = BOTH, padx = 5, pady = 5)

        # Mettre le choix de la visibilité: (facultatif)
        if len(self.__visibilitees):
            # Séparateur :
            Separator(dialogue, orient=HORIZONTAL).pack(side = TOP, fill = X)
            # On crée le cadre et les variable de calcul :
            cadreVisibilitee = LabelFrame(dialogue, text = "Visibilité de %s"%self.__leNom)
            cadreVisibilitee.pack(side = TOP, fill = X, padx = 5, pady = 5)
            varV = StringVar(value = self.__defautVisibilitee)
            # Calcul du nombre de lignes et colonnes pour garder une grille à peu près carrée :
            rows = math.ceil (math.sqrt(len(self.__visibilitees))/2)
            cols = math.floor(math.sqrt(len(self.__visibilitees))*2)
            if cols*rows < len(self.__visibilitees):
                cols += 1
            while (cols-1)*rows >= len(self.__visibilitees):
                cols -= 1

            # on crée/place les widgets :
            for i, v in enumerate(self.__visibilitees):
                Radiobutton(cadreVisibilitee, text = v, value = v, variable = varV).grid(row = i // cols, column = i % cols, sticky = "w")
            varV.set(self.__defautVisibilitee)
        
        # Mettre le choix des modifiers
        if len(self.__modifiers):
            # Séparateur :
            Separator(dialogue, orient=HORIZONTAL).pack(side = TOP, fill = X)
            # On crée le cadre et les variable de calcul :
            cadreModifiers = LabelFrame(dialogue, text = "Modifiers de %s"%self.__leNom)
            cadreModifiers.pack(side = TOP, fill = X, padx = 5, pady = 5)
            varsM = {}
            # Calcul du nombre de lignes et colonnes pour garder une grille à peu près carrée :
            rows = math.ceil (math.sqrt(len(self.__modifiers))/2)
            cols = math.floor(math.sqrt(len(self.__modifiers))*2)
            if cols*rows < len(self.__modifiers):
                cols += 1
            while (cols-1)*rows >= len(self.__modifiers):
                cols -= 1

            # on crée/place les widgets :
            for i, v in enumerate(self.__modifiers):
                var = BooleanVar(value=False)
                Checkbutton(cadreModifiers, text = v, variable = var).grid(row = i // cols, column = i % cols, sticky = "w")
                varsM[v] = var
        
        # Mettre le choix du type:
        if self.__typable:
            # Séparateur :
            Separator(dialogue, orient=HORIZONTAL).pack(side = TOP, fill = X)
            # On crée le cadre et les variable de calcul :
            cadreType = LabelFrame(dialogue, text = "Type de %s"%self.__leNom)
            cadreType.pack(side = TOP, fill = X, padx = 5, pady = 5)
            cadreTypeNatifs = Frame(cadreType)
            cadreTypeNatifs.pack(expand=YES, fill = BOTH, side = TOP)
            varT = StringVar(value = self.__defautType)
            # Calcul du nombre de lignes et colonnes pour garder une grille à peu près carrée :
            rows = math.ceil (math.sqrt(len(self.__types))/2)
            cols = math.floor(math.sqrt(len(self.__types))*2)
            if cols*rows < len(self.__types):
                cols += 1
            while (cols-1)*rows >= len(list(inter(self.__types, DialogBuilder.__nativeTypes))):
                cols -= 1

            # on crée/place les widgets :
            for i, t in enumerate(inter(self.__types, DialogBuilder.__nativeTypes)):
                Radiobutton(cadreTypeNatifs, text = t, value = t, variable = varT).grid(row = i // cols, column = i % cols, sticky = "w")
            
            # TODO : Mettre les types custom. Avec un combobox ?
            cbbTypes = Combobox(cadreType, values = [i for i in self.__types if not i in DialogBuilder.__nativeTypes], state="readonly", textvariable=varT)
            Label(cadreType, text="Autre objet :").pack(side=LEFT)
            cbbTypes.pack(side=LEFT, fill=X)
            varT.set(self.__defautType)
            

        # Activer puis récupérer le résultat pour le renvoyer
        if dialogue.activateandwait() == "Ok":
            options = {"nom" : etr.get(), "style":self.__style}
            if master is not None:          options["master"] = master
            if len(self.__visibilitees):    options["visibilitee"] = varV
            if self.__typable:              options["type"] = varT
            result = self.__cls(**options)
        else:
            result = None
        dialogue.destroy()
        return result

