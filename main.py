#!/usr/bin/env python3
"""Main entry point for Memecoin AI Agent."""

import asyncio
from loguru import logger
from src.ai_agent import MemecoingAIAgent, run_agent_analysis
from src.data_collector import collect_market_data
from config.settings import settings
import json
from datetime import datetime
import os

# Create logs and results directories
os.makedirs("logs", exist_ok=True)
os.makedirs("results", exist_ok=True)

logger.add(
    "logs/memecoin_agent.log",
    rotation="500 MB",
    retention="10 days",
    format="{time} | {level: <8} | {message}"
)


async def main():
    """Main function."""
    logger.info("="*50)
    logger.info("Memecoin AI Agent Starting")
    logger.info(f"Timestamp: {datetime.utcnow().isoformat()}")
    logger.info("="*50)
    
    # Example tokens to monitor
    tokens_to_monitor = [
        {
            "name": "BASED",
            "address": "0x0000000000000000000000000000000000000000"
        },
        {
            "name": "DEGEN",
            "address": "0x0000000000000000000000000000000000000000"
        },
        {
            "name": "TOSHI",
            "address": "0x0000000000000000000000000000000000000000"
        }
    ]
    
    try:
        # Step 1: Collect market data
        logger.info(f"Collecting data for {len(tokens_to_monitor)} tokens...")
        market_data = await collect_market_data(tokens_to_monitor)
        logger.info(f"✓ Collected data for {len(market_data)} tokens")
        
        # Step 2: Run agent analysis
        logger.info("Running AI Agent analysis...")
        
        # Prepare tokens dict for analysis
        tokens_for_analysis = {}
        for token in tokens_to_monitor:
            market_info = next(
                (m for m in market_data if m["token"] == token["name"]),
                None
            )
            if market_info:
                tokens_for_analysis[token["name"]] = {
                    "address": token["address"],
                    "sentiment_data": market_info.get("sentiment_texts", [])
                }
        
        # Run analysis
        results = await run_agent_analysis(tokens_for_analysis)
        
        logger.info("✓ Analysis completed")
        
        # Step 3: Display results
        portfolio_analysis = results["portfolio_analysis"]
        
        logger.info("\n" + "="*50)
        logger.info("PORTFOLIO ANALYSIS SUMMARY")
        logger.info("="*50)
        logger.info(f"Tokens Analyzed: {portfolio_analysis['token_count']}")
        logger.info(f"Buy Signals: {portfolio_analysis['buy_signals']}")
        logger.info(f"Sell Signals: {portfolio_analysis['sell_signals']}")
        logger.info(f"Hold Signals: {portfolio_analysis['hold_signals']}")
        logger.info(f"Portfolio Sentiment: {portfolio_analysis['portfolio_sentiment']:.2%}")
        logger.info(f"Portfolio Trend: {portfolio_analysis['portfolio_trend'].upper()}")
        logger.info(f"Total Recommended Position: ${portfolio_analysis['total_recommended_position']:.2f}")
        logger.info("="*50)
        
        # Log individual token signals
        for token_name, analysis in portfolio_analysis["analyses"].items():
            signal = analysis["trading_signal"]
            logger.info(f"\n{token_name}:")
            logger.info(f"  Action: {signal['action']}")
            logger.info(f"  Confidence: {signal['confidence']:.2%}")
            logger.info(f"  Sentiment Score: {signal['sentiment_score']:.2f}")
            logger.info(f"  Position Size: ${signal['position_size_usd']:.2f}")
            logger.info(f"  24h Price Change: {signal['price_change_24h']:.2f}%")
            logger.info(f"  Risk Level: {signal['liquidity_risk'].upper()}")
        
        # Save results to file
        output_file = f"results/analysis_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"\n✓ Results saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        raise
    finally:
        logger.info("\nMemecoin AI Agent Shutdown")
        logger.info("="*50)


if __name__ == "__main__":
    asyncio.run(main())
