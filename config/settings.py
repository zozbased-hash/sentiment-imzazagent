from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Base Blockchain
    BASE_RPC_URL: str = "https://mainnet.base.org"
    BASE_CHAIN_ID: int = 8453
    
    # Uniswap Configuration
    UNISWAP_V3_ROUTER: str = "0x2626664c2603336e57b271c5c0b26f421741e481"
    UNISWAP_V3_FACTORY: str = "0x33128a8fC17869897dcE68Ed026d694621f6FDaD"
    UNISWAP_QUOTER_V2: str = "0x3d4e44eb1374240ce5f1b282db3ec61eb6a3f64c"
    
    # AI Configuration
    HUGGINGFACE_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # Data Sources
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "postgresql://localhost/memecoin_db"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Webhooks
    DISCORD_WEBHOOK_URL: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    
    # Agent Settings
    SENTIMENT_THRESHOLD: float = 0.65
    TRADE_AMOUNT_USD: float = 100.0
    SLIPPAGE_TOLERANCE: float = 0.01
    MAX_TOKENS_TO_MONITOR: int = 50
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
