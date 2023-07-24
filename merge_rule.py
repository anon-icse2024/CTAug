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

    # Merging if statements if more than two
    if len(statements) > 2:
        merged_statement = "if ("
        for i, statement in enumerate(statements):
            if i > 0:
                merged_statement += " && "
            merged_statement += statement.getText()[3:-1] # Removing "if (" and ")" from statement
        merged_statement += ") {"

        # Replacing individual if statements with merged if statement
        code_lines = []
        with open(filename, 'r') as file:
            for line in file:
                for statement in statements:
                    if statement.getText() in line:
                        line = line.replace(statement.getText(), "")
                code_lines.append(line)
        code_lines.insert(listener.get_if_statement_index(), merged_statement)
        code_lines.append("}")
        new_filename = os.path.splitext(filename)[0] + "_modified" + ext
        with open(new_filename, 'w') as file:
            file.write(''.join(code_lines))
        print("Merged {} if statements in {}".format(len(statements), filename))
        print("Modified file saved as {}".format(new_filename))
    else:
        print("No need to merge if statements in {}".format(filename))

# Listener class to identify if statements
class IfStatementListener(ParseTreeListener):
    def __init__(self):
        self.if_statements = []
        self.if_statement_index = None

    def enterIfStatement(self, ctx):
        self.if_statements.append(ctx)
        if self.if_statement_index is None:
            self.if_statement_index = ctx.start.line - 1

    def get_if_statements(self):
        return self.if_statements

    def get_if_statement_index(self):
        return self.if_statement_index


# Parsing command line arguments
parser = ArgumentParser()
parser.add_argument("filename", help="name of the input code file")
args = parser.parse_args()

# Calling the parse_code function with the filename
parse_code(args.filename)
