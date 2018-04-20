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
import string

warning_list = []
error_list = []
port_list = {}
local_var_list = {}
comb_global_logic = {}
seq_logic = {}
key_words_in_line = []
operators = {"bitwise" : {"and" : "&", "or" : "|", "not" : "~", "inverted" : "~", "invert": "~", "xor" : "^", "xnor" : "~^"},
             "logical" : {"and" : "&&", "or" : "||", "not" : "!", "inverted" : "!", "invert": "!"}}

def syntax_checker(syntax_check_list):
    error_found = False
    logic_block_start = False
    logic_block_end = False
    for line in syntax_check_list:
        #print(line)
        syntax_to_check = line.split("++")
        if syntax_to_check[0].split()[0].split(":")[0] == "logic" or logic_block_start:
            if syntax_to_check[0].split()[0] == "end_of_logic":
                logic_block_end = True
            if (syntax_to_check[0][-1] != "," and syntax_to_check[0][-1] != ".") and logic_block_start and not logic_block_end:
                print("[Syntax Error] : Missing '.' or ',' on Line no. "+syntax_to_check[1])
                error_found = True
            logic_block_start = True
    if error_found:
        sys.exit()

def port_finder(port_line_list):
    print("\nPort List: ")
    for line in port_line_list:
        print(line)

def logic_solver(logic_line_list):
    print("\nLogic List: ")
    for line in logic_line_list:
        print(line)

def main():
    if(len(sys.argv) == 1):
        print("\nNo file path/name provided.. Exiting now..")
        sys.exit()
    else:
        shard_file_name = sys.argv[1].strip()
    print("\nWelcome to Spoken Hardware compiler")
    print(f"\nParsing {shard_file_name}")
    shard_file_line_list = []
    syntax_check_list = []
    shard_module_file = open(shard_file_name, "rt")
    module_name = ""
    logic_line_list = []
    port_line_list = []
    line_count = 1
    for line in shard_module_file:
        stripped_line = line.strip()
        #print(stripped_line)
        if stripped_line != "":
            if stripped_line.split()[0] != "//":
                shard_file_line_list.append(stripped_line)
                syntax_check_list.append(stripped_line+"++"+str(line_count))
        line_count = line_count + 1
    #print(shard_file_line_list)
    if "module" in shard_file_line_list[0] and "end_of_module" in shard_file_line_list[-1]:
        module_name = shard_file_line_list[0].split()[1].split(":")[0]
        end_of_module_name = shard_file_line_list[-1].split()[1]
        if module_name == end_of_module_name:
            print("\n"+module_name + " module found")
        else:
            print("\n[Syntax Error] : Start and end of Module not matching")
            sys.exit()
        module_found = False
        logic_found = False
        end_of_logic_found = False
        for line in shard_file_line_list:
            if line.split()[0] == "end_of_logic" and logic_found:
                end_of_logic_found = True
            if logic_found and not end_of_logic_found:
                logic_line_list.append(line)
            if line.split()[0].split(":")[0] == "logic" and not logic_found:
                logic_found = True
            if module_found and not logic_found:
                port_line_list.append(line)
            if line.split()[0].split(":")[0] == "module" and not module_found:
                module_found = True
        if logic_found and end_of_logic_found:
            print("\nLogic block found")
        else:
            print("\n[Syntax Error] : Logic block not found or syntax invalid")
            sys.exit()
    else:
        print("\n[Syntax Error] : Invalid syntax at start or end of Module")
        sys.exit()
    syntax_checker(syntax_check_list)
    #print(operators)
    port_finder(port_line_list)
    logic_solver(logic_line_list)

if __name__ == '__main__':
    main()
    print("\n******* End of Program ********")
