from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
# from django.contrib.auth.models import User
from django.contrib import messages
from authentication.forms import RegistrationForm, LoginForm
from authentication.models import User


# homepage
def reward_home_view(request):
    return render(request, "rewards/index.html")


"""
---------------------
login_signup_view: 
---------------------
description:
    login and signup page
    if POST & sign up button has been clicked => save form into database and redirect to profile page.
    if GET => Rendering webpage with LoginForm and RegistrationForm
"""


def login_signup_view(request):
    context = {}
    register_form = RegistrationForm()
    login_form = LoginForm()
    context['registration_form'] = register_form
    context['login_form'] = login_form
    if request.method == "POST":
        if request.POST.get('submit') == 'sign_up':
            register_form = RegistrationForm(request.POST, request.FILES)
            if register_form.is_valid():
                register_form.save()
                user = register_form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)
                return redirect("login-signup")
            else:
                context['registration_form'] = register_form
    return render(request, "rewards/login-signup.html", context)


"""
---------------------
sign_out: 
---------------------
description:
    sign user out
    there should be a button to allowed sign out actions
"""


def sign_out(request):
    pass


"""
---------------------
user_profile_view: 
---------------------
description:
    user profile page
    if POST & submit request equal to add_points => update user's current green point in database
    if POST & submit request equal to sign_in => sign user in, authenticate form and refresh profile page
"""


def user_profile_view(request):
    if request.method == "POST":
        # if request.POST.get('submit') == 'add_points':
        #     user = User.objects.get(phone_number=request.POST.get("user_id"))
        #     user.green_point += 10
        #     user.save()
        #     context = {
        #         'object': user
        #     }
        #     return render(request, 'rewards/user_profile.html', context)
        if request.POST.get('submit') == 'sign_in':
            phone_number = request.POST.get('username')
            raw_password = request.POST.get('password')
            user = authenticate(request, phone_number=phone_number, password=raw_password)
            if user is not None:
                login(request, user)
                obj = User.objects.get(phone_number=user.phone_number)
                context = {
                    'object': obj
                }
                return render(request, "rewards/user_profile.html", context)
            else:
                messages.info(request, 'Phone number OR password is incorrect')
    return render(request, 'rewards/user_profile.html', {})
