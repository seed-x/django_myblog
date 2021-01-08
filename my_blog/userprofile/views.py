from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检查账号，密码是否和数据库中的用户匹配
            # 匹配返回user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在session中，实现登录动作
                # 登陆后跳转
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入有误， 请重新输入。")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 用户退出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            #注册成功，保存好数据后就登陆跳转到博客列表页面
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误， 请重新输入。")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据。")


# 调用此函数必须登录，未登录则重定向到登录接口
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("请使用POST请求。")


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
                print(profile.avatar)
            profile.save()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入。")
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile':profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据。")