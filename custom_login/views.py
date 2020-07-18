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
                helper.send_otp_soap(mobile, otp)
                # save otp
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
                helper.send_otp_soap(mobile, otp)
                # save otp
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))
    return render(request, 'register.html', {'form': form})


def verify(request):
    mobile = request.session.get('user_mobile')
    return render(request, 'verify.html', {'mobile': mobile})

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
