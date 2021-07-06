#from django.shortcuts import render
from django.http import HttpResponse
#from .models import ALBUMS

# Create your views here.

def index(request):
    message = "Hellooo !"
    return HttpResponse(message)

def listing(request):
    albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
    message = "<ul>{}</ul>".format("\n".join(albums))
    return HttpResponse(message)

def detail(request, album_id):
    id = int(album_id)
    album = ALBUMS[id]
    artists = ", ".join([artist['name'] for artist in album['artistes']])
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album['name'], artists)
    return HttpResponse(message)

def search(request):
    query = request.GET['query']
    if not query:
        message = "Aucun artiste n'a été demandé"
    else:
        albums = [
            album for album in ALBUMS
            if query in " ".join(artist['name'] for artist in album['artistes'])
        ]
        if len(albums) == 0:
            message = "Aucun album n'a été trouvé !"
        else:
            albums = ["<li>{}</li>".format(album['name']) for album in albums]
            message = """
                Nous avons trouvé {} albums ! Les voici :
                <ul>
                    {}
                </ul>
            """.format(len(albums), "</li><li>".join(albums))
    return HttpResponse(message)
