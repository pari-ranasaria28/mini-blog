from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import SignUpForm,SignInForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

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
        user = request.user
        full_name = user.get_full_name()
        group = user.groups.all()
        ip = request.session.get('ip',0)
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':group,'ip':ip})
    else:
        return HttpResponseRedirect('/login/')


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations! You have became an author now....")
            user = form.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
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


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                post = Post(title=title,desc=desc)
                post.save()
                messages.success(request,"Post added successfully")
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    

def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=post)
            if form.is_valid():
                form.save()
                messages.success(request,"Post updated successfully")
                return HttpResponseRedirect('/dashboard/')
        else:
            post = Post.objects.get(pk=id)
            form=PostForm(instance=post)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                post = Post.objects.get(pk=id)
                post.delete()
                messages.success(request,"Post deleted successfully ")
                return HttpResponseRedirect('/dashboard/')
            else:
                return redirect('/no_permission/')
        else:
            return redirect('/no_permission/')
    else:
        return HttpResponseRedirect('/login/')
    

def no_permission(request):
    return render(request,'blog/nopermission.html')