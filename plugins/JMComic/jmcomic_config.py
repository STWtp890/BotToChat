from yaml import (
    load as yaml_load,
    FullLoader as YamlFullloader
)
from os.path import (
    join as os_path_join,
    exists as os_path_exists
)

from AbstractClass.AbstractYamlConfig import AbstractYamlConfig
from .jmcomic_path import jmcomic_base_dir


class JMComicYamlConfig(AbstractYamlConfig):
    def __init__(self, config_file_path: str = os_path_join(jmcomic_base_dir, "jmcomic_config.yaml")):
        super().__init__(config_file_path)
    
    def config_exist(self) -> bool:
        return os_path_exists(f"{self.yaml_path}")
    
    def new_default_yaml(self) -> None:
        with open(f"{self.yaml_path}", "w") as cfg:
            cfg.write(
                f'jmcomic_username: "" \n'
                f'jmcomic_password: "" \n'
                
                f'jmcomic_database: "jmcomic_artworks" \n'
                f'jmcomic_database_host: "localhost" \n'
                f'jmcomic_database_port: "3306" \n'
                f'jmcomic_database_username: "ncatbot_jmcomic_plugin" \n'
                f'jmcomic_database_password: "ncatbot_jmcomic_plugin" \n'
            )
    
    def set_config(self) -> None:
        yaml_attribute = self.get_yaml()
        
        self.jmcomic_username = yaml_attribute["jmcomic_username"]
        self.jmcomic_password = yaml_attribute["jmcomic_password"]
        
        self.jmcomic_database = yaml_attribute["jmcomic_database"]
        self.jmcomic_database_host = yaml_attribute["jmcomic_database_host"]
        self.jmcomic_database_port = yaml_attribute["jmcomic_database_port"]
        self.jmcomic_database_username = yaml_attribute["jmcomic_database_username"]
        self.jmcomic_database_password = yaml_attribute["jmcomic_database_password"]
        
    def get_yaml(self) -> dict:
        return yaml_load(open(self.yaml_path, "r", encoding="utf-8"), Loader=YamlFullloader)


jmcomic_config_yaml = JMComicYamlConfig()

jmcomic_config_dict = {
    "jmcomic_username": jmcomic_config_yaml.jmcomic_username,
    "jmcomic_password": jmcomic_config_yaml.jmcomic_password,
    
    "jmcomic_database": jmcomic_config_yaml.jmcomic_database,
    "jmcomic_database_host": jmcomic_config_yaml.jmcomic_database_host,
    "jmcomic_database_port": jmcomic_config_yaml.jmcomic_database_port,
    "jmcomic_database_username": jmcomic_config_yaml.jmcomic_database_username,
    "jmcomic_database_password": jmcomic_config_yaml.jmcomic_database_password,
    
}