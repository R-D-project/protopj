from django import shortcuts
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import is_safe_url
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, View
from extra_views import ModelFormSetView

from oscar.apps.basket.signals import (
    basket_addition, voucher_addition, voucher_removal)
from oscar.core import ajax
from oscar.core.loading import get_class, get_classes, get_model
from oscar.core.utils import redirect_to_referrer, safe_referrer

Applicator = get_class('offer.applicator', 'Applicator')
(BasketLineForm, AddToBasketForm, BasketVoucherForm, SavedLineForm) = get_classes(
    'basket.forms', ('BasketLineForm', 'AddToBasketForm',
                     'BasketVoucherForm', 'SavedLineForm'))
BasketLineFormSet, SavedLineFormSet = get_classes(
    'basket.formsets', ('BasketLineFormSet', 'SavedLineFormSet'))
Repository = get_class('shipping.repository', 'Repository')

OrderTotalCalculator = get_class(
    'checkout.calculators', 'OrderTotalCalculator')
BasketMessageGenerator = get_class('basket.utils', 'BasketMessageGenerator')


class BasketView(ModelFormSetView):
    model = get_model('basket', 'Line')
    basket_model = get_model('basket', 'Basket')
    formset_class = BasketLineFormSet
    form_class = BasketLineForm
    factory_kwargs = {
        'extra': 0,
        'can_delete': True
    }
    template_name = 'oscar/basket/basket.html'

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs['strategy'] = self.request.strategy
        return kwargs

    def get_queryset(self):
        return self.request.basket.all_lines()

    def get_shipping_methods(self, basket):
        return Repository().get_shipping_methods(
            basket=self.request.basket, user=self.request.user,
            request=self.request)

    def get_default_shipping_address(self):
        if self.request.user.is_authenticated:
            return self.request.user.addresses.filter(is_default_for_shipping=True).first()

    def get_default_shipping_method(self, basket):
        return Repository().get_default_shipping_method(
            basket=self.request.basket, user=self.request.user,
            request=self.request, shipping_addr=self.get_default_shipping_address())

    def get_basket_warnings(self, basket):
        """
        このバスケットに適用される警告のリストを返す
        """
        warnings = []
        for line in basket.all_lines():
            warning = line.get_warning()
            if warning:
                warnings.append(warning)
        return warnings

    def get_upsell_messages(self, basket):
        offers = Applicator().get_offers(basket, self.request.user,
                                         self.request)
        applied_offers = list(basket.offer_applications.offers.values())
        msgs = []
        for offer in offers:
            if offer.is_condition_partially_satisfied(basket) \
                    and offer not in applied_offers:
                data = {
                    'message': offer.get_upsell_message(basket),
                    'offer': offer}
                msgs.append(data)
        return msgs

    def get_basket_voucher_form(self):
        """
        This is a separate method so that it's easy to e.g. not return a form
        if there are no vouchers available.
        """
        return BasketVoucherForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voucher_form'] = self.get_basket_voucher_form()

        # Shipping information is included to give an idea of the total order
        # cost.  It is also important for PayPal Express where the customer
        # gets redirected away from the basket page and needs to see what the
        # estimated order total is beforehand.
        context['shipping_methods'] = self.get_shipping_methods(
            self.request.basket)
        method = self.get_default_shipping_method(self.request.basket)
        context['shipping_method'] = method
        shipping_charge = method.calculate(self.request.basket)
        context['shipping_charge'] = shipping_charge
        if method.is_discounted:
            excl_discount = method.calculate_excl_discount(self.request.basket)
            context['shipping_charge_excl_discount'] = excl_discount

        context['order_total'] = OrderTotalCalculator().calculate(
            self.request.basket, shipping_charge)
        context['basket_warnings'] = self.get_basket_warnings(
            self.request.basket)
        context['upsell_messages'] = self.get_upsell_messages(
            self.request.basket)

        if self.request.user.is_authenticated:
            try:
                saved_basket = self.basket_model.saved.get(
                    owner=self.request.user)
            except self.basket_model.DoesNotExist:
                pass
            else:
                saved_basket.strategy = self.request.basket.strategy
                if not saved_basket.is_empty:
                    saved_queryset = saved_basket.all_lines()
                    formset = SavedLineFormSet(strategy=self.request.strategy,
                                               basket=self.request.basket,
                                               queryset=saved_queryset,
                                               prefix='saved')
                    context['saved_formset'] = formset
        return context

    def get_success_url(self):
        return safe_referrer(self.request, 'basket:summary')

    def formset_valid(self, formset):
        # Store offers before any changes are made so we can inform the user of
        # any changes
        offers_before = self.request.basket.applied_offers()
        save_for_later = False

        # Keep a list of messages - we don't immediately call
        # django.contrib.messages as we may be returning an AJAX response in
        # which case we pass the messages back in a JSON payload.
        flash_messages = ajax.FlashMessages()

        for form in formset:
            if (hasattr(form, 'cleaned_data')
                    and getattr(form.cleaned_data, 'save_for_later', False)):
                line = form.instance
                if self.request.user.is_authenticated:
                    self.move_line_to_saved_basket(line)

                    msg = render_to_string(
                        'oscar/basket/messages/line_saved.html',
                        {'line': line})
                    flash_messages.info(msg)

                    save_for_later = True
                else:
                    msg = _("You can't save an item for later if you're "
                            "not logged in!")
                    flash_messages.error(msg)
                    return redirect(self.get_success_url())

        if save_for_later:
            # No need to call super if we're moving lines to the saved basket
            response = redirect(self.get_success_url())
        else:
            # Save changes to basket as per normal
            response = super().formset_valid(formset)

        # If AJAX submission, don't redirect but reload the basket content HTML
        if self.request.is_ajax():
            # Reload basket and apply offers again
            self.request.basket = get_model('basket', 'Basket').objects.get(
                id=self.request.basket.id)
            self.request.basket.strategy = self.request.strategy
            Applicator().apply(self.request.basket, self.request.user,
                               self.request)
            offers_after = self.request.basket.applied_offers()

            for level, msg in BasketMessageGenerator().get_messages(
                    self.request.basket, offers_before, offers_after, include_buttons=False):
                flash_messages.add_message(level, msg)

            # Reload formset - we have to remove the POST fields from the
            # kwargs as, if they are left in, the formset won't construct
            # correctly as there will be a state mismatch between the
            # management form and the database.
            kwargs = self.get_formset_kwargs()
            del kwargs['data']
            del kwargs['files']
            if 'queryset' in kwargs:
                del kwargs['queryset']
            formset = self.get_formset()(queryset=self.get_queryset(),
                                         **kwargs)
            ctx = self.get_context_data(formset=formset,
                                        basket=self.request.basket)
            return self.json_response(ctx, flash_messages)

        BasketMessageGenerator().apply_messages(self.request, offers_before)

        return response

    def json_response(self, ctx, flash_messages):
        basket_html = render_to_string(
            'oscar/basket/partials/basket_content.html',
            context=ctx, request=self.request)

        return JsonResponse({
            'content_html': basket_html,
            'messages': flash_messages.as_dict()
        })

    def move_line_to_saved_basket(self, line):
        saved_basket, _ = get_model('basket', 'basket').saved.get_or_create(
            owner=self.request.user)
        saved_basket.merge_line(line)

    def formset_invalid(self, formset):
        flash_messages = ajax.FlashMessages()
        flash_messages.warning(_(
            "Your basket couldn't be updated. "
            "Please correct any validation errors below."))

        if self.request.is_ajax():
            ctx = self.get_context_data(formset=formset,
                                        basket=self.request.basket)
            return self.json_response(ctx, flash_messages)

        flash_messages.apply_to_request(self.request)
        return super().formset_invalid(formset)


class BasketAddView(FormView):
    """
    Handles the add-to-basket submissions, which are triggered from various
    parts of the site. The add-to-basket form is loaded into templates using
    a templatetag from module basket_tags.py.
    サイトのさまざまな部分からトリガーされる、バスケットに追加する処理を実装
    バスケットに追加フォームは、モジュールbasket_tags.pyのテンプレートタグを使用して
    テンプレートにロードされる
    """
    form_class = AddToBasketForm  # forms.pyから製品IDを渡すことのできるViewを呼び出す。
    # アプリの名前（catalogue）とモデル（product）を取得するメソッドを呼び出している。
    product_model = get_model('catalogue', 'product')
    add_signal = basket_addition #basket_additionは引き数追加メソッドのように見える（不明）
    http_method_names = ['post']  # postメソッドを変数に保存しているように見える（不明）

    def post(self, request, *args, **kwargs):
        # product_modelで取得した値のオブジェクトを取得するメソッドを変数「self.product」に格納
        self.product = shortcuts.get_object_or_404(
            self.product_model, pk=kwargs['pk'])
        # 取得したフォームインスタンスをインスタンス化する親クラスを返却する
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        # フォームをインスタンス化するためのキーワード引き数を返却する親メソッドを変数kwargsに格納
        # 辞書型が変数に格納されてくる（予想）
        kwargs = super().get_form_kwargs()
        # 辞書型に['basket':リクエストを送ったバスケット（予想）]が格納される
        kwargs['basket'] = self.request.basket
        # 辞書型に['product':製品のオブジェクト（不明）]が格納される
        kwargs['product'] = self.product
        # リクエストを送ったバスケットとバスケットに格納される商品の格納された辞書型が返却される（予想）
        return kwargs

    def form_invalid(self, form):
        # 変数msgsに空のリストを格納
        msgs = []
        # for文でmsgsリストの中に値を格納（格納している値の内容は不明）
        for error in form.errors.values():
            msgs.append(error.as_text())
        #不明
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        messages.error(self.request, ",".join(clean_msgs))
        #class BasketViewへリダイレクト
        return redirect_to_referrer(self.request, 'basket:summary')

    def form_valid(self, form):
        #不明
        offers_before = self.request.basket.applied_offers()

        #フォームで取得した製品をバスケットに追加（不明）
        self.request.basket.add_product(
            form.product, form.cleaned_data['quantity'],
            form.cleaned_options())

        #get_success_messageで生成した文字列を引数として持ち、メッセージ追加メソッドを呼ぶ
        messages.success(self.request, self.get_success_message(form),
                         extra_tags='safe noicon')

        # Check for additional offer messages（追加のオファーメッセージを確認する）
        BasketMessageGenerator().apply_messages(self.request, offers_before)

        # Send signal for basket addition（バスケット追加の信号を送信する）
        self.add_signal.send(
            sender=self, product=form.product, user=self.request.user,
            request=self.request)

        #self.get_success_url()で作成したURLにHttpResponseRedirectを返却する
        return super().form_valid(form)

    def get_success_message(self, form):
        # メッセージの文字列を作成する
        return render_to_string(
            'oscar/basket/messages/addition.html',
            {'product': form.product,
             'quantity': form.cleaned_data['quantity']})

    def get_success_url(self):
        # カート追加通知を返却する先のURLを作成する
        post_url = self.request.POST.get('next')
        if post_url and is_safe_url(post_url, self.request.get_host()):
            return post_url
        return safe_referrer(self.request, 'basket:summary')


class VoucherAddView(FormView):
    form_class = BasketVoucherForm
    voucher_model = get_model('voucher', 'voucher')
    add_signal = voucher_addition

    def get(self, request, *args, **kwargs):
        return redirect('basket:summary')

    def apply_voucher_to_basket(self, voucher):
        if voucher.is_expired():
            messages.error(
                self.request,
                _("The '%(code)s' voucher has expired") % {
                    'code': voucher.code})
            return

        if not voucher.is_active():
            messages.error(
                self.request,
                _("The '%(code)s' voucher is not active") % {
                    'code': voucher.code})
            return

        is_available, message = voucher.is_available_to_user(self.request.user)
        if not is_available:
            messages.error(self.request, message)
            return

        self.request.basket.vouchers.add(voucher)

        # Raise signal
        self.add_signal.send(
            sender=self, basket=self.request.basket, voucher=voucher)

        # Recalculate discounts to see if the voucher gives any
        Applicator().apply(self.request.basket, self.request.user,
                           self.request)
        discounts_after = self.request.basket.offer_applications

        # Look for discounts from this new voucher
        found_discount = False
        for discount in discounts_after:
            if discount['voucher'] and discount['voucher'] == voucher:
                found_discount = True
                break
        if not found_discount:
            messages.warning(
                self.request,
                _("Your basket does not qualify for a voucher discount"))
            self.request.basket.vouchers.remove(voucher)
        else:
            messages.info(
                self.request,
                _("Voucher '%(code)s' added to basket") % {
                    'code': voucher.code})

    def form_valid(self, form):
        code = form.cleaned_data['code']
        if not self.request.basket.id:
            return redirect_to_referrer(self.request, 'basket:summary')
        if self.request.basket.contains_voucher(code):
            messages.error(
                self.request,
                _("You have already added the '%(code)s' voucher to "
                  "your basket") % {'code': code})
        else:
            try:
                voucher = self.voucher_model._default_manager.get(code=code)
            except self.voucher_model.DoesNotExist:
                messages.error(
                    self.request,
                    _("No voucher found with code '%(code)s'") % {
                        'code': code})
            else:
                self.apply_voucher_to_basket(voucher)
        return redirect_to_referrer(self.request, 'basket:summary')

    def form_invalid(self, form):
        messages.error(self.request, _("Please enter a voucher code"))
        return redirect(reverse('basket:summary') + '#voucher')


class VoucherRemoveView(View):
    voucher_model = get_model('voucher', 'voucher')
    remove_signal = voucher_removal
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        response = redirect('basket:summary')

        voucher_id = kwargs['pk']
        if not request.basket.id:
            # Hacking attempt - the basket must be saved for it to have
            # a voucher in it.
            return response
        try:
            voucher = request.basket.vouchers.get(id=voucher_id)
        except ObjectDoesNotExist:
            messages.error(
                request, _("No voucher found with id '%s'") % voucher_id)
        else:
            request.basket.vouchers.remove(voucher)
            self.remove_signal.send(
                sender=self, basket=request.basket, voucher=voucher)
            messages.info(
                request, _("Voucher '%s' removed from basket") % voucher.code)

        return response


class SavedView(ModelFormSetView):
    model = get_model('basket', 'line')
    basket_model = get_model('basket', 'basket')
    formset_class = SavedLineFormSet
    form_class = SavedLineForm
    factory_kwargs = {
        'extra': 0,
        'can_delete': True
    }

    def get(self, request, *args, **kwargs):
        return redirect('basket:summary')

    def get_queryset(self):
        try:
            saved_basket = self.basket_model.saved.get(owner=self.request.user)
            saved_basket.strategy = self.request.strategy
            return saved_basket.all_lines()
        except self.basket_model.DoesNotExist:
            return []

    def get_success_url(self):
        return safe_referrer(self.request, 'basket:summary')

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs['prefix'] = 'saved'
        kwargs['basket'] = self.request.basket
        kwargs['strategy'] = self.request.strategy
        return kwargs

    def formset_valid(self, formset):
        offers_before = self.request.basket.applied_offers()

        is_move = False
        for form in formset:
            if form.cleaned_data.get('move_to_basket', False):
                is_move = True
                msg = render_to_string(
                    'oscar/basket/messages/line_restored.html',
                    {'line': form.instance})
                messages.info(self.request, msg, extra_tags='safe noicon')
                real_basket = self.request.basket
                real_basket.merge_line(form.instance)

        if is_move:
            # As we're changing the basket, we need to check if it qualifies
            # for any new offers.
            BasketMessageGenerator().apply_messages(self.request, offers_before)
            response = redirect(self.get_success_url())
        else:
            response = super().formset_valid(formset)
        return response

    def formset_invalid(self, formset):
        messages.error(
            self.request,
            '\n'.join(
                error for ed in formset.errors for el
                in ed.values() for error in el))
        return redirect_to_referrer(self.request, 'basket:summary')
    #臨時で追加

