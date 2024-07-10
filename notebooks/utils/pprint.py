"""Pretty Printer
"""
def pprint(data):
    if type(data) == list:
        for msg in data:
            print(str(msg).replace(r'\n', '\n'))
            print("#############################################")
    else:
        print(str(data).replace(r'\n', '\n'))
