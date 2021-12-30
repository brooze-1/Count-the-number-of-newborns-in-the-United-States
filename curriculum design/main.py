# 开发时间：2021/12/28  19:39
import csv
from zipfile import ZipFile
import requests
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image
from tkinter import messagebox as msgbox
import pygal
import cairosvg


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

class NEW_BORN(object):

    def download(self):
        """下载数据并将其保存到本地磁盘中"""
        print("正在下载数据：")
        url = "https://www.ssa.gov/oact/babynames/names.zip"

        # # 将获取到的names.zip作为response返回
        # with requests.get(url) as response:
        #     # 将response的内容写入names.zip中
        #     with open("datafile/names.zip", "wb") as temp_file:
        #         temp_file.write(response.content)

        def clicked():
            msgbox.showinfo("info", "数据下载成功！")
        clicked()
        print('数据下载成功！！！！！')

    def parse_zip(self):
        """读取ZIP文件的内容并用它们创建CSV文件"""
        print("正在解析数据：")
        # 读取ZIP文件的内容并用它们创建CSV文件.
        data_list = [["year", "name", "gender", "count"]]

        # 首先使用zip file.zip file对象读取zip文件
        with ZipFile("datafile/names.zip") as temp_zip:

            # 读取文件列表
            for file_name in temp_zip.namelist():

                # 只处理.txt文件
                if ".txt" in file_name:

                    # 从zip文件读取当前文件.
                    with temp_zip.open(file_name) as temp_file:

                        # 该文件以二进制方式打开，我们使用utf-8对其进行解码，以便可以将其作为字符串进行操作。
                        for line in temp_file.read().decode("utf-8").splitlines():
                            # 准备所需的数据字段并将它们添加到数据列表中
                            line_chunks = line.split(",")
                            # 获取年份
                            year = file_name[3:7]
                            # 获取姓名
                            name = line_chunks[0]
                            # 获取性别
                            gender = line_chunks[1]
                            # 获取名字的使用次数
                            count = line_chunks[2]

                            # 将获取到的四个字段添加到data_list列表中
                            data_list.append([year, name, gender, count])

        # 将数据列表保存到一个csv文件中.
        csv.writer(open("datafile/data3.csv", "w", newline="",
                        encoding="utf-8")).writerows(data_list)

        def clicked():
            msgbox.showinfo("info", "数据解析完成！")
        clicked()
        print("数据解析完成！！！！！")

    def write_to_database(self):
        '''将数据写入数据库'''
        print("开始将数据写入数据库：")
        # 连接数据库并将爬取到的数据存储到数据库中
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='jianmysql',
            database='test3',
            charset='utf8',
        )
        #  create table data(id int primary key auto_increment,year int,name char(32),gender char(32),count int);
        # 使用cursor()创建一个游标对象 cursor
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 写入前现将数据库中的数据删除
        sql = 'delete from data'
        # 执行删除数据表中数据的操作
        cursor.execute(sql)
        # 以读的方式打开一个data.csv文件（源文件）
        f = open('datafile/data1.csv', 'r', encoding='utf8')
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            year = line[0]
            name = line[1]
            gender = line[2]
            count = line[3]
            # print(year,name,gender,count)
            # 千万注意插入字符串时，占位符%S要加上引号引起来
            sql = "insert into data(year,name,gender,count) values(%s,'%s','%s',%s)" % (year, name, gender, count)
            # 将year,name,gender,count插入到数据表中
            cursor.execute(sql)
        # 提交操作数据库的操作
        conn.commit()
        def clicked():
            msgbox.showinfo("info", "成功将数据写入数据库！")
        clicked()
        print("成功将数据写入数据库！！！！")


    def read_data_with_pandas_from_mysql(self):
        """从mysql数据库中读取数据"""
        print("正在从数据库中读取数据：")
        # 使用pandas从数据库中读取数据
        # MySQL的用户：root, 密码:jianmysql, 端口：3306,数据库：
        engine = create_engine('mysql+pymysql://root:jianmysql@localhost:3306/new_born')
        sql = ''' select year,name,gender,count from data; '''
        # read_sql_query的两个参数: sql语句， 数据库连接
        df = pd.read_sql_query(sql, engine)
        # 将pandas读取到的是数据存入到temp_img.csv中用于后续的画表操作
        df.to_csv("datafile/temp_img.csv")
        print("打印前五行数据：\n",df.head())
        # 设置提示框
        def clicked():
            msgbox.showinfo("info", "成功读取数据库数据！")
        clicked()
        print('成功读取数据库数据！！！')
        return df

    # def write_data_from_sql_to_csv(self):
    #     """将数据库中的数据读取出来存到csv文件中方便后续画图"""
    #     print("正在从数据库中读取数据：")
    #     engine = create_engine('mysql+pymysql://root:jianmysql@localhost:3306/new_born')
    #     sql = ''' select year,name,gender,count from data; '''
    #     # read_sql_query的两个参数: sql语句， 数据库连接
    #     df = pd.read_sql_query(sql, engine)
    #     print("数据读取成功！！！！")
    #     df.to_csv("datafile/temp_img.csv")



    def plot_low_10_trending(self):
        # print("正在从数据库中读取数据：")
        # engine = create_engine('mysql+pymysql://root:jianmysql@localhost:3306/new_born')
        # sql = ''' select year,name,gender,count from data; '''
        # # read_sql_query的两个参数: sql语句， 数据库连接
        # df = pd.read_sql_query(sql, engine)
        df = pd.read_csv('datafile/temp_img.csv')
        print("数据读取成功！！！！")

        """画出最受欢迎的名字，以及它们是如何随着岁月的流逝而成长的。.
        """
        print("正在绘制图片：")
        # First we remove all records previous to 2008.
        filtered_df = df[df["year"] >= 2008]
        # print(filtered_df.head())
        '''
                 year      name gender  count
        1588437  2008      Emma      F  18817 
        1588438  2008  Isabella      F  18622
        1588439  2008     Emily      F  17437
        '''

        # 合并来自男性和女性的值，并以表格为轴，这样名称就是我们的索引，年份就是我们的列。
        # #还用零填充缺少的值。
        pivoted_df = filtered_df.pivot_table(
            index="name", columns="year", values="count", aggfunc=np.sum).fillna(0)
        # print(pivoted_df.head())  # 从2018年开始
        '''
        year     2008  2009  2010  2011  2012  2013  2014  2015  2016  2017  2018  .....
        name                                                                        
        Aaban     0.0   6.0   9.0  11.0  11.0  14.0  16.0  15.0   9.0  11.0   7.0   .....
        Aabha     0.0   0.0   0.0   7.0   5.0   0.0   9.0   7.0   7.0   0.0   0.0   .....
        '''

        # 计算每年每个名字的百分比.  指定名字被取次数/这一年内的名字总数
        percentage_df = pivoted_df / pivoted_df.sum() * 100

        # 添加了一个新列来存储累计百分比和.
        percentage_df["total"] = percentage_df.sum(axis=1)

        # 对数据帧进行排序，以检查哪些是顶级值并对其进行切片。在那之后删除“total”列，因为它将不再使用。(同样是根据total进行排序)
        sorted_df = percentage_df.sort_values(
            by="total", ascending=False).drop("total", axis=1)[0:10]
        # print(sorted_df.head())
        '''
        year          2008      2009      2010      2011      2012      2013  ....
        name                                                                   
        Emma      0.479382  0.469520  0.470274  0.515529  0.574004  0.575790   ....
        Olivia    0.435675  0.457235  0.461853  0.474568  0.474496  0.507002   ....
        Noah      0.403346  0.453777  0.447855  0.463678  0.477233  0.503789   ....
        '''

        # 翻转轴以便更容易地绘制数据帧.
        transposed_df = sorted_df.transpose()
        # print(transposed_df.head())
        '''
        name      Emma    Olivia      Noah    Sophia  Isabella     Jacob      Liam  ....
        year                                                                         
        2008  0.479382  0.435675  0.403346  0.409812  0.474724  0.576114  0.152480   ....
        2009  0.469520  0.457235  0.453777  0.444164  0.585086  0.555592  0.224898   ....
        2010  0.470274  0.461853  0.447855  0.559737  0.621527  0.600244  0.296494   .... 
        '''

        # 使用列名称作为标签和Y轴，分别绘制每个名称.
        for name in transposed_df.columns.tolist():
            # x轴为年份，y轴为人名每年出现的频率，图例为人名
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
        plt.savefig("img/trending_names2.png", facecolor="#443941")
        plt.close('all')

        def clicked():
            msgbox.showinfo("info", "图片成功绘制!")
        clicked()
        img = Image.open(
            'D:\\pycharm_professional\\PycharmProjects\\Python advanced programming\\curriculum design\\img\\total_by_year.png')
        plt.figure("trending_names")
        plt.imshow(img)
        plt.show()
        print("图片成功绘制!!!!!")

    def draw_pie(self):
        '''绘制饼状图（有关名字的首字母的分布情况）'''
        # 读取temp_img.csv中的是数据
        df = pd.read_csv('datafile/temp_img.csv')
        '''
             year       name gender  count
        0    1880       Mary      F   7065
        1    1880       Anna      F   2604
        2    1880       Emma      F   2003
        '''
        print("数据读取成功！！！！")
        print("正在绘制图片：")
        df['name'] = df['name'].map(lambda x: x[0])
        # print(df.head())
        '''
             year name gender  count
        0    1880    M      F   7065
        1    1880    A      F   2604
        2    1880    E      F   2003
        '''
        both_df = df.groupby("name").sum()
        del both_df['year']
        count_sum = sum(both_df['count'])
        both_df['total'] = both_df['count'] / count_sum
        '''
                   count     total
        name                                  
        A        30264825  0.084425
        B        17106077  0.047718
        C        26216242  0.073132
        D        24637980  0.068729
'''
        # 也就是name
        labels = both_df.index
        pie_chart = pygal.Pie()
        pie_chart.title = 'Proportion of surnames'
        for i in range(len(labels)):
            pie_chart.add(both_df.index[i], both_df['total'][i])
        pie_chart.render_to_file('./img/bar_chart.svg')

        svg_path = './img/bar_chart.svg'
        png_path = './img/bar_chart.png'
        cairosvg.svg2png(url=svg_path, write_to=png_path)

        def clicked():
            msgbox.showinfo("info", "图片成功绘制!")
        clicked()
        print("图片成功绘制!!!!!")

    def display_img(self):
        '''展示生成的图片'''
        img = Image.open(
            r'D:\pycharm_professional\PycharmProjects\Python advanced programming\curriculum design\img\bar_chart.png')
        plt.figure("trending_names")
        plt.imshow(img)
        plt.show()



    def main(self):
        """主函数"""
        # self.download() # 载数据并将其保存到本地磁盘中
        # self.parse_zip() # 读取ZIP文件的内容并用它们创建CSV文件
        # self.write_to_database() # 将数据写入数据库
        # self.read_data_with_pandas_from_mysql() # 从mysql数据库中读取数据
        # self.plot_low_10_trending() # 画出最受欢迎的名字，以及它们是如何随着岁月的流逝而成长的
        # self.write_data_from_sql_to_csv() # 将数据库中的数据读取出来存到csv文件中方便后续画图
        self.draw_pie() # 绘制饼状图（有关名字的首字母的分布情况）


if __name__=="__main__":
    obj = NEW_BORN()
    obj.main()