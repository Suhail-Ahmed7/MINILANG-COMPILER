# src/semantic.py
from ast_nodes import *


class TypeChecker:
    @staticmethod
    def check_binary_operation(left_type, op, right_type):
        arithmetic_ops = ['+', '-', '*', '/']
        relational_ops = ['=', '<>', '<', '>', '<=', '>=']
        logical_ops = ['and', 'or']

        if op in arithmetic_ops:
            if left_type in ['integer', 'real'] and right_type in ['integer', 'real']:
                return 'real' if 'real' in [left_type, right_type] else 'integer'

        elif op in relational_ops:
            if left_type == right_type or (left_type in ['integer', 'real'] and right_type in ['integer', 'real']):
                return 'boolean'

        elif op in logical_ops:
            if left_type == 'boolean' and right_type == 'boolean':
                return 'boolean'

        raise Exception(
            f"Type error: Incompatible types {left_type} and {right_type} for operator {op}"
        )

    @staticmethod
    def check_unary_operation(op, expr_type):
        if op == 'not' and expr_type == 'boolean':
            return 'boolean'
        raise Exception(
            f"Type error: Operator '{op}' cannot be applied to type {expr_type}"
        )


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        if isinstance(node, ProgramNode):
            self.analyze_program(node)
        elif isinstance(node, AssignmentNode):
            self.analyze_assignment(node)
        elif isinstance(node, BinOpNode):
            return self.analyze_binop(node)
        elif isinstance(node, UnaryOpNode):
            return self.analyze_unaryop(node)
        elif isinstance(node, IfNode):
            self.analyze_if(node)
        elif isinstance(node, WhileNode):
            self.analyze_while(node)
        elif isinstance(node, ReadNode):
            if node.var_name not in self.symbol_table:
                raise Exception(
                    f"Semantic error: Variable '{node.var_name}' not declared"
                )
            return self.symbol_table[node.var_name]
        elif isinstance(node, WriteNode):
            self.analyze(node.expression)
        elif isinstance(node, VarNode):
            return self.analyze_var(node)
        elif isinstance(node, NumNode):
            return self.analyze_num(node)
        elif isinstance(node, BooleanNode):
            return self.analyze_boolean(node)
        else:
            raise Exception(
                f"Semantic error: Unknown node type {type(node).__name__}"
            )

    def analyze_program(self, node):
        # Analyze declarations
        for decl in node.declarations:
            self.analyze_declaration(decl)
        # Analyze statements
        for stmt in node.statements:
            self.analyze(stmt)

    def analyze_declaration(self, node):
        for identifier in node.identifiers:
            self.symbol_table[identifier] = node.type_node.type_name

    def analyze_assignment(self, node):
        if node.var_name not in self.symbol_table:
            raise Exception(
                f"Semantic error: Variable '{node.var_name}' not declared"
            )
        var_type = self.symbol_table[node.var_name]
        expr_type = self.analyze(node.expression)
        if var_type != expr_type and not (
            var_type in ['integer', 'real'] and expr_type in [
                'integer', 'real']
        ):
            raise Exception(
                f"Type error: Cannot assign {expr_type} to {var_type} variable '{node.var_name}'"
            )

    def analyze_binop(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        return TypeChecker.check_binary_operation(
            left_type, node.op.value, right_type
        )

    def analyze_unaryop(self, node):
        expr_type = self.analyze(node.expr)
        return TypeChecker.check_unary_operation(node.op.value, expr_type)

    # ✅ FIXED: supports single stmt, list, or BlockNode
    def _iter_statements(self, maybe):
        if maybe is None:
            return
        if isinstance(maybe, list):
            for s in maybe:
                yield s
            return
        if hasattr(maybe, "statements"):
            for s in maybe.statements:
                yield s
            return
        yield maybe  # single node

    def analyze_if(self, node):
        condition_type = self.analyze(node.condition)
        if condition_type != 'boolean':
            raise Exception(
                f"Type error: If condition must be boolean, got {condition_type}"
            )

        for stmt in self._iter_statements(node.then_branch):
            self.analyze(stmt)

        for stmt in self._iter_statements(node.else_branch):
            self.analyze(stmt)

    def analyze_while(self, node):
        condition_type = self.analyze(node.condition)
        if condition_type != 'boolean':
            raise Exception(
                f"Type error: While condition must be boolean, got {condition_type}"
            )

        for stmt in self._iter_statements(node.body):
            self.analyze(stmt)

    def analyze_var(self, node):
        if node.var_name not in self.symbol_table:
            raise Exception(
                f"Semantic error: Variable '{node.var_name}' not declared"
            )
        return self.symbol_table[node.var_name]

    def analyze_num(self, node):
        return "integer" if isinstance(node.value, int) else "real"

    def analyze_boolean(self, node):
        return "boolean"
