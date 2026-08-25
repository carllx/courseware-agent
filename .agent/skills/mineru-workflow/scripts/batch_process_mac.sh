#!/bin/zsh

# macOS/Linux bash or zsh script for batch processing PDFs

if [[ -z "$1" || -z "$2" ]]; then
    echo "Usage: $0 <INPUT_DIR> <OUTPUT_DIR>"
    exit 1
fi

INPUT_DIR=${1}
OUTPUT_DIR=${2}

# Make sure conda is available
if [ -f /opt/miniconda3/etc/profile.d/conda.sh ]; then
    source /opt/miniconda3/etc/profile.d/conda.sh
fi
conda activate MinerU || { echo "Failed to activate MinerU environment"; exit 1; }

mkdir -p "$OUTPUT_DIR"

for f in "$INPUT_DIR"/*.pdf; do
    echo "Processing $f"
    magic-pdf -p "$f" -o "$OUTPUT_DIR"
done
