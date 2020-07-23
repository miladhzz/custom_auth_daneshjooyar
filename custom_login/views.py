from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import MyUser
from . import forms
from . import helper


def register_view(request):
    form = forms.RegisterForm

    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = MyUser.objects.get(mobile=mobile)
                # send otp
                otp = helper.get_random_otp()
                # helper.send_otp(mobile, otp)
                # helper.send_otp_soap(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))

        except MyUser.DoesNotExist:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = helper.get_random_otp()
                # helper.send_otp(mobile, otp)
                # helper.send_otp_soap(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))
    return render(request, 'register.html', {'form': form})


def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        user = MyUser.objects.get(mobile = mobile)

        if request.method == "POST":

            # check otp expiration
            if not helper.check_otp_expiration(user.mobile):
                return HttpResponseRedirect(reverse('register_view'))

            if user.otp != int(request.POST.get('otp')):
                return  HttpResponseRedirect(reverse('register_view'))

            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))

        return render(request, 'verify.html', {'mobile': mobile})

    except MyUser.DoesNotExist:
        return HttpResponseRedirect(reverse('register_view'))


# def mobile_login(request):
#     if request.method == "POST":
#         if "mobile" in request.POST:
#             mobile = request.POST.get('mobile')
#             user = MyUser.objects.get(mobile=mobile)
#             login(request, user)
#             return HttpResponseRedirect(reverse('dashboard'))
#
#     return render(request, 'mobile_login.html')


def dashboard(request):
    return render(request, 'dashboard.html')
