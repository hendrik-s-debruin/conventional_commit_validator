#!/usr/bin/env python
import re

class Token:
    def __init__(self, text: str, start_index: int, end_index: int):
        self.text        = text
        self.start_index = start_index
        self.end_index   = end_index

class CommitMsg(Token):
    def __init__(self, text: str, start_index: int, end_index: int):
        super().__init__(text, start_index, end_index)
        self.TagLine = None
        self.Body    = None
        self.Footer  = None

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
        self.Type        = None
        self.Description = None
        self.Ellipsis    = None

# class Word(Token):
#     def __init__(self, text: str, start_index: int, end_index: int):
#         super().__init__(text, start_index, end_index)

class AST:
    def __init__(self, text: str, token: Token):
        self.text = text
        self.root = Token

class Parser:
    """
    Parser Grammar
    --------------
    CommitMsg:         TagLine ['\n' Body] ['\n' Footer]
    TagLine:           Type ': ' Description [Ellipsis]
    Type:              Word [Scope] [BreakingChangeTag]
    Ellipsis:          '...'
    BreakingChangeTag: '!'
    Scope:             '(' Word ')'
    Description:       Sentence
    Word:              [a-zA-Z0-9]+
    Sentence:          (Word [::space::]+)+ '.'
    Body:              Paragraph+
    Paragraph:         Sentence+ '\n'
    Footer:            ([BreakingChange] Paragraph+)+
    BreakingChange:    'BREAKING CHANGE: '
    """

    def __init__(self, msg: str):
        self.msg       = msg
        self.msg_index = 0

    def parse(self) -> AST:
        commit_msg = self.gobble_commit_msg(self.msg)
        ast = AST(self.msg, commit_msg)
        return ast

    def gobble_commit_msg(self, msg: str) -> CommitMsg:
        start_index = self.msg_index
        tagline     = self.gobble_tagline()
        end_index   = self.msg_index - 1
        commit_msg  = CommitMsg(self.msg, start_index, end_index)
        # # TODO these two are optional
        # body    = self.gobble_body()
        # footer  = self.gobble_footer()
        return commit_msg

    def gobble_tagline(self) -> TagLine:
        start_index = self.msg_index
        type_ = self.gobble_type()
        self.gobble_string(': ')
        description = self.gobble_description()
        # TODO this one is optional
        self.gobble_ellipsis()
        end_index = self.msg_index - 1

        tagline = TagLine(self.msg, start_index, end_index)
        return tagline

    def gobble_type(self) -> Type:
        start_index = self.msg_index
        self.gobble_word()
        # TODO these two are optional
        # scope           = self.gobble_scope()
        # breaking_change = self.gobble_breaking_change_tag()
        end_index = self.msg_index - 1

        type_ = Type(self.msg, start_index, end_index)
        return type_

    def gobble_ellipsis(self) -> EllipsisTag:
        self.gobble_string("...")
        return EllipsisTag()

    def gobble_breaking_change_tag(self) -> BreakingChangeTag:
        self.gobble_string('!')
        return BreakingChangeTag()

    def gobble_scope(self) -> ScopeTag:
        self.gobble_string('(')
        start_index = self.msg_index
        scope_name  = self.gobble_word()
        end_index   = self.msg_index - 1
        self.gobble_string(')')

        scope = Scope(self.msg, start_index, end_index)

    def gobble_description(self) -> Description:
        start_index = self.msg_index
        self.gobble_sentence()
        end_index = self.msg_index - 1
        description = Description(self.msg, start_index, end_index)

        return description

    def gobble_word(self):
        # TODO do not compile this on each invocation
        regex = re.compile("[a-zA-Z0-9]")
        gobbled = False
        while(regex.match(self.current())):
            gobbled = True
            self.gobble()
        if not gobbled:
            # TODO handle failure to gobble a word here
            pass

    def gobble_sentence(self):
        # TODO do not compile this on each invocation
        regex = re.compile("[a-zA-Z0-9\s]+")
        gobbled = False
        while(regex.match(self.current())):
            gobbled = True
            self.gobble()
        if not gobbled:
            # TODO handle failure here
            pass


    # def gobble_body(self):
    #     pass

    # def gobble_paragraph(self):
    #     pass

    # def gobble_footer(self):
    #     pass

    # def gobble_breaking_change(self):
    #     pass

    def gobble_string(self, string: str):
        for i in range(len(string)):
            if string[i] == self.current():
                self.gobble()
            else:
                # TODO handle error
                pass

    def gobble(self):
        self.msg_index = self.msg_index + 1

    def current(self):
        return self.msg[self.msg_index]

    def peek(self):
        return self.msg[self.msg_index + 1]

def main():
    p = Parser("msg(AH):description")
    ast = p.parse()
    print(ast)
if __name__ == "__main__":
    main()
