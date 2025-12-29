from parser import Parser
from lexer import Lexer
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


class TestParser(unittest.TestCase):
    def test_simple_program(self):
        code = """
program test;
var
  x: integer;
begin
  x := 10;
  write(x);
end.
"""
        lexer = Lexer(code)
        parser = Parser(lexer)

        # Should not raise an exception
        try:
            ast = parser.parse()
            self.assertIsNotNone(ast)
            self.assertEqual(ast.name, "test")
        except Exception as e:
            self.fail(f"Parser failed with error: {e}")

    def test_if_statement(self):
        code = """
program test;
var
  x: integer;
begin
  if x > 5 then
    write(x);
  end;
end.
"""
        lexer = Lexer(code)
        parser = Parser(lexer)

        try:
            ast = parser.parse()
            self.assertIsNotNone(ast)
        except Exception as e:
            self.fail(f"Parser failed with error: {e}")


if __name__ == '__main__':
    unittest.main()
