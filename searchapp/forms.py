from django import forms


class GoodSearchForm(forms.Form):

    goodsid = forms.CharField(
            initial = '',
            label = '商品ID',
            required = False,
        )
    categoryID = forms.CharField(
            initial = '',
            label = 'カテゴリ',
            required = False,
        )
    price = forms.IntegerField(
            initial = '',
            label = '値段',
            required = False,
        )
