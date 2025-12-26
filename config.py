"""
Configuration file for the text analysis project
"""

# Paths
DATA_DIR = "data"
OUTPUT_DIR = "output"
MODELS_DIR = "models"

# spaCy configuration
SPACY_MODEL = "es_core_news_sm"  # Spanish model for text analysis
# Alternative models:
# - "en_core_web_sm" for English
# - "es_core_news_md" for medium Spanish model
# - "es_core_news_lg" for large Spanish model

# Analysis settings
MAX_TEXT_LENGTH = 1000000  # Maximum text length for spaCy processing
BATCH_SIZE = 50  # Batch size for processing multiple texts

# Column names (customize based on your Google Forms structure)
TEXT_COLUMN = "Respuesta"  # Default column name for text responses
TIMESTAMP_COLUMN = "Marca temporal"  # Timestamp column
ID_COLUMN = "ID"  # Optional ID column

# Visualization settings
FIGURE_SIZE = (12, 8)
DPI = 100

# Export settings
EXPORT_FORMAT = "csv"  # Options: "csv", "xlsx", "json"
