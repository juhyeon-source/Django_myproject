from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    AuthenticationForm, 
    UserCreationForm,
    PasswordChangeForm,)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

@require_http_methods(["GET","POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("products:product_list")
    else:
        form = AuthenticationForm()
    context = {'form' : form }
    return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("products:product_list")

@require_http_methods(["GET","POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("products:product_list")
    else:
        form = CustomUserCreationForm()
    context = {"form" : form}
    return render(request, "accounts/signup.html", context)

@require_POST
def leave(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('products:product_list')

@require_http_methods(["GET","POST"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid:
            form.save()
            return redirect('products:product_list')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form" : form}
    return render(request, 'accounts/update.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('products:product_list')
    else:
        form = PasswordChangeForm(request.user)
    context = {"form" : form}
    return render(request, 'accounts/change_password.html', context)



def users(request):
    return render(request, "accounts/users.html")


def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username) # 1. 유저 모델,  2. 유저네임
    context = {
        "member": member,
    }
    return render(request, "accounts/profile.html", context)


@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if request.user in member.followers.all():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("accounts:profile", member.username)
    return redirect("accounts:login")







