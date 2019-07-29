from django.test import TestCase
from searchapp.models import GoodsTBL
from searchapp.models import CategoryTBL
from searchapp.models import HighCategoryTBL
from searchapp.forms import SizeForm
from searchapp.forms import ColorForm
from searchapp.views import DetailsListView


class HighCategoryTBLModelTests(TestCase):
    '''
    モデル「HighCategoryTBL」のテストケース
    '''
    def test_is_empty(self):
        '''
        何も登録しなければ保存されたレコード数は0件
        '''
        saved_HighCategoryTBL = HighCategoryTBL.objects.all()
        self.assertEqual(saved_HighCategoryTBL.count(),0)

    def test_is_not_empty(self):
        '''
        1件登録した場合、保存されたレコード数は1件
        '''
        HighCate = HighCategoryTBL(highcategoryid='highcate0001')
        HighCate.save()
        saved_HighCategoryTBL = HighCategoryTBL.objects.all()
        self.assertEqual(saved_HighCategoryTBL.count(), 1)

    def test_tyouhuku(self):
        '''
        登録するHighCategoryidが重複している場合エラーとなること
        '''

class CategoryTBLModelTests(TestCase):
    '''
    モデル「CategoryTBL」のテストケース
    '''
    def test_is_empty(self):
        '''
        何も登録しなければ保存されたレコード数は0件
        '''
        saved_CategoryTBL = CategoryTBL.objects.all()
        self.assertEqual(saved_CategoryTBL.count(),0)

    def test_is_not_empty(self):
        '''
        1件登録した場合、保存されたレコード数は1件
        '''
        table = CategoryTBL()
        table.save()
        saved_CategoryTBL = CategoryTBL.objects.all()
        self.assertEqual(saved_CategoryTBL.count(), 1)


class GoodsTBLModelTests(TestCase):
    '''
    モデル「GoodsTBL」のテストケース
    '''
    def test_is_empty(self):
        '''
        DBアクセス検証
        何も登録しなければ保存されたレコード数は0件
        '''
        saved_GoodsTBL = GoodsTBL.objects.all()
        self.assertEqual(saved_GoodsTBL.count(), 0)

    def test_is_not_empty(self):
        '''
        1件登録した場合、保存されたレコード数は1件
        '''
        HighCate = HighCategoryTBL(highcategoryid='highcate0001')
        Cate = CategoryTBL(categoryid='category00001',
                           highcategoryid=HighCate)
        Goods = GoodsTBL(goodsid='AABBCC001S001', productno='AABBCC001',
                         sizename='S', colorname='red',
                         categoryid=Cate)
        HighCate.save()
        Cate.save()
        Goods.save()
        saved_HighCate = HighCategoryTBL.objects.all()
        saved_Cate = CategoryTBL.objects.all()
        saved_GoodsTBL = GoodsTBL.objects.all()
        self.assertEqual(saved_HighCate.count(),1)
        self.assertEqual(saved_Cate.count(),1)
        self.assertEqual(saved_GoodsTBL.count(), 1)
