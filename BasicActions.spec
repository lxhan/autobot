# -*- mode: python -*-

block_cipher = None


a = Analysis(['BasicActions.py'],
             pathex=['C:\\Users\\ALEX\\PycharmProjects\\AutoBot'],
             binaries=[('C:\\Users\\ALEX\\PycharmProjects\\AutoBot\\chromedriver.exe', '.')],
             datas=[('C:\\Users\\ALEX\\PycharmProjects\\AutoBot\\chromedriver.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='BasicActions',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='AutoBot')
