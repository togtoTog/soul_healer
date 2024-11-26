import os
import requests
import logging
from urllib.parse import urlparse


class FileUtils:

    # 重新加载模块
    @staticmethod
    def export_file(file_url, target_dir, chunk_size=1024 * 4):
        file_base_url = urlparse(file_url)
        file_base_name = os.path.basename(file_base_url.path)
        file_name, file_suffix = os.path.splitext(file_base_name)
        file_prefix = os.path.basename(target_dir)
        file_new_name = file_prefix + str(FileUtils.count_path_files(target_dir)) + file_suffix
        file_path = target_dir + "/" + file_new_name
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        logging.info("start export file, old_name = %s, new_name = %s", file_name, file_new_name)
        response = requests.get(file_url, stream=True)
        # 将响应内容保存为图片文件
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
            f.flush()
            f.close()
        return file_path

    # 获取指定文件夹的文件数
    @staticmethod
    def count_path_files(file_path):
        file_list = os.listdir(file_path)
        return len(file_list)
