# 下载新生儿信息数据的ZIP文件，读取其内容，并生成一个包含我们需要的字段的新CSV文件。

from main import NEW_BORN as n
import tkinter as tk
import ctypes
import threading

# 多线程解决tk处理大量数据的卡顿问题
class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


class App(tk.Tk):
    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.title("课程设计！")
        # self.state("zoomed")
        self.geometry("300x450")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)
        # 注意如何绑定类中方法携带参数
        button = tk.Button(self, text='数据下载',width=15, command=lambda:MyThread(n.download,self)).grid(row=0, column=0,sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='数据解析', width=15, command=lambda:MyThread(n.parse_zip,self)).grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='写入数据库', width=15, command=lambda:MyThread(n.write_to_database,self)).grid(row=2, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='读取数据库数据并存入本地csv文件', width=15,command=lambda:MyThread(n.read_data_with_pandas_from_mysql,self)).grid(row=3, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='绘出图形', width=15,command=lambda:n.plot_low_10_trending(self)).grid(row=4, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='退出', width=15,command=lambda:MyThread(self.quit)).grid(row=5, column=0, sticky=tk.N + tk.S + tk.W + tk.E)


app = App()
app.mainloop()
