from django.conf.urls import patterns, include, url

from .views import UserListView, UserDeleteView, SchoolListView, SchoolDeleteView

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),  

    url(r'^signup/$', 'user_create', name='user-create'),
    url(r'^signup/student/$', 'fill_student', name='student-form'),    
    
    url(r'^school/$', SchoolListView.as_view(), name='school-list'),    
    url(r'^school/create/$', 'school_create', name='school-create'),
    url(r'^school/(?P<pk>\d+)/delete/$', SchoolDeleteView.as_view(), name='school-delete'),
    url(r'^school/(?P<pk>\d+)/edit/$', 'school_edit', name='school-edit'),

    url(r'^school/class/$', 'ajax_school_class', name='school-class'),    
    url(r'^school/class/show/$', 'ajax_class_student_show', name='class-show'),    
    
    url(r'^school/(?P<id_szkoly>\d+)/classes/$', 'class_list', name='class-list'),
    url(r'^school/(?P<id_szkoly>\d+)/classes/create/$', 'class_create', name='class-create'),
    url(r'^school/(?P<id_szkoly>\d+)/classes/(?P<nazwa_klasy>\w+)/delete/$', 'class_delete', name='class-delete'),

    url(r'^forms/$', 'certificate', name='certificate'),
    url(r'^forms/create/$', 'create_certificate', name='create-certificate'),
    url(r'^forms/create/fill/$', 'fill_certificate_form', name='fill-certificate'),
    url(r'^forms/show/$', 'ajax_show_certificate', name='show-cert'),

    

    url(r'^users/$', UserListView.as_view(), name='user-list'),        
    url(r'^users/(?P<pk>\d+)/delete/$', UserDeleteView.as_view(), name='user-delete'),    
    url(r'^users/(?P<pesel>\w+)/edit/$', 'user_edit', name='user-edit'),  


    #lila 
    url(r'^certificate_edit/$', 'certificate_edit', name='certificate_edit'),
    url(r'^proba/$', 'proba', name='proba'),


)
