import mass as m
import  importlib
#from IPython.lib.deepreload import reload as dreload
importlib.reload(m.synths)
importlib.reload(m.tables)
importlib.reload(m.converters)
importlib.reload(m)
#dreload(m,exclude="pytz")

bt=m.BasicTables()
co=m.BasicConverter()
sy=m.Synth()
note=sy.render()
