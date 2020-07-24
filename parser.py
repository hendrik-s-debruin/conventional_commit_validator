import ast
import re
import error

class Parser:
    """
    Parser Grammar
    --------------
    CommitMsg:         TagLine ['\n' Body] ['\n' Footer]
    TagLine:           Type ': ' Description [' ' Ellipsis]
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

    def parse(self) -> ast.Token:
        commit_msg = self.gobble_commit_msg(self.msg)
        return commit_msg

    def gobble_commit_msg(self, msg: str) -> ast.CommitMsg:
        start_index = self.msg_index
        tagline     = self.gobble_tagline()
        end_index   = self.msg_index
        commit_msg  = ast.CommitMsg(self.msg, start_index, end_index)
        # # TODO these two are optional
        # body    = self.gobble_body()
        # footer  = self.gobble_footer()

        commit_msg.attach_child(tagline)
        return commit_msg

    def gobble_tagline(self) -> ast.TagLine:
        start_index = self.msg_index
        type_       = self.gobble_type()
        self.gobble_string(': ')
        description = self.gobble_description()
        # TODO this one is optional
        # self.gobble_ellipsis()
        end_index = self.msg_index

        tagline = ast.TagLine(self.msg, start_index, end_index)

        tagline.attach_child(type_)
        tagline.attach_child(description)
        return tagline

    def gobble_type(self) -> ast.Type:
        start_index = self.msg_index
        word = self.gobble_word()
        # TODO these two are optional
        scope           = None
        breaking_change = None
        try:
            before_scope_index = self.msg_index
            scope = self.gobble_scope()
        except:
            self.rollback_index(before_scope_index)
            # print("has no scope")

        try:
            before_breaking_change_index = self.msg_index
            breaking_change = self.gobble_breaking_change_tag()
            # print("is breaking change")
        except:
            self.rollback_index(before_breaking_change_index)
            # print("is not breaking change")
            raise

        end_index = self.msg_index

        type_tag = ast.Type(self.msg, start_index, end_index)
        type_tag.attach_child(word)
        if scope is not None:
            type_tag.attach_child(scope)
        if breaking_change is not None:
            type_tag.attach_child(breaking_change)

        return type_tag

    # def gobble_ellipsis(self) -> ast.EllipsisTag:
    #     self.gobble_string("...")
    #     return ast.EllipsisTag()

    def gobble_breaking_change_tag(self) -> ast.BreakingChangeTag:
        start_index = self.msg_index
        self.gobble_string('!')
        end_index = self.msg_index

        return ast.BreakingChangeTag(self.msg, start_index, end_index)

    def gobble_scope(self) -> ast.ScopeTag:
        self.gobble_string('(')
        start_index = self.msg_index
        scope_name  = self.gobble_word()
        end_index   = self.msg_index
        self.gobble_string(')')

        scope = ast.Scope(self.msg, start_index, end_index)
        scope.attach_child(scope_name)

        return scope

    def gobble_description(self) -> ast.Description:
        start_index = self.msg_index
        text = self.gobble_sentence()
        end_index = self.msg_index
        description = ast.Description(self.msg, start_index, end_index)
        description.attach_child(text)

        return description

    def gobble_word(self) -> ast.Text:
        # TODO do not compile this on each invocation
        regex = re.compile("[a-zA-Z0-9]")
        start_index = self.msg_index
        gobbled = False
        while(regex.match(self.current())):
            gobbled = True
            self.gobble()
        if not gobbled:
            # TODO handle failure to gobble a word here
            print("did not gobble! THIS IS AN ERROR")
            pass
        end_index = self.msg_index
        text = ast.Text(self.msg, start_index, end_index)
        return text

    def gobble_sentence(self) -> ast.Text:
        # TODO do not compile this on each invocation
        regex = re.compile("[a-zA-Z0-9\s]+")
        start_index = self.msg_index
        gobbled = False
        while(regex.match(self.current())):
            gobbled = True
            self.gobble()
        if not gobbled:
            # TODO make this better
            raise RuntimeError("Could not gobble sentence")
            pass
        if(self.peek() == '.'):
            self.gobble()
        end_index = self.msg_index

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
                raise RuntimeError("Expected string: '" + string + "'")

    def gobble(self):
        # print("gobble: '" + self.msg[self.msg_index] + "'")
        self.msg_index = self.msg_index + 1

    def current(self):
        if self.msg_index >= len(self.msg):
            # print("reached EOF")
            return '~' # TODO something better -- EOF?
        return self.msg[self.msg_index]

    def peek(self):
        if self.msg_index >= len(self.msg):
            # print("reached EOF")
            return '~' # TODO something better -- EOF?
        return self.msg[self.msg_index + 1]

    def rollback_index(self, i):
        self.msg_index = i

