from os import (
    makedirs as os_makedirs
)

from os.path import (
    join as os_path_join,
    abspath as os_path_abspath,
    exists as os_path_exists
)

from ncatbot_path import plugins_dir


# Base directory
jmcomic_base_dir = os_path_join(plugins_dir, 'JMComic')

# Download directory
jmcomic_download_dir = os_path_abspath(os_path_join(jmcomic_base_dir, 'download'))
if not os_path_exists(jmcomic_download_dir):
    os_makedirs(jmcomic_download_dir)

# Download jpg directory
jmcomic_download_jpg_dir = os_path_abspath(os_path_join(jmcomic_download_dir, 'jpg'))
if not os_path_exists(jmcomic_download_jpg_dir):
    os_makedirs(jmcomic_download_jpg_dir)

# Download pdf directory
jmcomic_download_pdf_dir = os_path_abspath(os_path_join(jmcomic_download_dir, 'pdf'))
if not os_path_exists(jmcomic_download_pdf_dir):
    os_makedirs(jmcomic_download_pdf_dir)

# Download zip directory
jmcomic_download_zip_dir = os_path_abspath(os_path_join(jmcomic_download_dir, 'zip'))
if not os_path_exists(jmcomic_download_zip_dir):
    os_makedirs(jmcomic_download_zip_dir)

# Database path
jmcomic_database_path = os_path_abspath(os_path_join(jmcomic_base_dir, 'db'))

if __name__ == '__main__':
    print(jmcomic_base_dir)
    print(jmcomic_download_dir)
    print(jmcomic_download_jpg_dir)
    # print(jmcomic_download_pdf_dir)
    # # print(jmcomic_download_zip_dir)
    # # print(jmcomic_database_path)