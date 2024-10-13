# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['home_screen.py'],
    pathex=[],
    binaries=[],
    datas=[('media', 'media'), ('Venora-G36PO.otf', '.'), ('background-ezgif.com-gif-to-sprite-converter.png', '.'), ('endgamebackground.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='home_screen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['media/tron-icon.icns'],
)
app = BUNDLE(
    exe,
    name='home_screen.app',
    icon='media/tron-icon.icns',
    bundle_identifier=None,
)
