#!/usr/bin/env python
# coding:utf-8
"""
authors: gening
date:    2017-06-07 13:48:26
version: 1.1.0
desc:    download online images within a markdown file and save to a local folder.
usage:   ./note_offline.py <md_file_name>
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import imghdr
import os
import re
import shutil
import sys
import time

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
from markdown_note.note_lib import FOLDER_SUFFIX
from markdown_note.note_lib import SUPPORT_EXT_LIST
from markdown_note.note_lib import TRASH_DIR
from markdown_note.note_lib import TIMESTAMP_FORMAT
from markdown_note.note_lib import parse_file_name
from markdown_note.note_lib import create_new_folder
from markdown_note.note_lib import clean_empty_folder
from markdown_note.note_lib import str_decode_utf8
from markdown_note.note_lib import get_url_data

# ![abc](http://www.xyz.com/123.jpg)
# group(1) = http://www.xyz.com/123.jpg
image_regex = re.compile('!\[.*?\]\((http.+?)\)')


def note_offline(filename):
    # validate filename name
    if not os.path.exists(filename):
        raise Exception('%s: No such file' % filename)
    # create folder
    dir_path, base_name, ext_name = parse_file_name(filename)
    if ext_name not in SUPPORT_EXT_LIST:
        raise Exception('UNKNOWN FILE TYPE')
    folder_name = base_name + FOLDER_SUFFIX
    create_new_folder(os.path.join(dir_path, folder_name))

    # parse text
    text_lines = []
    # read original filename
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        map_url_to_name = dict()
        for line in f:
            # extract image url
            line_builder = []
            pos_begin = 0
            for match in image_regex.finditer(line):
                img_url = match.group(1)
                if img_url not in map_url_to_name:
                    img_data = download_image(img_url)
                    img_number = len(map_url_to_name) + 1
                    img_type = imghdr.what(None, h=img_data)
                    img_name = 'image' + '_' + str(img_number) + '.' + img_type
                    save_image(img_data, os.path.join(dir_path, folder_name, img_name))
                    map_url_to_name[img_url] = img_name
                else:
                    img_name = map_url_to_name[img_url]
                # replace image url
                pos_end = match.start(1)
                line_builder.append(line[pos_begin: pos_end])
                line_builder.append(folder_name + '/' + img_name)
                pos_begin = match.end(1)
            # the rest of the line
            line_builder.append(line[pos_begin:])
            # output the result
            text_lines.append(''.join(line_builder))

    # move original filename to Trash
    # use time stamp to resolve the filename conflict in Trash
    time_str = time.strftime(TIMESTAMP_FORMAT, time.localtime())
    # os.rename works only if source and destination are on the same volume.
    # using shutil.move instead.
    shutil.move(filename, os.path.join(TRASH_DIR, base_name + ext_name + '_' + time_str + ext_name))

    # write new filename
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.writelines(text_lines)

    # clean folder
    clean_empty_folder(os.path.join(dir_path, folder_name), warning=False)


# import requests  # http://docs.python-requests.org/
# def download_image(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         image_data = response.content
#         return image_data
#     else:
#         raise Exception('INTERNET DISCONNECTED')


def download_image(url):
    return get_url_data(url)


def save_image(image_data, image_file):
    with codecs.open(image_file, 'wb') as f:
        f.write(image_data)


def main():
    if len(sys.argv) == 2:
        try:
            markdown_file = str_decode_utf8(sys.argv[1])
            note_offline(markdown_file)
            return 0
        except Exception as e:
            print(e)
    else:
        print('usage: note-offline <file>')
    return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
