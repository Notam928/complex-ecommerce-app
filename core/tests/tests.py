from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse

from core import views

class HomePageTests(SimpleTestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get(reverse("core:index"))
        self.assertEquals(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("core:index"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        

    
        