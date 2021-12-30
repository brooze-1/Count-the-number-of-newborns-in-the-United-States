# 开发时间：2021/11/29  10:24
# 在标准GUI程序Tkinter中使用matplotlib绘制图表，并能通过拖动左侧的滑块来控制绘制的图表

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# 构建App类继承tk.Tk
class App(tk.Tk):
    # 初始化操作，继承tk.Tk的类属性，并添加一个parent属性
    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        # 调用initialize()方法
        self.initialize()


    def initialize(self):
        # 设置窗口标题为在Tkinter中使用Matplotlib！
        self.title("在Tkinter中使用Matplotlib！")
        # 设置为全屏显示
        self.state("zoomed")
        # 设置第0行的控件随窗口变化
        self.rowconfigure(0, weight=1)
        # 设置第1行的控件不随窗口变化
        self.rowconfigure(1, weight=0)
        # 设置第0列的控件不随窗口变化
        self.columnconfigure(0, weight=0)
        # 设置第1列的控件不随窗口变化
        self.columnconfigure(1, weight=0)
        # 设置第2列的控件随窗口变化
        self.columnconfigure(2, weight=1)

        # 定义一个退出（Button）按钮，绑定on_click函数
        button = tk.Button(self, text="退出", width=6, height=2, command=self.on_click)
        # 将退出(Button)按钮布局在窗口的第1行第0列，并将按钮设置为四周对齐
        button.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W+tk.E)

        self.mu = tk.DoubleVar()                #实例化一个DoubleVar()类对象，用self.mu接收，其能自动刷新的浮点数变量，可用set和get方法进行传值和取值，类似的还有IntVar,StringVar
        self.mu.set(7.0)                        #参数的默认值是"mu"

        # 定义一个（slider_mu）滑块控件，绑定on_change方法
        # Scale()表示滑块；允许通过滑块来设置一数字值
        # resolution属性指定 Scale 组件的分辨率（步长，即在凹槽点击一下鼠标左键它移动的数量），默认值是 1
        slider_mu = tk.Scale(self,
                             from_=7, to=0, resolution=0.1,
                             label='mu', variable=self.mu,
                             command=self.on_change
                             )
        # 将（slider_mu）滑块控件布局在窗口的第0行第0列，并将该滑块控件设置为四周对齐
        slider_mu.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)

        # 实例化一个IntVar()类对象，用self.n接收，其能自动刷新的整型变量，可用set和get方法进行传值和取值
        self.n = tk.IntVar()
        self.n.set(512)  #参数的默认值是"n"

        # 定义一个（slider_n）滑块控件，绑定on_change方法,并且设置orient参数为横向放置，默认情况下是纵向放置的
        slider_n = tk.Scale(self,
                            from_=2, to=512,
                            label='n', variable=self.n, command=self.on_change,orient='horizonta')
        # 将（slider_mu）滑块控件布局在窗口的第0行第1列，并将该滑块控件设置为四周对齐
        # slider_n.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        # 修改成了跨列放，并将该控件布局在第1行第1列
        slider_n.grid(row=1, column=1,columnspan=2,sticky=tk.N+tk.S+tk.W+tk.E)

        # 指定画布fig的宽和高（单位为英寸），画布分辨率为96
        fig = Figure(figsize=(6, 4), dpi=96)
        # 将画布划分为一行一列，并取出第一张子图
        ax = fig.add_subplot(111)

        # 初始化数据和图表
        # 分别用x,y接收横纵坐标数据
        x, y = self.data(self.n.get(), self.mu.get())
        # 根据x,y数据绘制折线图
        self.line1, = ax.plot(x, y)

        # 生成一个FigureCanvasTkAgg的实例对象，并将我们之前定义的画布fig传入
        self.graph = FigureCanvasTkAgg(fig, master=self)        #FigureCanvasXAgg就是一个渲染器，渲染器的工作就是drawing，执行绘图的这个动作。渲染器是使物体显示在屏幕上
        canvas = self.graph.get_tk_widget()                     # 生成画布用变量canvas接收
        # 将画布（canvas）布局在窗口的第0行第2列，并将该画布控件设置为四周对齐
        canvas.grid(row=0, column=2, sticky=tk.N+tk.S+tk.W+tk.E)                            # 放置画布

    def on_click(self):
        # 退出窗口
        self.quit()

    # 重新生成一批数据，然后画图，然后显示
    def on_change(self, value):
        x, y = self.data(self.n.get(), self.mu.get())       # 获取当前滑块对应的数值，重新生成一批数据
        self.line1.set_data(x, y)                           # 重新画图
        # 更新graph
        self.graph.draw()                                   # 显示渲染器的结果，在窗口展示出来

    # 重新生成一批数据，数量为n，取值范围在[0,mu)之间
    def data(self, n, mu):
        # 创建一个空列表lst_y用于接收
        lst_y = []
        # n为此时slider_n滑块所在位置的示数，也就是此时对应的x轴的最大值
        for i in range(n):
            # 循环随机更改mu的值添加到lst_y中
            lst_y.append(mu * random.random())              # random()方法返回随机生成的一个实数,它在[0,1)范围内。
        # 返回两个列表对象
        return range(n), lst_y

if __name__ == "__main__":
    # 实例化一个App的对象
    app = App()
    app.mainloop()              # 通过mainloop()进入到事件（消息）循环。一旦检测到事件，就刷新组件。





'''
设计思想：结合matplotlib画图与tkinter制作窗口实现一个可以自变化的折线图，使用tkinter定义了一个两行三列的窗口，在tkinter定义的窗口中创建了四个控件分别是一个退出按钮控件，两个滑块控件，以及一个画布控件
，退出按钮用于实现退出窗口的作用，两个滑块控件用于调节matplotlib绘制的折线图的x,y轴的取值范围，画布控件用于动态渲染matplotlib绘制的折线图。
'''

