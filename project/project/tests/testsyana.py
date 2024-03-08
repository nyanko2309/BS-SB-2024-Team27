from django.test import TestCase
from django.urls import reverse
from django.test import Client

class TestProfilePage(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Log in a user
        self.client.login(email='test@example.com', password='password123')

    def test_profile_page_empty_fields(self):
        # Make a GET request to the profile page
        response = self.client.get(reverse('profile'))

        # Check if the empty fields are not present in the rendered HTML content
        self.assertNotContains(response,
                               '<input type="text" id="name" name="name" value="" readonly onclick="enableEdit(this)">')
        self.assertNotContains(response,
                               '<input type="text" id="age" name="age" value="" readonly onclick="enableEdit(this)">')
        self.assertNotContains(response,
                               '<input type="text" id="mail" name="mail" value="" readonly onclick="enableEdit(this)">')
        self.assertNotContains(response,
                               '<input type="text" id="description" name="description" value="" readonly onclick="enableEdit(this)">')
