# -*- coding: utf-8 -*-
"""
dice_for_COC - COC跑团骰子 / COC dice for TRPG
Merged bilingual version (中文 / EN), one-file with live language switch.

Author: kxdxzr (original by yuleping, 2022)
Merged: 2026
"""

from random import randint
from datetime import datetime
import os
import sys

# PySimpleGUI is now commercial; FreeSimpleGUI is the free fork with the same API.
# Support both so old environments keep working.
try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    import FreeSimpleGUI as sg


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log.log")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.set")

LANG_ZH = "中文"
LANG_EN = "EN"

TEXTS = {
    LANG_ZH: {
        "skill_name": "技能名",
        "pc_name": "PC名",
        "result": "结果",
        "log": "日志",
        "custom_dice": "自定义骰子",
        "fumbles": "大失败",
        "criticals": "大成功",
        "show_q": "暗投?",
        "btn_calc": "自定义计算",
        "btn_delete": "移除上一条",
        "btn_load": "加载日志",
        "btn_exit": "退出",
        "lang_label": "语言/Language",
        "err_fumbles": "大失败错误",
        "err_criticals": "大成功错误",
        "err_input": "输入错误",
        "err_no_log": "无日志文件",
        "hidden_skill": "暗投",
        "window_title": "Dice 骰子",
    },
    LANG_EN: {
        "skill_name": "Skill Name",
        "pc_name": "PC Name",
        "result": "Result",
        "log": "Log",
        "custom_dice": "Customized Dice",
        "fumbles": "Fumbles",
        "criticals": "Criticals",
        "show_q": "Show Results?",
        "btn_calc": "Calculate",
        "btn_delete": "Delete Last",
        "btn_load": "Load Log",
        "btn_exit": "Exit",
        "lang_label": "语言/Language",
        "err_fumbles": "Fumbles Error",
        "err_criticals": "Criticals Error",
        "err_input": "Input Error",
        "err_no_log": "No log file",
        "hidden_skill": "Hidden",
        "window_title": "Dice",
    },
}


def t(lang, key):
    return TEXTS[lang][key]


# ---------------- persistence (no numpy needed) ----------------

def save_to_txt(data, title):
    with open(title, "w", encoding="utf-8") as f:
        for line in data:
            f.write(str(line) + "\n")


def load_from_log(title):
    with open(title, "r", encoding="utf-8") as f:
        # filter out trailing empty lines instead of .remove('') which crashes
        return [line for line in f.read().splitlines() if line != ""]


# ---------------- dice logic (pure, testable) ----------------

def parse_manual(text):
    """Parse '1d3 + 2d6 + 2' (spaces allowed) -> total. Raises ValueError."""
    text = text.replace(" ", "")
    if not text:
        raise ValueError("empty")
    total = 0
    for cur in text.split("+"):
        if not cur:
            raise ValueError("empty term")
        parts = cur.lower().split("d")
        if len(parts) == 1:
            total += int(parts[0])
        elif len(parts) == 2:
            number = int(parts[0])
            value = int(parts[1])
            if number <= 0 or value <= 0:
                raise ValueError("non-positive dice")
            for _ in range(number):
                total += randint(1, value)
        else:
            raise ValueError("bad term: " + cur)
    return total


def dice_color(result, faces, fumbles_value, criticals_value):
    """Only d100 changes color."""
    if faces == 100:
        if result >= fumbles_value:
            return "Red"
        if result <= criticals_value:
            return "Gold"
    return "Black"


# ---------------- GUI ----------------

def apply_language(window, lang):
    window["skill_name_key"].update(t(lang, "skill_name"))
    window["PC_name_key"].update(t(lang, "pc_name"))
    window["result_key"].update(t(lang, "result"))
    window["log_key"].update(t(lang, "log"))
    window["customized_dice_key"].update(t(lang, "custom_dice"))
    window["Fumbles_key"].update(t(lang, "fumbles"))
    window["Criticals_key"].update(t(lang, "criticals"))
    window["show_label_key"].update(t(lang, "show_q"))
    window["lang_label_key"].update(t(lang, "lang_label"))
    window["Cal_Manual"].update(text=t(lang, "btn_calc"))
    window["delete"].update(text=t(lang, "btn_delete"))
    window["load"].update(text=t(lang, "btn_load"))
    window["EXIT_BUTTON"].update(text=t(lang, "btn_exit"))
    window.set_title(t(lang, "window_title"))


def Main_GUI():
    try:
        sg.theme("Default1")
    except Exception:
        pass

    try:
        settings = load_from_log(SETTINGS_FILE)
        if len(settings) < 3:
            raise ValueError("bad settings")
    except Exception:
        settings = [LANG_ZH, "96", "05"]

    lang = settings[0] if settings[0] in TEXTS else LANG_ZH

    global log_list, values, Showing, skill_name
    log_list = []
    Showing = "Show"

    col1 = sg.Column([
        [sg.Text(t(lang, "skill_name"), font=("Times New Roman", 12), key="skill_name_key")],
        [sg.Input(default_text="", size=(10, 2), key="Skill", enable_events=True)],
        [sg.Text(t(lang, "pc_name"), font=("Times New Roman", 12), key="PC_name_key")],
        [sg.Input(default_text="", size=(10, 2), key="PC", enable_events=True)],
        [sg.Button("1d3", key="1d3", size=(10, 2))],
        [sg.Button("1d4", key="1d4", size=(10, 2))],
        [sg.Button("1d6", key="1d6", size=(10, 2))],
        [sg.Button("1d8", key="1d8", size=(10, 2))],
        [sg.Button("1d10", key="1d10", size=(10, 2))],
        [sg.Button("1d100", key="1d100", size=(10, 2))],
        [sg.Button(t(lang, "btn_calc"), key="Cal_Manual", size=(10, 2))],
    ])
    col2 = sg.Column([
        [sg.Text(t(lang, "result"), font=("Times New Roman", 12), key="result_key")],
        [sg.Text("000", key="Result_Text", font=("Times New Roman", 40))],
        [sg.Text(t(lang, "log"), font=("Times New Roman", 12), key="log_key")],
        [sg.Listbox([], size=(40, 15), key="Log")],
        [sg.Text(t(lang, "custom_dice"), font=("Times New Roman", 12), key="customized_dice_key")],
        [sg.Input(default_text="", size=(40, 8), key="Manual", enable_events=True)],
    ])
    col3 = sg.Column([
        [sg.Text(t(lang, "fumbles"), font=("Times New Roman", 12), key="Fumbles_key")],
        [sg.Input(default_text=settings[1], size=(4, 2), key="Fumbles", enable_events=True)],
        [sg.Text(t(lang, "criticals"), font=("Times New Roman", 12), key="Criticals_key")],
        [sg.Input(default_text=settings[2], size=(4, 2), key="Criticals", enable_events=True)],
        [sg.Text(t(lang, "show_q"), font=("Times New Roman", 12), key="show_label_key")],
        [sg.Spin(["Show", "Hide"], size=(10, 30), enable_events=True,
                 key="Choose_show", initial_value="Show")],
        [sg.Button(t(lang, "btn_delete"), key="delete", size=(10, 2))],
        [sg.Button(t(lang, "btn_load"), key="load", size=(10, 2))],
        [sg.Text(t(lang, "lang_label"), font=("Times New Roman", 12), key="lang_label_key")],
        [sg.Spin([LANG_ZH, LANG_EN], size=(10, 30), enable_events=True,
                 key="language", initial_value=lang)],
    ])
    layout = [
        [col1, col2, col3],
        [sg.Button(t(lang, "btn_exit"), key="EXIT_BUTTON", size=(10, 2))],
    ]
    layout2 = [
        [sg.Text("1d???: ??? 000", key="Showing", font=("Times New Roman", 80))],
    ]

    window = sg.Window(t(lang, "window_title"), layout, finalize=True, resizable=True)
    window2 = sg.Window("Front_end", layout2, finalize=True, resizable=True)

    global result_window, result_window2, log_window
    result_window = window["Result_Text"]
    result_window2 = window2["Showing"]
    log_window = window["Log"]

    def do_log(info):
        time = datetime.now().strftime("%H:%M:%S")
        log_list.append("{}: {}".format(time, info))
        log_window.update(values=log_list, scroll_to_index=len(log_list))

    def do_random(faces):
        result = randint(1, faces)
        result_str = str(result).zfill(3)
        try:
            fumbles_value = int(values["Fumbles"])
            settings[1] = values["Fumbles"]
        except Exception:
            result_window.update(value=t(lang, "err_fumbles"), text_color="Red")
            return
        try:
            criticals_value = int(values["Criticals"])
            settings[2] = values["Criticals"]
        except Exception:
            result_window.update(value=t(lang, "err_criticals"), text_color="Red")
            return
        pc = values["PC"]
        color = dice_color(result, faces, fumbles_value, criticals_value)
        result_window.update(value=result_str, text_color=color)
        if Showing == "Show":
            result_window2.update(
                value="{} {} 1d{}: {}".format(pc, skill_name, faces, result_str),
                text_color=color)
        else:
            result_window2.update(
                value="{} {} 1d{}: {}".format(pc, t(lang, "hidden_skill"), "?", "???"),
                text_color="Black")
        do_log("{} {} 1d{}: {}".format(pc, skill_name, faces, result_str))

    skill_name = ""
    while True:
        event, values = window.read(timeout=100)
        # allow closing the front-end window without killing the app state
        if window2.was_closed():
            window2 = sg.Window("Front_end", layout2, finalize=True, resizable=True)
            result_window2 = window2["Showing"]
        # pump front-end window events so it stays responsive
        window2.read(timeout=0)

        if event in ("EXIT_BUTTON", sg.WIN_CLOSED):
            settings[0] = lang
            save_to_txt(log_list, LOG_FILE)
            save_to_txt(settings, SETTINGS_FILE)
            window.close()
            try:
                window2.close()
            except Exception:
                pass
            return

        skill_name = values.get("Skill", "")

        if event in ("1d3", "1d4", "1d6", "1d8", "1d10", "1d100"):
            do_random(int(event[1:]))
        elif event == "Cal_Manual":
            pc = values.get("PC", "")
            manual = values.get("Manual", "")
            try:
                result = parse_manual(manual)
                result_str = str(result).zfill(3)
                result_window.update(value=result_str, text_color="Black")
                result_window2.update(
                    value="{} {} {}: {}".format(pc, skill_name, manual, result_str),
                    text_color="Black")
                do_log("{} {} {}: {}".format(pc, skill_name, manual, result_str))
            except Exception:
                result_window.update(value=t(lang, "err_input"), text_color="Red")
        elif event == "Choose_show":
            Showing = values["Choose_show"]
        elif event == "load":
            try:
                loaded = load_from_log(LOG_FILE)
                log_list.clear()
                log_list.extend(loaded)
                log_window.update(values=log_list, scroll_to_index=len(log_list) if log_list else 0)
            except Exception:
                result_window.update(value=t(lang, "err_no_log"), text_color="Red")
        elif event == "delete":
            try:
                log_list.pop()
                log_window.update(values=log_list, scroll_to_index=len(log_list) if log_list else 0)
                result_window.update(value="000", text_color="Black")
            except IndexError:
                pass
        elif event == "language":
            new_lang = values["language"]
            if new_lang in TEXTS and new_lang != lang:
                lang = new_lang
                settings[0] = lang
                apply_language(window, lang)


if __name__ == "__main__":
    Main_GUI()
