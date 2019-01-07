# coding=utf-8
import AST
from AST import addToClass

vars = {}
stack = []

def whilecounter():
	whilecounter.current += 1
	return whilecounter.current
whilecounter.current = 0

# noeud de programme
# retourne la suite d'opcodes de tous les enfants
@addToClass(AST.ProgramNode)
def compile(self):
	bytecode = ""
	for c in self.children:
		bytecode += c.compile()
	return bytecode

@addToClass(AST.PushNode)
def compile(self):
	stack.append(self.child.execute())
	return ""

@addToClass(AST.PopNode)
def compile(self):
	bytecode = ""
	vars[self.child.tok] = stack.pop()
	bytecode += "%s = %s\n" % (self.child.tok, vars[self.child.tok])
	return ""

@addToClass(AST.TokenNode)
def compile(self):
	return "%s" % self.tok

@addToClass(AST.TokenNode)
def execute(self):
	if isinstance(self.tok, str):
		if self.tok in vars:
			return vars[self.tok]
		else:
			vars[self.tok] = 0
			return 0
	return self.tok

@addToClass(AST.OpNode)
def compile(self):
	bytecode = ""
	if self.op == "mov":
		bytecode += self.children[0].compile()
		bytecode += " = "
		bytecode += self.children[1].compile()
		bytecode += "\n"
		vars[self.children[0].tok] = self.children[1].execute()
	return bytecode
	
if __name__ == "__main__":
	from parser1 import parse
	import sys,os
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	print(ast)
	compiled = ast.compile()
	print(compiled)
	name = os.path.splitext(sys.argv[1])[0]+'.vm'
	outfile = open(name, 'w')
	outfile.write(compiled)
	outfile.close()
	print ("Wrote output to", name)