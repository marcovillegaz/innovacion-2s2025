"""
Visualization utilities for text analysis results
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
from typing import List, Tuple
import config


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = config.FIGURE_SIZE
plt.rcParams['figure.dpi'] = config.DPI


def plot_word_frequency(word_counts: List[Tuple[str, int]], title: str = "Most Frequent Words", top_n: int = 20):
    """
    Create a bar plot of word frequencies.
    
    Args:
        word_counts: List of (word, count) tuples
        title: Plot title
        top_n: Number of words to display
    """
    words, counts = zip(*word_counts[:top_n])
    
    plt.figure(figsize=config.FIGURE_SIZE)
    plt.barh(range(len(words)), counts)
    plt.yticks(range(len(words)), words)
    plt.xlabel('Frequency')
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    return plt.gcf()


def create_wordcloud(word_counts: List[Tuple[str, int]], title: str = "Word Cloud"):
    """
    Create a word cloud from word frequencies.
    
    Args:
        word_counts: List of (word, count) tuples
        title: Plot title
    """
    word_freq = dict(word_counts)
    
    wordcloud = WordCloud(width=800, height=400, 
                         background_color='white',
                         colormap='viridis').generate_from_frequencies(word_freq)
    
    plt.figure(figsize=config.FIGURE_SIZE)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.tight_layout()
    
    return plt.gcf()


def plot_entity_distribution(entities_df: pd.DataFrame, title: str = "Named Entity Distribution"):
    """
    Plot distribution of named entity types.
    
    Args:
        entities_df: DataFrame with entity information
        title: Plot title
    """
    if entities_df.empty:
        print("No entities found to plot")
        return None
    
    entity_counts = entities_df['label'].value_counts()
    
    plt.figure(figsize=config.FIGURE_SIZE)
    entity_counts.plot(kind='bar')
    plt.xlabel('Entity Type')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return plt.gcf()


def plot_text_statistics(stats_df: pd.DataFrame, column: str = 'num_tokens', title: str = None):
    """
    Plot distribution of text statistics.
    
    Args:
        stats_df: DataFrame with text statistics
        column: Column to plot
        title: Plot title
    """
    if title is None:
        title = f"Distribution of {column.replace('_', ' ').title()}"
    
    plt.figure(figsize=config.FIGURE_SIZE)
    plt.hist(stats_df[column], bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel(column.replace('_', ' ').title())
    plt.ylabel('Frequency')
    plt.title(title)
    plt.tight_layout()
    
    return plt.gcf()


def plot_multiple_statistics(stats_df: pd.DataFrame):
    """
    Create a multi-panel plot of text statistics.
    
    Args:
        stats_df: DataFrame with text statistics
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Number of tokens
    axes[0, 0].hist(stats_df['num_tokens'], bins=30, edgecolor='black', alpha=0.7)
    axes[0, 0].set_xlabel('Number of Tokens')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Token Distribution')
    
    # Number of sentences
    axes[0, 1].hist(stats_df['num_sentences'], bins=30, edgecolor='black', alpha=0.7, color='green')
    axes[0, 1].set_xlabel('Number of Sentences')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Sentence Distribution')
    
    # Number of entities
    axes[1, 0].hist(stats_df['num_entities'], bins=30, edgecolor='black', alpha=0.7, color='orange')
    axes[1, 0].set_xlabel('Number of Entities')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Entity Count Distribution')
    
    # Average word length
    axes[1, 1].hist(stats_df['avg_word_length'], bins=30, edgecolor='black', alpha=0.7, color='red')
    axes[1, 1].set_xlabel('Average Word Length')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Word Length Distribution')
    
    plt.tight_layout()
    
    return fig


def save_plot(fig, filename: str, output_dir: str = None):
    """
    Save a plot to file.
    
    Args:
        fig: Matplotlib figure
        filename: Output filename (without extension)
        output_dir: Output directory (uses config default if None)
    """
    import os
    
    if output_dir is None:
        output_dir = config.OUTPUT_DIR
    
    output_path = os.path.join(output_dir, f"{filename}.png")
    fig.savefig(output_path, bbox_inches='tight', dpi=config.DPI)
    print(f"Plot saved to: {output_path}")
