#!/usr/bin/env python
# coding:utf-8
"""
authors: gening
date:    2017-06-07 13:48:26
version: 1.1.1
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

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
from markdown_note.note_lib import FOLDER_SUFFIX
from markdown_note.note_lib import parse_file_name
from markdown_note.note_lib import str_decode_utf8
from markdown_note.note_lib import str_encode_base64

# ![abc](xxx_files/image_1.jpg)
# [abc](xxx_files/doc_1.pdf)
# group(1) = [abc](
# group(2) = xxx
# group(3) = _files/doc_1.pdf)
link_re_pattern = '(\[.*?\]\()(.*?)(_files/.*?\))'


def note_copy(src, dst):
    """copy note

    :return: 0 = not copied
             1 = shallow copied
             2 = deep copied
    """
    path_params_dict = get_path_params_dict(src, dst)

    # different type of copy
    if path_params_dict['dst'] == path_params_dict['src']:
        # not need to copy
        copy_type = 0
    elif path_params_dict['dst_base'] == path_params_dict['src_base']:
        # not need to rename, but need to move only
        copy_type = 1
        shallow_copy_file(path_params_dict)
        copy_folder(path_params_dict)
    else:
        # need to rename, and to move if required
        copy_type = 2
        deep_copy_file(path_params_dict)
        copy_folder(path_params_dict)
    return copy_type


def get_path_params_dict(src, dst):
    params_dict = dict()
    # validate and parse src file name
    # validate src file name
    if not os.path.exists(src):
        raise Exception('%s: No such file' % src)
    elif os.path.isdir(src):
        raise Exception('%s is a directory (skipped)' % src)
    # parse src file name
    src_dir, src_base, src_ext = parse_file_name(src)
    src_folder = os.path.join(src_dir, src_base + FOLDER_SUFFIX)

    # validate and parse dst file name
    # dst may be changed
    if os.path.exists(dst) and os.path.isfile(dst):
        # do not overwrite
        raise Exception('%s exists (not overwritten)' % dst)
    elif os.path.exists(dst) and os.path.isdir(dst):
        dst_dir, dst_base, dst_ext = dst, src_base, src_ext
        dst = os.path.join(dst_dir, dst_base + dst_ext)
    else:
        # parse dst file name
        dst_dir, dst_base, dst_ext = parse_file_name(dst, ignore_unsupported_ext=True)
        if dst_ext is None:
            dst_ext = src_ext
            dst = os.path.join(dst_dir, dst_base + dst_ext)
    dst_folder = os.path.join(dst_dir, dst_base + FOLDER_SUFFIX)

    # return the result
    params_dict['src'] = src
    params_dict['src_base'] = src_base
    params_dict['src_ext'] = src_ext
    params_dict['src_folder'] = src_folder
    params_dict['dst'] = dst
    params_dict['dst_base'] = dst_base
    params_dict['dst_ext'] = dst_ext
    params_dict['dst_folder'] = dst_folder
    return params_dict


def copy_folder(path_params_dict):
    src_folder = path_params_dict['src_folder']
    dst_folder = path_params_dict['dst_folder']
    if os.path.exists(src_folder) and os.path.isdir(src_folder):
        # metadata is copied as well
        shutil.copytree(src_folder, dst_folder)


def shallow_copy_file(path_params_dict):
    src = path_params_dict['src']
    dst = path_params_dict['dst']
    # metadata is copied as well
    shutil.copy2(src, dst)


def deep_copy_file(path_params_dict):
    src = path_params_dict['src']
    src_base = path_params_dict['src_base']
    dst = path_params_dict['dst']
    dst_base = path_params_dict['dst_base']
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


def replace_match(match, old_str, new_str):
    old_str_base64 = str_encode_base64(old_str)
    if match.group(2) == old_str or match.group(2) == old_str_base64:
        return match.group(1) + new_str + match.group(3)
    else:
        return match.group(0)


def main():
    if len(sys.argv) == 3:
        try:
            markdown_src = str_decode_utf8(sys.argv[1])
            markdown_dst = str_decode_utf8(sys.argv[2])
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
