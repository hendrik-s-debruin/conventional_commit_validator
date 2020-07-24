# Finds the text inside a node
class Printer:
    def visit(self, token):
        return token.text[token.start_index : token.end_index]

# Pretty prints a node and its descendants
class PrettyPrinter:
    def __init__(self):
        self.visitor = Printer()

    def visit(self, token, indentation_level: int = 0):
        typename = str(token.__class__.__name__)
        content  = token.accept(self.visitor)
        print("\t" * indentation_level + typename + ": '" + content + "'")
        for child in token.children:
            if child is not None:
                self.visit(child, indentation_level + 1)

# Calls a visitor recursively on a node and its descendants
class Walker:
    def __init__(self, visitor):
        self.visitor = visitor

    def visit(self, token):
        token.accept(self.visitor)
        for child in token.children:
            if child is not None:
                self.visit(child)
