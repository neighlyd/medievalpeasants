from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login
from django.views.generic import TemplateView

# Create your views here.


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    return render(request)

class TemporaryRegistration(TemplateView):
    template_name = 'temp_registration.html'