import mass as m, numpy as n
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

note=sy.rawRender()
note2=sy.rawRender(d=4.)
# test: rawRender + applyAdsr
note3=sy.rawRender(d=4.,fv=4.)
note4=sy.rawRender(d=4.,fv=4.,nu=8.)
note5=sy.rawRender(d=4.,fv=1.,nu=8.)
note6=sy.rawRender(d=4.,fv=0.5,nu=8.)
notes=[note,note2,note3,note4,note5,note6]
notes=[sy.adsrApply(i) for i in notes]
vibratos=n.hstack(notes)
ut.write(vibratos,"vibratos.wav") # saved to fooname.wav
# tremoloEnvelope
note6=sy.rawRender(d=4.,fv=0.)
note7=sy.rawRender(440.,d=4.,fv=0.)
te=sy.tremoloEnvelope(d=4.)
te2=sy.tremoloEnvelope(4,d=4.)
te3=sy.tremoloEnvelope(4,20,d=4.)
te4=sy.tremoloEnvelope(4,20,d=4.,taba=sy.tables.triangle)

notes=[note6*te,note6*te2,note6*te3,note6*te4]
notes=[sy.adsrApply(i) for i in notes]
tremolos=n.hstack(notes)
ut.write(tremolos,"tremolos.wav") # saved to fooname.wav

# tremolog + envelope
R=sy.rawRender
T=sy.tremoloEnvelope
A=sy.adsrApply
notes=[T(sound=R(d=4.)), # == T(d=4.)*R(d=4.)
T(d=4.)*R(d=4.), # sould sound the same
T(tre_freq=4.,d=4.)*R(d=4.),
T(tre_freq=2.,d=4.)*R(d=4.,fv=4.),
T(tre_freq=4.,d=4.)*R(d=4.,fv=4.),
T(tre_freq=8.,d=4.)*R(d=4.,fv=4.),
T(tre_freq=4.,d=4.)*R(d=4.,fv=8.)]
notes=[sy.adsrApply(i) for i in notes]
tremolos=n.hstack(notes)
ut.write(tremolos,"TV.wav") # saved to fooname.wav

f0=220.
M=co.midi2HzInterval
H=n.hstack
R=sy.render2
notes_=[T(2.,d=4.)*R(f0*M(7),d=4.,fv=4.)+
T(2.,d=4.)*R(f0,d=4.,fv=4.),

T(4.,d=4.)*H(( R(f0*M(7),d=2.,fv=4.), R(f0*M(7),d=2.,fv=4.) )) +
T(4.,d=4.)*R(f0,d=4.,     fv=4.),

T(2.,d=4.)*R(f0*M(7),d=4.,fv=4.)+
T(2.,d=4.)*R(f0,d=4.,fv=4.),

T(4.,d=4.)*R(f0*M(7),d=4.,fv=2.)+
T(4.,d=4.)*R(f0,d=4.,     fv=2.),

T(6.,d=4.)*R(f0*M(7),d=4.,fv=4.)+
T(8.,d=4.)*R(f0,d=4.,     fv=2.),

T(6.,d=4.)*R(f0*M(-7),d=4.,fv=4.)+
T(8.,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0,d=2.,     fv=4.) )),

T(6.,d=4.)*R(f0*M(-7),d=4.,fv=8.)+
T(8.,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0,d=2.,     fv=8.) )),

T(8.,d=4.)*R(f0*M(-7),d=4.,fv=8.)+
T(8.,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0,d=2.,     fv=6.) )),

T(.5,d=4.)*R(f0*M(-7),d=4.,fv=1.)+
T(.5,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0,d=2.,     fv=6.) )),

T(1.,d=4.)*R(f0*M(-5),d=4.,fv=1.)+
T(.5,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0*M(2),d=2.,     fv=6.) )),

T(2.,d=4.)*R(f0*M(-5),d=4.,fv=1.)+
T(1.,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0*M(2.2),d=2.,     fv=8.) )),

T(2.,d=4.)*R(f0*M(5),d=4.,fv=2.)+
T(2.,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0*M(0.2),d=2.,     fv=8.) )),

T(2.,d=4.)*R(f0*M(5.2),d=4.,fv=2.)+
T(2.,d=4.)*H(( R(f0,d=2.,     fv=2.), R(f0*M(-.2),d=2.,     fv=8.) )),

T(2.,d=4.)*R(f0*M(7.2),d=4.,fv=2.)+
T(2.,d=4.)*H(( R(f0*M(-1),d=2.,     fv=2.), R(f0*M(-.2),d=2.,     fv=8.) )),

T(2.,d=4.)*R(f0*M(12.),d=4.,fv=2.)+
T(2.,d=4.)*H(( R(f0*M(0),d=2.,     fv=2.), R(f0*M(4.2),d=2.,     fv=6.) )),

T(2.,d=4.)*R(f0*M(12.),d=4.,fv=2.)+
T(2.,d=4.)*H(( R(f0*M(-12),d=2.,     fv=2.), R(f0,d=2.,     fv=4.) )),

T(2.,d=4.)*R(f0*M(7.),d=4.,fv=4.)+
T(2.,d=4.)*H(( R(f0*M(-12),d=2.,     fv=2.), R(f0,d=2.,     fv=4.) )),
]

#notes_=[sy.adsrApply(i) for i in notes_]
#
#
#notes=[T(sound=R(d=4.)), # == T(d=4.)*R(d=4.)
#T(d=4.)*R(d=4.), # sould sound the same
#T(tre_freq=4.,d=4.)*R(d=4.),
#T(tre_freq=2.,d=4.)*R(d=4.,fv=4.),
#T(tre_freq=4.,d=4.)*R(d=4.,fv=4.),
#T(tre_freq=8.,d=4.)*R(d=4.,fv=4.),
#T(tre_freq=4.,d=4.)*R(d=4.,fv=8.)][::-1]
#
#notes=[sy.adsrApply(i) for i in notes]
#
#vibrosong=H(notes_+notes)

# fadeout in last three seconds:
sy.adsrSetup(0,0,0,3000)
vibrosong=A(H(notes_+[n.zeros(44100)]))
ut.write(vibrosong,"vibrosong.wav")

# render
