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
from project.views import get_average_rating
from project.views import delete_account
from project.views import rate_site
from project.views import submit_rating
from django.contrib.auth import authenticate
import json
from posts.models import Post
from django.http import HttpRequest
from login.forms import RegistrationForm
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.handlers.base import BaseHandler
from django.contrib.messages.storage.fallback import FallbackStorage


class TestSite(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

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
        mock_error.assert_called_once_with(request, 'Invalid credentials. Please try again.')
        self.assertEqual(response.status_code, 200)


    @patch('project.views.getIdByUserCredentials') # -tests login button function
    def test_login_button_working(self, mock_get_id):
        # Mock the getIdByUserCredentials function to return an integer user ID
        mock_get_id.return_value = 123  # Assuming 123 is the user ID

        # Create a request with session support
        request = self.factory.post(reverse('login_button'))
        request.session = {}  # Initialize an empty session dictionary

        # Create a SessionMiddleware instance with the get_response parameter
        middleware = SessionMiddleware(get_response=BaseHandler().get_response)
        middleware.process_request(request)
        request.session.save()

        data = {'mail': 'user@unittest.com', 'password': 'Aa123'}
        request.POST = data

        response = login_button(request)

        # Assert that the response redirects to the homepage (status code 302)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('homepage'))



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

    @patch('project.views.User.objects.exclude')
    def test_get_average_rating(self, mock_exclude):
        # Mock the values_list method to return sample ratings
        mock_exclude.return_value.values_list.return_value = [3, 4, 5]

        # Create a mock GET request
        request = self.factory.get('/get_average_rating')

        # Call the view function
        response = get_average_rating()

        # Check if the response is a JSON response
        self.assertIsInstance(response, JsonResponse)

        # Parse the content of the response as JSON
        content = response.content.decode('utf-8')
        data = json.loads(content)

        # Check if the JSON response contains the correct average rating
        expected_average_rating = (3 + 4 + 5) / 3
        self.assertEqual(data['average_rating'], expected_average_rating)

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

    @patch('project.views.get_average_rating')
    @patch('project.views.User.objects.get')
    def test_rate_site_authenticated_user(self, mock_get_user, mock_get_average_rating):
        # Mock the user object
        user_id = 1  # Assuming user ID 1
        mock_user = MagicMock(spec=User)
        mock_user.site_rating = 4.5  # Assuming site rating is 4.5 for the user
        mock_get_user.return_value = mock_user

        # Create a mock session object
        session = {}
        session['global_user_id'] = user_id

        # Create a request with the session
        request = self.factory.get(reverse('rating'))
        request.session = session

        # Mock the return value of get_average_rating function
        mock_get_average_rating.return_value = 4.5

        # Call the view function
        response = rate_site(request)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)


    @patch('project.views.User.objects.get')
    def test_submit_rating_authenticated_user(self, mock_get_user):
        # Mock the user object
        user_id = 1  # Assuming user ID 1
        mock_user = MagicMock(spec=User)
        mock_get_user.return_value = mock_user

        # Create a mock session object
        session = {}
        session['global_user_id'] = user_id
        # Create a request with session support
        request = self.factory.get(reverse('submit_rating', kwargs={'rating': 4}))  # Adjust the rating value as needed
        request.session = {'global_user_id': 1}  # Assuming user ID 1 is authenticated

        # Call the view function
        response = submit_rating(request, rating=4)

        # Assert the response status code or any other expected behavior
        self.assertEqual(response.status_code, 302)  # Assuming the view redirects after successful rating submission