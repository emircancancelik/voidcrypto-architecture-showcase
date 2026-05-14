from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class InfrastructureSettings(BaseSettings):
    rabbitmq_url: SecretStr 
    redis_url: SecretStr
    
    azure_storage_connection: Optional[SecretStr] = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
