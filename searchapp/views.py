from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
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
    template_name = 'searchapp/details.html'
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    #model = モデル名を定義すると「モデル名.objects.all()」を裏で定義してくれる(ListViewの特徴)
    model = GoodsTBL
    context_object_name = 'goodsdetails'

    def post(self, request, *args, **kwargs):
        print (request.POST)
        if request.method == 'post':
            form = 'yes'
            #sizeform(request.post)
        else:
            form = 'no'
            #form = sizeform()

        #return render(request,'searchapp/details.html',{'form': form})
        return self.get(request, *args, **kwargs)


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
        pdfull = GoodsTBL.objects.select_related().filter(exact_productno)


        hairetu = []
        a = 0
        for pddata in pdfull:
            hairetu.append([pddata.productno,pddata.sizename,pddata.colorname,pddata.goodsstocks])
            print(hairetu)
            a += 1

        for bb in range(int(len(hairetu))):
            print(hairetu[bb])

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


