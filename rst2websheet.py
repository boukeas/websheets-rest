import sys
import docutils.core
import docutils.parsers.rst
import docutils.writers.html5_polyglot

class Writer(docutils.writers.html5_polyglot.Writer):

    def __init__(self):
        self.parts = {}
        self.translator_class = WebsheetHTMLTranslator

class WebsheetHTMLTranslator(docutils.writers.html5_polyglot.HTMLTranslator):

    def visit_section(self, node):
        self.section_level += 1
        if self.section_level == 1:
            self.body.append(
                self.starttag(node, 'section', CLASS='unit'))
        elif self.section_level == 2:
            self.body.append(
                self.starttag(node, 'section', CLASS='step'))
        else: # this is where you can BAN deeper sections
            self.body.append(
                self.starttag(node, 'section'))

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append('</section>\n')


public = docutils.core.publish_file(
            source=open("answer.rst", 'r'),
            writer=Writer(),
            settings_overrides={
                #'generator': 'a generator',
                #'language-code': 'el',
                'initial_header_level': 2,
                #'embed-stylesheet': 0
            })


'''
public = docutils.core.publish_file(
            source=open("answer.rst", 'r'),
            parser=docutils.parsers.rst.Parser(),
            writer=docutils.writers.html5_polyglot.Writer(),
            settings_overrides={
                'generator': 'a generator',
                'language-code': 'el',
                'initial_header_level': 2,
                'embed-stylesheet': 0
            })
'''
