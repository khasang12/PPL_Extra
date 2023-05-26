from Utils import *
from Visitor import *

class IdentifierCollector(Visitor, Utils):
    def __init__(self):
        self.identifiers = [[]]
        
    def visitBinExpr(self, ast, param):
        self.visit(ast.left,param)
        self.visit(ast.right,param)

    def visitUnExpr(self, ast, param):
        self.visit(ast.val,param)
    
    def visitId(self, ast, param):
        self.identifiers[-1].append(ast.name)
    
    def visitAssignStmt(self, ast, param):
        self.identifiers += [[]]
        self.visit(ast.lhs,param)
        self.visit(ast.rhs,param)

    def visitBlockStmt(self, ast, param):
        for stmtdecl in ast.body:
            self.visit(stmtdecl,param)
            
    def visitVarDecl(self, ast, param):
        self.identifiers += [[ast.name]]
        if ast.init:
            self.visit(ast.init,param)

    def visitFuncDecl(self, ast, param):
        self.visit(ast.body,param)

    def visitProgram(self, ast, param):
        for stmtdecl in ast.decls:
            self.visit(stmtdecl,param)
        
    def visitFloatType(self, ast, param):
        pass
    
    def visitParamDecl(self, ast, param):
        pass
    
    def visitIntegerType(self, ast, param):
        pass
    
    def visitBooleanType(self, ast, param):
        pass

    def visitStringType(self, ast, param):
        pass
    
    def visitArrayType(self, ast, param):
        pass
    
    def visitAutoType(self, ast, param):
        pass
    
    def visitVoidType(self, ast, param):
        pass
    
    
    
    def visitArrayCell(self, ast, param):
        pass
    
    def visitIntegerLit(self, ast, param):
        pass

    def visitFloatLit(self, ast, param):
        pass
    
    def visitStringLit(self, ast, param):
        pass
    
    def visitBooleanLit(self, ast, param):
        pass
    
    def visitArrayLit(self, ast, param):
        pass
    
    def visitFuncCall(self, ast, param):
        pass
    
    

    def visitIfStmt(self, ast, param):
        pass
    
    def visitForStmt(self, ast, param):
        pass

    def visitWhileStmt(self, ast, param):
        pass

    def visitDoWhileStmt(self, ast, param):
        pass

    def visitBreakStmt(self, ast, param):
        pass

    def visitContinueStmt(self, ast, param):
        pass

    def visitReturnStmt(self, ast, param):
        pass

    def visitCallStmt(self, ast, param):
        pass

    