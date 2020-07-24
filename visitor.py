class Printer:
    def visit(self, token):
        # print(token.text[token.start_index : token.end_index])
        return token.text[token.start_index : token.end_index]

class Walker:
    def __init__(self):
        self.printer = Printer()

    def visit(self, token, indentation_level: int = 0):
        typename = str(token.__class__.__name__)
        content  = token.accept(self.printer)
        print("\t" * indentation_level + typename + ": '" + content + "'")
        for child in token.children:
            if child is not None:
                self.visit(child, indentation_level + 1)

