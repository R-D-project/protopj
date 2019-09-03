'''
formのバリデーションチェック用ファイル
'''
from django.test import TestCase
from accounts.forms import LoginForm


class LoginFormTests(TestCase):
    '''
    フォーム「Loginform」のテストケース
    '''
    def test_valid(self):
        '''
        SizeForm1.正常に入力した場合にエラーにならないことを検証する
        '''
        parmas = []
        parmas.append(('admin', 'admin'))
        form = LoginForm(request=parmas)
        self.assertTrue(form.is_valid())

    def test_either1(self):
        '''
        SizeForm2.何も入力していない場合にエラーとなることを検証する
        '''
        parmas = dict()
        form = LoginForm(parmas)
        self.assertTrue(form.is_valid())
