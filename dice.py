
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:28:24 2022

@author: yuleping
"""

from random import randint
import PySimpleGUI as sg
import numpy as np
from datetime import datetime, date
import sys
  
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
    Fumbles_value = int(values["Fumbles"])
    Criticals_value = int(values["Criticals"])
    PC_name = values["PC"]
    
    color = "Black"
    if result > Fumbles_value - 1 and value == 100:
        color = "Red"
    elif result < Criticals_value + 1 and value == 100:
        color = "Yellow"
    result_window.update(value = result_str, text_color = color)
    if Showing == "Show":
        result_window2.update(value = "{} {} 1d{}: {}".format(PC_name,skill_name, value,result_str), 
                             text_color = color)
    else:
        result_window2.update(value = "{} {} 1d{}: {}".format(PC_name,"暗投","?","???"), 
                             text_color = "Black")
    Log("{} {} 1d{}: {}".format(PC_name,skill_name,value,result_str))


log_list = []


def Main_GUI():
    
    ############# initial value #############
    sg_theme = sg.theme("Default1")

    
    ############## log control ###############
    global Showing
    Showing = "Show"
    global values
    ############## log control ###############
    
    
    ############# layout #############
    
    ############# initial value #############
    Column1 = sg.Column([
        [sg.Text("Skill Name",font = ("Times New Roman",12))],
        [sg.Input(default_text = "",
                  size = (10, 2), 
                  key=("Skill"),
                  enable_events = True),],
        [sg.Text("PC Name",font = ("Times New Roman",12))],
        [sg.Input(default_text = "",
                  size = (10, 2), 
                  key=("PC"),
                  enable_events = True),],
        [sg.Button('1d3', key='1d3',size = (10,2))],
        [sg.Button('1d4', key='1d4',size = (10,2))],
        [sg.Button('1d6', key='1d6',size = (10,2))],
        [sg.Button('1d8', key='1d8',size = (10,2))],
        [sg.Button('1d10', key='1d10',size = (10,2))],
        [sg.Button('1d100', key='1d100',size = (10,2))],
        [sg.Button('Calculate', key='Cal_Manual',size = (10,2))],
        ])
    Column2 = sg.Column([
        [sg.Text("Result",font = ("Times New Roman",12))],
        [sg.Text("000",key = "Result_Text",
                 font = ("Times New Roman",40))],
        [sg.Text("Log ",font = ("Times New Roman",12))],
        [sg.Listbox([],size = (40, 15),key = "Log")],
        [sg.Text("Customized Dice",font = ("Times New Roman",12))],
        [sg.Input(default_text = "",
                  size = (40, 8), 
                  key=("Manual"),
                  enable_events = True),]
        ])
    Column3 = sg.Column([
        [sg.Text("Fumbles",font = ("Times New Roman",12))],
        [sg.Input(default_text = "96",
                  size = (4, 2), 
                  key=("Fumbles"),
                  enable_events = True)],
        [sg.Text("Criticals",font = ("Times New Roman",12))],
        [sg.Input(default_text = "05",
                  size = (4, 2), 
                  key=("Criticals"),
                  enable_events = True)],
        [sg.Text("Show Results?",font = ("Times New Roman",12))],
        [sg.Spin(["Show","Hide"],
                 size = (10,30),
                 enable_events=True,
                 key = "Choose_show",
                 initial_value = "Show")]
        ])
    layout = [
        [Column1,Column2,Column3
         ],
        [sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))],
        ]
    
    layout2 = [
        [sg.Text("1d???: ? ?  000",key = "Showing",
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
        elif event == '1d8':
            random(8)    
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
            
            result_window2.update(value = "{} {} {}: {}".format(PC_name, skill_name,Manual_input,result_str))
            
            Log("{} {}:{} {}".format(PC_name, Manual_input,skill_name,result_str))
        elif event == "Choose_show":
            Showing = values["Choose_show"]
        else:
            pass
        ##################### GUI Handling #####################

Main_GUI()