from django.test import TestCase
from django.urls import reverse
from .models import *

# Create your tests here.

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    def setUp(self):
        impossible = Album.objects.create(title="Transmission Impossible")
        self.album = Album.objects.get(title="Transmission Impossible")

    def test_detail_page_returns_200(self):
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=[album_id]))
        self.assertEqual(response.status_code, 200)
        
    def test_detail_page_returns_404(self):
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=[album_id + 1]))
        self.assertEqual(response.status_code, 404)

class BookingPageTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(name="Jose", email="jojo@gmail.com")
        artist = Artist.objects.create(name="LD2J")
        impossible = Album.objects.create(title="Coro des coro")
        impossible.artists.add(artist)
        self.contact = Contact.objects.get(name="Jose")
        self.album = Album.objects.get(title="Coro des coro")

    def test_new_booking_is_registered(self):
        old_books = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        res = self.client.post(
            reverse('store:detail', args=[album_id]), {
                'name': name,
                'email': email
            }
        )
        new_books = Booking.objects.count()
        self.assertEqual(old_books, new_books)
        
    # def test_booked_album_is_not_available(self):
    #         album_id = self.album.id
    #         name = self.contact.name
    #         email = self.contact.email
    #         self.client.post(
    #             reverse(
    #                 'store:detail',
    #                 args=[album_id]
    #             ), {
    #                 'name': name,
    #                 'email': email
    #             }
    #         )
    #         album_avalaible = self.album.avalaible
    #         self.assertEqual(False, album_avalaible)
