'''
This script compiles the binary G.fst file based on a text grammar fst (fsg.txt)
'''
import os, sys, shutil

generated_lang_dir="model_data/generated/L/lang/"
grammar_working_dir="model_data/generated/G/"
fsg=grammar_working_dir+"fsg.txt"

print("Performing preliminary safety checks...")
if not os.path.isfile(generated_lang_dir+"L.fst"):
    print("ERROR: L.fst does not exist, please run generate_L.py first to generate L-layer files.")
    sys.exit()

if not os.path.isfile(fsg):
    print("ERROR: text grammar FST (fsg.txt) does not exist, please run generate_G_fsg.py first.")
    sys.exit()

if os.path.isfile(grammar_working_dir+"G.fst"):
    print("ERROR: G.fst already exists, please ensure clear generation directory of previous generation remnants.")
    sys.exit()


print("Now compiling fsg.txt to binary G.fst...")
# Note: the path.sh part in the command below is absolutely necessary otherwise fstcompile crashes. Don't ask me why though.
compile_cmd='[ -f ./path.sh ] && . ./path.sh && cat {0} | fstcompile --isymbols={1} --osymbols={2} --keep_isymbols=false --keep_osymbols=false | fstarcsort --sort_type=ilabel > {3} || exit 1'.format(fsg, generated_lang_dir+'words.txt', generated_lang_dir+'words.txt', grammar_working_dir+'G.fst')
os.system(compile_cmd)
print("If the above succeeded without errors, you have succesfully generated the G.fst. You may now proceed to compose all layers into the HCLG.fst.")
