from bitarray import bitarray
from bitarray.util import *

instructions = {"JMP": "000", "JRP": "100", "LDN": "010", "STO": "110", "SUB": "001", "CMP": "011", "STP": "111"}

def load_program(filename):
    output = []
    with open(filename, "r") as f:
        lines = f.readlines()
    
    for l in lines:
        if l[:3] in instructions:
            try:
                inst_arg = int2ba(int(l[4:]), length=13, signed=True)
                word_str = ""
                for x in inst_arg:
                    word_str += str(x)
            except:
                word_str = "0000000000000"
            word_str += instructions[l[:3]]
            word_str += "0000000000000000"
            word = bitarray(word_str)
        else:
            word = int2ba(int(l), length=32, signed=True) 
        output.append(word)

    while len(output) < 32:
        output.append(bitarray("000000000000000000000000000000000000000000000000000000"))

    return output
