import json
import os, sys

class Sort_File:
    def __init__(self):
        self.file_criteria = {
            "文本": [".txt"],
            "图片": (".jpg", ".png", ".bmp", ".gif"),
            "应用": (".exe",),
            "快捷方式": (".lnk", ".url"),

            "办公文件": (".doc", ".docx", ".xls", ".xlsx", ".pptx"),
            "编程文件": (".json", ".cfg", ".jar", ".cpp", ".py")
        }
        self.ignore_file = [
            os.path.basename(__file__), "pyvenv.cfg", ".gitignore", "criteria.json"
        ]

        # 自建标准
        if os.path.exists("criteria.json"):
            with open("criteria.json", "r", encoding="utf-8") as criteria_file:
                criteria_data = json.load(criteria_file)
                self.file_criteria.update(criteria_data.get("criteria", {}))
                self.ignore_file += criteria_data.get("ignore", [])
    def sort(self, path=None):
        file_criteria = self.file_criteria
        ignore_file = self.ignore_file

        for file in os.listdir(path):
            if file not in ignore_file and os.path.isfile(file):
                file_info = os.path.splitext(file)[-1]
                if file_info:
                    # 获取
                    for dir_name, suffix in file_criteria.items():
                        if file_info in suffix:
                            if not os.path.exists(dir_name):
                                os.mkdir(dir_name)
                            os.replace(file, dir_name+"/"+file)

if __name__ == '__main__':
    sort()