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

# vas enregistrer une valeur sur le stack
# ne renvoit pas de code java, cette valeur de stack sera utilisée plus tard
@addToClass(AST.PushNode)
def compile(self):
	stack.append(self.child.execute())
	return ""

# affecte la valeur du stack à l'enfant
# correspond donc à une affectation basique en java étant effectué en deux étapes sur assembleur
@addToClass(AST.PopNode)
def compile(self):
	bytecode = ""
	vars[self.child.tok] = stack.pop()
	bytecode += "%s = %s\n" % (self.child.tok, vars[self.child.tok])
	return ""

# renvoi
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

# vas interpréter les différentes oppérations
# peut correspondre à une affectation ou une addition
@addToClass(AST.OpNode)
def compile(self):
	bytecode = ""
	bytecode += self.children[0].compile()
	if self.op == "mov":
		bytecode += " = "
		vars[self.children[0].tok] = self.children[1].execute()

	elif self.op == "add":
		bytecode += " += "
		vars[self.children[0].tok] += self.children[1].execute()

	elif self.op == "sub":
		bytecode += " -= "
		vars[self.children[0].tok] -= self.children[1].execute()

	bytecode += self.children[1].compile()
	bytecode += "\n"
	return bytecode

@addToClass(AST.IncNode)
def compile(self):
	bytecode = ""
	bytecode += self.child.compile()
	if self.op == "inc":
		bytecode += " ++ "
		vars[self.child.tok] = vars[self.child.tok] + 1

	elif self.op == "dec":
		bytecode += " -- "
		vars[self.child.tok] = vars[self.child.tok] - 1

	bytecode += "\n"
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