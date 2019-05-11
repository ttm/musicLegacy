import musicLegacy as m
import  importlib
#from IPython.lib.deepreload import reload as dreload
importlib.reload(m.converters)
importlib.reload(m)
#dreload(m,exclude="pytz")


co=m.BasicConverter()
