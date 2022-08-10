from app.core.settings.app import AppSettings

class DevelopmentAppSettings(AppSettings):
    debug: bool = True 
    title: str = "3Dinner development"
    class Config:
        env_file = ".env"

settings = DevelopmentAppSettings()