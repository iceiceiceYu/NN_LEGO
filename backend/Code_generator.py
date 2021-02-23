from block import Block
from pytorch_block import PytorchBlockFactory

var_index = 0
"""

1. Input: (x)
2. Conv2D:
3. MaxPooling2D
4. ReLU
5. Linear
6. Softmax
7. Concat
8. ResIncp
"""
class Container:
    pass

class Translator:
    def __init__(self, b_list):
        self.template_code = \
"""
import torch
import torch.nn

class MyModel(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
[INIT_AREA]

    def forward(self, *input: Any, **kwargs: Any) -> T_co:
[FORWARD_PROPRAGATION_AREA]
"""
        self.template_code_init_replace = "[INIT_AREA]"
        self.template_code_forw_replace = "[FORWARD_PROPRAGATION_AREA]"

        self.var_index = 0
        self.out_index = 0
        self.block_list = b_list
        self.layer_names = []
        self.start_block = None

    def translate(self):
        self.model_init()
        self.repl_forward()
        return self.template_code

    def model_init(self):
        # find input block by name
        b_list = self.block_list
        input_block = None
        for i in range(len(b_list)):
            if b_list[i].name == "Input":
                input_block = b_list[i]
                self.start_block = input_block
                break

        init_declarations = []

        # walk through the graph and mark nodes
        block_to_deal = [input_block]
        while len(block_to_deal) != 0:
            curr_block = block_to_deal.pop(0)
            if Translator.check_input(curr_block):
                curr_block.declared_var_name = self.gen_var_name(curr_block)
                line_code = '\t\t' + Translator.block_to_var_declaration(curr_block, curr_block.declared_var_name)
                if line_code.strip(): init_declarations.append(line_code)
                # 用for循环是为了不重复加入
                for next_block in curr_block.output:
                    if next_block not in block_to_deal:
                        block_to_deal.append(next_block)

        self.template_code = self.template_code.replace(self.template_code_init_replace, '\n'.join(init_declarations))

    def repl_forward(self):
        # 给 Input 也加上之前的东西，这些都是Mock的家的东西
        mockInput = Container()
        mockInput.output_var_name = "input"
        mockInput.declared_var_name = "input"
        self.start_block.input.append(mockInput)

        block_to_deal = [self.start_block]
        forward_codes = []
        end_blocks = []  # 可能有多个返回值

        while len(block_to_deal) != 0 :
            curr_block = block_to_deal.pop(0)
            if Translator.check_input_2(curr_block):
                out_name = self.gen_out_name()
                curr_block.output_var_name = out_name
                forward_code = '\t\t' + Translator.block_to_calling(curr_block, out_name)
                forward_codes.append(forward_code)
                if len(curr_block.output) > 0:
                    for next_block in curr_block.output:
                        if next_block not in block_to_deal:
                            block_to_deal.append(next_block)
                else:
                    end_blocks.append(curr_block)

        return_stat = "\t\treturn (" + ", ".join([end_block.output_var_name for end_block in end_blocks]) + ")"
        forward_codes.append(return_stat)
        self.template_code = self.template_code.replace(self.template_code_forw_replace, "\n".join(forward_codes))

    def gen_out_name(self):
        self.out_index += 1
        return "out" + str(self.out_index)

    def gen_var_name(self, block: Block):
        self.var_index += 1
        return "self." + block.name.lower() + "_var_" + str(self.var_index)

    # 下面的两个东西只有一个变量不同，是因为阶段不同
    # 仔细想想逻辑
    @staticmethod
    def check_input(block: Block):
        for i in range(len(block.input)):
            if block.input[i].declared_var_name is None:
                return False
        return True

    @staticmethod
    def check_input_2(block: Block):
        for i in range(len(block.input)):
            if block.input[i].output_var_name is None:
                return False
        return True

    @staticmethod
    def block_to_var_declaration(block, out_var_name):
        return PytorchBlockFactory.new_instance(block.name, block).to_declare_code(out_var_name)

    @staticmethod
    def block_to_calling(block, out_forward_name):
        return PytorchBlockFactory.new_instance(block.name, block).to_forward_code(out_forward_name)