from django import forms
from .models import GoodsTBL

class GoodSearchForm(forms.Form):
    categoryname = forms.CharField(
            initial = '',
            label = 'カテゴリ名',
            required = False,
        )
    searchchar = forms.CharField(
            initial = '',
            label = '検索項目',
            required = False,
        )

class GoodListForm(forms.Form):

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
    size = forms.ChoiceField(
            initial = '',
            label = 'サイズ',
            required = False,
            widget=forms.Select(attrs={
               'id': 'size',}),
        )
    color = forms.ChoiceField(
            initial = '',
            label = '色',
            required = False,
        )
    goodsstocks = forms.IntegerField(
            initial = '',
            label = '在庫数',
            required = False,
        )

    def __init__(self, queryset=None, *args, **kwargs):
        super(GoodListForm,self).__init__(*args,**kwargs)
        if queryset :
            self.fields['size'].queryset = queryset
