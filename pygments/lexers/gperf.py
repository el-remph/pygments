"""
    pygments.lexers.gperf
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for gperf.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, DelegatingLexer, bygroups, default
from pygments.token import Keyword, Punctuation, Comment, Other, \
    Whitespace, Text, Operator, String
from pygments.lexers.c_cpp import CLexer, CFamilyLexer

__all__ = ['GperfLexer']

class GperfBase(RegexLexer):
    tokens = {
        'string': CFamilyLexer.tokens['string'],
        'space_sep': [
            (r'[ \f\r\v\t]+', Whitespace),
            (r'\n+', Whitespace, '#pop'),
            (r'\S+', Text)
        ],
        'definition': [
            (r'(=)(.*)', bygroups(Operator, Text), '#pop'),
            default(('#pop', 'space_sep'))
        ],
        'struct_def': [
            (r'\{', Other, '#push'),
            (r'\}\s*;?', Other, '#pop'),
            (r'[^{}]+', Other)
        ],
        'struct_decl': [
            (r';', Other, '#pop'), # simple forward declaration
            (r'{', Other, ('#pop', 'struct_def')) # definition
        ],
        'inline_c': [
            (r'%\}', Punctuation, '#pop'),
            (r'[^%}]+|[%}]', Other)
        ],
        'declarations': [
            (r'(?s)/\*.*?\*/', Comment),
            (r'\s+', Whitespace),
            (r'^(%)([A-Za-z_][-\w]*)', bygroups(Punctuation, Keyword), 'definition'),
            (r'\bstruct\s+\w+\s*', Other, 'struct_decl'),
            (r'%\{', Punctuation, 'inline_c'),
            (r'%%', Keyword, '#pop'),
            default('#pop')
        ],
        'keywords': [
            (r'#.*', Comment),
            (r'^"', String, 'string'),
            (r'^%%', Keyword, '#pop'),
            (r'^(\S+)(\s*?[,\n])', bygroups(String, Other)),
            (r'(?<!^).+|\n', Other)
        ],
        'root': [
            (r'(?s).+', Other)
        ]
    }

    # Set a default stack
    def get_tokens_unprocessed(self, text, stack=('root', 'keywords', 'declarations')):
        yield from RegexLexer.get_tokens_unprocessed(self, text, stack)

class GperfLexer(DelegatingLexer):
    name = 'gperf'
    aliases = ['gperf']
    filenames = ['*.gperf']
    url = 'https://gnu.org/s/gperf'
    version_added = '2.20'
    def __init__(self, **options):
        super().__init__(CLexer, GperfBase, **options)
