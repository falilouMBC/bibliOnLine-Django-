"""myProjet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Biblio.views import *
# from . import vie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from Biblio.forms import loginForm
from django.conf.urls.static import static

urlpatterns = [
#admin
    path('admin/', admin.site.urls),
    path('newsletter',login_required(sendEmail),name='newsletter'),
#visiteur
    path('accounts', include('django.contrib.auth.urls')),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('privacy-policy/', politique, name='politique'),
    path('terms/', using, name='using'),
    path('profil', profil, name='profil'),

#Users  
    path('login/', views.LoginView.as_view(template_name='users/login.html', authentication_form=loginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('inscription/', create_user, name='inscription'),
    path('profil/update_user/', login_required(update_user), name='update'),
    path('profil/change_password/', login_required(changePassword_user), name='password'),
    path('contact/abonnement',login_required(newsletterTrue),name='newsletterTrue'),
#Epreuve
    path('bibliotheque/dashboard/', login_required(dashboard), name='dashboard'),
    path('bibliotheque/new_epreuve/',  login_required(add_epreuve), name='new_epreuve'),
    path('bibliotheque/epreuve/<int:pk>', login_required(details_epreuve), name='details_epreuve'),
    path('bibliotheque/update/epreuve/<int:pk>', login_required(update_epreuve), name='update_epreuve'),
    path('bibliotheque/delete/epreuve/<int:pk>', login_required(delete_epreuve), name='delete_epreuve'),
   
#Correction
    path('bibliotheque/add_correction/epreuve/<int:pk>',  login_required(add_correction), name='add_correction'),
    path('bibliotheque/corrections/epreuve/<int:pk>', login_required(correction_byEpreuveId),name = 'corrections'),
    path('bibliotheque/update/correction/<int:pk>/', login_required(update_correction), name='update_correction'),
    path('bibliotheque/list_correction/<int:pk>', login_required(list_correction), name='list_correction' ),
    path('bibliotheque/delete/correction/<int:pk>', login_required(delete_epreuve), name='delete_correction'),

    path('download/files/<str:path>/',login_required(download), name='download'),
    
]+ static('read/files/', document_root='files/')
