import os
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
#Le decorateur interdit l'accès à des pages tt qu'on est pas connecté
from django.http import *
from django.views.generic import TemplateView
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail import send_mass_mail

from .models import *
from .forms import *

# Create your views here.

def index(request):
    template_name = 'pages/home.html'  ###Template de view correction
    corrections = Correction.objects.all()
    epreuves = Epreuve.objects.all()
    context ={
        'corrections' : corrections,
        'epreuves' : epreuves,
    }
    if(request.user.is_authenticated):
        return redirect('dashboard')
    return render(request=request, template_name=template_name, context=context)

def about(request, *args, **kwargs):
    return render(request, 'pages/about.html')

def contact(request, *args, **kwargs):
    return render(request, 'pages/contact.html')

def politique(request, *args, **kwargs):
    return render(request, 'pages/politiqueConfidentialite.html')

def using(request, *args, **kwargs):
    return render(request, 'pages/conditionUtilisation.html')

def profil(request):
    return render(request, 'users/profil.html' )

# Utilisateurs
class LoginView(TemplateView):

    template_name = 'users/login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL )
    
        return render(request, self.template_name)

class LogoutView(TemplateView):

  template_name = 'users/login.html'

  def get(self, request, **kwargs):
    logout(request)
    return render(request, self.template_name)

def dashboard(request):
    template_name = 'Biblio/dashboard.html'  ###Template de view correction
    corrections = Correction.objects.all()
    epreuves = Epreuve.objects.all()
    context ={
        'corrections' : corrections,
        'epreuves' : epreuves,
    }
    return render(request=request, template_name=template_name, context=context)

def create_user(request,*args,**kwargs):
    template_name= 'users/inscription.html'

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'GET':
        form = CustomUserCreationForm(
            initial={}
        )

        context = {'form': form,}

        return render(request=request,template_name=template_name,context=context,)
    
    if request.method == 'POST':
        form =CustomUserCreationForm(
           request.POST,
           request.FILES,
           initial={}
        )

        context = {'form': form, }
 
        if form.is_valid():
          print(form.cleaned_data)
          form.save()
          return redirect('home')
        return render(request=request,template_name=template_name,context=context,)
      
def update_user(request,*args,**kwargs):
    template_name= 'users/update_user.html'
    current_user = request.user
     
    obj = get_object_or_404(
        User,pk=current_user.id,
    )
    if request.method == 'GET':
        form = CustomUserChangeForm(
            initial={
              'email': obj.email,
              'is_active': obj.is_active,
              'is_fromEsmt': obj.is_fromEsmt,
              'is_newsletter': obj.is_newsletter,
          
            }
        )
        context = {
            'form': form,
        }
        return render(request=request,template_name=template_name,context=context,)
    
    if request.method == 'POST':
        form =CustomUserChangeForm(
           request.POST,
           request.FILES,
           initial={
              'email': obj.email,
              'is_active': obj.is_active,
              'is_fromEsmt': obj.is_fromEsmt,
              'is_newsletter': obj.is_newsletter,
             
            }
        )
        context = {
            'form': form,
        }
        if form.is_valid():
          print(form.cleaned_data)
          obj.is_fromEsmt = form.cleaned_data['is_fromEsmt']
          obj.is_newsletter = form.cleaned_data['is_newsletter']
          obj.save()
          return redirect('profil')
        return render(request=request,template_name=template_name,context=context,)
      
def changePassword_user(request,*args,**kwargs):
    template_name= 'users/change_password.html'
    current_user = request.user
    
    obj = get_object_or_404(
        User,pk=current_user.id,
    )
    if request.method == 'GET':
        form = passwordChangeForm(obj)
        context = {
            'form': form,
        }
        return render(request=request,template_name=template_name,context=context,)
    
    if request.method == 'POST':
        form =passwordChangeForm(obj,
           request.POST,
           request.FILES,
             initial={
            
            }
        )
        context = {
            'form': form,
        }
        if form.is_valid():
          print(form.cleaned_data)
          user = form.save
          update_session_auth_hash(request, user)  # Important!
          return redirect('home')
        return render(request=request,template_name=template_name,context=context,)

def newsletterTrue(request,*args,**kwargs):
    template_name= 'pages/contact.html'
    current_user = request.user
     
    obj = get_object_or_404(
        User,pk=current_user.id,
    )
    if request.method == 'GET':
        form = CustomUserChangeForm(
            initial={
              'email': obj.email,
              'is_active': obj.is_active,
              'is_fromEsmt': obj.is_fromEsmt,
              'is_newsletter': obj.is_newsletter,
          
            }
        )
        context = {
            'form': form,
        }
        return render(request=request,template_name=template_name,context=context,)
    
    if request.method == 'POST':
        form =CustomUserChangeForm(
           request.POST,
           request.FILES,
           initial={
              'email': obj.email,
              'is_active': obj.is_active,
              'is_fromEsmt': obj.is_fromEsmt,
              'is_newsletter': obj.is_newsletter,
             
            }
        )
        context = {
            'message': "Vous etes bien abonné a la newsletter !",
        }
        if form.is_valid():
          print(form.cleaned_data)
          obj.is_fromEsmt = form.cleaned_data['is_fromEsmt']
          obj.is_newsletter = True
          obj.save()
          send_mail(
            subject="elibrary newsletter",
            message="Bonjour, \n"+"Vous étes bien abonné a la newsletter de eLibrary ! \nCordialement eLibrary votre library favorite :)",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[obj.email],
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,)
          return render(request=request,template_name=template_name,context=context,)
        return render(request=request,template_name=template_name,context=context,)
# Epreuve

def add_epreuve(request, **kwargs):
    
    template_name = 'Biblio/add_epreuve.html' ###Template de add epreuve
    
    current_user = request.user
    obj = get_object_or_404(
        User,pk=current_user.id,
    )
    
    objet = Epreuve()
    
    if request.method == 'GET':
        form = EpreuveForm(
            initial={
              
            }
        )
        context = {
            'form': form
        }
        return render(
            request=request,
            template_name=template_name,
            context=context
        )
    
    if request.method == 'POST':
        form = EpreuveForm(request.POST, request.FILES)
        context = {
            'form': form,
        }
        if form.is_valid():
            print(form.cleaned_data)
            objet.intitulet = form.cleaned_data.get('intitulet')
            objet.matiere = form.cleaned_data.get('matiere')
            objet.filiere = form.cleaned_data.get('filiere')
            objet.professeur = form.cleaned_data.get('professeur')
            objet.file = request.FILES['file']
            objet.id_user = obj
            objet.save(force_insert=True)
            return redirect('dashboard')
        return render(request=request,template_name=template_name,context=context,)


         
    return render(request=request, template_name=template_name, context=context)

def list_epreuve(request):
    # Liste des épreuve les plus récentesS
    template_name = 'Biblio/dashboard.html'
    epreuves = Epreuve.objects.order_by('-id').all()
    corrections = Correction.objects.order_by('-id').all()
    context ={
        'epreuves' : epreuves,
        'corrections': corrections,
    }    
    return render(request=request, template_name=template_name, context=context)

def details_epreuve(request, pk):
    template_name = 'Biblio/details.html'  ###Template de view correction
    epreuve = Epreuve.objects.get(pk=pk)

    context = {
        'epreuve': epreuve,
    }
    return render(request=request, template_name=template_name, context=context)

def update_epreuve(request, *args, **kwargs):
    template_name = 'Biblio/update_epreuve.html' ###Template de update epreuve
    obj = get_object_or_404(
        Epreuve,
        pk = kwargs.get('pk')
    )
    if request.method == 'GET':
        form = EpreuveForm(
            initial={
                'intitulet': obj.intitulet,
                'matiere': obj.matiere,
                'filiere': obj.filiere,
                'professeur': obj.professeur,
                'file': obj.file,
            }
        )

        context = { 'form': form }

        return render(request=request,template_name=template_name,context=context)

    if request.method == 'POST':
        form = EpreuveForm(
            request.POST,
            request.FILES,
            initial={
                'intitulet': obj.intitulet,
                'matiere': obj.matiere,
                'filiere': obj.filiere,
                'professeur': obj.professeur,
                'file': obj.file,
            }
        )

        context = {'form': form }

        if form.is_valid():
            print(form.cleaned_data)
            obj.intitulet = form.cleaned_data.get('intitulet')
            obj.matiere = form.cleaned_data.get('matiere')
            obj.filiere = form.cleaned_data.get('filiere')
            obj.professeur = form.cleaned_data.get('professeur')
            if obj.file != form.cleaned_data.get('file'):
                obj.deleteFile()
            obj.file = form.cleaned_data.get('file')
            obj.save()
            return redirect('dashboard') ###Template de view epreuve
        
        return render(request=request, template_name=template_name ,context=context)

def delete_epreuve(request, *args, **kwargs):
    # template_name = 'Biblio/delete_epreuve.html'  ###Template de suppression 
    obj = get_object_or_404(
        Epreuve,
        pk = kwargs.get('pk')
    )
    obj.delete()
    return redirect("dashboard") ###Template de view epreuve
    
#### Correction

def add_correction(request, **kwargs):
    template_name = 'Biblio/add_correction.html' ###Template de add correction
    current_user = request.user
    obj1 = get_object_or_404(
        User,pk=current_user.id,
    )

    obj = get_object_or_404(
        Epreuve,
        pk = kwargs.get('pk'),
    )
    objet = Correction()
    if request.method == 'GET':
        form = CorrectionForm(
            initial={
            }
        )
        context = {
            'form': form
        }
        return render(
            request=request,
            template_name=template_name,
            context=context
        )
        
    if request.method == 'POST':
        form = CorrectionForm(
            request.POST,
            request.FILES,
            initial={
            }
        )
        context = {
            'form': form
        }
        if form.is_valid():
            print(form.cleaned_data)
            objet.intitulet = form.cleaned_data.get('intitulet')
            objet.file = request.FILES['file']
            objet.id_user = obj1
            objet.id_epreuve = obj
            objet.save()
            return redirect('dashboard')
        return render(request=request,template_name=template_name,context=context,)

def list_correction(request, **kwargs):
    template_name = 'Biblio/correction.html'  ###Template de view correction
    corrections = Correction.objects.order_by('-id').all()
    context ={
        'corrections' : corrections,
    }  
    return render(request=request, template_name=template_name, context=context)

def correction_byId(request, **kwargs):
    template_name = 'Biblio/view_correction.html'  ###Template de view correction

def correction_byEpreuveId(request, **kwargs):
    template_name = 'Biblio/correction.html'  ###Template de view correction
    obj = get_object_or_404(
        Epreuve,
        pk = kwargs.get('pk')
    )
    corrections = Correction.objects.filter(id_epreuve=obj.id).order_by('-id')
    context ={
        'corrections' : corrections,
        'epreuve': obj,
    }
         
    return render(request=request, template_name=template_name, context=context)

def update_correction(request, *args, **kwargs):
    template_name = 'Biblio/update_correction.html' ###Template de update correction
    obj = get_object_or_404(
            Correction,
            pk = kwargs.get('pk')
        )
    if request.method == 'GET':
        form = CorrectionForm(
            initial={
                'intitulet': obj.intitulet,
                'file': obj.file,
                }
        )
        context = { 'form': form }   
        return render(
            request=request,
            template_name=template_name,
            context=context
            )
            
    if request.method == 'POST':
        form = CorrectionForm(
                request.POST,
                request.FILES,
                initial={
                'intitulet': obj.intitulet,
                'file': obj.file,
                }
            )
        context = { 'form': form }
        if form.is_valid():
                print(form.cleaned_data)
                obj.intitulet = form.cleaned_data.get('intitulet')
                if obj.file != form.cleaned_data.get('file'):
                    obj.deleteFile()
                obj.file = form.cleaned_data.get('file')
                obj.save()
                return redirect('corrections' ,pk=obj.id_epreuve.id) ###Template de view correction

def delete_correction(request, *args, **kwargs):
    template_name = 'Biblio/delete_epreuve.html' ######Template de suppression
    obj = get_object_or_404(
        Correction,
        pk = kwargs.get('pk')
    )
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("dashboard") ###Template de view correction
    return render(
        request=request,
        template_name=template_name
        )
    
#download

def download(request, *args, **kwargs):
    path=kwargs.get('path')
    file_path = "files/" + path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
        
    # return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL )
    raise Http404

#mail
def sendEmail(request, *args, **kwargs):
    template_name = 'users/newsletter.html'
    users= User.objects.all().filter(is_newsletter=True)
    usersEMAIL=list(users)
    
    if not request.user.is_staff:
        raise Http404
    
    if request.method == 'GET':
        return render(request=request,template_name=template_name)
    
    if request.method == 'POST':
        subject=request.POST.get('subject', False)
        body=request.POST.get('body', False)
        context = {
            'message': 'Mail envoyé aux abonnés de la newsletter',
        }
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=usersEMAIL,
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,)
        return render(request=request, template_name=template_name,context=context)
        
    return render(request=request, template_name=template_name,context=context)
