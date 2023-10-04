# -*- coding:utf-8 -*-
from .links.AbstractLink import *
from .links.AssociationLink import *
from .links.DoubleAssociationLink import *
from .links.InheritanceLink import *
from .links.InterfaceImplementationLink import *
from .links.AggregationLink import *
from .links.CompositionLink import *

from .AbstractObject import *

from util.constants.arrowTypes import *
from util.log import *

class InterfaceObject(AbstractObject):
    def __init__(self, app, can, nom="NouvelleInterface"):
        super().__init__(app, can, nom, style = "interface")
        
        # Spécifications :
        (self._builderAttribut.visibilitee("package", "public")
                              .visibiliteeDefaut("public"))

        (self._builderMethode.modifiers("default")
                             .visibilitee("package", "public")
                             .visibiliteeDefaut("public"))
    
    @staticmethod
    def load(app, can, o):
        """Alternative constructor for loading from files."""
        return InterfaceObject(app, can, o["name"])
    
    def acceptLinkTo(self, obj):
        return isinstance(obj, InterfaceObject) if self._linkType == INHERITANCE else True
    
    def getLinkClassTo(self, obj):
        debug("Link type : %s"%self._linkType)
        if self._linkType == DEPENDANCE:
            return DependanceLink
        if self._linkType == ASSOCIATION:
            return AssociationLink
        if self._linkType == DOUBLE_ASSOCIATION:
            return DoubleAssociationLink
        if self._linkType == INHERITANCE:
            if isinstance(obj, InterfaceObject):
                return InheritanceLink
        if self._linkType == AGGREGATION:
            return AggregationLink
        if self._linkType == COMPOSITION:
            return CompositionLink
        # Default :
        warn("Link Class Type not Found, falling back to Association Link.")
        warn("It is either the Link Class does not exist or the link configuration was invalid.")
        return AssociationLink

    def redraw(self):
        super().redraw()
        
        # Correction, un interface n'ayants pas d'attributs privés,
        # ne peut donc pas faire de composition.
        self.rmenu.createLink.delete(self.rmenu.createLink.index(COMPOSITION))
        