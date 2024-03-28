from django.test import RequestFactory, TestCase
from django.urls import reverse
from login.models import User
from project.views import submit
from project.views import login_button
from project.views import getIdByUserCredentials
from project.views import login_page
from project.views import addtoaarr
from project.views import removefromarr
from project.views import register
from project.views import is_not_allowed_email
from project.views import delete_account
from django.contrib.auth import authenticate
import json
from posts.models import Post
from django.http import HttpRequest
from login.forms import RegistrationForm
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock


class TestSite(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='Aa123')

    @patch('project.views.messages.success')  # -tests submit function
    def test_submit_working(self, mock_success):
        data = {'mail': "test@example.com", 'password': "Aa123"}
        request = self.factory.post(reverse('submit'), data)
        response = submit(request)
        self.assertEqual(response.status_code, 302)

    @patch('project.views.messages.error')  # -tests login button function
    def test_login_button_not_working(self, mock_error):
        data = {'mail': 'test@example.com', 'password': 'Aa123'}
        request = self.factory.post(reverse('login_button'), data)
        response = login_button(request)
        self.assertEqual(response.status_code, 200)

    @patch('project.views.User.objects.get')  # -tests save profile changes function
    def test_save_profile_changes_success(self, mock_user_get):
        # Mocking the user object returned by User.objects.get
        mock_user = MagicMock(spec=User)
        mock_user.name = 'John'
        mock_user.age = 30
        mock_user.mail = 'john@example.com'
        mock_user.description = 'Test description'
        mock_user_get.return_value = mock_user

        data = {'name': 'John Doe', 'age': 35, 'mail': 'johndoe@example.com', 'description': 'New description'}
        session = self.client.session
        session['global_user_id'] = 1
        session.save()

        # Making a POST request to the view function
        response = self.client.post(reverse('save_profile_changes'), data)

        # Asserting the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"message": "Profile changes saved successfully"}')

    def test_login_page(self):  # -tests login page function
        request = self.factory.get(reverse('login_page'))
        response = login_page(request)
        self.assertEqual(response.status_code, 200)

    def test_user_does_not_exists(self):  # -tests getIdByUserCredentials function
        mail = 'test@example.com'
        password = 'Aa123'
        result = getIdByUserCredentials(mail, password)
        self.assertEqual(result, 'user does not exist')

    def test_addtoaarr(self):  # -tests addtoarr function
        arr = [1, 2, 3]
        addtoaarr(arr, 4)
        self.assertEqual(arr, [1, 2, 3, 4])  # Test if 4 is added to the array

    def test_removefromarr(self):  # -tests removefromarr function
        arr = [1, 2, 3, 4]
        removefromarr(arr, 3)
        self.assertEqual(arr, [1, 2, 4])  # Test if 3 is removed from the array

    def test_register_view(self):
        # Create a request object
        request = HttpRequest()

        # Call the register view function
        response = register(request)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)


    def test_helppage_view(self):
        response = self.client.get(reverse('helppage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'helppage.html')

    def test_TOS_view(self):
        response = self.client.get(reverse('TOS'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'TOS.html')

    def test_create_post_view(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')

    def test_rating_view(self):
        response = self.client.get(reverse('rating'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rating.html')

    def test_email_not_allowed(self):
        # Test when the email is in the not allowed list
        not_allowed_emails = ['bademail@example.com', '3124@e444.com', 'undesirable@example.com']
        for email in not_allowed_emails:
            self.assertTrue(is_not_allowed_email(email))


    def test_delete_account_with_invalid_session(self):
        # Create a mock POST request
        request = self.factory.post(reverse('delete_account'))

        # Set the session data to simulate invalid session
        request.session = {}

        # Call the view function
        response = delete_account(request)

        # Check if the response contains the expected error message and status code
        self.assertEqual(response.status_code, 401)
        content = json.loads(response.content)
        self.assertEqual(content, {'error': 'User not logged in'})