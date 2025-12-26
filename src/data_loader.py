"""
Data loader utilities for handling Google Forms CSV data
"""

import pandas as pd
import os
from typing import Optional, List
import config


def load_data(file_path: str, encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Load tabulated data from a CSV or Excel file.
    
    Args:
        file_path: Path to the data file
        encoding: File encoding (default: utf-8)
        
    Returns:
        DataFrame with the loaded data
    """
    _, ext = os.path.splitext(file_path)
    
    if ext.lower() == '.csv':
        try:
            df = pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            # Try with latin-1 encoding if utf-8 fails
            df = pd.read_csv(file_path, encoding='latin-1')
    elif ext.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
    return df


def get_text_column(df: pd.DataFrame, column_name: Optional[str] = None) -> pd.Series:
    """
    Extract text column from DataFrame.
    
    Args:
        df: Input DataFrame
        column_name: Name of the text column (if None, uses config default)
        
    Returns:
        Series containing text data
    """
    if column_name is None:
        column_name = config.TEXT_COLUMN
    
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found. Available columns: {df.columns.tolist()}")
    
    return df[column_name]


def clean_text(text: str) -> str:
    """
    Basic text cleaning.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    if pd.isna(text):
        return ""
    
    text = str(text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def preprocess_dataframe(df: pd.DataFrame, text_column: str = None) -> pd.DataFrame:
    """
    Preprocess the DataFrame for analysis.
    
    Args:
        df: Input DataFrame
        text_column: Name of the text column to clean
        
    Returns:
        Preprocessed DataFrame
    """
    df_clean = df.copy()
    
    if text_column is None:
        text_column = config.TEXT_COLUMN
    
    if text_column in df_clean.columns:
        df_clean[text_column] = df_clean[text_column].apply(clean_text)
        # Remove empty responses
        df_clean = df_clean[df_clean[text_column].str.len() > 0]
    
    return df_clean


def save_results(df: pd.DataFrame, output_name: str, format: str = None):
    """
    Save analysis results to file.
    
    Args:
        df: DataFrame to save
        output_name: Base name for output file
        format: Output format ('csv', 'xlsx', or 'json')
    """
    if format is None:
        format = config.EXPORT_FORMAT
    
    output_path = os.path.join(config.OUTPUT_DIR, f"{output_name}.{format}")
    
    if format == 'csv':
        df.to_csv(output_path, index=False, encoding='utf-8')
    elif format == 'xlsx':
        df.to_excel(output_path, index=False)
    elif format == 'json':
        df.to_json(output_path, orient='records', force_ascii=False, indent=2)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    print(f"Results saved to: {output_path}")
