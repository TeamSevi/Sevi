from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyDHECxnjEG1AmiN_pbbunQQPEyUW_Ffl34",
    'authDomain': "seviapp-30ad7.firebaseapp.com",
    'databaseURL': "https://seviapp-30ad7.firebaseio.com",
    'projectId': "seviapp-30ad7",
    'storageBucket': "seviapp-30ad7.appspot.com",
    'messagingSenderId': "985230084588",
    'appId': "1:985230084588:web:edc65dd96831e96bbb58c9"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

    

# Create your views here.
def index(request):
    global firstname
    if "user" not in request.session:
        return redirect("login")
    else:
        firstname = request.session["username"]
        return render(request, "index.html", {"personname" : firstname})

def login(request):
    if request.method == "POST":
        phone = request.POST['phone']
        password = request.POST['password']
        try:
            usersdb = db.child("Web").child("hotelusers").get()
        except:
            return render(request, "login.html",{"msg" : "Error in database connection"}) 
        for person in usersdb.each():
            if phone==person.key() and password==person.val()["password"]:
                request.session["user"] = person.key()
                request.session["username"] = person.val()["firstname"]
                return HttpResponseRedirect(reverse("index"))
    return render(request, "login.html")    

def logout(request):
    try:
        request.session.flush()
        #del request.session["username"]
    except KeyError:
        pass
    return redirect('index')

def signup(request):
    return render(request, "signup.html")


def neworders(request):
    return render(request, "neworders.html")

def orders(request):
    uid = request.session["user"]
    hotelid = db.child("Web").child("hotelusers").child(uid).get().val()
    for hotel,id in hotelid.items():
        if hotel=="hotelid":
            hid = id
    orderlist = db.child("Hotel").child(hid).child("orders").get().val()
    li = []
    for orderid,details in orderlist.items():
        sl = []
        i=0
        sl.append(orderid)
        #sl.append(details["itemdetails"])
        ord_details=""
        itemdetail = details["itemdetails"]
        for value in itemdetail.values():
            ord_details += value["itemname"]
            i+=1
            if i != len(itemdetail):
                ord_details += ", "
        sl.append(ord_details)
        sl.append(details["username"])
        sl.append(details["tableno"])
        sl.append(details["date"])
        sl.append(details["time"])
        sl.append(details["price"])
        li.append(sl)
    return render(request, "orders.html",{ "orderlist":li})

def myhotel(request):
    return render(request, "myhotel.html")

def listitem(request):
    return render(request, "productlist.html")   

def additem(request):
    return render(request, "addproduct.html") 
