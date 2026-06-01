"""Main AI Agent for memecoin sentiment analysis and trading."""

from typing import Dict, List, Optional
from loguru import logger
import asyncio
from datetime import datetime
from src.sentiment_engine import SentimentAnalyzer, analyze_token_sentiment
from src.uniswap_monitor import UniswapV3Monitor, monitor_memecoin_market
from config.settings import settings


class MemecoingAIAgent:
    """AI Agent for memecoin market analysis and decision making."""
    
    def __init__(self):
        """Initialize the AI Agent."""
        logger.info("Initializing Memecoin AI Agent...")
        
        self.sentiment_analyzer = SentimentAnalyzer()
        self.uniswap_monitor = UniswapV3Monitor(
            settings.BASE_RPC_URL,
            settings.UNISWAP_V3_ROUTER
        )
        
        self.monitored_tokens = {}
        self.trading_signals = {}
        self.analysis_history = []
        
        logger.info("✓ Memecoin AI Agent initialized successfully")
    
    async def analyze_token(
        self,
        token_address: str,
        token_name: str,
        sentiment_data: List[str]
    ) -> Dict:
        """Analyze a single token with sentiment and market data.
        
        Args:
            token_address: Token contract address
            token_name: Human-readable token name
            sentiment_data: List of recent sentiment texts (tweets, messages, etc.)
            
        Returns:
            Complete analysis with signals
        """
        logger.info(f"Analyzing token: {token_name} ({token_address})")
        
        # Get sentiment analysis
        sentiment_result = await analyze_token_sentiment(
            token_name,
            sentiment_data
        )
        
        # Get Uniswap market data
        market_data = await self.uniswap_monitor.monitor_token_pair(
            token_address
        )
        
        # Extract relevant metrics
        sentiment_score = sentiment_result["composite"]["composite_score"]
        trend = sentiment_result["composite"]["final_trend"]
        
        # Calculate trading signal
        signal = self._generate_trading_signal(
            token_name,
            sentiment_score,
            market_data
        )
        
        analysis = {
            "token": token_name,
            "address": token_address,
            "timestamp": datetime.utcnow().isoformat(),
            "sentiment": sentiment_result["sentiment"],
            "signals": sentiment_result["signals"],
            "composite_sentiment": sentiment_result["composite"],
            "market_data": market_data,
            "trading_signal": signal
        }
        
        self.analysis_history.append(analysis)
        self.trading_signals[token_name] = signal
        
        return analysis
    
    def _generate_trading_signal(
        self,
        token_name: str,
        sentiment_score: float,
        market_data: Dict
    ) -> Dict:
        """Generate trading signal based on analysis.
        
        Args:
            token_name: Token name
            sentiment_score: Sentiment score (0-1)
            market_data: Market data from Uniswap
            
        Returns:
            Trading signal
        """
        price_data = market_data.get("price", {})
        price_change = price_data.get("price_change_24h", 0)
        volume_24h = price_data.get("volume_24h", 0)
        liquidity = price_data.get("liquidity", 0)
        
        # Risk assessment
        liquidity_risk = "high" if liquidity < 100000 else "medium" if liquidity < 1000000 else "low"
        volume_risk = "low" if volume_24h > liquidity * 0.5 else "high"
        
        # Signal determination
        if sentiment_score > settings.SENTIMENT_THRESHOLD:
            action = "BUY"
            confidence = sentiment_score
        elif sentiment_score < (1 - settings.SENTIMENT_THRESHOLD):
            action = "SELL"
            confidence = 1 - sentiment_score
        else:
            action = "HOLD"
            confidence = 0.5
        
        # Calculate position size
        position_size = settings.TRADE_AMOUNT_USD
        if liquidity_risk == "high":
            position_size *= 0.5
        if volume_risk == "high":
            position_size *= 0.7
        
        return {
            "action": action,
            "confidence": float(confidence),
            "sentiment_score": float(sentiment_score),
            "price_change_24h": float(price_change),
            "position_size_usd": float(position_size),
            "liquidity_risk": liquidity_risk,
            "volume_risk": volume_risk,
            "recommended_slippage": settings.SLIPPAGE_TOLERANCE,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def analyze_portfolio(
        self,
        tokens: Dict[str, Dict]
    ) -> Dict:
        """Analyze multiple tokens in portfolio.
        
        Args:
            tokens: Dict with token_name as key and {address, sentiment_data} as value
            
        Returns:
            Portfolio analysis
        """
        logger.info(f"Analyzing portfolio with {len(tokens)} tokens...")
        
        analyses = {}
        for token_name, token_data in tokens.items():
            try:
                analysis = await self.analyze_token(
                    token_data["address"],
                    token_name,
                    token_data.get("sentiment_data", [])
                )
                analyses[token_name] = analysis
            except Exception as e:
                logger.error(f"Error analyzing {token_name}: {e}")
        
        # Generate portfolio summary
        buy_signals = sum(
            1 for a in analyses.values()
            if a["trading_signal"]["action"] == "BUY"
        )
        sell_signals = sum(
            1 for a in analyses.values()
            if a["trading_signal"]["action"] == "SELL"
        )
        
        avg_sentiment = sum(
            a["composite_sentiment"]["composite_score"]
            for a in analyses.values()
        ) / len(analyses) if analyses else 0.5
        
        total_position_size = sum(
            a["trading_signal"]["position_size_usd"]
            for a in analyses.values()
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "token_count": len(analyses),
            "buy_signals": buy_signals,
            "sell_signals": sell_signals,
            "hold_signals": len(analyses) - buy_signals - sell_signals,
            "portfolio_sentiment": avg_sentiment,
            "total_recommended_position": total_position_size,
            "portfolio_trend": "bullish" if avg_sentiment > 0.65 else "bearish" if avg_sentiment < 0.45 else "neutral",
            "analyses": analyses
        }
    
    def get_trading_signals(self) -> List[Dict]:
        """Get all current trading signals.
        
        Returns:
            List of trading signals
        """
        return [
            {"token": name, **signal}
            for name, signal in self.trading_signals.items()
        ]
    
    def get_analysis_history(self, limit: int = 100) -> List[Dict]:
        """Get analysis history.
        
        Args:
            limit: Maximum number of analyses to return
            
        Returns:
            Analysis history
        """
        return self.analysis_history[-limit:]


async def run_agent_analysis(
    tokens: Dict[str, Dict],
    sentiment_data_source: Optional[callable] = None
) -> Dict:
    """Run complete agent analysis.
    
    Args:
        tokens: Token portfolio to analyze
        sentiment_data_source: Optional function to fetch sentiment data
        
    Returns:
        Complete analysis results
    """
    agent = MemecoingAIAgent()
    
    # Enrich tokens with sentiment data if source provided
    if sentiment_data_source:
        for token in tokens.values():
            token["sentiment_data"] = await sentiment_data_source(token["address"])
    
    # Run portfolio analysis
    portfolio_analysis = await agent.analyze_portfolio(tokens)
    
    return {
        "portfolio_analysis": portfolio_analysis,
        "trading_signals": agent.get_trading_signals()
    }
