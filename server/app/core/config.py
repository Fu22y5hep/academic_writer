from typing import Any, Dict, List, Optional, Union
import os
import yaml
from pathlib import Path

from pydantic import AnyHttpUrl, EmailStr, HttpUrl, validator
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
    @property
    def DATABASE_URL(self) -> str:
        return self._yaml_config['database']['url']

    # JWT
    @property
    def SECRET_KEY(self) -> str:
        return self._yaml_config['security']['secret_key']

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        return self._yaml_config['cors']['allowed_origins']

    # OpenAI
    @property
    def OPENAI_API_KEY(self) -> str:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        return key
    
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
        return self._yaml_config['openai']['settings']['system_prompts']['writing']

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        case_sensitive = True

settings = Settings()
