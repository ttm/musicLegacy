import music as m, numpy as n
import  importlib
#from IPython.lib.deepreload import reload as dreload
importlib.reload(m.synths)
importlib.reload(m.tables)
importlib.reload(m.converters)
importlib.reload(m.utils)
importlib.reload(m)
#dreload(m,exclude="pytz")

bt=m.BasicTables()
co=m.BasicConverter()
sy=m.Synth()

note=sy.render()

ut=m.Utils()
ut.write(note) # saved to fooname.wav

melody=n.hstack([sy.render(f,.2) for f in co.p2f(220,[0,7,7,5,6,7,0,4,7,0])])
sy.vib_depth=3.
sy.vib_freq=3.
sy.tab=bt.saw
section2=n.hstack([sy.render(f,d) for f,d in zip(co.p2f(110,[0,7,7,5,6,7,0,4,7,0]),[.2,.4,.2,.2,.8,.2,.4,.2,.4])])

song=n.hstack((melody,section2))

ut.write(song,"song.wav")
