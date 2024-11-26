# from meta_data import *
from ketu import ketu, ketu_simillar, ketu_ref
from chat import chat


def kwaiyi(theme):
    presuppose_prefix = "你现在是一个电影的演员，你的角色是："

    character_1 = "一个性格孤僻的大叔，不苟言笑，发言冷酷犀利。"
    character_2 = "一个活泼的小萝莉，爱开玩笑，阳光有活力。"
    prompt = "以 %s 为主题，进行一场情景演出，现在你来给出第一句台词" % theme
    original_history = []

    question, original_history = chat(prompt, original_history)
    presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % question
    print("开场白: %s \n" % question)
    pic_key = ketu(question)
    for i in range(3):
        answer_1, query_history = chat(
            presuppose_prefix + character_1 + presuppose_suffix, original_history)
        print("AI 1 号: %s \n" % answer_1)
        ketu_ref(answer_1, pic_key, character_1)

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % answer_1
        original_history = query_history

        answer_2, query_history = chat(
            presuppose_prefix + character_2 + presuppose_suffix, original_history)
        print("AI 2 号: %s \n" % answer_2)
        ketu_ref(answer_2, pic_key, character_2)

        presuppose_suffix = "对方的台词是：%s 。请你根据他的台词给出回应。" % answer_2
        original_history = query_history