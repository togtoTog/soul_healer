from chat import chat

def gen_scene(theme, style):
    prompt = "请你扮演一个短剧场景生成器，你熟悉国内外流行的各种短剧，能够根据主题设计合适的场景。现在我给的主题是：%s。\
        请生成30字内的精炼的场景描述，注意场景中只有2个人物。" % theme
    answer, _ = chat(prompt, [])
    return answer

# scene = gen_scene("打工人职场发疯")
# print(scene)