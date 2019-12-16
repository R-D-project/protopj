#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # 開発と商用(AWS)で動作するsettingsファイルを分ける。
    # 動作環境に合わせて有効化（コメント解除）する。
    # local：ローカル端末で直接動かす場合の設定ファイル
    # aws_local：AWS上でDebugモードTrue(Djangoサーバ使用）で動かす場合の設定ファイル
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.aws_local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
