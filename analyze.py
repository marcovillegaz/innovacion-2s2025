"""
Main script for analyzing Google Forms text data with spaCy
"""

import os
import sys
import argparse
import pandas as pd

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data, preprocess_dataframe, save_results
from src.text_analyzer import TextAnalyzer
from src.visualizer import (plot_word_frequency, create_wordcloud, 
                           plot_entity_distribution, plot_multiple_statistics,
                           save_plot)
import config


def main(input_file: str, text_column: str = None, output_prefix: str = "analysis"):
    """
    Main analysis function.
    
    Args:
        input_file: Path to input CSV/Excel file
        text_column: Name of the column containing text responses
        output_prefix: Prefix for output files
    """
    print("=" * 60)
    print("Google Forms Text Analysis with spaCy")
    print("=" * 60)
    
    # Ensure output directory exists
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # Load data
    print(f"\n1. Loading data from: {input_file}")
    df = load_data(input_file)
    print(f"   Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"   Columns: {df.columns.tolist()}")
    
    # Preprocess
    print("\n2. Preprocessing data...")
    df_clean = preprocess_dataframe(df, text_column)
    print(f"   {len(df_clean)} rows after cleaning")
    
    # Get text column
    if text_column is None:
        text_column = config.TEXT_COLUMN
    
    if text_column not in df_clean.columns:
        print(f"\nError: Column '{text_column}' not found!")
        print(f"Available columns: {df_clean.columns.tolist()}")
        return
    
    texts = df_clean[text_column].tolist()
    
    # Initialize analyzer
    print(f"\n3. Initializing spaCy with model: {config.SPACY_MODEL}")
    analyzer = TextAnalyzer()
    
    # Perform analysis
    print("\n4. Analyzing texts...")
    
    # Get statistics
    print("   - Computing text statistics...")
    stats_df = analyzer.get_sentiment_statistics(texts)
    
    # Get top words
    print("   - Extracting top words...")
    top_words = analyzer.get_top_words(texts, n=30)
    
    # Get top nouns
    print("   - Extracting top nouns...")
    top_nouns = analyzer.get_top_words(texts, n=30, pos_filter=['NOUN'])
    
    # Get top verbs
    print("   - Extracting top verbs...")
    top_verbs = analyzer.get_top_words(texts, n=30, pos_filter=['VERB'])
    
    # Extract entities
    print("   - Extracting named entities...")
    entities_df = analyzer.extract_entities(texts)
    
    # Save results
    print("\n5. Saving results...")
    
    # Save statistics
    stats_output = df_clean.copy()
    stats_output = pd.concat([stats_output.reset_index(drop=True), 
                             stats_df.reset_index(drop=True)], axis=1)
    save_results(stats_output, f"{output_prefix}_statistics", format='csv')
    
    # Save entities
    if not entities_df.empty:
        save_results(entities_df, f"{output_prefix}_entities", format='csv')
    
    # Save word frequencies
    words_df = pd.DataFrame(top_words, columns=['word', 'frequency'])
    save_results(words_df, f"{output_prefix}_top_words", format='csv')
    
    nouns_df = pd.DataFrame(top_nouns, columns=['noun', 'frequency'])
    save_results(nouns_df, f"{output_prefix}_top_nouns", format='csv')
    
    verbs_df = pd.DataFrame(top_verbs, columns=['verb', 'frequency'])
    save_results(verbs_df, f"{output_prefix}_top_verbs", format='csv')
    
    # Create visualizations
    print("\n6. Creating visualizations...")
    
    # Word frequency plot
    print("   - Creating word frequency plot...")
    fig = plot_word_frequency(top_words, "Most Frequent Words")
    save_plot(fig, f"{output_prefix}_word_frequency")
    
    # Word cloud
    print("   - Creating word cloud...")
    fig = create_wordcloud(top_words, "Word Cloud")
    save_plot(fig, f"{output_prefix}_wordcloud")
    
    # Entity distribution
    if not entities_df.empty:
        print("   - Creating entity distribution plot...")
        fig = plot_entity_distribution(entities_df)
        if fig:
            save_plot(fig, f"{output_prefix}_entities")
    
    # Statistics plots
    print("   - Creating statistics plots...")
    fig = plot_multiple_statistics(stats_df)
    save_plot(fig, f"{output_prefix}_statistics")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print(f"Results saved to: {config.OUTPUT_DIR}/")
    print("=" * 60)
    
    # Print summary
    print("\nSummary:")
    print(f"  - Total texts analyzed: {len(texts)}")
    print(f"  - Average tokens per text: {stats_df['num_tokens'].mean():.2f}")
    print(f"  - Average sentences per text: {stats_df['num_sentences'].mean():.2f}")
    print(f"  - Total entities found: {len(entities_df)}")
    print(f"  - Unique entity types: {entities_df['label'].nunique() if not entities_df.empty else 0}")
    print(f"\nTop 5 words: {', '.join([w for w, c in top_words[:5]])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Google Forms text data with spaCy")
    parser.add_argument("input_file", help="Path to input CSV or Excel file")
    parser.add_argument("--text-column", "-c", help="Name of the column containing text responses")
    parser.add_argument("--output-prefix", "-o", default="analysis", help="Prefix for output files")
    
    args = parser.parse_args()
    
    main(args.input_file, args.text_column, args.output_prefix)
