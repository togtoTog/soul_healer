import time

from meta_data import *
from handle_img import *

from chat import chat

from draw import draw_prepare, draw
from draw_ref import draw_ref_pic_prepare, draw_ref_pic
from draw_simillar import draw_simillar_pic_prepare, draw_simillar_pic


def ketu(prompt, frame):
    # TODO 这里可以加图片风格
    # new_prompt = "现在正在演短剧，请根据以下描述生成一个场景图：%s，画面风格是 %s。" % (prompt, frame)
    new_prompt = prompt + frame + "风格"
    print(new_prompt)
    task_id = draw_prepare(new_prompt)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw(task_id, new_prompt)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 4 or result_code == 1:
            print(result_code)
            return ketu_when_exception(prompt, frame)
        if result_code == 0:
            print("\n-----处理完成-----\n")
            if image_url_keys == []:
                return ketu_when_exception(prompt, frame)
            for key in image_url_keys:
                img_path = save_image(key, prompt)
                return key, img_path


def ketu_when_exception(prompt, frame):
    new_prompt = "将原场景描述转换成符合下列要求的文字：\
                1、字数在30字以内，简短精炼，能够包括角色的外貌特征和符合台词的场景描述；\
                2、参考示例如：都市女白领在被老板指责，全身，高级感，超写实，超细致，写实，精致，良好的照明，电影场景。\
                原场景描述是：%s" % prompt
    desc, _ = chat(new_prompt, [])
    print("desc:" + desc)
    return ketu(desc, frame)


def ketu_simillar(prompt, pic_key, character):
    new_prompt = "现在正在演短剧，说话者的人设是：%s。请根据以下台词生成相应的图片：%s，图片内容需要和之前的场景关联起来。" % (
        character, prompt)
    task_id = draw_simillar_pic_prepare(new_prompt, pic_key)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw_simillar_pic(task_id, new_prompt, pic_key)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 0:
            print("\n-----处理完成-----\n")
            for key in image_url_keys:
                img_path = save_image(key, prompt)
                return key, img_path


def ketu_ref(prompt, pic_key, character):
    new_prompt = "你是一个台词转场景描述的智能助手，可以根据原台词和人物描述转成符合以下要求的场景描述：\
        1、字数在30字以内，简短精炼，能够包括角色的外貌特征和符合台词的场景描述；\
            2、参考示例如：都市女白领在被老板指责，全身，高级感，超写实，超细致，写实，精致，良好的照明，电影场景。\
                原台词是：%s，人物描述是：%s，请转成相应的场景描述。重点：人物尤其是人脸部分保持一致！画面中只有2个人。" % (prompt, character)
    # new_prompt = "你是一个台词转场景描述的智能助手，可以根据原台词和人物描述转成符合以下要求的场景描述：\
    #     1、字数在30字以内，简短精炼，能够包括角色的外貌特征和符合台词的场景描述；\
    #         2、参考示例如：都市女白领在被老板指责，全身，高级感，超写实，超细致，写实，精致，良好的照明，电影场景。\
    #             原台词是：%s，人物描述是：%s，请转成相应的场景描述。" % (prompt, character)
    # desc, _ = chat(new_prompt, [])
    # print("desc:" + desc)
    # new_prompt = desc + "重点：人物部分保持一致！画面中只有2个人。"

    task_id = draw_ref_pic_prepare(new_prompt, pic_key)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw_ref_pic(task_id, new_prompt, pic_key)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 4 or result_code == 1:
            return ketu_ref_when_exception3(prompt, pic_key, character)
        if result_code == 0:
            print("\n-----处理完成-----\n")
            if image_url_keys == []:
                return ketu_ref_when_exception3(prompt, pic_key, character)
            for key in image_url_keys:
                img_path = save_image(key, prompt)
                return key, img_path

def ketu_ref_when_exception(prompt, pic_key, character):
    new_prompt = prompt

    task_id = draw_ref_pic_prepare(new_prompt, pic_key)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw_ref_pic(task_id, new_prompt, pic_key)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 4 or result_code == 1:
            return ketu_ref_when_exception2(prompt, pic_key, character)
        if result_code == 0:
            print("\n-----处理完成-----\n")
            if image_url_keys == []:
                return ketu_ref_when_exception2(prompt, pic_key, character)
            for key in image_url_keys:
                img_path = save_image(key, prompt)
                return key, img_path

def ketu_ref_when_exception2(prompt, pic_key, character):
    # new_prompt = "你是一个台词转场景描述的智能助手，可以根据原台词和人物描述转成符合以下要求的场景描述：\
    #     1、字数在30字以内，简短精炼，能够包括角色的外貌特征和符合台词的场景描述；\
    #         2、参考示例如：都市女白领在被老板指责，全身，高级感，超写实，超细致，写实，精致，良好的照明，电影场景。\
    #             原台词是：%s，人物描述是：%s，请转成相应的场景描述。重点：人物部分保持一致！画面中只有2个人。" % (prompt, character)
    # new_prompt = "你是句子转场景描述的高手，可以在不改变原意的基础上，将句子以场景描述的形式改写出来，与原来的句子相比要有较大的区别。\
    #     参考示例如：都市女白领在被老板指责，真实，光线明亮。请改写该句子：%s。不超过50字。只给出改写后的内容。" % prompt
    new_prompt = "你是句子转场景描述的高手，请将原来的句子转成另一种区别较大的表述\
        参考示例如：都市女白领在被老板指责，真实，光线明亮。请改写该句子：%s。不超过50字" % prompt
    desc, _ = chat(new_prompt, [])
    print("desc:" + desc)
    new_prompt = desc + "重点：人物尤其是人脸部分保持一致！画面中只有2个人。"

    task_id = draw_ref_pic_prepare(new_prompt, pic_key)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw_ref_pic(task_id, new_prompt, pic_key)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 4 or result_code == 1:
            return ketu_ref_when_exception3(desc, pic_key, character)
        if result_code == 0:
            print("\n-----处理完成-----\n")
            if image_url_keys == []:
                return ketu_ref_when_exception3(desc, pic_key, character)
            for key in image_url_keys:
                img_path = save_image(key, prompt)
                return key, img_path

def ketu_ref_when_exception3(prompt, pic_key, character):
    new_prompt = "你是一个台词转场景描述的智能助手，可以根据原台词和人物描述转成符合以下要求的场景描述：\
        1、字数在30字以内，简短精炼，能够包括角色的外貌特征和符合台词的场景描述；\
            2、参考示例如：都市女白领在被老板指责，全身，高级感，超写实，超细致，写实，精致，良好的照明，电影场景。\
                原台词是：%s，人物描述是：%s，请转成相应的场景描述。重点：人物部分保持一致！画面中只有2个人。" % (prompt, character)
    desc, _ = chat(new_prompt, [])
    print("desc:" + desc)
    new_prompt = desc + "重点：人物尤其是人脸部分保持一致！画面中只有2个人。"

    task_id = draw_ref_pic_prepare(new_prompt, pic_key)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw_ref_pic(task_id, new_prompt, pic_key)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 4 or result_code == 1:
            return ketu_ref(desc, pic_key, character)
        if result_code == 0:
            print("\n-----处理完成-----\n")
            if image_url_keys == []:
                return ketu_ref(desc, pic_key, character)
            for key in image_url_keys:
                img_path = save_image(key, prompt)
                return key, img_path


def test_draw(prompt):
    task_id = draw_prepare(prompt)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw(task_id, prompt)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 0:
            print("\n-----处理完成-----\n")
            for key in image_url_keys:
                get_image(key, prompt)
                return key


def test_draw_ref(prompt, pic_key):
    task_id = draw_ref_pic_prepare(prompt, pic_key)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw_ref_pic(task_id, prompt, pic_key)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 0:
            print("\n-----处理完成-----\n")
            for key in image_url_keys:
                get_image(key, prompt)
                return key


def test_draw_simillar(prompt, pic_key):
    task_id = draw_simillar_pic_prepare(prompt, pic_key)
    second = 0
    print("-----正在生成图片中-----")
    while True:
        result_code, image_url_keys = draw_simillar_pic(task_id, prompt, pic_key)
        time.sleep(1)
        second += 1
        print("\r已处理 %d 秒，请耐心等待" % second, end='')
        if result_code == 0:
            print("\n-----处理完成-----\n")
            for key in image_url_keys:
                get_image(key, prompt)
                return key


# prompt = "东京美少女，穿着和服走在街头"
# print(test_draw(prompt))

# img_url = "1b2c9a67b5a120925cf74ce392956aa4.png"
# prompt = "以这张照片为模版，生成这个女生生气摔杯子的图片"
# test_draw_ref(prompt, img_url)
# test_draw_simillar(prompt, img_url)