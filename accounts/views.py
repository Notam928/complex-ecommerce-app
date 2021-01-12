from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from accounts.forms import UserLoginForm, UserSignupForm


class UserLoginView(LoginView):
    
    form_class = UserLoginForm
    authentication_form = UserLoginForm
    redirect_authenticated_user = True
    #gabarit
    template_name = "accounts/login.html"
    
    def form_valid(self, form):
        #form_login = UserLoginForm(self.request.POST)
        remember_me = self.request.POST.get("rememberme")
        if not remember_me:
            # session expire when use close browser
            self.request.session.set_expiry(1209600)
            self.request.session.modified = True
        return super(UserLoginView, self).form_valid(form)
    


class UserSignupView(CreateView, LoginView):
    """
    View for creation user account
    """
    template_name ="accounts/signup.html"
    success_url = reverse_lazy("core:index")
    form_class = UserSignupForm     
    redirect_authenticated_user = True   
    
    
    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
    
    