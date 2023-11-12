from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import ProductCategory, Product, Basket
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    context = {
        'title': 'Start - Fun Store',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):
    if category_id:
        product_items = Product.objects.filter(category_id=category_id)
    else:
        product_items = Product.objects.all()

    items_per_page = 3
    paginator = Paginator(product_items, items_per_page)
    products_on_page = paginator.page(page_number)

    context = {
        'title': 'Shop - Fun Store',
        'categories': ProductCategory.objects.all(),
        'products': products_on_page
    }

    return render(request, 'products/products.html', context)


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
