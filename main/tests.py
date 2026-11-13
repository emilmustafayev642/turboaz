from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Brand, CarModel, Listing


class DeleteListingTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username='owner', password='password')
        self.other_user = user_model.objects.create_user(username='other', password='password')
        brand = Brand.objects.create(name='Test brand')
        car_model = CarModel.objects.create(brand=brand, name='Test model')
        self.listing = Listing.objects.create(
            owner=self.owner,
            car_model=car_model,
            year=2020,
            condition='used',
            body_type='sedan',
            price=10000,
            mileage=50000,
            city='Baku',
            description='Test listing',
            image='listing_photos/test.jpg',
        )
        self.delete_url = reverse('delete_listing', args=[self.listing.pk])

    def test_owner_can_delete_listing_from_edit_form(self):
        self.client.force_login(self.owner)

        edit_response = self.client.get(reverse('edit_listing', args=[self.listing.pk]))
        self.assertContains(edit_response, 'Elanı sil')
        self.assertContains(edit_response, f'action="{self.delete_url}"', html=False)

        delete_response = self.client.post(self.delete_url)

        self.assertRedirects(delete_response, reverse('home'))
        self.assertFalse(Listing.objects.filter(pk=self.listing.pk).exists())

    def test_other_user_cannot_delete_listing(self):
        self.client.force_login(self.other_user)

        response = self.client.post(self.delete_url)

        self.assertRedirects(response, reverse('detail', args=[self.listing.pk]))
        self.assertTrue(Listing.objects.filter(pk=self.listing.pk).exists())

    def test_delete_requires_post(self):
        self.client.force_login(self.owner)

        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Listing.objects.filter(pk=self.listing.pk).exists())
