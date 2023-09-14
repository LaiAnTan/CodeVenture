from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import *
from PIL import Image
import PIL.ImageOps
import os

code = []

with open(os.getcwd() + "/somerandompythoncode.py") as fd:
	for lines in fd:
		code.append(lines)
code = "".join(code)

print(highlight(code, PythonLexer(), ImageFormatter(line_number_separator=True), outfile="hehe.png"))

image = Image.open(os.getcwd() + "/hehe.png")
inverted_image = PIL.ImageOps.invert(image)
inverted_image.save("hehe-invert.png")