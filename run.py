if __name__ == '__main__':
    from ncatbot_config import NcatbotYamlConfig
    config = NcatbotYamlConfig()
    
    from main import NcatBot
    new_bot = NcatBot()
    new_bot.run()
