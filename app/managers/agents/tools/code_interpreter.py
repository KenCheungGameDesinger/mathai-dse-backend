from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()

code = '''
a = 2
b = 3
print(a)
print(b)
print(a + b)
'''
# result = python_repl.run(code)
code_runner_tool = Tool(
    name="python_code_runner",
    description="Must check steps using this toos. A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`. Useful to calulate math operations.",
    func=python_repl.run,
)
