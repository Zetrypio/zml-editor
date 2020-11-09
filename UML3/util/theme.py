# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
from colorsys import *
from util.theme import *
from tkinter.colorchooser import askcolor


def getColor(what):
    return THEME[getThemeActif()][what]

def getThemeActif():
    return THEME_ACTIF

def setThemeActif(theme):
    global THEME_ACTIF
    THEME_ACTIF = theme.lower()

THEME = {
    "normal": {
        "foreground": "#000000", "fg": "#000000",
        "background": "#EEEEEE", "bg": "#EEEEEE",
        "classtitlebg" : "beige",
        "classbg" : "beige",
        "enumtitlebg" : "#2bff60",
        "enumbg" : "#6aff8f",
        "interfacetitlebg" : "#B732FF",
        "interfacebg" : "#D47FFF"
    },
    "dark": {
        "foreground": "#AAAAAA", "fg": "#AAAAAA",
        "background": "#333333", "bg": "#333333",
        "classtitlebg" : "black",
        "classbg" : "#111111",
        "enumtitlebg" : "#004010",
        "enumbg" : "#005515",
        "interfacetitlebg" : "#2F004F",
        "interfacebg" : "#3F007F"
    },
    "aqua": {
        "foreground": "#003333", "fg": "#003333",
        "background": "#00AAAA", "bg": "#00AAAA",
        "classtitlebg" : "dark cyan",
        "classbg" : "cyan",
        "enumtitlebg" : "#2bff60",
        "enumbg" : "#6aff8f",
        "interfacetitlebg" : "#7D00CC",
        "interfacebg" : "#50007F"
    }
}

THEME_ACTIF = "dark"

# TH�ME :
style = Style()
#style.theme_use("clam")
style.configure(".",
    foreground=getColor("fg"),
    selectforeground=getColor("fg"),
    background=getColor("bg"),
    highlightbackground=getColor("bg"),
    )

def createTheme(name, col, dodarker = True):
    global THEME
    if dodarker:
        THEME[name] = {
            "foreground": darker(col), "fg": darker(col),
            "background": col, "bg": col,
            "windowtitlebg" : darker(darker(col)),
            "windowbg" : darker(col)
        }
    else:
        THEME[name] = {
            "foreground": brighter(col), "fg": brighter(col),
            "background": col, "bg": col,
            "windowtitlebg" : "black",
            "windowbg" : "#111111"
        }


def darker(col):
    r, g, b = getrgb(col)
    h, l, s = rgb_to_hls(r, g, b)
    l /= 1.3
    r, g, b = hls_to_rgb(h, l, s)
    return ("#%2x%2x%2x"%(r, g, b)).replace(" ", "0")

#try:
#    createTheme("candy", askcolor()[1])
#    setThemeActif("candy")
#except:
#    setThemeActif("dark")
