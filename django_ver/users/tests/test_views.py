import json
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile, Contact
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.detail_url = reverse('contact-detail', args=[1])
        self.contact_list_url = reverse('user-contacts', args=['admin'])

    def test_login(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        # print(response.status_code)
        self.assertTemplateUsed(response, 'users/login.html')






