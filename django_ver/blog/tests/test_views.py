import json
from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import Post


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.post_detail_url = reverse('post-detail', args=[1])
        self.post_list_url = reverse('blog-home')

    # def test_post_detail_GET(self):
    #     response = self.client.get(self.post_detail_url)
    #     print(self.post_detail_url)
    #     print(response.status_code)
    #     print(response)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_list_GET(self):
        response = self.client.get(self.post_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog.html')

