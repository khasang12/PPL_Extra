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
            d: integer = a + b; //3 [a,b,c]
            e: integer = a + c; //4 [c,a,d]
            f: integer = d + a; //5 [c,a,d]
            g: integer = d; //3 [c,a,d,f]
            e = c; //3 [c,a,d,f] 
            h: integer = a + d; //4 [c,a,d,f]
            i: integer = f + 1; //6 [c,h,f]
            j,l: integer = h,i; //4,6 [c,h,i] [c,i] 
            k: integer = c; //3 [c]
            h = h + k; //7 [k]
            printInteger(h); // [h,k]
        }"""
        expect = "7"
        self.assertTrue(TestCodeGen.test(input,expect,502))
    
