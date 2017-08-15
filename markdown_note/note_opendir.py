# coding: utf-8
"""
authors: gening
date:    2017-08-15 21:28:29
version: 1.0.0
desc:    open folder attached to its markdown file.
usage:   ./note_opendir.py <md_file_name>

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
from markdown_note.note_lib import FOLDER_SUFFIX
from markdown_note.note_lib import SUPPORT_EXT_LIST
from markdown_note.note_lib import parse_file_name
from markdown_note.note_lib import open_in_os
from markdown_note.note_lib import str_decode_utf8


def note_opendir(filename):
    # validate filename name
    if not os.path.exists(filename):
        raise Exception('%s: No such file' % filename)
    # create folder
    dir_path, base_name, ext_name = parse_file_name(filename)
    if ext_name not in SUPPORT_EXT_LIST:
        raise Exception('UNKNOWN FILE TYPE')
    folder_name = base_name + FOLDER_SUFFIX
    open_in_os(os.path.join(dir_path, folder_name))


def main():
    if len(sys.argv) == 2:
        try:
            markdown_file = str_decode_utf8(sys.argv[1])
            note_opendir(markdown_file)
            return 0
        except Exception as e:
            print(e)
    else:
        print('usage: note-opendir <file>')
    return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
