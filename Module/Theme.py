import json
import os, sys
from tkinter import ttk
import tkinter as tk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)

class Theme:
    def __init__(self, master=None, theme=None):
        self.theme_json = []
        # 获取所有 Json 文件
        select_theme = None
        for path in [resource_path("Theme")] + (["Theme"] if os.path.abspath("Theme") != os.path.abspath(resource_path("Theme")) else []):
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    if file.split(".")[-1] == "json":
                        self.theme_json.append(os.path.join(root, file))
            # 加载
            if master and theme:
                for file in self.theme_json:
                    with open(file, "r", encoding="utf-8") as File:
                        Json = json.load(File)
                        keyword = Json.get("keyword")
                        for key, value in Json.get("theme").items():
                            if keyword + "." + key == theme:
                                select_theme = value
                                select_theme[0] = os.path.split(file)[0] + "\\" + select_theme[0]
                                break
        if select_theme:
            # 加载
            master.tk.call("source", select_theme[0])
            if select_theme[1].get("mode") == "call":
                master.tk.call("set_theme", select_theme[1].get("sorce"))
            elif select_theme[1].get("mode") == "style":
                ttk.Style().theme_use(select_theme[1].get("sorce"))
    def get(self):
        themes = []
        for file in self.theme_json:
            with open(file, "r", encoding="utf-8") as File:
                Json = json.load(File)
            keyword = Json.get("keyword")
            for key, value in Json.get("theme").items():
                themes.append(keyword + "." + key)
        return themes

