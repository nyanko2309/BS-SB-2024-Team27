from django.test import RequestFactory, TestCase
from django.urls import reverse
from .views import submit
from project.views import login_button
from django.test import Client
from login.models import User
from django.http import JsonResponse
from posts.models import Post
from django.contrib import messages
from login.models import User
from django.http import JsonResponse
from posts.models import Post
from django.shortcuts import render, redirect
from login.forms import RegistrationForm


class TestSite(TestCase):

    def setUp(self):
        self.factory = RequestFactory()


    def test_register_working(self):
        data = {'mail': "test@example.com", 'password': "Aa123"}
        request = self.factory.post(reverse('submit'), data)
        response = submit(request)
        self.assertEqual(response.status_code, 302)


    def test_login_working(self):
        data = {'mail': 'test@example.com', 'password': 'Aa123'}
        request = self.factory.post(reverse('login_button'), data)
        response = login_button(request)
        self.assertEqual(response.status_code, 200)