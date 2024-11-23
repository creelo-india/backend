from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from django.urls import path
from .views import add_to_cart, get_cart
from creelo_app import views
router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', get_cart, name='get-cart'),
    path('add-to-cart', add_to_cart, name='add-to-cart'),
     path('get-product', views.GetProductList.as_view(), name='get-product'),
]
