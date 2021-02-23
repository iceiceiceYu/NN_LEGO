import json
from block import Block
from curve import Curve


def loader(path):
    with open(path, 'r') as JSON_file:
        original = JSON_file.read()
    reformed = reform(original)
    data = json.loads(reformed)['pens']

    block_list = []
    curve_list = []

    for i in range(len(data)):
        tmp_data = data[i]
        if tmp_data['type'] == 0:
            block_list.append(Block(tmp_data['id'], tmp_data['name'], tmp_data['text'], tmp_data['data']))
        elif tmp_data['type'] == 1:
            curve_list.append(Curve(tmp_data['id'], tmp_data['name'], tmp_data['from']['id'], tmp_data['to']['id']))

    return block_list, curve_list


def reform(original):
    return original.replace(
        '"fontFamily":"\"Hiragino Sans GB\", \"Microsoft YaHei\", \"Helvetica Neue\", Helvetica, Arial",', '')
