'''
setting.pyのINSTALLED_APPに設定することで
アプリ内にあるmodelsやviewsを別アプリで呼び出しが可能となる。
'''
from django.apps import AppConfig


class SearchappConfig(AppConfig):
    '''
    アプリの設定を定義する。
    '''
    name = 'searchapp'
