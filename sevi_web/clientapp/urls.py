from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup",views.signup, name="signup"),
    path("login",views.login, name="login"),
    path("payment",views.payment,name="payment"),
    path("logout",views.logout, name="logout"),
    path("neworders", views.neworders, name="neworders"),
    path("orders", views.orders, name="orders"),
    path("hotelDetail", views.myhotel, name="hotel"),
    path("itemList", views.listitem, name="productlist"),
    path("addItem", views.additem, name="addproduct"),
    path("updateitem/<str:uid>",views.updateitem,name="updateproduct"),
    path("tabledetails",views.tabledetails,name="tabledetails"),
    path("check-status",views.check_status,name="check-status"),
    path("customerlist", views.customerlist,name="customerlist"),
    path("customersreview",views.customersreview,name="customersreview"),
    path("statistics",views.statistics,name="statistics"),
    path("location",views.location,name="location"),
]