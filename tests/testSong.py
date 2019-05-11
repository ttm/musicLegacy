import musicLegacy as m, numpy as n
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

#melody=n.hstack([sy.render(f,.2) for f in co.p2f(220,[0,7,7,5,6,7,0,4,7,0])])
#sy.vib_depth=3.
#sy.vib_freq=3.
#sy.tab=bt.saw
#section2=n.hstack([sy.render(f,d) for f,d in zip(co.p2f(110,[0,7,7,5,6,7,0,4,7,0]),[.2,.4,.2,.2,.8,.2,.4,.2,.4])])
#
#song=n.hstack((melody,section2))

# notes of .5s with sharp to long attacks
sy.adsrSetup(10,10,-10,10)
song=sy.render()
As=n.linspace(10,450,10)
notes=[]
for aa in As:
    sy.adsrSetup(aa,10,-10,10)
    notes.append(sy.render(d=.5))
measure1=n.hstack(notes)
notes=[]
for aa in As[::-1]:
    sy.adsrSetup(10,10,-10,aa)
    notes.append(sy.render(d=.5))
measure2=n.hstack(notes)

# explore fast and slow sustain
notes=[sy.adsrSetup(10,10,-10,10 , True),
       sy.adsrSetup(10,450,-10,10, True)]
measure3=n.hstack(notes*3)

sharp=    sy.adsrSetup(10,10,-10,10 ,True)
intro=    sy.adsrSetup(450,10,-10,10,True)
semsharp=    sy.adsrSetup(10,450,-10,10,True)
tend=    sy.adsrSetup(10,10,-10,450,True)
middle=    sy.adsrSetup(220,10,-10,220,True)
sharper=    sy.adsrSetup(10,10,-20,10 ,True)
measure4=n.hstack([sharp,intro,tend,
intro,sharp,tend,
intro,tend,sharp,
tend,intro,sharp,
tend,sharp,intro,
sharp,tend,intro,
                 ])

intro=n.hstack((measure1,measure2,measure3,measure4))

# somar measure4 pra sempre daqui em diante
# notes with different tables
sharper=    sy.adsrSetup(70,50,-15,10 )
sy.tab=sy.tables.square
n1=sy.render(d=2)
sy.tab=sy.tables.saw
n2=sy.render(d=2)
sy.tab=sy.tables.sine
n3=sy.render(d=2)
silence=n.zeros(44100)
measure5_=n.hstack((n1,silence,n2,silence,n3,silence))
measure5=measure5_+measure4

# notes on different pitches
notes=[0,4,8]
sy.adsrSetup(70,50,-15,210 )
sy.tab=sy.tables.sine
notes_=[sy.render(ff,d=.5) for ff in co.p2f(220.,notes)]

def peal(a,b,c):
    return [a,b,c,
            b,a,c,
            b,c,a,
            c,b,a,
            c,a,b,
            a,c,b]
measure6_=n.hstack(peal(*notes_))
measure6=measure4+measure6_

second_intro=n.hstack((measure5,measure6))

# 
introduction=n.hstack((intro,second_intro))

# development:
pieces=[]
size=0
increment=1100
i=1
while len(measure6)/2>size+increment*i:
    size+=increment*i
    i+=1
    piece_=measure6[len(measure6)/2-size:len(measure6)/2+size]
    msize=1000*(size/(44100))
    sy.adsrSetup(msize//3,msize//3,-15,msize//3 )
    piece=sy.adsrApply(piece_)
    pieces.append(piece[::8])
measure7=n.hstack(pieces)

# substitui tempos de .5s
delta=44100*0.5
total=44100*9
ntempos=9/0.5
# measure4 e 6_ intercaladas
side=n.random.randint(0,2,ntempos)
side_=n.repeat(side,delta)
side_I=side_*-1+1
measure8_=measure4*side_+measure6*side_I
sy.tab=sy.tables.sine
sy.adsrSetup(8000)
measure8=measure8_+sy.render(220*(3/2),d=9)

development=n.hstack((measure7,measure8))

# coda
sy.adsrSetup(200,100,-10,800)
final_note=sy.render(d=4.)
coda=n.hstack([sharp,semsharp,middle,middle,middle,middle,final_note])

song=n.hstack((introduction, development, coda))
ut.write(song,"testSong.wav")

# Second music
# long note with long and short vibrattos with variable depth
# long note tieh long and short tremolos with variable depth

# band limited collored noise with variable central frequency
# and bandwidth
# reverb, delay, localization, filters

