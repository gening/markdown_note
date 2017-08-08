#!/usr/bin/env python
# coding:utf-8
"""
authors: gening
date:    2017-08-08 11:41:26
version: 1.0.0
desc:    delete a markdown file and its folder.
usage:   ./note_copy.py <md_file_name>
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil
import sys
import time
from zipfile import ZipFile

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
from markdown_note.note_lib import FOLDER_SUFFIX
from markdown_note.note_lib import SUPPORT_EXT_LIST
from markdown_note.note_lib import TRASH_DIR
from markdown_note.note_lib import parse_file_name


def note_remove(file):
    # validate file name
    if not os.path.exists(file):
        raise Exception('%s: No such file' % file)
    # parse file name
    dir_path, base_name, ext_name = parse_file_name(file)
    if ext_name not in SUPPORT_EXT_LIST:
        raise Exception('UNKNOWN FILE TYPE')
    folder = os.path.join(dir_path, base_name + FOLDER_SUFFIX)

    # move file and folder to Trash
    # use time stamp to resolve the filename conflict in Trash
    time_str = time.strftime("%H%M%S", time.localtime())
    if os.path.exists(folder) and os.path.isdir(folder):
        # compress file and folder into a zip file
        zip_file_name = os.path.join(TRASH_DIR, base_name + ext_name + '_' + time_str + '.zip')
        with ZipFile(zip_file_name, 'w') as zf:
            # relative path for zip archive
            zf.write(file, file[len(dir_path):])
            for root, dirs, files in os.walk(folder):
                for name in files:
                    full_name = os.path.join(root, name)
                    zf.write(full_name, full_name[len(dir_path):])
        os.remove(file)
        shutil.rmtree(folder)
    else:
        # move original file to Trash
        # os.rename works only if source and destination are on the same volume.
        # using shutil.move instead.
        shutil.move(file, os.path.join(TRASH_DIR, base_name + ext_name + '_' + time_str + ext_name))
    return 0


def main():
    if len(sys.argv) == 2:
        try:
            markdown_file = sys.argv[1]
            note_remove(markdown_file)
            return 0
        except Exception as e:
            print(e)
    else:
        print('usage: note-rm <file>')
    return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
