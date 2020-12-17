from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth, messages
from accounts.models import Account


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


def loginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(
            email=email,
            password=password
        )

        if user is not None:
            auth.login(request, user)
            return None
        else:
            messages.error(request, "Invalid User/Password")
            return redirect("/")
    else:
        return render(request, 'accounts/login.html')

def signupView(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if Account.objects.filter(email=email).exists():
                messages.error(request, "Already have an account with the Email")
                return redirect('accounts:signup')
            if Account.objects.filter(username=username).exists():
                messages.error(request, "User name exists, Please choose aomething else")
                return redirect('accounts:signup')
            else:
                user = Account.objects.create_user(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    DOB=dob,
                    password=password1
                )

                user.save()
                messages.info(request, "Account has been successfully created")
                return redirect('/')

        else:
            messages.error(request, "Passwords ar not matching")
            return redirect('accounts:signup')
    
    else:
        return render(request, 'accounts/signup.html')
        