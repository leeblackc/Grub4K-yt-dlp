import sys

from PyInstaller.utils.hooks import collect_submodules, collect_data_files


def pycryptodome_module():
    try:
        import Cryptodome  # noqa: F401
    except ImportError:
        try:
            import Crypto  # noqa: F401
            print('WARNING: Using Crypto since Cryptodome is not available. '
                  'Install with: python3 -m pip install pycryptodomex', file=sys.stderr)
            return 'Crypto'
        except ImportError:
            pass
    return 'Cryptodome'


def get_hidden_imports():
    yield from ('yt_dlp.compat._legacy', 'yt_dlp.compat._deprecated')
    yield from ('yt_dlp.utils._legacy', 'yt_dlp.utils._deprecated')
    yield pycryptodome_module()
    # Only `websockets` is required, others are collected just in case
    for module in ('websockets', 'requests', 'urllib3'):
        yield from collect_submodules(module)
    # These are auto-detected, but explicitly add them just in case
    yield from ('mutagen', 'brotli', 'certifi', 'secretstorage', 'curl_cffi')


hiddenimports = list(get_hidden_imports())
print(f'Adding imports: {hiddenimports}')

excludedimports = ['youtube_dl', 'youtube_dlc', 'test', 'ytdlp_plugins', 'devscripts', 'bundle']

datas = collect_data_files('curl_cffi', includes=['cacert.pem'])


# Include JS challenge solver scripts
import os

# Add JS files from the jsc scripts directory
jsc_scripts_path = os.path.join('yt_dlp', 'extractor', 'youtube', 'jsc', '_builtin', 'vendor')
if os.path.exists(jsc_scripts_path):
    for file in os.listdir(jsc_scripts_path):
        if file.endswith('.js'):
            js_file_path = os.path.join(jsc_scripts_path, file)
            # Add the file to datas with the correct destination path
            dest_path = os.path.join('yt_dlp', 'extractor', 'youtube', 'jsc', '_builtin', 'vendor')
            datas.append((js_file_path, dest_path))
