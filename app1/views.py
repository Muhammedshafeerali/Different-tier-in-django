from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,Permission
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib import messages
from .models import Client,Subclient
from django.contrib.auth.decorators import login_required,permission_required
from .decorators import uauthenticateduser


# Create your views here

@uauthenticateduser
def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    elif request.method == 'POST':
        username=request.POST['username']
        password =request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            auth_login(request,user)
            return redirect(home)
            
            
        else:
            messages.info(request,'invalid credentil')
            

    return render(request,'login.html')



@login_required(login_url='/')
def home(request):

    user = User.objects.get(username=request.user.username)
    if user.is_superuser:
        clients=Client.objects.all()
        return render(request,'home.html',{'clients':clients})
    elif Client.objects.filter(user=user).exists():
        client=Client.objects.get(user=user)
        subClients=Subclient.objects.filter(client=client) 
        return render(request,'home.html',{'subclients':subClients,'client':client})
    else:
        subClient=Subclient.objects.get(user=user)

        return render(request,'home.html',{'subClient':subClient})




def logout(request):
    auth_logout(request)
    return render(request,'login.html')


def addClient(request):
    if request.user.is_superuser:

        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            if User.objects.filter(username=username).exists():
                    messages.info(request,'username already taken')
                    return render(request,'addclient.html')
            else:

                user=User.objects.create_user(username=username,password=password)
                client=Client.objects.create(user=user)
                permission=Permission.objects.get(codename='add_subclient')
                user.user_permissions.add(permission)
                return redirect(home)
        
        return render(request,'addclient.html')
    else:
        return HttpResponse('YOU HAVE NO PERMISSION')




@login_required(login_url='/')
@permission_required('app1.add_subclient',raise_exception=True)
def addSubClient(request):
    user=User.objects.get(username=request.user.username)
    client=Client.objects.get(user=user)
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request,'username already taken')
            return render(request,'addsubclient.html')
        else:

            user=User.objects.create_user(username=username,password=password)
            subclient=Subclient.objects.create(user=user,client=client)
            return redirect(home)

    return render(request,'addsubclient.html')

@login_required(login_url='/')
def showSubclients(request,id):
    if request.user.is_superuser:

        client=Client.objects.get(id=id)
        subclients=Subclient.objects.filter(client=client)
        return render(request,'showclient.html',{'subclients':subclients})
    
    else:
        return HttpResponse('No Permission')

    







