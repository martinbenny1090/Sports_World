from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Item, OrderItem, Order

# def owner(request):
#     return render(request, 'owner.html')

def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'home.html', context)

    
def product(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email,password=password)

        if user is not None:
            auth.login(request, user)
            if User.objects.filter(username=email, is_superuser="True").exists():
                messages.info(request,'Admin page')
                return render(request, 'owner/owhome.html')
            else:
                # auth.login(request, user)
                return redirect("/")

        else:
            messages.info(request,'Invalied Login')
            return redirect('login')

    else:
        return render(request, 'login.html')
    

#register 
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']

        if User.objects.filter(username=email).exists():
            # print('user taken')
            messages.info(request,'E-mail Id already using')
            return redirect('/Register')

        else:    
            user = User.objects.create_user(username=email, password=password1, email=email,first_name=name)
            user.save();
            print('user crested')
            return redirect('login')

    else:
        return render(request, 'Register.html')





def offer(request):
    return render(request, 'offer.html')

def about(request):
    return render(request, 'about-us.html')

def contact(request):
    return render(request, 'contact-us.html')