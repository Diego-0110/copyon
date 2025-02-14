import os

# TODO: Handle error when not exists
HOME_USER = os.environ['HOME']

# TODO: define default dir for Windows and Mac
CONFIG_COPYON = os.environ.get('HOME_COPYON', None) or f'{HOME_USER}/.config/copyon'
