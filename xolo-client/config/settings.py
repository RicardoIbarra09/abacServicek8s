# config/settings.py

from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    #para local
    #api_base_url: str = "http://localhost:10000"

    #para container
    api_base_url: str = "http://xolo-api:10000"

settings = Settings()
