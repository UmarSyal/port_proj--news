from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import messages

from accounts.forms import SignUpForm
from accounts.models import UserPreference

# Create your views here.
class SignUpView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'accounts/sign_up.html'
    success_url = reverse_lazy('news:accounts:sign_in')
    form_class = SignUpForm
    success_message = 'Thank you for joining us. You can set your preferences in your profile settings after Signing In.'

    # allow access to this view only if no user is logged in
    def test_func(self):
        return not self.request.user.is_authenticated

    # if a logged in user tries to access, redirect them to homepage
    def handle_no_permission(self):
        return redirect(reverse_lazy('news:news_list'))

    # create a UserPreference for this new user which they can update later on
    def form_valid(self, form):
        user = form.save()
        user_preferences = UserPreference.objects.create(user=user)
        return super().form_valid(form)


class SignInView(UserPassesTestMixin, SuccessMessageMixin, LoginView):
    template_name = 'accounts/sign_in.html'
    success_message = 'You are logged in. News are filtered based on your preferences.'

    # allow access to this view only if no user is logged in
    def test_func(self):
        return not self.request.user.is_authenticated

    # if a logged in user tries to access, redirect them to homepage
    def handle_no_permission(self):
        return redirect(reverse_lazy('news:news_list'))


class SignOutView(SuccessMessageMixin, LogoutView):
    success_message = 'Thank you for visiting. Login again for better user experience.'

    # LogoutView doesn't have message support so do it manualy
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.SUCCESS, self.success_message)
        return response


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('news:accounts:change_password')
    success_message = 'Your password was changed successfully.'


class UserPreferenceView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserPreference
    template_name = 'accounts/preferences.html'
    fields = ('category', 'provider',)
    success_message = 'Your preferences were updated successfully.'