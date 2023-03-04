from login_api.config.prod_settings import ProdSettings
from login_api.config.staging_settings import StagingSettings
from login_api.config.dev_settings import DevSettings
from login_api.config.ci_settings import CISettings
from login_api.config.docker_settings import DockerSettings
from login_api.config.common_settings import CommonSettings


configs = {
    "prod": ProdSettings(),
    "dev": DevSettings(),
    "ci": CISettings(),
    "docker": DockerSettings()
}


def load_current_config():
    import dotenv
    import os

    dotenv.load_dotenv()
    env = os.getenv("ENV")

    return configs[env]


current_config = load_current_config()
