'''
入力フォームの設定ファイル

'''
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    '''ログインフォーム'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 使用するclassを定義する。
            field.widget.attrs['class'] = 'form-control'
            # placeholder(入力欄に初期表示する内容)を定義する。
            field.widget.attrs['placeholder'] = field.label
