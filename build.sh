#!/bin/bash

# Set paths
INPUT_DIR="content"
OUTPUT_DIR="latent-content-viewer/public"

# Check if reduction method is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <reduction_method>"
    echo "Available reduction methods: pca, tsne, umap, isomap"
    exit 1
fi

REDUCTION_METHOD=$1

# Activate the virtual environment
source generator/venv/bin/activate

# Clear old files
rm -rf ${OUTPUT_DIR}/nodes
rm -rf ${OUTPUT_DIR}/content
rm -f ${OUTPUT_DIR}/nodes.json

# Run the Python script
python generator/main.py ${INPUT_DIR} ${OUTPUT_DIR} --reduction_method ${REDUCTION_METHOD}

# Deactivate the virtual environment
deactivate
