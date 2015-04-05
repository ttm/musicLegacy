=============================================================
music is a toolbox for music synthesis (MASS modeling)
=============================================================

This project delivers routines for music oriented sound synthesis
in a sample based system. Music can be though of as a sample level
DAW system, in which the objects manipulated are in fact the array
of samples describing the sound wave that will reach a listener ear.
The MASS (music and audio in sample sequences) modeling is used[1][2].

Install with:

    $ pip3 install music

Hack demo songs and make wav files with:

    $ python3 tests/testSong.py

To hear testSong.wav or

    $ python3 tests/testSong2.py

to hear vibrosong.wav. To hack the MASS package itself, and use it from the repo, don't forget to:

    $ pip install -e <path/to/repo>


Real time is possible but not the emphasis:
all parameters are updated sample by sample and calculations
are made in 64 bit floating point. All operations are described by
equations that directly relates audio samples to musical aspects.
Detailed descriptions can be found in:

- the article "Psychophysics of musical elements in the discrete-time representation of sound": http://arxiv.org/abs/1412.6853

- the msc dissertation "Música no áudio digital: descrição psicofísica e caixa de ferramentas": https://github.com/ttm/dissertacao/blob/master/dissertacaoCorrigida.pdf?raw=true

Usage example
=================
Download messages from one GMANE list:

.. code:: python

    import music as m

    # sine, triangle, square and sawtooth
    # are attributes of the bt object:
    bt=m.BasicTables()

    # for frequency to midi and decibels to amplitude relations:
    co=m.BasicConverter()
    # try co.db2Amp .amp2Db .hz2Midi .midi2Hz 

    sy=m.Synth()

    note=sy.render()
    ut=m.Utils()
    ut.write(note) # saved to fooname.wav

    melody=n.hstack([sy.render(f,.2) for f in 
                      co.p2f(220,[0,7,7,5,6,7,0,4,7,0])])
    sy.vib_depth=3.
    sy.vib_freq=3.
    sy.tab=bt.saw
    section2=n.hstack([sy.render(freq,dur) for freq,dur in 
                        zip(co.p2f(110,[0,7,7,5,6,7,0,4,7,0]),
                        [.2,.4,.2,.2,.8,.2,.4,.2,.4])])

    song=n.hstack((melody,section2))

    ut.write(song,"song.wav")

    # A core purpose of the toolbox is to serve other
    # toolboxes on the development sonic representations
    # E.g. m.pieces.FourHubsDance is used by gmane toolbox
    # to make sonified animations:
    # https://www.youtube.com/watch?v=YxDiwzAUPeU
    # sonicLine1 and sonicLine2 attributes are
    # most basic sonic "templates" used by:
    # https://pypi.python.org/pypi/gmane to make social music

    # more in the way. Take a look at the above literature.
    # Enjoy!
