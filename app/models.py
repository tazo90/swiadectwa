#coding: utf-8
from django.db import models
from django.contrib.auth.models import User

STALE_POLE = (
    ('t', 'tak'),
    ('n', 'nie'),
)

TYP_KONTA = (
    ('n', 'nauczyciel'),
    ('u', 'uczen'),
)

PLEC = (
    ('k', 'kobieta'),
    ('m', 'mężczyzna'),
)

WOJEWODZTWA = (
    (u'Dolnośląskie', u'Dolnośląskie'),
    (u'Kujawsko-Pomorskie', u'Kujawsko-Pomorskie'),
    (u'Lubelskie', u'Lubelskie'),
    (u'Lubuskie', u'Lubuskie'),
    (u'Łódzkie', u'Łódzkie'),
    (u'Małopolskie', u'Małopolskie'),
    (u'Mazowieckie', u'Mazowieckie'),
    (u'Opolskie', u'Opolskie'),
    (u'Podkarpackie', u'Podkarpackie'),
    (u'Podlaskie', u'Podlaskie'),
    (u'Pomorskie', u'Pomorskie'),
    (u'Śląskie', u'Śląskie'),
    (u'Świętokrzyskie', u'Świętokrzyskie'),
    (u'Warmińsko-Mazurskie', u'Warmińsko-Mazurskie'),
    (u'Wielkopolskie', u'Wielkopolskie'),
    (u'Zachodnio-Pomorskie', u'Zachodnio-Pomorskie'),
)


class Swiadectwo(models.Model):
    def url(self, filename):
        path = "uploads/form/%s" % (filename)
        return path   

    nazwa = models.CharField(max_length=50)
    obrazek = models.ImageField(upload_to=url)

    class Meta:
        unique_together = ('nazwa', 'obrazek')

    def __unicode__(self):
        return self.nazwa


class Pole(models.Model):
    id_swiad = models.ForeignKey(Swiadectwo)
    nazwa = models.CharField(max_length=50)    
    wsp_x = models.IntegerField()
    wsp_y = models.IntegerField()
    wysokosc = models.IntegerField()
    szerokosc = models.IntegerField()  
    stale = models.CharField(max_length=1, choices=STALE_POLE)

    class Meta:        
        verbose_name_plural = 'Pola'

    def __unicode__(self):
        return self.nazwa


class Profil(models.Model):
    user = models.OneToOneField(User)                    
    rola = models.CharField(max_length=15, choices=TYP_KONTA)            

    class Meta:
        verbose_name_plural = 'Profil'

    def __unicode__(self):
        return "%s" % (self.user)


User.profil = property(lambda u: Profil.objects.get_or_create(user=u)[0])


class Uczen(models.Model):
    id_user = models.OneToOneField(User)
    data_ur = models.DateField()
    miejsce_ur = models.CharField(max_length=100)
    plec = models.CharField(max_length=10, null=True, choices=PLEC, default='m')

    def __unicode__(self):
        return "%s" % (self.id_user)


class Wartosci(models.Model):
    #id_swiad = models.ForeignKey(Pola, to_field='id_swiad')
    id_user = models.ForeignKey(Uczen, to_field='id_user')
    #nazwa = models.ForeignKey(Pole, to_field='nazwa')
    id_pole = models.ForeignKey(Pole)
    wartosc = models.TextField()

    class Meta:
        unique_together = ('id_pole', 'id_user')
        verbose_name_plural = 'Wartosci'

    def __unicode__(self):
        return "%s %s" % (self.id_pole.nazwa, self.wartosc)


class Szkola(models.Model):
    nazwa = models.CharField(max_length=100, null=True)
    nr = models.IntegerField(null=True)
    miejscowosc = models.CharField(max_length=100)
    wojewodztwo = models.CharField(max_length=100, choices=WOJEWODZTWA, default='doln')

    class Meta:
        verbose_name_plural = 'Szkoly'
        unique_together = ('miejscowosc','nazwa')

    def __unicode__(self):
        return unicode(self.nazwa)


class Klasa(models.Model):
    id_szkola = models.ForeignKey(Szkola, related_name='klasy')
    klasa = models.CharField(max_length=10)    

    class Meta:
        unique_together = ('id_szkola', 'klasa')
        verbose_name_plural = 'Klasy'

    def __unicode__(self):
        return "%s %s" % (self.id_szkola.nazwa, self.klasa)


class Uczen_w_klasie(models.Model):
    id_user = models.ForeignKey(Uczen, to_field='id_user')
    szkola = models.ForeignKey(Szkola)
    klasa = models.ForeignKey(Klasa)

    class Meta:
        unique_together = ('id_user', 'szkola') 

    def save(self, *args, **kwargs):
        self.szkola = self.klasa.id_szkola
        super(Uczen_w_klasie, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.szkola.nazwa)

