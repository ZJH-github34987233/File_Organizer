import json
import os, sys
import tkinter as tk
import tkinter.ttk as ttk
import ctypes

import Module.Theme as Theme

class Sort_File:
    def __init__(self):
        self.default_criteria = {}

        self.file_criteria = {
            "文本": (".txt", ),
            "图片": (".jpg", ".png", ".bmp", ".gif"),
            "快捷方式": (".lnk", ".url"),
            "办公文件": (".doc", ".docx", ".xls", ".xlsx", ".pptx"),
            "编程文件": (".json", ".cfg", ".jar", ".cpp", ".py")
        }
        self.ignore_file = [
            "pyvenv.cfg", ".gitignore", "criteria.json"
        ]

        self.default_criteria["criteria"] = self.file_criteria.copy()
        self.default_criteria["ignore"] = self.ignore_file.copy()

        self.updata()
    def updata(self):
        # 自建标准
        if os.path.exists("criteria.json"):
            with open("criteria.json", "r", encoding="utf-8") as criteria_file:
                criteria_data = json.load(criteria_file)
                self.file_criteria = criteria_data.get("criteria", self.default_criteria["criteria"])
                self.ignore_file = criteria_data.get("ignore", self.default_criteria["ignore"])
        else:
            self.file_criteria = self.default_criteria["criteria"]
            self.ignore_file = self.default_criteria["ignore"]
    def sort(self, path=None, file_criteria=None, ignore_file=None):
        if file_criteria is None:
            file_criteria = self.file_criteria
        if ignore_file is None:
            ignore_file = self.ignore_file

        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if file not in ignore_file and file_path:
                file_info = os.path.splitext(file_path)[-1]
                if file_info:
                    # 获取
                    for dir_name, suffix in file_criteria.items():
                        if file_info in suffix:
                            if not os.path.exists(os.path.join(path, dir_name)):
                                os.mkdir(os.path.join(path, dir_name))
                            os.replace(file_path, os.path.join(path, dir_name+"\\"+file))


class UI(tk.Tk):
    def __init__(self):
        super(UI, self).__init__()
        self.title("文件整理管理器")

        self.sort_file = Sort_File()
        self.sort_ui(self)

    def sort_ui(self, master):
        sort_frame = tk.Frame(master)
        sort_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 地址框
        path_frame = tk.Frame(sort_frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(path_frame, text="整理地址", bg="#e7e7e7").pack(side=tk.LEFT, ipady=5, ipadx=5)
        path_entry = ttk.Entry(path_frame)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        sort_button = ttk.Button(path_frame, text="开始整理")
        sort_button.pack(side=tk.LEFT, padx=5)
        tk.Label(sort_frame, text="请注意：以下规则仅在保存至规则文件后才可在下次开启时保留，请确保已完成保存后再关闭应用！", fg="red", anchor="e").pack(fill=tk.X)

        rule_treeview, ignore_treeview = self.rules(sort_frame)
        sort_button.configure(command=lambda:self.sort_file.sort(path=path_entry.get(), file_criteria=self.get_rule(rule_treeview), ignore_file=self.get_ignore(ignore_treeview)))

    def rules(self, master):
        rule_frame = tk.Frame(master)
        rule_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        criteria_frame = tk.Frame(rule_frame)
        criteria_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        edit_frame = tk.Frame(criteria_frame)
        edit_frame.pack(fill=tk.X, padx=5, pady=5)
        rule_treeview = ttk.Treeview(criteria_frame, columns=("name", "suffix"), show="headings", selectmode=tk.BROWSE)
        rule_treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        rule_treeview.heading("name", text="类")
        rule_treeview.heading("suffix", text="后缀")
        # 添加
        for name, suffix in self.sort_file.file_criteria.items():
            rule_treeview.insert("", tk.END, values=(name, suffix), iid=name)
        # 编辑
        ttk.Button(edit_frame, text="编辑规则", command=lambda:self.change_item(rule_treeview)).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="添加规则", command=lambda:self.change_item(rule_treeview, is_new=True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="删除规则", command=lambda:self.remove_rule(rule_treeview)).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="保存至规则文件", command=lambda:self.save_rule(rule_treeview)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(edit_frame, text="重置规则", command=lambda:self.reset_rule(rule_treeview)).pack(side=tk.RIGHT, padx=5)

        ttk.Separator(rule_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ignore_frame = tk.Frame(rule_frame)
        ignore_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        edit_frame = tk.Frame(ignore_frame)
        edit_frame.pack(fill=tk.X, padx=5, pady=5)
        ignore_treeview = ttk.Treeview(ignore_frame, columns=("file", ), show="headings", selectmode=tk.BROWSE)
        ignore_treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ignore_treeview.heading("file", text="忽略的文件")
        # 添加
        for file in self.sort_file.ignore_file:
            ignore_treeview.insert("", tk.END, values=(file, ), iid=file)

        def append_ignore():
            userinput = ignorefile_entry.get()
            if userinput:
                userinput_spilt = userinput.split(" ")
                for useinput in userinput_spilt:
                    ignore_treeview.insert("", tk.END, values=useinput, iid=useinput)

        tk.Label(edit_frame, text="忽略文件", bg="#e7e7e7").pack(side=tk.LEFT, ipady=5, ipadx=5)
        ignorefile_entry = ttk.Entry(edit_frame)
        ignorefile_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="添加忽略文件", command=append_ignore).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="删除忽略文件", command=lambda:self.remove_rule(ignore_treeview)).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="保存至规则文件", command=lambda:self.save_ignore(ignore_treeview)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(edit_frame, text="重置忽略文件规则", command=lambda:self.reset_ignore(ignore_treeview)).pack(side=tk.RIGHT, padx=5)
        return rule_treeview, ignore_treeview

    def save_rule(self, widget):
        file_criteria = self.get_rule(widget)
        # 保存至规则
        path = "criteria.json"
        # 读取原数据
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as criteria_file:
                data = json.load(criteria_file)
        else:
            data = {}
        data["criteria"] = file_criteria
        # 录入数据
        with open(path, "w", encoding="utf-8") as criteria_file:
            json.dump(data, criteria_file)
    def reset_rule(self, widget):
        # 保存至规则
        path = "criteria.json"
        # 读取原数据
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as criteria_file:
                data = json.load(criteria_file)
            if "criteria" in data:
                del data["criteria"]
            if data:
                # 录入数据
                with open(path, "w", encoding="utf-8") as criteria_file:
                    json.dump(data, criteria_file)
            else:
                # 删除文件
                os.remove(path)
        # 重新加载
        items = widget.get_children()
        for i in items:
            widget.delete(i)
        # 添加
        self.sort_file.updata()
        for name, suffix in self.sort_file.file_criteria.items():
            widget.insert("", tk.END, values=(name, suffix), iid=name)

    def save_ignore(self, widget):
        ignore = self.get_ignore(widget)
        # 保存至规则
        path = "criteria.json"
        # 读取原数据
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as criteria_file:
                data = json.load(criteria_file)
        else:
            data = {}
        data["ignore"] = ignore
        # 录入数据
        with open(path, "w", encoding="utf-8") as criteria_file:
            json.dump(data, criteria_file)
    def reset_ignore(self, widget):
        # 保存至规则
        path = "criteria.json"
        # 读取原数据
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as criteria_file:
                data = json.load(criteria_file)
            if "ignore" in data:
                del data["ignore"]
            if data:
                # 录入数据
                with open(path, "w", encoding="utf-8") as criteria_file:
                    json.dump(data, criteria_file)
            else:
                # 删除文件
                os.remove(path)
        # 重新加载
        items = widget.get_children()
        for i in items:
            widget.delete(i)
        # 添加
        self.sort_file.updata()
        for file in self.sort_file.ignore_file:
            widget.insert("", tk.END, values=(file, ), iid=file)

    def get_rule(self, widget):
        # 获取/处理规则
        items = widget.get_children()
        file_criteria = {}
        for i in items:
            values = widget.item(i)["values"]
            text, suffix = values
            suffix = suffix.split(" ")
            file_criteria[text] = suffix
        return file_criteria
    def get_ignore(self, widget):
        # 获取/处理规则
        items = widget.get_children()
        ignore = []
        for i in items:
            values = widget.item(i)["values"][0]
            ignore.append(values)
        return ignore

    def remove_rule(self, widget):
        userselect = widget.selection()
        for i in userselect:
            widget.delete(i)

    def change_item(self, widget, is_new=False):
        if not is_new:
            selection = widget.selection()
        else:
            selection = None

        if selection or is_new:
            change_toplevel = tk.Toplevel(self)
            change_toplevel.title("新增/编辑规则")

            change_frame = tk.Frame(change_toplevel)
            change_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

            edit_frame = tk.Frame(change_frame)
            edit_frame.pack(fill=tk.X, padx=5, pady=5)

            # 显示项
            item_treeview = ttk.Treeview(change_frame, columns=("suffix"), show="headings")
            item_treeview.pack(fill=tk.BOTH, expand=True)

            item_treeview.heading("suffix", text="后缀")

            tk.Label(edit_frame, text="类名", bg="#f0f0f0").pack(side=tk.LEFT, ipady=5, ipadx=5)
            name_entry = ttk.Entry(edit_frame)
            name_entry.pack(side=tk.LEFT, padx=5)

            if not is_new:
                selection = selection[0]
                selection_item = widget.item(selection)
                text = selection_item["values"][0]
                suffix = selection_item["values"][1].split(" ")
                for i in suffix:
                    item_treeview.insert("", tk.END, values=i, iid=i)
                name_entry.insert(tk.END, text)

            def append_suffix():
                userinput = append_entry.get()
                if userinput:
                    userinput_spilt = userinput.split(" ")
                    for useinput in userinput_spilt:
                        item_treeview.insert("", tk.END, values=useinput, iid=useinput)
            def remove_suffix():
                userselect = item_treeview.selection()
                for i in userselect:
                    item_treeview.delete(i)
            def save_suffix():
                if not is_new:
                    widget.item(selection, values=(name_entry.get(),) + (item_treeview.get_children(), ))
                else:
                    widget.insert("", tk.END, values=(name_entry.get(),) + (item_treeview.get_children(), ), iid=name_entry.get())
                change_toplevel.destroy()

            tk.Label(edit_frame, text="添加后缀", bg="#f0f0f0").pack(side=tk.LEFT, ipady=5, ipadx=5)
            append_entry = ttk.Entry(edit_frame)
            append_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            ttk.Button(edit_frame, text="添加后缀", command=append_suffix).pack(side=tk.LEFT, padx=5)
            ttk.Button(edit_frame, text="删除后缀", command=remove_suffix).pack(side=tk.LEFT, padx=5)
            ttk.Button(edit_frame, text="保存", command=save_suffix).pack(side=tk.RIGHT, padx=5)


root = UI()
theme = Theme.Theme(root, "theme.Sun-Valley.light")

#告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
#获取屏幕的缩放因子
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
#设置程序缩放
root.tk.call('tk', 'scaling', ScaleFactor/85)

root.mainloop()