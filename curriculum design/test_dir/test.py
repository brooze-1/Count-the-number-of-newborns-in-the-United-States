# 开发时间：2021/12/28  20:15
import pymysql
import csv
import json
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from main import NEW_BORN as n
import pygal
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Edge

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
def readcsv():
    f = open('../datafile/data1.csv', 'r', encoding='utf8')
    reader = csv.reader(f)
    # next(reader)
    for line in reader:
        year = line[0]
        name = line[1]
        gender = line[2]
        count = line[3]
        print(year, name, gender, count)


def write_to_database():
    # 连接数据库
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='jianmysql',
        database='test2',
        charset='utf8',
        autocommit=True
    )
    # 使用cursor()创建一个游标对象 cursor
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    f = open('../datafile/data.csv', 'r', encoding='utf8')
    reader = csv.reader(f)
    next(reader)
    i = 1
    for line in reader:
        year = line[0]
        name = str(line[1])
        gender = line[2]
        count = line[3]
        # print(year,name,gender,count)
        sql = "insert into data(year,name,gender,count) values(%s,'%s','%s',%s)"%(year,name,gender,count)
        cursor.execute(sql)
        i += 1
        if i % 2000 == 0:
            print(i)
    # sql = 'select * from data'
    # data = cursor.execute(sql)
    # print(cursor.fetchall())
    # sql = 'delete from data'

def read_sql_with_pandas():
    # 连接数据库
    # MySQL的用户：root, 密码:147369, 端口：3306,数据库：test
    engine = create_engine('mysql+pymysql://root:jianmysql@localhost:3306/test2')
    sql = ''' select year,name,gender,count from data; '''
    # read_sql_query的两个参数: sql语句， 数据库连接
    df = pd.read_sql_query(sql, engine)
    print(df)

def test_png():
    """画出最受欢迎的名字，以及它们是如何随着岁月的流逝而成长的。.
            """
    obj = n()
    df = obj.read_data_with_pandas_from_mysql()
    # First we remove all records previous to 2008.
    print('开始绘制图片：')
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
    # '''
    # year     2008  2009  2010  2011  2012  2013  2014  2015  2016  2017  2018  .....
    # name
    # Aaban     0.0   6.0   9.0  11.0  11.0  14.0  16.0  15.0   9.0  11.0   7.0   .....
    # Aabha     0.0   0.0   0.0   7.0   5.0   0.0   9.0   7.0   7.0   0.0   0.0   .....
    # '''
    #
    # # 计算每年每个名字的百分比.  指定名字被取次数/这一年内的名字总数
    # percentage_df = pivoted_df / pivoted_df.sum() * 100
    #
    # # 添加了一个新列来存储累计百分比和.
    # percentage_df["total"] = percentage_df.sum(axis=1)
    #
    # # 对数据帧进行排序，以检查哪些是顶级值并对其进行切片。在那之后删除“total”列，因为它将不再使用。(同样是根据total进行排序)
    # sorted_df = percentage_df.sort_values(
    #     by="total", ascending=False).drop("total", axis=1)[0:10]
    # print(sorted_df.head())
    # '''
    # year          2008      2009      2010      2011      2012      2013  ....
    # name
    # Emma      0.479382  0.469520  0.470274  0.515529  0.574004  0.575790   ....
    # Olivia    0.435675  0.457235  0.461853  0.474568  0.474496  0.507002   ....
    # Noah      0.403346  0.453777  0.447855  0.463678  0.477233  0.503789   ....
    # '''

    # 翻转轴以便更容易地绘制数据帧.
    sorted_df = pivoted_df
    transposed_df = sorted_df.transpose()
    print(transposed_df.head())
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

    # # 将yticks设置为0.05%
    # yticks_labels = ["{:.2f}%".format(i) for i in np.arange(0.15, 0.66, 0.1)]
    # plt.yticks(np.arange(0.15, 0.66, 0.1), yticks_labels)

    yticks_labels = ["{:,}".format(i) for i in range(0, 4500000 + 1, 500000)]
    plt.yticks(np.arange(0, 4500000 + 1, 500000), yticks_labels)

    # 从2009年到2020年，我们将Xtick分为1步.
    xticks_labels = ["{}".format(i) for i in range(2008, 2020 + 1, 1)]
    plt.xticks(np.arange(2008, 2020 + 1, 1), xticks_labels)

    # 最终定制.
    plt.legend()
    plt.grid(False)
    plt.xlabel("Year")
    plt.ylabel("Percentage by Year")
    plt.title("Top 10 Trending Names")
    plt.savefig("../img/trending_names3.png", facecolor="#443941")
    print("图片成功绘制!!!!!")
    plt.close('all')


def draw():
    '''绘制饼状图'''
    df = pd.read_csv("../datafile/data.csv")
    print(df.head())
    df['name'] = df['name'].map(lambda x:x[0])
    print(df.head())
    both_df = df.groupby("name").sum()
    del both_df['year']
    count_sum = sum(both_df['count'])
    both_df['total'] = both_df['count']/count_sum
    labels = both_df.index
    pie_chart = pygal.Pie()
    pie_chart.title = 'Proportion of surnames'
    for i in range(len(labels)):
        pie_chart.add(both_df.index[i],both_df['total'][i])
    pie_chart.render_to_file('../img/bar_chart.svg')






if __name__=="__main__":
    # readcsv()
    # write_to_database()
    # read_sql_with_pandas()
    # test_png()
    draw()