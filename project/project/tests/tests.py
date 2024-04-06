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
        # setUp() initializes an instance variable self.factory with an instance of Django's RequestFactory class.
        # This is a utility provided by Django for creating mock requests in tests. By doing this in the setUp() method,
        # every test method within the test case will have access to the self.factory instance for creating
        # mock requests without duplicating this setup code in each test method.
        self.factory = RequestFactory()

    @patch('project.views.messages.success')  # -tests submit function
    def test_submit_working(self, mock_success):
        # we enter a name and a password as data
        data = {'mail': "test@example.com", 'password': "Aa123"}
        # .post() is a method inside self factory that simulates a POST request.
        # reverse('submit'): retrieves the URL associated with the name 'submit' like a normal request would.
        request = self.factory.post(reverse('submit'), data)
        # we send the request to the into the submit function, it returns as a code and references it with response
        response = submit(request)
        # the unit test checks if the response variable is code 302 which is the code we want
        # code 302 means a redirect response which is what our function does if the registration was successful
        self.assertEqual(response.status_code, 302)

    @patch('project.views.messages.error')  # -tests login button function
    def test_login_button_not_working(self, mock_error):
        # we enter a name and a password as data, this user does not exist in the db
        data = {'mail': 'test@example.com', 'password': 'Aa123'}
        # .post() is a method inside self factory that simulates a POST request.
        # reverse('login'): retrieves the URL associated with the name 'submit' like a normal request would.
        request = self.factory.post(reverse('login_button'), data)
        # we send the request to the into the submit function, it returns as a code and references it with response
        response = login_button(request)
        # this line is used to see if we have reached the fail message in the function
        mock_error.assert_called_once_with(request, 'Invalid credentials. Please try again.')
        # the function returns code 200 id login was unsuccessful which is what the inittest checks
        self.assertEqual(response.status_code, 200)


    @patch('project.views.getIdByUserCredentials') # -tests login button function
    def test_login_button_working(self, mock_get_id):
        # Mock the getIdByUserCredentials function to return an integer user ID
        mock_get_id.return_value = 123  # Assuming 123 is the user ID
        # .post() is a method inside self factory that simulates a POST request.
        # reverse('login_button'): retrieves the URL associated with the name 'submit' like a normal request would.
        request = self.factory.post(reverse('login_button'))
        # Initialize an empty session dictionary
        request.session = {}
        # Creates a SessionMiddleware instance. This middleware is responsible for managing sessions in Django.
        middleware = SessionMiddleware(get_response=BaseHandler().get_response)
        # Processes the request through the session middleware.
        middleware.process_request(request)
        #  Saves the session.
        request.session.save()
        # Creates a dictionary containing login credentials for a user.
        # this is a special user we created and attempt to login to, its a real user in our db
        data = {'mail': 'user@unittest.com', 'password': 'Aa123'}
        # Assigns the data dictionary to the POST attribute of the request object, simulating form data submission.
        request.POST = data
        #  Calls the login_button view function with the prepared request object.
        response = login_button(request)
        # Assert that the response redirects to the homepage (status code 302)
        self.assertEqual(response.status_code, 302)
        # Asserts that the URL the user is redirected to is the homepage.
        self.assertEqual(response.url, reverse('homepage'))



    @patch('project.views.User.objects.get')  # -tests save profile changes function
    def test_save_profile_changes_success(self, mock_user_get):
        # Mocking the user object returned by User.objects.get which has
        # the structure of a User model instance.
        mock_user = MagicMock(spec=User)
        mock_user.name = 'John'
        mock_user.age = 30
        mock_user.mail = 'john@example.com'
        mock_user.description = 'Test description'
        mock_user_get.return_value = mock_user
        # Setting attributes of the mock user object to simulate a user retrieved from the database.
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

    @patch('login.models.User.objects')
    def test_get_average_rating(self, mock_user_objects):
        # Mocking User.objects.exclude().values_list() to return some ratings
        mock_user_objects.exclude().values_list.return_value = [2, 3, 5]

        # Call the view function
        response = get_average_rating()

        # Assert that the response is a JsonResponse object
        self.assertIsInstance(response, JsonResponse)

        # Check if the JsonResponse contains the correct average rating
        data = response.content.decode('utf-8')
        self.assertEqual(data, '{"average_rating": 3.3333333333333335}')

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