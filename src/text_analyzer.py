"""
Text analysis utilities using spaCy
"""

import spacy
from typing import List, Dict, Tuple
import pandas as pd
from collections import Counter
import config
from tqdm import tqdm


class TextAnalyzer:
    """
    Main class for text analysis using spaCy
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the analyzer with a spaCy model.
        
        Args:
            model_name: Name of the spaCy model to use
        """
        if model_name is None:
            model_name = config.SPACY_MODEL
        
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Model '{model_name}' not found. Please install it using:")
            print(f"python -m spacy download {model_name}")
            raise
        
        # Set max length for processing
        self.nlp.max_length = config.MAX_TEXT_LENGTH
    
    def analyze_text(self, text: str) -> Dict:
        """
        Perform basic NLP analysis on a single text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with analysis results
        """
        doc = self.nlp(text)
        
        return {
            'text': text,
            'num_tokens': len([token for token in doc if not token.is_space]),
            'num_sentences': len(list(doc.sents)),
            'entities': [(ent.text, ent.label_) for ent in doc.ents],
            'nouns': [token.text for token in doc if token.pos_ == 'NOUN'],
            'verbs': [token.text for token in doc if token.pos_ == 'VERB'],
            'adjectives': [token.text for token in doc if token.pos_ == 'ADJ'],
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analyze multiple texts in batch.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of analysis results
        """
        results = []
        
        for doc in tqdm(self.nlp.pipe(texts, batch_size=config.BATCH_SIZE), 
                       total=len(texts), 
                       desc="Analyzing texts"):
            result = {
                'text': doc.text,
                'num_tokens': len([token for token in doc if not token.is_space]),
                'num_sentences': len(list(doc.sents)),
                'entities': [(ent.text, ent.label_) for ent in doc.ents],
                'nouns': [token.text for token in doc if token.pos_ == 'NOUN'],
                'verbs': [token.text for token in doc if token.pos_ == 'VERB'],
                'adjectives': [token.text for token in doc if token.pos_ == 'ADJ'],
            }
            results.append(result)
        
        return results
    
    def extract_entities(self, texts: List[str]) -> pd.DataFrame:
        """
        Extract named entities from texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            DataFrame with entity information
        """
        entities_list = []
        
        for i, doc in enumerate(tqdm(self.nlp.pipe(texts, batch_size=config.BATCH_SIZE),
                                    total=len(texts),
                                    desc="Extracting entities")):
            for ent in doc.ents:
                entities_list.append({
                    'text_id': i,
                    'entity': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        
        return pd.DataFrame(entities_list)
    
    def get_top_words(self, texts: List[str], n: int = 20, pos_filter: List[str] = None) -> List[Tuple[str, int]]:
        """
        Get most common words from texts.
        
        Args:
            texts: List of input texts
            n: Number of top words to return
            pos_filter: List of POS tags to filter (e.g., ['NOUN', 'VERB'])
            
        Returns:
            List of (word, count) tuples
        """
        words = []
        
        for doc in tqdm(self.nlp.pipe(texts, batch_size=config.BATCH_SIZE),
                       total=len(texts),
                       desc="Extracting words"):
            for token in doc:
                if not token.is_stop and not token.is_punct and not token.is_space:
                    if pos_filter is None or token.pos_ in pos_filter:
                        words.append(token.lemma_.lower())
        
        return Counter(words).most_common(n)
    
    def get_sentiment_statistics(self, texts: List[str]) -> pd.DataFrame:
        """
        Get basic statistics for each text.
        
        Args:
            texts: List of input texts
            
        Returns:
            DataFrame with statistics
        """
        stats = []
        
        for i, doc in enumerate(tqdm(self.nlp.pipe(texts, batch_size=config.BATCH_SIZE),
                                     total=len(texts),
                                     desc="Computing statistics")):
            non_space_tokens = [token for token in doc if not token.is_space]
            stats.append({
                'text_id': i,
                'num_tokens': len(non_space_tokens),
                'num_sentences': len(list(doc.sents)),
                'num_entities': len(doc.ents),
                'avg_word_length': sum(len(token.text) for token in non_space_tokens) / max(len(non_space_tokens), 1)
            })
        
        return pd.DataFrame(stats)
