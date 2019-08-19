'''
searchappアプリのソースコードファイル
'''
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.db.models import Q
from django.views import generic
from django.shortcuts import redirect
from .forms import CategorySearchForm
from .forms import GoodsSearchForm
from .forms import SizeForm
from .forms import ColorForm
from .forms import LoginForm
from .models import GoodsTBL


class IndexView(generic.ListView):
    '''
    検索画面表示、検索文字列取得のためのクラス
    '''

    model = GoodsTBL
    template_name = 'searchapp/index.html'
    # クエリ結果を格納する変数の名前を定義している
    context_object_name = 'goods_search_result'

    # ①-1 post関数を定義
    def post(self, request):
        '''
        変数form_valueに画面上の入力フォームからpostで取得した値を
        格納して、セッションに持たせるメソッド
        '''
        # ②-1
        # フォーム値をセッションに格納（次画面で使用）
        # 後からユーザが入力したフォームの値を格納するためのリストを作成（リスト名：form_value）
        form_value = [
            self.request.POST.get('category_name', None),
            self.request.POST.get('search_char', None)
        ]
        # ②-2　
        # ②-1で作成したフォームの値を格納するリストをセッション（request.session）に受け渡す
        request.session['form_value'] = form_value
        # generic/list.pyのget()メソッドが呼び出される

        # ②-3
        # redirectでページを遷移する
        return redirect('searchapp:result')

    # ①-2
    # get_context_dataメソッドでcontextデータをテンプレートに渡すことが出来る
    def get_context_data(self, *, object_list=None, **kwargs):
        '''
         初期値に空白を設定した入力フォームとプルダウンフォームを格納した変数を
         contextに持たせてindex.htmlへ返すメソッド
        '''
        # ①-3
        # 親クラスのメソッド呼び出し、変数contextに格納
        # context＝テンプレートに使用できる文字列タグの存在を定義　※辞書型しか格納できない
        context = super().get_context_data(**kwargs)

        # ①-4
        # 検索フォームの初期値を設定する処理
        #category_name、search_charにそれぞれ空白の文字列を設定する
        category_name = ''
        search_char = ''

        # ①-5
        # 初期値を格納するための辞書型変数を作成、変数名は「default_data」
        # ①-4で設定した中身が空白文字列の変数を辞書の中に格納。
        default_data = {'category_name': category_name,
                        'search_char': search_char}

        # ①-6
        # 予めインポートしてあるフォームに初期値を設定して、更にフォームを変数に格納する。
        # （文字列検索フォーム＝search_form）
        # （カテゴリ検索フォーム=category_form）
        search_form = GoodsSearchForm(initial=default_data)
        category_form = CategorySearchForm(initial=default_data)
        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理

        # ①-7
        # ①-3で設定したcontextに①-6でフォームを格納した変数を格納
        # テンプレートにフォームを表示させる処理
        #表示用フォームが格納されたリスト'search_value'をテンプレートに返す。
        context['search_value'] = [category_form, search_form]
        return context



class ResultList(generic.ListView):
    """検索結果一覧画面のクラス"""
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    template_name = 'searchapp/result.html'

    def post(self, request, *args, **kwargs):
        """
        次画面に必要な情報（製品番号）をセッションに格納してリダイレクトする
        """
        # 1-5(result.htmlから)
        # sessionへ製品番号を保存
        request.session['g_de_productno'] = request.POST.get('productno', None)
        # 1-6
        # セッションからサイズと色を削除
        # 次画面でのブラウザバック使用時の為の設定
        if 'size' in request.session:
            del request.session['size']
        if 'color' in request.session:
            del request.session['color']
        # 1-7
        # redirect関数でdetailsクラスを呼び出す
        return redirect('searchapp:details')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
         条件に合った商品を一覧で表示するメソッド
        '''
        # 1-1
        # セッションの中にユーザの入力値が入っているかどうかの判定
        # ↑（検索押した後に動いているので基本的にはなにかしら入ってる：Nullではない）
        # 入っている場合は変数form_valueの中に前画面でユーザ入力値を格納したセッションを格納する

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
        else:
            form_value = ['', '']

        # 変数category_nameとsearch_charにユーザの入力値を格納する
        category_id = form_value[0]
        search_char = form_value[1]

        # 1-2
        # Qオブジェクトを作成。
        # exact=完全一致、contains=含む、
        # lte=等しいか、より少ない値に一致、gt=より大きい値に一致
        exact_cate = Q(categoryid__exact=category_id)
        contains_name = Q(goodsname__contains=search_char)
        contains_color = Q(colorname__contains=search_char)
        contains_price = Q(price__contains=search_char)
        contains_size = Q(sizename__contains=search_char)
        exact_ronsaku = Q(deleteflag__exact=0)
        lte_salesstartdate = Q(salesstartdate__lte=datetime.now().date())
        gt_salesenddate = Q(salesenddate__gt=datetime.now().date())
        exact_salesenddate = Q(salesenddate__exact=None)
        # 1-3
        # 入力値（カテゴリプルダウンと入力フォーム）が空白どうかの条件分岐if文
        # 分岐先で指定のクエリセットを発行し、変数goods_search_resultの中に格納する
        if form_value[0] == '':
            if form_value[1] == '':
                # カテゴリ×文字×
                # (全ての商品データを取得)
                goods_search_result = GoodsTBL.objects\
                .filter(exact_ronsaku& lte_salesstartdate\
                & (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')
            else:
                # カテゴリ×文字〇の時
                # (入力文字を値に含む商品データを取得)
                goods_search_result = GoodsTBL.objects.select_related()\
                .filter(exact_ronsaku\
                & (contains_name | contains_color | contains_price | contains_size)\
                & lte_salesstartdate& (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')
        else:
            if form_value[1] == '':
                # カテゴリ〇文字×の時
                # (選択したカテゴリと同じカテゴリに設定した商品データを取得)
                goods_search_result = GoodsTBL.objects.select_related()\
                .filter(exact_cate, exact_ronsaku & lte_salesstartdate\
                & (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')
            else:
                # カテゴリ〇文字〇の時
                # (選択したカテゴリと同じカテゴリに設定した商品データのなかで、
                # かつ入力した文字を含む商品データを取得)
                goods_search_result = GoodsTBL.objects.select_related()\
                .filter(exact_cate, exact_ronsaku\
                & (contains_name | contains_color | contains_price | contains_size)\
                & lte_salesstartdate & (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')

            # 1-4
            # 1-3で作成された検索結果goods_search_resultをfor文で回し、
            # 製品番号が表示用リスト(result_list)に格納されている。
            # 製品番号と被っていなければ、表示用リスト(result_list)にクエリオブジェクトを追加する処理
        result_list = []
        for loop in goods_search_result:
            productno_list = [d.productno for d in result_list]
            if loop.productno in productno_list:
                pass
            else:
                result_list.append(loop)

        context['result_list'] = result_list
        return context


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
    context_object_name = 'goods_details'

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

        # Qオブジェクトを各変数に初期化
        exact_productno = Q()  # 製造番号のQオブジェクト(完全一致)
        exact_salesenddate = Q()  # 販売終了年月日のQオブジェクト(完全一致)
        exact_deleteflag = Q()  # 論理削除フラグのQオブジェクト(完全一致)
        lte_salesstartdate = Q()  # 販売開始年月日のQオブジェクト(以下)
        gt_salesenddate = Q()  # 販売終了年月日のQオブジェクト(より大きい)

        # Qオブジェクトを使用して条件を作成
        # TBLの製品番号が前画面から渡された製品番号と完全一致
        exact_productno = Q(productno__exact=str(productno))
        # TBLの論理削除フラグが1と完全一致
        exact_deleteflag = Q(deleteflag__exact=deleteflag)
        # TBLの販売開始年月日がメソッド起動時の年月日時分以下(今日より前に販売している商品)
        lte_salesstartdate = Q(salesstartdate__lte=datetime.now().date())
        # TBLの販売終了年月日がメソッド起動時の年月日時分より大きい(今日の時点でまだ販売している商品)
        gt_salesenddate = Q(salesenddate__gt=datetime.now().date())
        # TBLの販売終了年月日が空白と完全一致(終了年月日が登録されていないときは終了日未定と取る)
        exact_salesenddate = Q(salesenddate__exact=None)

        # クエリを発行
        kekka = GoodsTBL.objects.select_related().filter(
            exact_productno & exact_deleteflag & lte_salesstartdate
            & (gt_salesenddate | exact_salesenddate))
        # クエリ発行結果をgoods_detailsへ格納する。
        return kekka

    def get_context_data(self, *, object_list=None, **kwargs):
        '''
        テンプレートで使用するデータをcontextデータに格納する処理
        size_form:サイズのプルダウンで表示される値を格納する。
        color_form:色のプルダウンで表示される値を格納する。
        zaiko_form:在庫数の判定結果の値を格納する
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


        # Qオブジェクトを各変数に初期化
        exact_productno = Q()  # 製造番号が
        exact_deleteflag = Q()  # 論理削除フラグ(完全一致)
        lte_salesstartdate = Q()  # 販売開始年月日が今の時間より前であること
        gt_salesenddate = Q()  # 販売終了年月日(以上)
        exact_salesenddate = Q()  # 販売終了年月日(完全一致)
        exact_sizename = Q()  # サイズ(完全一致)
        exact_colorname = Q()  # 色(完全一致)

        # インスタンス化した変数にQオブジェクト(検索条件)を記述
        # TBLの製品番号が前画面から渡された製品番号と完全一致
        exact_productno = Q(productno__exact=str(productno))
        # TBLの論理削除フラグが1と完全一致
        exact_deleteflag = Q(deleteflag__exact=int(deleteflag))
        # TBLの販売開始年月日がメソッド起動時の年月日時分以下(今日より前に販売している商品)
        lte_salesstartdate = Q(salesstartdate__lte=datetime.now().date())
        # TBLの販売終了年月日がメソッド起動時の年月日時分より大きい(今日の時点でまだ販売している商品)
        gt_salesenddate = Q(salesenddate__gt=datetime.now().date())
        # TBLの販売終了年月日が空白と完全一致(終了年月日が登録されていないときは終了日未定と取る)
        exact_salesenddate = Q(salesenddate__exact=None)
        # TBLのサイズ名がプルダウンで指定したサイズ名と完全一致
        exact_sizename = Q(sizename__exact=str(size))
        # TBLの色名がプルダウンで指定したサイズ名と完全一致
        exact_colorname = Q(colorname__exact=str(color))

        '''  start サイズと色のプルダウンの値と初期位置を設定する処理  '''
        # Qオブジェクトで定義した検索条件でクエリを発行する。
        szdist = GoodsTBL.objects.select_related().filter(
            exact_productno & exact_deleteflag & lte_salesstartdate
            & (gt_salesenddate | exact_salesenddate))\
            .values('sizename')\
            .order_by('-sizename')\
            .distinct()
        cldist = GoodsTBL.objects.select_related().filter(
            exact_productno & exact_deleteflag & lte_salesstartdate
            & (gt_salesenddate | exact_salesenddate))\
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

        # 対象製品のサイズ(重複削除済み)を1件ずつ読み込みプルダウンのフォームに格納する。
        for sz_one in szdist:
            size_list.append((sz_one['sizename'], sz_one['sizename']))
            # 対象のサイズ名が、ユーザが選択したサイズ名と同一であれば、そのサイズの位置を初期位置とする。
            if sz_one['sizename'] == size:
                size_init = size
        # 対象製品の色(重複削除済み)を1件ずつ読み込みプルダウンのフォームに格納する。
        for cl_one in cldist:
            color_list.append((cl_one['colorname'], cl_one['colorname']))
            # 対象の色名が、ユーザが選択した色名と同一であれば、その色の位置を初期位置とする。
            if cl_one['colorname'] == color:
                color_init = color

        # フォームをインスタンス化し、choice(プルダウンのリスト)に
        # 「size_list」を入れ、初期表示位置(initiral)を設定する。
        sz_form = SizeForm(szchoice=size_list,
                           initial={'size': size_init},
                           )
        # フォームをインスタンス化し、choice(プルダウンのリスト)に
        # 「color_list」を入れ、初期表示位置(initiral)を設定する。
        cl_form = ColorForm(clchoice=color_list,
                            initial={'color': color_init},
                            )
        # contextにsz_formとcl_formと入れる
        context['size_form'] = sz_form
        context['color_form'] = cl_form
        '''  end サイズと色のプルダウンの値と初期位置を設定する処理  '''

        '''  start 対象商品(サイズ&色指定)の在庫数判定処理  '''
        # 条件に当てはまる数を確認(1件あるかないか)
        zaiko = GoodsTBL.objects.select_related().filter(
            exact_sizename & exact_colorname & exact_productno
            & exact_deleteflag & lte_salesstartdate
            & (gt_salesenddate | exact_salesenddate))

        # プライマリキーを使用して一意検索を掛ければfor文で回さなくても良い
        # zaiko = GoodsTBL.objects.select_related().get(
        #     Q(goodsid__exact = str(goodsid)))

        # 対象商品のサイズと色のパターンが存在しているか判定
        if int(zaiko.count()) != 0:
            # 対象商品のパターンが存在した場合
            # 在庫数を判定し、0か1以上かで'在庫あり','在庫無'を判定する。
            if zaiko[0].goodsstocks == 0:
                zaiko_judg = '在庫無'
            else:
                zaiko_judg = '在庫あり'


        # テンプレートで使用する変数'zaiko_form'に在庫有無の結果を代入する
        context['zaiko_form'] = zaiko_judg
        '''  end 対象商品(サイズ&色指定)の在庫数判定処理  '''
        # 戻り値としてcontextを返す。
        return context


# クラス関数を、別のビュー関数からの呼び出し可能にするための定義
DETAILS_LISTVIEW = DetailsListView.as_view()


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'registration/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    # template_name = 'registration/login.html'

