from os.path import (
    join as os_path_join,
    exists as os_path_exists,
)

from yaml import (
    load as yaml_load,
    FullLoader as YamlFullloader
)

from AbstractClass.AbstractYamlConfig import AbstractYamlConfig
from .autoremind_path import autoremind_base_dir


class AutoRemindYaml(AbstractYamlConfig):
    def __init__(self, config_file_path: str = os_path_join(autoremind_base_dir, "auto_remind.yaml")):
        # super method of AbstractYamlConfig class will call 'set_config' method to initialize 'yaml_task_list'
        self.yaml_task_list = None
        super().__init__(config_file_path)
        
    def config_exist(self) -> bool:
        return os_path_exists(f"{self.yaml_path}")
    
    def new_default_yaml(self) -> None:
        with open(f"{self.yaml_path}", "w") as cfg:
            cfg.write(
                '- "enable": false\n'
                '  "name": "Testing example name"\n'
                '  "content": "Testing example"\n'
                '  "interval": "15s"\n'
                '  "who_to_remind":\n'
                '    "group_id": null\n'
                '    "user_id":\n'
                '       - 1582160745\n'

            )
    
    def reload_yaml(self) -> None:
        self.set_config()
        
    def set_config(self) -> None:
        self.yaml_task_list = self.get_yaml()
    
    def get_yaml(self) -> dict:
        return yaml_load(open(self.yaml_path, "r", encoding="utf-8"), Loader=YamlFullloader)