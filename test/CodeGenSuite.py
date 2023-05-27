import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    def test_add_simple(self):
        """simple addition"""
        print("Test 500 - Simple Addition")
        input = """main: function void () {
            a,b,c: integer = 1,2,3;
            b = c; // [c]
            a = a + b; // [b]
            printInteger(a); // [a,b]
        }"""
        expect = "4"
        self.assertTrue(TestCodeGen.test(input,expect,500))
    def test_add_unused(self):
        """c is never used again -> no need to allocate"""
        print("Test 501 - Unused Variable Addition: c")
        input = """main: function void () {
            a,b,c: integer = 1,2,3;
            d: integer = 4; // [a,b]
            d = a + b; // [a,b]
            printInteger(d); // [a,b,d]
        }"""
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,501))
    def test_add_many_variables(self):
        """test num_vars(12) > num_regs(8)"""
        print("Test 502 - Mega Variable Addition")
        input = """main: function void () {
            a,b,c: integer = 1,2,3; // [] [a] [a,b]
            d: integer = a + b; //d=3 [a,b,c]
            e: integer = a + c; //e=4 [c,a,d]
            f: integer = d + a; //f=4 [c,a,d]
            g: integer = d; //g=3 [c,a,d,f]
            e = c; //e=3 [c,a,d,f] 
            h: integer = a + d; //h=4 [c,a,d,f]
            i: integer = f + 1; //i=5 [c,h,f]
            j,l: integer = h,i; //j=4,l=5 [c,h,i] [c,i] 
            k: integer = c; //k=3 [c]
            h = h + k; //h=7 [k]
            printInteger(h); // [h,k]
        }"""
        expect = "7"
        self.assertTrue(TestCodeGen.test(input,expect,502))
    def test_minus_simple(self):
        """simple addition"""
        input = """main: function void () {
            a,b: integer = 1,2;
            a = a-b;
            printInteger(a); // [a,b]
        }"""
        expect = "-1"
        self.assertTrue(TestCodeGen.test(input,expect,503))
    def test_multiply_simple(self):
        """simple addition"""
        input = """main: function void () {
            a,b: integer = 3,2;
            a = a*b;
            printInteger(a); // [a,b]
        }"""
        expect = "6"
        self.assertTrue(TestCodeGen.test(input,expect,504)) 
    def test_div_simple(self):
        """simple addition"""
        input = """main: function void () {
            a,b: integer = 6,2;
            a = a/b;
            printInteger(a); // [a,b]
        }"""
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,505))
    def test_mod_simple(self):
        """simple addition"""
        input = """main: function void () {
            a,b: integer = 6,2;
            a = a%b;
            printInteger(a); // [a,b]
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,505)) 
    def test_unary_int(self):
        """simple addition"""
        input = """main: function void () {
            a: integer = -6;
            a = -a;
            printInteger(a);
        }"""
        expect = "6"
        self.assertTrue(TestCodeGen.test(input,expect,506))
    def test_unary_bool(self):
        """simple addition"""
        input = """main: function void () {
            a: boolean = true;
            a = !a;
            printBoolean(a);
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,507)) 
    def test_binary_mixed_1(self):
        """simple addition"""
        input = """main: function void () {
            a,b: integer = 1,2;
            a = a+b;
            a = 1;
            b = a+1;
            a = 1+2;
            printInteger(a);
            printInteger(b);
        }"""
        expect = "32"
        self.assertTrue(TestCodeGen.test(input,expect,508))
    def test_binary_mixed_1(self):
        """simple addition"""
        input = """main: function void () {
            a,b: boolean = true, false;
            a = a && b;
            b = a || b;
            a = a && true;
            b = b || false;
            printBoolean(a);
            printBoolean(b);
        }"""
        expect = "00"
        self.assertTrue(TestCodeGen.test(input,expect,509))
