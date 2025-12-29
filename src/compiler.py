import sys
import os
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac import TACGenerator


class Compiler:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.semantic_analyzer = SemanticAnalyzer()
        self.tac_generator = TACGenerator()

    def compile(self, source_code):
        try:
            print("=== MiniLang Compiler ===")
            print("Source code:")
            print(source_code)
            print("\n" + "="*50)

            # Lexical Analysis
            print("\n1. LEXICAL ANALYSIS:")
            print("-" * 30)
            self.lexer = Lexer(source_code)
            tokens = []
            while True:
                token = self.lexer.get_next_token()
                tokens.append(token)
                print(token)
                if token.type == 'EOF':
                    break

            # Added: Print total tokens count
            print(f"Total tokens: {len(tokens)}")

            # Syntax Analysis
            print("\n2. SYNTAX ANALYSIS:")
            print("-" * 30)
            self.lexer = Lexer(source_code)  # Reset lexer
            self.parser = Parser(self.lexer)
            ast = self.parser.parse()
            print("✓ Parsing successful!")
            print(f"Program: {ast.name}")
            print(f"Declarations: {len(ast.declarations)}")
            print(f"Statements: {len(ast.statements)}")

            # Print AST details for debugging
            print("\nAST Details:")
            for i, decl in enumerate(ast.declarations):
                print(f"  Declaration {i+1}: {decl}")
            for i, stmt in enumerate(ast.statements):
                print(f"  Statement {i+1}: {stmt}")

            # Semantic Analysis
            print("\n3. SEMANTIC ANALYSIS:")
            print("-" * 30)
            self.semantic_analyzer.analyze(ast)
            print("✓ Semantic analysis successful!")
            print("✓ All variables properly declared")
            print("✓ Type checking passed")

            # Intermediate Code Generation
            print("\n4. INTERMEDIATE CODE GENERATION:")
            print("-" * 30)
            self.tac_generator = TACGenerator()  # Reset generator
            tac = self.tac_generator.generate(ast)
            print("Three-Address Code:")
            for instruction in self.tac_generator.get_code():
                print(f"  {instruction}")

            print("\n✓ Compilation completed successfully!")

        except Exception as e:
            print(f"\n❌ Compilation error: {e}")
            return False

        return True


def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source_file.ml>")
        print("Or using provided example:")

        # Use built-in example if no file provided
        example_code = """program example;
var
  x, y: integer;
  max: integer;
begin
  read(x);
  read(y);
  if x > y then
    max := x
  else
    max := y;
  write(max);
end."""

        compiler = Compiler()
        compiler.compile(example_code)
    else:
        filename = sys.argv[1]
        if not filename.endswith('.ml'):
            print("Error: Source file must have .ml extension")
            return

        source_code = read_file(filename)
        if source_code:
            compiler = Compiler()
            compiler.compile(source_code)


if __name__ == "__main__":
    main()
