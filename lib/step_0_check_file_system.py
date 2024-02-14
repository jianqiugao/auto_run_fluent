# 主要是生成指定的文件夹
import os
import datetime

from mod import parents_path
from mod.tools.read_config import _load_yaml

config = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/config.yaml')))


def make_dirs(date=None):
    if date is None:
        file_folder_name = datetime.datetime.now().strftime(config['DateFormate'])
    else:
        file_folder_name = date.strftime(config['DateFormate'])
    dist_dir = os.path.abspath(os.path.join(parents_path, 'run/', file_folder_name.replace('-', '_').replace(":","_").strip(), 'output_file'))
    os.makedirs(dist_dir, exist_ok=True)
    dist_dir = os.path.abspath(os.path.join(parents_path, 'run/', file_folder_name.replace('-', '_').replace(":", "_").strip(), 'fluent_data'))
    os.makedirs(dist_dir, exist_ok=True)

if __name__ == '__main__':
    date = datetime.datetime(year=2024, month=1, day=12, hour=12, minute=10, second=20)
    make_dirs(date=date)
