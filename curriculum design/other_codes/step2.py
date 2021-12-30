# 读取data.csv中的数据信息，并统计常见的分类信息。
#coding:utf-8
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
    print(df["name"].nunique())         #nunique() 用于获取唯一值的统计次数 （相当于统计共有多少个不同的名字）

    # 男性名字.
    print(df[df["gender"] == "M"]["name"].nunique())  # 统计男性共有多少个不同的名字

    # 女性名字.
    print(df[df["gender"] == "F"]["name"].nunique())  # 统计女性共有多少个不同的名字

    '''
    gender                  F          M
    name                                
    Aaden                 5.0     4975.0
    Aadi                 16.0      933.0
    Aadyn                16.0      555.0
    Aalijah             149.0      244.0
    '''
    # 设置索引为"name",利用values只显示出"count",定义aggfunc=np.sum使得"count"列会自动计算数据的和，以"gender"字段来分割数据
    both_df = df.pivot_table(
        index="name", columns="gender", values="count", aggfunc=np.sum).dropna()
    """
    透视表是一种可以对数据动态排布并且分类汇总的表格格式。或许大多数人都在Excel使用过数据透视表，也体会到它的强大功能，而在pandas中它被称作pivot_table。
    pivot_table有四个最重要的参数index、values、columns、aggfunc。
    Index就是层次字段，要通过透视表获取什么信息就按照相应的顺序设置字段；
    Columns类似Index可以设置列层次字段，它不是一个必要参数，作为一种分割数据的可选方式；
    Values可以对需要的计算数据进行筛选； 利用“values”域显式地定义我们关心的列，就可以实现移除那些不关心的列
    aggfunc参数可以设置我们对数据聚合时进行的函数操作。当我们未设置aggfunc时，它默认aggfunc='mean'计算均值。
    
    pivot_table中一个令人困惑的地方是“columns（列）”和“values（值）”的使用。记住，变量“columns（列）”是可选的，它提供一种额外的方法来分割你所关心的实际值。然而，聚合函数aggfunc最后是被应用到了变量“values”中你所列举的项目上。
    """

    # 男性和女性都出现过的名字
    print(both_df.index.nunique())
    print(both_df.head())


def totals_by_year(df):
#按性别获取最多的名字的数量及其出现的年份
#df : pandas.DataFrame        The DataFrame to be analyzed.
    # 通过年份进行分组
    both_df = df.groupby("year").sum()
    print(both_df.head())
    '''
           count
    year        
    1880  201484
    1881  192691
    1882  221533
    1883  216944
    1884  243461
    '''
    # print(both_df)
    # 按年份进行分组，获取男性的姓名
    male_df = df[df["gender"] == "M"].groupby("year").sum()
    # 按年份进行分组，获取女性的姓名
    female_df = df[df["gender"] == "F"].groupby("year").sum()

    # 打印出哪一年份姓名数最少以及对应的年份
    print("Both Min:", both_df.min()["count"], "-", both_df.idxmin()["count"])
    #idxmin()返回第一次出现的最小值的索引（在这个表中就是年份值）

    # 打印出哪一年份姓名数最多以及对应的年份
    print("Both Max:", both_df.max()["count"], "-", both_df.idxmax()["count"])
    #idxmax()返回第一次出现的最大值的索引（在这个表中就是年份值）

    # 打印出哪一年份男性姓名数最少以及对应的年份
    print("Male Min:", male_df.min()["count"], "-", male_df.idxmin()["count"])
    # 打印出哪一年份男性姓名数最多以及对应的年份
    print("Male Max:", male_df.max()["count"], "-", male_df.idxmax()["count"])
    # 打印出哪一年份女性姓名数最少以及对应的年份
    print("Female Min:", female_df.min()[
          "count"], "-", female_df.idxmin()["count"])
    # 打印出哪一年份女性姓名数最多以及对应的年份
    print("Female Max:", female_df.max()[
          "count"], "-", female_df.idxmax()["count"])


def get_top_10(df):
# 获得前10个最常用的男性和女性姓名.
# df : pandas.DataFrame

    # 创建了一个只有男性名字的新数据框，并统计数目，然后按降序排序.
    male_df = df[df["gender"] == "M"][["name", "count"]].groupby(
        "name").sum().sort_values("count", ascending=False)
    '''
               count
    name            
    James    5190161
    John     5142243
    Robert   4829631
    Michael  4383488
    William  4143886
    '''
    print(male_df.head(10))

    #  创建了一个只有女性名字的新数据框，并统计数目，然后按降序排序
    female_df = df[df["gender"] == "F"][["name", "count"]].groupby(
        "name").sum().sort_values("count", ascending=False)

    print(female_df.head(10))
    '''
                 count
    name              
    Mary       4130314
    Elizabeth  1653689
    Patricia   1572554
    Jennifer   1468730
    Linda      1453408
    '''


def get_top_20_gender_neutral(df):
# 获得前20个最常用的中性名名字.
# df : pandas.DataFrame

    # 设置索引为"name",利用values只显示出"count",定义aggfunc=np.sum使得"count"列会自动计算数据的和，以"gender"字段来分割数据
    # 对数据帧进行筛选处理，使名称成为索引，使性别成为列
    df = df.pivot_table(index="name", columns="gender",
                        values="count", aggfunc=np.sum).dropna()
    print(df.head())
    '''
    gender         F       M
    name                    
    Aaden        5.0  4975.0
    Aadi        16.0   933.0
    '''

    # 仅限男女记录均大于50000条的姓名.
    df = df[(df["M"] >= 50000) & (df["F"] >= 50000)]
    print(df.head(20))
    '''
    gender          F         M
    name                       
    Alexis   340737.0   64889.0
    Angel     97209.0  241248.0
    '''


def plot_counts_by_year(df):
    """按男性、女性和组合绘制年份计数.并绘制一张每年有多少记录的图片
    """
    print(df.head())
    #为男性、女性和组合创建了新的数据帧
    both_df = df.groupby("year").sum()                              # groupby()是pandas的数据分组函数，这句代码表示按照"year"进行分组，再统计数据记录的数量

    print(both_df.head())
    '''
           count
    year        
    1880  201484
    1881  192691
    1882  221533
    '''
    male_df = df[df["gender"] == "M"].groupby("year").sum()         #先筛选出性别为男性，再按"year"分组，再统计数据记录的数量
    print(male_df.head())
    '''
           count
    year        
    1880  110490
    1881  100738
    '''
    female_df = df[df["gender"] == "F"].groupby("year").sum()        #再筛选出性别为女性，再按"year"分组，再统计数据记录的数量
    print(female_df.head())
    '''
           count
    year        
    1880   90994
    1881   91953
    '''

    # 画折线图

    # X轴为索引，Y轴为总数.
    plt.plot(both_df, label="Both", color="yellow")
    plt.plot(male_df, label="Male", color="lightblue")
    plt.plot(female_df, label="Female", color="pink")


    yticks_labels = ["{:,}".format(i) for i in range(0, 4500000+1, 500000)]
    #<格式控制标记>中{}表示占位符，如果有多个参数，可在{:}的:前面设定参数的序号
    #<格式控制标记>中逗号用于显示数字的千位分隔符

    plt.yticks(np.arange(0, 4500000+1, 500000), yticks_labels)      #设定y轴的刻度值


    plt.legend()                                                #显示图例项
    plt.grid(False)                                             #不显示网格

    plt.xlabel("Year")
    plt.ylabel("Records Count")
    plt.title("Records per Year")

    plt.savefig("img/total_by_year.png", facecolor="#443941")       #facecolor参数表示图形表面颜色

    plt.close('all')            #关闭所有图


def plot_popular_names_growth(df):
    """画出最受欢迎的名字，以及它们是如何在岁月中成长起来的。
    """

    # 设置索引为"name",利用values只显示出"count",定义aggfunc=np.sum使得"count"列会自动计算数据的和，以"year"字段来分割数据
    # 筛选数据，合并男性和女性的值，并对筛选表，这样名称就是索引，年份就是列，并用零填充缺少的值.
    pivoted_df = df.pivot_table(
        index="name", columns="year", values="count", aggfunc=np.sum).fillna(0)
    print(pivoted_df.head())
    '''
    year     1880  1881  1882  1883  1884  1885  1886  1887  1888  1889  1890  .....
    name                                                                        
    Aaban     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   .....
    Aabha     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   .....
    Aabid     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   .....
    Aabidah   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   .....
    Aabir     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   .....
    '''

    # 计算每年每个名字的百分比.   指定名字/这一年内的名字总数
    percentage_df = pivoted_df / pivoted_df.sum() * 100
    # print(percentage_df.head())

    #添加一个新列来存储累计百分比和.
    percentage_df["total"] = percentage_df.sum(axis=1)
    print(percentage_df.head())
    '''
    year     1880  1881  1882  1883  1884  1885  1886  1887  1888  1889  1890   ..... total
    name                                                                        
    Aaban     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   ..... 0.00278  
    Aabha     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   ..... 0.0078  
    Aabid     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   ..... 0.003278  
    Aabidah   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   ..... 0.008  
    Aabir     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   ..... 0.00378  
    '''

    # 我们对数据帧进行排序，以检查哪些是顶级值并对其进行切片。然后删除“总计”列，因为它将不再使用。最后取前10名（通过total字段进行排序）。
    sorted_df = percentage_df.sort_values(
        by="total", ascending=False).drop("total", axis=1)[0:10]
    print(sorted_df.head())
    '''
    year         1880      1881      1882      1883      1884      1885      1886   .....
    name                                                                            
    Mary     3.519882  3.605773  3.691549  3.707869  3.800609  3.805625  3.885758   .....
    John     4.814774  4.564302  4.332086  4.118113  3.872489  3.654081  3.554013   .....
    James    2.952592  2.836147  2.667774  2.419057  2.351917  2.159399  2.108751   .....
    '''


    # 翻转轴以便更容易地绘制数据.
    transposed_df = sorted_df.transpose()
    print(transposed_df.head())
    '''
    name      Mary      John     James   William    Robert   Michael   Charles  ......
    year                                                                         
    1880  3.519882  4.814774  2.952592  4.745786  1.204562  0.175696  2.659765   .....
    1881  3.605773  4.564302  2.836147  4.439232  1.115257  0.154652  2.414747   .....
    1882  3.691549  4.332086  2.667774  4.211111  1.133917  0.144899  2.308460   .....
    1883  3.707869  4.118113  2.419057  3.884413  1.080924  0.141511  2.232834   .....
    1884  3.800609  3.872489  2.351917  3.668349  1.016590  0.153207  1.980194   .....
    '''

    # 使用列名称作为标签和Y轴，并分别绘制每个名称.（循环取出每一列）
    for name in transposed_df.columns.tolist():
        # x轴为年份，y轴为人名这一年出现的概率，图例为人名
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
    plt.savefig("img/most_popular_growth.png", facecolor="#443941")

    plt.close('all')


def plot_top_10_trending(df):
    """画出最受欢迎的名字，以及它们是如何随着岁月的流逝而成长的。.
    """

    # First we remove all records previous to 2008.
    filtered_df = df[df["year"] >= 2008]
    print(filtered_df.head())
    '''
             year      name gender  count
    1588437  2008      Emma      F  18817
    1588438  2008  Isabella      F  18622
    1588439  2008     Emily      F  17437
    1588440  2008    Olivia      F  17084
    1588441  2008       Ava      F  17042
    '''

    
    # 合并来自男性和女性的值，并以表格为轴，这样名称就是我们的索引，年份就是我们的列。
    # #还用零填充缺少的值。
    pivoted_df = filtered_df.pivot_table(
        index="name", columns="year", values="count", aggfunc=np.sum).fillna(0)
    print(pivoted_df.head()) # 从2018年开始
    '''
    year     2008  2009  2010  2011  2012  2013  2014  2015  2016  2017  2018  .....
    name                                                                        
    Aaban     0.0   6.0   9.0  11.0  11.0  14.0  16.0  15.0   9.0  11.0   7.0   .....
    Aabha     0.0   0.0   0.0   7.0   5.0   0.0   9.0   7.0   7.0   0.0   0.0   .....
    Aabid     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   5.0   0.0   6.0   .....
    Aabidah   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   5.0   .....
    Aabir     0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   5.0   0.0   5.0   .....
    '''

    #计算每年每个名字的百分比.  指定名字被取次数/这一年内的名字总数
    percentage_df = pivoted_df / pivoted_df.sum() * 100

    # 添加了一个新列来存储累计百分比和.
    percentage_df["total"] = percentage_df.sum(axis=1)

    # 对数据帧进行排序，以检查哪些是顶级值并对其进行切片。在那之后删除“total”列，因为它将不再使用。(同样是根据total进行排序)
    sorted_df = percentage_df.sort_values(
        by="total", ascending=False).drop("total", axis=1)[0:10]
    print(sorted_df.head())
    '''
    year          2008      2009      2010      2011      2012      2013  ....
    name                                                                   
    Emma      0.479382  0.469520  0.470274  0.515529  0.574004  0.575790   ....
    Olivia    0.435675  0.457235  0.461853  0.474568  0.474496  0.507002   ....
    Noah      0.403346  0.453777  0.447855  0.463678  0.477233  0.503789   ....
    Sophia    0.409812  0.444164  0.559737  0.598491  0.611334  0.583754   ....
    Isabella  0.474724  0.585086  0.621527  0.545737  0.523566  0.485281   ....
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
    2011  0.515529  0.474568  0.463678  0.598491  0.545737  0.558214  0.368102   ....
    2012  0.574004  0.474496  0.477233  0.611334  0.523566  0.523101  0.460621   ....
    '''

    # 使用列名称作为标签和Y轴，分别绘制每个名称.
    for name in transposed_df.columns.tolist():
        # x轴为年份，y轴为人名每年出现的频率，图例为人名
        plt.plot(transposed_df.index, transposed_df[name], label=name)

    # 将yticks设置为0.05%
    yticks_labels = ["{:.2f}%".format(i) for i in np.arange(0.15, 0.66, 0.1)]
    plt.yticks(np.arange(0.15, 0.66, 0.1), yticks_labels)

    #从2009年到2020年，我们将Xtick分为1步.
    xticks_labels = ["{}".format(i) for i in range(2008, 2020+1, 1)]
    plt.xticks(np.arange(2008, 2020+1, 1), xticks_labels)

    # 最终定制.
    plt.legend()
    plt.grid(False)
    plt.xlabel("Year")
    plt.ylabel("Percentage by Year")
    plt.title("Top 10 Trending Names")
    plt.savefig("img/trending_names.png", facecolor="#443941")

    plt.close('all')


if __name__ == "__main__":

    main_df = pd.read_csv("../datafile/data.csv")           #pandas库读取csv文件的方法，默认第一行为列标题["year", "name", "gender", "count"]
    print(main_df.head())

    # # 将读取到的内容传入get_essentials函数
    # get_essentials(main_df)
    # '''
    # year,name,gender,count
    # 1880,Mary,F,7065
    # 1880,Anna,F,2604
    # 1880,Emma,F,2003
    # 1880,Elizabeth,F,1939
    # '''
    #
    # totals_by_year(main_df)
    # #
    # get_top_10(main_df)
    # # #
    # get_top_20_gender_neutral(main_df)
    #
    plot_counts_by_year(main_df)                 #按男性、女性和总人数绘制年份计数图.
    #
    # plot_popular_names_growth(main_df)          #画出最受欢迎的名字，以及它们在每一年中所占的比重图。
    # #
    # plot_top_10_trending(main_df)               #画出2008年之后最受欢迎的名字，以及它们在每一年中所占的比重图。

'''
再来讲解step2.py中的方法：
利用pandas库读取csv文件的方法，默认第一行为列标题["year", "name", "gender", "count"]
构造get_essentials方法，将读取到的内容传入，打印前五行，后五行，男性名字，女性名字数据，设置索引为"name",利用values只显示出"count",定义aggfunc=np.sum使得"count"列会自动计算数据的和，以"gender"字段来分割数据，再打印男性和女性都出现过的名字构造totals_by_year方法，将读取到的内容传入，通过年份进行分组，按年份进行分组输出前五行数据，获取男性的姓名，按年份进行分组，获取女性的姓名，打印出哪一年份姓名数最少以及对应的年份，打印出哪一年份姓名数最多以及对应的年份，打印出哪一年份男性姓名数最少以及对应的年份，打印出哪一年份男性姓名数最多以及对应的年份，打印出哪一年份女性姓名数最少以及对应的年份，打印出哪一年份女性姓名数最多以及对应的年份。
构造get_top_10方法，将读取到的内容传入，用于获得前10个最常用的男性和女性姓名.创建了一个只有男性名字的新数据框，并统计数目，然后按降序排序，输出前十条数据。创建了一个只有女性名字的新数据框，并统计数目，然后按降序排序，输出前十条数据。
构造get_top_20_gender_neutral方法，将读取到的内容传入，用于获得前20个最常用的中性名名字，设置索引为"name",利用values只显示出"count",定义aggfunc=np.sum使得"count"列会自动计算数据的和，以"gender"字段来分割数据，筛选仅限男女记录均大于50000条的姓名，并打印出前20行。
构造plot_counts_by_year方法，将读取到的内容传入，用于按男性、女性和组合绘制年份计数，并绘制一张每年有多少记录的图片。为男性、女性和组合创建了新的数据帧，先筛选出性别为男性，再按"year"分组，再统计数据记录的数量，再筛选出性别为女性，再按"year"分组，再统计数据记录的数量，画折线图，以X轴为索引，Y轴为总数，设定y轴的刻度值、不显示网格、不显示网格。定义好图形的横纵坐标标题以及图表题，在保存所有图片后，关闭所有图。
构造plot_popular_names_growth方法，将读取到的内容传入，用来画出最受欢迎的名字，以及它们是如何在岁月中成长起来的，设置索引为"name",利用values只显示出"count",定义aggfunc=np.sum使得"count"列会自动计算数据的和，以"year"字段来分割数据，计算每年每个名字的百分比，添加一个新列来存储累计百分比和.我们对数据帧进行排序，以检查哪些是顶级值并对其进行切片。然后删除“总计”列，因为它将不再使用。最后取前10名（通过total字段进行排序），翻转轴以便更容易地绘制数据.使用列名称作为标签和Y轴，并分别绘制每个名称.（循环取出每一列），将yticks设置为0.5，设定y轴的刻度值、不显示网格、不显示网格。定义好图形的横纵坐标标题以及图表题，在保存所有图片后，关闭所有图。
构造plot_top_10_trending方法，将读取到的内容传入，画出2008年之后最受欢迎的名字，以及它们在每一年中所占的比重图，合并来自男性和女性的值，并以表格为轴，这样名称就是我们的索引，年份就是我们的列，还用零填充缺少的值，计算每年每个名字的百分比，对数据帧进行排序，以检查哪些是顶级值并对其进行切片。在那之后删除“total”列，因为它将不再使用。(同样是根据total进行排序)，翻转轴以便更容易地绘制数据帧.使用列名称作为标签和Y轴，分别绘制每个名称.将yticks设置为0.05%，从2009年到2020年，我们将Xtick分为1步.以X轴为索引，Y轴为总数，设定y轴的刻度值、不显示网格、不显示网格。定义好图形的横纵坐标标题以及图表题，在保存所有图片后，关闭所有图。

'''
