# 下载新生儿信息数据的ZIP文件，读取其内容，并生成一个包含我们需要的字段的新CSV文件。

import csv
from zipfile import ZipFile

import requests

def download():
    """下载数据并将其保存到本地磁盘中"""

    url = "https://www.ssa.gov/oact/babynames/names.zip"

    with requests.get(url) as response:

        with open("names.zip", "wb") as temp_file:
            temp_file.write(response.content)


def parse_zip():
    global a
    a = '下载成功'
    """读取ZIP文件的内容并用它们创建CSV文件"""

    # 读取ZIP文件的内容并用它们创建CSV文件.
    data_list = [["year", "name", "gender", "count"]]

    #首先使用zip file.zip file对象读取zip文件
    with ZipFile("names.zip") as temp_zip:

        # 读取文件列表
        for file_name in temp_zip.namelist():

            # 只处理.txt文件
            if ".txt" in file_name:

                #从zip文件读取当前文件.
                with temp_zip.open(file_name) as temp_file:

                    #该文件以二进制方式打开，我们使用utf-8对其进行解码，以便可以将其作为字符串进行操作。
                    for line in temp_file.read().decode("utf-8").splitlines():

                        # 准备所需的数据字段并将它们添加到数据列表中
                        line_chunks = line.split(",")
                        year = file_name[3:7]
                        name = line_chunks[0]
                        gender = line_chunks[1]
                        count = line_chunks[2]

                        data_list.append([year, name, gender, count])



    #将数据列表保存到一个csv文件中.
    csv.writer(open("data.csv", "w", newline="",
                    encoding="utf-8")).writerows(data_list)


# 读取data.csv中的数据信息，并统计常见的分类信息。

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 200)

# 这些参数生成带有淡紫色的绘图。
sns.set(style="ticks",
        rc={
            "figure.figsize": [12, 7],
            "text.color": "white",
            "axes.labelcolor": "white",
            "axes.edgecolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "axes.facecolor": "#443941",
            "figure.facecolor": "#443941"}
        )


def get_essentials(df):
#按性别获取总数.
#df : pandas.DataFrame        要分析的数据帧.

    # 前5行.
    print(df.head())

    #后5行.
    print(df.tail())

    # 名字
    print(df["name"].nunique())         #nunique() 用于获取唯一值的统计次数

    # 男性名字.
    print(df[df["gender"] == "M"]["name"].nunique())

    # 女性名字.
    print(df[df["gender"] == "F"]["name"].nunique())


    both_df = df.pivot_table(
        index="name", columns="gender", values="count", aggfunc=np.sum).dropna()
    """
    透视表是一种可以对数据动态排布并且分类汇总的表格格式。或许大多数人都在Excel使用过数据透视表，也体会到它的强大功能，而在pandas中它被称作pivot_table。
    pivot_table有四个最重要的参数index、values、columns、aggfunc。
    Index就是层次字段，要通过透视表获取什么信息就按照相应的顺序设置字段；
    Columns类似Index可以设置列层次字段，它不是一个必要参数，作为一种分割数据的可选方式；
    Values可以对需要的计算数据进行筛选；
    aggfunc参数可以设置我们对数据聚合时进行的函数操作。当我们未设置aggfunc时，它默认aggfunc='mean'计算均值。
    """

    # 男性和女性都出现过的名字
    print(both_df.index.nunique())
    # print(both_df)


def totals_by_year(df):
    # 按性别获取最多的名字的数量及其出现的年份
    # df : pandas.DataFrame        The DataFrame to be analyzed.

    both_df = df.groupby("year").sum()
    print(both_df)
    male_df = df[df["gender"] == "M"].groupby("year").sum()
    female_df = df[df["gender"] == "F"].groupby("year").sum()

    print("Both Min:", both_df.min()["count"], "-", both_df.idxmin()["count"])
    # idxmin()返回第一次出现的最小值的索引（在这个表中就是年份值）

    print("Both Max:", both_df.max()["count"], "-", both_df.idxmax()["count"])
    # idxmax()返回第一次出现的最大值的索引（在这个表中就是年份值）

    print("Male Min:", male_df.min()["count"], "-", male_df.idxmin()["count"])
    print("Male Max:", male_df.max()["count"], "-", male_df.idxmax()["count"])
    print("Female Min:", female_df.min()[
        "count"], "-", female_df.idxmin()["count"])
    print("Female Max:", female_df.max()[
        "count"], "-", female_df.idxmax()["count"])


def get_top_10(df):
    # 获得前10个最常用的男性和女性姓名.
    # df : pandas.DataFrame

    # 创建了一个只有男性名字的新数据框，并统计数目，然后按降序排序.
    male_df = df[df["gender"] == "M"][["name", "count"]].groupby(
        "name").sum().sort_values("count", ascending=False)

    print(male_df.head(10))

    #  创建了一个只有女性名字的新数据框，并统计数目，然后按降序排序
    female_df = df[df["gender"] == "F"][["name", "count"]].groupby(
        "name").sum().sort_values("count", ascending=False)

    print(female_df.head(10))


def get_top_20_gender_neutral(df):
    # 获得前20个最常用的中性名名字.
    # df : pandas.DataFrame

    # 对数据帧进行筛选处理，使名称成为索引，使性别成为列
    df = df.pivot_table(index="name", columns="gender",
                        values="count", aggfunc=np.sum).dropna()

    # 仅限男女记录均大于50000条的姓名.
    df = df[(df["M"] >= 50000) & (df["F"] >= 50000)]
    print(df.head(20))


def plot_counts_by_year(df):
    """按男性、女性和组合绘制年份计数.
    """
    # 为男性、女性和组合创建了新的数据帧
    both_df = df.groupby("year").sum()  # groupby()是pandas的数据分组函数，这句代码表示按照"year"进行分组，再统计数据记录的数量

    male_df = df[df["gender"] == "M"].groupby("year").sum()  # 先筛选出性别为男性，再按"year"分组，再统计数据记录的数量

    female_df = df[df["gender"] == "F"].groupby("year").sum()

    # 画折线图

    # X轴为索引，Y轴为总数.
    plt.plot(both_df, label="Both", color="yellow")
    plt.plot(male_df, label="Male", color="lightblue")
    plt.plot(female_df, label="Female", color="pink")

    yticks_labels = ["{:,}".format(i) for i in range(0, 4500000 + 1, 500000)]
    # <格式控制标记>中{}表示占位符，如果有多个参数，可在{:}的:前面设定参数的序号
    # <格式控制标记>中逗号用于显示数字的千位分隔符

    plt.yticks(np.arange(0, 4500000 + 1, 500000), yticks_labels)  # 设定y轴的刻度值

    plt.legend()  # 显示图例项
    plt.grid(False)  # 不显示网格

    plt.xlabel("Year")
    plt.ylabel("Records Count")
    plt.title("Records per Year")

    plt.savefig("total_by_year.png", facecolor="#443941")  # facecolor参数表示图形表面颜色

    plt.close('all')  # 关闭所有图
    return both_df.head()


def plot_popular_names_growth(df):
    """画出最受欢迎的名字，以及它们是如何在岁月中成长起来的。
    """

    # 筛选数据，合并男性和女性的值，并对筛选表，这样名称就是索引，年份就是列，并用零填充缺少的值.
    pivoted_df = df.pivot_table(
        index="name", columns="year", values="count", aggfunc=np.sum).fillna(0)

    # 计算每年每个名字的百分比.
    percentage_df = pivoted_df / pivoted_df.sum() * 100

    # 添加一个新列来存储累计百分比和.
    percentage_df["total"] = percentage_df.sum(axis=1)

    # 我们对数据帧进行排序，以检查哪些是顶级值并对其进行切片。然后删除“总计”列，因为它将不再使用。最后取前10名。
    sorted_df = percentage_df.sort_values(
        by="total", ascending=False).drop("total", axis=1)[0:10]

    # 翻转轴以便更容易地绘制数据.
    transposed_df = sorted_df.transpose()

    # 使用列名称作为标签和Y轴，并分别绘制每个名称.
    for name in transposed_df.columns.tolist():
        plt.plot(transposed_df.index, transposed_df[name], label=name)

    # 将yticks设置为0.5
    yticks_labels = ["{}%".format(i) for i in np.arange(0, 5.5, 0.5)]
    plt.yticks(np.arange(0, 5.5, 0.5), yticks_labels)

    # 最终定制.
    plt.legend()
    plt.grid(False)
    plt.xlabel("Year")
    plt.ylabel("Percentage by Year")
    plt.title("Top 10 Names Growth")
    plt.savefig("most_popular_growth.png", facecolor="#443941")

    plt.close('all')


def plot_top_10_trending(df):
    """画出最受欢迎的名字，以及它们是如何随着岁月的流逝而成长的。.

    """

    # First we remove all records previous to 2008.
    filtered_df = df[df["year"] >= 2008]

    # 合并来自男性和女性的值，并以表格为轴，这样名称就是我们的索引，年份就是我们的列。
    # #还用零填充缺少的值。
    pivoted_df = filtered_df.pivot_table(
        index="name", columns="year", values="count", aggfunc=np.sum).fillna(0)

    # 计算每年每个名字的百分比.
    percentage_df = pivoted_df / pivoted_df.sum() * 100

    # 添加了一个新列来存储累计百分比和.
    percentage_df["total"] = percentage_df.sum(axis=1)

    # 对数据帧进行排序，以检查哪些是顶级值并对其进行切片。在那之后删除“total”列，因为它将不再使用。
    sorted_df = percentage_df.sort_values(
        by="total", ascending=False).drop("total", axis=1)[0:10]

    # 翻转轴以便更容易地绘制数据帧.
    transposed_df = sorted_df.transpose()

    # 使用列名称作为标签和Y轴，分别绘制每个名称.
    for name in transposed_df.columns.tolist():
        plt.plot(transposed_df.index, transposed_df[name], label=name)

    # 将yticks设置为0.05%
    yticks_labels = ["{:.2f}%".format(i) for i in np.arange(0.15, 0.66, 0.1)]
    plt.yticks(np.arange(0.15, 0.66, 0.1), yticks_labels)

    # 从2009年到2020年，我们将Xtick分为1步.
    xticks_labels = ["{}".format(i) for i in range(2008, 2020 + 1, 1)]
    plt.xticks(np.arange(2008, 2020 + 1, 1), xticks_labels)

    # 最终定制.
    plt.legend()
    plt.grid(False)
    plt.xlabel("Year")
    plt.ylabel("Percentage by Year")
    plt.title("Top 10 Trending Names")
    plt.savefig("trending_names.png", facecolor="#443941")

    plt.close('all')


import tkinter as tk
import ctypes
from tkinter import*
from tkinter import messagebox as msgbox
from PIL import Image
import matplotlib.pyplot as plt

def photo():
    img = Image.open('D:\Tencent\QQ文档\934431448\FileRecv\设计\\trending_names.png')
    plt.figure("trending_names")
    plt.imshow(img)
    plt.show()

    img = Image.open('D:\Tencent\QQ文档\934431448\FileRecv\设计\\total_by_year.png')
    plt.figure("total_by_year")
    plt.imshow(img)
    plt.show()

    img = Image.open('D:\Tencent\QQ文档\934431448\FileRecv\设计\most_popular_growth.png')
    plt.figure("most_popular_growth")
    plt.imshow(img)
    plt.show()

    def clicked():
        msgbox.showinfo("info","绘图完毕")
    clicked()

def kaisi():
    global a
    main_df = pd.read_csv("data.csv")  # pandas库读取csv文件的方法，默认第一行为列标题

    get_essentials(main_df)

    totals_by_year(main_df)

    get_top_10(main_df)
    #
    get_top_20_gender_neutral(main_df)

    plot_counts_by_year(main_df)  # 按男性、女性和总人数绘制年份计数图.

    plot_popular_names_growth(main_df)  # 画出最受欢迎的名字，以及它们在每一年中所占的比重图。

    def clicked():
        msgbox.showinfo("info","解析成功")
    clicked()

def abc():
    parse_zip()
    def clicked():
        msgbox.showinfo("info","下载成功")
    clicked()

class App(tk.Tk):
    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.title("课程设计！")
        self.state("zoomed")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

        self.geometry("300x400")

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)

        button = tk.Button(self, text='数据下载', width=15, command=abc).grid(row=0, column=0,sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='数据解析', width=15, command=kaisi).grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='写入数据库', width=15, ).grid(row=2, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='读取数据库数据', width=15, ).grid(row=3, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        button = tk.Button(self, text='绘出图形', width=15,command=photo).grid(row=4, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

app = App()
app.mainloop()
