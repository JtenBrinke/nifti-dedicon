# This script will automatically remove all remnants of previously generated data.
model_data_generated="model_data/generated"
decoder_results="decoder/results"
decoder_scratch="decoder/scratch"
decoder_output="decoder/output"

echo "Now deleting all previously generated data..."
rm -vfr $model_data_generated
rm -vfr $decoder_results
rm -vfr $decoder_scratch
rm -vfr $decoder_output
echo "Done."