# -*- coding:utf-8 -*-


class AbstractDataFix:
    """
    Classe abstraite dont les sous-classes permettent de corriger les données
    qui viennent de fichiers de version antérieurs.
    """
    def __init__(self, fromVersion, toVersion=None):
        """
        Constructeur du correcteur de données.
        @param fromVersion: première version sur laquelle le fix peut être appliqué (inclue).
        @param toVersion: dernière version sur laquelle le fix peut être appliqué (inclue).
        Si toVersion n'est pas précisé, il est mis à la même valeur que fromVersion.
        """
        if toVersion is None:
            toVersion = fromVersion
        if toVersion < fromVersion:
            raise ValueError("fromVersion (=%s) must be <= to toVersion (=%s)"%(fromVersion, toVersion))
        self._fromVersion = fromVersion
        self._toVersion = toVersion

    def canBeApplied(self, version):
        """
        Permet de savoir si ce fix peut-être appliqué sur la version demandée.
        @param version: La version sur laquelle appliquer le fix.
        @return True si le fix peut-être appliqué, False sinon.
        """
        return version >= self._fromVersion and version <= self._toVersion

    def fixData(self, data):
        """
        Permet de corriger les données passées.
        Modifie l'instance originale, et la retourne également.
        @param data: Les données à corriger.
        @return les données corrigées.
        """
        raise NotImplementedError

    @staticmethod
    def fix(data):
        from .DataFixRegistry import REGISTRY
        version = float(data["version"])
        for fix in REGISTRY.getAllRegistries():
            if fix.canBeApplied(version):
                fix.fixData(data)

