
from util.theme import *

if __name__ != '__main__':
    import __main__
    if "ttk" in dir(__main__):
        from tkinter.ttk import *


def use_ttk():
    global Scrollbar
    from tkinter.ttk import Scrollbar as scrb
    Scrollbar = scrb


class ScrolledCanvas(Canvas):
    def __init__(self, master=None, scrollregion = None, **args):
        self.__frame = Frame(master)
        Canvas.__init__(self, self.__frame, scrollregion = scrollregion or (0,0,100,100),**args)
        self.__scroll_horiz = Scrollbar(self.__frame, orient = HORIZONTAL, command = self.xview)
        self.__scroll_verti = Scrollbar(self.__frame, orient = VERTICAL, command = self.yview)
        self.grid(column = 0, row = 0, sticky="nesw")
        self.__scroll_horiz.grid(column = 0, row = 1, sticky = "ew")
        self.__scroll_verti.grid(column = 1, row = 0, sticky = "ns")
        self.configure(xscrollcommand = self.__scroll_horiz.set, yscrollcommand = self.__scroll_verti.set)
        # nécéssaire
        self.__canstarted = False
        self.__started = False
        self.bind("<Configure>", self.__redim)
        self.__frame.bind("<Configure>", self.__canredim)
        # redirection des méthodes de placement.
        for i in dir(Grid)+dir(Place)+dir(Pack):
            exec("self.%s = self._ScrolledCanvas__frame.%s"%(i,i))
        self.__redim()

    def __canredim(self, event = None):
        if not self.__canstarted :
            self.__canstarted = True
            return
        larg, haut = self.__frame.winfo_width(), self.__frame.winfo_height()
        larg-=21
        haut-=21
        self.config(width = larg, height = haut)

    def __redim(self, event = None):
        if not self.__started:
            self.__started = True
            return
        larg, haut = self.winfo_width(), self.winfo_height()
        try:
            self.configure(scrollregion = (0, 0, larg, haut))
        except:
            pass
        self.__canredim()

class ScrolledFrame(Frame):
    def __init__(self, master=None, scrollregion = None, **args):
        self.__frame = Frame(master)
        self.__canvas = Canvas(self.__frame, scrollregion = scrollregion or (0,0,100,100))
        Frame.__init__(self, self.__canvas, **args)
        self.__window = self.__canvas.create_window(0, 0, anchor = "nw", window = self)
        self.__scroll_horiz = Scrollbar(self.__frame, orient = HORIZONTAL, command = self.__canvas.xview)
        self.__scroll_verti = Scrollbar(self.__frame, orient = VERTICAL, command = self.__canvas.yview)
        self.__canvas.grid(column = 0, row = 0, sticky="nesw")
        self.__scroll_horiz.grid(column = 0, row = 1, sticky = "ew")
        self.__scroll_verti.grid(column = 1, row = 0, sticky = "ns")
        self.__canvas.configure(xscrollcommand = self.__scroll_horiz.set, yscrollcommand = self.__scroll_verti.set)
        # nécéssaire
        self.__framestarted = False
        self.__started = False
        self.bind("<Configure>", self.__redim)
        self.__frame.bind("<Configure>", self.__fraredim)
        # redirection des méthodes de placement.
        for i in dir(Grid)+dir(Place)+dir(Pack):
            exec("self.%s = self._ScrolledFrame__frame.%s"%(i,i))
        self.__redim()

    def __fraredim(self, event = None):
        if not self.__framestarted :
            self.__framestarted = True
            return
        larg, haut = self.__frame.winfo_width(), self.__frame.winfo_height()
        larg-=21
        haut-=21
        self.__canvas.config(width = larg, height = haut)

    def __redim(self, event = None):
        if not self.__started:
            self.__started = True
            return
        larg, haut = self.winfo_width(), self.winfo_height()
        self.__canvas.config(scrollregion = (0, 0, larg, haut))
        self.__fraredim()
        
if __name__=='__main__':
    fen = Tk()
    fra = ScrolledFrame(fen, bg = "black")
    fraA = Frame(fra)
    fraB = Frame(fra)
    fraA.pack(side = LEFT, expand = YES, fill = BOTH)
    fraB.pack(side = RIGHT, expand = YES, fill = BOTH)
    fra1 = Frame(fraA, bg = "red", width = 400, height = 400)
    fra2 = Frame(fraA, bg = "yellow", height = 400, width = 400)
    fra3 = Frame(fraB, bg = "green", width = 400, height = 400)
    fra4 = Frame(fraB, bg = "blue", height = 400, width = 400)
    fra1.pack(expand = YES, fill = BOTH, side = TOP)
    fra2.pack(expand = YES, fill = BOTH, side = BOTTOM)
    fra3.pack(expand = YES, fill = BOTH, side = TOP)
    fra4.pack(expand = YES, fill = BOTH, side = BOTTOM)
    fra.pack(expand = YES, fill = BOTH)
    can = ScrolledCanvas(fen, width = 200, height = 200, scrollregion = (0,0,400,400))
    can.pack()
    can.create_oval(100, 100, 300, 300)
    fen.mainloop()
