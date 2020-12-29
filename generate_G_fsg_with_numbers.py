#! /usr/bin/python
# -*- coding: utf-8 -*-

import pdb, codecs, re, os, random, sys

# Dedicon directory is the parent directory of this script:
dedicon_home=os.path.dirname(os.getcwd())


numbers='model_data/input/G/numbers.txt'
units=['seconden','minuten','uur','procent']
final_commands='model_data/input/G/train_text.txt'
fsg_output='model_data/generated/G/fsg.txt'

### added this for convenience:
if os.path.exists(fsg_output):
    print("Overwriting existing fsg file at: "+fsg_output)
    os.remove(fsg_output)
else:
    print("Creating new fsg file at: "+fsg_output)
if not os.path.isfile(final_commands):
    print("ERROR: train_text is missing!")
    sys.exit()

if os.path.isfile(fsg_output):
    print("ERROR: {} already exists, please clean generation environment beforehand.".format(fsg_output))
    sys.exit()
    
os.makedirs(os.path.dirname(fsg_output))

print("Now generating text grammar FSG with numbers based on train text...")

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

for line in codecs.open(numbers,'r','utf-8'):
  fields=line.split()
  if len(fields)==1:
    fid_fsg.write(str(begin_number_state)+" "+str(begin_unit_state)+" "+fields[0]+" "+fields[0]+" "+penalty+"\n")
  elif len(fields)>1:
    fid_fsg.write(str(begin_number_state)+" "+str(current_state)+" "+fields[0]+" "+fields[0]+" "+penalty+"\n")
    current_state=current_state+1
    for word in fields[1:-1]:
      fid_fsg.write(str(current_state-1)+" "+str(current_state)+" "+word+" "+word+" "+penalty+"\n")
      current_state=current_state+1
    fid_fsg.write(str(current_state-1)+" "+str(begin_unit_state)+" "+fields[-1]+" "+fields[-1]+" "+penalty+"\n")

for unit in units:
  fid_fsg.write(str(begin_unit_state)+" "+str(end_number_state)+" "+unit+" "+unit+" "+penalty+"\n")

for line in codecs.open(final_commands,'r','utf-8'):
  if '<getal>' in line:
    fields=line.replace('seconden','').replace('minuten','').replace('uur','').replace('procent','').split()
    if fields[0]=='<getal>':
      fid_fsg.write(str(begin_state)+" "+str(begin_number_state)+" <eps> <eps> "+penalty_number+"\n")
    elif fields[0]!='<getal>' and fields[1]=='<getal>':
      fid_fsg.write(str(opera_state_number)+" "+str(begin_number_state)+" "+fields[0]+" "+fields[0]+" "+penalty_number+"\n")
    elif fields[0]!='<getal>' and fields[1]!='<getal>':
      fid_fsg.write(str(opera_state_number)+" "+str(current_state)+" "+fields[0]+" "+fields[0]+" "+penalty+"\n")
    current_state=current_state+1
    for cnt in range(1,len(fields[1:-1])+1):
      if fields[cnt-1]=='<getal>': 
        fid_fsg.write(str(end_number_state)+" "+str(current_state)+" "+fields[cnt]+" "+fields[cnt]+" "+penalty+"\n")
      elif fields[cnt]=='<getal>':
        continue
      elif fields[cnt+1]=='<getal>':
        fid_fsg.write(str(current_state-1)+" "+str(begin_number_state)+" "+fields[cnt]+" "+fields[cnt]+" "+penalty_number+"\n")
      elif fields[cnt]!='<getal>' and fields[cnt-1]!='<getal>' and fields[cnt+1]!='<getal>':
        fid_fsg.write(str(current_state-1)+" "+str(current_state)+" "+fields[cnt]+" "+fields[cnt]+" "+penalty+"\n")
      current_state=current_state+1
    if fields[-1]!='<getal>' and fields[-2]!='<getal>':
      fid_fsg.write(str(current_state-1)+" "+str(end_state)+" "+fields[-1]+" "+fields[-1]+" "+penalty+"\n")
    elif fields[-1]!='<getal>' and fields[-2]=='<getal>':
      fid_fsg.write(str(end_number_state)+" "+str(end_state)+" "+fields[-1]+" "+fields[-1]+" "+penalty+"\n")
    elif fields[-1]=='<getal>':
      fid_fsg.write(str(end_number_state)+" "+str(end_state)+" <eps> <eps> "+penalty+"\n")

  else:
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
print("Text grammar FSG with numbers has been generated, you may now compile the binary G.fst.")
