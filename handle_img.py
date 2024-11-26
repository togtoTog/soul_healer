import os
import requests
import matplotlib.pyplot as plt
import gol

from io import BytesIO
from meta_data import *

import matplotlib
matplotlib.use('module://ipympl.backend_nbagg')

import os

# 获取指定文件夹的文件数
def count_files(folder_path):
    file_list = os.listdir(folder_path)
    return len(file_list)

# 获取图片并添加文字，之后显示，这个会保存图片到本地
# 入参：img--图片文件名，text--需要添加的文本
# 出参：无
def get_image_from_local(img, text):
    text = insert_newlines(text, 40)
    url = 'https://bs3-hb1.corp.kuaishou.com/mmu-aiplatform-temp/' + img
    response = requests.get(url)

    # 将响应内容保存为图片文件
    with open('image.jpg', 'wb') as f:
        f.write(response.content)

    image = plt.imread('image.jpg')
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 防止中文乱码
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
    ax.annotate(text, xy=(0.5, -0.2), xycoords='axes fraction',
                ha='center', fontsize=12, color='green')
    # plt.text(0, 0, text, fontsize=15, color='green')
    plt.axis('off')
    # 自适应调整画布大小
    fig.tight_layout()
    # 显示图片
    plt.imshow(image)
    plt.show()

# 获取图片并添加文字，之后显示，这个不会保存图片
def get_image(img, text):
    text = insert_newlines(text, 40)
    url = 'https://bs3-hb1.corp.kuaishou.com/mmu-aiplatform-temp/' + img
    response = requests.get(url)

    # 将响应内容转换为文件对象
    image_file = BytesIO(response.content)

    image = plt.imread(image_file)
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 防止中文乱码
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
    ax.annotate(text, xy=(0.5, -0.2), xycoords='axes fraction',
                ha='center', fontsize=12, color='green')
    # plt.text(0, 0, text, fontsize=15, color='green')
    plt.axis('off')
    # 自适应调整画布大小
    fig.tight_layout()
    # 显示图片
    plt.imshow(image)
    plt.show()

# 保存图片到指定目录，返回path
def save_image(img, text):
    # 重新加载模块
    global_ip = gol.get_value('global_ip')
    print("global_ip:" + global_ip)

    url = 'https://bs3-hb1.corp.kuaishou.com/mmu-aiplatform-temp/' + img
    response = requests.get(url)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = current_dir + "/static/img/" + global_ip + "/"
    img_name = 'image' + str(count_files(img_dir)) + '.jpg'
    img_path = img_dir + img_name

    # 将响应内容保存为图片文件
    with open(img_path, 'wb') as f:
        f.write(response.content)
    return "static/img/" + global_ip + "/" + img_name

# 用来控制每行文字的长度
# 入参：text--原文本，n--长度
# 出参：格式化的文本
def insert_newlines(text, n):
    return '\n'.join(text[i:i+n] for i in range(0, len(text), n))

# test code
# img_url = "fbd0d2afbfc75b296cd1b91c0fa6e0df.png"
# get_image(img_url, "test")


