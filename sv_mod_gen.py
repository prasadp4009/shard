#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright Thu 04/12/2018  Prasad Pandit

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

File: sv_mod_gen.py
Author: Prasad Pandit
Email: ppandit@qti.qualcomm.com
Github: https://github.com/prasadp4009
Description: 
"""
import sys
import os
import re
import textwrap

def command_list():
    print ("1. Generate Directory Structure")
    print ("2. Add instance from sv file1 to sv file2")

def create_instance():
    inst_file_path = input("Enter File path/paths to search for instance: ")
    inst_file_path = " ".join(inst_file_path.split()).split(" ")
    print (len(inst_file_path))
    print (inst_file_path)
    print ("Enter instance name: ")
    print ("Enter File path where you wish to create instance: ")

def mod_gen():
    module_name = input("Enter name of module: ")
    if not re.match("^[A-Za-z0-9_]*$", module_name):
        if not re.match("^[A-Za-z_]*$", module_name[0]):
            print ("ERROR: Wrong module name format")
            sys.exit(0)
    
    try:
        module_name = module_name.capitalize()
        os.mkdir(module_name)
        os.chdir(module_name)
        module_name = module_name.lower()
        print ("Creating Directory: docs")
        os.mkdir("docs")
        print ("Creating Directory: src")
        os.mkdir("src")
        os.chdir("./src")
        print ("Creating Directory: rtl")
        os.mkdir("rtl")
        print ("Creating Directory: sim")
        os.mkdir("sim")
        print ("Creating Directory: tb")
        os.mkdir("tb")
        print ("Creating Directory: synth")
        os.mkdir("synth")
        print ("Creating Directory: scripts")
        os.mkdir("scripts")
        os.chdir("./rtl")
        module_rtl = module_name + ".sv"
        print ("Creating file: ",module_rtl)
        module_file = open(module_rtl,'w')
        module_file.write(textwrap.dedent("""\
        `ifndef {0}__SV
        `define {1}__SV

        module {2}
        (
          input logic clk,
          input logic rst_n
        );



        endmodule : {3}

        `endif

        //End of {4}
        """.format(module_name.upper(),module_name.upper(),module_name,module_name,module_name)))
        module_file.close()
        os.chdir("../tb")
        module_tb = module_name + "_tb.sv"
        print ("Creating file: ",module_tb)
        module_file = open(module_tb,'w')
        module_file.write(textwrap.dedent("""\
        `ifndef {0}_TB__SV
        `define {1}_TB__SV

        `timescale 1ns/100ps

        module {2}_tb;
          logic clk;
          logic rst_n;

          {3} DUT   (
                     .clk(clk),
                     .rst_n(rst_n)
                    );
    
          initial
          begin
            clk = 0;
            forever
               #10 clk = ~clk;
          end
    
          initial
          begin
            rst_n = 0;
            //$display("Starting Test");
            #10 $finish;
          end
        endmodule : {4}_tb

        `endif

        //End of {5}_tb
        """.format(module_name.upper(),module_name.upper(),module_name,module_name,module_name,module_name)))
        module_file.close()
        os.chdir("../sim")
        module_mk = "Makefile"
        print ("Creating file: ",module_mk)
        module_file = open(module_mk,'w')
        module_file.write(textwrap.dedent("""\
        # @Author: Pandit Prasad
        # @Date:   20-Jul-2016
        # @Last modified by:   Prasad Pandit
        # @Last modified time: 06-Apr-2018
        
        work= work
        
        top_tb_name= {0}_tb
        
        ifneq ("$(wildcard ../rtl)","") 
        RTL = ../rtl/*.sv 
        INCRTL = +incdir+../rtl 
        else 
        RTL = 
        INCRTL = 
        endif
        
        ifneq ("$(wildcard ../tb)","") 
        TB = ../tb/*.sv 
        INCTB = +incdir+../tb 
        else 
        TB = 
        INCTB = 
        endif
        
        ifneq ("$(wildcard ../agent)","") 
        AGT = ../agent/*.sv 
        INCAGT = +incdir+../agent 
        else 
        AGT = 
        INCAGT = 
        endif 
        
        ifneq ("$(wildcard ../env)","")
        ENV = ../env/*.sv
        INCENV = +incdir+../env
        else
        ENV =
        INCENV =
        endif
        
        ifneq ("$(wildcard ../pkg)","")
        PKG = ../pkg/*.sv
        INCPKG = +incdir+../pkg
        else
        PKG =
        INCPKG =
        endif
        
        ifneq ("$(wildcard ../tests)","")
        TESTS = ../tests/*.sv
        INCTESTS = +incdir+../tests
        else
        TESTS =
        INCTESTS =
        endif
        
        ifeq ($(OS),Windows_NT)
        DELFILES = clean_dos
        else
        DELFILES = clean_linux
        endif
        #VSIMOPT= -novopt -coverage work.tb
        
        VSIMOPT= -novopt -sva work.$(top_tb_name)
        
        #VSIMBATCH= -c -do "run -all; coverage report -html -htmldir covhtmlreport -verbose -threshL 50 -threshH 90; exit"
        
        VSIMBATCH= -c -do "run -all; exit"
        
        #VSIMDEBUG= -c -do "run -all; coverage report -html -htmldir covhtmlreport -verbose -threshL 50 -threshH 90; exit"
        
        VSIMDEBUG= -c -do "run -all; exit"
        
        #VSIMGUI= -do "do wave.do;run -all;coverage report -html -htmldir covhtmlreport -verbose -threshL 50 -threshH 90"
        
        VSIMGUI= -do "do wave.do;run -all;"
        
        cmp:
        	vlib $(work)
        	vmap work $(work)
        	vlog -work $(work) $(INCAGT) $(INCENV) $(INCTB) $(INCTESTS) $(INCRTL) $(PKG) $(RTL) $(TB)
        
        run_sim:
        	vsim $(VSIMBATCH) $(VSIMOPT) -l session.log
        
        run_debug:
        	vsim $(VSIMBATCH) $(VSIMOPT) -l session.log
        
        run_gui:
        	vsim $(VSIMGUI) $(VSIMOPT) -l session.log
        
        clean_linux:
        	rm -rf modelsim.* transcript* vlog.* work vsim.wlf *.log
        	clear
        
        clean_dos:
        	if exist modelsim.* del modelsim.* /F /S /Q /A
        	if exist transcript* del transcript* /F /S /Q /A
        	if exist vlog.* del vlog.* /F /S /Q /A
        	if exist vsim.wlf del vsim.wlf /F /S /Q /A
        	if exist *.log del *.log /F /S /Q /A
        	if exist work rd work /q /s
        	if exist covhtmlreport rd covhtmlreport /q /s
        
        clean_log:
        	if exist *.log del *.log /f /s /q /a
        
        clean:
        	make $(DELFILES)
        
        run_test:
        	make cmp
        	make run_sim
        
        run_test_gui:
        	make cmp
        	make run_gui
        
        run_all:
        	make clean
        	make cmp
        	make run_sim
        
        run_all_gui:
        	make clean
        	make cmp
        	make run_gui
        """.format(module_name)))
        module_file.close()
        os.chdir("../../../")
        print ("+_+_+_+_+_+_+_+ Done with module creation....!!!!! +_+_+_+_+_+_+_+\n")
        
    except FileNotFoundError as err:
        print("Error: File Not Found", format(err))
        sys.exit(0)
    except NameError:
        print("Error: Undefined variable", format(err))
        sys.exit(0)
          
    sys.exit(0)

def main():
    print ("+_+_+_+_+_+_+_+ Welcome to SystemVerilog Project Creator +_+_+_+_+_+_+_+\n")
    command_list()
    command = input("Enter command number to run: ")
    if not re.match("^[0-9]*$", command):
        print ("ERROR: Invalid entry. Exiting program...")
        sys.exit(0)
    else:
        if(command.strip() is "1"):
            mod_gen()
        elif (command.strip() is "2"):
            create_instance()
        else:
            print("Invalid command entry. Exiting program...")
            sys.exit()


if __name__ == "__main__":
    main()
