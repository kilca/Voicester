# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 02:54:18 2020

@author: Kilian
"""
import wave
import pyaudio
import settings


from urllib.request import urlopen

class StreamHandler():
    
    CHUNK = 2048
    RATE = 44100
    
    #called when errors occured
    def stopAll(self):
        settings.do_sound = False
        #?todo set data member of class and reset it
        
    
    def __init__(self):
        self.p=pyaudio.PyAudio()
        
        self.fulldata = bytearray(b'')
        self.fulleditdata = bytearray(b'')
        
        self.streamsound = None
        self.stream = None
        
        self.INPUT = settings.INPUT
        self.OUTPUT = settings.OUTPUT
        
        self.openStream()
    
    def isSystemFile(self,link):
        #SIMPLE TEST
        return (len(link)>2 and link[1]==':')

    def isWebFile(self,link):
        #TO IMPLEMENT
        return True
  
    def updateStream(self):
                
        if (settings.do_sound):
            rep = settings.songs[settings.index_song]
            link = rep.get()
            if (self.isSystemFile(link)):
                wf = self.openSystemSound(link)
                self.readSoundLoop(self.readSystem,wf)
            elif (self.isWebFile(link)):
                u = self.openWebSound(link)
                self.readSoundLoop(self.readWeb,u)
            
        #listen and write mic 
        input = self.stream.read(self.CHUNK,  exception_on_overflow = False)
        input = settings.effect(input,settings.val)
            
        output = self.stream.write(input)
    
    def readWeb(self,r,chunk):
        return r.read(chunk)
    def readSystem(self,r,chunk):
        return r.readframes(chunk)
    
    def readSoundLoop(self, func,r):
        
        data = func(r,self.CHUNK)
        
        while len(data) > 0 and settings.is_streaming:                        
            self.streamsound.write(data)
            data = func(r,self.CHUNK)
            
        settings.do_sound = False
        self.streamsound.stop_stream()
        self.streamsound.close()
        
    #for mic
    def openStream(self):
        self.stream=self.p.open(
                format = pyaudio.paInt16,
        	    channels = 1,
        		rate = self.RATE,
        		frames_per_buffer = self.CHUNK,
            input_device_index = self.INPUT,
            output_device_index = self.OUTPUT,
        		input = True,
        		output = True
                ) # inputとoutputを同時にTrueにする
    def openSystemSound(self,link):
        
        wf = wave.open(link, 'rb')
        
        self.streamsound = self.p.open(
            format = self.p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output_device_index = self.OUTPUT,
            output = True)
        
        return wf
        
    def openWebSound(self,link):
       
        srate=192000   
        self.streamsound = self.p.open(format = self.p.get_format_from_width(1),
            channels = 1,
            rate = srate,
            output_device_index = self.OUTPUT,
            output = True)
        
        url = "https://www.pacdv.com/sounds/voices/maybe-next-time.wav"
        u = urlopen(url)
        return u
        
    
