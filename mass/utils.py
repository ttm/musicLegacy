import numpy as n
from scipy.io import wavfile as w

class LPFilter:
    pass
class Notch:
    pass
class Notch:
    pass
class Utils:
    def __init__(self):
        pass
    def normalize(self, vector):
        return -1+2*(vector-vector.min())/(vector.max()-vector.min())
    def write(self,vector,filename="fooname.wav", normalize="yes",f_a=44100):
        if normalize:
            vector=self.normalize(vector)
        s = n.int16(vector * float(2**15-1))
        w.write(filename,f_a, s) # escrita do som
