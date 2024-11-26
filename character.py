from chat import chat

def gen_character(theme, scene):
    prompt = "请你扮演一个短剧角色生成器，你熟悉国内外流行的各种短剧，能够根据主题设计合适的角色，你给出的角色描述符合以下要求：\
    1、字数在30字以内，简短精炼，能够包括角色的外貌特征和性格特征；2、参考示例如：都市女白领，全身，高级感，超写实，超细致，写实，精致，良好的照明，电影场景；\
        性格温柔，待人友善。现在我给的主题是：%s，背景是：%s。请生成2个符合要求的角色描述。\
            输出2行内容，分别是角色1的姓名及人设，角色2的姓名及人设" % (theme, scene)
    answer, _ = chat(prompt, [])
    print(answer)
    lines = answer.split("\n")
    character_1 = lines[0]
    character_2 = lines[1]
    if character_2 == "":
        character_2 = lines[2]
    return character_1, character_2

# character_1, character_2 = gen_character("我一路打怪修仙，路上遇到三个真命天女，我最终抛弃爱情选择了事业")
# print("角色1:" + character_1)
# print("角色2:" + character_2)