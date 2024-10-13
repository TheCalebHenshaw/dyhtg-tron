from cx_Freeze import setup, Executable
import sys
import os

# Include necessary files and folders
include_files = [
    ('media', 'media')
]

# Base setting for the executable
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'  # Hides the console window on Windows

# Target executable
executables = [
    Executable(
        script='home_screen.py',  # Entry point of your application
        base=base,
        icon='icon.icns',  # Icon file (use .icns for macOS)
        target_name='tron'  # Output executable name
    )
]

# Setup configuration
setup(
    name='Tron',
    version='1.0',
    description='Simple Tron Game',
    options={
        'build_exe': {
            'include_files': include_files,
            'packages': ['pygame'],
            'include_msvcr': True,  # Include Microsoft Visual C++ Redistributable (Windows)
        }
    },
    executables=executables
)
