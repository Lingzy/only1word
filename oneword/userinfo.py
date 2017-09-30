from django.shortcuts import render_to_response, render

from django.http import HttpResponseRedirect, HttpResponse
from .models import Article, Comment, MyFavorite, MyLike
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


# 用户登录
def sign(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            return render(request, "sign.html", {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, "sign.html", {'form': form, })


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
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user:
                # 初始化收藏夹
                favorite = MyFavorite.objects.create(collector=user)
                favorite.save()

                # 登录网站
                login(request, user)
                # request.session['user'] = username
                return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form': form, })


# 用户修改密码
@login_required()
def change_pwd(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password1 = request.POST.get('new_password1', '')
        new_password2 = request.POST.get('new_password2', '')

        # 通过检查是否能登陆判断旧密码是否正确
        username = request.user.username
        user = authenticate(username=username, password=old_password)
        if not user:
            return JsonResponse({'status': 10021, 'message': 'Old password invalid'})

        # 修改密码

        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 200, 'message': 'change password success'})

    return JsonResponse({'status': 10023, 'message': 'please use post method'})
