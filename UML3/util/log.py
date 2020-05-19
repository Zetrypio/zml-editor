import sys
import time

DEBUG = True
INFO = True
WARN = True
ERROR = True
FATAL = True

def err(e):
    """return a nice string representation for error objects (with error type)"""
    if isinstance(e, Exception):
        error("%s : %s" % (e.__class__.__name__, e), base = 2)
    else:
        fatal("%s : %s" % (e.__class__.__name__, e), base = 2)
    return "%s : %s" % (e.__class__.__name__, e)

def debug(*txt, base = 1, **options):
    """print a debug if DEBUG = True"""
    if DEBUG:
        name = sys._getframe(base).f_globals['__name__']
#        try:
#            self = sys._getframe(base).f_locals['self'].__class__.__name__ + "."
#        except:
#            self = ""
        try:
            func = sys._getframe(base).f_code.co_name
        except:
            func = ""
#        name = name + "." + self + func
        name = name + "." + func
        millis = time.time()%60
        print(time.strftime("[%d/%m/%Y %H:%M:")+"%06.3f"%millis+"]["+name+"/DEBUG] ", end="")
        print(*txt, **options)

def info(*txt, base = 1, **options):
    """print an info if INFO = True"""
    if INFO:
        name = sys._getframe(base).f_globals['__name__']
#        try:
#            self = sys._getframe(base).f_locals['self'].__class__.__name__ + "."
#        except:
#            self = ""
        try:
            func = sys._getframe(base).f_code.co_name
        except:
            func = ""
#        name = name + "." + self + func
        name = name + "." + func
        millis = time.time()%60
        print(time.strftime("[%d/%m/%Y %H:%M:")+"%06.3f"%millis+"]["+name+"/INFO] ", end="")
        print(*txt, **options)

def warn(*txt, base = 1, **options):
    """print a warning if WARN = True"""
    if WARN:
        name = sys._getframe(base).f_globals['__name__']
#        try:
#            self = sys._getframe(base).f_locals['self'].__class__.__name__ + "."
#        except:
#            self = ""
        try:
            func = sys._getframe(base).f_code.co_name
        except:
            func = ""
#        name = name + "." + self + func
        name = name + "." + func
        millis = time.time()%60
        print(time.strftime("[%d/%m/%Y %H:%M:")+"%06.3f"%millis+"]["+name+"/WARN] ", end="", file=sys.stderr)
        sys.stderr.flush()
        time.sleep(0.001)
        print(*txt, **options)

def error(*txt, base = 1, **options):
    """print an error if ERROR = True"""
    if ERROR:
        name = sys._getframe(base).f_globals['__name__']
#        try:
#            self = sys._getframe(base).f_locals['self'].__class__.__name__ + "."
#        except:
#            self = ""
        try:
            func = sys._getframe(base).f_code.co_name
        except:
            func = ""
#        name = name + "." + self + func
        name = name + "." + func
        millis = time.time()%60
        print(time.strftime("[%d/%m/%Y %H:%M:")+"%06.3f"%millis+"]["+name+"/ERROR] ", end="", file=sys.stderr)
        print(*txt, **options, file=sys.stderr)

def fatal(*txt, base = 1, **options):
    """print a fatal error if FATAL = True"""
    if FATAL:
        name = sys._getframe(base).f_globals['__name__']
#        try:
#            self = sys._getframe(base).f_locals['self'].__class__.__name__ + "."
#        except:
#            self = ""
        try:
            func = sys._getframe(base).f_code.co_name
        except:
            func = ""
#        name = name + "." + self + func
        name = name + "." + func
        millis = time.time()%60
        print(time.strftime("[%d/%m/%Y %H:%M:")+"%06.3f"%millis+"]["+name+"/FATAL] ", end="", file=sys.stderr)
        print(*txt, **options, file=sys.stderr)
