from django.shortcuts import render_to_response,render

from django.http import HttpResponseRedirect,HttpResponse
from .models import Article,Comment,MyFavorite
from django.http import JsonResponse

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


# 用户登录
def sign(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request, user)
                request.session['user'] = username
                return HttpResponseRedirect("/")
        else:
            return render(request,"sign.html",{'form':form})
    else:
        form = AuthenticationForm()
    return render(request,"sign.html", {'form': form,})


# 用户退出
@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/')


# 用户注册
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)

            if user:
                login(request,user)
                request.session['user'] = username
                return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request,"register.html", {
        'form': form,
    })


# 用户修改密码
@login_required()
def change_pwd(request):
    if request.method == 'POST':
        old_pwd = request.POST.get('old_pwd','')
        new_pwd = request.POST.get('new_pwd','')
        username = request.session.get('username','')

        user = authenticate(username=username,password=old_pwd)

        if user:
            user = User.objects.get(username = username)
            user.password = new_pwd
            user.save()
            return JsonResponse({'status':200,'message':'password changed success'})
        else:
            return JsonResponse({'status':10025,'message':"Old password wrong"})

    return JsonResponse({'status':10021,'message':'parameter error'})

