# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 23:58:29 2020

@author: Kilian
"""
import numpy as np
import matplotlib.pyplot as plt

#https://github.com/MattMoony/figaro/search?q=filter&unscoped_q=filter

import settings

def none_effect(data, v):
    return data

def crackle_effect(d, fac):
    data = np.fromstring(d, np.int16)
    ifac = 1 - .9 * fac
    chunk = data.clip(data.min() * ifac, data.max() * ifac) * (.5 / ifac)
    return chunk.astype(np.int16).tobytes()

def volume_effect(data, volume):
    """ Change value of list of audio chunks """
    sound_level = (volume / 100.)
    chunk = np.fromstring(data, np.int16)
    chunk = chunk * sound_level
    
    return chunk.astype(np.int16).tobytes()

def pitch_effect(d,fac) -> np.ndarray:
    
    
    data = np.fromstring(d, np.int16)
    
    freq = np.fft.rfft(data)
    N = len(freq)
    sh_freq = np.zeros(N, freq.dtype)
    S = int(np.round(fac if fac > 0 else N + fac, 0))
    s = int(N-S)
    sh_freq[:S] = freq[s:]
    sh_freq[S:] = freq[:s]
    sh_chunk = np.fft.irfft(sh_freq)
    #return sh_chunk.astype(data.dtype)
    return sh_chunk.astype(np.int16).tobytes()



#the effect become visible near s=6
def trip_effect(d, s):
    scale = s/12
    data = np.fromstring(d, np.int16)
    if settings.prev is None or data.shape != settings.prev.shape:
        settings.prev = np.zeros(data.shape)
    #data, settings.prev = data + settings.prev, settings.prev * scale + data
    #print(data.shape," / ",settings.prev.shape)
    
    chunk, settings.prev = data + settings.prev, settings.prev * scale + data
    return chunk.astype(np.int16).tobytes()

def noise_effect(d, v):
    amp = 1+(v/20) * 100000
    data = np.fromstring(d, np.int16)
    chunk = data + (np.random.rand(*data.shape) - .5) * .05 * amp
    return chunk.astype(np.int16).tobytes()
        
#--------------------------------Ancien test -----------------------------
    

#effet star wars
#effet lag (taux : entier)
#entre 1 et 6 où 6 est incompréhensible
def lag_effect(data, taux):
    return data *(1+taux)

def saturation_effect(data, taux):
    return lag_effect(np.frombuffer(data, np.int16),taux).tobytes()

#0 voix grave bizarre       
def grave_effect(data: np.ndarray) -> np.ndarray:
    d = np.frombuffer(data, np.int16)
    #d = np.rint(d).astype(int) # plus smooth ?
    return (d).astype(int).tobytes()

def graphStream(frames, legend):
    fig = plt.figure()
    s = fig.add_subplot(111)
    #amplitude = np.fromstring(frames, np.int16)
    amplitude = np.frombuffer(frames, np.int16)
    s.plot(amplitude)
    s.legend([legend])
    fig.savefig('t.png')
    

#clamp
def clip16(x):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)