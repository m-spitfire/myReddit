from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .tokens import account_activation_token
from posts.models import Post


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            subject = 'Activate your account on myReddit'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'userid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('users:email_verification_done')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def email_verification_confirm(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.verified_email = True
        user.save()
        login(request, user)
        return redirect('posts:posts_home')
    else:
        return render(request, 'users/account_activation_invalid.html')


def email_verification_done(request):
    return render(request, 'users/email_verification_done.html')


@login_required
def profile_edit(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/profile_edit.html', context=context)


@login_required
def profile(request):
    context = {
        'posts': Post.objects.filter(author=request.user),
    }
    return render(request, 'users/profile.html', context=context)
