from cx_Freeze import setup, Executable

executables = [Executable('main.py', targetName='game.exe')]

excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib',
            'unicodedata', 'bz2', 'select']

# zip_include_packages = ['pygame', 'random', 'math', 'time']

includes = ['pygame']

include_files = ['src', 'stats.db']

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'excludes': excludes,
        'include_files': include_files,
        # 'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',

    }
}

setup(name='DungeonMaster',
      version='alpha 1.1.5',
      description='',
      executables=executables,
      options=options)
