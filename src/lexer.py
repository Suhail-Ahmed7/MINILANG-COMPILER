import re


class TokenType:
    # Keywords
    PROGRAM = 'PROGRAM'
    VAR = 'VAR'
    BEGIN = 'BEGIN'
    END = 'END'
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    DO = 'DO'
    READ = 'READ'
    WRITE = 'WRITE'
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    BOOLEAN = 'BOOLEAN'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'

    # Identifiers and literals
    ID = 'ID'
    NUMBER = 'NUMBER'
    BOOLEAN_LIT = 'BOOLEAN_LIT'

    # Operators
    ASSIGN = 'ASSIGN'
    EQ = 'EQ'
    NEQ = 'NEQ'
    LT = 'LT'
    GT = 'GT'
    LTE = 'LTE'
    GTE = 'GTE'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULT = 'MULT'
    DIV = 'DIV'

    # Separators
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    SEMI = 'SEMI'
    COLON = 'COLON'
    COMMA = 'COMMA'
    DOT = 'DOT'

    # Special
    EOF = 'EOF'


class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if text else None

        # Token patterns
        self.keywords = {
            'program': TokenType.PROGRAM,
            'var': TokenType.VAR,
            'begin': TokenType.BEGIN,
            'end': TokenType.END,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'do': TokenType.DO,
            'read': TokenType.READ,
            'write': TokenType.WRITE,
            'integer': TokenType.INTEGER,
            'real': TokenType.REAL,
            'boolean': TokenType.BOOLEAN,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
            'true': TokenType.BOOLEAN_LIT,
            'false': TokenType.BOOLEAN_LIT
        }

    def error(self, message):
        raise Exception(
            f"Lexical error at line {self.line}, column {self.column}: {message}")

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0

        self.pos += 1
        self.column += 1

        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()  # Skip the newline

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(TokenType.NUMBER, float(result), self.line, self.column)
        else:
            return Token(TokenType.NUMBER, int(result), self.line, self.column)

    def identifier(self):
        result = ''
        while (self.current_char is not None and
               (self.current_char.isalnum() or self.current_char == '_')):
            result += self.current_char
            self.advance()

        token_type = self.keywords.get(result.lower(), TokenType.ID)
        return Token(token_type, result, self.line, self.column)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.skip_comment()
                continue

            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            # Numbers
            if self.current_char.isdigit():
                return self.number()

            # Operators and separators
            if self.current_char == ':':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.ASSIGN, ':=', self.line, self.column)
                return Token(TokenType.COLON, ':', self.line, self.column)

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE, '<=', self.line, self.column)
                elif self.current_char == '>':
                    self.advance()
                    return Token(TokenType.NEQ, '<>', self.line, self.column)
                return Token(TokenType.LT, '<', self.line, self.column)

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE, '>=', self.line, self.column)
                return Token(TokenType.GT, '>', self.line, self.column)

            # Single character tokens
            char = self.current_char
            token_types = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULT,
                '/': TokenType.DIV,
                '=': TokenType.EQ,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                ';': TokenType.SEMI,
                ',': TokenType.COMMA,
                '.': TokenType.DOT
            }

            if char in token_types:
                self.advance()
                return Token(token_types[char], char, self.line, self.column)

            self.error(f"Unexpected character: '{self.current_char}'")

        return Token(TokenType.EOF, None, self.line, self.column)
