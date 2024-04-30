REG_DATA = {
    r'ExampleCsPlugin.MyPlugin': {
        '': 'ExampleCsPlugin.MyPlugin'
    },
    r'ExampleCsPlugin.MyPlugin\CLSID': {
        '': '{GUID}'
    },
    r'CLSID\{GUID}': {
        '': 'ExampleCsPlugin.MyPlugin'
    },
    r'CLSID\{GUID}\InprocServer32': {
        '': 'mscoree.dll',
        'ThreadingModel': 'Both',
        'Class': 'ExampleCsPlugin.MyPlugin',
        'Assembly': 'ExampleCsPlugin, Version=1.1.0.0, Culture=neutral, PublicKeyToken=null',
        'RuntimeVersion': 'v4.0.30319',
        'CodeBase': 'file:///C:/Program Files (x86)/Default Company Name/svn_plugin/ExampleCsPlugin.dll'#插件dll位置
    },
    r'CLSID\{GUID}\InprocServer32\1.1.0.0': {
        "Class": "ExampleCsPlugin.MyPlugin",
        "Assembly": "ExampleCsPlugin, Version=1.1.0.0, Culture=neutral, PublicKeyToken=null",
        "RuntimeVersion": "v4.0.30319",
        "CodeBase": "file:///C:/Program Files (x86)/Default Company Name/svn_plugin/ExampleCsPlugin.dll", #插件dll位置
    },
    r'CLSID\{GUID}\ProgId': {
        "": "ExampleCsPlugin.MyPlugin"
    },
    r'CLSID\{GUID}\Implemented Categories\{62C8FE65-4EBB-45E7-B440-6E39B2CDBF29}': {},
    r'CLSID\{GUID}\Implemented Categories\{3494FA92-B139-4730-9591-01135D5E7831}': {},
    # ...
}

CONFIG_DATA = {
    "version" : "1.0.0",
    "check":"1",
}