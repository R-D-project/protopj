'''
テーブルの情報を定義するファイル
'''

from django.db import models
from django.core import validators


# 新規テーブル作成
# 1クラス＝1テーブルに該当
class GoodsTBL(models.Model):
    '''
    商品マスタの設定
    '''
    class Meta:
        '''
        modelのメタデータ(フィールド定義以外)を定義する。
        '''
        db_table = 'goodstbl'  # テーブル名
        verbose_name_plural = '商品マスタ'  # 管理画面で表示されるテーブル名
        # 一意な組み合わせを定義
        # 設計上、製品番号、サイズ、色の組み合わせが重複させないために定義する。
        unique_together = ('productno', 'sizename', 'colorname')

    # テーブルのカラムに対応するフィールドを定義
    # max_length:単純な文字数。半角全角、英数字関係なく合計文字数入るという設定
    # primary_key=True:プライマリキーとして設定する。
    # null=True:TBL登録時に空白を許容する。
    # null=Flase:登録時に空白を許容しない。(デフォルト)
    # blank=True:フォームからの入力(登録)では空白を許容する。
    # blank=Flase:フォームからの入力(登録)では空白を許容しない。(デフォルト)
    goodsid = models.CharField(
        verbose_name='商品ID',
        primary_key=True,
        max_length=13,
    )
    productno = models.CharField(
        verbose_name='製品番号',
        max_length=9,
    )
    # カテゴリIDはCategoryTBLのcategoryidを外部キーとして設定する。
    categoryid = models.ForeignKey(
        'CategoryTBL',
        to_field='categoryid',
        # 外部キーであるCategoryTBLからcategoryidを削除するときにGoodsTBLで指定している同一categoryidを削除
        on_delete=models.CASCADE,
        verbose_name='カテゴリID'
    )
    sizename = models.CharField(
        verbose_name='サイズ',
        max_length=1,
    )
    colorname = models.CharField(
        verbose_name='色',
        max_length=15,
    )
    goodsname = models.CharField(
        verbose_name='商品名',
        max_length=70,
    )
    goodsdescription = models.CharField(
        verbose_name='商品記述',
        max_length=150,
        null=True,
        blank=True,
    )
    goodsurl = models.URLField(
        verbose_name='商品画像URL',
        max_length=100,
        null=True,
        blank=True,
    )
    price = models.IntegerField(
        verbose_name='価格',
    )
    goodsstocks = models.IntegerField(
        verbose_name='在庫数',
    )
    salesstartdate = models.DateField(
        verbose_name='販売開始年月日',
    )
    salesenddate = models.DateField(
        verbose_name='販売終了年月日',
        null=True,
        blank=True,
    )
    entrydate = models.DateTimeField(
        verbose_name='登録年月日時分秒',
        null=True,
        blank=True,
    )
    updatedate = models.DateTimeField(
        verbose_name='更新年月日時分秒',
        null=True,
        blank=True,
    )
    deleteflag = models.IntegerField(
        verbose_name='論理削除フラグ',
        # フラグの初期値を0にする。
        default='0',
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(1)]
    )

    # 管理サイトに表示させる文字列を定義
    def __str__(self):
        # adminページで表示するときの文字列を返す。
        return '[' + self.goodsid + ']' + self.goodsname


class CategoryTBL(models.Model):
    '''
    カテゴリー名を管理するテーブル
    '''
    class Meta:  # テーブル名を定義
        '''
        modelのメタデータ(フィールド定義以外)を定義する。
        '''
        db_table = 'categorytbl'
        verbose_name_plural = 'カテゴリマスタ'

    categoryid = models.CharField(
        verbose_name='カテゴリID',
        primary_key=True,
        max_length=13,
    )
    highcategoryid = models.ForeignKey(
        'HighCategoryTBL',
        to_field='highcategoryid',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='上位カテゴリID',
    )
    categoryname = models.CharField(
        verbose_name='カテゴリ名',
        max_length=15,
    )

    # 管理サイトに表示させる文字列を定義
    def __str__(self):
        # adminページで表示するときの文字列を返す。
        return '[' + self.categoryid + ']' + self.categoryname


class HighCategoryTBL(models.Model):
    '''
    上位カテゴリー名を管理するテーブル
    '''
    class Meta:  # テーブル名を定義
        '''
        modelのメタデータ(フィールド定義以外)を定義する。
        '''
        db_table = 'highcategorytbl'
        verbose_name_plural = '上位カテゴリマスタ'

    highcategoryid = models.CharField(
        verbose_name='上位カテゴリID',
        primary_key=True,
        max_length=10,
    )
    highcategoryname = models.CharField(
        verbose_name='上位カテゴリ名',
        max_length=15,
    )

    # 管理サイトに表示させる文字列を定義
    def __str__(self):
        # adminページで表示するときの文字列を返す。
        return '[' + self.highcategoryid + ']' + self.highcategoryname
