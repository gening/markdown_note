#!/usr/bin/env bash
# coding: utf-8
# author: gening
# date:   2017-08-16 21:09:27
# desc:   Fixing Spotlight indexing of Markdown content
#         http://brettterpstra.com/2011/10/18/fixing-spotlight-indexing-of-markdown-content/

# set parameters to capture the necessary errors
set -ue
set -o pipefail

# params
spotlight_lib_dir="/Library/Spotlight"

# unzip
cd "$( dirname "${BASH_SOURCE[0]}" )"
echo "macOS system permission required!"
sudo unzip Markdown.mdimporter.zip Markdown.mdimporter/* -d ${spotlight_lib_dir}

# import 
mdimport -r ${spotlight_lib_dir}/Markdown.mdimporter

# list
mdimport -L


