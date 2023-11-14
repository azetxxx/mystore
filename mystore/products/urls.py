from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from products.views import ProductsListView, add_to_basket, remove_from_basket

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>/', add_to_basket, name='basket_add'),
    path('baskets/remove/<int:basket_item_id>/', remove_from_basket, name='remove_from_basket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_roott=settings.MEDIA_ROOT)
