import ctypes
import sys
import winreg
from pathlib import WindowsPath
from win32com.client import Dispatch
def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    params = f'"{sys.executable}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
def check_registry_key(key_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, winreg.KEY_READ)
        winreg.CloseKey(key)
        print(f"The key {key_path} exists in the registry.")
        return True
    except FileNotFoundError:
        print(f"The key {key_path} does not exist in the registry.")
        return False


def append_path_env(path_str:str):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
    cur_path_env:str = winreg.QueryValueEx(key, "Path")[0]
    path = WindowsPath(path_str)
    for i in cur_path_env.split(";"):
        if WindowsPath(i) == path:
            winreg.CloseKey(key)
            return
    new_path_env = ";".join([cur_path_env, str(WindowsPath(path_str))])
    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_env)
    winreg.CloseKey(key)



