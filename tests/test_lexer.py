from lexer import Lexer, TokenType
import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


class TestLexer(unittest.TestCase):
    def test_keywords(self):
        code = "program var begin end if then else while do read write integer real boolean and or not"
        lexer = Lexer(code)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token.type)

        expected = [
            TokenType.PROGRAM, TokenType.VAR, TokenType.BEGIN, TokenType.END,
            TokenType.IF, TokenType.THEN, TokenType.ELSE, TokenType.WHILE,
            TokenType.DO, TokenType.READ, TokenType.WRITE, TokenType.INTEGER,
            TokenType.REAL, TokenType.BOOLEAN, TokenType.AND, TokenType.OR, TokenType.NOT
        ]
        self.assertEqual(tokens, expected)

    def test_operators(self):
        code = "+ - * / := = <> < > <= >="
        lexer = Lexer(code)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token.type)

        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV,
            TokenType.ASSIGN, TokenType.EQ, TokenType.NEQ, TokenType.LT,
            TokenType.GT, TokenType.LTE, TokenType.GTE
        ]
        self.assertEqual(tokens, expected)

    def test_numbers(self):
        code = "123 45.67"
        lexer = Lexer(code)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append((token.type, token.value))

        expected = [
            (TokenType.NUMBER, 123),
            (TokenType.NUMBER, 45.67)
        ]
        self.assertEqual(tokens, expected)

    def test_identifiers(self):
        code = "x y123 total_sum _temp"
        lexer = Lexer(code)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append((token.type, token.value))

        expected = [
            (TokenType.ID, 'x'),
            (TokenType.ID, 'y123'),
            (TokenType.ID, 'total_sum'),
            (TokenType.ID, '_temp')
        ]
        self.assertEqual(tokens, expected)


if __name__ == '__main__':
    unittest.main()
