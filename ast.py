class Token:
    def __init__(self, text: str, start_index: int, end_index: int):
        self.text        = text
        self.start_index = start_index
        self.end_index   = end_index
        self.children    = []

    def attach_child(self, child):
        self.children.append(child)

    def accept(self, visitor):
        return visitor.visit(self)

class CommitMsg(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)
        # self.TagLine = None
        # self.Body    = None
        # self.Footer  = None

class Scope(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

class Description(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

class EllipsisTag(Token):
    def __init__(self):
        pass

class Type(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

class BreakingChangeTag(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

class ScopeTag(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

class TagLine(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)
        # self.Type        = None
        # self.Description = None
        # self.Ellipsis    = None

class Text(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

# class AST:
#     def __init__(self, text: str, token: Token):
#         self.text = text
#         self.root = token
