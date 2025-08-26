import yaml

# read ncatbot config yaml
class _Yaml:
    def __init__(self):
        if not self._config_exist:
            self._new_config_yaml()
            
        self.yaml_path = "ncatbot_config.yaml"
        self._set_config()

    def _get_yaml(self) -> dict:
        return yaml.load(open(self.yaml_path, "r", encoding="utf-8"), Loader=yaml.FullLoader)

    def _set_config(self):
        self.yaml = self._get_yaml()
        self.ws_uri = self.yaml["ws_uri"]
        self.token = self.yaml["token"]
        self.webui_uri = self.yaml["webui_uri"]
        self.bot_uin = self.yaml["bot_uin"]
        self.root = self.yaml["root"]
    
    @staticmethod
    def _new_config_yaml() -> None:
        with open("ncatbot_config.yaml", "w") as cfg:
            cfg.write(
                f"# ncatbot config"
                f"ws_uri: \"ws://localhost:3001\"      # websocket url\n"
                f"token: \"\"                          # ws token\n"
                f"webui_uri: \"http://localhost:6099\" # napcat webui\n"
                f"bot_uin: \"\"                        # your bot qq acount\n"
                f"root: \"\"                           # rooter\n"
            )
    
    @staticmethod
    def _config_exist() -> bool:
        from os.path import exists
        return exists("ncatbot_config.py")

_yaml = _Yaml()

config = {
    "ws_uri": _yaml.ws_uri,
    "token": _yaml.token,
    "webui_uri": _yaml.webui_uri,
    "bot_uin": _yaml.bot_uin,
    "root": _yaml.root
}