import yaml


def _load_yaml(file: str):
    with open(file, 'r',encoding='UTF-8') as f:
        config = yaml.safe_load(f)
    return config


if __name__ == '__main__':
    _load_yaml('../../config/promts.yaml')
