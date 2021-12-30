# 下载新生儿信息数据的ZIP文件，读取其内容，并生成一个包含我们需要的字段的新CSV文件。
'''
设计思想：使用requests库下载生儿信息数据的ZIP文件，读取其内容，并生成一个包含我们需要的字段的新CSV文件（data.csv）。
然后读取data.csv中的数据信息，统计常见的分类信息，并绘制出相关的关系曲线。
'''

import csv
from zipfile import ZipFile

import requests


def download():
    """下载数据并将其保存到本地磁盘中"""

    url = "https://www.ssa.gov/oact/babynames/names.zip"

    # 将获取到的names.zip作为response返回
    with requests.get(url) as response:
        # 将response的内容写入names.zip中
        with open("../datafile/names.zip", "wb") as temp_file:
            temp_file.write(response.content)


def parse_zip():
    """读取ZIP文件的内容并用它们创建CSV文件"""

    # 读取ZIP文件的内容并用它们创建CSV文件.
    data_list = [["year", "name", "gender", "count"]]

    #首先使用zip file.zip file对象读取zip文件
    with ZipFile("../datafile/names.zip") as temp_zip:

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

    #将数据列表保存到一个csv文件中.
    csv.writer(open("../datafile/data.csv", "w", newline="",
                    encoding="utf-8")).writerows(data_list)


if __name__ == "__main__":

    # download()
    parse_zip()

# '''
# 首先定义了两个py文件分别是step1.py和step2.py两个python文件，step1.py用来下载新生儿信息数据的ZIP文件，读取其内容，并生成一个包含我们需要的字段的新CSV文件。
# step2.py用来读取data.csv中的数据信息，并统计常见的分类信息
# 先来讲解step1.py中的方法：
#     构造了download()方法用来载数据并将其保存到本地磁盘中，访问指定的url,将获取到的names.zip作为response返回,将response的内容写入names.zip中
#     构造parse_zip方法用来读取ZIP文件的内容并用它们创建CSV文件，首先使用zip file.zip file对象读取zip文件，读取文件列表，只处理.txt文件，从zip文件读取当前文件，该文件以二进制方式打开，我们使用utf-8对其进行解码，以便可以将其作为字符串进行操作，准备所需的数据字段并将它们添加到数据列表中，获取年份，获取姓名，获取性别，获取名字的使用次数，将获取到的四个字段添加到data_list列表中，将数据列表保存到一个csv文件中。
# '''