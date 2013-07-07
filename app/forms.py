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
        fields = ['data_ur', 'miejsce_ur', 'plec']              

    def __init__(self, *args, **kwargs):        
        super(UczenForm, self).__init__(*args, **kwargs)
        self.fields['data_ur'].widget.attrs['placeholder'] = 'Data urodzenia dd.mm.yyyy'
        self.fields['miejsce_ur'].widget.attrs['placeholder'] = 'Miejsce urodzenia'        

        #### Labels ####
        self.fields['data_ur'].label = 'Data urodzenia'
        self.fields['miejsce_ur'].label = 'Miejsce urodzenia'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Pesel'
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
        fields = ['szkola', 'klasa', 'id_user']     

    def __init__(self, *args, **kwargs):
        super(UczenWKlasieForm, self).__init__(*args, **kwargs)        
        # wypelnij id_user uczniami        
        self.fields['szkola'].choices = [('', '--- wybierz szkołę ---')] + [(s.id, s.nazwa + ' ' + str(s.nr) + ' w ' + s.miejscowosc) for s in Szkola.objects.all()]
        self.fields['id_user'].choices = [('', '--- wybierz ucznia ---')] + [(u.id_user.id, u.id_user.first_name + ' ' + u.id_user.last_name) for u in Uczen.objects.all()]
        
        self.fields['klasa'].empty_label = '--- wybierz klasę --'

        #self.fields['klasa'].queryset = Klasa.objects.none()
    
class SwiadectwoForm(forms.ModelForm):
    class Meta:
        model = Swiadectwo

class SwiadectwoSelectForm(forms.Form):    
    """
    Wypelnia form z pierwsza strona kazdego swiadectwa,
    strony tego samego swiadectwa maja te same nazwy, pobiera strone o tej
    samej nazwie i najmniejszym id
    """
    swiadectwa = forms.ChoiceField(label='Lista świadectw', widget=forms.Select(attrs={'size':'15'}))        

    def __init__(self, *args, **kwargs):
        super(SwiadectwoSelectForm, self).__init__(*args, **kwargs)
        #self.fields['swiadectwa'].choices = [(s.id,s.nazwa) for s in Swiadectwo.objects.all()]    
        self.fields['swiadectwa'].choices = [(s.id,s.nazwa) for s in Swiadectwo.objects.all().distinct('nazwa')]    

class SwiadectwoPagesForm(forms.Form):
    """
    Pobiera wszystkie strony swiadectwa, razem ze strona pierwsza,
    ktora jest wyswietlana przez SwiadectwoSelectForm
    """
    strony = forms.ChoiceField(label='Lista stron', widget=forms.Select(attrs={'size':'3'}))


class PoleForm(forms.ModelForm):
    """
    Dodaje pola do swiadectwa
    """    
    class Meta:
        model = Pole
        fields = ['nazwa', 'wsp_x', 'wsp_y', 'wysokosc', 'szerokosc', 'stale']

    def __init__(self, *args, **kwargs):
        super(PoleForm, self).__init__(*args, **kwargs)                
        self.fields['stale'].choices = [('', '-- wybierz stałą --')] + [('t', 'tak'), ('n', 'nie')]        
        self.fields['nazwa'].widget.attrs['placeholder'] = 'Nazwa pola'        
        self.fields['wsp_x'].widget.attrs['placeholder'] = 'Współrzędna x'
        self.fields['wsp_y'].widget.attrs['placeholder'] = 'Współrzędna y'
        self.fields['wysokosc'].widget.attrs['placeholder'] = 'Wysokość'
        self.fields['szerokosc'].widget.attrs['placeholder'] = 'Szerokość'                                


