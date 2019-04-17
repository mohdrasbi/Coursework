#!/usr/bin/env python3
 
from pynput import keyboard
import numpy as np
import pandas as pd
import time

timestamps = {}
raw_data = []
 
def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)
 
def on_press(key):
    press_time = time.time()
    key_name = get_key_name(key)

    print('Key {} pressed.'.format(key_name))

    if key_name != 'Key.esc':
        timestamps[key_name] = press_time

 
def on_release(key):
    release_time = time.time()
    key_name = get_key_name(key)

    print('Key {} released.'.format(key_name))

    if key_name == 'Key.esc':
        print('Exiting...')
        return False

    try:
        press_time = timestamps.pop(key_name)
        key_info = (key_name, press_time, release_time, release_time - press_time)
    except KeyError:
        press_time = timestamps.pop(key_name.upper())
        key_info = (key_name.upper(), press_time, release_time, release_time - press_time)

    key_info = (key_name, press_time, release_time, release_time - press_time)
    raw_data.append(key_info)


with keyboard.Listener(
    on_press = on_press,
    on_release = on_release) as listener:
    listener.join()


raw_data_arr = np.array(raw_data)
df = pd.DataFrame(raw_data_arr, columns=['key', 'press_time', 'release_time', 'hold_time'])
df.to_csv("output.csv")
