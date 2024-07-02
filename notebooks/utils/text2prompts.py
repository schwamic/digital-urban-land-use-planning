"""Converts a list of text to a list of text prompts
@param: list of text
@return: list of text prompts
"""
def text2prompts(list_text):
    return list(map(lambda item: {"type": "text", "text": item}, list_text))
