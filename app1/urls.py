from django.urls import  path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('home',views.home,name='home'),
    path('logout',views.logout,name='logout'),
    path('addclient',views.addClient,name='addclient'),
    path('addsubclient',views.addSubClient,name='addsubclient'),
    path('showSubclients/<int:id>/',views.showSubclients,name='showsubclients')

]
