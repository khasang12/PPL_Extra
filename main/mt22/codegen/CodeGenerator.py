"""
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
"""
from Utils import *
from Visitor import *
from StaticCheck import *
from StaticError import *
from IdentifierCollector import IdentifierCollector
from LivenessAnalysis import LivenessAnalysis
from GraphAllocator import GraphAllocator
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod


class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [
            Symbol("readInteger", MType(list(), IntegerType()), CName(self.libName)),
            Symbol("printInteger", MType([IntegerType()], VoidType()), CName(self.libName)),
        ]
        
    def createIdentifierList(self,ast):
        collector = IdentifierCollector()
        collector.visit(ast,[])
        return collector.identifiers
    
    def handleLivenessDetection(self,lst):
        liveness = LivenessAnalysis(lst)
        flow = liveness.createFlowGraph()
        ids = liveness.getUniqueIds(flow)
        return ids,flow
    
    def createRIG(self,lst,flow):
        allocator = GraphAllocator(lst,flow)
        adj = allocator.flowToAdj()
        print("\tAdj List from Flow:",adj)
        
        number_of_registers = 8
        done = 0;
        while done == 0: 
            if allocator.graphColoring(number_of_registers):
                done = 1
            else:
                allocator.reduceGraph()
        return {k: v-1 for k, v in zip(lst, allocator.color_global)}

    def gen(self, ast, dir_):
        # ast: AST
        # dir_: String

        gl = self.init()
        
        
        id_list = self.createIdentifierList(ast)
        print("Module 1 - Identifier Collector: \n\t",id_list)
        
        unique_id_list, flow = self.handleLivenessDetection(id_list)
        print("Module 2 - Liveness Analysis: \n\t","Unique IDs: ",unique_id_list, "\n\tFlow Graph: ",flow)
        
        print("Module 3 - Register Interference Graph:")
        id_map = self.createRIG(unique_id_list, flow)
        print("\tRegister Mapping: ",id_map)
        print("---------\n")
        
        gc = CodeGenVisitor(ast, gl, dir_,id_map)
        gc.visit(ast, None)


class StringType(Type):
    def __str__(self):
        return "StringType"

    def accept(self, v, param):
        return None


class ArrayPointerType(Type):
    def __init__(self, ctype):
        # cname: String
        self.eleType = ctype

    def __str__(self):
        return "ArrayPointerType({0})".format(str(self.eleType))

    def accept(self, v, param):
        return None


class ClassType(Type):
    def __init__(self, cname):
        self.cname = cname

    def __str__(self):
        return "Class({0})".format(str(self.cname))

    def accept(self, v, param):
        return None


class SubBody:
    def __init__(self, frame, sym):
        # frame: Frame
        # sym: List[Symbol]

        self.frame = frame
        self.sym = sym


class Access:
    def __init__(self, frame, sym, isLeft):
        # frame: Frame
        # sym: List[Symbol]
        # isLeft: Boolean
        # isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft


class Val(ABC):
    pass


class Index(Val):
    def __init__(self, value):
        # value: Int

        self.value = value


class CName(Val):
    def __init__(self, value):
        # value: String

        self.value = value


class CodeGenVisitor(Visitor, Utils):
    def __init__(self, astTree, env, dir_, id_map):
        # astTree: AST
        # env: List[Symbol]
        # dir_: File

        self.astTree = astTree # Graph here
        self.env = env
        self.className = "MT22Class"
        self.path = dir_
        self.id_map = id_map
        #self.emit = Emitter(self.path + "/" + self.className + ".j")
        self.emit = Emitter(self.path + "/" + self.className + ".asm")

    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any

        self.emit.printout("# preamble")
        e = SubBody(None, self.env)
        for x in ast.decls:
            e = self.visit(x, e)
        # generate default constructor
        #self.genMETHOD(FuncDecl("<init>", None, list(), None, BlockStmt( list())), c, Frame("<init>", VoidType))
        self.emit.emitEPILOG() # write file
        return c

    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame

        isInit = consdecl.return_type is None
        isMain = consdecl.name == "main" and len(consdecl.params) == 0 and type(consdecl.return_type) is VoidType
        returnType = VoidType() if isInit else consdecl.return_type
        methodName = "<init>" if isInit else consdecl.name
        intype = [ArrayPointerType(StringType())] if isMain else list()
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))
        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations
        #if isInit:
            #self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
        #if isMain:
            #self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))

        body = consdecl.body
        list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body.body))
        #self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        ''' if isInit: 
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType: 
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame)) '''
        frame.exitScope();

    def visitFuncDecl(self, ast, o):
        # ast: FuncDecl
        # o: Any

        subctxt = o
        frame = Frame(ast.name, ast.return_type)
        self.genMETHOD(ast, subctxt.sym, frame)
        return SubBody(None, [Symbol(ast.name, MType(list(), ast.return_type), CName(self.className))] + subctxt.sym)

    def visitCallStmt(self, ast, o):
        # ast: FuncCall
        # o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.name, nenv, lambda x: x.name)
        cname = sym.value.value

        ctype = sym.mtype

        in_ = ("", list())
        for x in ast.args:
            str1, typ1 = self.visit(x, Access(frame, nenv, False))
            in_ = (in_[0] + str1, in_[1] + [typ1])
        #self.emit.printout(in_[0])
        self.emit.printout(
            self.emit.emitINVOKESTATIC(ast.name, ctype, frame, in_[0])
        )

    def visitFuncCall(self, ast, o):
        # ast: FuncCall
        # o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.name, nenv, lambda x: x.name)
        cname = sym.value.value

        ctype = sym.mtype

        in_ = ("", list())
        for x in ast.args:
            str1, typ1 = self.visit(x, Access(frame, nenv, False))
            in_ = (in_[0] + str1, in_[1] + [typ1])
        #self.emit.printout(in_[0])
        self.emit.printout(
            self.emit.emitINVOKESTATIC(ast.name, ctype, frame, in_[0])
        )

    def visitIntegerLit(self, ast, o):
        # ast: IntLiteral
        # o: Any
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(ast.val, frame), IntegerType()

    def visitAssignStmt(self,ctx,o):
        right,righttyp = self.visit(ctx.rhs,Access(o.frame, o.sym, False))
        left,lefttyp = self.visit(ctx.lhs,Access(o.frame, o.sym, True))
        if not right or not left: return
        if type(right) is list: # BinExpr
            if "$" in right[2]: # Id
                self.emit.printout("\tadd "+left+", "+right[1]+", "+right[2]+"\n")
            else: # Literal
                self.emit.printout("\taddi "+left+", "+right[1]+", "+right[2]+"\n")
        elif "$" in right: # Id
            self.emit.printout("\taddi "+left+", "+right+", 0"+"\n")
        else: # Literal
            self.emit.printout("\tli "+left+", "+right+"\n")
        
    def visitId(self,ctx,o):
        code = None
        sym = list(filter(lambda x: x.name==ctx.name,o.sym))[0]
        # Graph: Check if actually used
        if sym.name not in self.id_map: 
            return None,None
        if o.isLeft: # Write
            if type(sym.value) is Index: # Local
                code = self.emit.emitWRITEVAR(sym.name,sym.mtype,sym.value.value,o.frame,self.id_map[sym.name])
            else: #Global
                code = self.emit.emitPUTSTATIC(sym.value.value+"."+sym.name,sym.mtype,o.frame,self.id_map[sym.name])
        else: # Read
            if type(sym.value) is Index: # Local
                code = self.emit.emitREADVAR(sym.name,sym.mtype,sym.value.value,o.frame,self.id_map[sym.name])
            else: #Global
                code = self.emit.emitGETSTATIC(sym.value.value+"."+sym.name,sym.mtype,o.frame,self.id_map[sym.name])
        return code, sym.mtype
    
    def visitVarDecl(self,ctx,o):
        index = None
        ''' if o.frame: #local
            index = o.frame.getNewIndex()
            code = self.emit.emitVAR(index,ctx.name,ctx.typ,o.frame.getStartLabel(),o.frame.getEndLabel(),o.frame)
        else: #global
            code = self.emit.emitATTRIBUTE(ctx.name,ctx.typ,False) '''
        o.sym += [Symbol(ctx.name,ctx.typ,Index(index) if o.frame else CName(self.className))]
        # Graph: Check if actually used
        if ctx.name not in self.id_map: return
        if ctx.init is not None:
            right,litt = self.visit(ctx.init,Access(o.frame, o.sym, False))
            left,idt = self.visit(Id(ctx.name),Access(o.frame, o.sym, True))
            if type(right) is list: # BinExpr
                if "$" in right[2]: # Id
                    self.emit.printout("\tadd "+left+", "+right[1]+", "+right[2]+"\n")
                else: # Literal
                    self.emit.printout("\taddi "+left+", "+right[1]+", "+right[2]+"\n")
            elif "$" in right: # Id
                self.emit.printout("\taddi "+left+", "+right+", 0"+"\n")
            else: # Literal
                self.emit.printout("\tli "+left+", "+right+"\n")

    def visitBinExpr(self, ast, o):
        # ast: BinExpr(op,left,right)
        # o: Any
        ctxt = o
        frame = ctxt.frame
        left, lefttyp = self.visit(ast.left,o)
        right, righttyp = self.visit(ast.right,o)
        return [ast.op,left,right], lefttyp
    
    def visitUnExpr(self, ast, o):
        # ast: UnExpr(op,val)
        # o: Any
        ctxt = o
        frame = ctxt.frame
        val, valtyp = self.visit(ast.val,o)
        return val + self.emit.emitNEGOP(valtyp, frame), valtyp
    
    def visitIfStmt(self, ast, o):
        #expr
        exp_c, exp_t = self.visit(ast.cond, Access(o.frame,o.sym,False,True))
        self.emit.printout(exp_c)
        
        #fLabel
        fLabel = o.frame.getNewLabel()
        # skip to fLabel if False
        self.emit.printout(self.emit.emitIFFALSE(fLabel,o.frame))
        # tstmt
        self.visit(ast.tstmt,o)
        # fstmt 
        if ast.fstmt is None:
            # put fLabel here
            code = self.emit.emitLABEL(fLabel,o.frame)
            self.emit.printout(code)
        else:
            # eLabel
            eLabel = o.frame.getNewLabel()
            # skip to eLabel
            code = self.emit.emitGOTO(eLabel,o.frame)
            self.emit.printout(code)
            # put fLabel here
            code = self.emit.emitLABEL(fLabel,o.frame)
            self.emit.printout(code)
            # estmt
            self.visit(ast.fstmt,o)
            # put eLabel here
            code = self.emit.emitLABEL(eLabel,o.frame)
            self.emit.printout(code)
            
    def visitForStmt(self, ast, o):
        # Initial
        self.visit(ast.init, o)
        
        # -> Loop
        o.frame.enterLoop()
        
        # Labels
        conLabel = o.frame.getContinueLabel()
        brkLabel = o.frame.getBreakLabel()
        chkLabel, bodyLabel,updLabel = o.frame.getNewLabel(),o.frame.getNewLabel(),o.frame.getNewLabel()
        
        # Condition Check
        self.emit.printout(self.emit.emitLABEL(chkLabel, o.frame))
        ccode,ctyp = self.visit(ast.cond, Access(o.frame, o.sym, False, True))
        self.emit.printout(ccode)
        self.emit.printout(self.emit.emitIFFALSE(brkLabel,o.frame))
        
        # Body
        self.emit.printout(self.emit.emitLABEL(bodyLabel, o.frame))
        self.visit(ast.stmt,o)
        
        ## Put Continue: Update->Check Cond
        self.emit.printout(self.emit.emitLABEL(conLabel,o.frame))
        
        # Update
        self.emit.printout(self.emit.emitLABEL(updLabel, o.frame))
        self.visit(AssignStmt(ast.init.lhs,ast.upd),o)
        self.emit.printout(self.emit.emitGOTO(chkLabel,o.frame))
        
        ## Put Break
        self.emit.printout(self.emit.emitLABEL(brkLabel,o.frame))
        
        # <- Loop
        o.frame.exitLoop()
    
    def visitWhileStmt(self, ast, o):
        o.frame.enterLoop()
        # cont, break
        cntLabel = o.frame.getContinueLabel()
        brkLabel = o.frame.getBreakLabel()
        # Put cont
        code = self.emit.emitLABEL(cntLabel, o.frame)
        self.emit.printout(code)
        # expr
        ec, et = self.visit(ast.cond, Access(o.frame, o.sym, False))
        self.emit.printout(ec)
        # break if False
        code = self.emit.emitIFFALSE(brkLabel, o.frame)
        self.emit.printout(code)
        # stmt
        self.visit(ast.stmt,o)
        # Jump to cont
        code = self.emit.emitGOTO(cntLabel, o.frame)
        self.emit.printout(code)
        # Put break
        code = self.emit.emitLABEL(brkLabel, o.frame)
        self.emit.printout(code)
        # exit
        o.frame.exitLoop()
    
    def visitDoWhileStmt(self, ast, o):
        o.frame.enterLoop()
        # cont, break
        cntLabel = o.frame.getContinueLabel()
        brkLabel = o.frame.getBreakLabel()
        
        # Put cont
        code = self.emit.emitLABEL(cntLabel, o.frame)
        self.emit.printout(code)
        
        # stmt
        self.visit(ast.stmt,o)
        
        # expr
        ec, et = self.visit(ast.cond, Access(o.frame, o.sym, False))
        self.emit.printout(ec)
        # break if False
        code = self.emit.emitIFFALSE(brkLabel, o.frame)
        self.emit.printout(code)
        
        # Jump to cont
        code = self.emit.emitGOTO(cntLabel, o.frame)
        self.emit.printout(code)
        # Put break
        code = self.emit.emitLABEL(brkLabel, o.frame)
        self.emit.printout(code)
        # exit
        o.frame.exitLoop()
        
    def visitBreakStmt(self, ast, o):
        return self.emit.printout(self.emit.emitGOTO(o.frame.getBreakLabel(), o.frame))
    
    def visitContinueStmt(self, ast, o):
        return self.emit.printout(self.emit.emitGOTO(o.frame.getContinueLabel(), o.frame))
    
    def visitReturnStmt(self, ast, o):
        if ast.expr:
            code,typ = self.visit(ast.expr,Access(o.frame,o.sym,False,True))
            if type(typ) is IntegerType and type(o.frame.returnType) is FloatType:
                code += self.emit.emitI2F(o.frame) + self.emit.emitRETURN(FloatType(),o.frame)
            else:
                code += self.emit.emitRETURN(typ, o.frame)
            self.emit.printout(code)
    
    


