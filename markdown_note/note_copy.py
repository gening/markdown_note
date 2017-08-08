#!/usr/bin/env python
# coding:utf-8
"""
authors: gening
date:    2017-06-07 13:48:26
version: 1.1.0
desc:    make a copy of a markdown file and its folder.
         meanwhile, the title, and images and files links are updated.
usage:   ./note_copy.py <src> <dst>
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import os
import re
import shutil
import sys

from six.moves import urllib_parse

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
from markdown_note.note_lib import FOLDER_SUFFIX
from markdown_note.note_lib import SUPPORT_EXT_LIST
from markdown_note.note_lib import parse_file_name

# ![abc](xxx_files/image_1.jpg)
# [abc](xxx_files/doc_1.pdf)
# group(1) = [abc](
# group(2) = xxx
# group(3) = _files/doc_1.pdf)
link_re_pattern = '(\[.*?\]\()(.*?)(_files/.*?\))'


def note_copy(src, dst):
    """copy note

    :return: 0 = copied
             1 = not copied
    """
    # validate src file name
    if not os.path.exists(src):
        raise Exception('%s: No such file' % src)
    elif os.path.isdir(src):
        raise Exception('%s is a directory (skipped)' % src)
    # parse src file name
    src_dir, src_base, src_ext = parse_file_name(src)
    if src_ext not in SUPPORT_EXT_LIST:
        raise Exception('UNKNOWN FILE TYPE')
    src_folder = os.path.join(src_dir, src_base + FOLDER_SUFFIX)

    # validate and parse dst file name
    if os.path.exists(dst) and os.path.isfile(dst):
        # do not overwrite
        raise Exception('%s exists (not overwritten)' % dst)
    elif os.path.exists(dst) and os.path.isdir(dst):
        dst_dir, dst_base, dst_ext = dst, src_base, src_ext
        dst = os.path.join(dst_dir, dst_base + dst_ext)
    else:
        # parse dst file name
        dst_dir, dst_base, dst_ext = parse_file_name(dst)
        if dst_ext not in SUPPORT_EXT_LIST:
            dst_ext = src_ext
            dst = os.path.join(dst_dir, dst_base + dst_ext)
    dst_folder = os.path.join(dst_dir, dst_base + FOLDER_SUFFIX)

    # validate more
    if dst == src:
        return 1  # dst may be changed

    # parse text
    text_lines = []
    # read src file
    with codecs.open(src, 'r', encoding='utf-8') as f:
        header = None
        title_line_no = 0
        for i, line in enumerate(f):
            if header is None and line.strip() == '':
                # trim blank lines at the beginning / before header lines
                title_line_no += 1
                continue
            else:
                if header is None and line.startswith('---'):
                    # header begins
                    title_line_no += 1
                    header = True
                elif header:
                    # header ends
                    title_line_no += 1
                    if line.startswith('---'):
                        header = False
                else:
                    # after header lines
                    header = False
                    if i == title_line_no:
                        if line.strip() == '':
                            # skip blank lines after title
                            title_line_no += 1
                        else:
                            # title line if applicable
                            line = line.replace(src_base, dst_base)
                    else:
                        # normal lines
                        line = re.sub(link_re_pattern,
                                      lambda match: replace_match(match,
                                                                  src_base, dst_base),
                                      line)
            text_lines.append(line)

    # write dst file
    with codecs.open(dst, 'w', encoding='utf-8') as f:
        f.writelines(text_lines)

    # copy folder
    if os.path.exists(src_folder) and os.path.isdir(src_folder):
        # metadata is copied as well
        shutil.copytree(src_folder, dst_folder)

    return 0  # dst may be changed


def replace_match(match, old_str, new_str):
    src_base_quoted = urllib_parse.quote(old_str.encode('utf-8'))
    if match.group(2) == old_str or match.group(2) == src_base_quoted:
        return match.group(1) + new_str + match.group(3)
    else:
        return match.group(0)


def main():
    if len(sys.argv) == 3:
        try:
            markdown_src = sys.argv[1]
            markdown_dst = sys.argv[2]
            note_copy(markdown_src, markdown_dst)
            return 0
        except Exception as e:
            print(e)
    else:
        print('usage: note-cp <source_file> <target_file>\n'
              '       note-cp <source_file> <target_directory>')
    return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
