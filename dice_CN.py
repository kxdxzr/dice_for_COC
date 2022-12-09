
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

def load_from_log(title):
    f=open(title,'r')
    ls = f.read().split("\n")
    ls.remove('')
    return ls   
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
    try:
        settings[1] = values["Fumbles"].zfill(2)
        Fumbles_value = int(values["Fumbles"])
    except:
        result_window.update(value = "大失败错误", text_color = "Red")
        return
    try:
        settings[2] = values["Criticals"].zfill(2)
        Criticals_value = int(values["Criticals"])
    except:
        result_window.update(value = "大成功错误", text_color = "Red")
        return
    PC_name = values["PC"]
    
    color = "Black"
    if result > Fumbles_value - 1 and value == 100:
        color = "Red"
    elif result < Criticals_value + 1 and value == 100:
        color = "Gold"
    result_window.update(value = result_str, text_color = color)
    if Showing == "Show":
        result_window2.update(value = "{} {} 1d{}: {}".format(PC_name,skill_name, value,result_str), 
                             text_color = color)
    else:
        result_window2.update(value = "{} {} 1d{}: {}".format(PC_name,"暗投","?","???"), 
                             text_color = "Black")
    Log("{} {} 1d{}: {}".format(PC_name,skill_name,value,result_str))




def Main_GUI():
    
    ############# initial value #############
    sg_theme = sg.theme("Default1")
    global log_list
    log_list = []
    global settings
    try:
        settings = load_from_log('settings.set')
    except:
        settings = ["中文","96","05"]
    
    ############# initial value #############
    
    ############# Two languages #############
    skill_name_text = ["技能名", "Skill Name"]
    PC_name_text = ["PC名", "PC Name"]
    
    
    ############# Two languages #############
    
    ############## log control ###############
    global Showing
    Showing = "Show"
    global values
    ############## log control ###############
    
    
    ############# layout #############
    
    ############# initial value #############
    Column1 = sg.Column([
        [sg.Text("技能名",font = ("Times New Roman",12),key = "skill_name_key")],
        [sg.Input(default_text = "",
                  size = (10, 2), 
                  key=("Skill"),
                  enable_events = True),],
        [sg.Text("PC名",font = ("Times New Roman",12),key = "PC_name_key")],
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
        [sg.Button('自定义计算', key='Cal_Manual',size = (10,2))],
        ])
    Column2 = sg.Column([
        [sg.Text("结果",font = ("Times New Roman",12), key = "result_key")],
        [sg.Text("000",key = "Result_Text",
                 font = ("Times New Roman",40))],
        [sg.Text("日志",font = ("Times New Roman",12),key = "log_key")],
        [sg.Listbox([],size = (40, 15),key = "Log")],
        [sg.Text("自定义骰子",font = ("Times New Roman",12), key = "customized_dice_key")],
        [sg.Input(default_text = "",
                  size = (40, 8), 
                  key=("Manual"),
                  enable_events = True),]
        ])
    Column3 = sg.Column([
        [sg.Text("大失败",font = ("Times New Roman",12), key = "Fumbles_key")],
        [sg.Input(default_text = settings[1],
                  size = (4, 2), 
                  key=("Fumbles"),
                  enable_events = True)],
        [sg.Text("大成功",font = ("Times New Roman",12), key = "Criticals_key")],
        [sg.Input(default_text = settings[2],
                  size = (4, 2), 
                  key=("Criticals"),
                  enable_events = True)],
        [sg.Text("暗投?",font = ("Times New Roman",12))],
        [sg.Spin(["Show","Hide"],
                 size = (10,30),
                 enable_events=True,
                 key = "Choose_show",
                 initial_value = "Show")],
        [sg.Button('移除上一条', key='delete',size = (10,2))],
        [sg.Button('加载日志', key='load',size = (10,2))],
        [sg.Text("语言/Language",font = ("Times New Roman",12))],
        [sg.Spin(["中文","EN"],
                 size = (10,30),
                 enable_events=True,
                 key = "language",
                 initial_value = settings[0])],
        ])
    layout = [
        [Column1,Column2,Column3],
        [sg.Button('退出', key='EXIT_BUTTON',size = (5,2))],
        ]
    
    layout2 = [
        [sg.Text("1d???: ? ?  000",key = "Showing",
             font = ("Times New Roman",80))]
        ]
    window2 = sg.Window("Front_end", layout2, finalize=True,resizable=True)
    window = sg.Window("Dice", layout, finalize=True,resizable=True)
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
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            save_to_txt(log_list,"log.log")
            save_to_txt(settings,"settings.set")
            window.close()
            window2.close()
            return
        skill_name = values["Skill"]
        PC_name = values["PC"]
        if event == '1d3':
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
            try:
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
                result_window.update(value = result_str, text_color = "Black")
                
                result_window2.update(value = "{} {} {}: {}".format(PC_name, skill_name,Manual_input,result_str),text_color = "Black")
                
                Log("{} {} {}: {}".format(PC_name, skill_name, Manual_input,result_str))
            except:
                result_window.update(value = "输入错误", text_color = "Red")
        elif event == "Choose_show":
            Showing = values["Choose_show"]
        elif event == "load":
            try:
                log_list = load_from_log('log.log')
                log_window.update(values = log_list, scroll_to_index = len(log_list))
            except:
                result_window.update(value = "无日志文件", text_color = "Red")
        elif event == 'delete':
            try:
                log_list.pop()
                log_window.update(values = log_list, scroll_to_index = len(log_list))
                result_window.update(value = "000", text_color = "Black")
            except:
                pass
        elif event == 'language':
            pass
        else:
            pass
        ##################### GUI Handling #####################

Main_GUI()