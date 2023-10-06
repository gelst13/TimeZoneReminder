from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import ContactCreateView, ContactDetailView


class TestUrls(SimpleTestCase):
    def test_ContactCreateView_url_is_resolved(self):
        url = reverse('contact-add')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ContactCreateView)

    def test_contact_detail_url_is_resolved(self):
        url = reverse('contact-detail', args=[1])  # or args=[1]
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ContactDetailView)
