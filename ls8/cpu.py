"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branch_table = {
            0b00000001 : "HLT",
            0b10000010 : "LDI",
            0b01000111 : "PRN",
            0b10100010 : "MUL"
        }

    def ram_read(self,mar):   #Memory Address Register
        return self.ram[mar]

    def ram_write(self,mar,mdr):  #Memory Data Register
        self.ram[mar] = mdr

    def HLT(self):
        return False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        program = []
        with open(sys.argv[1]) as f:
            for line in f:
                try:
                    line = line.split("#",1)[0]
                    line = int(line, 2)
                    program.append(line)
                except ValueError:
                    pass
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def LDI(self, reg, value):
        self.reg[reg] = value

    def PRN(self,reg):
        print(self.reg[reg])

    def alu(self, op, reg_a = None, reg_b = None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "LDI":
            self.LDI(reg_a,reg_b)
        elif op == "PRN":
            print("PRINTING")
            self.PRN(reg_a)
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    

    def run(self):
        """Run the CPU."""
        running = True
        count = 1
        while running:
            ir = self.ram[self.pc] #instruction_register
            
            
            
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            
            if ir in self.branch_table and not self.branch_table[ir] == "HLT" :
                if self.branch_table[ir] == "LDI":
                    self.LDI(operand_a,operand_b)
                if self.branch_table[ir] == "PRN":
                    self.PRN(operand_a)
                else:
                    op = self.branch_table[ir]
                    self.alu(op,operand_a,operand_b)
            

            if (ir & (1 << 7)) >> 7 == 1:
                self.pc += 3
            else:
                self.pc += 2
            count+= 1
            
            if ir in self.branch_table and self.branch_table[ir] == "HLT":
                running = self.HLT()

            


            

        
        
'''

## KEY
# * `iiiiiiii`: 8-bit immediate value
# * `00000rrr`: Register number
# * `00000aaa`: Register number
# * `00000bbb`: Register number
## Establishing acronyms for all programs to be used in cpu.py
""" Primary Programs """
LDI = 0b10000010    ## Load Immediate - store value in register, set register to this value
LD = 0b10000011     ## Load from Other - Loads RegA with value at the memory address stored in Register B
PRN = 0b01000111    ## Print numeric value stored in register
HLT = 0b00000001    ## Halt. Stops CPU and exits emulator
POP = 0b01000110    ## Pop.
PUSH = 0b01000101   ## Push.
NOP = 0b00000000    ## No OPeration. Pass
CALL = 0b01010000   ## Calls specific subroutine (a function/program) at an address
# 01010000 00000rrr // This is address. After sending it call(address), the PC moves to the location in RAM and executes that program.
RET = 0b00010001    ## Return. 
""" Mathy Programs """
INC = 0b01100101    ## Increment (add 1) to value of the passed register
## 01100101 00000rrr
DEC = 0b01100110    ## Decrement (subtract 1 from) a value in the passed register
## 01100110 00000rrr // value
ADD = 0b10100000    ## Add. Add two registers, and replace RegA with the sum
# 10100000 00000aaa 00000bbb
SUB = 0b10100001    ## Subtract. Put result in RegA
MUL = 0b10100010   ## Multiply. Multiplies two Registers together.
DIV = 0b10100011    ## Divide. RegA/RegB. Result is stored as RegA. Exit case of RegB == 0, then HLT
## 10100011 00000aaa 00000bbb
MOD = 0b10100100    ## Remainder. Divide RegA/ReB, place the remainder in RegA. Exit Case of RegB == 0, then HLT
""" Comparison Programs """
AND = 0b10101000    ## And. The Bitwise AND ( & ). 
NOT = 0b01101001    ## Not. The Bitwise-NOT. Uses 1 Register. Stores result in that register
OR = 0b10101010     ## Or, can be Both. The Bitwise-OR. 2 Registers.
XOR = 0b10101011    ## One OR the Other, not Both.
## Comp Graphs
# A B   AND  OR  XOR  NOR  NAND
# 0 0    0   0    0    1    1
# 0 1    0   1    1    0    1
# 1 0    0   1    1    0    1
# 1 1    1   1    0    0    0
CMP = 0b10100111    ## Comparison(rega, regb). Compares two things and returns a value based upon it. Changes specific FL based it. Flag 'E' ==, sets to 1, Flag 'L' RegA < ReB sets to 1, Flag 'G' RegA > RegB sets to 1
## 10100111 00000aaa 00000bbb, A7 0a 0b
""" ????????? """
INT = 0b01010010    ## Interrupt ??????????????????
      # Issue the interrupt number stored in the given register.
      # This will set the _n_th bit in the `IS` register to the value in the given
      # register.
      # Machine code:
      # ```
      # 01010010 00000rrr
IRET = 0b00010011   ## Return from Interrupt
""" Jump Statements """
JMP = 0b01010100    ## Jump to address in the register. Set PC to that address
# Jump to an address in register if the noted Flags (FL) are set to True (1)
JNE = 0b10000011    ## Jump if Not Equal
JEQ = 0b01010101    ## Jump if Equal
JGE = 0b01011010    ## Jump if Greater/Equal
JGT = 0b01010111    ## Jump if Greater Than
JLE = 0b01011001    ## Jump if Less/Equal
JLT = 0b01011000    ## Jump if Less Than
""" Other Acronyms """
## Basic Acronyms
# CPU = Central Processing Unit
# ALU = Arithmetic-Logic Unit, carries out maths and logic operations
## Internal Registers
# IR = Instruction Register - address of currently running instruction
# MAR = Memory Address Register - Holds Memory Address we're reading/writing
# MDR = Memory Data Register - Holds value to write/Value just read
# FL = Flags (current Flags: E, L, G)
'''