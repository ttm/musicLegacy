==================================================================
MASS is Music and Audio in Sample Sequences
==================================================================

This project delivers routines for music oriented sound synthesis
in a sample based system.

All parameters are updated in a sample by sample rate and calculations
are made in 64 bit floating point. All operations are described by
equations that directly relates audio samples to musical aspects.
Detailed descriptions can be found in:

- the article "Psychophysics of musical elements in the discrete-time representation of sound": http://arxiv.org/abs/1412.6853

- the msc dissertation "Música no áudio digital: descrição psicofísica e caixa de ferramentas": https://github.com/ttm/dissertacao/blob/master/dissertacaoCorrigida.pdf?raw=true

Usage example
=================
Download messages from one GMANE list:

.. code:: python

    import mass as m

    wf=m.WaveForms()
    sy=m.MonoSynth(wf)

    melodic_line=sy.simpleLine([110,100,220,33.,14])
    # Enjoy!
