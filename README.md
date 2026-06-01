# Memecoin AI Agent - Base Blockchain 🚀

An advanced AI Agent for sentiment analysis and trading signals on memecoin projects on Base blockchain, integrated with Uniswap V3.

## Features

✨ **Core Features**
- **AI Sentiment Analysis**: NLP-powered sentiment detection from Twitter, Discord, and on-chain data
- **Multi-Token Monitoring**: Track up to 50+ memecoin tokens simultaneously
- **Uniswap V3 Integration**: Real-time pricing and pool monitoring on Base blockchain
- **Trading Signals**: Automated buy/sell/hold signals with confidence scores
- **Portfolio Analysis**: Comprehensive portfolio sentiment and risk assessment
- **Market Intelligence**: Whale activity detection, liquidity analysis, volume tracking

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Data Collection Layer                    │
│  (Twitter, Discord, On-Chain, Uniswap)          │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Sentiment Analysis Engine                │
│  (DistilBERT, Transformers)                     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Uniswap Market Monitor                   │
│  (Pool data, Pricing, Liquidity, Volume)        │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         AI Decision Engine                       │
│  (Signal Generation, Risk Assessment)           │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Trading Signals & Alerts                │
│  (Discord, Telegram, Logging)                   │
└─────────────────────────────────────────────────┘
```

## Installation

### Requirements
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- 4GB+ RAM (for ML models)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/zozbased-hash/memecoin-sentiment-agent.git
cd memecoin-sentiment-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Setup database** (Optional for full deployment)
```bash
docker-compose up -d postgres redis
```

## Quick Start

### Basic Usage

```python
from src.ai_agent import MemecoingAIAgent
import asyncio

async def main():
    agent = MemecoingAIAgent()
    
    # Analyze a single token
    analysis = await agent.analyze_token(
        token_address="0x...",
        token_name="BASED",
        sentiment_data=["Great project!", "Amazing community"]
    )
    
    print(analysis["trading_signal"])

asyncio.run(main())
```

### Portfolio Analysis

```python
from src.ai_agent import MemecoingAIAgent
import asyncio

async def main():
    agent = MemecoingAIAgent()
    
    tokens = {
        "BASED": {
            "address": "0x...",
            "sentiment_data": [...]
        },
        "DEGEN": {
            "address": "0x...",
            "sentiment_data": [...]
        }
    }
    
    portfolio = await agent.analyze_portfolio(tokens)
    print(f"Portfolio Trend: {portfolio['portfolio_trend']}")
    print(f"Buy Signals: {portfolio['buy_signals']}")

asyncio.run(main())
```

## Configuration

### Environment Variables

```env
# Base Blockchain
BASE_RPC_URL=https://mainnet.base.org
BASE_CHAIN_ID=8453

# Uniswap V3
UNISWAP_V3_ROUTER=0x2626664c2603336e57b271c5c0b26f421741e481
UNISWAP_V3_FACTORY=0x33128a8fC17869897dcE68Ed026d694621f6FDaD

# API Keys
TWITTER_BEARER_TOKEN=your_token_here
OPENAI_API_KEY=your_key_here

# Agent Settings
SENTIMENT_THRESHOLD=0.65
TRADE_AMOUNT_USD=100
SLIPPAGE_TOLERANCE=0.01
```

## Usage Examples

### Run Full Analysis

```bash
python main.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f agent

# Stop services
docker-compose down
```

## API Reference

### MemecoingAIAgent

**Methods:**
- `analyze_token()`: Analyze single token with sentiment and market data
- `analyze_portfolio()`: Analyze multiple tokens in portfolio
- `get_trading_signals()`: Get current trading signals
- `get_analysis_history()`: Get historical analysis data

### SentimentAnalyzer

**Methods:**
- `analyze_text_sentiment()`: Analyze sentiment of text
- `analyze_crypto_sentiment()`: Analyze crypto-specific sentiment
- `detect_market_signals()`: Detect market signals from texts

### UniswapV3Monitor

**Methods:**
- `get_token_price()`: Get token price from Uniswap
- `get_pool_info()`: Get Uniswap pool information
- `monitor_token_pair()`: Monitor token pair
- `monitor_multiple_tokens()`: Monitor multiple tokens

## Risk Warnings ⚠️

- This is a **BETA** product for educational and research purposes
- **Not financial advice** - Always do your own research
- Memecoin investments are **extremely high-risk**
- Test with small amounts first
- Never invest more than you can afford to lose
- AI predictions are **not guaranteed**

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Join Server](https://discord.gg/example)
- 🐦 Twitter: [@memecoin_agent](https://twitter.com/example)

## Roadmap

- [ ] Real-time Discord integration
- [ ] Advanced whale tracking
- [ ] Multi-chain support (Ethereum, Solana, Arbitrum)
- [ ] Historical sentiment data
- [ ] Web dashboard
- [ ] GraphQL API
- [ ] Automated trading execution
- [ ] Telegram bot integration

---

**Made with ❤️ for the memecoin community**
