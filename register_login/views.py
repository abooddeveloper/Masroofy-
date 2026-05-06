from django.shortcuts import render,redirect
from .forms import registration_login_form
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import userRegistration
# Create your views here.
def register(request):
    page="register"
    form=registration_login_form()
    if request.method=="POST":
        form=registration_login_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'registerLogin/registerLogin.html',{'form':form,'page':page})



def loginUser(request):
    page="login"
    if request.method =="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        try:
            user =userRegistration.objects.get(username=username)
        except:
            messages.error(request,"User not found")
            return render(request,'registerLogin/registerLogin.html',{'page':page})
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_first_login:
                user.is_first_login=False
                user.save()
                login(request, user)
                return redirect('setCycle')
            login(request, user)
            return redirect('spendingInsights')
        else:
            messages.error(request,"May be password is incorrect")

    return render(request,'registerLogin/registerLogin.html',{'page':page})




def logoutUser(request):
    logout(request)
    return redirect('login')




