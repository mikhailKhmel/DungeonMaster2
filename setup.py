from cx_Freeze import setup, Executable

executables = [Executable('main.py', targetName='game.exe')]

# excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib', 'xml',
#             'unicodedata', 'bz2', 'select']

# zip_include_packages = ['collections', 'encodings', 'importlib', 'wx']

includes = ['pygame']

include_files = ['src']

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        # 'excludes': excludes,
        # 'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='DungeonMaster',
      version='alpha 1.1.4',
      description='',
      executables=executables,
      options=options)