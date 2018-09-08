# docutils imports
from docutils.parsers.rst import directives, Directive
from docutils import nodes
from docutils.parsers.rst.roles import set_classes
# local imports
# language is currently hard-coded to greek
from languages import el as language

###

class commentary(nodes.container): pass

class Commentary(Directive):

    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'name': directives.unchanged,
                   'orphan': directives.flag}
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        try:
            if self.arguments:
                classes = directives.class_option(self.arguments[0])
            else:
                classes = []
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0]))
        node = commentary(text)
        node['classes'].extend(classes)
        self.add_name(node)
        if 'orphan' in self.options:
            node['orphan'] = '1'
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

directives.register_directive("commentary", Commentary)

###

class explanation(nodes.General, nodes.Element): pass

class Explanation(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged,
                   'open': directives.flag}
    has_content = True

    def run(self):
        self.assert_has_content()
        title_text = self.arguments[0]
        textnodes, messages = self.state.inline_text(title_text, self.lineno)
        titles = [nodes.title(title_text, '', *textnodes)]
        text = '\n'.join(self.content)
        node = explanation(text, *(titles + messages), **{'classes': ['explanation']})
        node['classes'] += self.options.get('class', [])
        if 'open' in self.options: node['open'] = 1
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

directives.register_directive("explanation", Explanation)

###

class hint(nodes.General, nodes.Element): pass

class Hint(Directive):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'name': directives.unchanged,
                   'open': directives.flag,
                   'solution': directives.flag}
    has_content = True

    node_class = hint

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = self.node_class(text, **self.options)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        if 'solution' in self.options:
            title_label = 'solution'
        else:
            title_label = 'hint'
        title = nodes.title('', language.labels[title_label])
        node.insert(0, title)
        return [node]

directives.register_directive("hint", Hint)

###

class code(nodes.literal_block): pass

class Code(Directive):
    # this is actually based on the ParsedLiteral directive
    # allowing us to process anonymous hyperlinks in the code (for commentary)

    # optional argument from original docutils Code directive
    # (refers to language option)
    optional_arguments = 1
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged}
                   # from original docutils Code directive
                   # 'number-lines': directives.unchanged # integer or None
    has_content = True

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        # following 3 if statements comes from original docutils Code directive
        if self.arguments:
            language = self.arguments[0]
        else:
            language = ''
        if language:
            classes.append(language)
        if 'classes' in self.options:
            classes.extend(self.options['classes'])
        #
        # TODO: check settings and (if required) setup Lexical Analyzer
        #       (from original docutils Code directive)
        #
        text = '\n'.join(self.content)
        text_nodes, messages = self.state.inline_text(text, self.lineno)
        node = code(text, '', *text_nodes, **self.options)
        node.line = self.content_offset + 1
        self.add_name(node)
        return [node] + messages

directives.register_directive("code", Code)


'''
class CodeBlock(Directive):
    """Parse and mark up content of a code block.

    Configuration setting: syntax_highlight
       Highlight Code content with Pygments?
       Possible values: ('long', 'short', 'none')

    """

    def run(self):
        self.assert_has_content()
        if self.arguments:
            language = self.arguments[0]
        else:
            language = ''
        set_classes(self.options)
        classes = ['code']
        if language:
            classes.append(language)
        if 'classes' in self.options:
            classes.extend(self.options['classes'])

        # set up lexical analyzer
        try:
            tokens = Lexer(u'\n'.join(self.content), language,
                           self.state.document.settings.syntax_highlight)
        except LexerError, error:
            raise self.warning(error)

        if 'number-lines' in self.options:
            # optional argument `startline`, defaults to 1
            try:
                startline = int(self.options['number-lines'] or 1)
            except ValueError:
                raise self.error(':number-lines: with non-integer start value')
            endline = startline + len(self.content)
            # add linenumber filter:
            tokens = NumberLines(tokens, startline, endline)

        node = nodes.literal_block('\n'.join(self.content), classes=classes)
        self.add_name(node)
        # if called from "include", set the source
        if 'source' in self.options:
            node.attributes['source'] = self.options['source']
        # analyze content and add nodes for every token
        for classes, value in tokens:
            # print (classes, value)
            if classes:
                node += nodes.inline(value, value, classes=classes)
            else:
                # insert as Text to decrease the verbosity of the output
                node += nodes.Text(value, value)

        return [node]
'''
