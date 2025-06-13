import re

def only_numbers(data):
    data = ''.join(filter(str.isdigit, data))  
    return data


def remove_space(data):
    return data.replace(" ", "")

def remove_special_characters(data):
    data = re.sub(r'[^a-zA-Z0-9]', '', data)
    return data

def remove_uppercase(data):
    data = ''.join(c for c in data if not c.isupper())
    return data