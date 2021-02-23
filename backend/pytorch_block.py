from block import Block


class PytorchBlockFactory:
    @staticmethod
    def new_instance(typename, block):
        return globals()[typename](block)


class PytorchBlock:
    """
    这是定义的接口Interface
    """
    def __init__(self, block: Block):
        self.src_block = block
        self.arg_keys = {}
        self.args = {}
        self.mapping_name = ""
        self.calling_name = ""

    # 在Model Init的时候，对该Block进行初始化时候应该返回的代码
    def to_declare_code(self, out_var_name):
        self.parse_args()
        ret = ""
        ret += out_var_name
        ret += " = "
        ret += self.mapping_name
        ret += "("
        for key, value in self.args.items():
            ret += key
            ret += "="
            ret += value
            ret += ", "
        if len(self.args.items()) != 0:
            ret = ret[0:-2]
        ret += ")"
        return ret

    # 在 Model进行forward的时候，根据input和output应该产生的代码
    def to_forward_code(self, out_forward_name):
        calling_name = ""
        if self.calling_name:
            calling_name = self.calling_name
        else:
            calling_name = self.src_block.declared_var_name

        self.parse_args()
        ret = ""
        ret += out_forward_name
        ret += " = "
        ret += calling_name
        ret += "("
        ret += ", ".join([in_block.output_var_name for in_block in self.src_block.input])
        ret += ")"
        return ret

    def parse_args(self):
        for key in self.arg_keys:
            for di in self.src_block.data:
                if di['key'] == key:
                    self.args[key] = di['value']

# 占位
class EmptyBlock(PytorchBlock):
    def to_declare_code(self, out_var_name):
        return ""

# Input模块就是Identity，什么也不做
class Input(PytorchBlock):
    def __init__(self, block: Block):
        super().__init__(block)
        self.mapping_name = "torch.nn.Identity"


class Conv2D(PytorchBlock):
    def __init__(self, block: Block):
        super().__init__(block)
        self.mapping_name = "torch.nn.Conv2D"
        self.arg_keys = ["in_channels", "out_channels", "kernel_size", "stride", "padding"]


class MaxPooling2D(PytorchBlock):
    def __init__(self, block: Block):
        super().__init__(block)
        self.mapping_name = "torch.nn.MaxPool2d"
        self.arg_keys = ["kernel_size"]


class ReLU(PytorchBlock):
    def __init__(self, block: Block):
        super().__init__(block)
        self.mapping_name = "torch.nn.ReLU"
        self.arg_keys = []


class Linear(PytorchBlock):
    def __init__(self, block: Block):
        super().__init__(block)
        self.mapping_name = "torch.nn.Linear"
        self.arg_keys = ["in_features", "out_features"]


class Softmax(PytorchBlock):
    def __init__(self, block: Block):
        super().__init__(block)
        self.mapping_name = "torch.nn.Softmax2d"
        self.arg_keys = []


# Concat申明的时候没有结果
# 调用的时候通过torch.stack进行调用
class Concatenation(PytorchBlock):
    def __init__(self, block: Block):
        super().__init__(block)
        self.mapping_name = "torch.stack"
        self.calling_name = "torch.stack"
        self.arg_keys = ["dim"]

    def parse_args(self):
        super(Concatenation, self).parse_args()
        tensor_arg = "(" + ', '.join([in_block.output_var_name for in_block in self.src_block.input]) + ')'
        self.args['tensors'] = tensor_arg

    def to_declare_code(self, out_var_name):
        return ""


#
# class ResInception(PytorchBlock):
#     def __init__(self, block: Block, output_name):
#         super().__init__(block, output_name)
#         self.mapping_name = "torch.nn.Conv2D"
#         self.arg_keys = ["in_channels", "out_channels", "kernel_size", "stride", "padding"]

