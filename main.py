# -*- coding:utf-8 -*-
import pyaudio
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import sys
import os

import settings

import effect as ef


from StreamThread import StreamThread
from KeyThread import KeyThread

def resource_path(relative): 
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def get_device_list():
    p = pyaudio.PyAudio()
    #device info type is dict
    device_li = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
    return device_li

def run_statusbar():
    status.configure(text="Now processing.." + 'input=' + str(settings.INPUT) + ' ' + 'output=' + str(settings.OUTPUT))

def kill_statusbar():
    status.configure(text="")

def click_playSound(i):
     
    if (settings.my_thread is not None and not settings.do_sound):
        settings.index_song = i
        settings.do_sound = True
    #global soundthread
    #soundthread = threading.Thread(target=playSound)
    #soundthread.start()
    

def press_button_start():

    settings.INPUT = int(input_combo.get()[1])
    settings.OUTPUT = int(output_combo.get()[1])

    if not settings.is_streaming:
        settings.is_streaming = True
        run_statusbar()
        settings.my_thread = StreamThread()
        settings.my_thread.start()
        '''
        my_thread = threading.Thread(target=stream_start)
        my_thread.start()
        '''
    
    
    

def press_button_stop():

    print("stop")
    if settings.is_streaming:
        settings.is_streaming = False
        settings.my_thread.join() 
        kill_statusbar()

'''
def on_field_change(index, value, op):
    print ("combobox updated to ", v)
'''
def combo_change(eventObject):
    comboval = effect_combo.get()

    if (comboval == "none"):
        settings.effect = ef.none_effect
    if (comboval == "volume"):
        settings.effect = ef.volume_effect
        effect_val.configure(from_=0)
        effect_val.configure(to=200)
    if (comboval == "pitch"):
        settings.effect = ef.pitch_effect
        effect_val.configure(from_=-10)
        effect_val.configure(to=10)
    if (comboval == "lag"):
        settings.effect = ef.pitch_effect
        effect_val.configure(from_=0)
        effect_val.configure(to=20)
    if (comboval == "saturation"):
        settings.effect = ef.saturation_effect
        effect_val.configure(from_=0)
        effect_val.configure(to=6)
    if (comboval == "noise"):
        settings.effect = ef.noise_effect
        effect_val.configure(from_=0)
        effect_val.configure(to=50)
    if (comboval == "trip"):
        settings.effect = ef.trip_effect
        effect_val.configure(from_=0)
        effect_val.configure(to=10)
    if (comboval == "crackle"):
        settings.effect = ef.crackle_effect
        effect_val.configure(from_=0)
        effect_val.configure(to=10)
    effect_val.set(0)

def slider_change(truc):
    settings.val = effect_val.get()

   
settings.init()


device_li = get_device_list()

root = tk.Tk()
root.title("Voicester")
root.geometry("400x300")



def on_closing():
    
    if (settings.my_thread is not None):
        print("we stop thread stream")
        settings.is_streaming = False
        settings.my_thread.join() 
    
    if (settings.key_thread is not None):
        settings.is_keylisten = False
        settings.key_thread.join()
        
    settings.save()
    
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


'''
app.configure(background='DimGray')
app.geometry('600x600')
app.resizable(width=False, height=False)
'''

tab_parent = ttk.Notebook(root, width=1000, height=650)
tab1 = ttk.Frame(tab_parent) 
tab2 = ttk.Frame(tab_parent) 


tab_parent.add(tab1, text="Main Device Window")
tab_parent.add(tab2, text="Sounds")

#tab_parent.pack(expand=1,fill='both')
#tab_parent.grid(row=0, column=0, columnspan=2, rowspan=5, sticky='NESW')
tab_parent.grid(row=0, column=0, columnspan=1, rowspan=5)

#status.pack(side=tk.BOTTOM, fill=tk.X)

#-------------------TAB 1 ----------------------

status = tk.Label(tab1, text="aaaaaaaa", borderwidth=2, relief="groove")
status.grid(row=1, column = 1)

input_combo = ttk.Combobox(tab1, state='readonly')
input_combo["values"] = tuple('['+str(i)+']'+' '+device_li[i]['name'] for i in range(len(device_li)))
input_combo.current(0)
input_combo.grid(column=1, row=2, sticky='NW')

output_combo = ttk.Combobox(tab1, state='readonly')
output_combo["values"] = tuple('['+str(i)+']'+' '+device_li[i]['name'] for i in range(len(device_li)))
output_combo.current(1)
output_combo.grid(column=1, row=3, sticky='NW')

button_start = tk.Button(tab1, text="START", command=press_button_start)
button_start.grid(column=1, row=4, sticky='NW')

button_stop = tk.Button(tab1, text="STOP", command=press_button_stop)
button_stop.grid(column=1, row=5, sticky='NW')

'''
button_playSound = tk.Button(tab1, text="PLAY SOUND", command=click_playSound)
input_combo.grid(column=0, row=0, sticky='NW')
'''


effect_combo = ttk.Combobox(tab1, state='readonly')
effect_combo.bind("<<ComboboxSelected>>", combo_change)
effect_combo["values"] = ["none","volume","pitch","lag","saturation","noise","trip","crackle"]
effect_combo.current(0)
effect_combo.grid(column=1, row=6, sticky='NW')

effect_val = tk.Scale(tab1, from_=0, to=100, orient=tk.HORIZONTAL,command=slider_change)
effect_val.grid(column=1, row=7, sticky='NW')

#space
tab1.grid_columnconfigure(0, minsize=140)


#--------------TAB 2 ---------------------------------

def change_toggle(val):
    for i in range(0,9):
        if (i != val):
            alltoggle[i].set(settings.keybinds[i])

    if alltoggle[i].get() == "OFF":
        settings.keybindselected = val
    else:
        settings.keybindselected = -1
        

def askdirectory(i):
  dirname = tk.filedialog.askopenfile()
  if dirname:
    settings.songs[i].delete(0, tk.END)
    settings.songs[i].insert(0, dirname.name)

def key(event):
    v=settings.keybindselected
    if v != -1:
        print(repr(event.char))
        settings.keybinds[v] = repr(event.char)
        alltoggle[v].set(repr(event.char))
        
    


alltoggle = []

for r in range(0,9):
    input_song = tk.Entry(tab2,text="")
    input_song.grid(column=1, row=r, sticky='NW')
    
    settings.songs.append(input_song)
    
    dirBut = tk.Button(tab2, text='dir', command =lambda i = r: askdirectory(i))
    dirBut.grid(column=2, row=r, sticky='NW')
    
    button_playSound = tk.Button(tab2, text="PLAY SOUND", command=lambda i = r: click_playSound(i))
    button_playSound.grid(column=3, row=r, sticky='NW')
    
    settings.keybinds.append("OFF")
    
    var = tk.StringVar()
    toggle = tk.Checkbutton(tab2, onvalue="( )", offvalue="OFF", width=4,
                    indicatoron=False, 
                    variable=var, textvariable=var,
                    selectcolor="green", background="red",
                    command=lambda val = r: change_toggle(val))
    toggle.grid(row=r,column=4, sticky='NW')
    var.set("OFF")
    
    alltoggle.append(var)

tab2.grid_columnconfigure(0, minsize=50)

tab2.bind("<Key>", key)

#----------------------Keys

settings.key_thread = KeyThread()
settings.key_thread.start()

root.mainloop()
