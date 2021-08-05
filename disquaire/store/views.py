from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError

from .models import Album, Artist, Contact, Booking
from .forms import ContactForm, ParagraphErrorList

def index(request):
    albums = Album.objects.filter(avalaible=True).order_by('-created_at')[:12]
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    context = {
        'albums': albums
    }
    return render(request, 'store/index.html', context)

def listing(request):
    albums_list = Album.objects.filter(avalaible=True)
    paginator = Paginator(albums_list, 2)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums,
        'paginate': True
    }
    return render(request, 'store/listing.html', context)

#@transaction.atomic
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    context = {
        'album_title': album.title,
        'artists_name': artists,
        'album_id': album.id,
        'album_pic': album.picture,
    }
    
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                    else:
                        contact = contact.first()
                    album = get_object_or_404(Album, id=album.id)
                    booking = Booking.objects.create(
                        contact=contact,
                        album=album,
                    )
                    album.avalaible = False
                    album.save()
                    context = {
                        'album_title': album.title,
                    }
                    return render(request, 'store/merci.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une errreur interne est apparue. Merci de recommencer votre requête."
    else:
        form = ContactForm()

    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET['query']
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)
        #albums = Album.objects.filter(title__unaccent__lower__trigram_similar=query)
        
        if not albums.exists():
            #albums = Album.objects.filter(artists__name__unaccent__lower__trigram_similar=query)
            albums = Album.objects.filter(artists__name__icontains=query)
    title = "Résultats pour '%s'"%query
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)
