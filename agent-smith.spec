# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['agent-smith.py'],
    pathex=[],
    binaries=[],
    datas=[('./application/gui/resources/agent-white.png', './application/gui/resources'), ('./application/source/games/*.py', './application/source/games'), ('./application/source/games/resources/*', './application/source/games/resources'), ('./application/source/alembic/alembic.ini', './application/source/alembic'), ('./application/source/alembic/env.py', './application/source/alembic'), ('./application/source/alembic/script.py.mako', './application/source/alembic'), ('./application/source/alembic/versions/*.py', './application/source/alembic/versions')],
    hiddenimports=['xml.etree.ElementTree', 'telnetlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='agent-smith',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['application\\gui\\resources\\agent-black.ico'],
)
