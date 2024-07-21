from config.settings.environment import Environment
from config.settings.base import BackendBaseSettings
from config.settings.production import BackendProdSettings
from config.settings.development import BackendDevSettings
from config.settings.staging import BackendStageSettings
import decouple
from functools import lru_cache

class BackendSettingsFactory:
    def __init__(self, environment: str) -> None:
        self.environment = environment
        
    def __call__(self) -> BackendBaseSettings:
        if self.environment == Environment.DEVELOPMENT.value:
            return BackendDevSettings()
        elif self.environment == Environment.STAGING.value:
            return BackendStageSettings()
        else:
            return BackendProdSettings()
        
@lru_cache()
def get_settings() -> BackendBaseSettings:
    return BackendSettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()

settings: BackendBaseSettings = get_settings()