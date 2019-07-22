from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from .forms import GoodSearchForm
from .forms import GoodListForm
from .forms import SizeForm
from .forms import ColorForm
from .models import CategoryTBL
from .models import GoodsTBL
from .models import HighCategoryTBL
from datetime import datetime



# Create your views here.
#class Searchscreen(TemplateView):
class SearchScreen(generic.FormView):
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/Search.html'

    form_class = GoodSearchForm

    def post(self, request, *args, **kwargs):
        """
        検索フォームに入力された値をセッションに格納するメソッド
        ⇒初期アクセスでは、検索フォームに入力されていない⇒セッションに格納される処理は呼ばれない
        ⇒初期アクセスではこのメソッドは呼ばれない
        """
        # 検索値を格納するリストを新規作成
        srh_value = [
                self.request.POST.get('categoryname', None),
                self.request.POST.get('searchchar', None),
            ]

        # 検索値を格納するリストをセッションで管理する
        request.session['srh_value'] = form_value

        # generic/list.pyのget()メソッドが呼び出される
        # getメソッドの中でget_querysetとget_context_dataを呼び出している。
        return self.get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        """
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        categoryname = ''
        searchchar = ''

        # 最初はセッションに値が無いからこのif節は呼ばれない
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            categoryname = form_value[0]
            searchchar = form_value[1]

        # 辞書新規作成⇒初期値ではそれぞれ「空白」が設定
        default_data = {'categoryname' :categoryname, 'searchchar' :searchchar}

        # 入力フォームに初期値では空白を設定する処理
        srh_form = GoodSearchForm(initial = default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理
        context['srh_form'] = srh_form
        return context



class Result_ListView(generic.ListView):
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/result.html'

    def post(self, request, *args, **kwargs):
        print(request.POST.get('productno',None))
        request.session['g_de_productno'] = request.POST.get('productno',None)


        '''クエリ発行データをセッションに格納する方法を検証中
        kueri = GoodsTBL.objects.select_related().all()
        goodsiddata = [aa.goodsid for aa in kueri]
        cate = [aa.categoryid.categoryname for aa in kueri]
        Hcate = [aa.categoryid.highcategoryid.highcategoryname for aa in kueri]

        dic = dict.fromkeys(['goodsid','prodocutno','goodsname','categoryname','Highcategoryname','price'])
        dict_test = {}
        for aa in kueri:
            dic['goodsid']= aa.goodsid
            print(dic['goodsid'])

        print(dic)
        '''

        return redirect('searchapp:details')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        return context

    # 呼び出された（オーバーライドされたメソッド）
    def get_queryset(self):

        goodsid = 'AABBCC001S003'
        productno = goodsid[:9]
        deleteflag = 0 # 有効状態

        return GoodsTBL.objects.select_related().all()



class DetailsView(TemplateView):
    template_name = 'searchapp/details.html'

    def display(request):
        if request.POST:
            pass

    def details_list(request):
        #posts = get_object_or_404(Post, pk=pk)
        posts = pk
        return render(request,'searchapp/details.html',{'posts':posts})

class details_ListView(generic.ListView):
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/details.html'
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    #model = モデル名を定義すると「モデル名.objects.all()」を裏で定義してくれる(ListViewの特徴)
    model = GoodsTBL
    #get_querysetメソッドで返すテンプレートタグの名前
    #何も設定しないと、「object_list」で返す。
    context_object_name = 'goodsdetails'


    # POSTメソッドを呼び出すのはプルダウンの選択を変更したときのみ
    def post(self, request, *args, **kwargs):

        '''
        if 'sizeselect' in request.POST and 'colorselect' in request.POST:
            request.session['sizeselect'] = self.request.POST.get('sizeselect',None)
            request.session['colorselect'] = self.request.POST.get('colorselect',None)
        else:
            print('プルダウン以外の処理')
        '''

        # 在庫判定処理で使用するため、session['size]と['color']に画面上で定義している'size'と'color'を格納する。
        # HTMLの＜form＞タグ内にsizeselectとcolorselectがあることを確認(プルダウンの処理)
        if 'size' in request.POST and 'color' in request.POST:
            request.session['size'] = self.request.POST.get('size',None)
            request.session['color'] = self.request.POST.get('color',None)
        else:
            print('プルダウン以外の処理')

        # generic/list.pyのget()メソッドが呼び出される
        # getメソッドの中でget_querysetとget_context_dataを呼び出している。
        return self.get(request, *args, **kwargs)

        # return redirect(reverse('searchapp:details'))

        #post処理だけして返す場合
        #return render(request,'searchapp/details.html')

    def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）
        '''
        詳細画面に表示する商品を検索する。
        (19/07/23)ここでやっている処理は初期表示のみなので、前画面から表示する商品データを取得できる場合は不要になる。
        '''

        # SQL文の検索条件の値を変数に持たせる。
        # goodsid = 'AABBCC001S003'
        # productno = goodsid[:9]
        # セッションに持たせていた'g_de_productno'を変数'productnoに代入する。
        productno = self.request.session['g_de_productno']
        deleteflag = 0 # 有効状態

        '''■詳細画面表示に必要なDB検索条件(and)
            製品番号が変数'productno'と一致
            論理削除フラグが有効状態(削除されていない状態)
            販売開始年月日が現在の時間よりも前
            販売終了年月日が現在の時間よりも後
        '''

        #Qオブジェクトを各変数にインスタンス化
        exact_productno = Q() # 製造番号のQオブジェクト(完全一致)
        condition_salesstartdate = Q() # 販売開始年月日のQオブジェクト(含め)
        condition_salesenddate = Q() # 販売終了年月日のQオブジェクト(含め)
        exact_deleteflag = Q() #論理削除フラグのQオブジェクト(完全一致)

        # Qオブジェクトを使用して条件を作成
        exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='AABBCC001'
        exact_deleteflag = Q(deleteflag__exact = deleteflag) # 条件：論理削除フラグ = 1
        lte_salesstartdate = Q(salesstartdate__lte = datetime.now().date())
        gte_salesenddate = Q(salesenddate__gte = datetime.now().date())
        exact_salesenddate = Q(salesenddate__exact = None)

        # クエリを発行
        kekka = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag & lte_salesstartdate & (gte_salesenddate | exact_salesenddate))

        # クエリ発行結果をgoodsdetailsへ格納する。
        return kekka


    def get_context_data(self, *, object_list=None, **kwargs):
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        # goodsid = 'AABBCC001S003'
        # productno = goodsid[:9]
        # クエリ発行時の条件となる「製品番号」と「論理削除フラグ」を変数に入れる
        productno = ''
        deleteflag = 0 # 有効状態
        # session情報に'g_de_productno'が格納されているか判定（前画面から画面遷移されてきているか判定）
        if 'g_de_productno' in self.request.session:
            productno = self.request.session['g_de_productno']

        # 在庫状況の初期表示文字
        zaikoJudg = '-'
        '''
        サイズ、色のプルダウンが二つとも選択された時に在庫数を判定しcontextに判定結果を返す処理
        '''
        # クライアント側(HTML側)で実行した処理メソッド判定
        if self.request.method == 'POST':
            # 在庫数判定の前提条件:'sizeselect'と'colorselect'がsessionに登録されている
            # if 'sizeselect' in self.request.session and 'colorselect' in self.request.session
            if 'size' in self.request.session and 'color' in self.request.session:

                # 処理改善：結果を一意に(1件)に絞り込みたい)
                # 色の名前から色番号(商品IDと対になるもの)を参照してくる
                # colorID_search(self,colorname=self.request.session['color'])

                # session['size']とsession['color']の値が番号になっているから検索に引っかからない
                exact_sizename = Q(sizename__exact = str(self.request.session['size']))
                exact_colorname = Q(colorname__exact = str(self.request.session['color']))
                exact_productno = Q(productno__exact = str(productno))
                exact_deleteflag = Q(deleteflag__exact = deleteflag) # 条件：論理削除フラグ = 1
                lte_salesstartdate = Q(salesstartdate__lte = datetime.now().date())
                gte_salesenddate = Q(salesenddate__gte = datetime.now().date())
                exact_salesenddate = Q(salesenddate__exact = None)

                #条件に当てはまる数を確認(1件あるかないか)
                zaikaku = GoodsTBL.objects.select_related().filter( \
                    exact_sizename \
                    & exact_colorname \
                    & exact_productno \
                    & exact_deleteflag \
                    & lte_salesstartdate \
                    & (gte_salesenddate | exact_salesenddate))\
                    .count()

                # 対象商品のサイズと色のパターンが存在しているか判定
                if int(zaikaku) != 0:
                    # 対象商品のパターンが存在した場合
                    # 製造番号、色、サイズで商品を特定する。(プライマリキーでは無いため、内部では1件なのかが分からない
                    zaiko = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag & lte_salesstartdate & (gte_salesenddate | exact_salesenddate))

                    # プライマリキーを使用して一意検索を掛ければfor文で回さなくても良い
                    # zaiko = GoodsTBL.objects.select_related().get(Q(goodsid__exact = str(goodsid)))

                    # 在庫数を判定し、0か1以上かで'在庫あり','在庫なし'を判定する。
                    for zz in zaiko:
                        if zz.goodsstocks == 0:
                            zaikoJudg = "在庫なし"
                        elif zz.goodsstocks >= 1:
                            zaikoJudg = "在庫あり"
                        else:
                            zaikoJudg = "-"

                    # zaikofm = {'goodsstocks' : zaikoJudg}

                # テンプレートで使用する変数'zaiko_form'に在庫有無の結果を代入する


            else:
                print('get_contect_data:session値なし')
        else:
            print('get_contect_data:GET')

        context['zaiko_form'] = zaikoJudg


        # Qオブジェクトの初期設定(インスタンス化)
        # exact_goodsid = Q() # 商品IDのQオブジェクト(完全一致)
        exact_productno = Q() # 製造番号のQオブジェクト(完全一致)
        exact_deleteflag = Q() # 論理削除フラグのQオブジェクト(完全一致)
        lte_salesstartdate = Q()
        gte_salesenddate = Q()
        exact_salesenddate = Q()
        #インスタンス化した変数にQオブジェクト(検索条件)を記述
        # exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='AABBCC001S003'
        exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='AABBCC001'
        exact_deleteflag = Q(deleteflag__exact = int(deleteflag))  # 条件：論理削除フラグ = 1
        lte_salesstartdate = Q(salesstartdate__lte = datetime.now().date())
        gte_salesenddate = Q(salesenddate__gte = datetime.now().date())
        exact_salesenddate = Q(salesenddate__exact = None)

        # Qオブジェクトで定義した検索条件でクエリを発行する。
        szdist = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag & lte_salesstartdate & (gte_salesenddate | exact_salesenddate)).values('sizename').order_by('-sizename').distinct()
        cldist = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag & lte_salesstartdate & (gte_salesenddate | exact_salesenddate)).values('colorname').order_by('-colorname').distinct()
        # goodsdetail = GoodsTBL.objects.select_related().filter(exact_goodsid & exact_deleteflag)



        # プルダウンの項目をフォームに持たせる処理(テスト) Start

        # プルダウンをフォームで管理するための選択列情報取得
        size_list = []
        color_list = []
        size_list.append((0,'サイズをお選びください'))
        color_list.append((0,'色をお選びください'))
        colorcnt = 1
        sizecnt = 1
        color_init = 0
        size_init = 0

        if \
            self.request.method == 'POST' \
            and 'size' in self.request.session \
            and 'color' in self.request.session:

            # サイズとカラーの２つ選ばれたときのプルダウン設定
            for sz in szdist:
                size_list.append((sz['sizename'],sz['sizename']))
                if sz['sizename'] == self.request.session['size']:
                    size_init = self.request.session['size']
            for cl in cldist:
                color_list.append((cl['colorname'],cl['colorname']))
                if cl['colorname'] == self.request.session['color']:
                    color_init = self.request.session['color']


        else:
            for sz in szdist:
                size_list.append((sz['sizename'],sz['sizename']))
            for cl in cldist:
                color_list.append((cl['colorname'],cl['colorname']))


        # フォームをインスタンス化し、choice(プルダウンのリスト)に「size_list」を入れ、初期表示位置(initiral)を設定する。
        sz_form = SizeForm(szchoice=size_list,initial={'size' : size_init })
        # フォームをインスタンス化し、choice(プルダウンのリスト)に「color_list」を入れ、初期表示位置(initiral)を設定する。
        cl_form = ColorForm(clchoice=color_list,initial={'color': color_init})

        print(sz_form)
        #print(cl_form)
        # contextにsz_formとcl_formと入れる
        context['sizeform'] = sz_form
        context['colorform'] = cl_form

        # プルダウンの項目をフォームに持たせる処理(テスト) End

        # 戻り値としてcontextを返す。
        return context

details_listview = details_ListView.as_view()


class details_detailView(generic.DetailView):
    template_name = 'searchapp/details.html'
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    #model = モデル名を定義すると「モデル名.objects.all()」を裏で定義してくれる(DetailViewの特徴)
    model = GoodsTBL
    # 内部では、このquerysetに対して「pk」を使って「.filter(pk=pk)」のようなことを行っています。
    queryset = GoodsTBL.objects.all()
    # urls.pyで使用する[pk]という文字列を変える。(urls.pyも変えた文字列で定義すること)
    # id=製造番号とする。（仮決め）
    pk_url_kwarg = 'id'


def colorID_search(self,colorname=None):
    colorId = {"白":"001", "黒":"002","赤":"003"}

    if colorname in colorId:
        ans = colorId[colorname]
        print(ans)
    else:
        print("色なし")

