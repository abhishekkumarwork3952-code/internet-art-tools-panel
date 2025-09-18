from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import UserAccount

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user exists in UserAccount
        try:
            user_account = UserAccount.objects.get(user_id=username, password=password, status=True)
            
            # Check if user is already logged in
            if user_account.is_logged_in:
                messages.error(request, f'User {username} is already logged in from another session!')
                return redirect('login')
            
            # Authenticate with Django's built-in auth
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Update UserAccount with session details
                device_ip = request.META.get('REMOTE_ADDR', 'Unknown')
                user_account.login_user(request.session.session_key, device_ip)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        except UserAccount.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'users/login.html')

@login_required
def dashboard(request):
    users = UserAccount.objects.all().order_by('user_id')
    msg = request.GET.get('msg')
    return render(request, 'users/dashboard.html', {'users': users, 'msg': msg})

@login_required
def logout_view(request):
    # Update UserAccount logout status
    try:
        user_account = UserAccount.objects.get(user_id=request.user.username)
        user_account.logout_user()
    except UserAccount.DoesNotExist:
        pass
    
    logout(request)
    return redirect('login')

@login_required
def create_user(request):
    if request.method == 'POST':
        uid = request.POST.get('user_id')
        pwd = request.POST.get('password')
        if uid and pwd:
            UserAccount.objects.create(user_id=uid, password=pwd, status=True)
            return redirect('/dashboard/?msg=User+created')
    return redirect('/dashboard/?msg=Missing+fields')

@login_required
def enable_user(request, user_id):
    u = get_object_or_404(UserAccount, user_id=user_id)
    u.status = True
    u.save()
    return redirect('/dashboard/?msg=Enabled')

@login_required
def disable_user(request, user_id):
    u = get_object_or_404(UserAccount, user_id=user_id)
    u.status = False
    u.save()
    return redirect('/dashboard/?msg=Disabled')

@login_required
def delete_user(request, user_id):
    u = get_object_or_404(UserAccount, user_id=user_id)
    u.delete()
    return redirect('/dashboard/?msg=Deleted')

@login_required
def force_logout(request, user_id):
    u = get_object_or_404(UserAccount, user_id=user_id)
    u.logout_user()
    return redirect('/dashboard/?msg=User+logged+out')
