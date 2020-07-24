import ast

class ParseError(RuntimeError):
    def __init__(self, expected: str, at: int, msg: str):
        self.expected = expected.replace("\n", "\\n")
        self.index    = at
        self.msg      = msg

    def __str__(self):
        # return "Received: '" + self.msg[self.index] + "' Expected: '" + self.expected + "' while parsing: " + self.msg[0: self.index]
        return "Expected: '" + self.expected + "' while parsing: '" + self.msg[0: self.index] + "'"

class ContextParseError(RuntimeError):
    def __init__(self, parse_error: ParseError, token: ast.Token):
        self.parse_error = parse_error
        self.token = token

    def __str__(self):
        return self.token.__class__.__name__ + " " + str(self.parse_error)
