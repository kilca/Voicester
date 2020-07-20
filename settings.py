# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:16:26 2020

@author: Kilian
"""

import json
import effect as ef
import sys

def init():
    global is_streaming
    global is_keylisten #KeyThread active
    global is_playing#StreamThread active
    
    global do_sound
    
    global my_thread
    global key_thread

    global INPUT 
    global OUTPUT
    
    global effect
    global val
    
    global prev
    
    global index_song#index song selected
    global keybinds
    global songs
    global keybindselected
    
    index_song = 0
    
    do_sound = False
    
    songs = []
    keybinds = []
    keybindselected = None
    
    prev = None
    
    effect = ef.none_effect
    val = 0
    
    is_keylisten = True
    is_playing = False
    is_streaming = False
    
    my_thread = None
    key_thread = None
    
    INPUT = ''
    OUTPUT = ''

def save():
    print("input : ",INPUT)
    try:
        saved_dict = {"languages": ["English", "Fench"]
        }
        song_array = []
        for i in range(0,9):
            #print("song :",songs[i].get())
            song_array.append(songs[i].get())
        
        for i in range(0,9):
            saved_dict["songs"] = song_array
        
        
        with open('person.json', 'w') as json_file:
          json.dump(saved_dict, json_file)
        
    except:
          e = sys.exc_info()[0]
          print(e)
        