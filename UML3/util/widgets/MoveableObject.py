#from Canvas import *
#from Canvas import Group as _Group, Window as _Window

## INTEGRATION MODULE Canvas : ##

# This module exports classes for the various canvas item types

# NOTE: This module was an experiment and is now obsolete.
# It's best to use the Tkinter.Canvas class directly.

from tkinter import Canvas, _cnfmerge, _flatten

class CanvasItem:
    def __init__(self, canvas, itemType, *args, **kw):
        self.canvas = canvas
        self.id = canvas._create(itemType, args, kw)
        if not hasattr(canvas, 'items'):
            canvas.items = {}
        canvas.items[self.id] = self
    def __str__(self):
        return str(self.id)
    def __repr__(self):
        return '<%s, id=%d>' % (self.__class__.__name__, self.id)
    def delete(self):
        del self.canvas.items[self.id]
        self.canvas.delete(self.id)
    def __getitem__(self, key):
        v = self.canvas.tk.split(self.canvas.tk.call(
                self.canvas._w, 'itemconfigure',
                self.id, '-' + key))
        return v[4]
    cget = __getitem__
    def __setitem__(self, key, value):
        self.canvas.itemconfig(self.id, {key: value})
    def keys(self):
        if not hasattr(self, '_keys'):
            self._keys = map(lambda x, tk=self.canvas.tk:
                             tk.splitlist(x)[0][1:],
                             self.canvas.tk.splitlist(
                                     self.canvas._do(
                                             'itemconfigure',
                                             (self.id,))))
        return self._keys
    def has_key(self, key):
        return key in self.keys()
    def __contains__(self, key):
        return key in self.keys()
    def addtag(self, tag, option='withtag'):
        self.canvas.addtag(tag, option, self.id)
    def bbox(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        return (x1, y1), (x2, y2)
    def bind(self, sequence=None, command=None, add=None):
        return self.canvas.tag_bind(self.id, sequence, command, add)
    def unbind(self, sequence, funcid=None):
        self.canvas.tag_unbind(self.id, sequence, funcid)
    def config(self, cnf={}, **kw):
        return self.canvas.itemconfig(self.id, _cnfmerge((cnf, kw)))
    def coords(self, pts = ()):
        flat = ()
        for x, y in pts: flat = flat + (x, y)
        return self.canvas.coords(self.id, *flat)
    def dchars(self, first, last=None):
        self.canvas.dchars(self.id, first, last)
    def dtag(self, ttd):
        self.canvas.dtag(self.id, ttd)
    def focus(self):
        self.canvas.focus(self.id)
    def gettags(self):
        return self.canvas.gettags(self.id)
    def icursor(self, index):
        self.canvas.icursor(self.id, index)
    def index(self, index):
        return self.canvas.index(self.id, index)
    def insert(self, beforethis, string):
        self.canvas.insert(self.id, beforethis, string)
    def lower(self, belowthis=None):
        self.canvas.tag_lower(self.id, belowthis)
    def move(self, xamount, yamount):
        self.canvas.move(self.id, xamount, yamount)
    def tkraise(self, abovethis=None):
        self.canvas.tag_raise(self.id, abovethis)
    raise_ = tkraise # BW compat
    def scale(self, xorigin, yorigin, xscale, yscale):
        self.canvas.scale(self.id, xorigin, yorigin, xscale, yscale)
    def type(self):
        return self.canvas.type(self.id)

class Arc(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'arc', *args, **kw)

class Bitmap(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'bitmap', *args, **kw)

class ImageItem(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'image', *args, **kw)

class Line(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'line', *args, **kw)

class Oval(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'oval', *args, **kw)

class Polygon(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'polygon', *args, **kw)

class Rectangle(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'rectangle', *args, **kw)

# XXX "Text" is taken by the Text widget...
class CanvasText(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'text', *args, **kw)

class Window(CanvasItem):
    def __init__(self, canvas, *args, **kw):
        CanvasItem.__init__(self, canvas, 'window', *args, **kw)

class Group:
    def __init__(self, canvas, tag=None):
        if not tag:
            tag = 'Group%d' % id(self)
        self.tag = self.id = tag
        self.canvas = canvas
        self.canvas.dtag(self.tag)
    def str(self):
        return self.tag
    __str__ = str
    def _do(self, cmd, *args):
        return self.canvas._do(cmd, (self.tag,) + _flatten(args))
    def addtag_above(self, tagOrId):
        self._do('addtag', 'above', tagOrId)
    def addtag_all(self):
        self._do('addtag', 'all')
    def addtag_below(self, tagOrId):
        self._do('addtag', 'below', tagOrId)
    def addtag_closest(self, x, y, halo=None, start=None):
        self._do('addtag', 'closest', x, y, halo, start)
    def addtag_enclosed(self, x1, y1, x2, y2):
        self._do('addtag', 'enclosed', x1, y1, x2, y2)
    def addtag_overlapping(self, x1, y1, x2, y2):
        self._do('addtag', 'overlapping', x1, y1, x2, y2)
    def addtag_withtag(self, tagOrId):
        self._do('addtag', 'withtag', tagOrId)
    def bbox(self):
        return self.canvas._getints(self._do('bbox'))
    def bind(self, sequence=None, command=None, add=None):
        return self.canvas.tag_bind(self.id, sequence, command, add)
    def unbind(self, sequence, funcid=None):
        self.canvas.tag_unbind(self.id, sequence, funcid)
    def coords(self, *pts):
        return self._do('coords', pts)
    def dchars(self, first, last=None):
        self._do('dchars', first, last)
    def delete(self):
        self._do('delete')
    def dtag(self, tagToDelete=None):
        self._do('dtag', tagToDelete)
    def focus(self):
        self._do('focus')
    def gettags(self):
        return self.canvas.tk.splitlist(self._do('gettags', self.tag))
    def icursor(self, index):
        return self._do('icursor', index)
    def index(self, index):
        return self.canvas.tk.getint(self._do('index', index))
    def insert(self, beforeThis, string):
        self._do('insert', beforeThis, string)
    def config(self, cnf={}, **kw):
        return self.canvas.itemconfigure(self.tag, _cnfmerge((cnf,kw)))
    def lower(self, belowThis=None):
        self._do('lower', belowThis)
    def move(self, xAmount, yAmount):
        self._do('move', xAmount, yAmount)
    def tkraise(self, aboveThis=None):
        self._do('raise', aboveThis)
    lift = tkraise
    def scale(self, xOrigin, yOrigin, xScale, yScale):
        self._do('scale', xOrigin, yOrigin, xScale, yScale)
    def select_adjust(self, index):
        self.canvas._do('select', ('adjust', self.tag, index))
    def select_from(self, index):
        self.canvas._do('select', ('from', self.tag, index))
    def select_to(self, index):
        self.canvas._do('select', ('to', self.tag, index))
    def type(self):
        return self._do('type')

_Group = Group # because before, I was doing: from Canvas import Group as _Group
_Window = Window

from ..log import *

# Correction d'un bug + ajout d'un fonctionnalité et/ou correction d'un autre bug
class Group(_Group):
    def __init__(self, canvas, tag = None):
        _Group.__init__(self, canvas, tag)
        self.__masters = []
        self.__listeDessins = []

    def bind(self, sequence=None, command=None, add = None):
        return self.canvas.tag_bind(self.id, sequence, command, add)

    def addtag_withtag(self, tagOrId):
        _Group.addtag_withtag(self, tagOrId)
        self.__listeDessins.append(tagOrId)
        if isinstance(tagOrId, Group):
            tagOrId._add_master(self)
        for g in self.__masters:
            g.addtag_withtag(tagOrId)

    def slaves(self):
        return self.__listeDessins[:]

    def _add_master(self, group):
        self.__masters.append(group)
    
    def tkraise(self, aboveThis=None):
        _Group.tkraise(self, aboveThis=aboveThis)
        self.canvas.tkraise(self)
        for e in self.__listeDessins:
            e.tkraise()

    def delete(self):
        for d in self.__listeDessins:
            try:
                d.delete()
            except:
                pass
        self.__listeDessins = []

class Window(_Window):
    def __init__(self, canvas, *args, **kwargs):
        try:
            window = kwargs["window"]
            del kwargs["window"]
        except:
            window = None
        _Window.__init__(self, canvas, *args, window = window, **kwargs)
        self.__window = window
    def slaves(self):
        return [self.__window]

class MoveableObject(Group):
    """Class that allow graphicals groups to move by the user's mouse"""
    def enableMouseControlling(self):
        debug("Enabling Mouse Controling for %s"%self)
        self.__b1=self.__bind_inside_of(self, "<ButtonPress-1>", self.__mouseControlling_Down)
        debug("Mouse down control ok on %s for %s"%(self.__b1, self))
        self.__b2=self.__bind_inside_of(self, "<B1-Motion>", self.__mouseControlling_Move)
        debug("Mouse move control ok on %s for %s"%(self.__b2, self))
        self.__b3=self.__bind_inside_of(self, "<ButtonRelease-1>", self.__mouseControlling_Up)
        debug("Mouse up control ok on %s for %s"%(self.__b3, self))
        self.__mousepressed = False

    def disableMouseControlling(self):
        self.__unbind_all(self.__b1)
        self.__unbind_all(self.__b2)
        self.__unbind_all(self.__b3)
        del self.__b1
        del self.__b2
        del self.__b3

    def rebind(self):
        try:
            debug("rebind")
            self.disableMouseControlling()
            debug("disabled ok")
            self.enableMouseControlling()
            debug("enabled ok")
        except e:
            debug(e)

    def __mouseControlling_Down(self,event):
        if not self.__mousepressed:
            self.__xa = event.x_root
            self.__ya = event.y_root
            #debug("Mouse down for %s at <%s, %s>"%(self, self.__xa, self.__ya))
            self.tkraise()
            self.__mousepressed = True
    def __mouseControlling_Move(self,event):
        self.moveby(event.x_root-self.__xa,event.y_root-self.__ya)
        self.__xa=event.x_root
        self.__ya=event.y_root
    def __mouseControlling_Up(self,event):
        if self.__mousepressed:
            del self.__xa
            del self.__ya
            self.__mousepressed = False
    def __bind_inside_of(self, widget, seq, func):
        try:
            binding = {widget: widget.bind(seq, func)}
            debug("binded : %s" % widget.__class__.__name__)
        except: # Widget has been destroyed
            return {}
        try:
            txt = widget.cget("text")
            debug("txt = %s"%txt)
        except:
            pass
        try:
            subwidget = widget.slaves()
            debug("slaves = %s"%subwidget)
        except:
            return binding
        for w in subwidget:
            binding.update(self.__bind_inside_of(w, seq, func))
        return binding
    def __unbind_all(self, allbindings):
        for w in allbindings:
            try:
                w.unbind(allbindings[w])
            except:
                pass

