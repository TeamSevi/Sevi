from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core import serializers
from django.urls import reverse
import json
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
    if "hotelid" not in request.session:
        return redirect("login")
    else:
        firstname = request.session["username"]
        hotalid = request.session["hotelid"]
        tables = db.child("Hotel").child(hotalid).child("tables").get().val()
        return render(request, "index.html", {"tables": tables,  "personname" : firstname})


def tabledetails(request):
    #tableid = json.loads(request.body)
    #tid = tableid["tableid"]
    tid = request.GET["tableid"]
    hotalid = request.session["hotelid"]
    data = db.child("Hotel").child(hotalid).child("tables").child(tid).child("order").get().val()
    #inst = serializers.serialize('json',[data])
    print(data)
    return JsonResponse({"instance":data})
    #return JsonResponse(json.dumps(data))  

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
    firstname = request.session["username"]
    usersdetail,hoteldetail="",""
    err = {}
    if request.method=="POST":
        try:
            hotelname = request.POST["hotelname"]
            ttables = request.POST["tables"]
            city = request.POST["city"]
            address = request.POST["address"]
            img = request.POST["image"]
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            phone = request.POST["phone"]
            email = request.POST["email"]
            cpassword = request.POST["cpassword"]
            npassword = request.POST["npassword"]
            hotelid = request.session["hotelid"]
            userid = request.session["user"]
            curr_t = db.child("Web").child("hotelusers").child(userid).child("totaltables").get().val()
            if ttables!=curr_t:
                up_table = {}
                db.child("Hotel").child(hotelid).child("tables").remove()
                for i in range(1,int(ttables)+1):
                    up_table.update({"table "+str(i):{"status":"free"}})
                db.child("Hotel").child(hotelid).child("tables").update(up_table)
            if img:
                db.child("Hotel").child(hotelid).update({"hotelimage": img})
            if npassword:
                cpass = db.child("Web").child("hotelusers").child(userid).child("password").get().val()
                if cpass==cpassword:
                    db.child("Web").child("hotelusers").child(userid).update({"password":npassword})
                else:
                    err = {"status":"danger","one":"Try again!","two":"Enter correct password"}
            user_update = {"firstname": firstname,"lastname": lastname,"phoneno": phone,"email": email}
            db.child("Web").child("hotelusers").child(userid).update(user_update)
            update_db = {"hotelname": hotelname,"hotelcity": city,"hoteladdress": address,"totaltables":ttables}
            db.child("Hotel").child(hotelid).update(update_db)
            err = {"status":"success","one":"Well done!","two":"Details Updated Successfully."}
        except:
            err = {"status":"danger","one":"Try again!","two":"Something went wrong."}
    hotalid = request.session["hotelid"]
    try:
        hoteldetail = db.child("Hotel").child(hotalid).get().val()
        hoteldetail.pop("items")
        hoteldetail.pop("orders")
        userid = request.session["user"]
        usersdetail = db.child("Web").child("hotelusers").child(userid).get().val()
        usersdetail.pop("password")
    except:
        pass
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
            offer = request.POST.get("offer","False")
            hotelid = request.session["hotelid"]
            if 'updateitem' in request.POST and "uitemid" in request.session:
                itemid = request.session["uitemid"]
                if img:
                    db.child("hotel").child(hotelid).child("items").child(itemid).update({"itemimage": img})
                update_db = {"itemname":itemname,"itemcategory":catagory,"itemdescription":desc,"itemprice":price,"offer":offer,"status":item_status}
                db.child("Hotel").child(hotelid).child("items").child(itemid).update(update_db)
                del request.session["uitemid"]
                return HttpResponseRedirect(reverse("productlist"))
            elif 'additem' in request.POST and "uitemid" not in request.session:
                titem = db.child("Hotel").child(hotelid).child("items").get().val()
                if titem is None:
                    titem = {}
                titem = len(titem)+1
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
