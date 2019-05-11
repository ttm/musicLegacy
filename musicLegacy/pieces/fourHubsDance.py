import numpy as n
from ..synths import Synth
from ..converters import BasicConverter
from ..utils import Utils
sy=Synth()
co=BasicConverter()
ut=Utils()

def find_closest(grid, arbitrary):
    """Find closes grid values to arbitrary values"""
    #A must be sorted
    A=n.array(grid)
    target=n.array(arbitrary)
    idx = A.searchsorted(target)
    idx = n.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    tarray=A[idx]
    return tarray


class FourHubsDance:
    def __init__(self):
        pass
    def setupEngine(self,samplerate,total_time,beat_duration):
        self.samplerate=samplerate
        self.total_time=total_time
        self.beat_duration=beat_duration
        self.total_samples=samplerate*total_time
        self.total_beats=total_time/beat_duration
        self.samples_beat=samplerate*beat_duration

    def sonicLine1(self,measures=[7,2,17],possible_notes=[0,2,4,6,8,10],ambit=12,rythmic_pattern=[0,0,1,1],f0=220):
        """A mapping of measures to notes"""
        notes=measures*ambit
        notes_=notes%12
        self.possible_notes=possible_notes

        self.closest=find_closest(possible_notes,notes_)
        self.diff=self.closest-notes_
        notes__=notes+self.diff
        self.notes__=notes__
        self.notes=notes
        # ver qual nota eh mais proximo da grade
        # bater com padrao ritmico
        self.freqs=co.p2f(f0,self.notes__)
        if len(rythmic_pattern)==4:
            line=n.hstack([self.sy.render(f,self.beat_duration/4)
                 if (rythmic_pattern[i%4]==1) else n.zeros(int(self.samples_beat/4))
                            for i,f in enumerate(self.freqs)])
        elif len(rythmic_pattern)==1:
            line=n.hstack([self.sy.render(f,self.beat_duration)
                for f in self.freqs[::4]])
        return line
    def makeGaussianNoise(self,mean,std,DUR=2):
        Lambda = DUR*self.samples_beat # Lambda sempre par
        df = self.samplerate/float(Lambda)
        Lambda = int(Lambda)
        MEAN=mean
        STD=.1
        coefs = n.exp(1j*n.random.uniform(0, 2*n.pi, int(Lambda)))
        # real par, imaginaria impar
        coefs[Lambda//2+1:] = n.real(coefs[1:Lambda//2])[::-1] - 1j * \
            n.imag(coefs[1:Lambda//2])[::-1]
        coefs[0] = 0.  # sem bias
        if Lambda%2==0:
            coefs[Lambda//2] = 0.  # freq max eh real simplesmente

        # as frequências relativas a cada coeficiente
        # acima de Lambda/2 nao vale
        fi = n.arange(coefs.shape[0])*df
        f0 = 15.  # iniciamos o ruido em 15 Hz
        f1=(mean-std/2)*3000
        f2=(mean+std/2)*3000
        i1 = int(n.floor(f1/df))  # primeiro coef a valer
        i2 = int(n.floor(f2/df))  # ultimo coef a valer
        coefs[:i1] = n.zeros(i1)
        coefs[i2:]=n.zeros(len(coefs[i2:]))

        # obtenção do ruído em suas amostras temporais
        ruido = n.fft.ifft(coefs)
        r = n.real(ruido)
        r = ((r-r.min())/(r.max()-r.min()))*2-1

        # fazer tre_freq variar conforme measures2
        return r

    def sonicLine2(self,measures1=[7,2,17],tmean=.5,DUR=2):
        """Noise controlled by two measures vectors.
        
        Central frequency by measures1 
        Tremolo frequency by measures2
        """
        # diferença das frequências entre coeficiêntes vizinhos:
        self.measures1=measures1
        ### 2.50 Ruido branco
        noise=n.hstack(
                [self.makeGaussianNoise(mean=tmean+delta,std=.1, DUR=DUR) for delta
                    in (measures1[::4*DUR]-0.5)*.2])

        self.noise=noise=ut.normalize(noise)
        # multiply tre_freq by a factor of measures2
        #envelope=n.hstack([self.sy.tremoloEnvelope(tre_freq,d=self.beat_duration/4,V_dB=20.) for tre_freq in 8+7*(2*(measures2-0.5))])
        # if necessary, low-pass this envelope
        #return noise[:len(envelope)]*envelope
        return noise
