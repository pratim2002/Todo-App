from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User

# Create your views here.
from users.forms import LoginForm, SignUpForm, ProfileEditForm, PasswordChangeForm


def dashboard(request):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    if user.is_admin():
        if request.COOKIES.get("uid"):
            #     context = {
            #         'cookie1': request.COOKIES['uid'],
            #         'cookie2': request.COOKIES['upw']
            # }
            return redirect('tasks:admin_task_list')
    if user.is_user():
        if request.COOKIES.get("uid"):
            print(request.COOKIES['uid'])
            return redirect('tasks:task_list')
        else:
            return redirect('tasks:task_list')


def user_login(request):
    next = request.GET.get('next', None)
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(data=request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            request.session['uid'] = request.POST['email']
            if request.POST.get("chk"):
                response = HttpResponse("cookie")
                response.set_cookie('uid', request.POST['email'])
                response.set_cookie('upw', request.POST['password'])
            user = authenticate(username=email, password=password)
            if user is None:
                messages.error(request, "Invalid login credentials")
                templates = 'users/login.html'
                return render(request, templates, context)
            else:
                login(request, user)
                if next:
                    return redirect(next)
                messages.success(request, 'Successfully logged in!')
                return redirect('dashboard')
    templates = 'users/login.html'
    return render(request, templates, context)


def user_signup(request):
    form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.role = 'user'
            instance.save()
            password = form.cleaned_data['password1']
            instance.set_password(password)
            instance.save()
            messages.success(request, 'sign up successfully'.format(instance.first_name))
            return redirect('login')
    template = "users/signup.html"
    return render(request, template, {'form': form})


@login_required
def user_password_change(request):
    """
    Change user password
    """
    form = PasswordChangeForm(data=request.POST or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully")
            return redirect('login')
    context = {
        'form': form
    }
    template = 'users/change_password.html'
    return render(request, template, context)


@login_required
def profile_edit_view(request, id=None):
    instance = get_object_or_404(User, id=id)
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.avatar is True:
            instance.avatar = request.FILES['avatar']
        instance.save()
        # profile_img = form.cleaned_data.get("avatar")
        # if profile_img and type(profile_img) != str:
        #     instance.profile_img = instance.save_img(profile_img)
        #     instance.save()
        return redirect("dashboard")

    template_name = "users/profile_edit.html"
    context = {
        "form": form,
        "instance": instance
    }
    return render(request, template_name, context)


def update_profile_ajax(request, id=None):
    instance = get_object_or_404(User, id=id)
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=instance)

    data = {}
    if request.is_ajax():
        if form.is_valid():
            form.save()
            data['first_name'] = form.cleaned_data.get('first_name')
            data['status'] = 'ok'
            return JsonResponse(data)
    context = {
        'form': form,
    }
    template = 'users/profile_edit_ajax.html'
    return render(request, template, context)


def user_logout(request):
    """
    Logout a user
    """
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


def set_cookie(request):
    responce = HttpResponse('cookie')
    responce.set_cookie('uid', 'user_email')
    responce.set_cookie('upw', 'user_password')


def get_cookie(request):
    uid = request.COOKIES['uid']
    upw = request.COOKIES['upw']
    return HttpResponse('user email' + uid)
