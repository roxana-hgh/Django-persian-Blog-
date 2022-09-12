from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, EditUserForm
from Blog.forms import ProfileForm
from Blog.models import Profile, Followers
from django.contrib import messages


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            Followers.objects.create(user=user)
            return redirect('login')
    return render(request, 'users/register.html',{'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('profile',pk = request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username , password = password)

        if user is not None:
            login(request,user),
            return redirect('profile',pk = request.user)
        else:
            messages.info(request,'Username or Password is incorrect')
            return render(request, 'users/login.html',)

    return render(request, 'users/login.html',)


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url = 'login')
def profile_edit(request):
    user = request.user
    profile = request.user.profile
    user_form = EditUserForm(instance=user)
    profile_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user )
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if (user_form.is_valid() and profile_form.is_valid()):
            profile_form.instance.user = request.user
            user_form.save()
            profile_form.save()
            return redirect('profile', pk=request.user)
    
    return render(request, 'users/edit_profile.html',{'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url = 'login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Something went wrong! Please try again. Make sure  to enter information carefully')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
})

