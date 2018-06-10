# coding: utf8
import string
from django.db import models
from ckeditor.fields import RichTextField

from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Partnership(models.Model):
    name = models.CharField("Partner's name", max_length=50)
    logo = models.ImageField(upload_to='image/partners')
    website = models.CharField(max_length=50)
    order = models.IntegerField()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Showcase(models.Model):
    image = models.ImageField(upload_to='image/showcase')
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Production(models.Model):
    order = models.IntegerField(help_text="L'ordre d'apparition dans le menu du haut, dans l'ordre croissant")
    name = models.CharField(max_length=80)
    description = models.TextField()
    fa_icon = models.CharField(_("Icone Font Awesome"),max_length=20, help_text="Choisir une icone ici: http://fontawesome.io/icons/. Exemple: fa-home")

    def __str__(self):
        return self.name

def content_file_name(instance, filename):
    printable = set(string.printable)
    name = ''.join(filter(lambda x: x in printable, instance.production.name))
    filename = ''.join(filter(lambda x: x in printable, filename))
    return '/'.join(['video', name +" "+str(date.today().year), filename])

@python_2_unicode_compatible
class Video(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to=content_file_name, help_text="N'upload que des VIDEOS, format webm ou mp4, voir le tableau dans cette page : https://developer.mozilla.org/fr/docs/Web/HTML/Formats_pour_audio_video")
    thumbnail = models.FileField(upload_to=content_file_name, help_text="La vignette de la vidéo au format 16/9")
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    year = models.IntegerField(help_text="Année de publication")
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@python_2_unicode_compatible
class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="images", help_text="Pour prendre l'URL il faut selectionner la partie en /media/image/name.xxx")

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Video)
def mymodel_delete(sender, instance, **kwargs):
    instance.video.delete(False)
    instance.thumbnail.delete(False)

@python_2_unicode_compatible
class Team(models.Model):
    group_photo = models.ImageField(_("Photo de groupe"), upload_to="image/team", blank=True, null=True)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1977)])

    def __str__(self):
        return str(self.year)

def personn_file_name(instance, filename):
    return '/'.join(['image/team', str(instance.team.year)])

@python_2_unicode_compatible
class Member(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=personn_file_name, help_text="Mettre des images carrés uniquement. Ce champs n'est pas requis.", blank=True, null=True)
    fonction = models.CharField(max_length=50)
    is_prez = models.BooleanField("Cette personne est présidente", default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

@python_2_unicode_compatible
class News(models.Model):
    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'

    title = models.CharField(max_length=100)
    content = RichTextField()
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Page(models.Model):

    title = models.CharField(max_length=50)
    content = RichTextField()
    fa_icon = models.CharField("Icone Font Awesome",max_length=20, help_text="Choisir une icone ici: http://fontawesome.io/icons/. Exemple: fa-home")

    def __str__(self):
        return self.title
