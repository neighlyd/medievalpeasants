from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView

from .forms import ProfileSignupForm

# Create your views here.

class ProfileCreateView(CreateView):
    form_class = ProfileSignupForm
    template_name = 'signup_form.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return super(ProfileCreateView, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        valid = super(ProfileCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class TemporaryRegistration(TemplateView):
    template_name = 'temp_registration.html'


def logout(request):
    return render(request)
