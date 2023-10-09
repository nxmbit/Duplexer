import os
import gi
from gi.repository import Xdp
gi.require_version('Xdp', '1.0')

user_config_dir = os.environ.get(
    "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
)

user_data_dir = os.environ.get(
    "XDG_DATA_HOME", os.environ["HOME"] + "/.local/share"
)

user_cache_dir = os.environ.get(
    "XDG_CACHE_HOME", os.environ["HOME"] + "/.cache"
)


duplexer_config_dir = os.path.join(user_config_dir, "duplexer")
duplexer_data_dir = os.path.join(user_data_dir, "duplexer")
duplexer_cache_dir = os.path.join(user_cache_dir, "duplexer")

duplexer_virtual_printers_path = os.path.join(duplexer_config_dir, "virtual_printers.json")
duplexer_log_path = os.path.join(duplexer_data_dir, "duplexer.log")

def init_paths():
    if not os.path.exists(duplexer_config_dir):
        os.makedirs(duplexer_config_dir)

    if not os.path.exists(duplexer_data_dir):
        os.makedirs(duplexer_data_dir)

    if not os.path.exists(duplexer_cache_dir):
        os.makedirs(duplexer_cache_dir)