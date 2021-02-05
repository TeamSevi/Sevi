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
firstname = ""

# Create your views here.
def index(request):
    global firstname
    if "user" not in request.session:
        return redirect("login")
    else:
        firstname = request.session["username"]
        hotalid = request.session["hotelid"]
        my_stream = db.child("Hotel").child(hotalid).child("totaltables")
        
        return render(request, "index.html", {"t":my_stream,  "personname" : firstname})

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
                request.session["hotelid"] = person.val()["hotelid"]
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
    return render(request, "neworders.html",{"personname" : firstname})

def orders(request):
    hotalid = request.session["hotelid"]
    orderlist = db.child("Hotel").child(hotalid).child("orders").get().val()
    return render(request, "orders.html",{ "orderlist":orderlist,"personname" : firstname})

def myhotel(request):
    err = {}
    if request.method=="POST":
        try:
            hotelname = request.POST["hotelname"]
            ttables = request.POST["tables"]
            #price = request.POST["price"]
            #desc = request.POST["description"]
            #img = request.POST["image"]
            #status = request.POST["status"]
            #offer = request.POST["offer"]
            hotelid = request.session["hotelid"]

            update_db = {"hotelname": hotelname,"totaltables": ttables }
            db.child("Hotel").child(hotelid).update(update_db)
            err = {"status":"success","one":"Well done!","two":"Details Updated Successfully."}
        except:
            err = {"status":"danger","one":"Try again!","two":"Something went wrong."}
    hotalid = request.session["hotelid"]
    hoteldetail = db.child("Hotel").child(hotalid).get().val()
    hoteldetail.pop("items")
    hoteldetail.pop("orders")
    userid = request.session["user"]
    usersdetail = db.child("Web").child("hotelusers").child(userid).get().val()
    usersdetail.pop("password")
    return render(request, "myhotel.html",{ "hdetail": hoteldetail,"udetail": usersdetail, "personname" : firstname,"err":err})

def listitem(request):
    hotalid = request.session["hotelid"]
    itemlist = db.child("Hotel").child(hotalid).child("items").get().val()
    return render(request, "productlist.html",{"itemlist":itemlist,"personname" : firstname})   

def additem(request):
    b = {"u":"disabled","a":""}
    err = {}
    if request.method=="POST":
        try:
            itemname = request.POST["itemname"]
            catagory = request.POST["catagory"]
            price = request.POST["price"]
            desc = request.POST["description"]
            img = request.POST["image"]
            item_status = request.POST.get('itemstatus',"False")
            offer = request.POST["offer"]
            hotelid = request.session["hotelid"]
            if 'updateitem' in request.POST and "uitemid" in request.session:
                itemid = request.session["uitemid"]
                update_db = {"itemname":itemname,"itemcategory":catagory,"itemdescription":desc,"itemimage":img,"itemprice":price,"offer":offer,"status":item_status}
                db.child("Hotel").child(hotelid).child("items").child(itemid).update(update_db)
                del request.session["uitemid"]
                return HttpResponseRedirect(reverse("productlist"))
            elif 'additem' in request.POST and "uitemid" not in request.session:
                titem = len(db.child("Hotel").child(hotelid).child("items").get().val())+1
                itemid = "item" + str(titem)
                add_db = {"itemname":itemname,"itemcategory":catagory,"itemdescription":desc,"itemimage":img,"itemprice":price,"offer":offer,"status":item_status}
                db.child("Hotel").child(hotelid).child("items").child(itemid).set(add_db)
                err = {"status":"success","one":"Well done!","two":"You successfully added item."}
        except:
            err = {"status":"danger","one":"Try again!","two":"Something went wrong."}
    try:
        del request.session["uitemid"]
    except KeyError:
        pass  
    return render(request, "addproduct.html",{"err":err, "personname" : firstname, "b":b,"t":"True"}) 

def updateitem(request,uid):
    b = {"u":"","a":"disabled"}
    request.session["uitemid"] = uid
    hotalid = request.session["hotelid"]
    itemdetail = db.child("Hotel").child(hotalid).child("items").child(uid).get().val()
    return render(request, "addproduct.html",{"idetail":itemdetail, "b":b, "personname" : firstname})
