import sys
import docutils.core
import docutils.readers.standalone
import docutils.parsers.rst
import docutils.transforms
import docutils.writers.html5_polyglot
import docutils.frontend

filename = "answer.rst"
infile = open(filename, 'r')

components = (docutils.readers.standalone.Reader,
              docutils.parsers.rst.Parser,
              docutils.writers.html5_polyglot.Writer)

defaults = docutils.frontend.OptionParser(components).get_default_values()
print(defaults)

'''
public = docutils.core.publish_file(
            source=infile,
            destination=sys.stdout,
            reader=docutils.readers.standalone.Reader(),
            parser=docutils.parsers.rst.Parser(),
            writer=docutils.writers.html5_polyglot.Writer())
'''

'''
public = docutils.core.publish_file(
    source=infile,
    destination=sys.stdout,
    writer=docutils.writers.html5_polyglot.Writer(),
    settings_overrides={'traceback':True})
'''
