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

class Scope(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

class Description(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

class EllipsisTag(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)

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

class Text(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)
