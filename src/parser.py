"""
MiniLang Parser
===============
Recursive descent parser for the MiniLang programming language.
Implements syntax analysis and builds Abstract Syntax Tree (AST).
"""

from lexer import Lexer, TokenType
from ast_nodes import *


class SymbolTable:
    """
    Symbol Table for variable declarations and type tracking.
    """

    def __init__(self):
        self.symbols = {}

    def declare(self, name, type_name):
        """Declare a new variable in the symbol table."""
        if name in self.symbols:
            raise Exception(
                f"Semantic error: Variable '{name}' already declared at line {self.current_token.line}")
        self.symbols[name] = {
            'type': type_name,
            'initialized': False,
            'line_declared': self.current_token.line
        }

    def is_declared(self, name):
        """Check if a variable is declared."""
        return name in self.symbols

    def get_type(self, name):
        """Get the type of a declared variable."""
        return self.symbols[name]['type'] if self.is_declared(name) else None

    def set_initialized(self, name):
        """Mark a variable as initialized (assigned)."""
        if self.is_declared(name):
            self.symbols[name]['initialized'] = True

    def get_all_symbols(self):
        """Get all declared symbols for debugging."""
        return self.symbols.copy()


class Parser:
    """
    Recursive Descent Parser for MiniLang.
    Transforms token stream into Abstract Syntax Tree (AST).
    """

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = SymbolTable()
        # Add reference to symbol table for error context
        self.symbol_table.current_token = self.current_token

    def error(self, message):
        """Raise a syntax error with current line context."""
        raise Exception(
            f"Syntax error at line {self.current_token.line}: {message}\n"
            f"Current token: {self.current_token}"
        )

    def eat(self, token_type):
        """
        Consume the current token if it matches the expected type.
        Otherwise, raise a syntax error.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            expected = token_type
            found = self.current_token.type
            line = self.current_token.line
            self.error(
                f"Expected '{expected}', but found '{found}' at line {line}")

    def peek(self, token_type):
        """Check if the next token matches the given type without consuming it."""
        return self.current_token.type == token_type

    def expect_in(self, expected_types, context=""):
        """Check if current token is one of the expected types."""
        if self.current_token.type not in expected_types:
            expected_str = "', '".join(expected_types)
            context_msg = f" in {context}" if context else ""
            self.error(f"Expected one of ['{expected_str}']{context_msg}")

    # ========================
    # PROGRAM STRUCTURE
    # ========================

    def program(self):
        """
        program : PROGRAM ID SEMI declarations BEGIN statements END DOT
        """
        self.eat(TokenType.PROGRAM)

        program_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.SEMI)

        # Parse declarations and statements
        declarations = self.declarations()
        self.eat(TokenType.BEGIN)
        statements = self.statements()
        self.eat(TokenType.END)
        self.eat(TokenType.DOT)

        # Verify we reached end of file
        if not self.peek(TokenType.EOF):
            self.error("Unexpected tokens after program end")

        return ProgramNode(program_name, declarations, statements)

    # ========================
    # DECLARATIONS
    # ========================

    def declarations(self):
        """
        declarations : VAR declaration_list | ε
        """
        declarations = []
        if self.peek(TokenType.VAR):
            self.eat(TokenType.VAR)
            declarations = self.declaration_list()
        return declarations

    def declaration_list(self):
        """
        declaration_list : declaration (SEMI declaration)*
        """
        declarations = [self.declaration()]

        while self.peek(TokenType.SEMI):
            self.eat(TokenType.SEMI)
            # Stop if we encounter BEGIN (end of declarations)
            if self.peek(TokenType.BEGIN):
                break
            declarations.append(self.declaration())

        return declarations

    def declaration(self):
        """
        declaration : id_list COLON type
        """
        ids = self.id_list()
        self.eat(TokenType.COLON)
        type_node = self.type()

        # Register all identifiers in symbol table
        for id_name in ids:
            self.symbol_table.declare(id_name, type_node.type_name)

        return DeclarationNode(ids, type_node)

    def id_list(self):
        """
        id_list : ID (COMMA ID)*
        """
        ids = [self.current_token.value]
        self.eat(TokenType.ID)

        while self.peek(TokenType.COMMA):
            self.eat(TokenType.COMMA)
            ids.append(self.current_token.value)
            self.eat(TokenType.ID)

        return ids

    def type(self):
        """
        type : INTEGER | REAL | BOOLEAN
        """
        self.expect_in([TokenType.INTEGER, TokenType.REAL, TokenType.BOOLEAN],
                       "type specification")

        if self.peek(TokenType.INTEGER):
            self.eat(TokenType.INTEGER)
            return TypeNode('integer')
        elif self.peek(TokenType.REAL):
            self.eat(TokenType.REAL)
            return TypeNode('real')
        elif self.peek(TokenType.BOOLEAN):
            self.eat(TokenType.BOOLEAN)
            return TypeNode('boolean')

    # ========================
    # STATEMENTS
    # ========================

    def statements(self, stop_tokens=None):
        """
        statements : statement (SEMI statement)*

        Args:
            stop_tokens: List of tokens that indicate end of statements
        """
        if stop_tokens is None:
            stop_tokens = [TokenType.END, TokenType.ELSE]

        statements = []

        while self.current_token.type not in stop_tokens + [TokenType.EOF]:
            statements.append(self.statement())

            # Handle semicolon as statement separator
            if self.peek(TokenType.SEMI):
                self.eat(TokenType.SEMI)
                # Check if next token is a stop token
                if self.current_token.type in stop_tokens:
                    break
            else:
                # No semicolon - stop unless it's a block structure
                if self.current_token.type in stop_tokens:
                    break

        return statements

    def statement(self):
        """
        statement : assignment | if_stmt | while_stmt | read_stmt | write_stmt
        """
        self.expect_in([
            TokenType.ID, TokenType.IF, TokenType.WHILE,
            TokenType.READ, TokenType.WRITE
        ], "statement")

        if self.peek(TokenType.ID):
            return self.assignment()
        elif self.peek(TokenType.IF):
            return self.if_stmt()
        elif self.peek(TokenType.WHILE):
            return self.while_stmt()
        elif self.peek(TokenType.READ):
            return self.read_stmt()
        elif self.peek(TokenType.WRITE):
            return self.write_stmt()

    def assignment(self):
        """
        assignment : ID ASSIGN expression
        """
        var_name = self.current_token.value
        line = self.current_token.line
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)

        expr = self.expression()

        # Semantic check: variable must be declared
        if not self.symbol_table.is_declared(var_name):
            raise Exception(
                f"Semantic error at line {line}: "
                f"Variable '{var_name}' not declared")

        # Mark variable as initialized
        self.symbol_table.set_initialized(var_name)

        return AssignmentNode(var_name, expr)

    # ========================
    # EXPRESSIONS (Operator Precedence)
    # ========================

    def expression(self):
        """
        expression : simple_expr (REL_OP simple_expr)?
        """
        left = self.simple_expr()
        return self.expression_rest(left)

    def expression_rest(self, left):
        """Handle relational operators."""
        rel_ops = [
            TokenType.EQ, TokenType.NEQ, TokenType.LT,
            TokenType.GT, TokenType.LTE, TokenType.GTE
        ]

        if self.current_token.type in rel_ops:
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.simple_expr()
            return BinOpNode(left, op, right)
        return left

    def simple_expr(self):
        """
        simple_expr : term (ADD_OP term)*
        """
        left = self.term()
        return self.simple_expr_rest(left)

    def simple_expr_rest(self, left):
        """Handle addition operators (+, -, OR)."""
        add_ops = [TokenType.PLUS, TokenType.MINUS, TokenType.OR]

        while self.current_token.type in add_ops:
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.term()
            left = BinOpNode(left, op, right)
        return left

    def term(self):
        """
        term : factor (MUL_OP factor)*
        """
        left = self.factor()
        return self.term_rest(left)

    def term_rest(self, left):
        """Handle multiplication operators (*, /, AND)."""
        mul_ops = [TokenType.MULT, TokenType.DIV, TokenType.AND]

        while self.current_token.type in mul_ops:
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.factor()
            left = BinOpNode(left, op, right)
        return left

    def factor(self):
        """
        factor : ID | NUMBER | LPAREN expression RPAREN | NOT factor | BOOLEAN_LIT
        """
        token = self.current_token

        if self.peek(TokenType.ID):
            # Variable reference
            var_name = token.value
            if not self.symbol_table.is_declared(var_name):
                raise Exception(
                    f"Semantic error at line {token.line}: "
                    f"Variable '{var_name}' not declared")
            self.eat(TokenType.ID)
            return VarNode(var_name)

        elif self.peek(TokenType.NUMBER):
            # Numeric literal
            value = token.value
            self.eat(TokenType.NUMBER)
            return NumNode(value)

        elif self.peek(TokenType.LPAREN):
            # Parenthesized expression
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        elif self.peek(TokenType.NOT):
            # Logical NOT
            self.eat(TokenType.NOT)
            node = self.factor()
            return UnaryOpNode(token, node)

        elif self.peek(TokenType.BOOLEAN_LIT):
            # Boolean literal
            value = token.value.lower() == 'true'
            self.eat(TokenType.BOOLEAN_LIT)
            return BooleanNode(value)

        else:
            self.error(
                f"Expected factor (identifier, number, or expression), "
                f"but found '{token.type}'"
            )

    # ========================
    # CONTROL STRUCTURES
    # ========================

    def block(self):
        """
        block : BEGIN statements END
        """
        self.eat(TokenType.BEGIN)
        statements = self.statements(stop_tokens=[TokenType.END])
        self.eat(TokenType.END)
        return statements

    def if_stmt(self):
        """
        if_stmt : IF expression THEN statement (ELSE statement)?
        """
        self.eat(TokenType.IF)
        condition = self.expression()
        self.eat(TokenType.THEN)

        # Parse then branch (single statement or block)
        if self.peek(TokenType.BEGIN):
            then_branch = self.block()
        else:
            then_branch = [self.statement()]

        # Parse else branch if present
        else_branch = []
        if self.peek(TokenType.ELSE):
            self.eat(TokenType.ELSE)
            if self.peek(TokenType.BEGIN):
                else_branch = self.block()
            else:
                else_branch = [self.statement()]

        return IfNode(condition, then_branch, else_branch)

    def while_stmt(self):
        """
        while_stmt : WHILE expression DO statement
        """
        self.eat(TokenType.WHILE)
        condition = self.expression()
        self.eat(TokenType.DO)

        # Parse loop body (single statement or block)
        if self.peek(TokenType.BEGIN):
            body = self.block()
        else:
            body = [self.statement()]

        return WhileNode(condition, body)

    # ========================
    # I/O STATEMENTS
    # ========================

    def read_stmt(self):
        """
        read_stmt : READ LPAREN ID RPAREN
        """
        self.eat(TokenType.READ)
        self.eat(TokenType.LPAREN)

        var_name = self.current_token.value
        line = self.current_token.line
        self.eat(TokenType.ID)
        self.eat(TokenType.RPAREN)

        # Semantic check
        if not self.symbol_table.is_declared(var_name):
            raise Exception(
                f"Semantic error at line {line}: "
                f"Variable '{var_name}' not declared")

        # Mark as initialized (read implies assignment)
        self.symbol_table.set_initialized(var_name)

        return ReadNode(var_name)

    def write_stmt(self):
        """
        write_stmt : WRITE LPAREN expression RPAREN
        """
        self.eat(TokenType.WRITE)
        self.eat(TokenType.LPAREN)
        expr = self.expression()
        self.eat(TokenType.RPAREN)
        return WriteNode(expr)

    # ========================
    # PARSER ENTRY POINT
    # ========================

    def parse(self):
        """
        Main parsing entry point.
        Returns the complete Program AST node.
        """
        try:
            ast = self.program()
            print("✓ Parsing completed successfully")
            print(
                f"✓ Symbol table: {len(self.symbol_table.get_all_symbols())} variables declared")
            return ast
        except Exception as e:
            # Add parsing context to error
            raise Exception(f"Parsing failed: {str(e)}")

    def get_symbol_table(self):
        """Get the symbol table for debugging/inspection."""
        return self.symbol_table
