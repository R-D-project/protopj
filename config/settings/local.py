"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 2.1.9.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 開発時はTrue,商用提供時はFalse

ALLOWED_HOSTS = ['*']  # デバックモードがFalseの時に設定要

# ローカルPC用のデータベース定義
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'protodb',
        'USER': 'root',
        'PASSWORD': 'rootpassword',  # ローカル端末にインストールしたときのパスワード
        'HOST': 'localhost',
        'PORT': '3306',
        # トランザクションの有効範囲をリクエストの開始から終了までに設定
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            # 桁溢れの登録時にエラー（厳密モード）
            'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO',
            },
    }
}

# ログ出力機能
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# デバックモードがFalseの時に有効化
# セッションの設定
# SESSION_COOKIE_AGE = 600  # 10分
# SESSION_SAVE_EVERY_REQUEST = True  # 1リクエストごとにセッション情報更新


# django-nose, coverage configure
INSTALLED_APPS += ('django_nose',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',  # coverage を取る
    '--cover-html',  # coverage を html で cover/ に出力する
    # coverage を取得する対象アプリ名を定義する。
    '--cover-package=searchapp,accounts',
]

if DEBUG:
    def show_toolbar(request):
        return True

    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }
