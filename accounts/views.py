# from django.shortcuts import render
# from django.test import TestCase
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
# from .forms import LoginForm
# # Create your tests here.
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(request,
#                                 username = data['username'],
#                                 password = data['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse("Zo'r boldi")
#                 else:
#                     return HttpResponse("bumepti")
#
#             else :
#                 return HttpResponse('xato bor')
#         form = LoginForm()
#         context = {
#             'form':form
#         }
#
#     return render(request, 'account/login.html', context )
#
#
#

from idlelib.autocomplete import FILES

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    context = {'form': LoginForm()}  # `context` ni oldindan aniqlash

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Zo'r boldi")
                else:
                    return HttpResponse("bumepti")
            else:
                return HttpResponse('xato bor')

        # Agar forma noto‘g‘ri bo‘lsa, uni kontekstga qo‘shish
        context['form'] = form

    return render(request, 'registration/login.html', context)
@login_required
def dashboard_view(request):
    user = request.user
    # profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        # 'profile':profile
    }

    return render(request, 'page/dashboard.html', context)

def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            context = {
                'new_user':new_user

            }
            Profile.objects.create(user=new_user)
            return render(request, 'account/register.html', context)
    else:
        user_form = UserRegistrationForm
    return render(request, 'account/register_done.html', {'user_form':user_form})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register_done.html'
@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile_edit.html', {
        'user_form': user_form,  # TO‘G‘RI
        'profile_form': profile_form  # XATO: 'profile_form:' → TO‘G‘RI: 'profile_form'
    })

class EditUserView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'account/profile_edit.html', {
        'user_form': user_form,  # TO‘G‘RI
        'profile_form': profile_form  # XATO: 'profile_form:' → TO‘G‘RI: 'profile_form'
    })


    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

