# coding=utf-8
import AST
from AST import addToClass

stack = []

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
	stack.append(self.child.compile())
	return ""

# affecte la valeur du stack à l'enfant
# correspond donc à une affectation basique en java étant effectué en deux étapes sur assembleur
@addToClass(AST.PopNode)
def compile(self):
	bytecode = ""
	popedValue = stack.pop()
	bytecode += "%s = %s" % (self.child.tok, popedValue)
	bytecode += ";\n"
	return bytecode

# renvoi
@addToClass(AST.TokenNode)
def compile(self):
	return "%s" % self.tok

# vas interpréter les différentes oppérations
# peut correspondre à une affectation ou une addition
@addToClass(AST.OpNode)
def compile(self):
	bytecode = ""
	bytecode += self.children[0].compile()
	if self.op == "mov":
		bytecode += " = "

	elif self.op == "add":
		bytecode += " += "

	elif self.op == "sub":
		bytecode += " -= "

	elif self.op == "imul":
		bytecode += " *= "

	bytecode += self.children[1].compile()
	bytecode += ";\n"
	return bytecode

# correspond aux opération d'incrémentation et décrémentation
@addToClass(AST.IncNode)
def compile(self):
	bytecode = ""
	bytecode += self.child.compile()
	if self.op == "inc":
		bytecode += " ++"

	elif self.op == "dec":
		bytecode += " --"

	elif self.op == "idiv":
		bytecode += " /= eax"

	bytecode += ";\n"
	return bytecode
	
if __name__ == "__main__":
	from parseur import parse
	import sys,os
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	print(ast)
	compiled = ast.compile()
	print("Compiled output:")
	print(compiled)
	name = os.path.splitext(sys.argv[1])[0]+'.java'
	outfile = open(name, 'w')
	outfile.write(compiled)
	outfile.close()
	print ("Wrote output to", name)