import os
import sys
from argparse import ArgumentParser
from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from CSharpLexer import CSharpLexer
from CSharpParser import CSharpParser

def parse_code(filename):
    # Identifying language of code file
    ext = os.path.splitext(filename)[1]
    if ext == ".java":
        lexer = JavaLexer(FileStream(filename))
        stream = CommonTokenStream(lexer)
        parser = JavaParser(stream)
        tree = parser.compilationUnit()
    elif ext == ".cs":
        lexer = CSharpLexer(FileStream(filename))
        stream = CommonTokenStream(lexer)
        parser = CSharpParser(stream)
        tree = parser.compilation_unit()
    else:
        print("Unsupported file type")
        sys.exit()

    # Identifying all if statements
    listener = IfStatementListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    statements = listener.get_if_statements()

    # Splitting if statement conditions if it contains &&
    modified_statements = []
    for statement in statements:
        if "&&" in statement.getText():
            condition = statement.expression().getText()
            split_conditions = condition.split("&&")
            for i, split_condition in enumerate(split_conditions):
                split_condition = split_condition.strip()
                new_condition = "if (" + split_condition + ")"
                if i == 0:
                    new_condition += " {"
                else:
                    new_condition += " else {"
                modified_statement = statement.getText().replace(condition, split_condition)
                modified_statement = modified_statement.replace("if (", new_condition, 1)
                modified_statements.append(modified_statement)
        else:
            modified_statements.append(statement.getText())

    # Replacing individual if statements with modified if statements
    code_lines = []
    with open(filename, 'r') as file:
        for line in file:
            for statement in statements:
                if statement.getText() in line:
                    modified_statement = modified_statements.pop(0)
                    line = line.replace(statement.getText(), modified_statement)
            code_lines.append(line)

    new_filename = os.path.splitext(filename)[0] + "_modified" + ext
    with open(new_filename, 'w') as file:
        file.write(''.join(code_lines))
    print("Transformed code saved as {}".format(new_filename))


# Listener class to identify if statements
class IfStatementListener(ParseTreeListener):
    def __init__(self):
        self.if_statements = []

    def enterIfStatement(self, ctx):
        self.if_statements.append(ctx)

    def get_if_statements(self):
        return self.if_statements


# Parsing command line arguments
parser = ArgumentParser()
parser.add_argument("filename", help="name of the input code file")
args = parser.parse_args()

# Calling the parse_code function with the filename
parse_code(args.filename)
