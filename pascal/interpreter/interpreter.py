from .parser import Parser
from .ast import Number, BinOp, UnaryOp, AssignOp, Variable,StatementList, Statement,ComplexStatement, Empty

class NodeVisitor:
    def visit(self):
        pass

class Interpreter(NodeVisitor):
    def __init__(self):
        self.variables={}
        self._parser = Parser()

    def visit(self, node):
        if isinstance(node, Number):
            return self._visit_number(node)
        elif isinstance(node, BinOp):
            return self._visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self._visit_unary(node)
        elif isinstance(node, AssignOp):
            return self._visit_assign(node)
        elif isinstance(node, Statement):
            return self._visit_statement(node)
        elif isinstance(node, StatementList):
            return self._visit_statement_list(node)
        elif isinstance(node, ComplexStatement):
            return self._visit_complex_statement(node)
        elif isinstance(node, Variable):
            return self._visit_var(node)
        elif isinstance(node, Empty):
            return
        
    def _visit_unary(self, node:UnaryOp):
        match node.op.value:
            case "+":
                return +self.visit(node.expr)
            case "-":
                return -self.visit(node.expr)
            case _:
                raise RuntimeError("wrong unary operator")
    def _visit_number(self, node:Number)->float:
        return float(node.token.value)

    def _visit_binop(self, node:BinOp):
        match node.op.value:
            case "+":
                return self.visit(node.left)+self.visit(node.right)
            case "-":
                return self.visit(node.left)-self.visit(node.right)
            case "*":
                return self.visit(node.left)*self.visit(node.right)
            case "/":
                return self.visit(node.left)/self.visit(node.right)
            case _:
                raise RuntimeError("invalid operator")
    def _visit_var(self, node:Variable):
        if node.token.value in self.variables:
            return self.variables[node.token.value]
        else:
            raise SyntaxError(f"Unassigned variable '{node.token.value}'")
    def _visit_statement(self, node:Statement):
        self.visit(node.stat)
    def _visit_assign(self, node:AssignOp):
        self.variables[node.var.token.value]=self.visit(node.expr)
    def _visit_complex_statement(self, node:ComplexStatement):
        self.visit(node.statlist)
    def _visit_statement_list(self, node:StatementList):
        self.visit(node.stat)
        if node.statlist!=None:
            self.visit(node.statlist)


    def eval(self, code:str) ->float:
        tree=self._parser.eval(code)
        print(tree)
        a=self.visit(tree)
        return self.variables
