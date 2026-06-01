"""AI Sentiment Analysis Engine for memecoin market data."""

from typing import Dict, List, Tuple
import asyncio
from transformers import pipeline
from loguru import logger
import numpy as np
from datetime import datetime


class SentimentAnalyzer:
    """Analyze sentiment from multiple data sources."""
    
    def __init__(self):
        """Initialize sentiment analyzer with pretrained models."""
        logger.info("Initializing Sentiment Analyzer...")
        
        # Load sentiment analysis model (DistilBERT fine-tuned for sentiment)
        self.sentiment_pipe = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )
        
        logger.info("✓ Sentiment Analyzer initialized successfully")
    
    def analyze_text_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of a single text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores (0-1)
        """
        try:
            if not text or len(text) < 3:
                return {"positive": 0.5, "negative": 0.5, "neutral": 0.5}
            
            # Truncate if too long
            text = text[:512]
            
            result = self.sentiment_pipe(text)[0]
            label = result["label"]
            score = result["score"]
            
            if label == "POSITIVE":
                return {"positive": score, "negative": 1 - score}
            else:
                return {"positive": 1 - score, "negative": score}
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"positive": 0.5, "negative": 0.5}
    
    def analyze_crypto_sentiment(
        self, 
        texts: List[str], 
        token_name: str = "memecoin"
    ) -> Dict[str, float]:
        """Analyze sentiment specifically for cryptocurrency.
        
        Args:
            texts: List of texts to analyze
            token_name: Name of token for context
            
        Returns:
            Aggregated sentiment scores
        """
        if not texts:
            return {"score": 0.5, "confidence": 0.0, "trend": "neutral"}
        
        sentiment_scores = []
        
        for text in texts:
            sent = self.analyze_text_sentiment(text)
            sentiment_scores.append(sent["positive"] - sent["negative"])
        
        # Calculate aggregate sentiment
        avg_sentiment = np.mean(sentiment_scores)
        std_sentiment = np.std(sentiment_scores)
        
        # Normalize to 0-1 range
        normalized_score = (avg_sentiment + 1) / 2
        
        # Determine trend
        if normalized_score > 0.65:
            trend = "bullish"
        elif normalized_score > 0.45:
            trend = "neutral"
        else:
            trend = "bearish"
        
        return {
            "score": float(normalized_score),
            "confidence": float(1 - std_sentiment),
            "trend": trend,
            "raw_scores": sentiment_scores
        }
    
    def detect_market_signals(
        self, 
        texts: List[str]
    ) -> Dict[str, float]:
        """Detect specific market signals from texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Dictionary with signal strengths
        """
        signal_scores = {
            "bullish": [],
            "bearish": [],
            "hype": [],
            "fud": []
        }
        
        bullish_keywords = ["bull", "moon", "hodl", "pump", "gem", "diamond", "buy", "strong", "green"]
        bearish_keywords = ["bear", "crash", "dump", "rug", "scam", "fud", "red", "weak", "sell"]
        hype_keywords = ["hype", "excited", "amazing", "love", "great", "awesome", "best"]
        fud_keywords = ["fud", "bad", "hate", "terrible", "worst", "danger", "risk", "warning"]
        
        for text in texts:
            text_lower = text.lower()
            
            bullish_count = sum(1 for kw in bullish_keywords if kw in text_lower)
            bearish_count = sum(1 for kw in bearish_keywords if kw in text_lower)
            hype_count = sum(1 for kw in hype_keywords if kw in text_lower)
            fud_count = sum(1 for kw in fud_keywords if kw in text_lower)
            
            if bullish_count > 0:
                signal_scores["bullish"].append(min(bullish_count / 5, 1.0))
            if bearish_count > 0:
                signal_scores["bearish"].append(min(bearish_count / 5, 1.0))
            if hype_count > 0:
                signal_scores["hype"].append(min(hype_count / 5, 1.0))
            if fud_count > 0:
                signal_scores["fud"].append(min(fud_count / 5, 1.0))
        
        # Average the scores
        aggregated = {}
        for label, scores in signal_scores.items():
            aggregated[label] = float(np.mean(scores)) if scores else 0.0
        
        return aggregated
    
    def calculate_composite_sentiment(
        self,
        sentiment_score: float,
        signal_weights: Dict[str, float],
        price_change: float = 0.0,
        volume_change: float = 0.0
    ) -> Dict[str, float]:
        """Calculate composite sentiment from multiple factors.
        
        Args:
            sentiment_score: Base sentiment score (0-1)
            signal_weights: Weighted signals
            price_change: Percentage price change
            volume_change: Percentage volume change
            
        Returns:
            Composite sentiment analysis
        """
        # Weight calculations
        sentiment_weight = 0.4
        signal_weight = 0.3
        technical_weight = 0.3
        
        # Calculate signal component
        bullish_signals = signal_weights.get("bullish", 0)
        bearish_signals = signal_weights.get("bearish", 0)
        
        signal_score = bullish_signals - bearish_signals
        signal_score = (signal_score + 1) / 2  # Normalize
        
        # Calculate technical component
        price_score = (price_change + 100) / 200 if price_change else 0.5
        volume_score = (volume_change + 100) / 200 if volume_change else 0.5
        technical_score = (price_score + volume_score) / 2
        
        # Composite calculation
        composite = (
            sentiment_score * sentiment_weight +
            signal_score * signal_weight +
            technical_score * technical_weight
        )
        
        return {
            "composite_score": float(composite),
            "sentiment_component": float(sentiment_score),
            "signal_component": float(signal_score),
            "technical_component": float(technical_score),
            "final_trend": "bullish" if composite > 0.65 else "bearish" if composite < 0.45 else "neutral"
        }


async def analyze_token_sentiment(
    token_name: str,
    recent_data: List[str]
) -> Dict:
    """Async function to analyze token sentiment.
    
    Args:
        token_name: Name of the token
        recent_data: Recent market/social data
        
    Returns:
        Comprehensive sentiment analysis
    """
    analyzer = SentimentAnalyzer()
    
    sentiment = analyzer.analyze_crypto_sentiment(recent_data, token_name)
    signals = analyzer.detect_market_signals(recent_data)
    composite = analyzer.calculate_composite_sentiment(
        sentiment["score"],
        signals
    )
    
    return {
        "token": token_name,
        "timestamp": datetime.utcnow().isoformat(),
        "sentiment": sentiment,
        "signals": signals,
        "composite": composite
    }
