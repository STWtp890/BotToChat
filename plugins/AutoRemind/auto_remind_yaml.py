from os.path import (
    join as os_path_join,
    exists as os_path_exists,
)

from yaml import (
    load as yaml_load,
    FullLoader as YamlFullloader
)

from .auto_remind_path import autotask_base_dir


class AutoRemindYaml:
    def __init__(self) -> None:
        self.__yaml_path = os_path_join(autotask_base_dir, "auto_remind.yaml")
        if not self.config_exist():
            self.new_default_yaml()
        self._set_config()
        
    def config_exist(self) -> bool:
        return os_path_exists(f"{self.__yaml_path}")
    
    def new_default_yaml(self) -> None:
        with open(f"{self.__yaml_path}", "w") as cfg:
            cfg.write(
                f'[                                     \n'
                f'  {{                                  \n'
                f'      "enable": false,                \n'
                f'      "name": "example name",         \n'
                f'      "content": "example content",   \n'
                f'      "interval": "00:00",            \n'
                f'      "who_to_remind": {{,            \n'
                f'          "group_id": [               \n'
                f'              114514,                 \n'
                f'              1919810,                \n'
                f'          ],                          \n'
                f'          "user_id": [                \n'
                f'              114514,                 \n'
                f'              1919810,                \n'
                f'          ]                           \n'
                f'      }}                              \n'
                f'  }},                                 \n'
                f']                                     \n'
            )
    
    def _set_config(self) -> None:
        yaml_attribute = self.get_yaml()
        
        self.task_list = yaml_attribute
        
    def reload_yaml(self) -> None:
        self._set_config()
    
    def get_yaml(self) -> dict:
        return yaml_load(open(self.__yaml_path, "r", encoding="utf-8"), Loader=YamlFullloader)