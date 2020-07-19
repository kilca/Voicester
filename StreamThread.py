# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:05:43 2020

@author: Kilian
"""
import effect as ef
import threading
import wave
import pyaudio
import numpy as np
import sys
import os
import settings

def resource_path(relative): 
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class StreamThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)



    def run(self):
        
        chunk = 1024
        CHUNK = 512
        RATE = 44100
        
        INPUT = settings.INPUT
        OUTPUT = settings.OUTPUT
        
        fulldata = bytearray(b'')
        fulleditdata = bytearray(b'')


        p=pyaudio.PyAudio()
        try:
            stream=p.open(
                    format = pyaudio.paInt16,
            	    channels = 1,
            		rate = RATE,
            		frames_per_buffer = CHUNK,
                        input_device_index = INPUT,
                        output_device_index = OUTPUT,
            		input = True,
            		output = True
                    ) # inputとoutputを同時にTrueにする
            
        except OSError as err:
            print("OS error: see comment")#faut que la sortie soit aussi un input
        
        while stream.is_active() and settings.is_streaming:
            
            #Lancement du son custom
            if (settings.do_sound):
                
                
                rep = settings.songs[settings.index_song]
                print("dir sel :",rep.get())
                
                #wf = wave.open(resource_path('./9000.wav'), 'rb')
                #wf = wave.open(resource_path(rep.get()), 'rb')
                wf = wave.open(rep.get(), 'rb')
                streamsound = p.open(
                    format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output_device_index = OUTPUT,
                    output = True)
                
                data = wf.readframes(chunk)
                
                #np.set_printoptions(threshold=np.inf)
                np.set_printoptions(threshold=20)
                
                #print(np.frombuffer(data, np.int16))
                #print(np.frombuffer(test_effect(data), np.int16))
                
                
                while len(data) > 0 and settings.is_streaming:
                    
                    
                    fulldata+=data
                    
                    data = settings.effect(data,settings.val)
                    
                    fulleditdata += data
                    
                    streamsound.write(data)
                    data = wf.readframes(chunk)
                
                settings.do_sound = False
                streamsound.stop_stream()
                streamsound.close()
            
                #ef.graphStream(fulldata,'fulldata')
                #ef.graphStream(fulleditdata,'fulleditdata')
            
            #son voix
            input = stream.read(CHUNK,  exception_on_overflow = False)
            input = settings.effect(input,settings.val)
            """
            if (getattr(t, "test", False)):
                audio_trans(input)
                setattr(t,"test",False)
            """
            
            output = stream.write(input)
            
        stream.stop_stream()
        stream.close()
        p.terminate() 