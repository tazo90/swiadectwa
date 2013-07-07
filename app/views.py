from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView

from .forms import AuthenticateForm, UserCreateForm, \
    ProfilForm, UserEditForm, UczenForm, SzkolaForm, \
    KlasaForm, UczenWKlasieForm, SwiadectwoForm, SwiadectwoSelectForm, \
    PoleForm, SwiadectwoPagesForm
from .models import Uczen, Szkola, Klasa, Swiadectwo, Wartosci, Pole


def index(request, auth_form=None):    
    """ 
    Handles index page
    """
    if request.user.is_anonymous():
        auth_form = auth_form or AuthenticateForm()
        return render(request, 
                     'login.html', 
                     {'auth_form': auth_form,})    
    else:                        
        if request.user.profil.rola == 'u':
            swiad_form = SwiadectwoSelectForm()            

            wart = Wartosci.objects.filter(id_user=request.user.id).distinct('id_pole__id_swiad')                    
            swiad_form.fields['swiadectwa'].choices = [(s.id_pole.id_swiad.id, s.id_pole.id_swiad.nazwa) for s in wart]

            swiad_pages = SwiadectwoPagesForm()                        
            return render(request,
                          'home.html',
                          {'swiad_form': swiad_form, 
                           'swiad_pages': swiad_pages, })


        return render(request,'home.html')


def login_view(request):    
    """ 
    Login forms
    """
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


@permission_required('auth.add_user')
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


@permission_required('auth.add_user')
def fill_student(request):
    """
    Formularz dostepny tylko dla ucznia, zawiera pola
    z dodatkowymi danymi 
    """        
    if request.method == 'POST':
        uczen_form = UczenForm(data=request.POST)        

        if uczen_form.is_valid():            
            _form = uczen_form.save(commit=False)            
            _user = User.objects.get(username=request.GET['user'])            
            _form.id_user = _user                        

            _form.save()                                    
            return redirect(reverse('user-list'))        
        else:
            return redirect(reverse('student-form'))        

    szkoly = Szkola.objects.all().order_by('miejscowosc')
    
    uczen_form = UczenForm()    
    return render(request, 
                  'uczen_form.html',
                  {'uczen_form': uczen_form,                   
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
        szkola_id = request.POST['szkola_id']        
        if szkola_id:            
            klasy = Szkola.objects.get(pk=int(szkola_id)).klasy.select_related().order_by('klasa')       
            _kl = dict([(s.id, s.klasa) for s in klasy])            # konwertuj do slownika            
            
            data = simplejson.dumps(_kl)                            # zapisz slownik do jsona
            return HttpResponse(data, mimetype='application/json')  # zwroc jsona, odbiera go ajax
    return HttpResponse('')    


@permission_required('auth.add_user')
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
                if uczen_form.is_valid():
                    user_form.save()
                    uczen_form.save()                
                    return redirect(reverse('user-list'))
                else:
                    return redirect(reverse('user-list'))
            else:
                user_form.save()
                return redirect(reverse('user-list'))

    user_form = UserEditForm(instance=instance)

    if instance.profil.rola == 'u':        
        uczen_form = UczenForm(instance=instance.uczen)                
        return render(request,
                     'edit_user_form.html', 
                     {'user_form': user_form,
                      'uczen_form': uczen_form, 
                      })

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

    @method_decorator(permission_required('auth.add_user'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)        


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

    @method_decorator(permission_required('auth.add_user'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)  


class UczenListView(ListView):
    """
    widok klasy wyswietla liste uczniow
    """
    model = Uczen
    template_name = "uczen_list.html"
    context_object_name = "uczniowie"
    paginate_by = 9

    def get_queryset(self):
        objects = Uczen.objects.all().order_by('id_user__username')
        return objects 


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

    @method_decorator(permission_required('auth.add_user'))
    def dispatch(self, request, *args, **kwargs):
        return super(SchoolDeleteView, self).dispatch(request, *args, **kwargs)


@permission_required('auth.add_user')
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


@permission_required('auth.add_user')
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
    if request.method == 'POST':        
        uczen_w_klasie = UczenWKlasieForm(data=request.POST)
        if uczen_w_klasie.is_valid():            
            uczen_w_klasie.save()
            return redirect(reverse('class-list', kwargs={'id_szkoly': id_szkoly, }))
        else:
            print 'nie'

    uczen_klasa_form = UczenWKlasieForm()
    szkola = Szkola.objects.filter(pk=id_szkoly)[0]
    klasy = szkola.klasy.select_related().order_by('klasa')
    
    return render(request,
                  'classes.html',
                  {'klasy': klasy, 
                   'szkola': szkola,
                   'uczen_klasa_form': uczen_klasa_form})


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


@permission_required('auth.add_user')
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
    Widok pokazuje wszystkich uczniow ze szkoly id_szkola i klasy nazwa_klasy
    """        
    if request.is_ajax():        
        szkola_id = request.POST['szkola_id']
        klasa = request.POST['klasa']
        
        uczen_klasa = Szkola.objects.get(pk=int(szkola_id)).klasy.get(klasa=klasa).uczen_w_klasie_set.all()
        user_list = [u.id_user.id_user for u in uczen_klasa]        

        data = serializers.serialize('json', user_list)        
        return HttpResponse(data, mimetype='application/json')        
    return HttpResponse('')


def certificate(request):
    """
    Widok swiadectwa
    """    
    if request.user.profil.rola == 'n':
        uczen_klasa_form = UczenWKlasieForm()
        swiad_sel = SwiadectwoSelectForm()
        swiad_pages = SwiadectwoPagesForm()

        return render(request,
                  'certificate.html',
                  {'uczen_klasa_form': uczen_klasa_form,
                   'swiad_sel': swiad_sel,                
                   'swiad_pages': swiad_pages, })
    

    pole_form = PoleForm()
    swiad_sel = SwiadectwoSelectForm()
    swiad_pages = SwiadectwoPagesForm()
    return render(request,
                  'certificate.html',
                  {'pole_form': pole_form,
                   'swiad_sel': swiad_sel,                
                   'swiad_pages': swiad_pages, })    


@permission_required('auth.add_user')
def create_certificate(request, swiad_form=None):
    """
    Widok tworzenia swiadectwa
    """
    if request.method == 'POST':
        swiad_form = SwiadectwoForm(request.POST, request.FILES)
        if swiad_form.is_valid():
            swiad_form.save()
            return redirect(reverse('certificate'))

        else:            
            return redirect(reverse('create-certificate'))

    swiad_form = SwiadectwoForm()
    return render(request, 
                  'create_certificate_form.html',
                  {'swiad_form': swiad_form, })



from django.template.loader import render_to_string
@csrf_exempt
def ajax_show_certificate(request):  
    if request.is_ajax():         
        if request.POST.has_key('swiadectwo_show'):              # pokaz swiadectwo (pierwsza strona)
            swiad = Swiadectwo.objects.get(id=int(request.POST['swiadectwo_show']))
            
            first_page = Swiadectwo.objects.get(id=int(request.POST['swiadectwo_show']))
            pages = Swiadectwo.objects.filter(nazwa=first_page.nazwa)
            #data = serializers.serialize('json', [swiad]) # gdy zwraca tylko jeden obiekt (tzn gdy get to [])
            data = serializers.serialize('json', pages) 
            print data          
            
            return HttpResponse(data, mimetype='application/json')
        elif request.POST.has_key('strona_show'):                # pokaz strone swiadectwa            
            page = Swiadectwo.objects.get(id=int(request.POST['strona_show']))            
            data = serializers.serialize('json', [page])

            return HttpResponse(data, mimetype='application/json')
        elif request.POST.has_key('swiadectwo_del'):                        
            Swiadectwo.objects.get(id=int(request.POST['swiadectwo_del'])).delete()                        
            first_pages = Swiadectwo.objects.all().distinct('nazwa')  # tylko pierwsze strony swiadectwa
            data = serializers.serialize('json', first_pages)                        

            return HttpResponse(data, mimetype='application/json')
        elif request.POST.has_key('strona_del'):            
            page_del = Swiadectwo.objects.get(id=int(request.POST['strona_del']))
            page_del_name = page_del.nazwa
            page_del.delete()
            
            #first_pages = Swiadectwo.objects.all().distinct('nazwa')  # tylko pierwsze strony swiadectwa
            rest_pages = Swiadectwo.objects.filter(nazwa=page_del_name) # reszta stron aktualnego swiadectwa            

            data = serializers.serialize('json', rest_pages)

            return HttpResponse(data, mimetype='application/json')
    return HttpResponse('')


def certificate_edit(request):
    return render(request, 'certificate_edit.html', {"obrazek": "http://img197.imageshack.us/img197/8002/xn5l.jpg"})


@csrf_exempt
def generic_certificate(request, user=None):
    """
    Display student certificate filled with values 
    """
    uczen = None
    szkola = None
    user = None
    
    if request.user.profil.rola == 'u':
        uczen = Uczen.objects.get(id=request.user.uczen.id)        
        szkola = Szkola.objects.get(id=uczen.uczen_w_klasie_set.all()[0].szkola_id)
        user = User.objects.get(username=uczen.id_user)            
    elif request.user.profil.rola == 'n':
        user = User.objects.get(id=int(request.GET['id_uczen']))
        uczen = Uczen.objects.get(id=user.uczen.id)
        szkola = Szkola.objects.get(id=int(request.GET['id_szkola']))                


    id_swiad = None
    swiad = None
    page_nr = None    

    if request.GET.has_key('id_swiad'):
        id_swiad = int(request.GET['id_swiad'])
        swiad = Swiadectwo.objects.get(id=id_swiad)
        
        if request.GET.has_key('page_nr'):
            page_nr = int(request.GET['page_nr'])                
    
    if request.is_ajax():          
        swiad = Swiadectwo.objects.get(id=int(request.POST['id_swiad']))
        
        Pole.objects.create(
            id_swiad=swiad,
            nazwa=request.POST['nazwa_pola'],
            wsp_x=int(request.POST['wsp_x']),
            wsp_y=int(request.POST['wsp_y']),
            wysokosc=int(request.POST['wysokosc']),
            szerokosc=int(request.POST['szerokosc']),
            stale=request.POST['stale']
            )

        data = serializers.serialize('json', [swiad])        

        return HttpResponse(data, mimetype='application/json')

    if request.method == 'POST':        
        for field in request.POST:
            if field is not None:
                pole = Pole.objects.filter(id_swiad=id_swiad, nazwa=field, stale='n')
                if pole:
                    pole = pole[0]                    
                    if Wartosci.objects.filter(id_pole = pole.id):
                        Wartosci.objects.filter(id_pole = pole.id).update(wartosc=request.POST[field])
                    else:                        
                        Wartosci.objects.create(id_user=uczen, id_pole=pole, wartosc = request.POST[field])
    
    ids = [p.id for p in [w.id_pole for w in Wartosci.objects.all()]]
    
    pole = Pole.objects.filter(id_swiad=id_swiad, stale='n').exclude(id__in=ids)
    stale = Pole.objects.filter(id_swiad=id_swiad, stale='t').values() #lista slownikow
    wartosci = []    

    # UWAGA: ZMIENIC ID_USER DLA NAUCZYCIELA !!!    
    if request.user.profil.rola == 'u':
        for w  in Wartosci.objects.filter(id_pole__id_swiad=id_swiad, id_user=request.user.uczen):
            wartosci.append((w, w.id_pole))
    elif request.user.profil.rola == 'n':
        for w  in Wartosci.objects.filter(id_pole__id_swiad=id_swiad, id_user=2):
            wartosci.append((w, w.id_pole))
    
    for s in stale:        
        if hasattr(szkola, s["nazwa"]):
            s["value"] = getattr(szkola, s["nazwa"])
        elif hasattr(uczen, s["nazwa"]):
            s["value"] = getattr(uczen, s["nazwa"])
        elif hasattr(user, s["nazwa"]):
            if s["nazwa"] == 'first_name':
                s["value"] = getattr(user, s["nazwa"]) + ' ' + getattr(user, 'last_name')
            else:
                s["value"] = getattr(user, s["nazwa"])    

    page = ""
    if request.GET.has_key("read"):
        page = 'generic_certificate_read.html'
    else:
        page = 'generic_certificate.html'

    return render(request, 
                  page, 
                  {
                  'swiad': swiad,
                  'page_nr': page_nr,
                  "pole": pole, 
                  "stale": stale, 
                  "wartosc": wartosci,
                  })
