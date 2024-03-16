from project.views import login_button
from django.urls import reverse
def test_login_working(self):
    data = {'mail': 'test@example.com', 'password': 'Aa123'}
    request = self.factory.post(reverse('login_button'), data)
    response = login_button(request)
    self.assertEqual(response.status_code, 200)