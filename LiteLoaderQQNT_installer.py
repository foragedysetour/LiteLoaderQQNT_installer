#coding=utf-8
import requests
import os
import winreg
import maliang
import threading
import tkinter.filedialog as _fd


class LiteLoaderQQNT_installer:
    def __init__(self):
        pass
    @staticmethod
    def get_qq_path():
        try:
            hive, subkey, value_name = winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\QQ", "UninstallString"
            key = winreg.OpenKey(hive, subkey)
            # 读取注册表项中指定名称的值
            uninstall_string, _ = winreg.QueryValueEx(key, value_name)
            uninstall_string = uninstall_string.strip('"')  # 去除路径两端的引号
            # 关闭注册表项
            winreg.CloseKey(key)
            if not uninstall_string or not os.path.exists(uninstall_string):
                raise FileNotFoundError("无法通过注册表读取 QQNT 的安装目录或路径不存在") 
            qq_exe_path = uninstall_string.replace("Uninstall.exe", "QQ.exe")
            qq_exe_path = qq_exe_path.replace("/", "\\")
            print(f"QQNT 的安装目录为: {qq_exe_path}")
        except Exception as e:
            print(e)
            print("请手动选择 QQ.exe 文件 ")  
        return qq_exe_path
    @staticmethod
    def get_lastest_version():
        try:
            latest_url = "https://github.com/Mzdyl/LiteLoaderQQNT_Install/releases/latest"
            response = requests.get(latest_url, timeout=2)
            last_version = response.url.split('/')[-1]
            print(f"最新版本为: {last_version}")
            return last_version
        except Exception as e:
            raise Exception(f"获取最新版本失败: {e}")

    def main_GUI(self):
        self.root = maliang.Tk(title="LiteLoaderQQNT 安装器", size=(600, 800))
        
        # Set up Canvas with place layout
        cv = maliang.Canvas(auto_zoom=True, keep_ratio="min", free_anchor=True)
        cv.place(x=300, y=400, width=600, height=800,anchor="center")
        app_info = maliang.Text(cv, (250, 10), text="📦 LiteLoaderQQNT 安装器",fontsize=30,anchor="n")

        y = 100
        # version label at top
        version_label = maliang.Text(cv, (10, y), text="版本: 获取中...")

        def _fetch_version():
            try:
                v = self.get_lastest_version()
                self.root.after(0, lambda: version_label.set(f"版本: {v}"))
                self.last_version = v
            except Exception:
                self.root.after(0, lambda: version_label.set("版本: 获取失败"))

        threading.Thread(target=_fetch_version, daemon=True).start()

        # input fields with browse buttons
        labels = ["QQ安装目录", "插件加载器安装目录", "插件存储目录"]
        inputs = []

        y+=40
        for idx, txt in enumerate(labels):
            maliang.Text(cv, (10, y), text=txt)
            ib = maliang.InputBox(cv, (150, y), size=(300, 30))
            inputs.append(ib)
            # prefill first input with qq path
            if idx == 0:
                try:
                    ib.set(self.get_qq_path())
                    self.qq_path = ib.get()
                except Exception:
                    pass

            def make_cmd(i):
                def cmd():
                    # choose a directory and update inputbox
                    path = _fd.askdirectory()
                    if path:
                        inputs[i].set(path)
                return cmd

            maliang.Button(cv, (460, y), size=(80, 25), text="浏览", command=make_cmd(idx))
            y += 50

        # bottom action buttons
        maliang.Button(cv, (150, 310), size=(100, 35), text="开始安装")
        maliang.Button(cv, (280, 310), size=(100, 35), text="开始卸载")

        self.root.mainloop()
if __name__ == '__main__':
    main_gui = LiteLoaderQQNT_installer()
    main_gui.main_GUI()