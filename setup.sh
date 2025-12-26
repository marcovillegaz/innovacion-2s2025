#!/bin/bash

# Setup script for the text analysis project

echo "=========================================="
echo "Text Analysis with spaCy - Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Download spaCy model
echo "Downloading spaCy Spanish model..."
python -m spacy download es_core_news_sm

if [ $? -ne 0 ]; then
    echo "Warning: Failed to download spaCy model. You may need to install it manually."
else
    echo "✓ spaCy model downloaded"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the analysis:"
echo "  python analyze.py data/ejemplo_formulario.csv --text-column Respuesta"
echo ""
echo "To start Jupyter:"
echo "  jupyter notebook notebooks/analisis_interactivo.ipynb"
echo ""
