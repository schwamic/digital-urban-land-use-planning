def text2prompts(list_text):
    return list(map(lambda item: {"type": "text", "text": item}, list_text))
