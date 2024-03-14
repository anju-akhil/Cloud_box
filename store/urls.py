from django.urls import path
from store import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("products",views.ProductsView,basename="products")
router.register("baskets",views.BasketView,basename="baskets")
router.register("baskets/item",views.BasketItemsView,basename="basketitems")

urlpatterns = [
    path("register/",views.SignupView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
]+router.urls
