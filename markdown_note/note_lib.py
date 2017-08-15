# coding: utf-8
"""
authors: gening
date:    2017-08-08 11:53:53
version: 1.0.0
desc:    constraints

"""
import os
import platform

from six import PY2

SUPPORT_EXT_LIST = ['.md', '.markdown']
FOLDER_SUFFIX = '_files'
TIMESTAMP_FORMAT = '%H%M%S'


def get_trash_dir():
    operating_system = platform.system()
    if operating_system in ['Linux', 'Darwin']:
        return os.getenv('HOME') + '/.trash/'
    elif operating_system in ['Windows']:
        return 'C:\\$Recycle.Bin\\'
    else:
        raise Exception('UNKNOWN TRASH DIR')


TRASH_DIR = get_trash_dir()


def open_in_os(path):
    import subprocess
    operating_system = platform.system()
    if operating_system == 'Windows':
        return os.startfile(path)
    elif operating_system == 'Darwin':
        return subprocess.run(['open', path])
    elif operating_system == 'Linux':
        return subprocess.run(['xdg-open', path])
    else:
        raise Exception('UNKNOWN OPERATION')


def parse_file_name(filename):
    dir_path, base_ext = os.path.split(filename)
    base, ext = os.path.splitext(base_ext)
    return dir_path, base, ext


def create_new_folder(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def clean_empty_folder(directory):
    ignore = ['.DS_Store']
    if not os.path.exists(directory):
        raise Exception('%s: Not a directory' % directory)
    if not os.path.isdir(directory):
        raise Exception('%s: No such file or directory' % directory)
    files_and_dirs = os.listdir(directory)
    if len(files_and_dirs) == 0 or len(set(files_and_dirs) - set(ignore)) == 0:
        os.rmdir(directory)
    else:
        raise Exception('%s: Directory not empty' % directory)


def str_decode_utf8(chars):
    return chars.decode('utf-8') if PY2 else chars
