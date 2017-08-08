# coding: utf-8
"""
authors: gening
date:    2017-08-08 11:53:53
version: 1.0.0
desc:    constraints

"""
import os
import platform

SUPPORT_EXT_LIST = ['.md', '.markdown']
FOLDER_SUFFIX = '_files'


def get_trash_dir():
    operating_system = platform.system()
    if operating_system in ['Linux', 'Darwin']:
        return os.getenv('HOME') + '/.trash/'
    elif operating_system in ['Windows']:
        return 'C:\\$Recycle.Bin\\'
    else:
        raise Exception('UNKNOWN TRASH DIR')


TRASH_DIR = get_trash_dir()


def parse_file_name(file):
    dir, base_ext = os.path.split(file)
    base, ext = os.path.splitext(base_ext)
    return dir, base, ext
