import ast
import re
import error

def _parse(parse_func):
    """
    Decorator function to simplify some of the code

    The parse function should return a tuple, with two elements:

    * The class (not instance) of the tag to be created
    * a list of all the instance's children. A child may be 'None'

    Returns an instantiated tag
    """

    def inner(self):
        start_index         = self.msg_index
        (TagType, children) = parse_func(self)
        end_index           = self.msg_index
        tag = TagType(self.msg, start_index, end_index)
        for child in children:
            if child is not None:
                tag.attach_child(child)
        return tag

    return inner

class Parser:
    """
    Parser Grammar
    --------------
    CommitMsg:         TagLine ['\n' Body] ['\n' Footer]
    TagLine:           Type ': ' Description [Ellipsis]
    Type:              Word [Scope] [BreakingChangeTag]
    Ellipsis:          ' ...'
    BreakingChangeTag: '!'
    Scope:             '(' Word ')'
    Description:       Sentence
    Word:              '[a-zA-Z0-9]'+
    Sentence:          Word ['[::space::]' Word]+ '.'
    Body:              Paragraph+
    Paragraph:         Sentence+
    Footer:            ([BreakingChange] Paragraph+)+
    BreakingChange:    'BREAKING CHANGE: '
    """

    def __init__(self, msg: str):
        self.msg       = msg
        self.msg_index = 0

    def optional_parse(self, parse_fn):
        """
        Parses a component using the parse function 'parse_fn'. If the component
        is not present, rolls back the parser. Returns the parsed tag if it is
        present, else None
        """
        try:
            start_index = self.msg_index
            return parse_fn()
        except:
            self.rollback_index(start_index)
            return None

    def parse_zero_or_more(self, parse_fn):
        parsed_tags = []
        should_continue = True
        while should_continue:
            try:
                before_loop_index = self.msg_index
                parsed_tags.append(parse_fn())
            except:
                self.rollback_index(before_loop_index)
        return parsed_tags

    def parse_one_or_more(self, parse_fn):
        return [parse_fn() + self.parse_zero_or_more(parse_fn)]

    def parse(self) -> ast.Token:
        commit_msg = self.gobble_commit_msg()
        return commit_msg

    @_parse
    def gobble_commit_msg(self) -> ast.CommitMsg:
        tagline = self.gobble_tagline()
        body    = None #self.optional_parse(self.gobble_body)
        footer  = None #self.optional_parse(self.gobble_footer)
        return (ast.CommitMsg, [tagline, body, footer])

    @_parse
    def gobble_tagline(self) -> ast.TagLine:
        type_        = self.gobble_type()
        self.gobble_string(': ')
        description  = self.gobble_description()
        ellipsis_tag = self.optional_parse(self.gobble_ellipsis)
        return (ast.TagLine, [type_, description, ellipsis_tag])

    @_parse
    def gobble_type(self) -> ast.Type:
        word            = self.gobble_word()
        scope           = self.optional_parse(self.gobble_scope)
        breaking_change = self.optional_parse(self.gobble_breaking_change_tag)
        return (ast.Type, [word, scope, breaking_change])

    @_parse
    def gobble_ellipsis(self) -> ast.EllipsisTag:
        self.gobble_string(" ...")
        return (ast.EllipsisTag, [])

    @_parse
    def gobble_breaking_change_tag(self) -> ast.BreakingChangeTag:
        self.gobble_string('!')
        return (ast.BreakingChangeTag, [])

    @_parse
    def gobble_scope(self) -> ast.ScopeTag:
        self.gobble_string('(')
        scope_name  = self.gobble_word()
        self.gobble_string(')')
        return (ast.Scope, [scope_name])

    @_parse
    def gobble_description(self) -> ast.Description:
        text = self.gobble_sentence()
        return (ast.Description, [text])

    @_parse
    def gobble_word(self) -> ast.Text:
        regex = re.compile("[a-zA-Z0-9]") # TODO do not compile this on each invocation
        gobbled = False
        start_index = self.msg_index
        while(regex.match(self.current())):
            gobbled = True
            self.gobble()
        if not gobbled:
            raise error.ParseError("[::alphanumeric::]", start_index, self.msg)
        return (ast.Text, [])

    @_parse
    def gobble_sentence(self) -> ast.Text:
        self.gobble_word()
        should_continue = True
        while should_continue:
            try:
                begin_loop_index = self.msg_index
                self.gobble_string(" ")
                try:
                    self.gobble_word()
                except Exception as e:
                    print(e)
            except:
                self.rollback_index(begin_loop_index)
                should_continue = False
        self.gobble_string(".")

        return (ast.Text, [])

    @_parse
    def gobble_body(self):
        self.gobble_string("\n")
        self.parse_one_or_more(self.gobble_paragraph)
        return (ast.Text, [])

    @_parse
    def gobble_paragraph(self):
        self.parse_one_or_more(self.gobble_sentence)
        return (ast.Text, [])

    def gobble_footer(self):
        pass

    def gobble_breaking_change(self):
        pass

    def gobble_string(self, string: str):
        initial_index = self.msg_index
        for i in range(len(string)):
            if string[i] == self.current():
                self.gobble()
            else:
                raise error.ParseError(string, initial_index, self.msg)

    def gobble(self):
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
