from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'swiad.views.home', name='home'),
    # url(r'^swiad/', include('swiad.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'app.views.login_view', name='login'),
    url(r'^logout$', 'app.views.logout_view', name='logout'),
    
    url(r'^', include('app.urls')),    


    # to musi byc, zeby dziala {{ MEDIA_URL }} w template
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),  
) 
