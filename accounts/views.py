import imp
from importlib.resources import contents
from pickle import NONE
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from shop.models import *
from django.contrib.auth import get_user_model
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username Has Already Been Taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords Must Match'})
    else:
        alluser = get_user_model().objects.all()
        context = {'allusers': alluser}
        return render(request, 'accounts/signup.html', context)


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or Password is Incorrect'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def profile(request, edit=""):
    if request.method == 'POST':
        address = request.POST['city']+'  '+request.POST['address']
        User.objects.filter(username=request.user).update(
            first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'])
        Profile.objects.filter(user=request.user).update(mobilephone=request.POST['mobilephone'],
                                                         address=address, postalCode=request.POST['postalcode'], phone=request.POST['phone'])
        return redirect('profile')
    else:
        if(edit == "edit"):
            editable = ""
        else:
            editable = "readonly"
        information = ''
        context = {'editable': editable, 'information': information}
    return render(request, 'accounts/profile.html', context)
