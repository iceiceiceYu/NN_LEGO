import os
import JSON_loader
import Code_generator
from block import Block
from curve import Curve
if __name__ == '__main__':

    b_list, c_list = JSON_loader.loader('final_demo.json')
    print(c_list)
    print(b_list)

    id2block = {}
    for i in range(len(b_list)):
        id2block[b_list[i].b_id] = b_list[i]
        print(b_list[i])

    for i in range(len(c_list)):
        from_block = id2block[c_list[i].from_id]
        to_block = id2block[c_list[i].to_id]

        from_block.output.append(to_block)
        to_block.input.append(from_block)

    code = Code_generator.Translator(b_list).translate()
    print(code)

# for i in range(len(b_list)):
#     print(b_list[i].output)
#     print(b_list[i].input)