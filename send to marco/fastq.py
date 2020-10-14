import sys
import os

def DNA_sequence(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

# try:
#     fn = sys.argv[1]
# except IndexError as ie:
#     raise SystemError("Error: Specify file name\n")

# if not os.path.exists(fn):
#     raise SystemError("Error: File does not exist\n")
def process(fn, dna_key="C", dna_limit=80, frame_limit=1000):
    arr = []
    n = 4

    with open(fn, 'r') as fh:
        lines = []
        for line in fh:
            lines.append(line.rstrip())
            if len(lines) == n:
                record = DNA_sequence(lines)
                # sys.stderr.write("Record: %s\n" % (str(record)))
                arr.append(record["sequence"])
                # {'name': '@M04241:576:GW200209AmpliconEZ:1:2113:14653:29204 1:N:0:AAGGCGTA+TTGCTTGC', 'sequence': 'AGGTGCAGCTGGTGGAGTCTGGAGCTGAGGTGAAGAAGCCTGGGGCCTCAGTGAAGGTCTCCTGCAAGGCTTCTGGTTACACCTTTACCAGCTATGGTATCAGCTGGGTGCGACAGGCCCCTGGACAAGGGCTTGAGTGGATGGGATGGATCAGCGCTTACAATGGTAACACAAACTATGCACAGAAGTTCCAGGGCAGAGTCACCATGACCACAGACACATCCACGAGCACAGCCTACATGGAGCTG', 'optional': '+', 'quality': 'BBCACFFFFFFFGGGGGGGGGGHHHHHHHGHGGHHHHHHHHHHGGGGGHHHHHFGHHGHHHHHHHHHHGHHHHHHHFHHHHHHHHHHHHHHHHHHHHFGHHHHHHHHGHGGGGGGGGGGGGHGHHHHHHHGGHHGHHFFFHHHGHHHGGHHHHHHGGGGGHHHHHHGHHFHHHGHHHHHHDHHHGHHF=DGHHHHGGGGGHCHHHHHHHFGGGGGGGGGGGGGFGGGGGGGGGGFFFFFFFFFFFBFF'}
                lines = []
    
    # XXX tring each sequence inside the array
    # Adini, Citozin, Timin, Goanin
    ct = 0
    C_ct = 0

    sq_array = []
    frame_limit = len(arr) / frame_limit
    for a in range(len(arr)):
        reaction_power = count_v2_demo(arr[a], dna_key)
        if reaction_power > dna_limit:
            # one sec = 30 frame
            sq_array.append([{ "key_frame": round(a / frame_limit), "reaction_power": reaction_power, "dna_key": dna_key }])
            #print(sq_array[-1])
            ct=round(a / frame_limit)
    return sq_array

def dna_split(dna, base):
    return dna.split(base)
            
def count_v2_demo(dna, base):
    #print('dna:', dna)
    #print('base:', base)
    i = 0 # counter
    for c in dna:
        if c == base:
            i += 1
    #print(i)
    return i

# n = count_v2_demo('ATGCGGACCTAT', 'C')
# print(n)

# C_dna = process("Marco_R1_001.txt", "C")
# G_dna = process("Marco_R1_001.txt", "G")
# T_dna = process("Marco_R1_001.txt", "T")
# A_dna = process("Marco_R1_001.txt", "A")
# print(len(C_dna))