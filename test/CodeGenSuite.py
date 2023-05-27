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
        
    def test_cond_1(self):
        input = """main: function void () {
            a: integer = 1;
            if(a>1){
                printInteger(1);
            }
            else{
                printInteger(0);
            }
            if(a<1){
                printInteger(0);
            }
            else{
                printInteger(1);
            }
            if(a>=1){
                printInteger(1);
            }
            else{
                printInteger(0);
            }
            if(a<=1){
                printInteger(1);
            }
            else{
                printInteger(0);
            }
        }"""
        expect = "0111"
        self.assertTrue(TestCodeGen.test(input,expect,510))
    def test_cond_2(self):
        input = """main: function void () {
            a: integer = 1;
            if(a>1){
                printInteger(1);
            }
            printInteger(0);
        }"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,511))
    def test_cond_3(self):
        input = """main: function void () {
            a: integer = 1;
            if(a>0) printInteger(1);
            else printInteger(0);
        }"""
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,512)) 
    def test_cond_4(self):
        input = """main: function void () {
            a: integer = 1;
            if(a==0) printInteger(0);
            else printInteger(a);
        }"""
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,513))
    def test_cond_5(self):
        input = """main: function void () {
            a: integer = 1;
            if(a>0){
                if(a!=5) printInteger(6);
            }
        }"""
        expect = "6"
        self.assertTrue(TestCodeGen.test(input,expect,514)) 
    def test515_simple_while(self):
        input = """
        main:function void(){
            b: integer = 5;
            while(b>0){
                printInteger(b);
                b = b-1;
            }
            printInteger(b);
        }
        """
        expect = "543210"
        self.assertTrue(TestCodeGen.test(input,expect,515))
    def test516_while_inline(self):
        input = """
        main:function void(){
            b: integer = 5;
            while(b>0) b=b-1;
            printInteger(b);
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,516))
    def test517_nested_while(self):
        input = """
        main:function void(){
            b: integer = 5;
            while(b>0){
                i: integer = 2;
                while(i>0){
                    i = i-1;
                }
                b = b-1;
            }
            printInteger(b);
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,517))
    def test518_simple_dowhile(self):
        input = """
        main:function void(){
            b: integer = 5;
            do{
                printInteger(b);
                b = b-1;
            }while(b>0);
            printInteger(b);
        }
        """
        expect = "543210"
        self.assertTrue(TestCodeGen.test(input,expect,518))
    def test519_dowhile_inline(self):
        input = """
        main:function void(){
            b: integer = 0;
            do {b=b+1;} while(b<0);
            printInteger(b);
        }
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,519))
    def test520_nested_dowhile(self):
        input = """
        main:function void(){
            b: integer = 5;
            do{
                i:integer = 2;
                do{
                    i = i-1;
                } while(i>0);
                b = b-1;
            } while(b>0);
            printInteger(b);
        }
        """
        expect = "0"
        self.assertTrue(TestCodeGen.test(input,expect,520))
    def test521_simple_for(self):
        input = """
        main:function void(){
            b: integer;
            for(b=0,b<5,b+1){
                printInteger(b);
            }
            printInteger(b);
        }
        """
        expect = "012345"
        self.assertTrue(TestCodeGen.test(input,expect,521))
    def test522_for_inline(self):
        input = """
        b: integer;
        main:function void(){
            for(b=0,b<5,b+1) printInteger(b);
            printInteger(b);
        }
        """
        expect = "012345"
        self.assertTrue(TestCodeGen.test(input,expect,522))
    def test523_nested_while(self):
        input = """
        main:function void(){
            b: integer = 5;
            for(b=5,b>0,b-1){
                i:integer = 0;
                for(i=2,i>0,i-1){
                    i = i-1;
                }
                printInteger(b);
            }
            printInteger(b);
        }
        """
        expect = "543210"
        self.assertTrue(TestCodeGen.test(input,expect,523))
    def test524_continue1(self):
        input = """
        main:function void(){
            b: integer = 5;
            for(b=5,b>0,b-1){
                if(b>3) {
                    continue;
                }
                printInteger(b);
            }
        }
        """
        expect = "321"
        self.assertTrue(TestCodeGen.test(input,expect,524))
    def test525_continue2(self):
        input = """
        main:function void(){
            b: integer = 10;
            while(b<15){
                if(b>3){
                    b = b+1;
                    continue;
                }
                printInteger(b);
                b=b+1;
            }
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input,expect,525))
    def test526_continue3(self):
        input = """
        main:function void(){
            b: integer = 5;
            for(b=2,b>0,b-1){
                i:integer = 0;
                for(i=2,i>0,i-1){
                    if(b==i) continue;
                    else{
                        printInteger(i);
                        printInteger(b);
                    }
                }
            }
        }
        """
        expect = "1221"
        self.assertTrue(TestCodeGen.test(input,expect,526))
    def test527_break1(self):
        input = """
        main:function void(){
            b: integer = 5;
            for(b=5,b>0,b-1){
                if(b<2) {
                    break;
                }
                printInteger(b);
            }
        }
        """
        expect = "5432"
        self.assertTrue(TestCodeGen.test(input,expect,527))
    def test528_break2(self):
        input = """
        main:function void(){
            b: integer = 10;
            while(b<15){
                if(b>13)
                    if(b>14){
                        break;
                    }
                printInteger(b);
                b=b+1;
            }
        }
        """
        expect = "1011121314"
        self.assertTrue(TestCodeGen.test(input,expect,528))
    def test529_break3(self):
        input = """
        main:function void(){
            b: integer = 5;
            for(b=2,b>0,b-1){
                i:integer;
                for(i=2,i>0,i-1){
                    if(b!=i) break;
                    else{
                        printInteger(i);
                        printInteger(b);
                    }
                }
            }
        }
        """
        expect = "22"
        self.assertTrue(TestCodeGen.test(input,expect,529))
