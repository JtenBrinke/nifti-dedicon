#This script will run the cleaning script and then all generation and decoding scripts. This is mostly used for quick testing purposes.
echo "Running all scripts in sequence..."
./clear_all_generated_data.sh
python generate_L.py
python generate_G_fsg.py
python generate_binary_G_fst.py
python compose_HCLG.py
./decode_audio.sh
echo "ALL SCRIPTS FINISHED!"