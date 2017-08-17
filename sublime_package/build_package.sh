#!/usr/bin/env bash
# coding: utf-8
# author: gening
# date:   2017-08-16 21:09:27
# desc:

# set parameters to capture the necessary errors
set -ue
set -o pipefail

# params
sublime_package_dir="${HOME}/Library/Application Support/Sublime Text 3/Installed Packages/"

# build package
cd "$( dirname "${BASH_SOURCE[0]}" )"
rm note_side_bar.sublime-package.zip || echo "building note_side_bar.sublime-package"
zip -r note_side_bar.sublime-package.zip note_side_bar.py "Side Bar.sublime-menu"
cd ..
zip -r ./sublime_package/note_side_bar.sublime-package.zip markdown_note/*.py

# reload package
cp ./sublime_package/note_side_bar.sublime-package.zip "${sublime_package_dir}"  # due to whitespace in the path
rm "${sublime_package_dir}/note_side_bar.sublime-package" || echo "reloading note_side_bar.sublime-package"
sleep 1s  # wait
mv "${sublime_package_dir}/note_side_bar.sublime-package.zip" "${sublime_package_dir}/note_side_bar.sublime-package"