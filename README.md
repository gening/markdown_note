Command Line on Markdown Note
==============================

Manage a markdown file (`xxx.md`) and its attached files (`xxx_files`) in the same time.
The attached files are all included in the folder whose name has the suffix `_files` 
additionally to the file name itself under the same directory. For example:
```
dir
├── note1.md
└── note1_files
    ├── image_1.jpg
    └── image_2.jpg
```

Usage
-----
```
  note <  rm  | cp | mv |offline> ...
  note <remove|copy|move|offline> ...
  note-rm <file>
  note-cp <source_file> <target_file>
  note-cp <source_file> <target_directory>
  note-mv <source_file> <target_file>
  note-mv <source_file> <target_directory>
  note-offline <file>
```

Operations
----------

*  note remove  = note rm =  note-rm: 
          delete `xxx.md` file and `xxx_files` folder.

* note copy    = note cp =  note-cp: 
         make a copy of `xxx.md` file with `xxx_files` folder.

* note move    = note mv =  note-mv: 
         move or rename `xxx.md` file with `xxx_files` folder.

* note-offline: 
         download images linked within `xxx.md` file into `xxx_files` folder.


Installation
------------

This program has been tested in Python 3.6 and Python 2.7, 
and is compatible with Python 3.x and Python 2.6-2.7.

Ensure pip is already installed, then run: 

```shell
$ pip install ./markdown_note/
```
pip will install the prerequisite package `six` and `requests` at the same time.

Once the installation has been done successfully, 
the shell-commands are available under $PATH.
