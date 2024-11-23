from typing import Any, Dict, List, Optional, Union
import os
import yaml
from pathlib import Path

from pydantic import AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings

def load_yaml_config():
    config_path = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

class Settings(BaseSettings):
    # Load YAML config
    _yaml_config: Dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._yaml_config = load_yaml_config()

    # App settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Academic Writing Assistant"
    
    # Database
    DATABASE_URL: PostgresDsn

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # OpenAI
    OPENAI_API_KEY: str
    
    @property
    def OPENAI_MODEL(self) -> str:
        return self._yaml_config['openai']['models']['default']
    
    @property
    def OPENAI_MAX_TOKENS(self) -> int:
        return self._yaml_config['openai']['settings']['max_tokens']
    
    @property
    def OPENAI_TEMPERATURE(self) -> float:
        return self._yaml_config['openai']['settings']['temperature']
    
    @property
    def OPENAI_TIMEOUT(self) -> int:
        return self._yaml_config['openai']['settings']['timeout']
    
    @property
    def OPENAI_SYSTEM_PROMPT(self) -> str:
        return self._yaml_config['openai']['settings']['system_prompts']['default']

    # Rate Limiting
    @property
    def RATE_LIMIT_WINDOW(self) -> int:
        return self._yaml_config['rate_limits']['window']
    
    @property
    def FREE_TIER_RATE_LIMIT(self) -> int:
        return self._yaml_config['rate_limits']['tiers']['free']
    
    @property
    def BASIC_TIER_RATE_LIMIT(self) -> int:
        return self._yaml_config['rate_limits']['tiers']['basic']
    
    @property
    def PREMIUM_TIER_RATE_LIMIT(self) -> int:
        return self._yaml_config['rate_limits']['tiers']['premium']
    
    @property
    def UNLIMITED_TIER_RATE_LIMIT(self) -> int:
        return self._yaml_config['rate_limits']['tiers']['unlimited']

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
