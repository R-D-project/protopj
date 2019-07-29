'''
searchappアプリのソースコードファイル
'''
from datetime import datetime
from django.db.models import Q
from django.views import generic
from django.shortcuts import redirect
from .forms import SizeForm
from .forms import ColorForm
from .models import GoodsTBL


class ResultListView(generic.ListView):
    '''
    一覧表示画面用のクラス
    '''
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/result.html'

    def post(self, request, *args, **kwargs):
        '''
        クライアント側からのリクエストが'POST'の場合に実行される処理
        次画面に必要な情報をsessionに格納してリダイレクトする。
        '''
        print(request.POST.get('productno', None))
        request.session['g_de_productno'] = request.POST.get('productno', None)
        if 'size' in request.session:
            del request.session['size']
        if 'color' in request.session:
            del request.session['color']

        return redirect('searchapp:details')

    def get_context_data(self, *, object_list=None, **kwargs):
        '''
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        '''
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        return context

    # 呼び出された（オーバーライドされたメソッド）
    def get_queryset(self):

        return GoodsTBL.objects.select_related().all()


class DetailsListView(generic.ListView):
    '''
    詳細表示画面用のクラス
    '''
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/details.html'
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    # model = モデル名を定義すると「モデル名.objects.all()」を裏で定義してくれる(ListViewの特徴)
    model = GoodsTBL
    # get_querysetメソッドで返すテンプレートタグの名前
    # 何も設定しないと、「object_list」で返す。
    context_object_name = 'goodsdetails'

    # POSTメソッドを呼び出すのはプルダウンの選択を変更したときのみ
    def post(self, request, *args, **kwargs):
        '''
        クライアント側からのリクエストが'POST'の場合に実行される処理
        次画面に必要な情報をsessionに格納してリダイレクトする。
        '''
        # 在庫判定処理で使用するため、session['size]と['color']に画面上で定義している'size'と'color'を格納する。
        # HTMLの＜form＞タグ内にsizeselectとcolorselectがあることを確認(プルダウンの処理)
        if 'size' in request.POST and 'color' in request.POST:
            request.session['size'] = self.request.POST.get('size', None)
            request.session['color'] = self.request.POST.get('color', None)

        # generic/list.pyのget()メソッドが呼び出される
        # getメソッドの中でget_querysetとget_context_dataを呼び出している。
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        '''
        詳細画面に表示する商品を検索する。
        '''
        # SQL文の検索条件の値を変数に持たせる。
        # セッションに持たせていた'g_de_productno'を変数'productnoに代入する。
        productno = self.request.session.get('g_de_productno', '')
        deleteflag = 0  # 有効状態

        # Qオブジェクトを各変数にインスタンス化
        exact_productno = Q()  # 製造番号のQオブジェクト(完全一致)
        exact_salesenddate = Q()  # 販売終了年月日のQオブジェクト(完全一致)
        exact_deleteflag = Q()  # 論理削除フラグのQオブジェクト(完全一致)

        # Qオブジェクトを使用して条件を作成
        exact_productno = Q(productno__exact=str(productno))
        exact_deleteflag = Q(deleteflag__exact=deleteflag)
        lte_salesstartdate = Q(salesstartdate__lte=datetime.now().date())
        gte_salesenddate = Q(salesenddate__gte=datetime.now().date())
        exact_salesenddate = Q(salesenddate__exact=None)
        # クエリを発行
        kekka = GoodsTBL.objects.select_related().filter(
            exact_productno & exact_deleteflag & lte_salesstartdate
            & (gte_salesenddate | exact_salesenddate))
        # クエリ発行結果をgoodsdetailsへ格納する。
        return kekka

    def get_context_data(self, *, object_list=None, **kwargs):
        '''
        テンプレートで使用するデータをcontextデータに格納する処理
        '''
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        # クエリ発行時の条件となる「製品番号」と「論理削除フラグ」を変数に入れる
        deleteflag = 0  # 有効状態
        zaiko_judg = '-'  # 在庫状況の初期表示文字

        # 前画面のViewからsession情報に'g_de_productno'を格納した状態で
        # 遷移されている場合はその値を格納する。
        productno = self.request.session.get('g_de_productno', '')
        # プルダウン押下してsessionに'size'と'color'が入っている場合は
        # その値を、入っていない場合は0を各変数に格納する。
        size = self.request.session.get('size', '0')
        color = self.request.session.get('color', '0')

        '''
        Qオブジェクトの初期設定(インスタンス化)
        exact_productno = Q()  製造番号(完全一致)
        exact_deleteflag = Q()  論理削除フラグ(完全一致)
        lte_salesstartdate = Q()  販売開始年月日(以上)
        gte_salesenddate = Q()  販売終了年月日(以下)
        exact_salesenddate = Q()  販売終了年月日(完全一致)
        exact_sizename = Q()  サイズ(完全一致)
        exact_colorname = Q()  色(完全一致)
        '''
        # インスタンス化した変数にQオブジェクト(検索条件)を記述
        exact_productno = Q(productno__exact=str(productno))
        exact_deleteflag = Q(deleteflag__exact=int(deleteflag))
        lte_salesstartdate = Q(salesstartdate__lte=datetime.now().date())
        gte_salesenddate = Q(salesenddate__gte=datetime.now().date())
        exact_salesenddate = Q(salesenddate__exact=None)
        exact_sizename = Q(sizename__exact=str(size))
        exact_colorname = Q(colorname__exact=str(color))

        '''  start サイズと色のプルダウンの値と初期位置を設定する処理  '''
        # Qオブジェクトで定義した検索条件でクエリを発行する。
        szdist = GoodsTBL.objects.select_related().filter(
            exact_productno & exact_deleteflag & lte_salesstartdate
            & (gte_salesenddate | exact_salesenddate))\
            .values('sizename').\
            order_by('-sizename').\
            distinct()
        cldist = GoodsTBL.objects.select_related().filter(
            exact_productno & exact_deleteflag & lte_salesstartdate
            & (gte_salesenddate | exact_salesenddate))\
            .values('colorname')\
            .order_by('-colorname')\
            .distinct()

        # プルダウンをフォームで管理するための選択列情報取得
        size_init = 0
        color_init = 0
        color_list = []
        size_list = []
        size_list.append((size_init, 'サイズをお選びください'))
        color_list.append((color_init, '色をお選びください'))

        for sz_one in szdist:
            size_list.append((sz_one['sizename'], sz_one['sizename']))
            if sz_one['sizename'] == size:
                size_init = size

        for cl_one in cldist:
            color_list.append((cl_one['colorname'], cl_one['colorname']))
            if cl_one['colorname'] == color:
                color_init = color

        # フォームをインスタンス化し、choice(プルダウンのリスト)に
        # 「size_list」を入れ、初期表示位置(initiral)を設定する。
        # デフォルト指定されているラベル後ろの「:」を「(空白)」に変更する。
        sz_form = SizeForm(szchoice=size_list,
                           initial={'size': size_init},
                           label_suffix='')
        # フォームをインスタンス化し、choice(プルダウンのリスト)に
        # 「color_list」を入れ、初期表示位置(initiral)を設定する。
        # デフォルト指定されているラベル後ろの「:」を「(空白)」に変更する。
        cl_form = ColorForm(clchoice=color_list,
                            initial={'color': color_init},
                            label_suffix='')
        # contextにsz_formとcl_formと入れる
        context['sizeform'] = sz_form
        context['colorform'] = cl_form
        '''  end サイズと色のプルダウンの値と初期位置を設定する処理  '''
        '''  start 対象商品(サイズ&色指定)の在庫数判定処理  '''
        # 条件に当てはまる数を確認(1件あるかないか)
        zai_kaku = GoodsTBL.objects.select_related().filter(
            exact_sizename & exact_colorname & exact_productno
            & exact_deleteflag & lte_salesstartdate
            & (gte_salesenddate | exact_salesenddate))\
            .count()

        # 対象商品のサイズと色のパターンが存在しているか判定
        if int(zai_kaku) != 0:
            # 対象商品のパターンが存在した場合
            # 製造番号、色、サイズで商品を特定する。
            # (プライマリキーでは無いため、内部では1件なのかが分からない
            zaiko = GoodsTBL.objects.select_related().filter(
                exact_productno & exact_deleteflag & lte_salesstartdate
                & (gte_salesenddate | exact_salesenddate))

            # プライマリキーを使用して一意検索を掛ければfor文で回さなくても良い
            # zaiko = GoodsTBL.objects.select_related().get(
            #     Q(goodsid__exact = str(goodsid)))

            # 在庫数を判定し、0か1以上かで'在庫あり','在庫なし'を判定する。
            for zk_one in zaiko:
                if zk_one.goodsstocks == 0:
                    zaiko_judg = "在庫なし"
                elif zk_one.goodsstocks >= 1:
                    zaiko_judg = "在庫あり"

        # テンプレートで使用する変数'zaiko_form'に在庫有無の結果を代入する
        context['zaiko_form'] = zaiko_judg
        '''  end 対象商品(サイズ&色指定)の在庫数判定処理  '''

        # 戻り値としてcontextを返す。
        return context


# クラス関数を、別のビュー関数からの呼び出し可能にするための定義
DETAILS_LISTVIEW = DetailsListView.as_view()
