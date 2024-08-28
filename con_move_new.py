# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 09:20:54 2024

@author: blibl
"""

import VAPython as va
import os, csv, time, random
import numpy as np
from psychopy import gui, core, visual, event

current_working_dir = os.getcwd()
audio_path = os.path.join(current_working_dir, 'Stimuli_Buchstaben', 'f1_consonant')
path_va = os.path.join(current_working_dir, 'VA_full.v2023b.win64.vc14')
path_transfunc = os.path.join(current_working_dir, 'Input_Data', 'Directivities')
def VA_start_server(path_server):
    import os, psutil
    from subprocess import Popen, CREATE_NEW_CONSOLE
    tmp = os.getcwd()
    os.chdir(path_server)

    # Iterate over all running process.
    for proc in psutil.process_iter():
        try:
            if proc.name() == 'VAServer.exe':
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    os.startfile('run_VAServer.bat')
    os.chdir(tmp) 

def VA_stop_server():
    import os, psutil
    for proc in psutil.process_iter():
        try:

            if proc.name() == 'VAServer.exe':
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
def VA_generate_signal_sources(audio_path):   
    import os
    import VAPython as va
    signal_source_ids = {
        'F': va.create_signal_source_buffer_from_file(os.path.join(audio_path, 'f1_' + 'F' + '.wav')),
        'G': va.create_signal_source_buffer_from_file(os.path.join(audio_path, 'f1_' + 'G' + '.wav')),                                              
        'K': va.create_signal_source_buffer_from_file(os.path.join(audio_path, 'f1_' + 'K' + '.wav')),                                                    
        'L': va.create_signal_source_buffer_from_file(os.path.join(audio_path, 'f1_' + 'L' + '.wav')),
        'M': va.create_signal_source_buffer_from_file(os.path.join(audio_path, 'f1_' + 'M' + '.wav')),
        'R': va.create_signal_source_buffer_from_file(os.path.join(audio_path, 'f1_' + 'R' + '.wav')),
        }
    return signal_source_ids
def VA_generate_signal_sources1(audio_path):   
    import os
    import VAPython as va
    signal_source_ids = {
        'speech': va.create_signal_source_buffer_from_file(os.path.join(audio_path, 'combined_output' + '.wav')),
        }
    return signal_source_ids

def VA_generate_sound_sources(audio_path, positions_dict):
    import os
    import VAPython as va
    #Generate Sound sources                                                  
    sound_source_ids ={
        't_front':  va.create_sound_source( 'Source_t_front' ),
        't_left_60':   va.create_sound_source( 'Source_t_left' ),
        't_right_60':  va.create_sound_source( 'Source_t_right' ),
        't_front_30': va.create_sound_source( 'Source_t_front_30' ),
        't_front_60': va.create_sound_source( 'Source_t_front_60' ),
        't_left_60_30': va.create_sound_source( 'Source_t_left_60_30' ),
        't_left_60_60': va.create_sound_source( 'Source_t_left_60_60' ),
        't_right_60_30': va.create_sound_source( 'Source_t_right_60_30' ),
        't_right_60_60': va.create_sound_source( 'Source_t_right_60_60' ),
        }

    for idx in sound_source_ids:
        va.set_sound_source_position( sound_source_ids[idx], positions_dict[idx[2:]][0:3])
        va.set_sound_source_orientation_vu( sound_source_ids[idx], positions_dict[idx[2:]][3:6], [0, 1, 0])
    return sound_source_ids

def interpolate_positions(start_pos, end_pos, steps):
    """Generates a list of positions interpolating between start_pos and end_pos."""
    positions = []
    for i in range(steps):
        interp_pos = [
            start_pos[j] + (end_pos[j] - start_pos[j]) * (i / steps)
            for j in range(len(start_pos))
        ]
        positions.append(interp_pos)
    return positions
       
list_height     = 0;            
src_dist        = 2             
src_angle_60       = np.radians(60)   
src_angle_30      = np.radians(30)
height_30 = 1
height_60 = 3**(1/2)
positions_dict = { #Location, orientation
    'receiver': [0, list_height, 0, 0, 0, -1],
    'front':    [0, list_height, -2, 0, 0, 1],
    'left_60':     [-np.sin(src_angle_60)*src_dist, list_height, -np.cos(src_angle_60)*src_dist, 
                 np.sin(src_angle_60)*src_dist, 0, np.cos(src_angle_60)*src_dist],
    'right_60':    [np.sin(src_angle_60)*src_dist, list_height, -np.cos(src_angle_60)*src_dist, 
                 -np.sin(src_angle_60)*src_dist, 0, np.cos(src_angle_60)*src_dist],
    'front_30': [0, height_30, -(2-1/(3**(1/2))), 0, 0, 1],
    'front_60': [0, height_60, -1, 0, 0, 1],
    'left_60_60': [-src_dist*np.sin(src_angle_60)*np.sin(src_angle_60), src_dist*np.cos(src_angle_60),
                   -src_dist*np.sin(src_angle_60)*np.cos(src_angle_60), 0, 0, 1],
    'left_60_30': [-src_dist*np.sin(src_angle_60)*np.sin(src_angle_30), src_dist*np.cos(src_angle_30),
               -src_dist*np.sin(src_angle_30)*np.cos(src_angle_60), 0, 0, 1],
    'right_60_60': [src_dist*np.sin(src_angle_60)*np.sin(src_angle_60), src_dist*np.cos(src_angle_60),
               -src_dist*np.sin(src_angle_60)*np.cos(src_angle_60), 0, 0, 1],
    'right_60_30': [src_dist*np.sin(src_angle_60)*np.sin(src_angle_30), src_dist*np.cos(src_angle_30),
               -src_dist*np.sin(src_angle_30)*np.cos(src_angle_60), 0, 0, 1],
    }

keys_without_first = list(positions_dict.keys())[1:]
random_positions = random.sample(keys_without_first, 9)
VA_start_server(path_va)
va.connect()
#signal_source_ids = VA_generate_signal_sources(audio_path)
signal_source_ids1 = VA_generate_signal_sources1(audio_path)
sound_source_ids = VA_generate_sound_sources(audio_path, positions_dict)
#sound_source_ids1 = VA_generate_sound_sources_continuous(positions_dict_new, steps)
sound_receiver_id = va.create_sound_receiver( 'SoundReceiverMiddle' )
va.set_sound_receiver_position( sound_receiver_id, positions_dict['receiver'][0:3])
va.set_sound_receiver_orientation_vu( sound_receiver_id, positions_dict['receiver'][3:6], [0, 1, 0])
hrir_id = va.create_directivity_from_file(os.path.join(path_transfunc, 'ITA_KK_HRIR'+'.daff'))
va.set_sound_receiver_directivity( sound_receiver_id, hrir_id )
#S = va.create_sound_source('Comb')

#sound_keys = list(sound_source_ids.keys())
#sound_keys1 = list(sound_source_ids1.keys())
#signal_keys = list(signal_source_ids.keys())

#random.shuffle(signal_keys)
#random.shuffle(sound_keys)

signal_id1 = signal_source_ids1['speech']
S = va.create_sound_source('Source')
left_60 = [-np.sin(src_angle_60)*src_dist, list_height, -np.cos(src_angle_60)*src_dist]
left_60_60 = [-src_dist*np.sin(src_angle_60)*np.sin(src_angle_60), src_dist*np.cos(src_angle_60),
                   -src_dist*np.sin(src_angle_60)*np.cos(src_angle_60)]
x = 0
start_time = time.time()
while(x < 60):
    
    va.set_sound_source_position( S, [ -src_dist*np.sin(src_angle_60)*np.sin(np.radians(90-x)), 
                                  src_dist*np.cos(90-x),
                                  -src_dist*np.sin(90-x)*np.cos(src_angle_60)])
    time.sleep(1/60)
    va.set_sound_source_signal_source(S, signal_id1)
    va.set_signal_source_buffer_playback_action_str(signal_id1, 'play')
    x = x + 1
end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)