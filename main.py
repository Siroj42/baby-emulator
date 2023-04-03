from bitarray import bitarray
from bitarray.util import *
import program_loader
import time

# Define output CRT modes
OUTPUT_MAIN = 1
OUTPUT_ACC = 2
OUTPUT_INSTRUCTION = 3
OUTPUT_NONE = 0

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
if ".snp" in fn:
	with open(fn, "r") as f:
		lines = f.readlines()
		for l in range(int(lines[0])):
			store[l] = bitarray(lines[l+1][5:37])
else:		
	store = program_loader.load_program(fn)

# Create an empty accumulator
acc = 0

# Main loop
inst_nr = 1
stopped = False

def conv(x):
    x = str(x)[10:len(str(x))-2]
    y = 0
    for i in x:
        if i == "0":
    	    y += 1
        else:
            break
    x = x[y:][::-1]
    x = bitarray(x)
    x = ba2int(x, signed=True)
    return x

try:
    while not stopped:
        inst = store[inst_nr-1][13:16]
        print(store[inst_nr-1])
        inst_arg = ba2int(store[inst_nr-1][:13], signed=True)
        if inst == INSTRUCTION_JMP:
            x = int2ba(inst_arg, signed=True, length=13)
            x = conv(x)
            print("jumped according to storage position", x, store[x])
            print("jumping to", conv(store[x]))
            inst_nr = conv(store[x])
        elif inst == INSTRUCTION_JRP:
            x = int2ba(inst_arg, signed=True, length=13)
            x = conv(x)
            inst_nr += conv(store[x])
        elif inst == INSTRUCTION_LDN:
            x = int2ba(inst_arg, signed=True, length=13)
            x = conv(x)
            acc = 0 - conv(store[x])
        elif inst == INSTRUCTION_STO:
            x = int2ba(inst_arg, signed=True, length=13)
            x = conv(x)
            store[x] = int2ba(acc, signed=True, length=32)[::-1]
        elif inst == INSTRUCTION_SUB:
            x = int2ba(inst_arg, signed=True, length=13)
            x = conv(x)
            acc -= conv(store[x])
        elif inst == INSTRUCTION_CMP:
            if acc < 0:
                inst_nr += 1
        elif inst == INSTRUCTION_STP:
            stopped = True
        inst_nr += 1


        # Update output CRT
        if output_mode == OUTPUT_MAIN:
            for s in store:
                print(s)
                pass
        elif output_mode == OUTPUT_ACC: 
            #print("ACC:", acc)
            pass
except KeyboardInterrupt:
    print("Shutting down...")
