'''
入力フォームの設定ファイル

'''
from django import forms
from .models import CategoryTBL
from django.contrib.auth.forms import (
    AuthenticationForm
)


# ModelChoiceField=プルダウンの選択肢をmodels.pyから参照するフォームの種類
class CategorySearchField(forms.ModelChoiceField):
    '''
    プルダウンフォームを表示するためのModelChoiceFormを継承したクラス
    label_from_instanceでプルダウンの値を上書きしている
    '''
    #選択肢の表示をカスタマイズするメソッド
    def label_from_instance(self, obj=CategoryTBL):
        #  f"{}＝フォーマット文字列（{}内の文字をpythonの式として認識する）
        # obj.categoryname（カテゴリネーム）をmodelchoicefieldの値としてreturn
        return f"{obj.categoryname}"


class CategorySearchForm(forms.Form):
    '''
    この中で↑のモデルを呼びだしてカテゴリプルダウンとして使用する
    '''
    category_name = CategorySearchField(
        label='',
        required=False,  # 入力値の空白を許可
        queryset=CategoryTBL.objects.all(), # クエリ発行結果をプルダウンの選択肢に設定
        empty_label='カテゴリ',
    )


class GoodsSearchForm(forms.Form):
    '''
    フリーワード検索のフォームを表示する為のクラス
    '''
    def __init__(self, *args, **kwargs):
        super(GoodsSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # class="form-inline＝formの要素を横並びに隙間なく配置する設定
            field.widget.attrs["class"] = "form-inline"

    search_char = forms.CharField(
        max_length=180,
        initial='',
        label='',
        required=False,
        # プレイスホルダー（入力内容ヒント）の文字列を設定
        widget=forms.TextInput(
            attrs={
                'placeholder': 'フリーワード検索', 'class': 'class_name'
                }
        )
    )


class SizeForm(forms.Form):
    '''
        サイズのプルダウンを設定するクラス
    '''
    def __init__(self, szchoice, *args, **kwargs):
        '''
        __init__はインスタンス化されたときに起動する。
        プルダウンの値をインスタンス化(フォーム作成時)に格納する
        '''
        # 親クラス(今回は自分自身)を呼び、フィールド情報を取得する。
        super(SizeForm, self).__init__(*args, **kwargs)
        # sizeフィールドのchoices(プルダウンの値)にリスト変数szchoiceを代入
        # szchoiceはviewでプルダウン情報を定義している。
        self.fields['size'].choices = szchoice

    size = forms.ChoiceField(
        choices=(),  # __init__で定義するため、ここでは空白を設定する。
        label='サイズ',
        label_suffix='',  # デフォルト指定されているラベル後ろの「:」を「(空白)」に変更する。
        disabled=False,  # この要素を有効化(False)
        widget=forms.Select(
            # HTMLのselectタグに各設定を定義する。
            attrs={
                # プルダウンの値が変更されたときform名'selform'をsubmitする。
                'onChange': 'document.selform.submit()',
                'id': 'size_id',  # selectタグのidを'color_id'にする
                'tabindex': '1',  # tabindexを1にする
                },
            ),
    )


class ColorForm(forms.Form):
    '''
        色のプルダウンを設定するクラス
    '''
    def __init__(self, clchoice, *args, **kwargs):
        '''
        __init__はインスタンス化されたときに起動する。
        プルダウンの値をインスタンス化(フォーム作成時)に格納する
        '''
        # 親クラス(今回は自分自身)を呼び、フィールド情報を取得する。
        super(ColorForm, self).__init__(*args, **kwargs)
        # colorフィールドのchoices(プルダウンの値)にリスト変数zlchoiceを代入
        # clchoiceはviewでプルダウン情報を定義している。
        self.fields['color'].choices = clchoice

    color = forms.ChoiceField(
        choices=(),  # __init__で定義するため、ここでは空白を設定する。
        label='色',
        label_suffix='',  # デフォルト指定されているラベル後ろの「:」を「(空白)」に変更する。
        disabled=False,  # この要素を有効化(False)
        widget=forms.Select(
            # HTMLのselectタグに各設定を定義する。
            attrs={
                # プルダウンの値が変更されたときform名'selform'をsubmitする。
                'onChange': 'document.selform.submit()',
                'id': 'color_id',  # selectタグのidを'color_id'にする
                'tabindex': '2',  # tabindexを2にする
                },
            ),
    )


class LoginForm(AuthenticationForm):
    '''ログインフォーム'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 使用するclassを定義する。
            field.widget.attrs['class'] = 'form-control'
            # placeholder(入力欄に初期表示する内容)を定義する。
            field.widget.attrs['placeholder'] = field.label
