# -*- mode: python -*-

block_cipher = None


a = Analysis(['DragonShout.py'],
             pathex=[],
             binaries=[],
             datas=[('ressources', 'ressources'),('dragonShout.png','.'), ('dragonShout.ico','.'), ('License.txt','.')],
             hiddenimports=['PyQt5','PyQt5.sip'],
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
          name='DragonShout',
          icon='DragonShout\\dragonShout.ico',
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
               name='main')
