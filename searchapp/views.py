from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView
from .forms import GoodSearchForm
from .forms import GoodListForm
from .forms import SizeForm
from .forms import ColorForm
from .models import CategoryTBL
from .models import GoodsTBL
from .models import HighCategoryTBL




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



class ResultList(generic.ListView):
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/post_list.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        """
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        title = ''
        category = ''
        price = ''

        # 最初はセッションに値が無いからこのif節は呼ばれない
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            title = form_value[0]
            category = form_value[1]
            price = form_value[2]

        # 辞書新規作成⇒初期値ではそれぞれ「空白」が設定
        default_data = {'title' :title, 'category' :category, 'price' :price}

        # 入力フォームに初期値では空白を設定する処理
        test_form = GoodListForm(initial = default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理
        context['test_form'] = test_form
        return context

    # 呼び出された（オーバーライドされたメソッド）
    def get_queryset(self):
    # DBから検索条件に一致したデータを取得

        # セッションに値があるときに動作する
        # ⇒最初にページに入ったときはセッションに値がないので、下のelse文が実行される
        #if 'form_value' in self.request.session:
            #form_value = self.request.session['form_value']
            #title = form_value[0]
            #category = form_value[1]
            #price = form_value[2]

            #Qオブジェクトを各変数にインスタンス化
            #condition_title = Q()
            #condition_category = Q()
            #condition_price = Q()

            # クエリを発行
            # 入力フォームに値が入っているかの判定
            # 変数の長さが1以上で、null値ではない場合、クエリを発行する。
            #if len(title) != 0 and title[0]:
            #    condition_title = Q(title__contains = title)
            #if len(category) != 0 and category[0]:
            #    condition_category = Q(category__contains = category)
            #if len(price) != 0 and price[0]:
            #    condition_price = Q(price__contains = price)

            # 定義されたクエリを発行し、データをobject_listへ格納する。
            return GoodsTBL.objects.select_related().all()

#        else:
#            return GoodsTBL.objects.none() # 何も返さない


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


    def post(self, request, *args, **kwargs):
        if 'sizeselect' in request.POST and 'colorselect' in request.POST:
            request.session['sizeselect'] = request.POST['sizeselect']
            request.session['colorselect'] = request.POST['colorselect']
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
        '''
        # セッションに値があるときに動作する
        # ⇒最初にページに入ったときはセッションに値がないので、下のelse文が実行される
        '''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            title = form_value[0]
            category = form_value[1]
            price = form_value[2]
        '''


        goodsid = 'AABBCC001S003'
        productno = goodsid[:9]
        deleteflag = 0 # 有効状態
        '''
        ■DB検索条件(and)
        製品番号 = 'AABBCC001'
        論理削除フラグ = 0
        販売開始年月日 < 現在時間(now)
        販売終了年月日 > 現在時間(now)
        '''
        #Qオブジェクトを各変数にインスタンス化
        condition_goodsid = Q() #商品IDのQオブジェクト(含め)
        exact_goodsid = Q() # 商品IDのQオブジェクト(完全一致)
        exact_productno = Q() # 製造番号のQオブジェクト(完全一致)
        condition_salesstartdate = Q() # 販売開始年月日のQオブジェクト(含め)
        condition_salesenddate = Q() # 販売終了年月日のQオブジェクト(含め)
        exact_deleteflag = Q() #論理削除フラグのQオブジェクト(完全一致)



        # クエリを発行
        exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='AABBCC001S003'
        condition_goodsid = Q(goodsid__contains = str(productno)) # 条件：商品IDに'AABBCC001'が含まれている
        exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='AABBCC001'
        exact_deleteflag = Q(deleteflag__exact = deleteflag) # 条件：論理削除フラグ = 1

            # 入力フォームに値が入っているかの判定
            # 変数の長さが1以上で、null値ではない場合、クエリを発行する。
        '''
            if len(title) != 0 and title[0]:
                condition_title = Q(title__contains = title)
            if len(category) != 0 and category[0]:
                condition_category = Q(category__contains = category)
            if len(price) != 0 and price[0]:
                condition_price = Q(price__contains = price)
        '''
        kekka = GoodsTBL.objects.select_related().filter(exact_goodsid & exact_deleteflag)
        # 定義されたクエリを発行し、データをgoodsdetailsへ格納する。
        return kekka
        '''
        kekka = GoodsTBL.objects.select_related().all()
        kekka = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag)
        kekka = GoodsTBL.objects.select_related().filter(condition_goodsid & exact_deleteflag)
        kekka = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag).values('productno').distinct()

         定義されたクエリを発行し、データをobject_listへ格納する。
         return GoodsTBL.objects.select_related().filter(condition_productno & condition_deleteflag)

        else:
            return Good.objects.none() # 何も返さない
        '''

    def get_context_data(self, *, object_list=None, **kwargs):
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)
        '''
        ■DB検索条件(and)
        製品番号 = 'AABBCC001'
        論理削除フラグ = 1
        販売開始年月日 < 現在時間(now)
        販売終了年月日 > 現在時間(now)
        '''

        goodsid = 'AABBCC001S003'
        productno = goodsid[:9]
        deleteflag = 0 # 有効状態

        # クライアント側(HTML側)からPOSTで返ってきたときの処理
        if self.request.method == 'POST':
            # 在庫数判定の前提条件
            # 'sizeselect'と'colorselect'がsessionに登録されている
            if 'sizeselect' in self.request.session and 'colorselect' in self.request.session:
                colorn = self.request.session['colorselect']
                colorID_search(self,colorname=colorn)
                exact_sizename = Q(sizename__exact = str(self.request.session['sizeselect']))
                exact_colorname = Q(colorname__exact = str(self.request.session['colorselect']))
                exact_productno = Q(productno__exact = str(productno))
                #zaiko = GoodsTBL.objects.select_related().filter(exact_colorname & exact_sizename & exact_productno).first()
                #条件に当てはまる数を確認(1件あるかないか)
                zaikaku = GoodsTBL.objects.select_related().filter(exact_colorname & exact_sizename & exact_productno).count()

                # 対象商品のサイズと色のパターンが存在しているか判定
                if int(zaikaku) == 0:
                    # 対象商品のパターンが存在しない場合
                    zaikoJudg = '-'

                else:
                    # 対象商品のパターンが存在した場合
                    # 製造番号、色、サイズで商品を特定する。(プライマリキーでは無いため、内部では1件なのかが分からない
                    zaiko = GoodsTBL.objects.select_related().filter(exact_colorname & exact_sizename & exact_productno)
                    '''
                    プライマリキーを使用して一意検索を掛ければfor文で回さなくても良い
                    zaiko = GoodsTBL.objects.select_related().get(Q(goodsid__exact = str(goodsid)))
                    print(zaiko.goodsstocks)
                    '''
                    # 在庫数を判定し、0か1以上かで'在庫あり','在庫なし'を判定する。
                    for zz in zaiko:
                        print(zz.goodsstocks)

                        if zz.goodsstocks == 0:
                            zaikoJudg = "在庫なし"
                        elif zz.goodsstocks >= 1:
                            zaikoJudg = "在庫あり"
                        else:
                            zaikoJudg = "-"

                        print(zaikoJudg)
                        zaikofm = {'goodsstocks' : zaikoJudg}

                # テンプレートで使用する変数'zaiko_form'に在庫有無の結果を代入する
                context['zaiko_form'] = zaikoJudg

        else:
            print('get_contect_data:GET')



        # Qオブジェクトの初期設定(インスタンス化)
        exact_goodsid = Q() # 商品IDのQオブジェクト(完全一致)
        exact_productno = Q() # 製造番号のQオブジェクト(完全一致)
        exact_deleteflag = Q() # 論理削除フラグのQオブジェクト(完全一致)

        #インスタンス化した変数にQオブジェクト(検索条件)を記述
        exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='AABBCC001S003'
        exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='AABBCC001'
        exact_deleteflag = Q(deleteflag__exact = int(deleteflag))  # 条件：論理削除フラグ = 1

        # Qオブジェクトで定義した検索条件でクエリを発行する。
        szdist = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag).values('sizename').order_by('-sizename').distinct()
        cldist = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag).values('colorname').order_by('-colorname').distinct()
        goodsdetail = GoodsTBL.objects.select_related().filter(exact_goodsid & exact_deleteflag)


        # プルダウンをフォームで管理するための選択列情報取得

        size_list = []
        '初期表示'
        size_list.append(('size','サイズをお選びください'))

        for sz in szdist:
            # print(sz['sizename'])
            size_list.append(('size',sz['sizename']))
            # print('sizelist' + str(size_list))

        sz_form = SizeForm(size_list)
        context['sss'] = sz_form


        '''
        hairetu = []
        a = 0
        for pddata in pdfull:
            hairetu.append([pddata.productno,pddata.sizename,pddata.colorname,pddata.goodsstocks])
            print(hairetu)
            a += 1

        for bb in range(int(len(hairetu))):
            print(hairetu[bb])
        '''

        '''
        zaikosc =   GoodsTBL.objects.select_related().filter(exact_goodsid).values('goodsid').get(pk=goodsid)
        print(zaikosc.get('goodsid'))
        print(str(zaikosc))
        '''

        '''
        print(productno)
        print(goodsdetail)
        print(szdist)
        print(cldist)
        '''
        # contextにクエリ発行した結果を追加し、テンプレートタグで使用可能にする。
        context['size_form'] = szdist
        context['color_form'] = cldist
        context['goods_form'] = goodsdetail

        # 戻り値としてcontextを返す。
        return context






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


