from django import forms


class GoodSearchForm(forms.Form):

    goodsname = forms.CharField(
            initial = '',
            label = '商品名',
            required = False,
        )
    categoryname = forms.CharField(
            initial = '',
            label = 'カテゴリ名',
            required = False,
        )
    highcategoryname = forms.CharField(
            initial = '',
            label ='上位カテゴリ名',
            required = False,
        )
    price = forms.IntegerField(
            initial = '',
            label = '価格',
            required = False,
        )
    size = forms.CharField(
            initial = '',
            label = 'サイズ',
            required = False,
        )
    color = forms.CharField(
            initial = '',
            label = '色',
            require = False,
        )
    goodsstocks = forms.IntegerField(
            initial = '',
            label = '在庫数',
            require = False,
        )