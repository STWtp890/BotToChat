from os import path

import yaml

from .jmcomic_path import jmcomic_base_dir


# read jmcomic config yaml
class JMComicYamlConfig:
    def __init__(self):
        self.__yaml_path = path.join(jmcomic_base_dir, "jmcomic_config.yaml")
        if not self._config_exist():
            self._new_config_yaml()
        self._set_config()
    
    def _get_yaml(self) -> dict:
        return yaml.load(open(self.__yaml_path, "r", encoding="utf-8"), Loader=yaml.FullLoader)
    
    def _set_config(self):
        _yaml_attribute = self._get_yaml()
        # config
        self.jmcomic_username = _yaml_attribute["jmcomic_username"]
        self.jmcomic_password = _yaml_attribute["jmcomic_password"]
        
        self.jmcomic_database = _yaml_attribute["jmcomic_database"]
        self.jmcomic_database_host = _yaml_attribute["jmcomic_database_host"]
        self.jmcomic_database_port = _yaml_attribute["jmcomic_database_port"]
        self.jmcomic_database_username = _yaml_attribute["jmcomic_database_username"]
        self.jmcomic_database_password = _yaml_attribute["jmcomic_database_password"]
        
    
    def _new_config_yaml(self) -> None:
        with open(f"{self.__yaml_path}", "w") as cfg:
            cfg.write(
                f'jmcomic_username: "" \n'
                f'jmcomic_password: "" \n'
                
                f'jmcomic_database: "jmcomic_artworks" \n'
                f'jmcomic_database_host: "localhost" \n'
                f'jmcomic_database_port: "3306" \n'
                f'jmcomic_database_username: "ncatbot_jmcomic_plugin" \n'
                f'jmcomic_database_password: "ncatbot_jmcomic_plugin" \n'
            )

    def _config_exist(self) -> bool:
        from os.path import exists
        return exists(f"{self.__yaml_path}")
    
jmcomic_yaml_config = JMComicYamlConfig()

# jmcomic yaml cofig dict
jmcomic_config_dict = {
    "jmcomic_username": jmcomic_yaml_config.jmcomic_username,
    "jmcomic_password": jmcomic_yaml_config.jmcomic_password,
    
    "jmcomic_database": jmcomic_yaml_config.jmcomic_database,
    "jmcomic_database_host": jmcomic_yaml_config.jmcomic_database_host,
    "jmcomic_database_port": jmcomic_yaml_config.jmcomic_database_port,
    "jmcomic_database_username": jmcomic_yaml_config.jmcomic_database_username,
    "jmcomic_database_password": jmcomic_yaml_config.jmcomic_database_password,
    
}

if __name__ == "__main__":
    print(jmcomic_config_dict)