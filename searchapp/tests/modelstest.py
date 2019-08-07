'''
modelsのテストケースを記述
    今回は各モデルのレコード追加、変更、削除処理はdjango標準機能である、
    admin画面で実施するため、追加、変更、削除のエラーケースは対象外とする。
'''
from django.test import TestCase
from django.test.utils import override_settings
from django.db import IntegrityError
from django.db import transaction
from searchapp.models import GoodsTBL
from searchapp.models import CategoryTBL
from searchapp.models import HighCategoryTBL


class HighCategoryTBLModelTests(TestCase):
    '''
    モデル「HighCategoryTBL」のテストケース
    '''

    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行

    def test_is_empty(self):
        '''
        何も登録しなければ保存されたレコード数は0件
        '''
        saved_highcategorytbl = HighCategoryTBL.objects.all()
        self.assertEqual(saved_highcategorytbl.count(), 0)

    def test_is_not_empty(self):
        '''
        1件登録した場合、保存されたレコード数は1件
        '''
        high_cate = HighCategoryTBL(highcategoryid='category01')
        high_cate.save()
        saved_highcategorytbl = HighCategoryTBL.objects.all()
        self.assertEqual(saved_highcategorytbl.count(), 1)

    def test_is_attribute(self):
        '''
        想定した属性以外の値をエラーにしているか
        '''
        high_cate = HighCategoryTBL()
        ck_num_hcate_id = int(1234567890)
        ck_hcate_id = '1234567890'
        ck_hcate_name = '衣類'
        high_cate.highcategoryid = ck_hcate_id
        high_cate.highcategoryname = ck_hcate_name
        high_cate.save()

        saved_highcate = HighCategoryTBL.objects.all()
        actual_hcate = saved_highcate[0]
        # 上位カテゴリーIDが数値ではないことを確認する。
        self.assertNotEqual(actual_hcate.highcategoryid, ck_num_hcate_id,
                            '上位カテゴリーＩＤの属性が想定(文字列)と異なっています。')
        # 上位カテゴリー名が文字列であることを確認する。
        self.assertEqual(actual_hcate.highcategoryname, ck_hcate_name,
                         '上位カテゴリー名の属性が想定(文字列)と異なっています。')
        # 上位カテゴリーIDが文字列であることを確認する。
        self.assertEqual(actual_hcate.highcategoryid, ck_hcate_id,
                         '上位カテゴリーＩＤの属性が想定(文字列)と異なっています。')

class CategoryTBLModelTests(TestCase):
    '''
    モデル「CategoryTBL」のテストケース
    '''

    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行

    def test_is_empty(self):
        '''
        何も登録しなければ保存されたレコード数は0件
        '''
        saved_categorytbl = CategoryTBL.objects.all()
        # 何も登録していないため、レコード数は0件であることを確認する。
        self.assertEqual(saved_categorytbl.count(), 0)

    def test_is_not_empty(self):
        '''
        1件登録した場合、保存されたレコード数は1件
        '''
        #上位カテゴリＩＤの外部キーである、上位カテゴリマスタを追加
        high_cate = HighCategoryTBL(highcategoryid='category01')
        high_cate.save()
        cate = CategoryTBL(categoryid='category01A01',
                           highcategoryid=high_cate)
        cate.save()
        saved_categorytbl = CategoryTBL.objects.all()
        # 1件登録したら、レコード数は1件であることを確認する。
        self.assertEqual(saved_categorytbl.count(), 1)


class GoodsTBLModelTests(TestCase):
    '''
    モデル「GoodsTBL」のテストケース
    '''

    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行

    def test_is_empty(self):
        '''
        DBアクセス検証
        何も登録しなければ保存されたレコード数は0件
        '''
        saved_goodstbl = GoodsTBL.objects.all()
        self.assertEqual(saved_goodstbl.count(), 0)

    def test_is_not_empty(self):
        '''
        1件登録した場合、保存されたレコード数は1件
        '''
        # 各マスタのレコード追加準備
        high_cate = HighCategoryTBL(highcategoryid='category01')
        cate = CategoryTBL(categoryid='category01A01',
                           highcategoryid=high_cate)
        goods = GoodsTBL(goodsid='product01S001', productno='product01',
                         sizename='S', colorname='黒',
                         categoryid=cate, price='4500',
                         goodsstocks='50', salesstartdate='2019-07-29',
                         deleteflag='0')
        # 各マスタのレコード追加
        high_cate.save()
        cate.save()
        goods.save()
        # 全件取得
        saved_highcate = HighCategoryTBL.objects.all()
        saved_cate = CategoryTBL.objects.all()
        saved_goodstbl = GoodsTBL.objects.all()
        # 取得した件数が1件か判定
        self.assertEqual(saved_highcate.count(), 1)
        self.assertEqual(saved_cate.count(), 1)
        self.assertEqual(saved_goodstbl.count(), 1)

    def test_is_num_attribute(self):
        '''
        数値型のレコード(価格と在庫数)に文字列型の数字を入れた場合のチェック
        '''
        # 各マスタのレコード追加準備
        high_cate = HighCategoryTBL(highcategoryid='category01')
        cate = CategoryTBL(categoryid='category01A01',
                           highcategoryid=high_cate)
        goods = GoodsTBL(goodsid='product01S001', productno='product01',
                         sizename='S', colorname='黒',
                         categoryid=cate, price='4500',
                         goodsstocks='50', salesstartdate='2019-07-29',
                         deleteflag='0')
        # 各マスタのレコード追加
        high_cate.save()
        cate.save()
        goods.save()
        # 全件取得
        saved_goodstbl = GoodsTBL.objects.all()
        actual_goods = saved_goodstbl[0]

        # 価格、在庫数の属性判定
        self.assertEqual(actual_goods.price, int(4500), '価格の属性が想定(数値)と異なっています。')
        self.assertEqual(actual_goods.goodsstocks, int(50), '在庫数の属性が想定(数値)と異なっています。')
        self.assertNotEqual(actual_goods.price, '4500', '価格の属性は文字列ではありません')
        self.assertNotEqual(actual_goods.goodsstocks, '50', '在庫数の属性は文字列ではありません')

    def test_is_duplicate(self):
        '''
        商品ＩＤは異なるが、製品番号、サイズ、色が全て一緒のデータが
        登録できないことを確認
        '''
        # 各マスタのレコード追加準備
        high_cate = HighCategoryTBL(highcategoryid='category01')
        cate = CategoryTBL(categoryid='category01A01',
                           highcategoryid=high_cate)
        goods1 = GoodsTBL(goodsid='product01S001', productno='product01',
                          sizename='S', colorname='黒',
                          categoryid=cate, price='4500',
                          goodsstocks='50', salesstartdate='2019-07-29',
                          deleteflag='0')
        goods2 = GoodsTBL(goodsid='product10S001', productno='product01',
                          sizename='S', colorname='黒',
                          categoryid=cate, price='4500',
                          goodsstocks='50', salesstartdate='2019-07-29',
                          deleteflag='0')
        # 各マスタのレコード追加
        high_cate.save()
        cate.save()
        goods1.save()
        # 商品マスタで、製品番号、サイズ、色がGoods1で定義した値と同等であり、
        # 商品ＩＤのみ異なる場合、レコード作成できるかチェックする。（出来ない想定)
        try:
            with transaction.atomic():
                goods2.save()
        except IntegrityError:  # 重複エラーとなった場合の処理
            pass  # 何もしない

        # 全件取得
        saved_highcate = HighCategoryTBL.objects.all()
        saved_cate = CategoryTBL.objects.all()
        saved_goodstbl = GoodsTBL.objects.all()
        # 取得した件数が1件か判定
        self.assertEqual(saved_highcate.count(), 1, '格納件数が想定と異なっています。')
        self.assertEqual(saved_cate.count(), 1, '格納件数が想定と異なっています。')
        # 重複したデータを追加し用としているが、エラーで追加されていないことをレコード数で確認する。
        self.assertEqual(saved_goodstbl.count(), 1, '格納件数が想定と異なっています。')
