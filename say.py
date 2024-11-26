from gtts import gTTS
from playsound import playsound

import gol
import os
 
def count_files(folder_path):
    file_list = os.listdir(folder_path)
    return len(file_list)

def say(text):
    if text == "" or text == None:
        return ""
    global_ip = gol.get_value('global_ip')
    # 将中文文本转换为语音
    tts = gTTS(text, lang='zh')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    voc_dir = current_dir + "/static/voice/" + global_ip + "/"
    voc_name = 'voice' + str(count_files(voc_dir)) + '.mp3'
    voc_path = voc_dir + voc_name


    current_dir = os.getcwd()
    # 保存语音为音频文件
    tts.save(voc_path)
    # 播放语音
    # playsound(voice_dir)

    return "static/voice/" + global_ip + "/" + voc_name