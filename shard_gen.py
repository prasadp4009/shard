#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File    : shard_gen.py
Author  : Prasad Pandit
Email   : prasadp4009@gmail.com
Github  : https://github.com/prasadp4009
Description: Spoken Hardware SV generator
"""

import sys
import os

port_list = {}
comb_global_logic = {}
seq_logic = {}
operators = {"bitwise" : {"and" : "&", "or" : "|", "not" : "~", "inverted" : "~", "invert": "~", "xor" : "^", "xnor" : "~^"},
             "logical" : {"and" : "&&", "or" : "||", "not" : "!", "inverted" : "!", "invert": "!"}}

def main():
    if(len(sys.argv) == 1):
        print("No file path/name provided.. Exiting now..")
        sys.exit()
    else:
        shard_file_name = sys.argv[1].strip()
    print("Welcome to Spoken Hardware compiler")
    print(f"Parsing {shard_file_name}")
    shard_file_line_list = []
    shard_module_file = open(shard_file_name, "rt")
    for line in shard_module_file:
        stripped_line = line.strip()
        print(stripped_line)
        if stripped_line != "":
            shard_file_line_list.append(stripped_line)
    print(shard_file_line_list)
    if "module" in shard_file_line_list[0] and "end_of_module" in shard_file_line_list[-1]:
        module_name = shard_file_line_list[0].split()[1].split(":")[0]
        end_of_module_name = shard_file_line_list[-1].split()[1]
        if module_name == end_of_module_name:
            print(module_name + " module found")
        else:
            print("[Syntax Error] : Start and end of Module not matching")
            sys.exit()
    else:
        print("[Syntax Error] : Invalid syntax at start or end of Module")
        sys.exit()
    print(operators)

if __name__ == '__main__':
    main()
