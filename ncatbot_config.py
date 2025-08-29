import yaml


# read ncatbot config yaml
class NcatbotYamlConfig:
    def __init__(self):
        self.__yaml_path = "./ncatbot_config.yaml"
        if not self._config_exist():
            self._new_config_yaml()
        self._set_config()

    def _get_yaml(self) -> dict:
        return yaml.load(open(self.__yaml_path, "r", encoding="utf-8"), Loader=yaml.FullLoader)

    def _set_config(self):
        _yaml_attribute = self._get_yaml()
        # config
        self.ws_uri = _yaml_attribute["ws_uri"]
        self.token = _yaml_attribute["token"]
        self.webui_uri = _yaml_attribute["webui_uri"]
        self.bot_uin = _yaml_attribute["bot_uin"]
        self.root = _yaml_attribute["root"]
    
    def _new_config_yaml(self) -> None:
        with open(f"{self.__yaml_path}", "w") as cfg:
            cfg.write(
                f'ws_uri: "ws://localhost:3001"      # websocket url\n'
                f'token: ""                          # ws token\n'
                f'webui_uri: "http://localhost:6099" # napcat webui\n'
                f'bot_uin: ""                        # your bot qq acount\n'
                f'root: ""                           # rooter\n'
            )
    
    def _config_exist(self) -> bool:
        from os.path import exists
        return exists(f"{self.__yaml_path}")

ncatbot_yaml_config = NcatbotYamlConfig()

# ncatbot yaml config dict
attribute_dict = {
    "ws_uri": ncatbot_yaml_config.ws_uri,
    "token": ncatbot_yaml_config.token,
    "webui_uri": ncatbot_yaml_config.webui_uri,
    "bot_uin": ncatbot_yaml_config.bot_uin,
    "root": ncatbot_yaml_config.root,
}

if __name__ == "__main__":
    print(attribute_dict)