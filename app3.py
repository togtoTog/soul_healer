import logging
import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO

import gol
from app.SoulHealerAppService import SoulHealerAppService
from character import gen_character
from chat import chat
from empty_folder import empty_folder
from ketu import ketu, ketu_ref
from say import say
from scene import gen_scene

logger_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(message)s'
logger = logging.getLogger(__name__)

gol._init()

app = Flask(__name__)
socketio = SocketIO(app)

original_history = []
scene = ""
character_1, character_2 = "", ""
pic_key = ""


soul_healer_app = SoulHealerAppService()

# 进入时创建相应IP文件夹，已存在则清空
@app.route('/', methods=['GET', 'POST'])
def index():
    global original_history
    original_history = []

    # 根据ip创建个人文件夹
    global_ip = request.remote_addr
    gol.set_value('global_ip', global_ip)
    print("global_ip:" + global_ip)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 存放图片文件夹
    img_dir = current_dir + "/static/img/"
    new_img_dir = os.path.join(img_dir, global_ip)
    if not os.path.exists(new_img_dir):
        os.mkdir(new_img_dir)
    else:
        empty_folder(new_img_dir)

    # 存放语音文件夹
    voc_dir = current_dir + "/static/voice/"
    new_voc_dir = os.path.join(voc_dir, global_ip)
    if not os.path.exists(new_voc_dir):
        os.mkdir(new_voc_dir)
    else:
        empty_folder(new_voc_dir)

    return render_template('index.html')


# 一键生成
@socketio.on('generate_image')
@app.route('/', methods=['GET', 'POST'])
def generate_image(data):
    global original_history
    global scene
    global pic_key
    global character_1, character_2
    # 获取输入的主题
    theme = data['theme']
    print("主题:" + theme)
    # 获取输入的画面风格
    frame = data['frame']
    print("画面风格:" + frame)
    # 获取输入的台词风格
    style = data['style']
    print("台词风格:" + style)
    # 打开文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_dir = current_dir + "/static/style/"
    file = open(style_dir + style + ".txt", "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()

    # 生成背景
    scene = gen_scene(theme, style)
    print("剧情背景: %s \n" % scene)
    # 根据主题和背景生成角色
    character_1, character_2 = gen_character(theme, scene)
    print("角色1:" + character_1)
    print("角色2:" + character_2)
    # 根据背景描述生成图片，后面的场景会用到这个做参考图
    pic_key, image_path = ketu(scene, frame)
    socketio.emit('image_generated', {'image_path': image_path, 'answer': scene, 'voice': say(scene)})
    # 生成开场台词
    prologue_prompt = "以 %s 为主题，背景是 %s，进行一场短剧演出，角色1的设定是:%s，角色2的设定是；%s。\
        请给出角色1的第一句台词。格式仿照下列形式，姓名：台词。比如，张三：你真的好漂亮呀！" % (theme, scene, character_1, character_2)
    prologue_prompt = content + prologue_prompt
    print(prologue_prompt)

    prologue, original_history = chat(prologue_prompt, original_history)
    print("角色1: %s \n" % prologue)
    # 根据开场台词生成图片
    _, image_path = ketu_ref(prologue, pic_key, character_1)
    socketio.emit('image_generated', {'image_path': image_path, 'answer': prologue, 'voice': say(prologue)})
    presuppose_prefix = "你是一个演员，故事的背景是 %s 。你的角色设定是：" % scene
    presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % prologue
    for i in range(3):
        answer_2, query_history = chat(presuppose_prefix + character_2 + presuppose_suffix, original_history)
        print("角色2: %s \n" % answer_2)
        _, image_path = ketu_ref(answer_2, pic_key, character_1)
        socketio.emit('image_generated', {
            'image_path': image_path, 'answer': answer_2, 'voice': say(answer_2)})

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % answer_2
        original_history = query_history

        answer_1, query_history = chat(presuppose_prefix + character_1 + presuppose_suffix, original_history)
        print("角色1: %s \n" % answer_1)
        _, image_path = ketu_ref(answer_1, pic_key, character_1)
        socketio.emit('image_generated', {
            'image_path': image_path, 'answer': answer_1, 'voice': say(answer_1)})

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % answer_1
        original_history = query_history


# 生成背景角色
@socketio.on('generate_scene_character')
@app.route('/', methods=['GET', 'POST'])
def generate_scene_character(data):
    global original_history
    global scene
    global pic_key
    global character_1, character_2
    theme = data['theme']
    print("主题:" + theme)
    # 获取输入的画面风格
    frame = data['frame']
    print("画面风格:" + frame)
    # 获取输入的台词风格
    style = data['style']
    print("台词风格:" + style)
    # 打开文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_dir = current_dir + "/static/style/"
    file = open(style_dir + style + ".txt", "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()

    # 生成背景
    scene = gen_scene(theme, style)
    print("剧情背景: %s \n" % scene)
    # 生成主题和背景生成角色
    character_1, character_2 = gen_character(theme, scene)
    print("角色1:" + character_1)
    print("角色2:" + character_2)
    socketio.emit('scene_character_generated', {'scene': scene, 'character_1': character_1, 'character_2': character_2})


# 生成背景角色
@socketio.on('generate_scene_character2')
@app.route('/', methods=['GET', 'POST'])
def generate_scene_character2(data):
    global original_history
    global scene
    global pic_key
    global character_1, character_2
    theme = data['theme']
    print("主题:" + theme)
    # 获取输入的画面风格
    frame = data['frame']
    print("画面风格:" + frame)
    # 获取输入的台词风格
    style = data['style']
    print("台词风格:" + style)
    # 打开文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_dir = current_dir + "/static/style/"
    file = open(style_dir + style + ".txt", "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()

    # 生成背景
    scene = gen_scene(theme, style)
    print("剧情背景: %s \n" % scene)
    # 生成主题和背景生成角色
    character_1, character_2 = gen_character(theme, scene)
    print("角色1:" + character_1)
    print("角色2:" + character_2)
    socketio.emit('scene_character_generated2', {'scene': scene, 'character_1': character_1, 'character_2': character_2})


# 生成背景图和第一句台词
@socketio.on('generate_image_with_people')
@app.route('/', methods=['GET', 'POST'])
def generate_image_with_people(data):
    global original_history
    global scene
    global pic_key
    global character_1, character_2
    # 获取输入的主题
    theme = data['theme']
    print("主题:" + theme)
    # 获取输入的画面风格
    frame = data['frame']
    print("画面风格:" + frame)
    # 获取输入的台词风格
    style = data['style']
    print("台词风格:" + style)
    # 打开文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_dir = current_dir + "/static/style/"
    file = open(style_dir + style + ".txt", "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()

    scene = data['scene']
    print("剧情背景: %s \n" % scene)
    character_1 = data['character_1']
    character_2 = data['character_2']
    print("角色1:" + character_1)
    print("角色2:" + character_2)
    # 根据背景描述生成图片，后面的场景会用到这个做参考图
    pic_key, image_path = ketu(scene, frame)
    socketio.emit('image_generated', {
        'image_path': image_path, 'answer': scene, 'voice': say(scene)})
    # 生成开场台词
    prologue_prompt = "以 %s 为主题，背景是 %s，进行一场短剧演出，角色1的设定是:%s，角色2的设定是；%s。\
        请给出角色1的第一句台词。格式仿照下列形式，姓名：台词。比如，张三：你真的好漂亮呀！请严格遵守这个形式。" % (theme, scene, character_1, character_2)
    prologue_prompt = content + prologue_prompt
    print(prologue_prompt)

    prologue, original_history = chat(prologue_prompt, original_history)
    print("角色1: %s \n" % prologue)
    # 根据开场台词生成图片
    _, image_path = ketu_ref(prologue, pic_key, character_1)
    socketio.emit('image_with_people_generated', {'image_path': image_path, 'answer': prologue, 'voice': say(prologue)})


# 人机共创
@socketio.on('generate_image_with_lines')
@app.route('/', methods=['GET', 'POST'])
def generate_image_with_lines(data):
    global original_history
    global scene
    global pic_key
    global character_1, character_2
    # 获取输入的主题
    lines = data['lines']
    print("用户输入台词:" + lines)
    print("角色1: %s \n" % lines)
    # 根据开场台词生成图片
    _, image_path = ketu_ref(lines, pic_key, character_2)
    socketio.emit('image_generated', {
        'image_path': image_path, 'answer': lines, 'voice': say(lines)})

    presuppose_prefix = "你是一个演员，故事的背景是 %s 。你的角色设定是：" % scene
    presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % lines

    answer, query_history = chat(presuppose_prefix + character_1 + presuppose_suffix, original_history)
    print("角色2: %s \n" % answer)
    _, image_path = ketu_ref(answer, pic_key, character_1)
    socketio.emit('image_with_lines_generated', {
        'image_path': image_path, 'answer': answer, 'voice': say(answer)})

    original_history = query_history


# 生成背景图和第一句台词
@socketio.on('generate_image_multiverse')
@app.route('/', methods=['GET', 'POST'])
def generate_image_multiverse(data):
    global original_history
    global scene
    global pic_key
    global character_1, character_2
    # 获取输入的主题
    theme = data['theme']
    print("主题:" + theme)
    # 获取输入的画面风格
    frame = data['frame']
    print("画面风格:" + frame)
    # 获取输入的台词风格
    style = data['style']
    print("台词风格:" + style)
    # 打开文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_dir = current_dir + "/static/style/"
    file = open(style_dir + style + ".txt", "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()

    scene = data['scene']
    print("剧情背景: %s \n" % scene)
    character_1 = data['character_1']
    character_2 = data['character_2']
    print("角色1:" + character_1)
    print("角色2:" + character_2)
    # 根据背景描述生成图片，后面的场景会用到这个做参考图
    pic_key, image_path = ketu(scene, frame)
    socketio.emit('image_generated', {
        'image_path': image_path, 'answer': scene, 'voice': say(scene)})
    # 生成开场台词
    prologue_prompt = "以 %s 为主题，背景是 %s，进行一场短剧演出，角色1的设定是:%s，角色2的设定是；%s。\
        请给出角色1的3种可能的台词，注意是一个角色的3种不同可能的台词。回复的内容只需要包括3句台词，不要有多余的内容！\
            使用换行符隔开!" % (theme, scene, character_1, character_2)
    prologue_prompt = content + prologue_prompt
    print(prologue_prompt)

    answer_list, original_history = chat(prologue_prompt, original_history)
    print("角色1: %s \n" % answer_list)
    lines = answer_list.split("\n")
    answer_1 = lines[0]
    n = 1
    while lines[n] == "":
        n = n + 1
    answer_2 = lines[n]
    n = n + 1
    while lines[n] == "":
        n = n + 1
    answer_3 = lines[n]
    socketio.emit('image_multiverse', {'answer_1': answer_1, 'answer_2': answer_2, 'answer_3': answer_3})


# 生成背景图和第一句台词
@socketio.on('generate_image_multiverse2')
@app.route('/', methods=['GET', 'POST'])
def generate_image_multiverse2(data):
    global original_history
    global scene
    global pic_key
    global character_1, character_2
    # 获取输入的主题
    lines = data['lines']
    print("用户输入台词:" + lines)
    print("角色1: %s \n" % lines)
    # 根据开场台词生成图片
    _, image_path = ketu_ref(lines, pic_key, character_2)
    socketio.emit('image_generated', {
        'image_path': image_path, 'answer': lines, 'voice': say(lines)})

    presuppose_prefix = "你是一个演员，故事的背景是 %s 。你的角色设定是：" % scene
    presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % lines

    answer, query_history = chat(presuppose_prefix + character_1 + presuppose_suffix, original_history)
    print("角色2: %s \n" % answer)
    _, image_path = ketu_ref(answer, pic_key, character_1)
    socketio.emit('image_generated', {
        'image_path': image_path, 'answer': answer, 'voice': say(answer)})

    original_history = query_history

    presuppose_prefix = "你是一个演员，故事的背景是 %s 。你的角色设定是：" % scene
    presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。请给出该角色的3种可能的台词，注意是一个角色的3种不同可能的台词。\
        回复的内容只需要包括3句台词，不要有多余的内容！使用换行符隔开!" % answer

    answer_list, original_history = chat(presuppose_prefix + character_1 + presuppose_suffix, original_history)
    print("角色1: %s \n" % answer_list)
    lines = answer_list.split("\n")

    answer_1 = lines[0]
    n = 1
    while lines[n] == "":
        n = n + 1
    answer_2 = lines[n]
    n = n + 1
    while lines[n] == "":
        n = n + 1
    answer_3 = lines[n]
    socketio.emit('image_multiverse', {'answer_1': answer_1, 'answer_2': answer_2, 'answer_3': answer_3})


@app.route('/soul/healer/create', methods=['GET', 'POST'])
def create_soul_healer():
    prompt = request.args.get('prompt', '')
    print("create soul healer, prompt = {}".format(prompt))
    tripo_url = soul_healer_app.create_soul_healer(prompt)
    path = soul_healer_app.export_soul_healer(tripo_url)
    return {
        "code": 0,
        "message": "success",
        "data": {
            "path": path
        }
    }

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=logger_format)
    app.run(host='0.0.0.0', port=9999)
