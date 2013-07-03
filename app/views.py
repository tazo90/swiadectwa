from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required

from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView

from .forms import AuthenticateForm, UserCreateForm, \
    ProfilForm, UserEditForm, UczenForm, SzkolaForm, \
    KlasaForm, UczenWKlasieForm, SwiadectwoForm, SwiadectwoSelectForm, PoleForm
from .models import Uczen, Szkola, Klasa, Swiadectwo


def index(request, auth_form=None):    
    if request.user.is_anonymous():
        auth_form = auth_form or AuthenticateForm()
        return render(request, 
                     'login.html', 
                     {'auth_form': auth_form,})    
    else:            
        user = request.user
        if user.profil.rola == 'n':
            """if request.method == 'POST':
                uczen_form = UczenForm(data=request.POST)
                szkola_klasa_form = UczenWKlasieForm(data=request.POST)

                if uczen_form.is_valid() and szkola_klasa_form.is_valid():
                    _form = uczen_form.save(commit=False)
                    _form2 = szkola_klasa_form.save(commit=False)

                    _user = User.objects.get(username=request.GET['user'])
                    _form.id_user = _user            
                    _form2.id_user = _user

                    _form.save()                        
                    _form2.save()
                    return redirect(reverse('user-list'))        

            szkoly = Szkola.objects.all().order_by('miejscowosc')

            uczen_form = UczenForm()
            szkola_klasa_form = UczenWKlasieForm()

            return render(request, 
                          'uczen_form.html',
                          {'uczen_form': uczen_form,
                           'szkola_klasa_form': szkola_klasa_form,
                           'szkoly': szkoly, })
            #return render(request,'home.html')
        """
        elif user.profil.rola == 'u':
            return render(request,'home.html')        
        return render(request,'home.html')

def login_view(request):    
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
        else:            
            return index(request, auth_form=form)            
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

def user_create(request, user_form=None):    
    """ 
    Standardowy formularz dodawania uzytkownika,
    wspolny dla ucznia i nauczyciela 
    """
    if request.method == 'POST':
        user_form = UserCreateForm(data=request.POST)      
        profil_form = ProfilForm(data=request.POST)
        if user_form.is_valid() and profil_form.is_valid():            
            user_form.save()
            p_form = profil_form.save(commit=False)
            
            _user = User.objects.get(username=user_form.cleaned_data['username'])
            p_form.user = _user
            p_form.save()
            
            if p_form.rola == 'u':                
                #return fill_student(request, _user)   
                return redirect("%s?user=%s" % (reverse('student-form'), _user))                

            return redirect(reverse('user-list'))            
        else:            
            return redirect(reverse('student-form'))            

    user_form = user_form or UserCreateForm()
    profil_form = ProfilForm()
    return render(request, 
                 'create_user_form.html', 
                 {'user_form': user_form,
                  'profil_form': profil_form,})


def fill_student(request):
    """
    Formularz dostepny tylko dla ucznia, zawiera pola
    z dodatkowymi danymi 
    """        
    if request.method == 'POST':
        uczen_form = UczenForm(data=request.POST)
        szkola_klasa_form = UczenWKlasieForm(data=request.POST)

        if uczen_form.is_valid() and szkola_klasa_form.is_valid():
            _form = uczen_form.save(commit=False)
            _form2 = szkola_klasa_form.save(commit=False)

            _user = User.objects.get(username=request.GET['user'])
            _form.id_user = _user            
            _form2.id_user = _user

            _form.save()                        
            _form2.save()
            return redirect(reverse('user-list'))        

    szkoly = Szkola.objects.all().order_by('miejscowosc')

    uczen_form = UczenForm()
    szkola_klasa_form = UczenWKlasieForm()

    return render(request, 
                  'uczen_form.html',
                  {'uczen_form': uczen_form,
                   'szkola_klasa_form': szkola_klasa_form,
                   'szkoly': szkoly, })

#========== AJAX
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.utils import simplejson
from django.core import serializers

def ajax_school_class(request):
    """
    ajax zwraca dla danej szkoly (szkola_id) wszystkie klasy 
    ktore sie w niej znajduja 
    """
    if request.is_ajax():
        #szkola_id = request.POST.get('szkola_id', request.POST['szkola_id'])))        
        szkola_id = request.POST['szkola_id']
        if szkola_id:            
            klasy = Szkola.objects.get(pk=int(szkola_id)).klasy.select_related().order_by('klasa')       
            _kl = dict([(s.id, s.klasa) for s in klasy])            # konwertuj do slownika            
            
            data = simplejson.dumps(_kl)                            # zapisz slownik do jsona
            return HttpResponse(data, mimetype='application/json')  # zwroc jsona, odbiera go ajax
    return HttpResponse('')    


def user_edit(request, pesel=None):
    """
    formularz edycji uzytkownika, dwa typy, w zaleznosci czy uczen czy nauczyciel
    """
    instance = get_object_or_404(User, username=pesel)        
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=instance)

        if user_form.is_valid():
            if instance.profil.rola == 'u':         # uczen                
                uczen_form = UczenForm(data=request.POST, instance=instance.uczen)  # wypelnij form ucznia
                szkola_klasa_form = UczenWKlasieForm(data=request.POST, instance=instance.uczen_w_klasie_set.select_related()[0])
                if uczen_form.is_valid() and szkola_klasa_form.is_valid():
                    user_form.save()
                    uczen_form.save()
                    szkola_klasa_form.save()
                    return redirect(reverse('user-list'))
                else:
                    return redirect(reverse('user-list'))
            else:
                user_form.save()
                return redirect(reverse('user-list'))

    user_form = UserEditForm(instance=instance)

    if instance.profil.rola == 'u':        
        uczen_form = UczenForm(instance=instance.uczen)        
        szkola_klasa_form = UczenWKlasieForm(instance=instance.uczen_w_klasie_set.select_related()[0])        
        return render(request,
                     'edit_user_form.html', 
                     {'user_form': user_form,
                      'uczen_form': uczen_form, 
                      'szkola_klasa_form': szkola_klasa_form, })

    return render(request,
                 'edit_user_form.html', 
                  {'user_form': user_form, })


class UserListView(ListView):
    """
    widok klasy wyswietla liste userow 
    """
    model = User
    template_name = "users.html"
    context_object_name = "users"
    paginate_by = 9

    def get_queryset(self):
        objects = User.objects.all().order_by('username')
        return objects

class UserDeleteView(DeleteView):
    """
    usuwa uzytkownika
    """
    model = User
    template_name = 'delete_user.html'    

    def get_queryset(self):        
        objects = User.objects.all().filter(id=self.kwargs['pk'])        
        return objects       

    def get_success_url(self):
        return reverse('user-list')


class SchoolListView(ListView):
    """
    wyswietla liste szkol
    """
    model = Szkola
    template_name = 'schools.html'
    context_object_name = 'szkoly'
    paginate_by = 9

    def get_queryset(self):
        objects = Szkola.objects.all().order_by('wojewodztwo')
        return objects


class SchoolDeleteView(DeleteView):
    """
    usuwa szkole
    """
    model = Szkola
    template_name = 'delete_school.html'

    def get_queryset(self):
        objects = Szkola.objects.all().filter(id=self.kwargs['pk'])
        return objects

    def get_success_url(self):
        return reverse('school-list')        


def school_create(request, school_form=None):
    """
    formularz umozliwiajacy dodanie szkoly
    """
    if request.method == 'POST':
        szkola_form = SzkolaForm(data=request.POST)
        if szkola_form.is_valid():
            szkola_form.save()
            return redirect(reverse('school-list'))

    szkola_form = SzkolaForm()
    return render(request,
                  'create_school_form.html',
                  {'szkola_form': szkola_form, })


#@permission_required('auth.add_user')
def school_edit(request, pk=None):
    """
    edycja szkoly
    """
    instance = get_object_or_404(Szkola, pk=pk)    
    if request.method == 'POST':                
        szkola_from = SzkolaForm(data=request.POST, instance=instance)
        if szkola_from.is_valid():
            szkola_from.save()
            return redirect(reverse('school-list'))

    szkola_form = SzkolaForm(instance=instance)
    return render(request,
                  'edit_school_form.html',
                  {'szkola_form': szkola_form, })


def class_list(request, id_szkoly=None):
    """
    Wyswietla liste klasy
    """
    szkola = Szkola.objects.filter(pk=id_szkoly)[0]
    klasy = szkola.klasy.select_related().order_by('klasa')
    return render(request,
                  'classes.html',
                  {'klasy': klasy, 
                   'szkola': szkola, })

def class_create(request, id_szkoly=None):
    """
    Tworzy klase w szkole id_szkoly
    """

    if request.method == 'POST':
        klasa_form = KlasaForm(data=request.POST)        
        if klasa_form.is_valid():            
            _form = klasa_form.save(commit=False)   # don't save to database
            _form.id_szkola = Szkola.objects.get(pk=id_szkoly)  # save instance of school
            # SPRAWDZIC CZY KLASA NIE ZOSTALA DODANA, bo wpp
            # RZUCA BLAD BAZY: podwojna wartosc klucza
            _form.save()
            return redirect(reverse('class-list', kwargs={'id_szkoly': id_szkoly, }))

    szkola = Szkola.objects.get(pk=id_szkoly)
    klasa_form = KlasaForm()
    return render(request,
                  'create_class_form.html',
                  {'klasa_form': klasa_form,
                   'szkola': szkola,})


def class_delete(request, id_szkoly=None, nazwa_klasy=None):                    
    """ 
    Usuwa klase ze szkoly id_szkola
    """

    Szkola.objects.get(pk=id_szkoly).klasy.select_related().filter(klasa=nazwa_klasy).delete()        
    return redirect(reverse('class-list', kwargs={'id_szkoly':id_szkoly,}))


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt        # zwolniony z ochrony csrf - inaczej nie dziala, bo blokuje middlware
def ajax_class_student_show(request):
    """ 
    Widok pokazuje wszystkich studentow ze szkoly id_szkola i klasy nazwa_klasy
    """        
    if request.is_ajax():        
        szkola_id = request.POST['szkola_id']
        klasa = request.POST['klasa']
        
        uczen_klasa = Szkola.objects.get(pk=int(szkola_id)).klasy.get(klasa=klasa).uczen_w_klasie_set.all()
        user_list = [u.id_user for u in uczen_klasa]
        #print uczen_list

        data = serializers.serialize('json', user_list)
        return HttpResponse(data, mimetype='application/json')        
    return HttpResponse('')


def certificate(request):
    """
    Widok swiadectwa
    """
    swiad_sel = SwiadectwoSelectForm()

    return render(request,
                  'certificate.html',
                  {'swiad_sel': swiad_sel, })

def create_certificate(request, swiad_form=None):
    """
    Widok tworzenia swiadectwa
    """
    if request.method == 'POST':
        swiad_form = SwiadectwoForm(request.POST, request.FILES)
        if swiad_form.is_valid():
            swiad_form.save()
            return redirect(reverse('fill-certificate'))
        else:            
            return redirect(reverse('create-certificate'))

    swiad_form = SwiadectwoForm()
    return render(request, 
                  'create_certificate_form.html',
                  {'swiad_form': swiad_form, })


def fill_certificate_form(request):
    """
    Formularz dodaje pola do swiadectwa
    """
    if request.method == 'POST':
        pole_form = PoleForm(data=request.POST)
        if pole_form.is_valid():
            pole_form.save()
            return redirect(reverse('certificate'))
        else:            
            return redirect(reverse('fill-certificate'))

    pole_form = PoleForm()
    return render(request, 
                  'fill_certificate_form.html',
                  {'pole_form': pole_form, })

from django.template.loader import render_to_string
@csrf_exempt
def ajax_show_certificate(request):  
    res = None    

    if request.is_ajax():         
        if request.POST.has_key('swiadectwo_show'):              
            swiad = Swiadectwo.objects.get(nazwa=request.POST['swiadectwo_show'])                                        
            data = serializers.serialize('json', [swiad])
        
            return HttpResponse(data, mimetype='application/json')
        elif request.POST.has_key('swiadectwo_del'):            

            Swiadectwo.objects.get(nazwa=request.POST['swiadectwo_del']).delete()

            swiad = Swiadectwo.objects.all()                                 
            data = serializers.serialize('json', swiad)            
            return HttpResponse(data, mimetype='application/json')
            return HttpResponse('')
    return HttpResponse('')

##########
def certificate_edit(request):
    return render(request, 'certificate_edit.html', {"obrazek": "http://img197.imageshack.us/img197/8002/xn5l.jpg"})

def proba(request):
    return render(request, 'proba.html')
