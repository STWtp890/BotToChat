from os.path import (
    exists as os_path_exists
)

from AbstractClass.AbstractYamlConfig import AbstractYamlConfig


# read ncatbot config yaml
class NcatbotYamlConfig(AbstractYamlConfig):
    def __init__(self, config_file_path: str = "config.yaml"):
        super().__init__(config_file_path)
        
    def config_exist(self) -> bool:
        return os_path_exists(f"{self.yaml_path}")
    
    def new_default_yaml(self) -> None:
        with open(f"{self.yaml_path}", "w") as cfg:
            cfg.write(
            'napcat:\n'
            '  ws_uri: "ws://localhost:3001"\n'
            '  ws_token: "ncatbot"\n'
            '  ws_listen_ip: "localhost"\n'
            '  webui_uri: "http://localhost:6099"\n'
            '  webui_token: "napcat"\n'
            '  enable_webui: false\n'
            '  check_napcat_update: false\n'
            '  stop_napcat: false\n'
            '  suppress_client_initial_error: false\n'
            '  remote_mode: false\n'
            '  report_self_message: false\n'
            '  report_forward_message_detail: true\n'
            '\n'
            'plugin:\n'
            '  plugins_dir: "plugins"\n'
            '  plugin_whitelist: []\n'
            '  plugin_blacklist: []\n'
            '  skip_plugin_load: false\n'
            '\n'
            'root: "123456"\n'
            'bt_uin: "123456"\n'
            'enable_webui_interaction: false\n'
            'debug: false\n'
            'github_proxy: null\n'
            'check_ncatbot_update: true\n'
            'skip_ncatbot_install_check: false\n'
            )