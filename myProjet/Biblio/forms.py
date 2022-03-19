import array
from cProfile import label
import email
import gettext
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Epreuve, User


class CustomUserCreationForm(UserCreationForm,forms.Form):
    email=forms.CharField(label='E-mail ',required=True, max_length=200, strip=True, min_length=2,
         widget=forms.TextInput(
            attrs={
                'type':'email',
                'class': 'form-control mb-3',
                'placeholder': 'Adresse e-mail',
            }
        )
    )
    password1=forms.CharField(label='Mot de passe',required=True, max_length=200, strip=True, min_length=2,
         widget=forms.PasswordInput(
            attrs={
                'type':'password',
                'class': 'form-control col-6',
                'placeholder': 'Mot de passe',
            }
        )
    )
    password2=forms.CharField(label='',required=True, max_length=200, strip=True, min_length=2,
         widget=forms.PasswordInput(
            attrs={
                'type':'password',
                'class': 'form-control col-6',
                'placeholder': 'Confirmer le mot de passe',
            }
        )
    )
    is_fromEsmt= forms.BooleanField(required=False, label= "Etudiant de L'ESMT",
        widget=forms.CheckboxInput(
            attrs={
                'type': 'checkbox',
                }
            )
        )
    is_newsletter=forms.BooleanField(required=False,label="S'abonner a la newsletter",
        widget=forms.CheckboxInput(
            attrs={
                'type': 'checkbox',
                }
            )
        )
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'is_fromEsmt','is_newsletter')
        

class CustomUserChangeForm(UserChangeForm,forms.Form):
    password = forms.Field(required=False,label='',
         widget=forms.HiddenInput(
            attrs={
                'type':'hidden',
            }
        ))
    is_fromEsmt= forms.BooleanField(required=False,label="Etudiant de L'ESMT",widget=forms.CheckboxInput(attrs={'type': 'checkbox'}))
    is_newsletter=forms.BooleanField(required=False,label="S'abonner a la newsletter",widget=forms.CheckboxInput(attrs={'type': 'checkbox'}))
    class Meta:
        model = User
        fields = ()

class passwordChangeForm(PasswordChangeForm,forms.Form):
    old_password = forms.CharField(label='', max_length=200, strip=True, min_length=2,
         widget=forms.PasswordInput(
            attrs={
                'type':'password',
                'class': 'form-control',
                'placeholder': 'Ancien mot de passe',
            }
        )
    )
    new_password1 = forms.CharField(label='', max_length=200, strip=True, min_length=2,
         widget=forms.PasswordInput(
            attrs={
                'type':'password',
                'class': 'form-control',
                'placeholder': 'Nouveau mot de passe',
            }
        )
    )
    new_password2 = forms.CharField(label='', max_length=200, strip=True, min_length=2,
         widget=forms.PasswordInput(
            attrs={
                'type':'password',
                'class': 'form-control',
                'placeholder': 'Confirmer mot de passe',
            }
        )
    )
    class Meta:
        model=User
        fields = ('old_password', 'new_password1', 'new_password2')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

########################################################################################################

class EpreuveForm(forms.ModelForm):
    intitulet = forms.CharField(
        label='',
        max_length=200,
        strip=True,
        min_length=2,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Entrez l\'intitulet',
            }
        )
    )

    matiere = forms.ChoiceField(
        label='Matiere ',
        required=True,
        choices=[(x,y) for(x,y) in settings.MATIERES],
        widget=forms.Select(
            attrs={
                'type': 'select',
                'class': 'form-control',
                'placeholder': 'Entrez le nom de la matière ',

            }
        )
    )
    filiere = forms.CharField(
        label='',
        max_length=200,
        strip=True,
        min_length=2,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Entrez la filière',
            }
        )
    )
    professeur = forms.CharField(
        label='',
        max_length=200,
        strip=True,
        min_length=2,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Entrez le nom du professeur',
            }
        )
    )
    file = forms.FileField(
        label='',
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-control',
            }

        )
    )
    
    class Meta: 
        model = Epreuve
        fields = ['intitulet', 'filiere', 'matiere', 'professeur', 'file']
        
class CorrectionForm(forms.ModelForm):
    intitulet = forms.CharField(
        label='',
        max_length=200,
        strip=True,
        min_length=2,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Entrez l\'intitulet',
            }
        )
    )
    file = forms.FileField(
        label='',
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-control',
            }
        )
    )
    
    class Meta: 
        model = Epreuve
        fields = ['intitulet', 'file']

class loginForm(AuthenticationForm):
    username = forms.CharField(label='', max_length=200, strip=True, min_length=2,
         widget=forms.TextInput(
            attrs={
                'type':'text',
                'class': 'form-control',
                'placeholder': 'Adresse e-mail',
            }
        )
    )

    password = forms.CharField(
        label='',
        required = True, min_length=1, max_length=30,
        widget = forms.PasswordInput(
            attrs = {
                'type': 'password',
                'class': 'form-control',
                'placeholder': 'Mot de passe',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password')