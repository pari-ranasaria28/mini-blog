from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,SignInForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def about(request):
    return render(request,'blog/about.html')


def contact(request):
    return render(request,'blog/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request,'blog/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/')


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations! You have became an author now....")
            form.save()
    else:
        form = SignUpForm()
    return render(request,'blog/signup.html',{'form':form})


def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else:
        if request.method == "POST":
            form = SignInForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upassword = form.cleaned_data['password']
                user = authenticate(username=uname,password=upassword)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged in Successfully !!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = SignInForm()
        return render(request,'blog/signin.html',{'form':form})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')