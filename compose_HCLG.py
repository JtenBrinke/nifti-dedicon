'''
This script composes previously generated layers into a new binary HCLG.fst.
'''
import os, sys, shutil
from pathlib import Path

# Import environment variables:
# TODO: this is an ugly way to deal with this but I haven't found a neat solution that works with both python and bash.
# NOTE: if you get errors about kaldi_dir not being defined, it's probably due to this import malfunctioning.
from environment import *

generated_lang_dir="model_data/generated/L/lang/"
generated_grammar_dir="model_data/generated/G/"
hclg_working_dir="model_data/generated/HCLG/"
acoustic_model_dir="model_data/input/AM/"

print("Performing preliminary safety checks...")
if not os.path.isfile(generated_lang_dir+"L.fst"):
    print("ERROR: L.fst does not exist, please run generate_L.py first to generate L-layer files.")
    sys.exit()

if not os.path.isfile(generated_grammar_dir+"G.fst"):
    print("ERROR: G.fst does not exist, please run generate_binary_G_fst.py first.")
    sys.exit()

if os.path.exists(hclg_working_dir):
    print("ERROR: graph directory already exists, please clear HCLG generation directory of any previous generation remnants.")
    sys.exit()

print("Now preparing HCLG composition environment...") 

shutil.copytree(generated_lang_dir, hclg_working_dir)
for file in os.listdir(generated_grammar_dir):
    shutil.copyfile(generated_grammar_dir+file, hclg_working_dir+file)

print("Starting composition operation...")
compose_cmd='[ -f ./path.sh ] && . ./path.sh && {0}utils/mkgraph.sh {1} {2} {3}'.format(kaldi_dir+'/egs/wsj/s5/',hclg_working_dir, acoustic_model_dir, hclg_working_dir+'graph')
os.system(compose_cmd)
print("In case no errors precede this message, the HCLG.fst should be generated (you can find it in the graph directory). You may now use the decoder.")    
