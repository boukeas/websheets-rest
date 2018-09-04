# docutil imports
import docutils.writers.html5_polyglot
from docutils import nodes, frontend, io, utils
# local imports
from directives import explanation, hint

# python2-compatible code in the html-translator uses this function
def unicode(v):
    return v


class Writer(docutils.writers.html5_polyglot.Writer):

    '''
    Standard docutils html5 writer with a custom html translator
    '''

    visitor_attributes = (docutils.writers.html5_polyglot.Writer.visitor_attributes[:2] +
                          ('scripts',) +
                          docutils.writers.html5_polyglot.Writer.visitor_attributes[2:])

    settings_spec = ('HTML-Specific Options', None,
                     docutils.writers.html5_polyglot.Writer.settings_spec[2] + (
                     ('Embed the script(s) in the output HTML file.',
                      ['--embed-script'],
                      {'default': 0,
                       'action': 'store_false',
                       'validator': frontend.validate_boolean}),
                     ('Link to the scripts(s) in the output HTML file. '
                      'This is the default.',
                      ['--link-script'],
                      {'dest': 'embed_script',
                       'action': 'store_true'}),
                     ('Comma separated list of script paths. '
                      'Relative paths are expanded if a matching file is found '
                      'in the --script-dirs. With --link-script, the path is '
                      'rewritten relative to the output HTML file. ',
                      ['--script-path'],
                      {'metavar': '<file[,file,...]>',
                       'validator': frontend.validate_comma_separated_list,
                       'default': ''}),
                     ('Comma-separated list of directories where scripts are found. '
                      'Used by --script-path when expanding relative path arguments. ',
                      ['--script-dirs'],
                      {'metavar': '<dir[,dir,...]>',
                       'validator': frontend.validate_comma_separated_list,
                       'default': ''}),
                     ))

    def __init__(self):
        super().__init__()
        self.translator_class = WebsheetHTMLTranslator


class WebsheetHTMLTranslator(docutils.writers.html5_polyglot.HTMLTranslator):

    head_prefix_template = ('<html lang="%(lang)s">\n<head>\n')
    content_type = ('<meta charset="%s">\n')
    generator = ('<meta name="generator" content="rst2websheets '
                 'based on docutils %s">\n')

    stylesheet_link = '<link rel="stylesheet" href="%s" type="text/css">\n'

    script_link = '<script type="text/javascript" src="%s"></script>\n'
    embedded_script = '<script type="text/javascript">\n%s\n</script>\n'

    def __init__(self, document):
        super().__init__(document)
        # Retrieve list of script references from the settings object
        scripts = document.settings.script_path or []
        if not isinstance(scripts, list):
            scripts = [path.strip() for path in scripts.split(',')]
        self.scripts = [self.script_call(path) for path in scripts]

    def script_call(self, path):
        """Return code to reference or embed script file `path`"""
        if self.settings.embed_script:
            try:
                content = io.FileInput(source_path=path, encoding='utf-8').read()
                self.settings.record_dependencies.add(path)
            except IOError as err:
                msg = "Cannot embed script '%s': %s." % (
                                path, err.strerror)
                self.document.reporter.error(msg)
                return '<--- %s --->\n' % msg
            return self.embedded_script % content
        # else link to script file:
        if self.settings.script_path:
            # adapt path relative to output
            path = utils.relative_path(self.settings._destination, path)
        return self.script_link % self.encode(path)

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

        # Removed "if ids" statement that handles element id or id's.
        # We don't want id's in the tags, we don't plan to format specific
        # elements using CSS

        # sorted used instead of original attlist.sort()
        attlist = sorted(atts.items())
        parts = [tagname]
        for name, value in attlist:
            # value=None is used for boolean attributes without value
            if value is None:
                parts.append('%s' % (name.lower()))
            elif isinstance(value, list):
                values = [v for v in value]
                parts.append('%s="%s"' % (name.lower(),
                                          self.attval(' '.join(values))))
            else:
                parts.append('%s="%s"' % (name.lower(),
                                          self.attval(value)))

        return ''.join(prefix) + '<%s>' % ' '.join(parts) + suffix

    # visitor methods (for new types of nodes or overriding for existing ones)

    def visit_admonition(self, node):
        """
        # this doesn't work, apparently, they are all admonitions
        # if isinstance(node, nodes.hint):
        if 'hint' in node['classes']:
            self.body.append(
                  self.starttag(node, 'details', ''))
            close_tag = '</details>\n'
        else:
            # default behaviour
        """
        node['classes'].insert(0, 'admonition')
        self.body.append(self.starttag(node, 'div'))
        # close_tag = '</div>\n'
        # self.context.append(close_tag)

    def depart_admonition(self, node=None):
        self.body.append('</div>\n')
        # self.body.append(self.context.pop())

    def visit_commentary(self, node):
        if 'orphan' in node:
            self.body.append(self.starttag(node, 'div',
                                           Class='commentary',
                                           Orphan=None))
        else:
            self.body.append(self.starttag(node, 'div',
                                           Class='commentary'))

    def depart_commentary(self, node):
        self.body.append('</div>\n')

    def visit_container(self, node):
        # overriden because default container class is "docutils container"
        self.body.append(self.starttag(node, 'div', CLASS='container'))

    def depart_container(self, node):
        self.body.append('</div>\n')

    def visit_explanation(self, node):
        if node.hasattr('open'):
            self.body.append(self.starttag(node, 'details',
                                           CLASS='explanation',
                                           OPEN=None))
        else:
            self.body.append(self.starttag(node, 'details',
                                           CLASS='explanation'))

    def depart_explanation(self, node):
        self.body.append('</details>\n')

    def visit_group(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='group'))

    def depart_group(self, node):
        self.body.append('</div>\n')

    def visit_hint(self, node):
        args = {'CLASS': 'hint'}
        if node.hasattr('open'): args['OPEN'] = None
        if node.hasattr('solution'): args['SOLUTION'] = None
        self.body.append(self.starttag(node, 'details', **args))

    def depart_hint(self, node):
        self.body.append('</details>\n')

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

    def visit_sidebar(self, node):
        self.body.append(self.starttag(node, 'aside'))

    def depart_sidebar(self, node):
        self.body.append('</aside>\n')

    def visit_title(self, node):
        """Only 6 section levels are supported by HTML."""
        check_id = 0  # TODO: is this a bool (False) or a counter?
        close_tag = '</p>\n'
        if isinstance(node.parent, explanation):
            self.body.append(self.starttag(node, 'summary', ''))
            close_tag = '</summary>\n'
        elif isinstance(node.parent, hint):
            self.body.append(self.starttag(node, 'summary', ''))
            close_tag = '</summary>\n'
        elif isinstance(node.parent, nodes.topic):
            self.body.append(
                  self.starttag(node, 'p', '', CLASS='topic-title'))
        elif isinstance(node.parent, nodes.sidebar):
            self.body.append(
                  self.starttag(node, 'p', '', CLASS='sidebar-title'))
        elif isinstance(node.parent, nodes.Admonition):
            self.body.append(
                self.starttag(node, 'p', '', CLASS='admonition-title'))
        elif isinstance(node.parent, nodes.table):
            self.body.append(
                  self.starttag(node, 'caption', ''))
            close_tag = '</caption>\n'
        elif isinstance(node.parent, nodes.document):
            self.body.append(self.starttag(node, 'h1', '', CLASS='title'))
            close_tag = '</h1>\n'
            self.in_document_title = len(self.body)
        else:
            assert isinstance(node.parent, nodes.section)
            h_level = self.section_level + self.initial_header_level - 1
            atts = {}
            if (len(node.parent) >= 2 and
                isinstance(node.parent[1], nodes.subtitle)):
                atts['CLASS'] = 'with-subtitle'
            self.body.append(
                  self.starttag(node, 'h%s' % h_level, '', **atts))
            atts = {}
            if node.hasattr('refid'):
                atts['class'] = 'toc-backref'
                atts['href'] = '#' + node['refid']
            if atts:
                self.body.append(self.starttag({}, 'a', '', **atts))
                close_tag = '</a></h%s>\n' % (h_level)
            else:
                close_tag = '</h%s>\n' % (h_level)
        self.context.append(close_tag)

    def depart_title(self, node):
        self.body.append(self.context.pop())
        if self.in_document_title:
            self.title = self.body[self.in_document_title:-1]
            self.in_document_title = 0
            self.body_pre_docinfo.extend(self.body)
            self.html_title.extend(self.body)
            del self.body[:]

    def visit_transition(self, node):
        self.body.append(self.emptytag(node, 'hr'))

    def depart_transition(self, node):
        pass
