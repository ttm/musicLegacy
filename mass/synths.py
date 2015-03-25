import numpy as n
from .tables import *

from .tables import *
BT=BasicTables()
class Synth:
    def __init__(self,f_a=44100, tables=None):
        self.f_a=f_a
        if tables:
            self.tables=tables
        else:
            self.tables=BasicTables()
        self.synthSetup()
        self.adsrSetup()
    def synthSetup(self,tab=BT.triangle,vib_depth=.1,vib_freq=2., vib_tab=BT.sine, tre_depth=3.,tre_freq=0.2,tre_tab=BT.sine):
        """Setup synth engine. ADSR is configured seperately"""
        self.tab=tab
        if vib_depth and vib_freq:
            self.vibrato=True
            self.vib_depth=vib_depth
            self.vib_freq=vib_freq
            self.vib_tab=vib_tab
            self.tam_vib_tab=len(vib_tab)
        if tre_depth and tre_freq:
            self.tremolo=True
            self.tre_depth=tre_depth
            self.tre_freq= tre_freq
            self.tre_tab=tre_tab
    def adsrSetup(self,A=100.,D=40,S=-5.,R=50,render_note=False, adsr_method="absolute"):
        self.adsr_method=adsr_method # implement relative and False
        self.A=A
        self.D=D
        self.S=S
        self.R=R
        self.a_S=10**(self.S/20.)
        self.Lambda_A=int(self.A*self.f_a*0.001)
        self.Lambda_D=int(self.D*self.f_a*0.001)
        self.Lambda_R=int(self.R*self.f_a*0.001)

        ii=n.arange(self.Lambda_A,dtype=n.float)
        A=ii/(self.Lambda_A-1)
        self.A_i=n.copy(A)
        A_i=A
        ii=n.arange(self.Lambda_A,self.Lambda_D+self.Lambda_A,dtype=n.float)
        D=1-(1-self.a_S)*(   ( ii-self.Lambda_A )/( self.Lambda_D-1) )
        self.D_i=n.copy(D)
        #ii=n.arange(self.Lambda-self.Lambda_R,self.Lambda,dtype=n.float)
        #R=self.a_S-self.a_S*((ii-(self.Lambda-self.Lambda_R))/(self.Lambda_R-1))
        R=self.a_S*(n.linspace(1,0,self.Lambda_R))
        self.R_i=n.copy(R)
        if render_note:
            return self.render(d=.5)
    def adsrApply(self,audio_vec):
        Lambda=len(audio_vec)
        S=n.ones(Lambda-self.Lambda_R-(self.Lambda_A+
                   self.Lambda_D),dtype=n.float)*self.a_S
        envelope=n.hstack((self.A_i, self.D_i, S, self.R_i))
        return envelope*audio_vec
    def render(self,f0=220.,d=2.):
        """Render a note with f0 Hertz and d seconds"""
        self.note=self.rawRender(f0,d,self.tab,self.vib_freq,self.vib_depth,
                         self.vib_tab)
        self.tre_env=self.tremoloEnvelope(self.tre_freq,self.tre_depth,
                                        d, self.tre_tab)
        self.note=self.note*self.tre_env
        self.note=self.adsrApply(self.note)
        return self.note
    def tremoloEnvelope(self,tre_freq=2.,V_dB=10.,d=2.,taba=BT.sine,sound=None):
        if sound!=None:
            Lambda=len(sound)
        else:
            Lambda=n.floor(self.f_a*d)
        ii=n.arange(Lambda)
        Lt=len(taba)
        Gammaa_i=n.floor(ii*tre_freq*Lt/self.f_a) # índices para a LUT
        Gammaa_i=n.array(Gammaa_i,n.int)
        # variação da amplitude em cada amostra
        A_i=taba[Gammaa_i%Lt] 
        A_i=10.**((V_dB/20.)*A_i)
        if sound!=None:
            return A_i*sound
        else:
            return A_i
    def rawRender(self,f=200,d=2.,tab=BT.triangle,fv=2.,nu=2.,tabv=BT.sine):
        Lambda=n.floor(self.f_a*d)
        ii=n.arange(Lambda)
        Lv=self.tam_vib_tab

        Gammav_i=n.floor(ii*fv*Lv/self.f_a) # índices para a LUT
        Gammav_i=n.array(Gammav_i,n.int)
        # padrão de variação do vibrato para cada amostra
        Tv_i=tabv[Gammav_i%Lv] 

        # frequência em Hz em cada amostra
        F_i=f*(   2.**(  Tv_i*nu/12.  )   ) 
        # a movimentação na tabela por amostra
        Lt=self.tables.size
        D_gamma_i=F_i*(Lt/self.f_a)
        Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
        Gamma_i=n.floor( Gamma_i) # já os índices
        Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
        return tab[Gamma_i%int(Lt)] # busca dos índices na tabela
    def render2(self,f=200,d=2.,tab=BT.triangle,fv=2.,nu=2.,tabv=BT.sine):
        Lambda=n.floor(self.f_a*d)
        ii=n.arange(Lambda)
        Lv=self.tam_vib_tab

        Gammav_i=n.floor(ii*fv*Lv/self.f_a) # índices para a LUT
        Gammav_i=n.array(Gammav_i,n.int)
        # padrão de variação do vibrato para cada amostra
        Tv_i=tabv[Gammav_i%Lv] 

        # frequência em Hz em cada amostra
        F_i=f*(   2.**(  Tv_i*nu/12.  )   ) 
        # a movimentação na tabela por amostra
        Lt=self.tables.size
        D_gamma_i=F_i*(Lt/self.f_a)
        Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
        Gamma_i=n.floor( Gamma_i) # já os índices
        Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
        sound=tab[Gamma_i%int(Lt)] # busca dos índices na tabela
        sound=self.adsrApply(sound)
        return sound





