'''
accountsアプリのソースコードファイル
'''
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from .forms import LoginForm


class Login(LoginView):
    '''ログインページ'''
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LogoutView):
    '''ログアウト時の処理'''

    def get_next_page(self):
        '''
        ログアウト後に遷移するページを設定するメソッド（親クラスのメソッドをオーバーライド）
        子ではフラッシュメッセージに表示する文字列を定義している。
        '''
        message = 'ログアウトしました'
        messages.info(self.request, message)
        return super().get_next_page()
