from jmcomic import JmOption

from .jmcomic_config import jmcomic_config_dict
from .jmcomic_path import jmcomic_download_jpg_dir, jmcomic_download_pdf_dir # ,jmcomic_download_zip_dir


class JMComicOption:
    def __init__(self):
        self.username = jmcomic_config_dict.get("jmcomic_username")
        self.password = jmcomic_config_dict.get("jmcomic_password")
        self.jm_option = self.__option_construct()
    
    def __option_construct(self) -> JmOption:
        """
         - Construct the option for JMComic.
         - This function is used to construct the option for JMComic.
         :return: JmOption
         """
        return \
            JmOption.construct(
                {
                    'client': {
                        'cache': None,
                        'domain': [],
                        'impl': 'api',
                        'postman': {
                            'meta_data': {
                                'headers': None,
                                'proxies': {},
                                'cookies': None
                            },
                            'type': 'cffi'
                        },
                        'retry_times': 5
                    },
                    'dir_rule': {
                        'base_dir': jmcomic_download_jpg_dir,
                        'rule': 'Bd/Aid/Pindex'
                    },
                    'download': {
                        'cache': True,
                        'image': {
                            'decode': True,
                            'suffix': '.jpg'
                        },
                        'threading': {
                            'image': 30,
                            'photo': 20
                        }
                    },
                    'plugins': {
                        'valid': 'log',
                        'log': True,
                        'after_init': [
                            {
                                'plugin': 'login',
                                'kwargs': {
                                    'username': self.username,
                                    'password': self.password
                                }
                            }
                        ],
                        'after_album': [
                            {
                                'plugin': 'img2pdf',
                                'kwargs': {
                                    'pdf_dir': jmcomic_download_pdf_dir,
                                    'filename_rule': 'Aid'
                                }
                            },
                            # {
                            #     'plugin': 'zip',
                            #     'kwargs': {
                            #         'level': 'album',
                            #         'filename_rule': 'Aid',
                            #         'zip_dir': jmcomic_download_zip_dir,
                            #         'delete_original_file': False
                            #     }
                            # }
                        ]
                    },
                    'version': '2.1'
                }
            )
    
jmcomic_option = JMComicOption()