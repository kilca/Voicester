# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:05:43 2020

@author: Kilian
"""
import threading
import settings

from win32api import GetKeyState

class KeyThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)



    def run(self):
        def key_down(key):
            state = GetKeyState(key)
            if (state != 0) and (state != 1):
                return True
            else:
                return False
        
        while settings.is_keylisten:
            for i in range(0,9):
                if (settings.keybinds[i] != "OFF"):
                    print(settings.keybinds[i].upper())
                    if (key_down(ord(settings.keybinds[i].upper()))):
                        print("select :",i)
#import time
#time.sleep(0.02)



