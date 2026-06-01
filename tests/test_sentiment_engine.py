"""Tests for sentiment analysis engine."""

import pytest
from src.sentiment_engine import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test sentiment analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return SentimentAnalyzer()
    
    def test_analyze_positive_sentiment(self, analyzer):
        """Test positive sentiment detection."""
        text = "This memecoin is amazing and I love it!"
        result = analyzer.analyze_text_sentiment(text)
        assert result["positive"] > 0.5
    
    def test_analyze_negative_sentiment(self, analyzer):
        """Test negative sentiment detection."""
        text = "This is a terrible investment and I hate it."
        result = analyzer.analyze_text_sentiment(text)
        assert result["negative"] > 0.5
    
    def test_analyze_crypto_sentiment(self, analyzer):
        """Test crypto sentiment analysis."""
        texts = [
            "HODL this gem!",
            "Great project",
            "Amazing community"
        ]
        result = analyzer.analyze_crypto_sentiment(texts, "TestCoin")
        assert "score" in result
        assert "confidence" in result
        assert "trend" in result
        assert result["score"] > 0.5


if __name__ == "__main__":
    pytest.main([__file__])
