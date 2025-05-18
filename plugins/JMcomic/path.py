import os


base_dir = os.path.abspath('.')
plugins_dir = os.path.join(base_dir, 'plugins')

jmcomic_base_dir = os.path.join(plugins_dir, 'JMcomic')

jmcomic_download_dir = os.path.abspath(os.path.join(jmcomic_base_dir, 'download'))
if not os.path.exists(jmcomic_download_dir):
    os.makedirs(jmcomic_download_dir)
    
jmcomic_database_path = os.path.abspath(os.path.join(jmcomic_base_dir, 'db'))
if not os.path.exists(jmcomic_database_path):
    open(jmcomic_database_path, 'w').close()

jmcomic_download_jpg_dir = os.path.abspath(os.path.join(jmcomic_download_dir, 'jpg'))
if not os.path.exists(jmcomic_download_jpg_dir):
    os.makedirs(jmcomic_download_jpg_dir)

jmcomic_download_pdf_dir = os.path.abspath(os.path.join(jmcomic_download_dir, 'pdf'))
if not os.path.exists(jmcomic_download_pdf_dir):
    os.makedirs(jmcomic_download_pdf_dir)

jmcomic_download_zip_dir = os.path.abspath(os.path.join(jmcomic_download_dir, 'zip'))
if not os.path.exists(jmcomic_download_zip_dir):
    os.makedirs(jmcomic_download_zip_dir)

if __name__ == '__main__':
    print(jmcomic_base_dir)
    print(jmcomic_download_dir)
    print(jmcomic_download_jpg_dir)
    print(jmcomic_download_pdf_dir)
    print(jmcomic_download_zip_dir)
