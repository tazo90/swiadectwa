#from django.db.models.signals import post_syncdb
#import app.models
#from django.contrib.auth.models import Group, Permission

#def add_perm_to_group(sender, **kwargs):    
    #Group(name='uczen').save()
    #Group(name='nauczyciel').save()  

    #g_uczen = Group.objects.get(name='uczen')
    #g_nauczyciel = Group.objects.get(name='nauczyciel')

    #g_nauczyciel.permissions = [
    #  Permission.objects.get(codename='change_swiadectwo'),
    #  Permission.objects.get(codename='change_pole'),
    #  Permission.objects.get(codename='change_profil'),
    #  Permission.objects.get(codename='add_wartosci'),
    #  Permission.objects.get(codename='change_wartosci'),
    #  Permission.objects.get(codename='delete_wartosci'),
    #]
    

#post_syncdb.connect(add_perm_to_group, sender=app.models)
