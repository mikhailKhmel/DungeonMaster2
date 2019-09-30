# coding: utf-8
from cx_Freeze import setup, Executable

executables = [Executable('main.py', targetName='game.exe')]

excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib',
            'bz2', 'select', 'socket']

includes = ['pygame']

include_files = ['src', 'stats.db']

options = {
    'build_exe': {
        # 'include_msvcr': True,
        'includes': includes,
        'excludes': excludes,
        'include_files': include_files,
        # 'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',

    }
}

setup(name='DungeonMaster',
      version='alpha 1.4.1',
      description='',
      executables=executables,
      options=options)

# from distutils.core import setup
# import entities, genmaps, render
# import py2exe
#
# setup(console=['main.py'], options={
#     'py2exe': {
#         'packages': ['pygame']
#     }
# })
