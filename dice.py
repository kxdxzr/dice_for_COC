
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:28:24 2022

@author: yulep
"""

from tkinter import *
from random import randint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import tkinter as Tk
import PySimpleGUI as sg
import time
import numpy as np
from datetime import datetime, date
import sys
import matplotlib.pylab as plt
  
######################### Saving #########################

def save_to_txt(data,title):
    f=open(title,'w')
    np.savetxt(f,data,delimiter=',',fmt='%s') 
    f.close() 

######################### Saving #########################


def Log(Info):
    time = datetime.now().strftime("%H:%M:%S")
    # generate time
    
    log_list.append("{}: {}".format(time, Info))
    # add new GUI including time and information
    
    log_window.update(values = log_list, scroll_to_index = len(log_list))
    #print(log_list)
    # update the window

def random(value):
    result = randint(1, value)
    result_str = str(result).zfill(3)
    color = "Black"
    if result > 94 and value == 100:
        color = "Red"
    elif result < 6 and value == 100:
        color = "Yellow"
    result_window.update(value = result_str, text_color = color)
    if Showing == "Show":
        result_window2.update(value = "1d{}: {} {}".format(value,skill_name,result_str), 
                             text_color = color)
    else:
        result_window2.update(value = "1d{}: {} {}".format("?","暗投","???"), 
                             text_color = "Black")
    Log("1d{}: {} {}".format(value,skill_name,result_str))


log_list = []


def Main_GUI():
    
    ############# initial value #############
    sg_theme = sg.theme("Default1")
    text_size = 18
    last_time = 0
    ran = 1
    tranmission_stable = True
    raw_y_list = []
    processed_y_list = []
    ploting_length = 5;
    raw_y_list = []
    high_warning = 100
    low_warning = 50
    Pulse_Ploting = "Processed"
    current = 0
    previous = 0
    first = True
    started = False
    tranmission_stable_time = True
    tranmission_stable_sequence = True
    tranmission_stop = False
    heart_rate_value = 70
    
    ############## log control ###############
    low_heart_rate_not_logged = True
    high_heart_rate_not_logged = True
    Tranmission_stop_by_user_not_logged = True
    Tranmission_unstable_not_logged = True
    global Showing
    Showing = "Show"
    ############## log control ###############
    
    
    ############# layout #############
    
    ############# initial value #############
    Column1 = sg.Column([
        [sg.Input(default_text = "",
                  size = (6, 2), 
                  key=("Skill"),
                  enable_events = True),],
        [sg.Button('1d3', key='1d3',size = (6,2))],
        [sg.Button('1d4', key='1d4',size = (6,2))],
        [sg.Button('1d6', key='1d6',size = (6,2))],
        [sg.Button('1d10', key='1d10',size = (6,2))],
        [sg.Button('1d100', key='1d100',size = (6,2))],
        [sg.Button('Calculate', key='Cal_Manual',size = (6,2))],
        [sg.Spin(["Show","Hide"],
                 size = (10,30),
                 enable_events=True,
                 key = "Choose_show",
                 initial_value = "Show")]
        ])
    Column2 = sg.Column([
        [sg.Text("000",key = "Result_Text",
                 font = ("Times New Roman",40))],
        [sg.Listbox([],size = (40, 15),key = "Log")],
        [sg.Input(default_text = "",
                  size = (40, 8), 
                  key=("Manual"),
                  enable_events = True),]
        ])
    
    layout = [
        [Column1,Column2,
         ],
        [sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))],
        ]
    
    layout2 = [
        [sg.Text("1d???: ？？ 000",key = "Showing",
             font = ("Times New Roman",80))]
        ]
    
    window = sg.Window("Dice", layout, finalize=True,resizable=True)
    window2 = sg.Window("Front_end", layout2, finalize=True,resizable=True)
    ############# layout #############
    global result_window
    result_window = window["Result_Text"]
    
    global result_window2
    result_window2 = window2["Showing"]
    
    Manual_dice = window["Manual"]
    global log_window
    log_window = window["Log"]
    
    global skill_name
    
    while True:
        event, values = window.read(timeout=0.1)
        skill_name = values["Skill"]
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
                Log("Exiting")
                save_to_txt(log_list,"log.log")
                print("close")
                window.close()
                window2.close()
                return
        elif event == '1d3':
            random(3)
        elif event == '1d4':
            random(4)
        elif event == '1d6':
            random(6)
        elif event == '1d10':
            random(10)
        elif event == '1d100':
            random(100)
        elif event == "Cal_Manual":
            result = 0
            Manual_input = values["Manual"]
            Manual_input_list = Manual_input.split("+")
            for cur in Manual_input_list:
                cur_list = cur.split("d")
                if len(cur_list) == 1:
                    result += int(cur_list[0])
                else:
                    number = int(cur_list[0])
                    value = int(cur_list[1])
                    i = 0
                    while i < number:
                        result += randint(1, value)
                        i += 1

            result_str = str(result).zfill(3)
            result_window.update(value = result_str)
            Log("{}:{} {}".format(Manual_input,skill_name,result_str))
        elif event == "Choose_show":
            Showing = values["Choose_show"]
        else:
            pass
        ##################### GUI Handling #####################

Main_GUI()