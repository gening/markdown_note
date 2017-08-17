Shell Commands on Markdown Notes
================================

Manage a markdown file (`xxx.md`) and its attached files (`xxx_files`) in the same time.
The attached files are all included in the folder whose name has the suffix `_files` additionally to the file name itself under the same directory. For example:
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
  note mkdir <file>
  note rmdir <file>
  note opendir <file>
```

* note remove  = note rm =  note-rm:  

  > delete `xxx.md` file and `xxx_files` folder.

* note copy    = note cp =  note-cp:  

  > make a copy of `xxx.md` file with `xxx_files` folder.

* note move    = note mv =  note-mv:  

  > move or rename `xxx.md` file with `xxx_files` folder.

* note-offline:  

  > download images within `xxx.md` file into `xxx_files` folder.

* note-mkdir:  

  > make `xxx_files` folder attached to `xxx.md` file.

* note-rmdir:  

  > remove empty `xxx_files` folder detached to `xxx.md` file.

* note-opendir:  

  > open `xxx_files` folder attached to `xxx.md` file.  

  ​       
Installation
------------

This program has been tested in Python 3.6 and Python 2.7, and is compatible with Python 3.5-3.6 and Python 2.6-2.7.

No third party package required.

Ensure pip is already installed, then run: 

```shell
$ pip install ./markdown_note/
```

Once the installation has been done successfully, the shell-commands are available under $PATH.

Sublime Text Plugin
-------------------

This plugin has been tested in Sublime Text 3. 

1. Download Sublime plugin package (release 1.0.0):  [note_side_bar.sublime-package](docs/note_side_bar.sublime-package) 
2. Browse the folder of Sublime packages:  
   ![sublime_packages_browse](docs/sublime_packages_browse.png)
3. Copy the package into the folder `Installed Packages`:  
   ![sublime_packages_installed](docs/sublime_packages_installed.png)
4. Open Sublime Text app, and right click on a markdown file in the side bar:  
   ![sublime_plugin_screenshot](docs/sublime_plugin_screenshot.png)