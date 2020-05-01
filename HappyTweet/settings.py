import sys

try: 
    from HappyTweet.settings_module.local_settings import *
except ImportError:
    print('''
    copy
        <root>/HappyTweet/settings_module/local_settings.examplepy
    into 
        <root>/HappyTweet/settings_module/local_settings.py
    ...
    ''')
    sys.exit()