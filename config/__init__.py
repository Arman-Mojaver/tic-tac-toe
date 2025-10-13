import os
from typing import TypeVar

from config.base import BaseConfig
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

CONFIG_MAPPER = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}


def get_environment() -> str:
    environment = os.environ.get("ENVIRONMENT", "development")

    if environment not in CONFIG_MAPPER:
        err = f"Invalid environment: {environment}"
        raise ValueError(err)

    return environment


ConfigType = TypeVar("ConfigType", bound=BaseConfig)


def get_config() -> ConfigType:
    environment = get_environment()
    config_class = CONFIG_MAPPER[environment]()
    config_class.ENVIRONMENT = environment
    return config_class


config: ConfigType = get_config()


__all__ = ["config", "get_config"]
