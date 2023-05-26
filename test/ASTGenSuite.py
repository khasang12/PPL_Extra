import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    ''' def test_simple_program(self):
        """Simple program: int main() {} """
        input = """int main() {}"""
        expect = str(Program([FuncDecl("main",IntegerType(),[],None,BlockStmt([]))]))
        self.assertTrue(TestAST.test(input,expect,300))

    def test_more_complex_program(self):
        """More complex program"""
        input = """int main () {
            putIntLn(4);
        }"""
        expect = str(Program([FuncDecl("main",IntegerType(),[],None,BlockStmt([FuncCall("putIntLn",[IntegerLit(4)])]))]))
        self.assertTrue(TestAST.test(input,expect,301))
    
    def test_call_without_parameter(self):
        """More complex program"""
        input = """int main () {
            getIntLn();
        }"""
        expect = str(Program([FuncDecl("main",IntegerType(),[],None,BlockStmt([FuncCall("getIntLn",[])]))]))
        self.assertTrue(TestAST.test(input,expect,302))
    
    def test_more_complex_program(self):
        """More complex program"""
        input = """int main () {
            putIntLn(4+5);
        }"""
        expect = """Program([
	FuncDecl(main, IntegerType, [], None, BlockStmt([FuncCall(putIntLn, [BinExpr(+, IntegerLit(4), IntegerLit(5))])]))
])"""
        self.assertTrue(TestAST.test(input,expect,303))
    
    def test_with_init_1(self):
        """More complex program"""
        input = """int main () {
            a: int = 2;
            b: int = 3;
            putIntLn(a+b);
        }"""
        expect = """Program([
	FuncDecl(main, IntegerType, [], None, BlockStmt([VarDecl(a, IntegerType, IntegerLit(2)), VarDecl(b, IntegerType, IntegerLit(3)), FuncCall(putIntLn, [BinExpr(+, Id(a), Id(b))])]))
])"""
        self.assertTrue(TestAST.test(input,expect,304))

    def test_with_init_2(self):
        """More complex program"""
        input = """int main() {
            a: int = 2;
            putIntLn(2);
        }"""
        expect = """Program([
	FuncDecl(main, IntegerType, [], None, BlockStmt([VarDecl(a, int, IntegerLit(2)), FuncCall(putIntLn, [IntegerLit(2)])]))
])"""
        self.assertTrue(TestAST.test(input,expect,305))
    
    def test_with_init_2(self):
        """More complex program"""
        input = """int main() {
            a,b,c: int = 2,3,4;
            putIntLn(a+b+c);
        }"""
        expect = """Program([
	FuncDecl(main, IntegerType, [], None, BlockStmt([VarDecl(a, IntegerType, IntegerLit(2)), VarDecl(b, IntegerType, IntegerLit(3)), VarDecl(c, IntegerType, IntegerLit(4)), FuncCall(putIntLn, [BinExpr(+, BinExpr(+, Id(a), Id(b)), Id(c))])]))
])"""
        self.assertTrue(TestAST.test(input,expect,306))
    
    def test_with_init_3(self):
        """More complex program"""
        input = """int main() {
            a,b,c: int;
            putIntLn(a+b+c);
        }"""
        expect = """Program([
	FuncDecl(main, IntegerType, [], None, BlockStmt([VarDecl(a, IntegerType), VarDecl(b, IntegerType), VarDecl(c, IntegerType), FuncCall(putIntLn, [BinExpr(+, BinExpr(+, Id(a), Id(b)), Id(c))])]))
])"""
        self.assertTrue(TestAST.test(input,expect,307)) '''
    
    def test_with_init_4(self):
        """More complex program"""
        input = """main: function void() {
            a,b,c: integer;
            a = 1;
            b = a + b;
            c = a + c;
            printInteger(a+b+c);
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([VarDecl(a, IntegerType), VarDecl(b, IntegerType), VarDecl(c, IntegerType), AssignStmt(Id(a), IntegerLit(1)), AssignStmt(Id(b), BinExpr(+, Id(a), Id(b))), AssignStmt(Id(c), BinExpr(+, Id(a), Id(c))), CallStmt(printInteger, BinExpr(+, BinExpr(+, Id(a), Id(b)), Id(c)))]))
])"""
        self.assertTrue(TestAST.test(input,expect,308))
   