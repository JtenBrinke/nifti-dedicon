 
#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Custom fst generation script for the Nifti application
'''

import pdb, codecs, re, os, random, sys, errno

# Dedicon directory is the parent directory of this script:
dedicon_home=os.path.dirname(os.getcwd())

final_commands='model_data/input/G/train_text.txt'
fsg_output='model_data/generated/G/fsg.txt'

if not os.path.isfile(final_commands):
    print("ERROR: train_text is missing!")
    sys.exit()

if os.path.isfile(fsg_output):
    print("ERROR: {} already exists, please clean generation environment beforehand.".format(fsg_output))
    sys.exit()
    
os.makedirs(os.path.dirname(fsg_output))

print("Now generating text grammar FSG based on train text...")

fid_fsg=codecs.open(fsg_output,'w','utf-8')
begin_state=0
opera_state_nonumber=1
opera_state_number=2
end_state=3
begin_number_state=4
begin_unit_state=5
end_number_state=6
current_state=7
penalty='0.0'
penalty_number='3.0'
fid_fsg.write(str(begin_state)+" "+str(opera_state_nonumber)+" <eps> <eps> "+penalty+"\n")
fid_fsg.write(str(begin_state)+" "+str(opera_state_number)+" <eps> <eps> "+penalty+"\n")

for line in codecs.open(final_commands,'r','utf-8'):
    fields=line.split()
    if len(fields)==1:
      fid_fsg.write(str(opera_state_nonumber)+" "+str(end_state)+" "+fields[0]+" "+fields[0]+" "+penalty+"\n")
    elif len(fields)>1:
      fid_fsg.write(str(opera_state_nonumber)+" "+str(current_state)+" "+fields[0]+" "+fields[0]+" "+penalty+"\n")
      current_state=current_state+1
      for cnt in range(1,len(fields[1:-1])+1):
        fid_fsg.write(str(current_state-1)+" "+str(current_state)+" "+fields[cnt]+" "+fields[cnt]+" "+penalty+"\n")
        current_state=current_state+1
      fid_fsg.write(str(current_state-1)+" "+str(end_state)+" "+fields[-1]+" "+fields[-1]+" "+penalty+"\n")
fid_fsg.write(str(end_state)+" "+penalty+"\n")
fid_fsg.close()
print("Text grammar FSG has been generated, you may now compile the binary G.fst.")
