import sys
from repl import Repl

interactive = len(sys.argv) == 1
script = None if len(sys.argv) == 1 else sys.argv[1]
repl = Repl(interactive)
repl.run(script)