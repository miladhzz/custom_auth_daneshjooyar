from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import MyUser


def mobile_login(request):
    if request.method == "POST":
        if "mobile" in request.POST:
            mobile = request.POST.get('mobile')
            user = MyUser.objects.get(mobile=mobile)
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'mobile_login.html')


def dashboard(request):
    return render(request, 'dashboard.html')
