import argparse
import os
from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from CSharpLexer import CSharpLexer
from CSharpParser import CSharpParser

# Helper function to transform conditionals
def transform_conditionals(condition: str) -> str:
    transformed = condition.replace(">", "<=").replace("<", ">=").replace("==", "!=")
    return transformed

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Transform if statements in Java or C# code files.')
parser.add_argument('filename', type=str, help='path to the input code file')
args = parser.parse_args()

# Check that the file exists
if not os.path.exists(args.filename):
    print(f"Error: File '{args.filename}' not found.")
    exit()

# Determine the language based on file extension
file_extension = os.path.splitext(args.filename)[1]
if file_extension == ".java":
    lexer = JavaLexer(FileStream(args.filename))
    parser = JavaParser(CommonTokenStream(lexer))
    tree = parser.compilationUnit()
elif file_extension == ".cs":
    lexer = CSharpLexer(FileStream(args.filename))
    parser = CSharpParser(CommonTokenStream(lexer))
    tree = parser.compilation_unit()
else:
    print("Error: Unsupported file type.")
    exit()

# Traverse the abstract syntax tree and transform if statements
class IfTransformer(ParseTreeVisitor):
    def visitIfStatement(self, ctx):
        # Check if there is a relational operator in the condition
        condition = ctx.expression().getText()
        if ">" in condition or "<" in condition or "==" in condition:
            new_condition = transform_conditionals(condition)
            new_condition_expr = parser.parseExpression(new_condition)
            if ctx.getChildCount() == 5:
                # There is an "else" clause
                new_if = parser.ifStatement(new_condition_expr, ctx.statement(0), ctx.statement(1))
            else:
                new_if = parser.ifStatement(new_condition_expr, ctx.statement(0))
            return new_if
        else:
            return ctx

if_transformer = IfTransformer()
transformed_tree = if_transformer.visit(tree)

# Output the transformed code to a new file
output_filename = os.path.splitext(args.filename)[0] + "_transformed" + file_extension
with open(output_filename, "w") as f:
    f.write(transformed_tree.toStringTree(recog=parser))

print(f"Transformed code written to '{output_filename}'")