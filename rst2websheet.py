# docutils import
import docutils.core
# local imports
from parser import Parser
from writer import Writer
from languages import el as language

# language is hard-coded to greek
# TODO: determine language via settings
language_tag = 'el'
output_language_module = language
docutils.languages._languages[language_tag] = output_language_module


public = docutils.core.publish_file(
            source=open("answer.rst", 'r'),
            parser=Parser(),
            writer=Writer(),
            settings_overrides={
                'language_code': language_tag,
                'embed_stylesheet': False,
                'stylesheet_path': 'css/websheets.css, css/fonts.css',
                # 'script_path': 'js/websheets.js',
                'template': './template.txt',
                'initial_header_level': 2,
                'dump_settings': 0,
                'dump_transforms': 0
            })
