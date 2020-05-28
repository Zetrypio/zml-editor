# -*- coding:utf-8 -*-
from .links.AbstractLink import *
from .links.DependanceLink import *
from .links.AssociationLink import *
from .links.DoubleAssociationLink import *
from .links.InheritanceLink import *
from .links.InterfaceImplementationLink import *
from .links.AggregationLink import *
from .links.CompositionLink import *

from .AbstractObject import *
from .InterfaceObject import *

from util.constants.arrowTypes import *
from util.log import *

class ClassObject(AbstractObject):
    def __init__(self, app, can, nom="NouvelleClasse"):
        super().__init__(app, can, nom)
        
        # Spécifications :
        (self._builderAttribut.visibilitee("private", "protected", "package", "public")
                              .visibiliteeDefaut("private"))

        (self._builderMethode.modifiers("abstract")
                             .visibilitee("private", "protected", "package", "public")
                             .visibiliteeDefaut("private"))
    
    @staticmethod
    def load(app, can, o):
        """Alternative constructor for loading from files."""
        return ClassObject(app, can, o["name"])
    
    def acceptLinkTo(self, obj):
        return True
    
    def getLinkClassTo(self, obj):
        debug("Link type : %s"%self._linkType)
        if self._linkType == DEPENDANCE:
            return DependanceLink
        if self._linkType == ASSOCIATION:
            return AssociationLink
        if self._linkType == DOUBLE_ASSOCIATION:
            return DoubleAssociationLink
        if self._linkType == INHERITANCE:
            if isinstance(obj, ClassObject):
                return InheritanceLink
            elif isinstance(obj, InterfaceObject):
                return InterfaceImplementationLink
        if self._linkType == AGGREGATION:
            return AggregationLink
        if self._linkType == COMPOSITION:
            return CompositionLink
        # Default :
        warn("Link Class Type not Found, falling back to Association Link.")
        warn("It is either the Link Class does not exist or the link configuration was invalid.")
        return AssociationLink
        