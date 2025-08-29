import os

base_dir = os.path.abspath('.')
plugins_dir = os.path.join(base_dir, 'plugins')

# Base directory
jmcomic_base_dir = os.path.join(plugins_dir, 'JMComic')

# Download directory
jmcomic_download_dir = os.path.abspath(os.path.join(jmcomic_base_dir, 'download'))
if not os.path.exists(jmcomic_download_dir):
    os.makedirs(jmcomic_download_dir)

# Download jpg directory
jmcomic_download_jpg_dir = os.path.abspath(os.path.join(jmcomic_download_dir, 'jpg'))
if not os.path.exists(jmcomic_download_jpg_dir):
    os.makedirs(jmcomic_download_jpg_dir)

# Download pdf directory
jmcomic_download_pdf_dir = os.path.abspath(os.path.join(jmcomic_download_dir, 'pdf'))
if not os.path.exists(jmcomic_download_pdf_dir):
    os.makedirs(jmcomic_download_pdf_dir)

# Download zip directory
jmcomic_download_zip_dir = os.path.abspath(os.path.join(jmcomic_download_dir, 'zip'))
if not os.path.exists(jmcomic_download_zip_dir):
    os.makedirs(jmcomic_download_zip_dir)

# Database path
jmcomic_database_path = os.path.abspath(os.path.join(jmcomic_base_dir, 'db'))

if __name__ == '__main__':
    print(jmcomic_base_dir)
    print(jmcomic_download_dir)
    print(jmcomic_download_jpg_dir)
    # print(jmcomic_download_pdf_dir)
    # # print(jmcomic_download_zip_dir)
    # # print(jmcomic_database_path)