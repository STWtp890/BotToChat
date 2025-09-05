from yaml import (
    load as yaml_load,
    FullLoader as YamlFullLoader
)

from os.path import (
    exists as os_path_exists
)

from AbstractClass.AbstractYamlConfig import AbstractYamlConfig


# read ncatbot config yaml
class NcatbotYamlConfig(AbstractYamlConfig):
    def __init__(self, config_file_path: str = "ncatbot_config.yaml"):
        super().__init__(config_file_path)
        
    def config_exist(self) -> bool:
        return os_path_exists(f"{self.yaml_path}")
    
    def new_default_yaml(self) -> None:
        with open(f"{self.yaml_path}", "w") as cfg:
            cfg.write(
                f'ws_uri: "ws://localhost:3001"      # websocket url\n'
                f'token: ""                          # ws token\n'
                f'webui_uri: "http://localhost:6099" # napcat webui\n'
                f'bot_uin: ""                        # your bot qq acount\n'
                f'root: ""                           # rooter\n'
            )

    def set_config(self):
        yaml_attribute = self.get_yaml()
        # config
        self.ws_uri = yaml_attribute["ws_uri"]
        self.token = yaml_attribute["token"]
        self.webui_uri = yaml_attribute["webui_uri"]
        self.bot_uin = yaml_attribute["bot_uin"]
        self.root = yaml_attribute["root"]
    
    def get_yaml(self) -> dict:
        return yaml_load(open(self.yaml_path, "r", encoding="utf-8"), Loader=YamlFullLoader)
    
    
ncatbot_config_yaml = NcatbotYamlConfig()

# ncatbot yaml config dict
ncatbot_config_dict = {
    "ws_uri": ncatbot_config_yaml.ws_uri,
    "token": ncatbot_config_yaml.token,
    "webui_uri": ncatbot_config_yaml.webui_uri,
    "bot_uin": ncatbot_config_yaml.bot_uin,
    "root": ncatbot_config_yaml.root,
}

if __name__ == "__main__":
    print(ncatbot_config_dict)