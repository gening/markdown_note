#!/usr/bin/env python
# coding: utf-8
"""
authors: gening
date:    2017-08-08 16:01:39
version: 1.0.0
desc:    move or rename a markdown file and its folder.
usage:   ./note_move.py <src> <dst>
"""
import os
import sys

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
from markdown_note.note_copy import note_copy
from markdown_note.note_remove import note_remove


def note_move(src, dst):
    """move note

    :return: 0 = moved
             1 = not moved
    """
    return_code = note_copy(src, dst)
    if return_code == 0:
        note_remove(src)
        return 0
    return 1


def main():
    if len(sys.argv) == 3:
        try:
            markdown_src = sys.argv[1]
            markdown_dst = sys.argv[2]
            note_move(markdown_src, markdown_dst)
            return 0
        except Exception as e:
            print(e)
    else:
        print('usage: note-mv <source_file> <target_file>\n'
              '       note-mv <source_file> <target_directory>')
    return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
