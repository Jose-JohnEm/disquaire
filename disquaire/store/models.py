from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Artist(models.Model):
    name = models.CharField('Nom', max_length=30, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Artiste"

class Contact(models.Model):
    email = models.EmailField('Courriel', max_length=100)
    name = models.CharField('Nom', max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client"

class Album(models.Model):
    reference = models.IntegerField(null=True)
    created_at = models.DateTimeField('Date de publication', auto_now_add=True)
    avalaible = models.BooleanField('Disponible', default=True)
    title = models.CharField('Titre' ,max_length=100)
    picture = models.URLField('Image', max_length=500)
    artists = models.ManyToManyField( Artist, related_name='albums', blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Disque"

class Booking(models.Model):
    created_at = models.DateTimeField("Date d'achat", auto_now_add=True)
    contacted = models.BooleanField("Demande traitée ?", default=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    album = models.OneToOneField(Album, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.contact.name

    class Meta:
        verbose_name = "Réservation"