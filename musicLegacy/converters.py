import numpy as n
class BasicConverter:
    """Delivers most basic converters for amplitude and frequency"""
    def db2Amp(self, db_difference):
        """Receives difference in decibels, returns amplitude proportion"""
        return 10.**(db_difference/20.)
    def amp2Db(self, amp_difference):
        """Receives amplitude proportion, returns decibel difference"""
        return 20.*n.log10(amp_difference)
    def hz2Midi(self, hz_val):
        """Receives Herz value and returns midi note value"""
        return 69+12*n.log2(hz_val/440)
    def midi2Hz(self, midi_val):
        """Receives midi note value and returns corresponding Herz frequency"""
        #return 440*n.log2((69+midi_val)/69)
        return 440*2**((midi_val-69)/12.)
    def midi2HzInterval(self,midi_interval):
        return 2**(midi_interval/12)
    def p2f(self,f0=220.,semitones=[0,7,7,4,7,0]):
        return [f0*2**(i/12) for i in semitones]


