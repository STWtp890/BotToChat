class AbstractYamlConfig:
    def __init__(self, config_file_path: str):
        self.yaml_path = f"{config_file_path}"
        if not self.config_exist():
            self.new_default_yaml()
        self.set_config()
    
    def config_exist(self) -> bool:
        pass
    
    def new_default_yaml(self) -> None:
        pass
    
    def set_config(self):
        pass
    
    def get_yaml(self):
        pass