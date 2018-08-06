# docutils imports
from docutils.parsers.rst import directives, Directive
from docutils import nodes

class explanation(nodes.container): pass

class Explanation(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged}
    has_content = True

    node_class = explanation

    def run(self):
        self.assert_has_content()
        title_text = self.arguments[0]
        textnodes, messages = self.state.inline_text(title_text, self.lineno)
        titles = [nodes.title(title_text, '', *textnodes)]
        text = '\n'.join(self.content)
        node = self.node_class(text, *(titles + messages), **{'classes': ['explanation']})
        node['classes'] += self.options.get('class', [])

        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

directives.register_directive("explanation", Explanation)
