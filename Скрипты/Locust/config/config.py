import logging
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field

class ScenarioConfig(BaseModel):
    included: bool
    weight: int
    pacing: int

class WebToursBaseScenarioConfig(ScenarioConfig):
    ...

class WebToursBaseScenarioConfig(ScenarioConfig):
    ...

class LoadShape(BaseModel):
    duration: int = Field(default=60, validate_default=True)
    users: int = Field(default=1, validate_default=True)
    spawn_rate: float = Field(default=1, validate_default=True)
    stages_count: int = Field(default=1, validate_default=True)

class Config(BaseSettings):
   locust_locustfile: str = Field("./locustfile.py", env="LOCAST_LOCASTFILE") 
   url: str = Field('http://webtours.load-test.ru:1080', env="URL")
   loadshape_type: str = Field('baseline', env="LOADSHAPE_TYPE")
   webtours_base: WebToursBaseScenarioConfig
   webtours_cancel: WebToursBaseScenarioConfig
   loadshape: LoadShape = LoadShape()
"""
    класс logConfig описывает логгер с помощью которого имеется возможность
    в произвольный .log-файл (в данном случае это будет test_logs_log)
"""

class LogConfig():
    logger = logging.getLogger('demo_logger')
    logger.setLevel('DEBUG')
    file = logging.FileHandler(filename='mycustomlogs.log')
    file.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(file)
    logger.propagate = False

""" 
    указываем файл env_file, из которого будут взяты переменные, в том случае, 
    если система не нашла данные параметры в Переменных среды системы
"""

env_file = Path(__file__).resolve().parent.parent / ".env"
cfg = Config(_env_file=(env_file if env_file.exists() else None), _env_nested_delimiter="__") # инициализация конфига

logger = LogConfig().logger # инициализация логгера