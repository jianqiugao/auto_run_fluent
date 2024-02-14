from mod.tools.read_config import _load_yaml
import os
from mod import parents_path
promts = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/promts.yaml')))
config = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/config.yaml')))