import sys
import docutils.core
import docutils.parsers.rst
import docutils.writers.html5_polyglot

import sys
import os.path
import re
import urllib

import docutils
from docutils import nodes, utils, writers, languages, io
from docutils.utils.error_reporting import SafeString
from docutils.transforms import writer_aux

class Writer(docutils.writers.html5_polyglot.Writer):

    def __init__(self):
        self.parts = {}
        self.translator_class = WebsheetHTMLTranslator

class WebsheetHTMLTranslator(docutils.writers.html5_polyglot.HTMLTranslator):

    def stylesheet_call(self, path):
        """Return code to reference stylesheet file `path`"""

        # link to style file:
        if self.settings.stylesheet_path:
            # adapt path relative to output (cf. config.html#stylesheet-path)
            path = utils.relative_path(self.settings._destination, path)
        return self.stylesheet_link % self.encode(path)

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
                'embed-stylesheet': False,
                'initial_header_level': 2
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
