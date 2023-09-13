from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import *

code = 'print "Hello World"'
print(highlight(code, PythonLexer(), TerminalFormatter()))