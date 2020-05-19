# -*- coding:utf-8 -*-
import sys
from util.theme import *

from Application import *

def main(args):
    """Fonction main() de l'application globale."""
    app = Application()
    if THEME_ACTIF != "normal":
        app.tk_setPalette(background=getColor("bg"), foreground=getColor("fg")) # configuration du thème par défaut.
    if len(args) > 1:
        app.openfile(args[1])
    app.pack(expand = YES, fill = BOTH)
    app.mainloop()
    try:
        app.destroy()
    except:
        pass

main(sys.argv)