#!/usr/bin/env bash
# coding: utf-8
# author: gening
# date:   2017-08-28 21:00:00
# desc:   Fix Spotlight indexing of Markdown content
#         * Add spotlight indexing （Using Apple's importer for text）
#         http://brettterpstra.com/2011/10/18/fixing-spotlight-indexing-of-markdown-content/

# set parameters to capture the necessary errors
set -ue
set -o pipefail

# Add spotlight indexing

# params
spotlight_lib_dir="/Library/Spotlight"

# unzip
cd "$( dirname "${BASH_SOURCE[0]}" )"
echo "macOS system permission required!"
sudo unzip Markdown.mdimporter.zip Markdown.mdimporter/* -d ${spotlight_lib_dir}

# import 
mdimport -r ${spotlight_lib_dir}/Markdown.mdimporter

# list
# mdimport -L