#!/usr/bin/env python
# coding:utf-8
"""
authors: gening
date:    2017-08-07 20:09:01
version: 1.0.0
desc:    Command Line on Markdown Notes.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
from markdown_note.note_lib import str_decode_utf8

usage = """Manage a markdown file (.md) and its attached files in the same time.
The attached files are all included in the folder whose name has the suffix `_files` 
additionally to the file name itself under the same directory. For example:
dir
├── note1.md
└── note1_files
    ├── image_1.jpg
    └── image_2.jpg

Usage:
  note <  rm  | cp | mv |offline> ...
  note <remove|copy|move|offline> ...
  note rm <file>
  note cp <source_file> <target_file>
  note cp <source_file> <target_directory>
  note mv <source_file> <target_file>
  note mv <source_file> <target_directory>
  note offline <file>

  note remove  = note rm =  note-rm
               delete `xxx.md` file and `xxx_files` folder.

  note copy    = note cp =  note-cp
               make a copy of `xxx.md` file with `xxx_files` folder.

  note move    = note mv =  note-mv
               move or rename `xxx.md` file with `xxx_files` folder.

  note-offline 
               download images linked within `xxx.md` file into `xxx_files` folder.
"""


def remove(filename):
    from markdown_note.note_remove import note_remove
    note_remove(filename)


def copy(source, target):
    from markdown_note.note_copy import note_copy
    note_copy(source, target)


def move(source, target):
    from markdown_note.note_move import note_move
    note_move(source, target)


def offline(filename):
    from markdown_note.note_offline import note_offline
    note_offline(filename)


def main():
    """The main entry.

    :return: 0 = Success
             1 = Fail
    """
    if len(sys.argv) >= 2:
        try:
            if sys.argv[1].lower() in ['rm', 'remove'] and len(sys.argv) == 3:
                filename = str_decode_utf8(sys.argv[2])
                remove(filename)
                return 0

            if sys.argv[1].lower() in ['cp', 'copy'] and len(sys.argv) == 4:
                source = str_decode_utf8(sys.argv[2])
                target = str_decode_utf8(sys.argv[3])
                copy(source, target)
                return 0

            if sys.argv[1].lower() in ['mv', 'move'] and len(sys.argv) == 4:
                source = str_decode_utf8(sys.argv[2])
                target = str_decode_utf8(sys.argv[3])
                move(source, target)
                return 0

            if sys.argv[1].lower() in ['offline'] and len(sys.argv) == 3:
                filename = str_decode_utf8(sys.argv[2])
                offline(filename)
                return 0
        except Exception as e:
            print(e)
            return 1
    print(usage)
    return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
