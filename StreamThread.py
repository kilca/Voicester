# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:05:43 2020

@author: Kilian
"""
import threading
import settings

from StreamHandler import StreamHandler

class StreamThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)



    def run(self):
        
        sh = StreamHandler()
        
        while sh.stream.is_active() and settings.is_streaming:
            try:
                sh.updateStream()
            except:
                print("incorrect file")
                sh.stopAll()
            
        sh.stream.stop_stream()
        sh.stream.close()
        sh.p.terminate() 