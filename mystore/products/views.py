from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory

# Create your views here.


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Home 🛒 Fun Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Shop 🛒 Fun Store'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


@login_required
def add_to_basket(request, product_id):
    product = Product.objects.get(id=product_id)
    item_for_basket = Basket.objects.filter(user=request.user, product=product)

    if not item_for_basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        item_for_basket = item_for_basket.first()
        item_for_basket.quantity += 1
        item_for_basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def remove_from_basket(request, basket_item_id):
    item_in_basket = Basket.objects.get(id=basket_item_id)
    item_in_basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
