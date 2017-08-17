# coding: utf-8
"""
authors: gening
date:    2017-08-08 11:53:53
version: 1.0.0
desc:    constraints

"""
import os
import platform
import subprocess

# global constrains
SUPPORT_EXT_LIST = ['.md', '.markdown']
FOLDER_SUFFIX = '_files'
TIMESTAMP_FORMAT = '%H%M%S'


# shared functions
def parse_file_name(filename):
    dir_path, base_ext = os.path.split(filename)
    base, ext = os.path.splitext(base_ext)
    return dir_path, base, ext


def create_new_folder(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def clean_empty_folder(directory, warning=True):
    ignore = ['.DS_Store']
    if not os.path.exists(directory):
        raise Exception('%s: Not a directory' % directory)
    if not os.path.isdir(directory):
        raise Exception('%s: No such file or directory' % directory)
    files_and_dirs = os.listdir(directory)
    if len(files_and_dirs) == 0 or len(set(files_and_dirs) - set(ignore)) == 0:
        os.rmdir(directory)
    elif warning:
        raise Exception('%s: Directory not empty' % directory)


# deal with compatibility across Windows, macOS and Linux
def open_in_os(path):
    operating_system = platform.system()
    if operating_system == 'Windows':
        return os.startfile(path)
    elif operating_system == 'Darwin':
        return subprocess.call(['open', path])  # if PY>=3.5, use subprocess.run
    elif operating_system == 'Linux':
        return subprocess.call(['xdg-open', path])
    else:
        raise Exception('UNKNOWN OPERATION')


def get_trash_dir():
    operating_system = platform.system()
    if operating_system in ['Linux', 'Darwin']:
        return os.getenv('HOME') + '/.trash/'
    elif operating_system in ['Windows']:
        return 'C:\\$Recycle.Bin\\'
    else:
        raise Exception('UNKNOWN TRASH DIR')


TRASH_DIR = get_trash_dir()

# deal with compatibility in Python 2 and Python 3
# six.PY2: A boolean indicating if the code is running on Python 2.
PY2 = (platform.python_version().split('.')[0] == '2')


def str_decode_utf8(text):
    return text if not PY2 else text.decode('utf-8')


def str_encode_base64(text):
    # from six.moves.urllib.parse import quote
    if not PY2:
        # noinspection PyCompatibility
        from urllib.parse import quote
    else:
        from urllib import quote
    return quote(text.encode('utf-8'))


def get_url_data(url):
    # from six.moves.urllib.request import Request
    # from six.moves.urllib.request import urlopen
    if not PY2:
        # noinspection PyCompatibility
        from urllib.request import Request
        # noinspection PyCompatibility
        from urllib.request import urlopen
    else:
        from urllib2 import Request
        from urllib2 import urlopen
    request = Request(url=url)
    response = urlopen(request)  # not compatible with `with ... as ...`
    data = response.read()
    response.close()
    if response.getcode() == 200:  # instead of response.status to be compatible with PY2
        return data
    else:
        raise Exception(response.reason)
