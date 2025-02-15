import os
from utils import is_linux, is_macos, is_windows

if is_linux():
    def_config_dir = os.path.join(os.environ.get('HOME'), '.config/copyon')
elif is_macos():
    def_config_dir = os.path.join(os.environ.get('HOME'), 'Application Support/copyon')
elif is_windows():
    def_config_dir = os.path.join(os.environ['LOCALAPPDATA'], 'copyon')
else:
    raise Exception('invalid platform')

CONFIG_COPYON = os.environ.get('CONFIG_COPYON', None) or def_config_dir
