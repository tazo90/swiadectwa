#coding: utf-8

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags

from .models import Profil, Uczen, Szkola, Klasa, Uczen_w_klasie, Swiadectwo, Pole

class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Nazwa użytkownika'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))


class UserCreateForm(UserCreationForm):    
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Imie'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Nazwisko'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Pesel'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        model = User


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['rola']

class UczenForm(forms.ModelForm):
    class Meta:
        model = Uczen  
        fields = ['dataUr', 'miejsceUr', 'plec']              

    def __init__(self, *args, **kwargs):        
        super(UczenForm, self).__init__(*args, **kwargs)
        self.fields['dataUr'].widget.attrs['placeholder'] = 'Data urodzenia dd.mm.yyyy'
        self.fields['miejsceUr'].widget.attrs['placeholder'] = 'Miejsce urodzenia'        

        #### Labels ####
        self.fields['dataUr'].label = 'Data urodzenia'
        self.fields['miejsceUr'].label = 'Miejsce urodzenia'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Pesel'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Imie'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'

class SzkolaForm(forms.ModelForm):
    class Meta:
        model = Szkola

    def __init__(self, *args, **kwargs):
        super(SzkolaForm, self).__init__(*args, **kwargs)
        self.fields['nazwa'].label = 'Nazwa szkoły'
        self.fields['nr'].label = 'Numer szkoły'
        self.fields['miejscowosc'].label = 'Miejscowość'

class KlasaForm(forms.ModelForm):
    class Meta:
        model = Klasa
        fields = ['klasa'] 

       
""" !!! PRZYDATNE - drop downa wypenia danymi z bazy!!!
class SzkolaKlasaForm(forms.Form):
    SZKOLY = [('', u'-- wybierz szkołę --'),] + [(s.pk, s.nazwa + ' ' + str(s.nr) + ' w ' + s.miejscowosc) for s in Szkola.objects.all()]
    KLASY = [('', u'-- najpierw wybierz szkołę --')]

    szkola = forms.ChoiceField(choices=SZKOLY)
    klasa = forms.ChoiceField(choices=KLASY)
"""

class UczenWKlasieForm(forms.ModelForm):   
    class Meta:
        model = Uczen_w_klasie
        fields = ['szkola', 'klasa']     

    def __init__(self, *args, **kwargs):
        super(UczenWKlasieForm, self).__init__(*args, **kwargs)
        self.fields['szkola'].empty_label = '--- wybierz szkołę --'
        self.fields['klasa'].empty_label = '--- najpierw wybierz klasę --'

        #self.fields['klasa'].queryset = Klasa.objects.none()
    
class SwiadectwoForm(forms.ModelForm):
    class Meta:
        model = Swiadectwo

class SwiadectwoSelectForm(forms.Form):    
    swiadectwa = forms.ChoiceField(label='Lista świadectw', widget=forms.Select(attrs={'size':'20'}))        

    def __init__(self, *args, **kwargs):
        super(SwiadectwoSelectForm, self).__init__(*args, **kwargs)
        self.fields['swiadectwa'].choices = [(s.nazwa,s.nazwa) for s in Swiadectwo.objects.all()]    


class PoleForm(forms.ModelForm):
    class Meta:
        model = Pole
