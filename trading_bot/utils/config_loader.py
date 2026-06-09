import json
import os


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_settings(base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return load_json(os.path.join(base_dir, "config", "settings.json"))


def load_signal_weights(base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return load_json(os.path.join(base_dir, "config", "signal_weights.json"))
