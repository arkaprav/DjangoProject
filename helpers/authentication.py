from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
#handles login requests 
def login_req(request):
    username = request.POST.get('username')
    password = request.POST.get('password1')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        previous_url = request.session.pop('previous_url', None)
        if previous_url:
            response = redirect(previous_url)# Redirect to the user's profile page after successful registration
            expiration_time = datetime.now() + timedelta(days=30)  
            response.set_cookie('user_id', user.id, expires=expiration_time)
            return response
        else:
            response = redirect('profile')
            expiration_time = datetime.now() + timedelta(days=30)  
            response.set_cookie('user_id', user.id, expires=expiration_time)
            return response
    redirect('login')