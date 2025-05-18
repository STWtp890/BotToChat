from jmcomic.jm_option import JmOption

from .jmcomic_config import jmcomic_username, jmcomic_password
from ..path import (
	jmcomic_download_jpg_dir,
	jmcomic_download_pdf_dir,
	jmcomic_download_zip_dir
)


def option_construct():
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
