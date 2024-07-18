from backend.config.settings.base import BackendBaseSettings
from backend.config.settings.environment import Environment

class BackendDevSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Development Environment"
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT