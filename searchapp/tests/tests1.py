from django.test import TestCase

from searchapp.models import GoodsTBL
from searchapp.forms import SizeForm
from searchapp.forms import ColorForm
from searchapp.views import DetailsListView


class GoodsTBLModelTests(TestCase):
    def test_is_empty(self):
        '''
        何も登録しなければ保存されたレコード数は0個
        '''
        saved_GoodsTBL = GoodsTBL.objects.all()
        self.assertEqual(saved_GoodsTBL.count(), 0)


class SizeFormTests(TestCase):
    '''
    Sizeformクラスのテスト
    '''
    def test_valid(self):
        '''
        SizeForm1.正常に入力した場合にエラーにならないことを検証する
        '''
        parmas = []
        parmas.append(('S','S'))
        form = SizeForm(szchoice=parmas)
        self.assertTrue(form.is_valid())

    def test_either1(self):
        '''
        SizeForm2.何も入力していない場合にエラーとなることを検証する
        '''
        parmas = dict()
        form = SizeForm(parmas)
        self.assertTrue(form.is_valid())

class ColorFormTests(TestCase):
    '''
    Colorformクラスのテスト
    '''
    def test_valid(self):
        '''
        ColorForm1.正常に入力した場合にエラーにならないことを検証する
        '''
        parmas = {'赤':'赤','黒':'黒'}
        form = ColorForm(clchoice=parmas)
        self.assertTrue(form.is_valid())

    def test_either1(self):
        '''
        ColorForm2.何も入力していない場合にエラーとなることを検証する
        '''
        parmas = dict()
        form = ColorForm(parmas)
        self.assertTrue(form.is_valid())

    def test_either2(self):
        '''
        ColorForm3.正常に入力した場合にエラーにならないことを検証する
        '''
        parmas = dict(color='赤')
        form = ColorForm(parmas)
        self.assertTrue(form.is_valid())