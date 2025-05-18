from jmcomic.jm_option import JmOption

from ..path import (
	jmcomic_download_jpg_dir,
	jmcomic_download_pdf_dir,
	jmcomic_download_zip_dir
)

def check_jmcfg() -> bool:
	"""
	Check if jmcomic_config.py exists
	"""
	from os.path import exists
	return exists("../jmcomic_config.py")
def new_jmcfg() -> None:
	"""
	New a jmcomic_config file for jmoption
	"""
	with open("../jmcomic_config.py", "w") as cfg:
		cfg.write(
			"jmcomic_username = ''\n"
			"jmcomic_password = ''\n"
		)

def option_construct() -> JmOption:
	"""
	 - Construct the option for JMComic.
	 - This function is used to construct the option for JMComic.
	 :return: JmOption
	 """
	if not check_jmcfg():
		new_jmcfg()
	
	from .. import jmcomic_config as jmcomic_config
	jmcomic_username = jmcomic_config.jmcomic_username
	jmcomic_password = jmcomic_config.jmcomic_password
	
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
								'username': jmcomic_username,
								'password': jmcomic_password
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
						{
							'plugin': 'zip',
							'kwargs': {
								'level': 'album',
								'filename_rule': 'Aid',
								'zip_dir': jmcomic_download_zip_dir,  # 压缩文件存放的文件夹
								'delete_original_file': False  # 压缩成功后，删除所有原文件和文件夹
							}
						}
					]
				},
				'version': '2.1'
			}
		)
