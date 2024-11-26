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

# v1.5
@socketio.on('generate_image')
@app.route('/', methods=['GET', 'POST'])
def generate_image(data):
    theme = data['theme']
    print(theme)
    presuppose_prefix = "你现在是一个电影的演员，你的角色是："

    character_1 = "一个性格孤僻的大叔，不苟言笑，发言冷酷犀利。"
    character_2 = "一个活泼的小萝莉，爱开玩笑，阳光有活力。"
    prompt = "以 %s 为主题，进行一场情景演出，现在你来给出第一句台词" % theme
    original_history = []

    question, original_history = chat(prompt, original_history)
    presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % question
    print("开场白: %s \n" % question)
    pic_key, image_path = ketu(question)
    socketio.emit('image_generated', {'image_path': image_path, 'answer': question, 'voice': say(question)})
    for i in range(3):
        answer_1, query_history = chat(
            presuppose_prefix + character_1 + presuppose_suffix, original_history)
        print("AI 1 号: %s \n" % answer_1)
        _, image_path = ketu_ref(answer_1, pic_key, character_1)
        socketio.emit('image_generated', {'image_path': image_path, 'answer': answer_1, 'voice': say(answer_1)})

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % answer_1
        original_history = query_history

        answer_2, query_history = chat(
            presuppose_prefix + character_2 + presuppose_suffix, original_history)
        print("AI 2 号: %s \n" % answer_2)
        _, image_path = ketu_ref(answer_2, pic_key, character_2)
        socketio.emit('image_generated', {'image_path': image_path, 'answer': answer_2, 'voice': say(answer_2)})

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % answer_2
        original_history = query_history

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
