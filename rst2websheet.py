import sys
import docutils.core
import docutils.parsers.rst
import docutils.writers.html5_polyglot

# import sys
# import os.path
# import re
# import urllib

# import docutils
from docutils import nodes, utils, writers, languages, io
# from docutils.utils.error_reporting import SafeString
# from docutils.transforms import writer_aux

def unicode(v):
    return v

class Writer(docutils.writers.html5_polyglot.Writer):

    def __init__(self):
        self.parts = {}
        self.translator_class = WebsheetHTMLTranslator

    """
    # use this if you want to check settings and overrides
    def translate(self):
        print(self.document.settings)
        exit()
    """


class WebsheetHTMLTranslator(docutils.writers.html5_polyglot.HTMLTranslator):

    head_prefix_template = ('<html lang="%(lang)s">\n<head>\n')
    content_type = ('<meta charset="%s">\n')
    generator = ('<meta name="generator" content="rst2websheets '
                 'based on docutils %s">\n')
    stylesheet_link = '<link rel="stylesheet" href="%s" type="text/css">\n'

    def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
        """
        Construct and return a start tag given a node (id & class attributes
        are extracted), tag name, and optional attributes.
        """
        tagname = tagname.lower()
        prefix = []
        atts = {}
        ids = []
        for (name, value) in attributes.items():
            atts[name.lower()] = value
        classes = []
        languages = []
        # unify class arguments and move language specification
        for cls in node.get('classes', []) + atts.pop('class', '').split() :
            if cls.startswith('language-'):
                languages.append(cls[9:])
            elif cls.strip() and cls not in classes:
                classes.append(cls)
        if languages:
            # attribute name is 'lang' in XHTML 1.0 but 'xml:lang' in 1.1
            atts[self.lang_attribute] = languages[0]
        if classes:
            atts['class'] = ' '.join(classes)
        assert 'id' not in atts
        ids.extend(node.get('ids', []))
        if 'ids' in atts:
            ids.extend(atts['ids'])
            del atts['ids']

        # Removed if statement
        # if ids:
        # We don't want id's in the tags, we don't plan to format specific
        # elements using CSS
        # TODO: have a setting that specifies whether or not id's will be used.
        if False:
            atts['id'] = ids[0]
            for id in ids[1:]:
                # Add empty "span" elements for additional IDs.  Note
                # that we cannot use empty "a" elements because there
                # may be targets inside of references, but nested "a"
                # elements aren't allowed in XHTML (even if they do
                # not all have a "href" attribute).
                if empty or isinstance(node,
                            (nodes.bullet_list, nodes.docinfo,
                             nodes.definition_list, nodes.enumerated_list,
                             nodes.field_list, nodes.option_list,
                             nodes.table)):
                    # Insert target right in front of element.
                    prefix.append('<span id="%s"></span>' % id)
                else:
                    # Non-empty tag.  Place the auxiliary <span> tag
                    # *inside* the element, as the first child.
                    suffix += '<span id="%s"></span>' % id

        # sorted used instead of original attlist.sort()
        attlist = sorted(atts.items())
        parts = [tagname]
        for name, value in attlist:
            # value=None was used for boolean attributes without
            # value, but this isn't supported by XHTML.
            assert value is not None
            if isinstance(value, list):
                values = [unicode(v) for v in value]
                parts.append('%s="%s"' % (name.lower(),
                                          self.attval(' '.join(values))))
            else:
                parts.append('%s="%s"' % (name.lower(),
                                          self.attval(unicode(value))))

        # empty tags need a closing / to be XHTML compatible
        # HTML5 does not require this, so I am removing the if statement
        # if empty:
        #     infix = ' /'
        # else:
        #     infix = ''
        # return ''.join(prefix) + '<%s%s>' % (' '.join(parts), infix) + suffix

        return ''.join(prefix) + '<%s>' % ' '.join(parts) + suffix

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

    def visit_container(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='container'))

    def depart_container(self, node):
        self.body.append('</div>\n')

    def visit_transition(self, node):
        self.body.append(self.emptytag(node, 'hr'))

    def depart_transition(self, node):
        pass

    def visit_sidebar(self, node):
        self.body.append(self.starttag(node, 'aside'))

    def depart_sidebar(self, node):
        self.body.append('</aside>\n')

    # inline literal
    def visit_literal(self, node):
        # special case: "code" role
        classes = node.get('classes', [])
        if 'code' in classes:
            # filter 'code' from class arguments
            node['classes'] = [cls for cls in classes if cls != 'code']
            self.body.append(self.starttag(node, 'code', ''))
            return
        self.body.append(
            self.starttag(node, 'span', '', CLASS='literal'))
        text = node.astext()
        # remove hard line breaks (except if in a parsed-literal block)
        if not isinstance(node.parent, nodes.literal_block):
            text = text.replace('\n', ' ')
        # Protect text like ``--an-option`` and the regular expression
        # ``[+]?(\d+(\.\d*)?|\.\d+)`` from bad line wrapping
        for token in self.words_and_spaces.findall(text):
            if token.strip() and self.in_word_wrap_point.search(token):
                self.body.append('<span class="pre">%s</span>'
                                    % self.encode(token))
            else:
                self.body.append(self.encode(token))
        self.body.append('</span>')
        # Content already processed:
        raise nodes.SkipNode

    def depart_literal(self, node):
        # skipped unless literal element is from "code" role:
        self.body.append('</code>')



public = docutils.core.publish_file(
            source=open("answer.rst", 'r'),
            # parser=docutils.parsers.rst.Parser(),
            # writer=docutils.writers.html5_polyglot.Writer())
            writer=Writer(),
            settings_overrides={
                'language_code': 'el',
                'embed_stylesheet': False,
                'initial_header_level': 2
            })
