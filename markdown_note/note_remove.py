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
from markdown_note.note_lib import TIMESTAMP_FORMAT
from markdown_note.note_lib import parse_file_name
from markdown_note.note_lib import str_decode_utf8


def note_remove(filename, backup=True):
    # validate filename name
    if not os.path.exists(filename):
        raise Exception('%s: No such filename' % filename)
    # parse filename name
    dir_path, base_name, ext_name = parse_file_name(filename)
    if ext_name not in SUPPORT_EXT_LIST:
        raise Exception('UNKNOWN FILE TYPE')
    folder = os.path.join(dir_path, base_name + FOLDER_SUFFIX)

    if backup:
        # move file and folder to Trash
        # use time stamp to resolve the filename conflict in Trash
        time_str = time.strftime(TIMESTAMP_FORMAT, time.localtime())
        if os.path.exists(folder) and os.path.isdir(folder):
            # compress filename and folder into a zip filename
            zip_file_name = os.path.join(TRASH_DIR, base_name + ext_name + '_' + time_str + '.zip')
            with ZipFile(zip_file_name, 'w') as zf:
                # relative path for zip archive
                zf.write(filename, filename[len(dir_path):])
                for root, dirs, files in os.walk(folder):
                    for name in files:
                        full_name = os.path.join(root, name)
                        zf.write(full_name, full_name[len(dir_path):])
            # delete file and folder
            os.remove(filename)
            shutil.rmtree(folder)
        else:
            # move original filename to Trash
            # os.rename works only if source and destination are on the same volume.
            # using shutil.move instead.
            shutil.move(filename, os.path.join(TRASH_DIR,
                                               base_name + ext_name + '_' + time_str + ext_name))
    else:
        # delete file and folder
        os.remove(filename)
        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)
    return 0


def main():
    if len(sys.argv) == 2:
        try:
            markdown_file = str_decode_utf8(sys.argv[1])
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
