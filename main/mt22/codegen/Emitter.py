from Utils import *
# from StaticCheck import *
# from StaticError import *
import CodeGenerator as cgen
from MachineCode import MIPSCode
from AST import *


class Emitter():
    def __init__(self, filename):
        self.filename = filename
        self.buff = list()
        self.mips = MIPSCode()

    def getMIPSType(self, inType):
        typeIn = type(inType)
        
        if typeIn is IntegerType:
            return "I"
        elif typeIn is FloatType:
            return "F"
        elif typeIn is BooleanType:
            return "Z"
        elif typeIn is StringType:
            return "Ljava/lang/String;"
        elif typeIn is VoidType:
            return "V"
        elif typeIn is ArrayType:
            return "[" + self.getJVMType(inType.typ)
        elif typeIn is cgen.MType:
            return "(" + "".join(list(map(lambda x: self.getJVMType(x) if type(x) is not tuple else self.getJVMType(x[0]), inType.partype))) + ")" + self.getJVMType(inType.rettype)
        elif typeIn is cgen.ClassType:
            return "L" + inType.cname + ";"

    def getFullType(self, inType):
        typeIn = type(inType)
        if typeIn is IntegerType:
            return "int"
        elif typeIn is BooleanType:
            return "boolean"
        elif typeIn is FloatType:
            return "float"
        elif typeIn is StringType:
            return "java/lang/String"
        elif typeIn is VoidType:
            return "void"
        elif typeIn is cgen.ClassType:
            return inType.cname

    def emitPUSHICONST(self, in_, frame):
        # in: Int or String
        # frame: Frame
        if frame:
            frame.push()
        if type(in_) is int:
            i = in_
            if i >= -1 and i <= 5:
                return self.mips.emitICONST(i)
            elif i >= -128 and i <= 127:
                return self.mips.emitBIPUSH(i)
            elif i >= -32768 and i <= 32767:
                return self.mips.emitSIPUSH(i)
        elif type(in_) is str:
            if in_ == "True":
                return self.emitPUSHICONST(1, frame)
            elif in_ == "False":
                return self.emitPUSHICONST(0, frame)
            else:
                return self.emitPUSHICONST(int(in_), frame)

    def emitPUSHFCONST(self, in_, frame):
        # in_: String
        # frame: Frame

        f = float(in_)
        frame.push()
        rst = "{0:.4f}".format(f)
        if rst == "0.0" or rst == "1.0" or rst == "2.0":
            return self.mips.emitFCONST(rst)
        else:
            return self.mips.emitLDC(in_)

    ''' 
    *    generate code to push a constant onto the operand stack.
    *    @param in the lexeme of the constant
    *    @param typ the type of the constant
    '''

    def emitPUSHCONST(self, in_, typ, frame):
        # in_: String
        # typ: Type
        # frame: Frame
        
        if type(typ) is IntegerType or type(typ) is BooleanType:
            return self.emitPUSHICONST(in_, frame)
        elif type(typ) is StringType:
            frame.push()
            return self.mips.emitLDC(in_)
        else:
            raise IllegalOperandException(in_)

    ##############################################################

    def emitALOAD(self, in_, frame):
        # in_: Type
        # frame: Frame
        # ..., arrayref, index, value -> ...

        frame.pop()
        if type(in_) is IntegerType:
            return self.mips.emitIALOAD()
        elif type(in_) is BooleanType:
            return self.mips.emitBALOAD()
        elif type(in_) is FloatType:
            return self.mips.emitFALOAD()
        # elif type(in_) is cgen.ArrayPointerType or type(in_) is cgen.ClassType or type(in_) is StringType:
        elif type(in_) is cgen.ClassType or type(in_) is StringType or type(in_) is ArrayType:
            return self.mips.emitAALOAD()
        else:
            raise IllegalOperandException(str(in_))

    def emitASTORE(self, in_, frame):
        # in_: Type
        # frame: Frame
        # ..., arrayref, index, value -> ...

        frame.pop()
        frame.pop()
        frame.pop()
        if type(in_) is IntegerType:
            return self.mips.emitIASTORE()
        elif type(in_) is BooleanType:
            return self.mips.emitBASTORE()
        elif type(in_) is FloatType:
            return self.mips.emitFASTORE()
        # elif type(in_) is cgen.ArrayPointerType or type(in_) is cgen.ClassType or type(in_) is StringType:
        elif type(in_) is cgen.ClassType or type(in_) is StringType or type(in_) is ArrayType:
            return self.mips.emitAASTORE()
        else:
            raise IllegalOperandException(str(in_))

    '''    generate the var directive for a local variable.
    *   @param in the index of the local variable.
    *   @param varName the name of the local variable.
    *   @param inType the type of the local variable.
    *   @param fromLabel the starting label of the scope where the variable is active.
    *   @param toLabel the ending label  of the scope where the variable is active.
    '''

    def emitVAR(self, in_, varName, inType, fromLabel, toLabel, frame, num):
        # in_: Int
        # varName: String
        # inType: Type
        # fromLabel: Int
        # toLabel: Int
        # frame: Frame
        return self.mips.emitVAR(in_, varName, "", fromLabel, toLabel, num)

    def emitREADVAR(self, name, inType, index, frame, num):
        # name: String
        # inType: Type
        # index: Int
        # frame: Frame
        # ... -> ..., value

        frame.push()
        if type(inType) is IntegerType or type(inType) is BooleanType:
            return self.mips.emitILOAD(index,num)
        elif type(inType) is FloatType:
            return self.mips.emitFLOAD(index,num)
        # elif type(inType) is cgen.ArrayPointerType or type(inType) is cgen.ClassType or type(inType) is StringType:
        elif type(inType) is cgen.ClassType or type(inType) is StringType or type(inType) is ArrayType:
            return self.mips.emitALOAD(index,num)
        else:
            raise IllegalOperandException(name)

    ''' generate the second instruction for array cell access
    *
    '''

    def emitREADVAR2(self, name, typ, frame):
        # name: String
        # typ: Type
        # frame: Frame
        # ... -> ..., value

        # frame.push()
        raise IllegalOperandException(name)

    '''
    *   generate code to pop a value on top of the operand stack and store it to a block-scoped variable.
    *   @param name the symbol entry of the variable.
    '''

    def emitWRITEVAR(self, name, inType, index, frame, num):
        # name: String
        # inType: Type
        # index: Int
        # frame: Frame
        # ..., value -> ...

        #frame.pop()

        if type(inType) is IntegerType or type(inType) is BooleanType:
            return self.mips.emitISTORE(index, num)
        elif type(inType) is FloatType:
            return self.mips.emitFSTORE(index, num)
        # elif type(inType) is cgen.ArrayPointerType or type(inType) is cgen.ClassType or type(inType) is StringType:
        elif type(inType) is cgen.ClassType or type(inType) is StringType or type(inType) is ArrayType:
            return self.mips.emitASTORE(index, num)
        else:
            raise IllegalOperandException(name)

    ''' generate the second instruction for array cell access
    *
    '''

    def emitWRITEVAR2(self, name, typ, frame):
        # name: String
        # typ: Type
        # frame: Frame
        # ..., value -> ...

        # frame.push()
        raise IllegalOperandException(name)

    ''' generate the field (static) directive for a class mutable or immutable attribute.
    *   @param lexeme the name of the attribute.
    *   @param in the type of the attribute.
    *   @param isFinal true in case of constant; false otherwise
    '''

    def emitATTRIBUTE(self, lexeme, in_, isFinal, value):
        # lexeme: String
        # in_: Type
        # isFinal: Boolean
        # value: String

        return self.mips.emitSTATICFIELD(lexeme, self.getJVMType(in_), isFinal)

    def emitGETSTATIC(self, lexeme, in_, frame, num):
        # lexeme: String
        # in_: Type
        # frame: Frame

        frame.push()
        return self.mips.emitGETSTATIC(lexeme, self.getJVMType(in_))

    def emitPUTSTATIC(self, lexeme, in_, frame, num):
        # lexeme: String
        # in_: Type
        # frame: Frame
        if frame:
            frame.pop()
        return self.mips.emitPUTSTATIC(lexeme, self.getJVMType(in_))

    def emitGETFIELD(self, lexeme, in_, frame):
        # lexeme: String
        # in_: Type
        # frame: Frame

        return self.mips.emitGETFIELD(lexeme, self.getJVMType(in_))

    def emitPUTFIELD(self, lexeme, in_, frame):
        # lexeme: String
        # in_: Type
        # frame: Frame

        frame.pop()
        frame.pop()
        return self.mips.emitPUTFIELD(lexeme, self.getJVMType(in_))

    ''' generate code to invoke a static method
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name)
    *   @param in the type descriptor of the method.
    '''

    def emitINVOKESTATIC(self, lexeme, in_, frame,num):
        # lexeme: String
        # in_: Type
        # frame: Frame

        typ = in_
        #list(map(lambda x: frame.pop(), typ.partype))
        if not type(typ.rettype) is VoidType:
            frame.push()
        return self.mips.emitINVOKESTATIC(lexeme, "",num)

    ''' generate code to invoke a special method
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name)
    *   @param in the type descriptor of the method.
    '''

    def emitINVOKESPECIAL(self, frame, lexeme=None, in_=None):
        # lexeme: String
        # in_: Type
        # frame: Frame

        if not lexeme is None and not in_ is None:
            typ = in_
            list(map(lambda x: frame.pop(), typ.partype))
            frame.pop()
            if not type(typ.rettype) is VoidType:
                frame.push()
            return self.mips.emitINVOKESPECIAL(lexeme, self.getJVMType(in_))
        elif lexeme is None and in_ is None:
            frame.pop()
            return self.mips.emitINVOKESPECIAL()

    ''' generate code to invoke a virtual method
    * @param lexeme the qualified name of the method(i.e., class-name/method-name)
    * @param in the type descriptor of the method.
    '''

    def emitINVOKEVIRTUAL(self, lexeme, in_, frame):
        # lexeme: String
        # in_: Type
        # frame: Frame

        typ = in_
        list(map(lambda x: frame.pop(), typ.partype))
        frame.pop()
        if not type(typ) is VoidType:
            frame.push()
        return self.mips.emitINVOKEVIRTUAL(lexeme, self.getJVMType(in_))

    '''
    *   generate ineg, fneg.
    *   @param in the type of the operands.
    '''

    def emitNEGOP(self, in_, frame):
        # in_: Type
        # frame: Frame
        # ..., value -> ..., result

        if type(in_) is IntegerType:
            return self.mips.emitINEG()
        else:
            return self.mips.emitFNEG()

    def emitNOT(self, in_, frame):
        # in_: Type
        # frame: Frame

        return MIPSCode.INDENT + "xori"

    '''
    *   generate iadd, isub, fadd or fsub.
    *   @param lexeme the lexeme of the operator.
    *   @param in the type of the operands.
    '''

    def emitADDOP(self, lexeme, in_, frame):
        # lexeme: String
        # in_: Type
        # frame: Frame
        # ..., value1, value2 -> ..., result

        frame.pop()
        if type(in_) is cgen.MType: in_ = in_.rettype
        if lexeme == "+":
            if type(in_) is IntegerType:
                return self.mips.emitIADD()
            else:
                return self.mips.emitFADD()
        else:
            if type(in_) is IntegerType:
                return self.mips.emitISUB()
            else:
                return self.mips.emitFSUB()

    '''
    *   generate imul, idiv, fmul or fdiv.
    *   @param lexeme the lexeme of the operator.
    *   @param in the type of the operands.
    '''

    def emitMULOP(self, lexeme, in_, frame):
        # lexeme: String
        # in_: Type
        # frame: Frame
        # ..., value1, value2 -> ..., result

        frame.pop()
        if type(in_) is cgen.MType: in_ = in_.rettype
        if lexeme == "*":
            if type(in_) is IntegerType:
                return self.mips.emitIMUL()
            else:
                return self.mips.emitFMUL()
        else:
            if type(in_) is IntegerType:
                return self.mips.emitIDIV()
            else:
                return self.mips.emitFDIV()

    def emitDIV(self, frame):
        # frame: Frame

        frame.pop()
        return self.mips.emitIDIV()

    def emitMOD(self, frame):
        # frame: Frame

        frame.pop()
        return self.mips.emitIREM()

    '''
    *   generate iand
    '''

    def emitANDOP(self, frame):
        # frame: Frame

        frame.pop()
        return self.mips.emitIAND()

    '''
    *   generate ior
    '''

    def emitOROP(self, frame):
        # frame: Frame

        frame.pop()
        return self.mips.emitIOR()

    def emitREOP(self, op, in_, frame):
        # op: String
        # in_: Type
        # frame: Frame
        # ..., value1, value2 -> ..., result

        result = list()
        labelF = frame.getNewLabel()

        if op == ">":
            result.append(self.mips.emitBLEZ(labelF))
        elif op == ">=":
            result.append(self.mips.emitBLTZ(labelF))
        elif op == "<":
            result.append(self.mips.emitBGEZ(labelF))
        elif op == "<=":
            result.append(self.mips.emitBGTZ(labelF))
        elif op == "!=":
            result.append("\taddi $t1, $t0, 0\n")
        elif op == "==":
            result.append("\taddi $t1, $t0, 0\n")
        #result.append(self.emitPUSHCONST("1", IntegerType(), frame))
        #frame.pop()
        #result.append(self.emitGOTO(labelO, frame))
        #result.append(self.emitLABEL(labelF, frame))
        #result.append(self.emitPUSHCONST("0", IntegerType(), frame))
        #result.append(self.emitLABEL(labelO, frame))
        return ''.join(result)

    def emitRELOP(self, op, in_, trueLabel, falseLabel, frame):
        # op: String
        # in_: Type
        # trueLabel: Int
        # falseLabel: Int
        # frame: Frame
        # ..., value1, value2 -> ..., result

        result = list()

        frame.pop()
        frame.pop()
        if op == ">":
            result.append(self.mips.emitIFICMPLE(falseLabel))
            result.append(self.emitGOTO(trueLabel))
        elif op == ">=":
            result.append(self.mips.emitIFICMPLT(falseLabel))
        elif op == "<":
            result.append(self.mips.emitIFICMPGE(falseLabel))
        elif op == "<=":
            result.append(self.mips.emitIFICMPGT(falseLabel))
        elif op == "!=":
            result.append(self.mips.emitIFICMPEQ(falseLabel))
        elif op == "==":
            result.append(self.mips.emitIFICMPNE(falseLabel))
        result.append(self.mips.emitGOTO(trueLabel))
        return ''.join(result)

    '''   generate the method directive for a function.
    *   @param lexeme the qualified name of the method(i.e., class-name/method-name).
    *   @param in the type descriptor of the method.
    *   @param isStatic <code>true</code> if the method is static; <code>false</code> otherwise.
    '''

    def emitMETHOD(self, lexeme, in_, isStatic, frame):
        # lexeme: String
        # in_: Type
        # isStatic: Boolean
        # frame: Frame

        return self.mips.emitMETHOD(lexeme, isStatic)

    '''   generate the end directive for a function.
    '''

    def emitENDMETHOD(self, frame):
        # frame: Frame

        buffer = list()
        buffer.append(self.mips.emitLIMITSTACK(frame.getMaxOpStackSize()))
        buffer.append(self.mips.emitLIMITLOCAL(frame.getMaxIndex()))
        buffer.append(self.mips.emitENDMETHOD())
        return ''.join(buffer)

    def getConst(self, ast):
        # ast: Literal
        if type(ast) is IntLiteral:
            return (str(ast.value), IntegerType())

    '''   generate code to initialize a local array variable.<p>
    *   @param index the index of the local variable.
    *   @param in the type of the local array variable.
    '''

    '''   generate code to initialize local array variables.
    *   @param in the list of symbol entries corresponding to local array variable.    
    '''

    '''   generate code to jump to label if the value on top of operand stack is true.<p>
    *   ifgt label
    *   @param label the label where the execution continues if the value on top of stack is true.
    '''

    def emitIFTRUE(self, label, frame):
        # label: Int
        # frame: Frame

        frame.pop()
        return self.mips.emitIFGT(label)

    '''
    *   generate code to jump to label if the value on top of operand stack is false.<p>
    *   ifle label
    *   @param label the label where the execution continues if the value on top of stack is false.
    '''

    def emitIFFALSE(self, label, frame, op):
        # label: Int
        # frame: Frame

        #frame.pop()
        if op in [">=","<=","=="]:
            return self.mips.emitBNE(label)
        return self.mips.emitBEQ(label)

    def emitIFICMPGT(self, label, frame):
        # label: Int
        # frame: Frame

        frame.pop()
        return self.mips.emitIFICMPGT(label)

    def emitIFICMPLT(self, label, frame):
        # label: Int
        # frame: Frame

        frame.pop()
        return self.mips.emitIFICMPLT(label)

    '''   generate code to duplicate the value on the top of the operand stack.<p>
    *   Stack:<p>
    *   Before: ...,value1<p>
    *   After:  ...,value1,value1<p>
    '''

    def emitDUP(self, frame):
        # frame: Frame

        frame.push()
        return self.mips.emitDUP()
    
    def emitNOP(self, frame):
        # frame: Frame

        frame.push()
        return self.mips.emitNOP()

    def emitPOP(self, frame):
        # frame: Frame

        frame.pop()
        return self.mips.emitPOP()

    '''   generate code to exchange an integer on top of stack to a floating-point number.
    '''

    def emitI2F(self, frame):
        # frame: Frame

        return self.mips.emitI2F()

    ''' generate code to return.
    *   <ul>
    *   <li>ireturn if the type is IntegerType or BooleanType
    *   <li>freturn if the type is RealType
    *   <li>return if the type is null
    *   </ul>
    *   @param in the type of the returned expression.
    '''

    def emitRETURN(self, in_, frame):
        # in_: Type
        # frame: Frame
        if type(in_) is cgen.MType: in_ = in_.rettype
        if type(in_) is IntegerType or type(in_) is BooleanType:
            frame.pop()
            return self.mips.emitIRETURN()
        elif type(in_) is FloatType:
            frame.pop()
            return self.mips.emitFRETURN()
        elif type(in_) is VoidType:
            return self.mips.emitRETURN()
        else:
            return self.mips.emitARETURN()

    ''' generate code that represents a label	
    *   @param label the label
    *   @return code Label<label>:
    '''

    def emitLABEL(self, label, frame):
        # label: Int
        # frame: Frame

        return self.mips.emitLABEL(label)

    ''' generate code to jump to a label	
    *   @param label the label
    *   @return code goto Label<label>
    '''

    def emitGOTO(self, label, frame):
        # label: Int
        # frame: Frame

        return self.mips.emitGOTO(label)

    ''' generate some starting directives for a class.<p>
    *   .source MPC.CLASSNAME.java<p>
    *   .class public MPC.CLASSNAME<p>
    *   .super java/lang/Object<p>
    '''

    def emitPROLOG(self, name, parent):
        # name: String
        # parent: String

        result = list()
        result.append(self.mips.emitSOURCE(name + ".java"))
        result.append(self.mips.emitCLASS("public " + name))
        result.append(self.mips.emitSUPER(
            "java/land/Object" if parent == "" else parent))
        return ''.join(result)

    def emitLIMITSTACK(self, num):
        # num: Int

        return self.mips.emitLIMITSTACK(num)

    def emitLIMITLOCAL(self, num):
        # num: Int

        return self.mips.emitLIMITLOCAL(num)

    def emitEPILOG(self):
        file = open(self.filename, "w")
        file.write(''.join(str(s) for s in self.buff if s is not None))
        file.close()

    ''' print out the code to screen
    *   @param in the code to be printed out
    '''

    def printout(self, in_):
        # in_: String
        self.buff.append(in_)

    def clearBuff(self):
        self.buff.clear()

    def emitARRAYLITERAL(self, array_type, frame):
        code = ""
        for dim in array_type.dimensions:
            code += self.emitPUSHICONST(dim, frame)
        typ = self.getJVMType(array_type.typ) if isinstance(array_type.typ, ArrayType) else self.getFullType(array_type.typ)
        code += self.mips.emitANEWARRAY(typ) if (type(array_type.typ) in [ArrayType, StringType]) else self.mips.emitNEWARRAY(typ)
        return code