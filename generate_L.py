# Front-end script to generate new L-fst
# by Jurriaan ten Brinke
import os, sys, shutil
from pathlib import Path

# Import environment variables:
# TODO: this is an ugly way to deal with this but I haven't found a neat solution that works with both python and bash.
# NOTE: if you get errors about kaldi_dir not being defined, it's probably due to this import malfunctioning.
from environment import *

lang_input_dir=os.getcwd()+"/model_data/input/L/"
lang_working_dir=os.getcwd()+"/model_data/generated/L/"

spoken_noise_word='<unk>' # All spoken noise sounds (e.g. coughing) will be mapped to this word. It needs to be in the lexicon, with "[SPN]" as its phonetic representation.

if not os.path.isfile("path.sh"):
    print("ERROR: path.sh does not exist, terminating!")
    sys.exit()


#cd ../../ #This was to make sure we were in the parent directory of utils...
print("Ensuring <SPOKEN NOISE> is in lexicon...")
with open(lang_input_dir+'lexicon.txt') as lexicon:
     if spoken_noise_word in lexicon.read():
         print('Lexicon OK.')
     else:
         print('ERROR: lexion does not contain spoken noise word. Please add it.')
         sys.exit()

print("Checking if no previously generated data is persistent (safety)...")
if os.path.exists(lang_working_dir):
    print("ERROR: {} is exists, please ensure clean file generation directory.".format(lang_working_dir))
    sys.exit()
    
print("Generating working directory for language files...")
Path(lang_working_dir+'dicttemp/').mkdir(parents=True, exist_ok=True)
for file in os.listdir(lang_input_dir):
    shutil.copyfile(lang_input_dir+file, lang_working_dir+"dicttemp/"+file)

print("Now running language preparation script...")
prep_lang_opts="--phone-symbol-table {}phones.txt".format(lang_working_dir+'dicttemp/')
prepare_cmd='cd {0}; ./utils/prepare_lang.sh {1} {2}dicttemp \"{3}\" {4}langtemp {5}lang'.format(kaldi_dir+'/egs/wsj/s5/',prep_lang_opts, lang_working_dir, spoken_noise_word, lang_working_dir, lang_working_dir)
os.system(prepare_cmd)
print("If the above succeeded, you have succesfully generated the L.fst. You may now proceed to generate a grammar layer (first make a grammar fsg, then generate the G.fst).")
