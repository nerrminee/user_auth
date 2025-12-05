from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST


def home(request):
    signup_form = SignupForm()
    context = {'signup_form': signup_form}

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('home')
            else:
                context['signup_form'] = signup_form

        if 'login' in request.POST:
            username = request.POST.get('login-username')
            password = request.POST.get('login-password')
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.full_name or user.username
                    messages.success(request, f'Welcome back, {user.full_name or user.username}!')
                    return redirect('welcome')
                else:
                    messages.error(request, 'Invalid infos.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid infos.')

    return render(request, 'users/home.html', context)


def welcome(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('home')
    context = {'user_name': user.full_name or user.username}
    return render(request, 'users/welcome.html', context)


@require_POST
def logout_view(request):
    
    request.session.pop('user_id', None)
    request.session.pop('user_name', None)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@require_POST
def delete_account(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        request.session.pop('user_id', None)
        request.session.pop('user_name', None)
        messages.success(request, f'Account {username} has been deleted.')
    except User.DoesNotExist:
        pass
    return redirect('home')