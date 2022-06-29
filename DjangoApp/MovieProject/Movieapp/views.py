from enum import Flag
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Movie,User,UserProfile,Cart
from .forms import movieform,UserProfileForm,Userform
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from MovieProject.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY ))

# Create your views here.

def addmovie(request):
    form=movieform()
    if request.method=="POST":
        print(request.FILES)
        form=movieform(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse('<h1>Saved</h1>')
    
    return render(request,'movieapp/addmovie.html',{'mform':form})

def showmovie(request):
    data=Movie.objects.all
    return render (request,'movieapp/showmovie1.html',{'showmovie':data})

def updatemovie(request,id):
    movie=Movie.objects.get(id=id)
    form=movieform(instance=movie)
    if request.method=='POST':
        print(request.FILES)
        print('-------------')
        form=movieform(request.POST,request.FILES,instance=movie)
        if form.is_valid():
            print('-------------')
            form.save(commit=True)
            return redirect('/showmovie')

    return render(request,'movieapp/addmovie.html',{'mform':form})

def deletemovie(request,id):
    data=Movie.objects.get(id=id)
    data.delete()
        
    return redirect('/showmovie')


def addUser(request):
    uform = Userform()
    custform =UserProfileForm()
    
    if request.method=='POST':
    
        role = request.POST['role']
        uform = Userform(request.POST)
        custform=UserProfileForm(request.POST)
        
        if uform.is_valid() and custform.is_valid():
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                messages.warning(request,'This email already exist')
            else:
                uobj = uform.save(commit=True)
                uobj.set_password(uobj.password)
                uobj.save()
                userobj=custform.save(commit=False)
                userobj.user=uobj
                userobj.save()
                if role == 'customer':
                    cust = Group.objects.get(name='customer')
                    uobj.groups.add(cust)
                elif role == 'admin':
                    admin = Group.objects.get(name='admin')
                    uobj.groups.add(admin)

    return render(request, 'movieapp/register.html', {'uform': uform, 'form': custform})    

def Login(request):
    form=AuthenticationForm()
    if request.method=="POST":
        uname=request.POST['username']
        pwd=request.POST['password']
        print(uname,pwd)
        
        user=authenticate(username=uname,password=pwd)
        if user!=None:
            login(request,user)
            return redirect('/showmovie1/')
        else:
            msg="INVALID USERNAME AND PASSWORD"
            return render(request,"movieapp/login.html",{'form':form, 'msg':msg})
        
    return render(request,"movieapp/login.html",{'form':form})   



def logoutUser(request):
    print('..............',request.user)
    logout(request)

    return redirect('/login/')   

def showUserlist(request):
    data=UserProfile.objects.all
    return render(request, 'movieapp/customerlist.html',{'users':data})

def showuserprofile(request):
    currentuser=request.user
    print(currentuser)
    userobject=UserProfile.objects.get(user=currentuser)
    print(userobject.user.email)
    groupobj=str(Group.objects.get(user=currentuser))
    print(groupobj,type(groupobj))
    return render(request,'movieapp/userprofile.html',{'user':userobject,'role':groupobj})


def edituser(request):
    currentuser=request.user
    print(currentuser)
    data = UserProfile.objects.get(user=currentuser)
    data1=User.objects.get(username=currentuser)
    if request.method=='POST':
        print(request.POST)
        uform = Userform(request.POST,instance=data1)
        form = UserProfileForm(request.POST,instance=data)
        print(uform)
        print(form)
        if uform.is_valid() and form.is_valid():
            uobj = uform.save(commit=True)

            uobj.save()
            userobj = form.save(commit=False)
            userobj.user = uobj
            userobj.save()
    return redirect('/index/')

    
def home(request):
     return render(request,'movieapp/home.html')

# def booking(request,id):
#     movie=Movie.objects.get(id=id)
#     form=movieform(instance=movie)    
#     print(movie)
#     return render(request,'movieapp/booking.html',{"data":movie})

def addtocart(request):
    print(request)
    mid=request.GET.get('movieid')
    movieobject=Movie.objects.get(id=mid)
    movieprice=movieobject.Price
    userobject=request.user
    print(movieobject,userobject,movieprice)
    Cart(movieobject=movieobject,userObject=userobject,totalprice=movieprice).save()
    return redirect('/showmovie1')


def showcart(request):
   items=Cart.objects.filter(userObject=request.user)
   flag=items.exists()
   if request.method=="POST":
       customer=UserProfile.objects.get(user=request.user)
      
       totalam=request.POST.get('totalamount')
       DATA = {
        "amount": int(totalam)*100,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"}}
       orderObject=client.order.create(data=DATA)  
       print(orderObject)
       orderid=orderObject['id']
       
       return render(request,'movieapp/payment.html',{'ordid':orderid,'customer':customer,'apiKey':RAZORPAY_API_KEY,'amount':totalam})
   return render(request,'movieapp/mycart.html',{'items':items,'flag':flag})  


def updatecart(request):
    p=request.POST.get('price')
    q=request.POST.get('qnt')
    id=request.POST.get('cid')
    totalprice=float(p)*int(q)
    Cart.objects.filter(id=id).update(number_of_ticket=q,totalprice=totalprice)
    total=Cart.objects.filter(userObject=request.user).aggregate(Sum('totalprice'))
    print(total)
    totalamount=total['totalprice__sum']

    return JsonResponse({'status':True,'totalprice':totalprice,'totalam':totalamount})


def addorders(request):
    print(request)