class Block:
    def __init__(self, b_id, name, text, data):
        self.b_id = b_id
        self.name = name
        self.text = text
        self.data = data
        self.input = []
        self.output = []
        # 申明变量时使用的变量名 在 __init__函数中分配
        self.declared_var_name = None
        # 调用该Block得到的output的变量名，在forward函数中进行分配
        self.output_var_name = None


    def __str__(self):
        return 'block info: [b_id: {}, name: {}, text: {}, data: {}]'.format(self.b_id, self.name, self.text, self.data)
