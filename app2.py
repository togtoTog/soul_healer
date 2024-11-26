import os

from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO

from chat import chat
from ketu import ketu, ketu_ref, ketu_simillar
from empty_folder import empty_folder
from character import gen_character
from scene import gen_scene
from say import say

app = Flask(__name__)
socketio = SocketIO(app)

# 进入时清空文件夹
@app.route('/', methods=['GET', 'POST'])
def index():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = current_dir + "/static/img/"
    empty_folder(img_dir)
    voc_dir = current_dir + "/static/voice/"
    empty_folder(voc_dir)
    return render_template('index.html')

# 监听图片生成
@socketio.on('generate_image')
@app.route('/', methods=['GET', 'POST'])
def generate_image(data):
    # 获取输入的主题
    theme = data['theme']
    print("主题:" + theme)
    # 生成背景
    scene = gen_scene(theme)
    print("剧情背景: %s \n" % scene)
    # 生成主题和背景生成角色
    character_1, character_2 = gen_character(theme, scene)
    print("角色1:" + character_1)
    print("角色2:" + character_2)
    # 根据背景描述生成图片，后面的场景会用到这个做参考图
    pic_key, image_path = ketu(scene)
    socketio.emit('image_generated', {'image_path': image_path, 'answer': scene, 'voice': say(scene)})
    #生成开场台词
    prologue_prompt = "以 %s 为主题，背景是 %s，进行一场短剧演出，角色1的设定是:%s，角色2的设定是；%s。\
        请给出角色1的第一句台词，。" % (theme, scene, character_1, character_2)
    original_history = []
    prologue, original_history = chat(prologue_prompt, original_history)
    print("角色1: %s \n" % prologue)
    # 根据开场台词生成图片
    _, image_path = ketu_ref(prologue, pic_key, character_1)
    socketio.emit('image_generated', {'image_path': image_path, 'answer': prologue, 'voice': say(prologue)})
    
    presuppose_prefix = "你是一个演员，故事的背景是 %s 。你的角色设定是：。" % scene
    presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。只需要包括台词即可，不要有多余的内容。" % prologue
    
    for i in range(3):
        answer_2, query_history = chat(presuppose_prefix + character_2 + presuppose_suffix, original_history)
        print("角色2: %s \n" % answer_2)
        _, image_path = ketu_ref(answer_2, pic_key, character_1)
        socketio.emit('image_generated', {'image_path': image_path, 'answer': answer_2, 'voice': say(answer_2)})

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。只需要包括台词即可，不要有多余的内容。" % answer_2
        original_history = query_history

        answer_1, query_history = chat(presuppose_prefix + character_1 + presuppose_suffix, original_history)
        print("角色1: %s \n" % answer_1)
        _, image_path = ketu_ref(answer_1, pic_key, character_1)
        socketio.emit('image_generated', {'image_path': image_path, 'answer': answer_1, 'voice': say(answer_1)})

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。只需要包括台词即可，不要有多余的内容。" % answer_1
        original_history = query_history
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
