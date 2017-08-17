# coding: utf-8
"""
authors: gening
date:    2017-08-16 16:27:58
version: 1.0.0
desc:

"""
import os
import sys
import threading

# noinspection PyUnresolvedReferences,PyPackageRequirements
import sublime
# noinspection PyUnresolvedReferences,PyPackageRequirements
import sublime_plugin

# from note_side_bar.markdown_note import note_lib  # It works.
# from note_side_bar import note   # It doesn't work due to import in note.py.
sys.path.append(os.path.split(os.path.abspath(__file__))[0])
from markdown_note import note
from markdown_note import note_lib


class NoteSideBarCommand(sublime_plugin.WindowCommand):
    def copy_to_clipboard_and_inform(self, data):
        sublime.set_clipboard(data)
        self.window.status_message('Copied "{}" to clipboard'.format(data))

    def get_path(self, paths):
        try:
            return paths[0]
        except IndexError:
            return self.window.active_view().file_name()

    def is_visible(self, paths):
        if paths:
            # noinspection PyBroadException
            try:
                if len(paths) == 1:
                    for ext in note_lib.SUPPORT_EXT_LIST:
                        if paths[0].endswith(ext):
                            return True
            except Exception:
                pass
            return False
        return bool(self.window.active_view().file_name())


class NoteSideBarSingleFileCommand(NoteSideBarCommand):
    def __init__(self, sublime_window, desc='', func=None):
        self.desc = desc
        self.func = func
        super(NoteSideBarSingleFileCommand, self).__init__(sublime_window)

    def run(self, paths):
        path = self.get_path(paths)
        try:
            if self.func:
                self.func(path)
        except OSError as error:
            self.window.status_message('Error: {error}'.format(error=error))

    def description(self):
        return self.desc


class NoteSideBarRemoveCommand(NoteSideBarSingleFileCommand):
    def __init__(self, sublime_window):
        desc = 'Note remove'
        func = note.remove
        super(NoteSideBarRemoveCommand, self).__init__(sublime_window, desc, func)


class NoteSideBarOfflineCommand(NoteSideBarSingleFileCommand):
    def __init__(self, sublime_window):
        desc = 'Note offline'
        func = note.offline
        super(NoteSideBarOfflineCommand, self).__init__(sublime_window, desc, func)


class NoteSideBarMkdirCommand(NoteSideBarSingleFileCommand):
    def __init__(self, sublime_window):
        desc = 'Note mkdir'
        func = note.mkdir
        super(NoteSideBarMkdirCommand, self).__init__(sublime_window, desc, func)


class NoteSideBarRmdirCommand(NoteSideBarSingleFileCommand):
    def __init__(self, sublime_window):
        desc = 'Note rmdir'
        func = note.rmdir
        super(NoteSideBarRmdirCommand, self).__init__(sublime_window, desc, func)


class NoteSideBarOpendirCommand(NoteSideBarSingleFileCommand):
    def __init__(self, sublime_window):
        desc = 'Note opendir'
        func = note.opendir
        super(NoteSideBarOpendirCommand, self).__init__(sublime_window, desc, func)


class NoteSideBarDoubleFilesCommand(NoteSideBarCommand):
    def __init__(self, sublime_window, desc='', tip='', func=None):
        self.desc = desc
        self.tip = tip
        self.func = func
        super(NoteSideBarDoubleFilesCommand, self).__init__(sublime_window)
        self.source = None

    def run(self, paths):
        self.source = self.get_path(paths)
        dir_path, base, ext = note_lib.parse_file_name(self.source)
        initial_text = os.path.join(dir_path, base + ext)
        input_panel = self.window.show_input_panel(
            self.tip, initial_text, self.on_done, None, None)
        input_panel.sel().clear()  # selection
        input_panel.sel().add(sublime.Region(len(dir_path) + 1, len(dir_path) + 1 + len(base)))

    def on_done(self, destination):
        source = self.source
        if self.func:
            threading.Thread(target=self.do,
                             args=(source, destination)
                             ).start()

    def do(self, source, destination):
        self.window.status_message(self.tip + destination)
        try:
            if self.func:
                self.func(source, destination)
        except OSError as error:
            self.window.status_message('Error: {error}'.format(error=error))
        self.window.run_command('refresh_folder_list')

    def description(self):
        return '%s ...' % self.desc


class NoteSideBarCopyCommand(NoteSideBarDoubleFilesCommand):
    def __init__(self, sublime_window):
        desc = 'Note copy'
        tip = 'Copy as: '
        func = note.copy
        super(NoteSideBarCopyCommand, self).__init__(sublime_window, desc, tip, func)


class NoteSideBarMoveCommand(NoteSideBarDoubleFilesCommand):
    def __init__(self, sublime_window):
        desc = 'Note move'
        tip = 'Move to: '
        func = note.move
        super(NoteSideBarMoveCommand, self).__init__(sublime_window, desc, tip, func)
