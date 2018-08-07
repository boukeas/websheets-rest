# docutil imports
import docutils.parsers.rst
from docutils import nodes
# local import
from transforms import group_transform, test_transform
from directives import explanation, commentary


class Parser(docutils.parsers.rst.Parser):

    '''
    Standard docutils reStructuredText parser with
    additional transforms.
    '''

    def get_transforms(self):
        return super().get_transforms() + [
                group_transform(nodes.hint, 916),
                group_transform(nodes.topic, 917),
                group_transform(explanation, 918),
                group_transform(commentary, 919)]
