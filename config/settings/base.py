"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 2.1.9.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = プロジェクトのpath
# PROJECT_NAME = プロジェクトの名前

# フォルダ階層を1つ落としたのでBASE_DIRの位置を1つ上にする
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_NAME = os.path.basename(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=zjgip(+y7x$z6sk-(n+u=0^8hkxkv$7!*0x0ip=*buld--v2c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 開発時はTrue,商用提供時はFalse

ALLOWED_HOSTS = ['*']  # デバックモードがFalseの時に設定要


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'searchapp.apps.SearchappConfig',  # アプリ紐付け
    'bootstrap4',  # bootstrap4紐付け
    'django.contrib.humanize',  # humanize紐付け(数値を3桁区切りにする際に使用する。)
]

# humanizeのappで指定可能。
# 数値を区切る桁数を設定する。
NUMBER_GROUPING = 3

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 初めに参照するURLCONFのルートパス設定
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # テンプレート探索優先ディレクトリ
        'APP_DIRS': True,  # アプリ名フォルダ直下探索有無
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# webサーバとwebアプリケーションを接続するためのインターフェイスを定義
WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# 今回はsqlite3を使用しないためコメント化
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

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

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

# パスワードのバリデーションチェック機能
AUTH_PASSWORD_VALIDATORS = [
    # 登録パスワードがusername,first_name,last_name,emailと類似していないかチェックする。
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator',
    },
    # minimumLengthValidator:パスワードの最小の長さを設定できる。
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator',
    },
    # CommonPasswordValidator:よくあるパスワードのリスト.txtと一致したらエラーを出す。
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator',
    },
    # NumericPasswordValidator:数値のみでパスワードが構成されていないかチェックする。
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator',
    },
]

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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# 言語をja(日本語)に設定する。
LANGUAGE_CODE = 'ja'

# 時間をAsia/Tokyo(日本)に設定する。(now等の時間取得で使用する)
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# デバックモードがFalseの時に有効化
STATIC_URL = '/static/'  # 静的ファイルの配信用ディレクトリ
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # 静的ファイルの置き場所
STATIC_ROOT = '/var/www/{}/static' .format(PROJECT_NAME)  # 静的ファイルの配信元

# セッションの設定
SESSION_COOKIE_AGE = 600  # 10分
SESSION_SAVE_EVERY_REQUEST = True  # 1リクエストごとにセッション情報更新

# django-nose, coverage configure
INSTALLED_APPS += ('django_nose',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',  # coverage を取る
    '--cover-html',  # coverage を html で cover/ に出力する
    # coverage を取得する対象アプリ名を定義する。
    '--cover-package=searchapp',
]