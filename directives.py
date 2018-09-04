# docutils imports
from docutils.parsers.rst import directives, Directive
from docutils import nodes
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
