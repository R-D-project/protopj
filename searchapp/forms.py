'''
入力フォームの設定ファイル
'''
from django import forms
from django.core.exceptions import ValidationError

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
