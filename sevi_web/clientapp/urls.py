from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup",views.signup, name="signup"),
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("neworders", views.neworders, name="neworders"),
    path("orders", views.orders, name="orders"),
    path("hotelDetail", views.myhotel, name="hotel"),
    path("ItemList", views.listitem, name="productlist"),
    path("AddItem", views.additem, name="addproduct"),
]