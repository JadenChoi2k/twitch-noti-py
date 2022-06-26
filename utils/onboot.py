import sys
import win32com.client
import winshell
import os
DEFAULT_FILE_NAME = "twitch-notipy.lnk"


# returns sys.executable if exists or just returns given path
def get_current_path(path=None):
    if getattr(sys, 'frozen', False):  # --one-file
        return sys.executable
    return path


def create_lnk(targetpath=None, filename=DEFAULT_FILE_NAME):
    target = get_current_path(targetpath)
    dest = os.path.join(winshell.startup(), filename)
    # start
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(dest)
    shortcut.Targetpath = target
    shortcut.save()


def delete_lnk(filename=DEFAULT_FILE_NAME):
    st_path = winshell.startup()
    rm_file = os.path.join(st_path, filename)
    if os.path.isfile(rm_file):
        os.remove(rm_file)


if __name__ == '__main__':
    create_lnk(__file__)
    delete_lnk()
