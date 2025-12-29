# src/ast_nodes.py
class ASTNode:
    pass


class ProgramNode(ASTNode):
    def __init__(self, name, declarations, statements):
        self.name = name
        self.declarations = declarations
        self.statements = statements

    def __str__(self):
        return f"Program({self.name})"


class DeclarationNode(ASTNode):
    def __init__(self, identifiers, type_node):
        self.identifiers = identifiers
        self.type_node = type_node

    def __str__(self):
        return f"Declaration({self.identifiers}: {self.type_node})"


class TypeNode(ASTNode):
    def __init__(self, type_name):
        self.type_name = type_name

    def __str__(self):
        return f"Type({self.type_name})"


class AssignmentNode(ASTNode):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

    def __str__(self):
        return f"Assignment({self.var_name} := {self.expression})"


class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp({self.left} {self.op.value} {self.right})"


class UnaryOpNode(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryOp({self.op.value} {self.expr})"


class VarNode(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name

    def __str__(self):
        return f"Var({self.var_name})"


class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Num({self.value})"


class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Boolean({self.value})"


class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __str__(self):
        return f"If({self.condition})"


class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"While({self.condition})"


class ReadNode(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name

    def __str__(self):
        return f"Read({self.var_name})"


class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return f"Block({len(self.statements)} statements)"


class WriteNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"Write({self.expression})"
