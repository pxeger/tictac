from sys import argv

from tictac.parser import parse
from tictac.interpreter import Interpreter

code = argv[1]
link = parse(code)
interpreter = Interpreter(link)
inputs = (eval(i) for i in argv[2:])
out = interpreter.run(*inputs)
print(*out, sep="\n")
