from mod.tools.read_config import _load_yaml
import os
from mod import parents_path

# promts = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/promts.yaml')))
# config = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/config.yaml')))


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class load_config:
    def __init__(self, config_path, promots_path):
        self.config_path = config_path
        self.promots_path = promots_path
        self.config = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/config.yaml')))
        self.promots = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/promts.yaml')))
        self.name_replace = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/name_replace.yaml')))
        self.config.update(self.promots)

    def update(self, dict_parms):
        for key in dict_parms.keys():
            if key in self.name_replace.keys():
                new_key = self.name_replace[key]
                self.config[new_key] = dict_parms[key]
            else:
                self.config[key] = dict_parms[key]

    def __getitem__(self, item):
        return self.config[item]
config = load_config('config/config.yaml', 'config/promts.yaml')
promts = load_config('config/config.yaml', 'config/promts.yaml')

if __name__ == '__main__':
    config = {
        "fluent_version": "3d",
        "precision": "double",
        "processor_count": 12,
        "show_gui": 1,
        "energy_equation": 1,
        "viscous": "sst",
        "gravity": 1,
        "time": "unsteady-1st-order",
        "thermal_conductivity": 0.152,
        "viscosity": 1.99e-05,
        "molecular_weight": 4.0026,
        "formation_entropy": 126029.4,
        "reference_temperature": 298.15,
        "critical_temperature": 5.3,
        "critical_pressure": 229000,
        "critical_volume": 0.014441,
        "acentric_factor": -0.39,
        "wall_feng_l": 1.5,
        "wall_feng_l__004": 1.5,
        "wall_feng_r": 1.5,
        "wall_inpipe": 0.45,
        "wall_l": 1.5,
        "wall_outpipe_inner": 0.45,
        "wall_pipe_outter": 0.45,
        "wall_pipe_top": 0.45,
        "wall_r": 1.5
    }

    raw_config = load_config('config/config.yaml', 'config/promts.yaml')

    raw_config.update(config)
    print(raw_config.config)
    print('hello')
