from django.db import models
from django.utils import timezone
from django.contrib.postgres.validators import RangeMaxValueValidator, RangeMinValueValidator

# 新規テーブル作成　※１クラス＝１テーブルに該当
class GoodsTBL(models.Model):
    """商品モデル"""

    class Meta:  # テーブル名を定義
        db_table = 'goodstbl'

    # テーブルのカラムに対応するフィールドを定義
    # max_lengthは単純な文字数。半角全角、英数字関係なく合計でその文字数入るという設定
    goodsid = models.CharField(
        verbose_name = '商品ID',
        primary_key=True,
        max_length = 13,
    )
    productno = models.CharField(
        verbose_name = '製品番号',
        max_length = 9,
    )
    categoryid = models.ForeignKey(
        'CategoryTBL',
        to_field='categoryid',
        on_delete=models.CASCADE,
        null=True,
        verbose_name = 'カテゴリID'
    )
    sizename = models.CharField(
        verbose_name = 'サイズ',
        max_length = 1,
    )
    colorname = models.CharField(
        verbose_name = '色',
        max_length = 15,
    )
    goodsname = models.CharField(
        verbose_name = '商品名',
        max_length = 70,
    )
    goodsdescription = models.CharField(
        verbose_name = '商品記述',
        max_length = 150
    )
    goodsurl = models.URLField(
        verbose_name = '商品画像URL',
        max_length = 100,
    )
    price = models.IntegerField(
        verbose_name = '価格',
    )
    goodsstocks = models.IntegerField(
        verbose_name = '在庫数',
    )
    salesstartdate= models.DateField(
        verbose_name = '販売開始年月日',
    )
    salesenddate = models.DateField(
        verbose_name = '販売終了年月日',
    )
    entrydate = models.DateTimeField(
        verbose_name = '登録年月日時分秒',
    )
    updatedate = models.DateTimeField(
        verbose_name = '更新年月日時分秒',
    )
    deleteflag = models.IntegerField(
        verbose_name = '論理削除フラグ',
        default = '1',
    )

    # 管理サイトに表示させる文字列を定義
    def __str__(self):
        return self.goodsname


class CategoryTBL(models.Model):
    """商品モデル"""

    class Meta:  # テーブル名を定義
        db_table = 'categorytbl'

    categoryid = models.CharField(
        verbose_name = 'カテゴリID',
        primary_key=True,
        max_length = 12,
    )
    highcategoryid = models.ForeignKey(
        'HighCategoryTBL',
        to_field='highcategoryid',
        on_delete=models.CASCADE,
        null=True,
        verbose_name = '上位カテゴリID',
    )
    categoryname = models.CharField(
        verbose_name = 'カテゴリ名',
        max_length = 15,
    )

    # 管理サイトに表示させる文字列を定義
    def __str__(self):
        return self.categoryid


class HighCategoryTBL(models.Model):
    """商品モデル"""

    class Meta:  # テーブル名を定義
        db_table = 'highcategorytbl'

    highcategoryid = models.CharField(
        verbose_name = '上位カテゴリID',
        primary_key=True,
        max_length = 12,
    )
    highcategoryname = models.CharField(
        verbose_name = '上位カテゴリ名',
        max_length = 15,
    )

    # 管理サイトに表示させる文字列を定義
    def __str__(self):
        return self.highcategoryid
