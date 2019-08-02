from django.test import TestCase
from django.test.utils import override_settings
from django.db import transaction
import logging
from django.urls import reverse
from searchapp.models import GoodsTBL
from searchapp.models import CategoryTBL
from searchapp.models import HighCategoryTBL
from searchapp.views import DetailsListView


def RecordAdd():
    '''
    各TBLに1件ずつデータを追加する。
    サイズ(S) 、色(黒)
    '''
    Hcate = HighCategoryTBL(highcategoryid='category01',
                            highcategoryname='衣類')
    Cate = CategoryTBL(categoryid='category01A01',
                       categoryname='スカート',
                       highcategoryid=Hcate)
    Goods1 = GoodsTBL(goodsid='product01S001',
                     categoryid=Cate,
                     productno='product01',
                     sizename='S',
                     colorname='黒',
                     price='4500',
                     goodsstocks='50',
                     salesstartdate='2019-07-29',
                     deleteflag='0')

    Hcate.save()
    Cate.save()
    Goods1.save()


def RecordAdd2():
    '''
    商品マスタに1件データを追加する。
    サイズ(M) 、色(黒)
    '''
    Hcate = HighCategoryTBL(highcategoryid='category01',
                            highcategoryname='衣類')
    Cate = CategoryTBL(categoryid='category01A01',
                       categoryname='スカート',
                       highcategoryid=Hcate)
    Goods2 = GoodsTBL(goodsid='product01M001',
                     categoryid=Cate,
                     productno='product01',
                     sizename='M',
                     colorname='黒',
                     price='4500',
                     goodsstocks='0',
                     salesstartdate='2019-07-29',
                     deleteflag='0')
    Goods2.save()


class DetailsListViewTest(TestCase):

    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行

    def test_normal_end(self):
        '''
        getメソッドでDetailsListViewを呼ばれたときのテスト
        1.詳細表示に反映されるobject_listが正しい値となっているか確認する。
        '''
        # テーブルにデータを1件追加する。
        RecordAdd()
        # 疑似的なsessionを作成し、'g_de_productno'に存在する製品番号を代入する。
        session = self.client.session
        session['g_de_productno'] = 'product01'
        session.save()
        # クライアント側からgetメソッドでリクエストされる。
        response = self.client.get(reverse('searchapp:details'))
        # レスポンスされたステータスコードを確認し、200(成功)であることを確認する。
        assert response.status_code == 200

        # contextデータ'goods_details'に1件データが入っていることを確認する。
        self.assertEqual(response.context['goods_details'].count(),1)
        # contextデータ'goods_details'のデータが正しく格納されていることを確認する。
        for a in response.context['goods_details']:
            self.assertEqual(a.productno,'product01','製品番号誤り')
            self.assertEqual(a.goodsid,'product01S001','商品ID誤り')
            self.assertEqual(a.sizename,'S','サイズ誤り')
            self.assertEqual(a.colorname,'黒','色誤り')

    def test_dynamic_choices(self):
        '''
        2.プルダウンに表示される項目が正しい値となっていることを確認する。
        '''
        # テーブルにデータを1件追加する。
        RecordAdd()
        # 疑似的なsessionを作成し、'g_de_productno'に存在する製品番号を代入する。
        session = self.client.session
        session['g_de_productno'] = 'product01'
        session.save()

        # サイズのプルダウンのみ変更し、色プルダウンは変更しない場合のテスト
        # サイズプルダウンを初期位置から'S'に変更した状態でpostする
        sizedata = {
            'size': 'S',
        }
        response = self.client.post(reverse('searchapp:details'), sizedata)
        # レスポンスされたステータスコードを確認し、200(正常終了)であることを確認する。
        self.assertEqual(response.status_code,200)

        # 色プルダウンのみ変更し、サイズプルダウンは変更しない場合のテスト
        # 色プルダウンを初期位置から'黒'に変更した状態でpostする
        colordata = {
            'color': '黒',
        }
        response = self.client.post(reverse('searchapp:details'), colordata)
        # レスポンスされたステータスコードを確認し、200(正常終了)であることを確認する。
        self.assertEqual(response.status_code,200)

        # サイズ、色両方のプルダウンが初期位置ではない場合のテスト
        # 在庫数を判定し、context['zaiko_form']に結果が反映されていることを確認する。
        # サイズ、色のプルダウンを初期位置から'S','黒'に変更した状態でpostする。
        data = {
            'size': 'S',
            'color': '黒',
        }
        response = self.client.post(reverse('searchapp:details'), data)
        self.assertEqual(response.context['zaiko_form'], '在庫あり')
        self.assertEqual(response.status_code, 200)


        # 在庫数0のデータを追加
        RecordAdd2()
        # サイズ、色両方のプルダウンが初期位置ではない場合のテスト
        # 在庫数を判定し、context['zaiko_form']に結果が反映されていることを確認する。
        # サイズ、色のプルダウンを初期位置から'M','黒'に変更した状態でpostする。
        zaiko0data = {
            'size': 'M',
            'color': '黒',
        }
        response = self.client.post(reverse('searchapp:details'), zaiko0data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['zaiko_form'], '在庫無')

        # 指定した色、サイズのパターンが存在しない場合のテスト
        # 在庫数を判定し、context['zaiko_form']に結果が反映されていることを確認する。
        # サイズ、色のプルダウンを初期位置から'S','赤'(存在しないパターン)に変更した状態でpostする。
        NotPattern = {
            'size': 'S',
            'color': '赤',
        }
        response = self.client.post(reverse('searchapp:details'), NotPattern)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['zaiko_form'], '-')



    def test_No_record(self):
        '''
        前画面から受け取った製品番号のレコードが1件も存在しない場合
        '''
        # テーブルにデータを1件追加する。
        RecordAdd()
        # 疑似的なsessionを作成し、'g_de_productno'に存在しない製品番号を代入する。
        session = self.client.session
        session['g_de_productno'] = 'product02'
        session.save()

        response = self.client.get(reverse('searchapp:details'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['goods_details'].count(),0)

    def test_coverage(self):
        '''
        カバレッジテスト
        一覧画面のResultListViewを通すためのメソッド
        '''
        session = self.client.session
        session['size'] = 'S'
        session['color'] = '黒'
        session.save()
        data = {
            'g_de_productno': 'product01',
        }
        # 商品名のリンクを押したときの処理テスト
        # sessionに['size']['color']が存在する場合は削除してから次画面へ遷移する。
        response = self.client.post(reverse('searchapp:result'),data)
        self.assertEqual(response.status_code,302)
        response = self.client.get(reverse('searchapp:result'))
        self.assertEqual(response.status_code,200)

    def test_no_postdata(self):
        # テーブルにデータを1件追加する。
        RecordAdd()
        # 疑似的なsessionを作成し、'g_de_productno'に存在する製品番号を代入する。
        session = self.client.session
        session['g_de_productno'] = 'product01'
        response = self.client.post(reverse('searchapp:details'))
        self.assertEqual(response.context['goods_details'].count(),0)


