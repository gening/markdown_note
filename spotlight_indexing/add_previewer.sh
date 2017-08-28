#!/usr/bin/env bash
# coding: utf-8
# author: gening
# date:   2017-08-28 21:00:00
# desc:   Support QuickLook preview of Markdown content in Finder
#         * Add quick look（Using discount C library to render markdown）
#         https://github.com/toland/qlmarkdown/releases (accessed 30 Nov 2015)
#         see also: http://mdk.org.pl/2009/2/10/quicklook-for-markdown

# set parameters to capture the necessary errors
set -ue
set -o pipefail

# Add quick look

# params
quicklook_lib_dir="/Library/QuickLook"

# unzip
cd "$( dirname "${BASH_SOURCE[0]}" )"
echo "macOS system permission required!"
sudo unzip QLMarkdown.qlgenerator.zip -d ${quicklook_lib_dir}

# refresh 
qlmanage -r

# list
# qlmanage -m plugins
