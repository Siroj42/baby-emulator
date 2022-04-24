from bitarray import bitarray
from bitarray.util import *
import program_loader

# Define output CRT modes
OUTPUT_MAIN = 1
OUTPUT_ACC = 2
OUTPUT_INSTRUCTION = 3

# Define programming instructions
INSTRUCTION_JMP = bitarray('000')
INSTRUCTION_JRP = bitarray('100')
INSTRUCTION_LDN = bitarray('010')
INSTRUCTION_STO = bitarray('110')
INSTRUCTION_SUB = bitarray('001')
INSTRUCTION_CMP = bitarray('011')
INSTRUCTION_STP = bitarray('111')

# Which tube's content should be visible on the output CRT
output_mode = OUTPUT_ACC

# Create a template of an empty, 32-bit row
empty_row = ""
for i in range(32):
    empty_row += "0"

# Populate the storage with empty rows
store = []
for i in range(32):
    store.append(bitarray(empty_row))

store[0] = bitarray("0000000011110"+"010"+"0000000000000000")
store[1] = bitarray("0000000011111"+"001"+"0000000000000000")
store[2] = bitarray("0000000011101"+"110"+"0000000000000000")
store[3] = bitarray("0000000011101"+"010"+"0000000000000000")
store[4] = bitarray("0000000000000"+"111"+"0000000000000000")
store[30] = int2ba(2000, length=32)
store[31] = int2ba(3000, length=32)

# Instead load a program from the given file
fn = input("File: ")
store = program_loader.load_program(fn)

# Create an empty accumulator
acc = 0

# Main loop
inst_nr = 0
stopped = False
try:
    while not stopped:
        inst_arg = ba2int(store[inst_nr][:13], signed=True)
        if store[inst_nr][13:16] == INSTRUCTION_JMP:
            print("JMP")
            inst_nr = ba2int(store[inst_arg], signed=True) -1
        elif store[inst_nr][13:16] == INSTRUCTION_JRP:
            print("JRP")
            inst_nr += ba2int(store[inst_arg], signed=True)
        elif store[inst_nr][13:16] == INSTRUCTION_LDN:
            print("LDN")
            acc = 0 - ba2int(store[ba2int(store[inst_nr][:13])], signed=True)
        elif store[inst_nr][13:16] == INSTRUCTION_STO:
            print("STO")
            store[ba2int(store[inst_nr][:13])] = int2ba(acc, signed=True, length=32)
        elif store[inst_nr][13:16] == INSTRUCTION_SUB:
            print("SUB")
            acc -= ba2int(store[ba2int(store[inst_nr][:13])], signed=True)
        elif store[inst_nr][13:16] == INSTRUCTION_CMP:
            print("CMP")
            if acc < 0:
                inst_nr += 1
        elif store[inst_nr][13:16] == INSTRUCTION_STP:
            print("STP")
            stopped = True
        inst_nr += 1


        # Update output CRT
        if output_mode == OUTPUT_MAIN:
            for s in store:
                print(s)
                pass
        elif output_mode == OUTPUT_ACC:
            print(acc)
except KeyboardInterrupt:
    print("Shutting down...")
