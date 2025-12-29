from ast_nodes import *


class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.code = []

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def generate(self, node):
        if isinstance(node, ProgramNode):
            self.generate_program(node)
        elif isinstance(node, AssignmentNode):
            return self.generate_assignment(node)
        elif isinstance(node, BinOpNode):
            return self.generate_binop(node)
        elif isinstance(node, UnaryOpNode):
            return self.generate_unary(node)
        elif isinstance(node, VarNode):
            return node.var_name
        elif isinstance(node, NumNode):
            temp = self.new_temp()
            self.code.append(f"{temp} := {node.value}")
            return temp
        elif isinstance(node, BooleanNode):
            temp = self.new_temp()
            self.code.append(f"{temp} := {1 if node.value else 0}")
            return temp
        elif isinstance(node, IfNode):
            self.generate_if(node)
        elif isinstance(node, WhileNode):
            self.generate_while(node)
        elif isinstance(node, ReadNode):
            self.generate_read(node)
        elif isinstance(node, WriteNode):
            self.generate_write(node)

        return self.code

    def generate_program(self, node):
        self.code.append(f"PROGRAM {node.name}")
        for stmt in node.statements:
            self.generate(stmt)
        self.code.append("END")

    def generate_assignment(self, node):
        target = node.var_name
        value_temp = self.generate(node.expression)
        self.code.append(f"{target} := {value_temp}")
        return target

    def generate_binop(self, node):
        left_temp = self.generate(node.left)
        right_temp = self.generate(node.right)
        result_temp = self.new_temp()

        op_map = {
            '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',
            '=': 'EQ', '<>': 'NE', '<': 'LT', '>': 'GT', '<=': 'LE', '>=': 'GE',
            'and': 'AND', 'or': 'OR'
        }

        op = op_map.get(node.op.value, node.op.value.upper())
        self.code.append(f"{result_temp} := {left_temp} {op} {right_temp}")
        return result_temp

    def generate_unary(self, node):
        expr_temp = self.generate(node.expr)
        result_temp = self.new_temp()

        if node.op.value == 'not':
            self.code.append(f"{result_temp} := NOT {expr_temp}")
        else:
            self.code.append(f"{result_temp} := {node.op.value} {expr_temp}")

        return result_temp

    def generate_if(self, node):
        condition_temp = self.generate(node.condition)
        false_label = self.new_label()
        end_label = self.new_label()

        self.code.append(f"IF_FALSE {condition_temp} GOTO {false_label}")

        for stmt in node.then_branch:
            self.generate(stmt)

        if node.else_branch:
            self.code.append(f"GOTO {end_label}")
            self.code.append(f"LABEL {false_label}")

            for stmt in node.else_branch:
                self.generate(stmt)

            self.code.append(f"LABEL {end_label}")
        else:
            self.code.append(f"LABEL {false_label}")

    def generate_while(self, node):
        start_label = self.new_label()
        end_label = self.new_label()

        self.code.append(f"LABEL {start_label}")
        condition_temp = self.generate(node.condition)
        self.code.append(f"IF_FALSE {condition_temp} GOTO {end_label}")

        for stmt in node.body:
            self.generate(stmt)

        self.code.append(f"GOTO {start_label}")
        self.code.append(f"LABEL {end_label}")

    def generate_read(self, node):
        self.code.append(f"READ {node.var_name}")

    def generate_write(self, node):
        value_temp = self.generate(node.expression)
        self.code.append(f"WRITE {value_temp}")

    def get_code(self):
        return self.code

    def print_code(self):
        for instruction in self.code:
            print(instruction)
