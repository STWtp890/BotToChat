import yaml


# read jmcomic config yaml
class JMComicYamlConfig:
    def __init__(self):
        self.__yaml_path = "./jmcomic_config.yaml"
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
    
    def _new_config_yaml(self) -> None:
        with open(f"{self.__yaml_path}", "w") as cfg:
            cfg.write(
                f"jmcomic_username: \"\"      # jmcomic_username\n"
                f"jmcomic_password: \"\"      # jmcomic_password\n"
            )

    def _config_exist(self) -> bool:
        from os.path import exists
        return exists(f"{self.__yaml_path}")
    
jmcomic_yaml_config = JMComicYamlConfig()

# jmcomic yaml cofig dict
attribute_dict = {
    "jmcomic_username": jmcomic_yaml_config.jmcomic_username,
    "jmcomic_password": jmcomic_yaml_config.jmcomic_password,
}

if __name__ == "__main__":
    print(attribute_dict)