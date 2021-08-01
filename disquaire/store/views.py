#from django.shortcuts import render
from django import template
from django.http import HttpResponse
from django.template import loader

from .models import Album, Artist, Contact, Booking

def index(request):
    albums = Album.objects.filter(avalaible=True).order_by('-created_at')[:12]
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    template = loader.get_template('store/index.html')
    context = {'albums': albums}
    return HttpResponse(template.render(context, request=request))

def listing(request):
    albums = Album.objects.filter(avalaible=True)
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format('\n'.join(formatted_albums))
    return HttpResponse(message)

def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album.title, artists)
    return HttpResponse(message)

def search(request):
    query = request.GET['query']
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)
        #albums = Album.objects.filter(name__unaccent__lower__trigram_similar=query)
        
        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)
        if not albums.exists():
            message = "On a rien trouvé chacal..."
        else:
            albums = ["<li>{}</li>".format(album.title) for album in albums]
            message = """
                Nous avons trouvé {} albums ! Les voici :
                <ul>
                    {}
                </ul>
            """.format(len(albums), "</li><li>".join(albums))
    return HttpResponse(message)
